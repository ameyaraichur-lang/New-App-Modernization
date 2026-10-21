"""Three samples: a majority route publishes, a split reaches a reviewer."""

from appmod.agents.consistency import combine
from appmod.agents.runtime import AgentOutcome


def _route(disposition: str, evidence: str) -> dict:
    return {"decisions": [{"application_id": "app", "proposed_disposition": disposition,
                           "evidence_ids": [evidence]}]}


def test_majority_route_publishes_without_a_review():
    vote = combine(2, "A6", [_route("Refactor", "ev-1"), _route("Refactor", "ev-2"),
                             _route("Rebuild", "ev-3")])
    assert vote["agreed"] is True
    assert vote["winner"] == 1
    assert vote["review"] is None
    assert vote["agreement"] >= 2 / 3


def test_split_routes_list_every_option_for_the_reviewer():
    vote = combine(2, "A6", [_route("Refactor", "ev-1"), _route("Rehost", "ev-2"),
                             _route("Rebuild", "ev-3")])
    assert vote["agreed"] is False
    assert vote["winner"] is None
    review = vote["review"]
    assert review["role"] == "P2.A6"
    assert [option["choice"]["app"] for option in review["options"]] == [
        "Refactor", "Rehost", "Rebuild"]
    assert review["options"][0]["evidence_ids"] == ["ev-1"]


def test_boundary_majority_and_split():
    def bounds(*names: str) -> dict:
        return {"boundaries": [{"boundary": name, "evidence_ids": [name]} for name in names]}
    agreed = combine(3, "A2", [bounds("orders", "billing"), bounds("billing", "orders"), bounds("catalog")])
    assert agreed["agreed"] is True and agreed["winner"] == 1
    split = combine(3, "A2", [bounds("orders"), bounds("billing"), bounds("catalog")])
    assert split["agreed"] is False
    assert split["review"]["options"][2]["evidence_ids"] == ["catalog"]


def test_empty_samples_do_not_invent_agreement():
    empty = combine(2, "A6", [{}, {}, {}])
    assert empty["agreed"] is False and empty["winner"] is None
    two = combine(2, "A6", [_route("Refactor", "ev-1"), {}, _route("Refactor", "ev-3")])
    assert two["agreed"] is True and two["winner"] == 1
    blank_bounds = combine(3, "A2", [{"boundaries": []}, {"boundaries": []}, {"boundaries": []}])
    assert blank_bounds["agreed"] is False


def test_runner_publishes_the_majority_sample():
    from appmod.agents.llm_runner import LLMAgentRunner
    reviews = []
    runner = LLMAgentRunner.__new__(LLMAgentRunner)
    runner.phase = 2
    runner.on_disagreement = reviews.append
    payloads = [_route("Refactor", "ev-1"), _route("Rebuild", "ev-2"), _route("Refactor", "ev-3")]

    def loop(spec, inputs, seed, ov, context):
        return AgentOutcome("COMPLETE", payloads[context["sample"] - 1], execution_metadata={"llm": {}})

    runner._agent_loop = loop
    seed = AgentOutcome("COMPLETE", {"decisions": []})
    out = runner._consistent({"local_id": "A6"}, {}, seed, None, {})
    assert out.payload["decisions"][0]["proposed_disposition"] == "Refactor"
    assert out.execution_metadata["llm"]["consistency"]["agreed"] is True
    assert reviews == []


def test_runner_sends_a_disagreement_to_the_reviewer():
    from appmod.agents.llm_runner import LLMAgentRunner
    reviews = []
    runner = LLMAgentRunner.__new__(LLMAgentRunner)
    runner.phase = 2
    runner.on_disagreement = reviews.append
    payloads = [_route("Refactor", "ev-1"), _route("Rehost", "ev-2"), _route("Rebuild", "ev-3")]

    def loop(spec, inputs, seed, ov, context):
        payload = payloads[context["sample"] - 1]
        return AgentOutcome("COMPLETE", payload, execution_metadata={"llm": {}})

    runner._agent_loop = loop
    seed = AgentOutcome("COMPLETE", {"decisions": [{"application_id": "app",
                                                    "proposed_disposition": "Rehost"}]})
    out = runner._consistent({"local_id": "A6"}, {}, seed, None, {})
    assert out.payload["decisions"][0]["proposed_disposition"] == "Rehost"
    assert out.payload["consistency_review"]["kind"] == "routes"
    assert reviews and len(reviews[0]["options"]) == 3
