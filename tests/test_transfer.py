"""Transfer operator: the brief (no model) and the fill step (fake model only)."""
import copy
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "engine" / "v3"))
import rosetta  # noqa: E402
import transfer  # noqa: E402


@pytest.fixture(scope="module")
def cores():
    return rosetta.load(ROOT)


@pytest.fixture(scope="module")
def graph(cores):
    return rosetta.Graph(ROOT, cores=cores)


@pytest.fixture(scope="module")
def doc(cores, graph):
    return transfer.brief(rosetta.core_by_id(cores, "RC-branching-threshold"), "EC", graph)


def good_answer(doc):
    return {
        "roles": {item["role"]: f"something for {item['role']}" for item in doc["roles"]},
        "assumptions": {item["id"]: {"met": "~", "reason": "roughly"} for item in doc["assumptions"]},
        "candidate_tool": "Cascade threshold for firm failures",
        "mismatches": ["Firms are not independent."],
        "ideas": ["Measure the mean number of failures each failure causes."],
        "already_known": "unsure", "already_known_note": "",
    }


class FakeLLM:
    def __init__(self, answer):
        self.answer, self.prompts = answer, []

    def __call__(self, prompt, max_tokens=4000):
        self.prompts.append(prompt)
        return self.answer


def test_brief_asks_about_every_role_and_assumption(doc, cores):
    core = rosetta.core_by_id(cores, "RC-branching-threshold")
    assert [item["role"] for item in doc["roles"]] == list(core["roles"])
    assert [item["id"] for item in doc["assumptions"]] == [a["id"] for a in core["assumptions"]]
    assert doc["status"] == "open question"
    assert doc["target"]["name"] == "Economics"


def test_brief_lists_most_distant_sources_first(doc):
    distances = [source["lineage_distance"] for source in doc["sources"]]
    assert distances == sorted(distances, reverse=True)
    assert len(doc["sources"]) == 4


def test_brief_refuses_bound_fields_mathematics_and_unknowns(cores, graph):
    core = rosetta.core_by_id(cores, "RC-branching-threshold")
    for field, message in (("MD", "already bound"), ("MA", "owns the cores"), ("ZZ", "unknown field")):
        with pytest.raises(rosetta.RosettaError, match=message):
            transfer.brief(core, field, graph)


def test_indigenous_knowledge_target_is_marked_provisional(cores, graph):
    core = rosetta.core_by_id(cores, "RC-branching-threshold")
    assert transfer.brief(core, "IK", graph)["provisional"] is True


def test_prompt_holds_the_brief_and_no_bench_material(doc):
    prompt = transfer.prompt_for(doc)
    assert "Economics" in prompt and "basic reproduction number" in prompt
    for item in doc["assumptions"]:
        assert item["text"] in prompt
    answers = json.loads((ROOT / "bench" / "retrodiction_answers.json").read_text(encoding="utf-8"))
    assert "retrodiction" not in prompt and "bench" not in prompt
    assert json.dumps(answers)[:200] not in prompt


def test_fill_returns_an_unverified_record_with_provenance(doc):
    llm = FakeLLM(good_answer(doc))
    record = transfer.fill(doc, llm, model_name="fake")
    assert record["status"] == "generated-unverified"
    assert record["provenance"]["model"] == "fake"
    assert record["provenance"]["conditions_checked_by"] == "model only"
    assert len(record["provenance"]["prompt_sha1"]) == 40
    assert record["provenance"]["sources"] and record["core"] == "RC-branching-threshold"
    assert record["guarantee_carries"] is False        # assumptions only approximately met
    assert len(llm.prompts) == 1


def test_guarantee_carries_only_when_every_assumption_holds_and_roles_are_filled(doc):
    answer = good_answer(doc)
    for value in answer["assumptions"].values():
        value["met"] = "y"
    assert transfer.fill(doc, FakeLLM(answer))["guarantee_carries"] is True
    answer["roles"]["mean"] = None
    record = transfer.fill(doc, FakeLLM(answer))
    assert record["guarantee_carries"] is False and record["unfilled_roles"] == ["mean"]


@pytest.mark.parametrize("change, expect", [
    (lambda a: a["roles"].pop("mean"), "roles must have exactly"),
    (lambda a: a["roles"].update(extra="x"), "roles must have exactly"),
    (lambda a: a["roles"].update(mean="  "), "non-empty string or null"),
    (lambda a: a["assumptions"]["a1"].update(met="maybe"), "met must be one of"),
    (lambda a: a["assumptions"]["a1"].update(reason=""), "a reason is required"),
    (lambda a: a["assumptions"].pop("a2"), "assumptions must have exactly"),
    (lambda a: a.update(mismatches=[]), "at least one mismatch"),
    (lambda a: a.update(ideas="none"), "ideas must be a list"),
    (lambda a: a.update(already_known="definitely"), "already_known must be"),
    (lambda a: a.update(candidate_tool=""), "candidate_tool"),
])
def test_malformed_answers_are_rejected(doc, change, expect):
    answer = copy.deepcopy(good_answer(doc))
    change(answer)
    with pytest.raises(rosetta.RosettaError, match=expect):
        transfer.fill(doc, FakeLLM(answer))


def test_non_object_answer_is_rejected(doc):
    with pytest.raises(rosetta.RosettaError, match="not a JSON object"):
        transfer.fill(doc, FakeLLM(["nope"]))


def test_cli_brief_and_errors(capsys):
    assert transfer.main(["RC-branching-threshold", "EC"]) == 0
    assert json.loads(capsys.readouterr().out)["kind"] == "transfer-brief"
    assert transfer.main(["RC-branching-threshold", "MD"]) == 2
    assert "already bound" in capsys.readouterr().err
