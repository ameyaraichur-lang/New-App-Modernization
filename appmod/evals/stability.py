"""Stability of agent decisions across repeated live runs of one pipeline version (C5).

A replicate is one or more finished jobs that together cover the corpus (the server takes at
most 25 repos per run). For every app seen in at least two replicates:

  P1 A5 capability route   identical in every replicate
  P2 A6 disposition        identical in every replicate
  P3 A2 boundary set       mean pairwise Jaccard >= 0.8
  P1 A11 risk score        per dimension, max - min <= 1 on the 1-5 scale

Each app (or app x risk dimension) is one trial; C5 takes the 95 % lower bound of each measure.
Decisions whose modal value holds in fewer than 80 % of replicates are listed.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
import subprocess
from collections import Counter
from itertools import combinations
from pathlib import Path
from typing import Any

from appmod.evals.confidence import Measure
from appmod.store.artifact_store import ArtifactStore

ROOT = Path(__file__).resolve().parents[2]
PIPELINE_PATHS = ("appmod", "data", "uv.lock")
NOT_PIPELINE = ("appmod/evals",)
JACCARD_MIN = 0.8
RISK_SPREAD_MAX = 1
FLAG_BELOW = 0.8
CATEGORICAL = {"route": "P1 A5 capability route", "disposition": "P2 A6 disposition"}


def pipeline_version(ref: str = "HEAD", root: Path = ROOT) -> str:
    """Hash of the git trees that decide agent behaviour (code, prompts, registry, data, locked deps)."""
    def git(*args: str) -> str:
        return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=True).stdout

    entries = [line for line in git("ls-tree", "-r", ref, "--", *PIPELINE_PATHS).splitlines()
               if not line.split("\t", 1)[1].startswith(NOT_PIPELINE)]
    version = hashlib.sha256("\n".join(entries).encode()).hexdigest()[:12]
    if ref == "HEAD" and git("status", "--porcelain", "--", *PIPELINE_PATHS, *(f":!{p}" for p in NOT_PIPELINE)):
        version += "+dirty"
    return version


def snapshot(runs_dir: Path, job: str) -> dict[str, dict[str, Any]]:
    """The stability-relevant decisions of one finished job, per app."""
    db = sqlite3.connect(runs_dir / "appmod.db")
    row = db.execute("SELECT state FROM jobs WHERE job_id=?", (job,)).fetchone()
    if row is None:
        raise KeyError(f"{job} not in {runs_dir}")
    state = json.loads(row[0])
    store = ArtifactStore(Path(state["facts"]["store_path"]))

    def payload(aid: str) -> dict[str, Any] | None:
        return store.get(aid)["payload"] if store.versions(aid) else None

    p2 = payload("P2/PF1/A6") or {}
    dispositions = {d.get("application_id"): d.get("proposed_disposition") for d in p2.get("decisions", [])}
    out: dict[str, dict[str, Any]] = {}
    for app in state["apps"]:
        a5, a11, p3 = payload(f"P1/{app}/A5"), payload(f"P1/{app}/A11"), payload(f"P3/{app}/A2")
        out[app] = {
            "route": a5.get("capability_route") if a5 else None,
            "disposition": dispositions.get(app),
            "boundaries": sorted({str(b.get("boundary")) for b in p3.get("boundaries", [])}) if p3 else None,
            "risk": {str(d.get("dimension")): d.get("score") for d in (a11 or {}).get("risk_dimensions", [])
                     if isinstance(d.get("score"), int | float)},
        }
    return out


def merge(snaps: list[dict[str, dict[str, Any]]]) -> dict[str, dict[str, Any]]:
    """One replicate from several jobs (e.g. the tune and holdout halves of a corpus run)."""
    out: dict[str, dict[str, Any]] = {}
    for s in snaps:
        overlap = set(out) & set(s)
        if overlap:
            raise ValueError(f"apps appear twice in one replicate: {sorted(overlap)}")
        out.update(s)
    return out


def _jaccard(a: list[str], b: list[str]) -> float:
    sa, sb = set(a), set(b)
    return len(sa & sb) / len(sa | sb) if sa | sb else 1.0


def compare(replicates: list[dict[str, dict[str, Any]]]) -> dict[str, Any]:
    apps = sorted(a for a in {a for r in replicates for a in r} if sum(a in r for r in replicates) >= 2)
    per_app: dict[str, dict[str, Any]] = {}
    flagged: list[dict[str, Any]] = []
    risk_pairs = risk_stable = 0
    for app in apps:
        runs = [r[app] for r in replicates if app in r]
        row: dict[str, Any] = {"runs": len(runs)}
        for key, label in CATEGORICAL.items():
            values = [r[key] for r in runs if r[key] is not None]
            if len(values) < 2:
                continue
            mode, count = Counter(values).most_common(1)[0]
            row[key] = {"values": values, "modal": mode, "share": round(count / len(values), 3),
                        "identical": count == len(values)}
            if count / len(values) < FLAG_BELOW:
                flagged.append({"agent": label, "app": app, "values": values})
        sets = [r["boundaries"] for r in runs if r["boundaries"] is not None]
        if len(sets) >= 2:
            j = sum(_jaccard(a, b) for a, b in combinations(sets, 2)) / (len(sets) * (len(sets) - 1) / 2)
            row["boundaries"] = {"mean_jaccard": round(j, 3), "stable": j >= JACCARD_MIN}
            if j < FLAG_BELOW:
                flagged.append({"agent": "P3 A2 boundaries", "app": app, "values": sets})
        spreads = {}
        for dim in sorted({d for r in runs for d in r["risk"]}):
            scores = [r["risk"][dim] for r in runs if dim in r["risk"]]
            if len(scores) >= 2:
                spreads[dim] = max(scores) - min(scores)
                risk_pairs += 1
                risk_stable += spreads[dim] <= RISK_SPREAD_MAX
                if spreads[dim] > RISK_SPREAD_MAX:
                    flagged.append({"agent": "P1 A11 risk score", "app": app, "dimension": dim, "values": scores})
        row["risk_spread"] = spreads
        per_app[app] = row

    def tally(key: str, ok: str) -> tuple[int, int]:
        rows = [r[key] for r in per_app.values() if key in r]
        return sum(bool(r[ok]) for r in rows), len(rows)

    measures = [Measure(f"{CATEGORICAL['route']} identical across runs", *tally("route", "identical")),
                Measure(f"{CATEGORICAL['disposition']} identical across runs", *tally("disposition", "identical")),
                Measure(f"P3 A2 boundary Jaccard >= {JACCARD_MIN}", *tally("boundaries", "stable")),
                Measure(f"P1 A11 risk score spread <= {RISK_SPREAD_MAX}", risk_stable, risk_pairs)]
    agents = {}
    for key, label in CATEGORICAL.items():
        shares = [r[key]["share"] for r in per_app.values() if key in r]
        if shares:
            agents[label] = round(sum(shares) / len(shares), 3)
    return {"replicates": len(replicates), "apps": apps, "per_app": per_app, "flagged": flagged,
            "agent_agreement": agents,
            "measures": [{"name": m.name, "k": m.k, "n": m.n, "lower_bound": m.lower} for m in measures]}


def to_md(r: dict[str, Any], label: str) -> str:
    lines = [f"# Stability — `{label}`", "",
             f"{r['replicates']} replicates; {len(r['apps'])} apps seen in at least two. "
             f"Pipeline version(s): {', '.join(f'`{v}`' for v in r.get('pipeline_versions', [])) or 'unrecorded'}.",
             "", "| measure | stable | n | 95% lower bound |", "|---|---|---|---|"]
    lines += [f"| {m['name']} | {m['k']} | {m['n']} | {m['lower_bound'] if m['n'] else '—'}% |" for m in r["measures"]]
    lines += ["", "## Mean agreement with the modal decision, per agent", "",
              "| agent | agreement | below 80%? |", "|---|---|---|"]
    lines += [f"| {a} | {round(100 * s, 1)}% | {'yes' if s < FLAG_BELOW else 'no'} |"
              for a, s in r["agent_agreement"].items()]
    lines += ["", "## Decisions that changed between runs", ""]
    lines += [f"- {f['agent']} — {f['app']}{' / ' + f['dimension'] if 'dimension' in f else ''}: "
              f"{' → '.join(str(v) for v in f['values'])}" for f in r["flagged"]] or ["None."]
    lines += ["", "## Per app", "", "| app | runs | route | disposition | boundary Jaccard | max risk spread |",
              "|---|---|---|---|---|---|"]
    for app, row in r["per_app"].items():
        def cat(key: str) -> str:
            return f"{row[key]['modal']} ({round(100 * row[key]['share'])}%)" if key in row else "—"
        b = row.get("boundaries", {}).get("mean_jaccard", "—")
        lines.append(f"| {app} | {row['runs']} | {cat('route')} | {cat('disposition')} | {b} | "
                     f"{max(row['risk_spread'].values(), default='—')} |")
    return "\n".join(lines) + "\n"
