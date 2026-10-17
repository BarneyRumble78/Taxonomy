"""Certainty cues and warrant ceilings (R19). The word true is not a level."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "engine" / "v3"))
from certainty import LEVELS, ceiling_ok, certainty


def test_levels_and_strongest_cue():
    assert LEVELS == ("hedged", "qualified", "assertive", "absolute")
    assert certainty("hello")["level"] == "hedged"
    assert certainty("This might hold.")["level"] == "qualified"
    assert certainty("The trial shows an effect.")["level"] == "assertive"
    assert certainty("This conclusively proves it.")["level"] == "absolute"
    assert "true" not in LEVELS


def test_is_is_assertive_not_absolute():
    found = certainty("The bridge was finished.")
    assert found["level"] == "assertive"
    assert "was" in found["cues"]


def test_ceilings():
    assert ceiling_ok("absolute", "W1")
    assert ceiling_ok("assertive", "W4")
    assert not ceiling_ok("absolute", "W4")
    assert ceiling_ok("qualified", "W9")
    assert not ceiling_ok("assertive", "W9")
    assert ceiling_ok("hedged", None)
    assert not ceiling_ok("assertive", None)
