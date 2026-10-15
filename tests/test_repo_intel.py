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
    ("carddemo", "cobol"),              # JCL and shell scripts must not outrank COBOL
    ("bugzilla", "perl"),               # JavaScript assets must not outrank Perl modules
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


def test_gin_routes_ci_files_and_runtime_versions(tmp_path):
    (tmp_path / "go.mod").write_text("module example.com/app\n\ngo 1.21\n")
    (tmp_path / "main.go").write_text(
        'package main\nfunc main() {\n\tv1 := router.Group("/api/v1")\n\tv1.GET("/albums", list)\n'
        '\tv1.POST("/albums", create)\n}\n')
    (tmp_path / "notes.py").write_text('client.GET("/not-a-route")\n')
    (tmp_path / ".travis.yml").write_text("language: go\n")
    (tmp_path / ".circleci").mkdir()
    (tmp_path / ".circleci" / "config.yml").write_text("version: 2\n")
    (tmp_path / "LICENSE").write_text("MIT License\n\nPermission is hereby granted, free of charge\n")
    s = scan_repo(tmp_path)
    assert {r["route"] for r in s.routes} >= {"/api/v1", "/albums"}
    assert all(r["file"] == "main.go" for r in s.routes)
    assert {".travis.yml", ".circleci/config.yml"} <= set(s.infra_files)
    assert s.runtime_versions == [{"runtime": "go 1.21", "file": "go.mod"}]

    from appmod.phases.p1.engine import P1AgentRunner
    r = P1AgentRunner()
    r.bind_repo(tmp_path)
    out = r.run({"local_id": "A1"}, {}, None)
    repo0 = out.payload["repositories"][0]
    assert repo0["license"] == "MIT License (LICENSE)"
    assert repo0["runtime_versions"] == ["go 1.21 (go.mod)"]


@pytest.mark.parametrize("name,text,want", [
    ("pom.xml", "<properties><java.version>17</java.version></properties>", "java 17"),
    ("build.gradle", "java { toolchain { languageVersion = JavaLanguageVersion.of(21) } }", "java 21"),
    ("package.json", '{"engines": {"node": ">=18.0.0"}}', "node 18"),
    ("composer.json", '{"require": {"php": "^8.1"}}', "php 8.1"),
    ("pyproject.toml", 'requires-python = ">=3.10"\n', "python 3.10"),
    ("Web.csproj", "<TargetFramework>net8.0</TargetFramework>", "net8.0"),
])
def test_runtime_version_manifests(tmp_path, name, text, want):
    (tmp_path / name).write_text(text)
    assert [r["runtime"] for r in scan_repo(tmp_path).runtime_versions] == [want]


def test_project_licence_is_the_root_file_not_vendored_ones(tmp_path):
    (tmp_path / "LICENSE").write_text("Apache License\nVersion 2.0, January 2004\n")
    (tmp_path / "NOTICE").write_text("This product includes software developed elsewhere.\n")
    (tmp_path / "vendor" / "fontawesome").mkdir(parents=True)
    (tmp_path / "vendor" / "fontawesome" / "LICENSE.txt").write_text("MIT License\n")
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "licenses.test.ts").write_text("test('licenses', () => {});\n")
    assert scan_repo(tmp_path).license == {"file": "LICENSE", "type": "Apache-2.0", "evidence": "DOCUMENTED"}
