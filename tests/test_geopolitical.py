"""Held-out geopolitical claims from the 10 Oct 2026 live trials.

The case-spec files were not in this repository. These thirteen sentences are the
failure classes named in that note: territorial control, naval mines, Yemen,
Italy, Albania, an official statement, claimed responsibility, satellite imagery,
testimony and an event count. Labels follow Standard v2. Conduct of force is ST.
Relations among states are PO. An official statement, testimony or a claim of
responsibility is W7. Imagery and a count of events are W4.

None of these sentences is a lexicon cue. The frozen 203-claim set is scored
only as a regression floor.
"""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "engine"))
import taxonomy_engine as te

HELD = Path(__file__).resolve().parent / "geopolitical_heldout.tsv"
FROZEN = ROOT / "pilot" / "heldout.tsv"
# Scores on pilot/heldout.tsv after the boundary matcher. They must not fall back
# toward the main-branch scores (owner 124, cell 94, warrant 77, method 86).
FLOOR = {"owner": 138, "cell": 106, "warrant": 81, "method": 93}
# Proper nouns from the trial sentences. They must not be added as cues.
PROPER = ("zarichne", "hormuz", "yemen", "houthi", "albania", "albanian", "italian", "italy", "oman", "baltic", "irgc")


def _rows(path):
    return list(csv.DictReader(path.open(encoding="utf-8"), delimiter="\t"))


def test_geopolitical_heldout_matches_standard_labels():
    rows = _rows(HELD)
    assert len(rows) == 13
    for r in rows:
        got = te.classify(r["claim"])
        assert got is not None, r["id"]
        assert got["owner"] == r["owner"], (r["id"], got["owner"], r["claim"])
        assert got["cell"] == r["cell"], (r["id"], got["cell"], r["claim"])
        assert got["warrant"] == r["warrant"], (r["id"], got["warrant"], r["claim"])


def test_heldout_claims_are_not_lexicon_cues():
    blob = json.dumps(te.LEXICON, ensure_ascii=False).lower()
    for name in PROPER:
        assert name not in blob, name
    for r in _rows(HELD):
        assert r["claim"].lower() not in blob


def test_frozen_203_does_not_regress():
    rows = _rows(FROZEN)
    assert len(rows) == 203
    hit = {"owner": 0, "cell": 0, "warrant": 0, "method": 0}
    for r in rows:
        got = te.classify(r["claim"]) or {}
        for key in hit:
            hit[key] += int(got.get(key) == r[key])
    for key, floor in FLOOR.items():
        assert hit[key] >= floor, (key, hit[key], floor)
