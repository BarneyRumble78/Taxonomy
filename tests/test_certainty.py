"""Certainty cues and warrant ceilings (R19). The word true is not a level."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "engine" / "v3"))
from certainty import LEVELS, ceiling_ok, certainty


def test_levels_and_strongest_cue():
    assert LEVELS == ("hedged", "qualified", "assertive", "absolute")
    assert certainty("hello")["level"] == "hedged"
    assert certainty("This might hold.")["level"] == "hedged"
    assert certainty("The trial shows an effect.")["level"] == "assertive"
    assert certainty("This conclusively proves it.")["level"] == "absolute"
    assert "true" not in LEVELS


def test_is_is_assertive_not_absolute():
    found = certainty("The bridge was finished.")
    assert found["level"] == "assertive"
    assert "was" in found["cues"]


def test_absolute_and_universal_wording():
    sentence = "This supplement definitely cures anxiety in everyone who takes it."
    found = certainty(sentence)
    assert found["level"] == "absolute"
    for cue in ("definitely", "cures", "everyone"):
        assert cue in found["cues"]
    more = [
        "The drug cures all patients with the infection.",
        "This vaccine is guaranteed to prevent flu in everybody.",
        "The pill cures arthritis in 100% of cases.",
        "This treatment is proven to cure the disease without doubt.",
        "The benefit is certainly real.",
        "It always works.",
        "It never fails.",
        "The result is undeniably settled.",
    ]
    for text in more:
        assert certainty(text)["level"] == "absolute", text


def test_real_hedges_stay_hedged():
    for text in (
        "This supplement may help some people with anxiety.",
        "The drug might treat some infections.",
        "Exercise likely helps some patients.",
        "The study suggests a small benefit.",
        "This might hold.",
    ):
        found = certainty(text)
        assert found["level"] == "hedged", (text, found)
        assert found["level"] != "absolute"


def test_ceilings():
    assert ceiling_ok("absolute", "W1")
    assert ceiling_ok("assertive", "W4")
    assert not ceiling_ok("absolute", "W4")
    assert ceiling_ok("qualified", "W9")
    assert not ceiling_ok("assertive", "W9")
    assert ceiling_ok("hedged", None)
    assert not ceiling_ok("assertive", None)
