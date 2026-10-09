"""Repo intelligence: code-only primary language, pinned commit, real P2 inputs."""

from pathlib import Path

import pytest

from appmod.tools.repo_intel import scan_repo

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT.parent / "corpus"


def test_primary_language_ignores_data_and_docs():
    s = scan_repo(ROOT)
    assert s.languages.get("json", 0) > 0
    assert s.primary_language == "python"
    assert "json" not in s.code_languages
    assert s.code_loc < s.loc


def test_commit_pinned_for_git_repo():
    assert len(scan_repo(ROOT).commit) == 40


@pytest.mark.parametrize("repo,lang", [
    ("spring-petclinic", "java"),
    ("microblog", "python"),
    ("node-express-realworld-example-app", "typescript"),
])
def test_corpus_primary_language(repo, lang):
    path = CORPUS / repo
    if not path.exists():
        pytest.skip(f"corpus repo {repo} not cloned")
    assert scan_repo(path).primary_language == lang


def test_p1_a1_payload_exposes_language_and_tests():
    from appmod.phases.p1.engine import P1AgentRunner
    r = P1AgentRunner()
    r.bind_repo(ROOT)
    out = r.run({"local_id": "A1"}, {}, None)
    repo0 = out.payload["repositories"][0]
    assert repo0["primary_language"] == "python"
    assert repo0["test_files"] == out.payload["coverage"]["test_files"] > 0
    assert all(p.startswith("tests/") for p in out.payload["coverage"]["test_paths"])
