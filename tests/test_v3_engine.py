"""Orchestration tests for v3 with a fake model (no network).
They check coverage (R13), signature cleaning, deepening and run records (R16)."""
import json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "engine" / "v3"))
import core


class FakeLLM:
    """Answers each prompt type with plausible JSON; drops one node to test coverage reporting."""
    def __init__(self):
        self.calls = []

    def __call__(self, prompt, max_tokens=4000):
        self.calls.append(prompt)
        if prompt.startswith("You frame problems"):
            return {"problem": "Recover a sparse signal from few noisy measurements.",
                    "scqa": {"question": "How?"}, "signature": {"task": ["infer"], "direction": ["inverse"], "bogus": ["x"], "data": ["data_poor", "nonsense"]},
                    "fields": ["MA", "CS", "ZZ"]}
        if "Consider EACH subfield" in prompt:
            ids = re.findall(r"^- (MSC:\S+)", prompt, re.M)
            return {"nodes": [{"id": i, "applies": "yes" if i.startswith("MSC:42") else "no", "approach": "a", "promise": 5 if i.startswith("MSC:42") else 0, "cost": 1}
                              for i in ids if i != "MSC:97-XX"]}
        if prompt.startswith("Go deeper"):
            return {"node": "MSC:42-XX", "picks": [{"code": "42A", "method": "m", "conditions": [], "first_step": "s"}]}
        if prompt.startswith("Synthesise"):
            return {"governing_thought": "g", "routes": [{"summary": "s", "nodes": ["MSC:42-XX"], "status": "proposed"}]}
        if "Apply the whole of human knowledge" in prompt:
            return {"views": [{"field": "MA"}], "set_aside": [{"field": "AR", "reason": "r"}], "synthesis": {}}
        if "Candidate tools" in prompt:
            return {"candidates": [], "most_surprising": ""}
        raise AssertionError("unexpected prompt")


def test_frame_cleans_signature_and_fields():
    r = core.frame("x", FakeLLM())
    assert r["signature"] == {"task": ["infer"], "direction": ["inverse"], "data": ["data_poor"]}
    assert r["fields"] == ["MA", "CS"]


def test_consult_covers_every_node_and_reports_gaps(tmp_path, monkeypatch):
    monkeypatch.setattr(core, "ROOT", ROOT)
    llm = FakeLLM()
    rec = core.consult("x", "MA", llm, batch=16, deepen=1)
    assert len(rec["consulted"]) == 63
    assert rec["not_returned"] == ["MSC:97-XX"]
    assert rec["deeper"] and rec["deeper"][0]["node"] == "MSC:42-XX"
    assert (ROOT / "runs" / f"{rec['id']}.json").exists()
    (ROOT / "runs" / f"{rec['id']}.json").unlink()


def test_survey_reports_uncovered_fields():
    rec = core.survey("x", FakeLLM(), fields=["MA", "AR", "LA"])
    assert rec["result"]["uncovered"] == ["LA"]
    (ROOT / "runs" / f"{rec['id']}.json").unlink()


def test_connect_runs_matcher_then_model():
    rec = core.connect_run("x", "MA", FakeLLM())
    assert any(c.startswith("MA.TK.") for c in rec["consulted"])
    (ROOT / "runs" / f"{rec['id']}.json").unlink()
