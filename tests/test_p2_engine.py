"""T2/T4 P2 engine tests: route router integrity, scope rules, IA02 register."""

from pathlib import Path

import pytest

from appmod.kernel.audit import AuditJournal
from appmod.kernel.orchestrator import PhaseOrchestrator
from appmod.kernel.policy import PolicyService
from appmod.phases.p2.engine import P2AgentRunner, P2_GATE_OVERRIDES, PortfolioApp
from appmod.store.artifact_store import ArtifactStore


def fixture_apps():
    return [
        PortfolioApp(app_id="app-decided", p1_g2_status="READY_FOR_PORTFOLIO_DECISION",
                     loc=40000, languages=5, dependencies=60, route="UI",
                     has_data_layer=True, primary_language="java", source_family="solo"),
        PortfolioApp(app_id="app-draft", p1_g2_status="READY_FOR_PORTFOLIO_DRAFT",
                     loc=8000, languages=2, dependencies=10, route="API_ONLY",
                     has_data_layer=False, primary_language="go", source_family="library"),
        PortfolioApp(app_id="app-retain", p1_g2_status="READY_FOR_PORTFOLIO_DRAFT",
                     loc=3000, languages=2, dependencies=5, route="UI",
                     has_data_layer=False, primary_language="js", source_family="js-demo", non_delivery_proposal="Retain"),
        PortfolioApp(app_id="app-retire", p1_g2_status="READY_FOR_PORTFOLIO_DRAFT",
                     loc=3000, languages=2, dependencies=5, route="UI",
                     has_data_layer=False, primary_language="js", source_family="js-demo", non_delivery_proposal="Retire"),
    ]


@pytest.fixture()
def run_p2(tmp_path):
    def _run():
        registry = pytest.importorskip
        from appmod.registry.compiler import resolve_registry
        reg = resolve_registry()
        store = ArtifactStore(tmp_path / "store")
        audit = AuditJournal(tmp_path / "audit")
        policy = PolicyService()
        apps = fixture_apps()
        orch = PhaseOrchestrator(reg["phases"][2], store, policy, audit,
                                 P2AgentRunner(apps), gate_overrides=P2_GATE_OVERRIDES)
        ctx = orch.start_run("p2-test", "PFIX", {
            "scope_manifest": {"portfolio_id": "PFIX"},
            "p1_packages": [
                {"application_id": a.app_id, "schema_version": "P1.discovery.v3.0",
                 "g2_status": a.p1_g2_status, "manifest_hash": "x"}
                for a in apps
            ],
            "p1_scope": {a.app_id: a.p1_g2_status for a in apps},
        })
        orch.run(ctx)
        return store, ctx
    return _run


def test_p2_full_run_and_routes(run_p2):
    store, ctx = run_p2()
    assert ctx.finished
    g2 = store.get("P2/PFIX/G2")
    dec = g2["payload"]["decision_record"]
    assert dec["status"] == "AUTHORIZED"
    assert dec["authorized_apps"] == ["app-decided"]
    assert set(dec["draft_only_apps"]) == {"app-draft"}


def test_route_register_single_route_per_app(run_p2):
    store, _ = run_p2()
    a7 = store.get("P2/PFIX/A7")
    register = a7["payload"]["route_register"]
    apps = [e["application_id"] for e in register]
    assert len(apps) == len(set(apps)), "duplicate route entries"
    routes = {e["application_id"]: e["route"] for e in register}
    assert routes["app-retain"] == "Retain"
    assert routes["app-retire"] == "Retire"
    assert routes["app-decided"] in ("Rearchitect", "Replatform", "Rehost", "Refactor",
                                     "Rebuild", "Replace")


def test_ia02_register_entries(run_p2):
    store, _ = run_p2()
    g2 = store.get("P2/PFIX/G2")
    entries = g2["payload"]["decision_record"]["non_delivery_register"]["entries"]
    assert {e["application_id"] for e in entries} == {"app-retain", "app-retire"}
    for e in entries:
        assert e["register"].startswith("IA02")
        assert "retirement_authority" in e or "review_date" in e


def test_no_app_dropped_from_inventory(run_p2):
    store, _ = run_p2()
    a4 = store.get("P2/PFIX/A4")
    assert set(a4["payload"]["retained_app_ids"]) == {
        "app-decided", "app-draft", "app-retain", "app-retire"}


def test_g1_consistency_refs(run_p2):
    store, _ = run_p2()
    g1 = store.get("P2/PFIX/G1")
    refs = g1["payload"]["evidence_manifest"]["artifact_refs"]
    assert {"A1", "A2", "A3", "A4", "A5"} <= set(refs)
    a3 = store.get("P2/PFIX/A3")
    assert a3["payload"]["complexity_ref"] == refs["A2"]["content_hash"]
