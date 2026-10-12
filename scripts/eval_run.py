"""Step 33 eval of a finished run, from persisted state only (store + run DB + repos).

    python scripts/eval_run.py --runs-dir runs/e2e-run3-root --job job-… [--label run3]

Metrics and release thresholds:
  schema_valid_after_repair  >= 95 %  every P1–P4 agent artifact passes ContractValidator
  evidence_resolvability     >= 90 %  ids cited by LLM findings resolve to a recorded tool result
                                      (TOOL_CALL event), an existing artifact version, or a seed finding
  hallucinated_paths/symbols == 0     file paths in P1 output and in OBSERVED/DOCUMENTED claims exist
                                      in the repo; A9 `function` names exist in the source
  golden agreement                    P1 facts vs evals/golden/corpus.json (reported per fact)
  variation                           distinct P2 dispositions / P3 boundary sets across apps
"""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from appmod.contracts.schemas import ContractValidator  # noqa: E402
from appmod.registry.compiler import resolve_registry  # noqa: E402
from appmod.store.artifact_store import ArtifactStore  # noqa: E402

GOLDEN = ROOT / "evals" / "golden" / "corpus.json"
THRESHOLDS = {"schema_valid_after_repair": 95.0, "evidence_resolvability": 90.0}
FILE_EXTS = ("java|kt|groovy|gradle|xml|properties|ya?ml|json|toml|ini|cfg|conf|env|py|rb|php|go|mod|sum|"
             "js|jsx|ts|tsx|mjs|cjs|vue|cs|csproj|sln|props|targets|cshtml|razor|html?|css|scss|less|sql|"
             "sqlite|db|md|txt|rst|lock|sh|ps1|cmd|bat|dockerfile|tf|jsp|blade\\.php|twig|erb|slim|map|log")
PATH_RE = re.compile(rf"(?<![\w/.:-])((?:[\w@.-]+/)+[\w.-]+\.(?:{FILE_EXTS}))(?![\w/])", re.I)
TEXT_SKIP = {".git", "node_modules", "bower_components", "vendor", "dist", "obj", "bin"}
SYMBOL_RE = re.compile(r"^[A-Za-z_$][\w$]*$")


def walk(obj: Any):
    if isinstance(obj, dict):
        yield obj
        for v in obj.values():
            yield from walk(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from walk(v)


def strings(obj: Any):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from strings(v)


class Repo:
    def __init__(self, root: Path):
        self.root = root
        self.files = [p.relative_to(root).as_posix() for p in root.rglob("*")
                      if p.is_file() and ".git" not in p.relative_to(root).parts]
        self.dirs = {str(Path(f).parent.as_posix()) for f in self.files}
        self._text: str | None = None

    def has_path(self, token: str) -> bool:
        """Exists as a file/dir, or is a path the repo itself names (runtime files such as
        ``storage/logs/laravel.log`` or ``./data/gorm.db`` are referenced, not checked in)."""
        t = re.sub(rf"^(\./|{re.escape(self.root.name)}/)", "", token)
        if any(f == t or f.endswith("/" + t) for f in self.files):
            return True
        if any(d == t or d.endswith("/" + t) for d in self.dirs):
            return True
        return t in self.text

    @property
    def text(self) -> str:
        if self._text is None:
            parts = []
            for f in self.files:
                if set(Path(f).parts) & TEXT_SKIP:
                    continue
                p = self.root / f
                if p.stat().st_size < 1_000_000:
                    parts.append(p.read_text("utf-8", "ignore"))
            self._text = "\n".join(parts)
        return self._text

    def has_symbol(self, name: str) -> bool:
        return re.search(rf"\b{re.escape(name)}\b", self.text) is not None


def is_candidate_path(tok: str) -> bool:
    return not (tok.startswith(("http", "www.")) or "://" in tok or tok.count("/") == 0
                or re.match(r"^\d", tok) or tok.endswith((".com", ".org", ".io", ".net")))


def evaluate(runs_dir: Path, job: str) -> dict[str, Any]:
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
    repos = {a: Repo(roots[a]) for a in apps}

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
                seeds = {f.get("id") for f in art.get("findings", []) if f.get("origin") != "llm"}
                for item in walk([art.get("findings", []), art.get("payload", {})]):
                    if item.get("origin") != "llm":
                        continue
                    for eid in item.get("evidence_ids") or []:
                        cited += 1
                        if eid.startswith("ev-"):
                            ok = eid in recorded
                        elif eid.startswith("art:"):
                            m = re.match(r"art:(.+)@v(\d+)$", eid)
                            ok = bool(m) and int(m.group(2)) in store.versions(m.group(1))
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
                claims = [art.get("payload", {})] if phase == 1 else []
                claims += [i for i in walk([art.get("findings", []), art.get("payload", {})])
                           if i.get("evidence_class") in ("OBSERVED", "DOCUMENTED")]
                seen: set[str] = set()
                for s in strings(claims):
                    for tok in PATH_RE.findall(s):
                        if tok in seen or not is_candidate_path(tok):
                            continue
                        seen.add(tok)
                        checked_paths += 1
                        if not repo.has_path(tok):
                            bad_paths.append({"artifact": aid, "path": tok})
                if phase == 1 and agent["local_id"] == "A9":
                    for i in walk(art.get("payload", {})):
                        if "function" not in i:
                            continue
                        for seg in re.split(r"[;,]", str(i.get("function") or "")):
                            seg = re.sub(r"\(.*?\)", "", seg).strip()
                            if not seg:
                                continue
                            name = re.split(r"::|->|#|\.", seg)[-1].strip()
                            checked_symbols += 1
                            if not SYMBOL_RE.match(name):
                                bad_symbols.append({"artifact": aid, "symbol": seg, "why": "not a code name"})
                            elif not repo.has_symbol(name):
                                bad_symbols.append({"artifact": aid, "symbol": seg, "why": "not in source"})

    golden = json.loads(GOLDEN.read_text())["repos"]
    facts: dict[str, list[dict[str, Any]]] = {}
    for app in apps:
        g = golden.get(app)
        if not g:
            continue
        a1 = store.get(f"P1/{app}/A1")["payload"]
        r0 = a1["repositories"][0]
        deps = " ".join(d.get("name", "") for d in a1.get("dependencies", [])).lower()
        dims = {d["dimension"]: d["score"] for d in store.get(f"P1/{app}/A11")["payload"]["risk_dimensions"]}
        pred = {"primary_language": r0.get("primary_language"),
                "framework": g["framework"] if g["framework"] and g["framework"].lower() in deps else None,
                "has_tests": (r0.get("test_files") or 0) > 0,
                "has_data_layer": (dims.get("data") or 1) > 1}
        for k, want in g.items():
            if k == "framework" and want is None:
                continue
            facts.setdefault(k, []).append({"app": app, "expected": want, "got": pred[k],
                                            "ok": pred[k] == want})

    dispositions = Counter(d.get("proposed_disposition")
                           for d in store.get("P2/PF1/A6")["payload"].get("decisions", []))
    boundaries = {a: tuple(sorted(str(b.get("boundary")) for b in
                                  store.get(f"P3/{a}/A2")["payload"].get("boundaries", [])))
                  for a in apps if store.versions(f"P3/{a}/A2")}
    pct = lambda n, d: round(100.0 * n / d, 2) if d else 100.0  # noqa: E731
    out = {
        "job": job,
        "schema_valid_after_repair": {"pct": pct(valid, total), "valid": valid, "total": total},
        "evidence_resolvability": {"pct": pct(resolved, cited), "resolved": resolved, "cited": cited,
                                   "unresolved_sample": unresolved},
        "hallucinated_paths": {"count": len(bad_paths), "checked": checked_paths, "items": bad_paths},
        "hallucinated_symbols": {"count": len(bad_symbols), "checked": checked_symbols, "items": bad_symbols},
        "golden_agreement": {k: {"pct": pct(sum(r["ok"] for r in v), len(v)), "rows": v}
                             for k, v in facts.items()},
        "variation": {"p2_dispositions": dict(dispositions),
                      "p3_distinct_boundary_sets": len(set(boundaries.values())), "p3_apps": len(boundaries)},
    }
    out["pass"] = (out["schema_valid_after_repair"]["pct"] >= THRESHOLDS["schema_valid_after_repair"]
                   and out["evidence_resolvability"]["pct"] >= THRESHOLDS["evidence_resolvability"]
                   and not bad_paths and not bad_symbols)
    return out


def to_md(r: dict[str, Any], label: str) -> str:
    sv, ev = r["schema_valid_after_repair"], r["evidence_resolvability"]
    hp, hs = r["hallucinated_paths"], r["hallucinated_symbols"]
    lines = [f"# Step 33 eval — `{label}` (`{r['job']}`)", "",
             f"**Release gate: {'PASS' if r['pass'] else 'FAIL'}**", "",
             "| metric | value | threshold |", "|---|---|---|",
             f"| schema-valid after repair | {sv['pct']}% ({sv['valid']}/{sv['total']}) | ≥ 95% |",
             f"| evidence resolvability | {ev['pct']}% ({ev['resolved']}/{ev['cited']}) | ≥ 90% |",
             f"| hallucinated paths | {hp['count']} of {hp['checked']} checked | = 0 |",
             f"| hallucinated symbols (A9 functions) | {hs['count']} of {hs['checked']} checked | = 0 |",
             "", "## Agreement with golden labels (`evals/golden/corpus.json`)", "",
             "| fact | agreement | misses |", "|---|---|---|"]
    for k, v in r["golden_agreement"].items():
        miss = ", ".join(f"{x['app']} (got {x['got']}, want {x['expected']})" for x in v["rows"] if not x["ok"])
        lines.append(f"| {k} | {v['pct']}% | {miss or '—'} |")
    var = r["variation"]
    lines += ["", "## Variation with evidence", "",
              f"- P2 dispositions: {var['p2_dispositions']}",
              f"- P3 decomposition: {var['p3_distinct_boundary_sets']} distinct boundary sets across "
              f"{var['p3_apps']} apps"]
    for name, key, field in (("Unresolved evidence ids (sample)", "evidence_resolvability", "unresolved_sample"),
                             ("Hallucinated paths", "hallucinated_paths", "items"),
                             ("Hallucinated symbols", "hallucinated_symbols", "items")):
        items = r[key][field]
        if items:
            lines += ["", f"## {name}", ""] + [f"- `{json.dumps(i)}`" for i in items[:40]]
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs-dir", type=Path, required=True)
    ap.add_argument("--job", required=True)
    ap.add_argument("--label", default="eval")
    args = ap.parse_args()
    r = evaluate(args.runs_dir, args.job)
    out = ROOT / "docs" / "runs"
    (out / f"eval-{args.label}.json").write_text(json.dumps(r, indent=1))
    (out / f"eval-{args.label}.md").write_text(to_md(r, args.label))
    print(to_md(r, args.label))
    return 0 if r["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
