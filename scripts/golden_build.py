"""Generate tool-derived golden facts for every corpus repo into evals/golden/facts/<name>.json.

    python scripts/golden_build.py [--only name ...]

Facts are derived from the checkout at its pinned commit (see scripts/corpus_sync.py) and
are reviewed with scripts/golden_review.py; never edit the facts files by hand.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from appmod.evals.golden import FACTS_DIR, derive  # noqa: E402
from appmod.tools.analyzers import _bin  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", type=Path,
                    default=Path(os.environ.get("APPMOD_CORPUS", ROOT.parent / "corpus")))
    ap.add_argument("--only", nargs="*")
    args = ap.parse_args()
    corpus = json.loads((ROOT / "evals" / "corpus.json").read_text())["repos"]
    scc = _bin("scc")
    FACTS_DIR.mkdir(parents=True, exist_ok=True)
    total = 0
    for e in corpus:
        if args.only and e["name"] not in args.only:
            continue
        facts = derive(args.dir / e["name"], scc)
        total += len(facts)
        (FACTS_DIR / f"{e['name']}.json").write_text(json.dumps(
            {"repo": e["name"], "commit": e["commit"], "split": e["split"],
             "facts": [asdict(f) for f in facts]}, indent=1) + "\n")
        print(f"{e['name']:<36} {len(facts):>3} {dict(Counter(f.type for f in facts))}")
    print(f"total facts: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
