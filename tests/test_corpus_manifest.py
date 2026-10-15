import json
import re
from collections import defaultdict
from pathlib import Path

MANIFEST = Path(__file__).resolve().parents[1] / "evals" / "corpus.json"


def _repos():
    return json.loads(MANIFEST.read_text())["repos"]


def test_corpus_is_pinned_and_unique():
    repos = _repos()
    assert len(repos) == 30
    assert len({r["name"] for r in repos}) == 30
    for r in repos:
        assert re.fullmatch(r"[0-9a-f]{40}", r["commit"]), r["name"]
        assert r["url"].startswith("https://github.com/") and r["url"].endswith(".git")
        assert r["split"] in ("tune", "holdout") and r["family"] and r["license"]


def test_holdout_split_covers_every_family_with_more_than_one_repo():
    by_family = defaultdict(set)
    for r in _repos():
        by_family[r["family"]].add(r["split"])
    counts = defaultdict(int)
    for r in _repos():
        counts[r["family"]] += 1
    for family, splits in by_family.items():
        if counts[family] > 1:
            assert splits == {"tune", "holdout"}, family
    assert sum(r["split"] == "holdout" for r in _repos()) == 10

