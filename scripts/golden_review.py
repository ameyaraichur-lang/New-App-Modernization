"""Human spot-check of the tool-derived golden facts.

    python scripts/golden_review.py            # review the 10 % sample interactively
    python scripts/golden_review.py --list     # print the sample without prompting
    python scripts/golden_review.py --status   # how much of the sample is reviewed

The sample is fixed (hash of repo + fact id) and stratified by fact type, so the same facts
come up every time and every type is represented. For each fact the source lines are shown;
answer  y = label is right,  n = label is wrong (fact dropped),  c = correct the value,
s = skip,  q = save and quit. Verdicts go to evals/golden/review.json, which the eval applies.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from appmod.evals.golden import FACTS_DIR, REVIEW  # noqa: E402

RATE = 0.10


def sample() -> list[dict[str, Any]]:
    by_type: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for path in sorted(FACTS_DIR.glob("*.json")):
        doc = json.loads(path.read_text())
        for f in doc["facts"]:
            by_type[f["type"]].append({"repo": doc["repo"], **f, "id": f"{f['type']}:{f['key']}"})
    picked = []
    for facts in by_type.values():
        facts.sort(key=lambda f: hashlib.sha1(f"{f['repo']}|{f['id']}".encode()).hexdigest())
        picked += facts[:max(1, round(len(facts) * RATE))]
    return sorted(picked, key=lambda f: (f["repo"], f["id"]))


def source_lines(corpus: Path, f: dict[str, Any], context: int = 2) -> str:
    rel, _, line = str(f["source"]).partition(":")
    path = corpus / f["repo"] / rel
    if not path.is_file():
        return f"    ({f['source']}){'  ' + f['snippet'] if f.get('snippet') else ''}"
    lines = path.read_text(errors="ignore").splitlines()
    n = int(line) if line.isdigit() else 1
    lo, hi = max(1, n - context), min(len(lines), n + context)
    return "\n".join(f"    {i:>5}{'>' if i == n else ' '} {lines[i - 1][:160]}" for i in range(lo, hi + 1))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", type=Path, default=Path(os.environ.get("APPMOD_CORPUS", ROOT.parent / "corpus")))
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--status", action="store_true")
    args = ap.parse_args()
    facts = sample()
    review: dict[str, dict[str, Any]] = json.loads(REVIEW.read_text()) if REVIEW.exists() else {}
    done = [f for f in facts if f["id"] in review.get(f["repo"], {})]
    if args.status:
        verdicts = [review[f["repo"]][f["id"]]["verdict"] for f in done]
        print(f"sample {len(facts)} facts; reviewed {len(done)}; "
              f"accepted {verdicts.count('accept')}, corrected {verdicts.count('correct')}, "
              f"rejected {verdicts.count('reject')}")
        return 0
    for i, f in enumerate(facts, 1):
        if not args.list and f["id"] in review.get(f["repo"], {}):
            continue
        print(f"\n[{i}/{len(facts)}] {f['repo']} — {f['type']} = {f['expected']!r}   key: {f['key']}")
        print(source_lines(args.dir, f))
        if args.list:
            continue
        while True:
            a = input("  y / n / c / s / q > ").strip().lower()
            if a in ("y", "n", "s", "q", "c"):
                break
        if a == "q":
            break
        if a == "s":
            continue
        entry: dict[str, Any] = {"verdict": {"y": "accept", "n": "reject", "c": "correct"}[a]}
        if a == "c":
            raw = input("  correct value (JSON, e.g. true / \"java 17\") > ").strip()
            try:
                entry["value"] = json.loads(raw)
            except ValueError:
                entry["value"] = raw
        review.setdefault(f["repo"], {})[f["id"]] = entry
        REVIEW.write_text(json.dumps(review, indent=1, sort_keys=True) + "\n")
    if not args.list:
        print(f"\nsaved {REVIEW.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
