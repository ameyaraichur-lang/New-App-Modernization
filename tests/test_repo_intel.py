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


def test_vendored_and_minified_files_are_not_app_code(tmp_path):
    (tmp_path / "Controllers").mkdir()
    (tmp_path / "Controllers" / "Home.cs").write_text("class Home {}\n" * 50)
    (tmp_path / "wwwroot").mkdir()
    for name in ("jquery-2.0.3.js", "bootstrap.js", "app.min.js", "jquery.validate-vsdoc.js"):
        (tmp_path / "wwwroot" / name).write_text("var x = 1;\n" * 5000)
    (tmp_path / "wwwroot" / "site.js").write_text("init();\n" * 10)
    s = scan_repo(tmp_path)
    assert s.primary_language == "csharp"
    assert {f["path"] for f in s.files if f["language"] == "javascript"} == {"wwwroot/site.js"}


def test_commit_pinned_for_git_repo():
    assert len(scan_repo(ROOT).commit) == 40


@pytest.mark.parametrize("repo,lang", [
    ("spring-petclinic", "java"),
    ("microblog", "python"),
    ("node-express-realworld-example-app", "typescript"),
    ("musicstore", "csharp"),           # vendored jQuery/Bootstrap must not win
    ("laravel58", "php"),
    ("sinatra", "ruby"),
    ("golang-example", "go"),
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


def test_p1_a11_scores_follow_policy_rubric():
    from appmod.kernel.policy import PolicyService
    from appmod.phases.p1.engine import P1AgentRunner
    policy = PolicyService()
    assert policy.get("risk_taxonomy", "rubric", "technical")
    scores = {}
    for repo in ("spring-petclinic", "microblog"):
        if not (CORPUS / repo).exists():
            pytest.skip(f"corpus repo {repo} not cloned")
        r = P1AgentRunner(use_analyzers=False)
        r.bind_repo(CORPUS / repo)
        out = r.run({"local_id": "A11"}, {}, policy)
        dims = {d["dimension"]: d for d in out.payload["risk_dimensions"]}
        assert "pilot-default mid band" not in str(out.payload)
        assert all(d["score"] == min(5, 1 + len(d["drivers"])) for d in dims.values())
        assert "security" in {u["dimension"] for u in out.payload["unassessed_dimensions"]}
        scores[repo] = {k: d["score"] for k, d in dims.items()}
    assert scores["spring-petclinic"]["data"] >= 2 and scores["microblog"]["data"] >= 2
