"""The post-tool adapter reports misses. A paraphrase that the span matcher drops is a miss."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_adapter_counts_the_paraphrase_as_a_miss():
    out = subprocess.check_output(
        [sys.executable, str(ROOT / "scripts" / "eval_post_tool.py"), str(ROOT / "pilot" / "post_tool_fixture.jsonl")],
        cwd=ROOT,
    )
    report = json.loads(out)
    by_id = {row["id"]: row for row in report["rows"]}
    assert by_id["F1"]["ok"] is True
    assert by_id["F1"]["verdicts"] == ["supported"]
    assert by_id["F2"]["verdicts"] == ["contradicted"]
    assert by_id["F3"]["verdicts"] == ["unverified"]
    assert by_id["F4"]["ok"] is False
    # "is not the Dirac value" is a faithful paraphrase. The span matcher reads the negation as a contradiction.
    assert by_id["F4"]["verdicts"] == ["contradicted"]
    assert report["faithful"]["hit"] == 1
    assert report["faithful"]["n"] == 2
    assert report["hallucinated"]["hit"] == 2
