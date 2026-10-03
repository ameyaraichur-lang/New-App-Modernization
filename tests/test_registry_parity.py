"""T0 registry parity CI — reproduces the blueprint's own static verification."""

from appmod.registry.compiler import PARITY, TOTAL_LINKS, TOTAL_ROLES, MASTER_LINKS


def test_parity_counts(registry):
    roles = sum(len(r["agents"]) for r in registry["phases"].values())
    links = sum(len(r["hard_edges"]) for r in registry["phases"].values())
    assert roles == TOTAL_ROLES == 78
    assert links == TOTAL_LINKS == 190
    assert len(registry["master"]["links"]) == MASTER_LINKS == 17


def test_per_phase_counts(registry):
    for phase, expect in PARITY.items():
        reg = registry["phases"][phase]
        assert len(reg["agents"]) == expect["roles"], f"P{phase} roles"
        assert len(reg["hard_edges"]) == expect["links"], f"P{phase} links"


def test_agent_anatomy_complete(registry):
    """Every compiled agent carries the six registry fields verbatim."""
    for phase, reg in registry["phases"].items():
        for a in reg["agents"]:
            assert a["id"].startswith(f"P{phase}.")
            for field_name in ("name", "activities", "inputs", "outputs",
                               "execution_raw", "origin", "contract_rule"):
                assert a[field_name], f"{a['id']} missing {field_name}"


def test_p1_specific_anatomy(registry):
    p1 = registry["phases"][1]
    agents = {a["local_id"]: a for a in p1["agents"]}
    assert agents["A8"]["lane"] == "async"
    assert agents["A1"]["tier"] == 0 and agents["A1"]["prerequisites"] == ["G0"]
    assert sorted(agents["A2"]["prerequisites"]) == ["A1", "A4"]
    assert agents["A11"]["tier"] == 4 and agents["A11"]["prerequisites"] == ["A10"]
    gates = {g["id"] for g in p1["gates"]}
    assert gates == {"G0", "G1", "G2"}


def test_p5_p6_gate_structure(registry):
    p5 = registry["phases"][5]
    assert {g["id"] for g in p5["gates"]} == {"G0", "G1", "G2", "G3", "G4"}
    a9 = next(a for a in p5["agents"] if a["local_id"] == "A9")
    assert sorted(a9["prerequisites"]) == ["G1", "G3"]

    p6 = registry["phases"][6]
    assert {g["id"] for g in p6["gates"]} == {"G0", "G1", "G2", "G3", "X1"}
    assert any(g["id"] == "X1" and g["kind"] == "execution" for g in p6["gates"])
    assert len(p6["execution_routes"]) == 6


def test_activation_matrices_and_routes(registry):
    assert len(registry["phases"][3]["activation_matrix"]) == 8  # 8 dispositions
    assert len(registry["phases"][5]["activation_matrix"]) == 8


def test_route_branch_edges(registry):
    p2 = registry["phases"][2]
    assert any(e["from"] == "G2" and e["to"] == "R" and e["external"] for e in p2["hard_edges"])
    p1 = registry["phases"][1]
    assert any(e["from"] == "G2" and e["to"] == "P2" and e["external"] for e in p1["hard_edges"])


def test_payload_contracts_parsed(registry):
    for phase in (1, 2, 3, 4, 5, 6):
        payloads = registry["phases"][phase]["artifact_contracts"]["agent_payloads"]
        assert payloads, f"P{phase} has no parsed payloads"
        for local_id, spec in payloads.items():
            assert spec["fields"], f"P{phase}.{local_id} payload has no typed fields"


def test_milestone_graphs_acyclic(registry):
    from appmod.registry.compiler import check_acyclic
    for phase, reg in registry["phases"].items():
        assert check_acyclic(reg) == [], f"P{phase} milestone graph cyclic"


def test_master_topology(registry):
    links = registry["master"]["links"]
    by_id = {l["id"]: l for l in links}
    assert by_id["M01"]["from"] == "P1" and by_id["M01"]["to"] == "P2"
    assert by_id["M06"]["type"] == "CONDITIONAL"       # P5 -> P6 data route
    assert by_id["M03"]["type"] == "BRANCH"            # P2 -> Retain/Retire
    assert by_id["M12"]["from"] == "P3" and by_id["M12"]["to"] == "P6"  # pinned reference
    findings = {f["id"] for f in registry["master"]["open_findings"]}
    assert findings == {"AH01", "AH02", "AH03", "AH04", "AH05", "AH06"}
