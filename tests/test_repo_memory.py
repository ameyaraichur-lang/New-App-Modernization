"""Hierarchical repo memory: content-hash cache, bounded map, retrieval budget."""

import json
import subprocess
from pathlib import Path

from appmod.retrieval.memory import AGENT_INPUT_TOKEN_CAP, MAP_BUDGET_CHARS, map_text, repo_map
from appmod.tools.builtin import build_gateway
from appmod.tools.gateway import EvidenceLedger, ToolEnv
from scripts.check_retrieval_budget import over_budget


def _repo(tmp_path: Path) -> Path:
    root = tmp_path / "app"
    (root / "orders").mkdir(parents=True)
    (root / "party" / "model").mkdir(parents=True)
    (root / "orders" / "pom.xml").write_text("<project/>")
    (root / "orders" / "Order.java").write_text("class Order {}")
    (root / "party" / "model" / "Person.java").write_text("class Person {}")
    subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True)
    subprocess.run(["git", "add", "."], cwd=root, check=True, capture_output=True)
    subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-m", "init"],
                   cwd=root, check=True, capture_output=True)
    return root


def test_module_summary_is_cached_by_content_hash(tmp_path: Path):
    root = _repo(tmp_path)
    cache = tmp_path / "cache"
    first = repo_map(root, cache_dir=cache)
    second = repo_map(root, cache_dir=cache)
    assert first["cached"] is False
    assert second["cached"] is True
    assert first["content_hash"] == second["content_hash"]
    names = {m["module"] for m in first["modules"]}
    assert names == {"orders", "party"}
    orders = next(m for m in first["modules"] if m["module"] == "orders")
    assert "pom.xml" in orders["manifests"][0]


def test_changing_a_file_changes_the_module_hash(tmp_path: Path):
    root = _repo(tmp_path)
    cache = tmp_path / "cache"
    before = repo_map(root, cache_dir=cache)["content_hash"]
    (root / "orders" / "Order.java").write_text("class Order { int x; }")
    after = repo_map(root, cache_dir=cache)
    assert after["cached"] is False
    assert after["content_hash"] != before


def test_map_text_stays_inside_its_budget(tmp_path: Path):
    root = tmp_path / "wide"
    for i in range(40):
        module = root / f"mod{i:02d}"
        module.mkdir(parents=True)
        for j in range(30):
            (module / f"f{j}.java").write_text("class F {}")
    text = map_text(root, 500, cache_dir=tmp_path / "cache")
    assert len(text) <= 500
    assert "omitted" in text


def test_tool_results_stop_at_the_retrieval_budget(tmp_path: Path):
    root = _repo(tmp_path)
    env = ToolEnv(application_id="app", phase=1, repo_root=root, retrieval_budget_chars=80)
    session = build_gateway().session("A1", ["repo_map", "read_file"], env, EvidenceLedger())
    first, eid = session.call("repo_map", {"application_id": None, "module": None})
    assert eid
    assert "orders" in first
    second, _ = session.call("read_file", {"application_id": None, "path": "orders/Order.java",
                                           "start_line": None, "end_line": None})
    assert "retrieval_budget_exhausted" in second


def test_ofbiz_map_is_bounded():
    root = Path(__file__).resolve().parents[2] / "corpus" / "ofbiz"
    if not (root / ".git").exists():
        return
    text = map_text(root, MAP_BUDGET_CHARS)
    assert len(text) <= MAP_BUDGET_CHARS
    assert "applications" in text or "framework" in text


def test_budget_checker_uses_twice_the_run4_median():
    assert AGENT_INPUT_TOKEN_CAP == 99_312
    report = {"agents": [{"phase": 1, "agent": "A1", "app": "ofbiz", "tokens": {"input": 99_312}},
                         {"phase": 1, "agent": "A2", "app": "ofbiz", "tokens": {"input": 99_313}}]}
    assert over_budget(report) == ["1.A2 ofbiz 99313 > 99312"]
    assert json.dumps(report)
