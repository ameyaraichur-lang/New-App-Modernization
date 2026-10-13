"""Offline tests for P2/P3 structure analyzer tools."""

from __future__ import annotations

import json
import subprocess
import time
from pathlib import Path

import pytest

from appmod.agents.overlays import OVERLAYS
from appmod.tools.builtin import STRUCTURE_TOOLS, build_gateway
from appmod.tools.gateway import EvidenceLedger, ToolEnv
from appmod.tools.structure import (
    api_surface,
    change_coupling,
    db_schema,
    dependency_graph,
)

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT.parent / "corpus"
VENV_PY = ROOT.parent / "New-App-Modernization" / ".venv" / "bin" / "python"


@pytest.fixture
def mini_repo(tmp_path):
    (tmp_path / "pkg").mkdir()
    (tmp_path / "pkg" / "a.py").write_text("import pkg.b\nX = 1\n")
    (tmp_path / "pkg" / "b.py").write_text("import pkg.a\nY = 2\n")
    (tmp_path / "pkg" / "routes.py").write_text(
        'from flask import Flask\napp = Flask(__name__)\n@app.get("/health")\ndef health():\n    return "ok"\n'
    )
    (tmp_path / "db").mkdir()
    (tmp_path / "db" / "schema.sql").write_text(
        "CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR(64));\n"
        "CREATE TABLE orders (id INT, user_id INT, FOREIGN KEY (user_id) REFERENCES users(id));\n"
    )
    (tmp_path / "db" / "001_create_posts.rb").write_text("create_table :posts do |t|\n  t.string :title\nend\n")
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "t@example.com"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=tmp_path, check=True)
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=tmp_path, check=True)
    (tmp_path / "pkg" / "c.py").write_text("import pkg.a\n")
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-m", "couple a and c"], cwd=tmp_path, check=True)
    return tmp_path


def test_dependency_graph_cycle_and_edges(mini_repo):
    g = dependency_graph(mini_repo)
    assert g["internal_edges"] >= 2
    assert g["edges"]
    mods = {m["module"] for m in g["modules"]}
    assert "pkg.a" in mods or "pkg.b" in mods
    assert g["cycles"]


def test_change_coupling_pairs(mini_repo):
    c = change_coupling(mini_repo)
    assert c["commits_scanned"] >= 1
    assert c["coupled_pairs"]
    mods = c["coupled_pairs"][0]["modules"]
    assert len(mods) == 2


def test_db_schema_from_ddl_and_rails(mini_repo):
    s = db_schema(mini_repo)
    names = {t["table"] for t in s["tables"]}
    assert "users" in names
    assert "posts" in names
    users = next(t for t in s["tables"] if t["table"] == "users")
    assert users["sources"]


def test_api_surface_routes(mini_repo):
    a = api_surface(mini_repo)
    assert a["endpoint_count"] >= 1
    assert any("/health" in (e.get("path") or "") for e in a["http_endpoints"])


def test_change_coupling_non_git(tmp_path):
    err = change_coupling(tmp_path)
    assert err["status"] == "ERROR"


def test_structure_tools_registered_and_mint_evidence(mini_repo):
    gw = build_gateway()
    for name in STRUCTURE_TOOLS:
        assert name in gw.tools
    env = ToolEnv(application_id="t", phase=3, repo_root=mini_repo, store=None, published={})
    ledger = EvidenceLedger()
    sess = gw.session("P3.A2", STRUCTURE_TOOLS, env, ledger)
    for tool in STRUCTURE_TOOLS:
        text, eid = sess.call(tool, {"application_id": None})
        assert eid and eid.startswith("ev-"), tool
        assert ledger.has(eid)
        assert f'tool="{tool}"' in text


@pytest.mark.parametrize("agent,phase", [
    ("A2", 2), ("A4", 2), ("A6", 2),
    ("A1", 3), ("A2", 3), ("A3", 3), ("A6", 3),
])
def test_overlays_allow_structure_tools(agent, phase):
    tools = set(OVERLAYS[phase][agent].tools)
    for name in STRUCTURE_TOOLS:
        assert name in tools, f"P{phase} {agent} missing {name}"


@pytest.mark.parametrize("repo", ["spring-petclinic", "golang-example", "laravel58"])
def test_corpus_structure_tools_smoke(repo):
    path = CORPUS / repo
    if not path.exists():
        pytest.skip(f"corpus repo {repo} not cloned")
    g = dependency_graph(path)
    assert g["modules_sampled"] > 0
    c = change_coupling(path)
    assert c.get("commits_scanned", 0) >= 0
    assert db_schema(path)["table_count"] >= 0
    assert api_surface(path)["endpoint_count"] >= 0


@pytest.mark.parametrize("repo", ["gitea", "ofbiz"])
def test_large_repo_timing(repo):
    path = CORPUS / repo
    if not path.exists():
        pytest.skip(f"corpus repo {repo} not cloned")
    timings = {}
    for name, fn in (
        ("dependency_graph", dependency_graph),
        ("change_coupling", change_coupling),
        ("db_schema", db_schema),
        ("api_surface", api_surface),
    ):
        t0 = time.perf_counter()
        fn(path)
        timings[name] = round(time.perf_counter() - t0, 2)
    print(json.dumps({"repo": repo, "seconds": timings}))
    assert timings["dependency_graph"] < 12.0
    assert timings["change_coupling"] < 12.0
    assert timings["db_schema"] < 12.0
    assert timings["api_surface"] < 15.0
