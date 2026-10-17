"""The verify response matches the verdict schema. The enum has no value true."""
import json
import sys
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "engine" / "v3"))
from claimguard import verify

SCHEMA = json.loads((ROOT / "schemas" / "verdict.schema.json").read_text(encoding="utf-8"))


def test_enum_has_six_verdicts_and_not_true():
    names = SCHEMA["$defs"]["verdict"]["enum"]
    assert names == [
        "out_of_scope", "contradicted", "contested", "overstated", "supported", "unverified",
    ]
    assert "true" not in names


def test_live_verify_matches_the_schema():
    out = verify("Hello")
    jsonschema.validate(out, SCHEMA)
    assert out["claims"][0]["verdict"] != "true"
