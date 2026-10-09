"""Phase handoff adapters: published artifacts of phase N -> inputs of N+1.

Every downstream brief is derived from sealed, stored artifacts (never from
in-memory guesses), so a resumed or re-run job rebuilds identical inputs and
the orchestrator's reuse-by-input-hash stays exact.
"""

from __future__ import annotations

import json
from typing import Any

from appmod.phases.p2.engine import PortfolioApp
from appmod.tools.repo_intel import CODE_LANGUAGES

PORTFOLIO_ID = "PF1"


def _p(store, aid: str) -> dict[str, Any]:
    return store.get(aid)


def _payload_field(art: dict[str, Any], key: str, default: Any = None) -> Any:
    v = art.get("payload", {}).get(key, default)
    if isinstance(v, str) and v[:1] in "[{":
        try:
            return json.loads(v)
        except ValueError:
            return default
    return v


# -- P1 -> P2 ---------------------------------------------------------------------


def p1_release(store, app: str) -> dict[str, Any]:
    return _p(store, f"P1/{app}/G2")["payload"]["decision_record"]


def portfolio_app(store, app: str) -> PortfolioApp:
    a1, a3, a5 = (_p(store, f"P1/{app}/{n}") for n in ("A1", "A3", "A5"))
    repo0 = a1["payload"]["repositories"][0]
    langs = repo0.get("languages", {})
    return PortfolioApp(
        app_id=app,
        p1_g2_status=p1_release(store, app)["status"],
        loc=int(repo0.get("code_loc") or repo0.get("loc", 0)),
        languages=max(1, sum(1 for k in langs if k in CODE_LANGUAGES)),
        dependencies=len(a1["payload"].get("dependencies", [])),
        tests=int((_payload_field(a1, "coverage", {}) or {}).get("test_files", 0)),
        route=a5["payload"]["capability_route"],
        has_data_layer=bool(a3["payload"].get("datasets")),
        primary_language=repo0.get("primary_language") or "unknown",
        source_family="solo",
        p1_manifest_hash=_p(store, f"P1/{app}/G1")["payload"]["evidence_manifest"]["manifest_hash"],
    )


def p2_run_inputs(store, apps: list[str]) -> dict[str, Any]:
    return {
        "scope_manifest": {"portfolio_id": PORTFOLIO_ID, "applications": sorted(apps)},
        "p1_packages": [{"application_id": a, "schema_version": "P1.discovery.v3.0",
                         "g2_status": p1_release(store, a)["status"],
                         "manifest_hash": portfolio_app(store, a).p1_manifest_hash}
                        for a in sorted(apps)],
        "p1_scope": {a: p1_release(store, a)["status"] for a in sorted(apps)},
    }


# -- P2 -> P3 -----------------------------------------------------------------------


def p2_release(store) -> dict[str, Any]:
    return _p(store, f"P2/{PORTFOLIO_ID}/G2")["payload"]["decision_record"]


def disposition(store, app: str) -> str:
    reg = _p(store, f"P2/{PORTFOLIO_ID}/A7")["payload"]["route_register"]
    return next((e["route"] for e in reg if e["application_id"] == app), "Replatform")


def wave_of(store, app: str) -> str:
    decisions = _p(store, f"P2/{PORTFOLIO_ID}/A6")["payload"].get("decisions", [])
    return next((d.get("wave_id") or "W1" for d in decisions if d["application_id"] == app), "W1")


def authorized_apps(store) -> list[str]:
    return list(p2_release(store).get("authorized_apps", []))


def design_brief(store, app: str) -> dict[str, Any]:
    a1, a3, a5 = (_p(store, f"P1/{app}/{n}") for n in ("A1", "A3", "A5"))
    return {
        "app_id": app, "disposition": disposition(store, app),
        "primary_language": a1["payload"]["repositories"][0].get("primary_language", "unknown"),
        "route": a5["payload"]["capability_route"],
        "components": [c["name"] for c in a1["payload"].get("components", [])[:8]],
        "routes": [i["endpoint"] for i in a3["payload"].get("integrations", [])][:20],
        "datasets": [d["name"] for d in a3["payload"].get("datasets", [])][:12],
        "journeys": [j.get("name") for j in a5["payload"].get("journeys", [])
                     if isinstance(j, dict) and j.get("name")][:6],
    }


def p3_run_inputs(store, app: str) -> dict[str, Any]:
    g2 = p2_release(store)
    return {
        "scope_manifest": {"workload_ids": [app]},
        "p2_package": {"application_id": app, "authorized": app in g2.get("authorized_apps", []),
                       "authorization": g2.get("status"), "disposition": disposition(store, app),
                       "candidate_hash": g2.get("candidate_hash")},
    }


# -- P3 -> P4 -----------------------------------------------------------------------


def p3_release(store, app: str) -> dict[str, Any]:
    return _p(store, f"P3/{app}/G2")["payload"]["decision_record"]


def plan_brief(store, app: str) -> dict[str, Any]:
    brief = design_brief(store, app)
    return {"app_id": app, "disposition": brief["disposition"], "wave": wave_of(store, app),
            "components": brief["components"]}


def p4_run_inputs(store, app: str) -> dict[str, Any]:
    g2 = p3_release(store, app)
    return {
        "scope_manifest": {"workload_ids": [app]},
        "p3_package": {"application_id": app, "status": g2["status"],
                       "conditions": g2.get("conditions", []),
                       "candidate_hash": g2.get("candidate_hash")},
    }


# -- P4 -> P5 -----------------------------------------------------------------------


def p4_release(store, app: str) -> dict[str, Any]:
    return _p(store, f"P4/{app}/G2")["payload"]["decision_record"]


def code_brief(store, app: str, repo_path: str) -> dict[str, Any]:
    a1, a3 = (_p(store, f"P1/{app}/{n}") for n in ("A1", "A3"))
    repo0 = a1["payload"]["repositories"][0]
    return {
        "app_id": app, "disposition": disposition(store, app), "repo_path": repo_path,
        "routes": [i["endpoint"] for i in a3["payload"].get("integrations", [])][:12],
        "datasets": [d["name"] for d in a3["payload"].get("datasets", [])][:8],
        "dependencies": a1["payload"].get("dependencies", []),
        "tests": (_payload_field(a1, "coverage", {}) or {}).get("test_paths", []),
        "pinned_commit": repo0.get("commit") or "unpinned",
        "route": _p(store, f"P1/{app}/A5")["payload"]["capability_route"],
    }
