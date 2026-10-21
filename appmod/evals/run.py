"""Release-gate eval of a finished run, from persisted state only (store + run DB + repos).

Step 33 gate (unchanged):
  schema_valid_after_repair  >= 95 %  every P1–P4 agent artifact passes ContractValidator
  evidence_resolvability     >= 90 %  ids cited by LLM findings resolve to a recorded tool result
                                      (TOOL_CALL event), an existing artifact version, or a seed finding
  hallucinated_paths/symbols == 0     file paths in P1 output and in OBSERVED/DOCUMENTED claims exist
                                      in the repo; A9 `function` names exist in the source
Also reported: golden-fact agreement per fact type (appmod.evals.golden), variation across apps, stability
(appmod.evals.stability, when a report is given), and the confidence score
(appmod.evals.confidence) with every component at its 95 % lower bound.
"""

from __future__ import annotations

import copy
import json
import re
import sqlite3
from collections import Counter
from pathlib import Path
from typing import Any

from appmod.agents.grounding import (RepoIndex, check_function_names, grounded_claims,
                                     path_tokens, walk)
from appmod.contracts.schemas import ContractValidator
from appmod.evals.calibration import summarize
from appmod.evals.confidence import Component, Measure, score
from appmod.evals.golden import confidence_pairs, score_app
from appmod.evals.golden import load as load_facts
from appmod.registry.compiler import resolve_registry
from appmod.store.artifact_store import ArtifactStore

ROOT = Path(__file__).resolve().parents[2]
SPLITS = {r["name"]: r["split"] for r in json.loads((ROOT / "evals" / "corpus.json").read_text())["repos"]}
THRESHOLDS = {"schema_valid_after_repair": 95.0, "evidence_resolvability": 90.0}
SCRIPTED_ACTORS = ("scripted-",)


def _pct(n: int, d: int) -> float:
    return round(100.0 * n / d, 2) if d else 100.0


def evaluate(runs_dir: Path, job: str, stability: dict[str, Any] | None = None) -> dict[str, Any]:
    db = sqlite3.connect(runs_dir / "appmod.db")
    state = json.loads(db.execute("SELECT state FROM jobs WHERE job_id=?", (job,)).fetchone()[0])
    store = ArtifactStore(Path(state["facts"]["store_path"]))
    apps: list[str] = state["apps"]
    roots = {a: Path(p) for a, p in (state.get("facts", {}).get("repo_paths") or {}).items()}
    if not roots:
        roots = {a: ROOT.parent / "corpus" / a for a in apps}
    recorded = {r[0] for r in db.execute(
        "SELECT json_extract(data,'$.evidence_id') FROM events WHERE job_id=? AND kind='TOOL_CALL'",
        (job,)) if r[0]}
    reg = resolve_registry()["phases"]
    validators = {p: ContractValidator(reg[p]) for p in (1, 2, 3, 4)}
    repos = {a: RepoIndex.of(roots[a]) for a in apps}

    total = valid = 0
    cited = resolved = 0
    unresolved: list[dict[str, str]] = []
    bad_paths: list[dict[str, str]] = []
    bad_symbols: list[dict[str, str]] = []
    checked_paths = checked_symbols = 0
    for phase in (1, 2, 3, 4):
        for app in (["PF1"] if phase == 2 else apps):
            for agent in reg[phase]["agents"]:
                aid = f"P{phase}/{app}/{agent['local_id']}"
                try:
                    art = store.get(aid)
                except Exception:
                    continue
                total += 1
                valid += not validators[phase].validate(art)
                seeds = {i.get("id") for i in walk([art.get("findings", []), art.get("payload", {})])
                         if i.get("origin") != "llm" and i.get("id")}
                for item in walk([art.get("findings", []), art.get("payload", {})]):
                    if item.get("origin") != "llm":
                        continue
                    for eid in item.get("evidence_ids") or []:
                        cited += 1
                        if eid.startswith("ev-"):
                            ok = eid in recorded
                        elif eid.startswith("art:"):
                            m = re.match(r"art:(.+)@v(\d+)$", eid)
                            ok = m is not None and int(m.group(2)) in store.versions(m.group(1))
                        elif eid.startswith("seed:"):
                            ok = eid[5:] in seeds
                        else:
                            ok = False
                        resolved += ok
                        if not ok and len(unresolved) < 40:
                            unresolved.append({"artifact": aid, "id": eid})
                repo = repos.get(app)
                if repo is None:
                    continue
                claims = grounded_claims(art.get("findings", []), art.get("payload", {}), phase)
                for tok in path_tokens(claims):
                    checked_paths += 1
                    if not repo.has_path(tok):
                        bad_paths.append({"artifact": aid, "path": tok})
                if phase == 1 and agent["local_id"] == "A9":
                    payload = copy.deepcopy(art.get("payload", {}))
                    checked_symbols += sum(len([n for n in re.split(r"[;,]", str(i.get("function") or ""))
                                                if n.strip()])
                                           for i in walk(payload) if "function" in i)
                    bad_symbols += [{"artifact": aid, "problem": p} for p in check_function_names(payload, repo)]

    facts: dict[str, list[dict[str, Any]]] = {}
    pairs: dict[str, list[tuple[float, bool]]] = {}
    pair_rows: list[dict[str, Any]] = []
    for app in apps:
        golden = load_facts(app)
        if not golden:
            continue
        arts = {f"A{i}": store.get(f"P1/{app}/A{i}") for i in range(1, 12) if store.versions(f"P1/{app}/A{i}")}
        payloads = {k: a["payload"] for k, a in arts.items()}
        for row in score_app(golden, payloads):
            facts.setdefault(row["type"], []).append({"app": app, **row})
        items = [i for i in walk([[a.get("findings", []), a["payload"]] for a in arts.values()])
                 if i.get("origin") == "llm"]
        for p in confidence_pairs(golden, payloads, items):
            pairs.setdefault(SPLITS.get(app, "unlisted"), []).append((p["confidence"], p["correct"]))
            pair_rows.append({"app": app, **p})

    dispositions: Counter[str] = Counter()
    if store.versions("P2/PF1/A6"):
        dispositions = Counter(d.get("proposed_disposition")
                               for d in store.get("P2/PF1/A6")["payload"].get("decisions", []))
    boundaries = {a: tuple(sorted(str(b.get("boundary")) for b in
                                  store.get(f"P3/{a}/A2")["payload"].get("boundaries", [])))
                  for a in apps if store.versions(f"P3/{a}/A2")}
    reviews = db.execute("SELECT decision, reviewer FROM reviews WHERE job_id=? AND status='DECIDED'",
                         (job,)).fetchall()
    out: dict[str, Any] = {
        "job": job,
        "schema_valid_after_repair": {"pct": _pct(valid, total), "valid": valid, "total": total},
        "evidence_resolvability": {"pct": _pct(resolved, cited), "resolved": resolved, "cited": cited,
                                   "unresolved_sample": unresolved},
        "hallucinated_paths": {"count": len(bad_paths), "checked": checked_paths, "items": bad_paths},
        "hallucinated_symbols": {"count": len(bad_symbols), "checked": checked_symbols, "items": bad_symbols},
        "golden_agreement": {k: {"pct": _pct(sum(r["ok"] for r in v), len(v)), "rows": v}
                             for k, v in facts.items()},
        "calibration": {"facts": summarize(pairs) | {"by_type": _by_type(pair_rows)},
                        "decisions": decision_confidence(store, apps)},
        "variation": {"p2_dispositions": dict(dispositions),
                      "p3_distinct_boundary_sets": len(set(boundaries.values())), "p3_apps": len(boundaries)},
    }
    out["pass"] = (out["schema_valid_after_repair"]["pct"] >= THRESHOLDS["schema_valid_after_repair"]
                   and out["evidence_resolvability"]["pct"] >= THRESHOLDS["evidence_resolvability"]
                   and not bad_paths and not bad_symbols)
    out["confidence"] = score(components(out, reviews, stability))
    return out


def _by_type(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for r in rows:
        t = out.setdefault(r["type"], {"n": 0, "correct": 0, "confidence_sum": 0.0})
        t["n"] += 1
        t["correct"] += r["correct"]
        t["confidence_sum"] += r["confidence"]
    return {k: {"n": v["n"], "accuracy": round(v["correct"] / v["n"], 3),
                "mean_confidence": round(v["confidence_sum"] / v["n"], 3)} for k, v in sorted(out.items())}


DECISIONS = (("P1 A5 capability route review", "P1/{app}/A5", "route_review"),
             ("P1 A11 risk scores", "P1/{app}/A11", "risk_dimensions"),
             ("P2 A6 dispositions", "P2/PF1/A6", "decisions"),
             ("P3 A2 boundaries", "P3/{app}/A2", "boundaries"),
             ("P4 A3 task estimates", "P4/{app}/A3", "tasks"))


def decision_confidence(store: ArtifactStore, apps: list[str]) -> dict[str, dict[str, Any]]:
    """Stated confidence on model-authored decisions. No labels exist for these, so it is uncalibrated."""
    out = {}
    for label, pattern, fld in DECISIONS:
        ids = {pattern.format(app=a) for a in apps}
        stated, missing = [], 0
        for aid in sorted(ids):
            if not store.versions(aid):
                continue
            val = store.get(aid)["payload"].get(fld)
            for it in (val if isinstance(val, list) else [val] if isinstance(val, dict) else []):
                if not isinstance(it, dict) or it.get("origin") != "llm":
                    continue
                c = it.get("confidence")
                if isinstance(c, int | float) and not isinstance(c, bool):
                    stated.append(float(c))
                else:
                    missing += 1
        out[label] = {"n": len(stated), "without_confidence": missing,
                      "mean": round(sum(stated) / len(stated), 3) if stated else None,
                      "min": min(stated, default=None), "max": max(stated, default=None)}
    return out


def components(r: dict[str, Any], reviews: list[tuple[str, str]],
               stability: dict[str, Any] | None = None) -> list[Component]:
    """Map eval results onto C1–C9. Components without data stay unassessed and score 0."""
    sv, ev = r["schema_valid_after_repair"], r["evidence_resolvability"]
    hp, hs = r["hallucinated_paths"], r["hallucinated_symbols"]
    rows = [x for v in r["golden_agreement"].values() for x in v["rows"]]
    human = [d for d, who in reviews if not str(who or "").startswith(SCRIPTED_ACTORS)]
    return [
        Component("C1", [Measure("schema valid after repair", sv["valid"], sv["total"]),
                         Measure("evidence ids resolve", ev["resolved"], ev["cited"]),
                         Measure("cited paths exist", hp["checked"] - hp["count"], hp["checked"]),
                         Measure("A9 function names exist", hs["checked"] - hs["count"], hs["checked"])]),
        Component("C2", [Measure("golden facts agree", sum(x["ok"] for x in rows), len(rows))]),
        Component("C3", reason="claim-support verifier not built (stack PR 6)"),
        Component("C4", reason="no expert decision labels (decision 2: skipped)"),
        Component("C5", [Measure(m["name"], m["k"], m["n"]) for m in (stability or {}).get("measures", [])],
                  reason="" if stability else "no stability report given (scripts/stability_run.py)"),
        _c6(r.get("calibration", {}).get("facts", {})),
        Component("C7", reason="P5 runtime differential NOT_RUN; sandbox deferred (decision 1)"),
        Component("C8", reason="adversarial suite not built (stack PR 8)"),
        Component("C9", [Measure("human reviews approved", sum(d == "approve" for d in human), len(human))],
                  reason="" if human else "all reviews were by scripted actors"),
    ]


def _c6(cal: dict[str, Any]) -> Component:
    if not cal.get("n"):
        return Component("C6", reason="no model confidence on facts that golden facts can check")
    return Component("C6", value=max(0.0, 1 - cal["ece_upper95"]),
                     basis=f"1 - ECE at bootstrap 95%: {cal['n']} fact confidences, ECE {cal['ece']}, "
                           f"95th percentile {cal['ece_upper95']}")


def to_md(r: dict[str, Any], label: str) -> str:
    sv, ev = r["schema_valid_after_repair"], r["evidence_resolvability"]
    hp, hs = r["hallucinated_paths"], r["hallucinated_symbols"]
    cs = r["confidence"]
    lines = [f"# Step 33 eval — `{label}` (`{r['job']}`)", "",
             f"**Release gate: {'PASS' if r['pass'] else 'FAIL'}**", "",
             "| metric | value | threshold |", "|---|---|---|",
             f"| schema-valid after repair | {sv['pct']}% ({sv['valid']}/{sv['total']}) | ≥ 95% |",
             f"| evidence resolvability | {ev['pct']}% ({ev['resolved']}/{ev['cited']}) | ≥ 90% |",
             f"| hallucinated paths | {hp['count']} of {hp['checked']} checked | = 0 |",
             f"| hallucinated symbols (A9 functions) | {hs['count']} of {hs['checked']} checked | = 0 |",
             "", "## Confidence score", "",
             f"**{cs['confidence_score']}%** — weakest component {cs['weakest']}; "
             f"{len(cs['not_assessed'])} of 9 components not assessed (each counts as 0). "
             "Every value is a 95% Wilson lower bound.", "",
             "| component | lower bound | basis |", "|---|---|---|"]
    for c in cs["components"]:
        if c["assessed"] and c.get("basis"):
            lines.append(f"| {c['id']} {c['name']} | {c['lower_bound']}% | {c['basis']} |")
        elif c["assessed"]:
            basis = "; ".join(f"{m['name']} {m['k']}/{m['n']} (LB {m['lower_bound']}%)"
                              for m in c["measures"] if m["n"])
            lines.append(f"| {c['id']} {c['name']} | {c['lower_bound']}% | {basis} |")
        else:
            lines.append(f"| {c['id']} {c['name']} | not assessed | {c['reason']} |")
    rows = [x for v in r["golden_agreement"].values() for x in v["rows"]]
    reviewed = sum(1 for x in rows if x.get("review"))
    lines += ["", "## Agreement with golden facts (`evals/golden/facts/`)", "",
              f"{len(rows)} tool-derived facts over {len({x['app'] for x in rows})} repos; "
              f"{reviewed} human-reviewed.", "",
              "| fact type | agreement | n | misses (first 5) |", "|---|---|---|---|"]
    for k, v in sorted(r["golden_agreement"].items()):
        misses = [x for x in v["rows"] if not x["ok"]]
        miss = ", ".join(f"{x['app']} {x['key']} (got {x['got']}, want {x['expected']})" for x in misses[:5])
        lines.append(f"| {k} | {v['pct']}% | {len(v['rows'])} | {miss or '—'} |")
    lines += _calibration_md(r.get("calibration", {}))
    var = r["variation"]
    lines += ["", "## Variation with evidence", "",
              f"- P2 dispositions: {var['p2_dispositions']}",
              f"- P3 decomposition: {var['p3_distinct_boundary_sets']} distinct boundary sets across "
              f"{var['p3_apps']} apps"]
    for name, key, fld in (("Unresolved evidence ids (sample)", "evidence_resolvability", "unresolved_sample"),
                           ("Hallucinated paths", "hallucinated_paths", "items"),
                           ("Hallucinated symbols", "hallucinated_symbols", "items")):
        items = r[key][fld]
        if items:
            lines += ["", f"## {name}", ""] + [f"- `{json.dumps(i)}`" for i in items[:40]]
    return "\n".join(lines) + "\n"


def _calibration_md(cal: dict[str, Any]) -> list[str]:
    facts, decisions = cal.get("facts", {}), cal.get("decisions", {})
    lines = ["", "## Calibration of model confidence", ""]
    if facts.get("n"):
        lines += [f"{facts['n']} fact confidences checked against golden facts: ECE {facts['ece']} "
                  f"(bootstrap 95th percentile {facts['ece_upper95']}). Only facts a model item states are "
                  "checkable, so wrong items that contradict a tool fact are not counted yet.", "",
                  "| confidence | n | mean confidence | accuracy |", "|---|---|---|---|"]
        lines += [f"| {b['bin']} | {b['n']} | {b['mean_confidence']} | {b['accuracy']} |" for b in facts["reliability"]]
        lines += ["", "| fact type | n | mean confidence | accuracy |", "|---|---|---|---|"]
        lines += [f"| {t} | {v['n']} | {v['mean_confidence']} | {v['accuracy']} |" for t, v in facts["by_type"].items()]
        if "holdout" in facts:
            h = facts["holdout"]
            lines += ["", f"Map fitted on tune repos, applied to {h['n']} held-out confidences: "
                          f"ECE {h['ece_raw']} raw, {h['ece_mapped']} mapped."]
    else:
        lines.append("No model confidences on checkable facts in this run.")
    lines += ["", "Decision confidence (uncalibrated: no labels exist for these decisions):", "",
              "| decision | n | mean | min | max | items without confidence |", "|---|---|---|---|---|---|"]
    lines += [f"| {k} | {v['n']} | {v['mean']} | {v['min']} | {v['max']} | {v['without_confidence']} |"
              for k, v in decisions.items()]
    return lines
