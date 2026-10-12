import json
from pathlib import Path

import pytest

from appmod.evals import golden
from appmod.evals.golden import Fact, derive, normalize_route, route_candidates, score_app

ROOT = Path(__file__).resolve().parents[1]
CORPUS = json.loads((ROOT / "evals" / "corpus.json").read_text())["repos"]


def _write(root: Path, rel: str, text: str) -> None:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    _write(tmp_path, "pom.xml", """<project><properties><java.version>17</java.version></properties>
<dependencies>
<dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-web</artifactId></dependency>
<dependency><groupId>org.postgresql</groupId><artifactId>postgresql</artifactId></dependency>
<dependency><groupId>org.junit.jupiter</groupId><artifactId>junit-jupiter</artifactId></dependency>
</dependencies></project>""")
    _write(tmp_path, "src/main/java/app/Owner.java", "@Entity\n@Table(name=\"owners\")\npublic class Owner {}\n")
    _write(tmp_path, "src/main/java/app/OwnerController.java",
           "@GetMapping(\"/owners/{id}\")\npublic String show() {}\n")
    _write(tmp_path, "src/test/java/app/OwnerTest.java", "class OwnerTest {}\n")
    _write(tmp_path, "src/main/resources/templates/owners.html", "<html/>")
    _write(tmp_path, ".devcontainer/Dockerfile", "FROM eclipse-temurin:17\n")
    _write(tmp_path, ".github/workflows/ci.yml", "on: push\n")
    _write(tmp_path, "docs/requirements.txt", "sphinx\n")
    _write(tmp_path, "LICENSE", "MIT License\n\nPermission is hereby granted, free of charge, ...")
    return tmp_path


def _by_id(facts: list[Fact]) -> dict[str, Fact]:
    return {f.id: f for f in facts}


def test_derive_reads_manifests_code_and_infra(repo: Path):
    facts = _by_id(derive(repo))
    assert facts["framework:spring-boot"].expected == "org.springframework.boot:spring-boot-starter-web"
    assert facts["datastore:postgresql"].expected is True
    assert facts["entity:Owner"].source == "src/main/java/app/Owner.java:1"
    assert facts["route:/owners/*"].expected is True
    assert facts["runtime_version:runtime"].expected == "java 17"
    assert facts["license:license"].expected == "mit"
    assert facts["has_tests:has_tests"].source == "src/test/java/app/OwnerTest.java"
    assert facts["containerized:containerized"].source == ".devcontainer/Dockerfile"
    assert facts["ci:ci"].expected is True
    assert facts["has_data_layer:has_data_layer"].expected is True
    assert facts["capability_route:capability_route"].expected == "UI"
    assert "build_manifest:requirements.txt" not in facts
    assert facts["dependency:org.postgresql:postgresql"].source == "pom.xml:4"


def test_derive_empty_repo_states_negatives(tmp_path: Path):
    _write(tmp_path, "index.js", "console.log(1)\n")
    facts = _by_id(derive(tmp_path))
    for fid in ("has_tests:has_tests", "containerized:containerized", "ci:ci", "has_data_layer:has_data_layer"):
        assert facts[fid].expected is False, fid


def test_route_normalisation_and_candidates():
    assert normalize_route("/owners/{ownerId}/pets/:petId") == "/owners/*/pets/*"
    payloads = {"A1": {"repositories": [{"path": "/Users/me/corpus/app/users"}]},
                "A3": {"api_contract_refs": ["GET /api/users/{id}", "src/routes/users.py"]}}
    assert route_candidates(payloads) == ["/api/users/{id}"]


def test_scoring_compares_like_with_like():
    facts = [Fact("license", "license", "apache", "LICENSE"),
             Fact("runtime_version", "runtime", "java 17", "pom.xml"),
             Fact("route", "/owners/*", True, "x"),
             Fact("ci", "ci", True, ".github/workflows/ci.yml")]
    payloads = {"A1": {"dependencies": [{"name": "org.apache.commons:commons-lang3"}]},
                "A6": {"notes": "Runs on Java 17."},
                "A9": {"processes": [{"steps": ["GET /owners/{id} shows an owner"]}]},
                "A4": {"resources": [{"path": ".github/workflows/ci.yml"}]}}
    got = {r["type"]: r for r in score_app(facts, payloads)}
    assert got["license"]["ok"] is False
    assert got["runtime_version"]["ok"] is True
    assert got["route"]["ok"] is True
    assert got["ci"]["ok"] is True
    payloads["A6"]["licence"] = "Apache License 2.0"
    assert score_app(facts[:1], payloads)[0]["ok"] is True


def test_review_verdicts_are_applied(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    (tmp_path / "facts").mkdir()
    doc = {"repo": "app", "commit": "x", "split": "tune", "facts": [
        {"type": "ci", "key": "ci", "expected": True, "source": "a"},
        {"type": "entity", "key": "Base", "expected": True, "source": "b"},
        {"type": "runtime_version", "key": "runtime", "expected": "java 8", "source": "c"}]}
    (tmp_path / "facts" / "app.json").write_text(json.dumps(doc))
    (tmp_path / "review.json").write_text(json.dumps({"app": {
        "ci:ci": {"verdict": "accept"}, "entity:Base": {"verdict": "reject"},
        "runtime_version:runtime": {"verdict": "correct", "value": "java 11"}}}))
    monkeypatch.setattr(golden, "FACTS_DIR", tmp_path / "facts")
    monkeypatch.setattr(golden, "REVIEW", tmp_path / "review.json")
    facts = _by_id(golden.load("app"))
    assert set(facts) == {"ci:ci", "runtime_version:runtime"}
    assert facts["ci:ci"].review == "accepted"
    assert (facts["runtime_version:runtime"].expected, facts["runtime_version:runtime"].review) == ("java 11", "corrected")


def test_committed_facts_match_the_pinned_corpus():
    total = 0
    for r in CORPUS:
        doc = json.loads((ROOT / "evals" / "golden" / "facts" / f"{r['name']}.json").read_text())
        assert (doc["commit"], doc["split"]) == (r["commit"], r["split"]), r["name"]
        assert len({f["type"] + ":" + f["key"] for f in doc["facts"]}) == len(doc["facts"]), r["name"]
        total += len(doc["facts"])
    assert total >= 1000


def test_routes_in_comments_are_ignored(tmp_path: Path):
    _write(tmp_path, "site/urls.py", '"""\n    2. Add a URL to urlpatterns:  url(r\'^blog/\', include(\'blog.urls\'))\n"""\n'
                                     "# path('old/', view)\nurlpatterns = [url(r'^api/', include('api.urls'))]\n")
    routes = {f.key for f in derive(tmp_path) if f.type == "route"}
    assert routes == {"/api"}
