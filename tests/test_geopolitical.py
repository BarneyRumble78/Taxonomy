"""Geopolitical claims from the 10 Oct 2026 live-trial failure classes.

Labels follow the standard: conduct of force is Strategy, relations among states
are Politics. An official statement, testimony or a claim of responsibility is W7.
Imagery and a count of events are W4. A bare situation report keeps the field
default and says so. None of these sentences is a lexicon cue.
"""
import csv, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "engine"))
import taxonomy_engine as te

HELD = Path(__file__).resolve().parent / "geopolitical_heldout.tsv"
FROZEN = ROOT / "pilot" / "heldout.tsv"
PROPER = ("zarichne", "hormuz", "yemen", "houthi", "albania", "albanian", "italian", "italy", "oman", "baltic", "irgc")


def _rows(path):
    return list(csv.DictReader(path.open(encoding="utf-8"), delimiter="\t"))


def test_geopolitical_heldout_matches_standard_labels():
    rows = _rows(HELD)
    assert len(rows) == 13
    for r in rows:
        got = te.rule_placement(r["claim"])
        assert got is not None, r["id"]
        assert got["owner"] == r["owner"], (r["id"], got["owner"], r["claim"])
        assert got["cell"] == r["cell"], (r["id"], got["cell"], r["claim"])
        assert got["warrant"] == r["warrant"], (r["id"], got["warrant"], r["claim"])
        if r["warrant"] == "W9" and r["id"] == "G01":
            assert got["default_applied"] is True


def test_heldout_claims_are_not_lexicon_cues():
    blob = json.dumps(te.LEXICON, ensure_ascii=False).lower()
    for name in PROPER:
        assert name not in blob, name
    for r in _rows(HELD):
        assert r["claim"].lower() not in blob


def test_short_cues_do_not_fire_inside_other_words():
    assert te.rule_placement("In an inertial frame, the net force on a particle equals its mass times its acceleration.")["owner"] == "PH"
    assert te.rule_placement("The unemployment rate is the share of the labour force that is without work and seeking work.")["owner"] == "EC"
    assert te.rule_placement("Prime numbers are infinite.")["owner"] == "MA"
    assert te.rule_placement("A national mobilisation followed the invasion.")["owner"] == "ST"
    single = te.rule_placement("Using a single press statement, the ministry described the withdrawal of its forces.")
    assert single["owner"] != "RE"
    assert single["warrant"] == "W7" and single["default_applied"] is False
    neighbour = te.rule_placement("Neighbouring states signed a ceasefire.")
    assert neighbour is None or neighbour["owner"] != "MA"


def test_frozen_rule_stage_does_not_regress():
    rows = _rows(FROZEN)
    assert len(rows) == 203
    hit = {k: 0 for k in ("owner", "cell", "warrant", "method")}
    for r in rows:
        got = te.rule_placement(r["claim"]) or {}
        for key in hit:
            hit[key] += int(got.get(key) == r[key])
    # Owner floor is the word-boundary pass. Cell stays below that pass because a
    # cell with no cue is left blank rather than labelled A1.
    assert hit["owner"] >= 138, hit
    assert hit["warrant"] >= 81, hit
    assert hit["method"] >= 90, hit
