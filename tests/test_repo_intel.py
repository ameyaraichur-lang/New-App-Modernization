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


def test_manifests_are_detected_case_insensitively_and_parsed(tmp_path):
    from appmod.tools.repo_intel import parse_dependencies
    (tmp_path / "Gemfile").write_text('source "https://rubygems.org"\ngem "sinatra"\ngem \'rack-cache\'\n')
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "x"\ndependencies = ["flask>=3", "click"]\n'
        '[project.optional-dependencies]\ntest = ["pytest"]\n')
    (tmp_path / "Web.csproj").write_text(
        '<Project><ItemGroup><PackageReference Include="Microsoft.AspNetCore.Mvc" Version="2.1" />'
        '</ItemGroup></Project>')
    (tmp_path / "build.gradle").write_text(
        "dependencies {\n  implementation 'org.springframework.boot:spring-boot-starter-web'\n}\n")
    names = {d["name"] for d in parse_dependencies(scan_repo(tmp_path))}
    assert {"sinatra", "rack-cache", "flask", "click", "pytest", "Microsoft.AspNetCore.Mvc",
            "org.springframework.boot:spring-boot-starter-web"} <= names


def test_data_layer_needs_server_persistence(tmp_path):
    (tmp_path / "js" / "models").mkdir(parents=True)
    (tmp_path / "js" / "models" / "todo.js").write_text("var Todo = Backbone.Model.extend({});\n")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "orm.md").write_text("Use ActiveRecord or SQLAlchemy for persistence.\n")
    assert not scan_repo(tmp_path).has_data_layer()
    (tmp_path / "api").mkdir()
    (tmp_path / "api" / "models.go").write_text('package api\nimport "gorm.io/gorm"\ntype A struct{ gorm.Model }\n')
    assert scan_repo(tmp_path).has_data_layer()
