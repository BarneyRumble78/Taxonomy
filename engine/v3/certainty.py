"""Stated certainty of a claim, and the ceiling a held warrant allows (R19).

The cue list is engine/certainty_lexicon.json so the JavaScript port can share it.
Levels run hedged < qualified < assertive < absolute. The strongest cue wins.
"""
import json, re
from pathlib import Path

_LEX = json.loads((Path(__file__).resolve().parents[1] / "certainty_lexicon.json").read_text(encoding="utf-8"))
LEVELS = tuple(_LEX["levels"])
CEILING = dict(_LEX["ceiling"])
_RANK = {name: i for i, name in enumerate(LEVELS)}
_CUES = []
for level in reversed(LEVELS):
    for cue in sorted(_LEX["cues"].get(level, []), key=len, reverse=True):
        _CUES.append((level, cue, re.compile(r"\b" + re.escape(cue) + r"\b", re.I)))


def certainty(text):
    """Return {level, cues}. No cue means hedged."""
    found = []
    best = "hedged"
    raw = text or ""
    for level, cue, pat in _CUES:
        if pat.search(raw):
            found.append(cue)
            if _RANK[level] > _RANK[best]:
                best = level
    return {"level": best, "cues": found}


def ceiling_ok(level, warrant_held):
    """True when the stated level does not exceed the warrant's ceiling."""
    cap = CEILING.get(warrant_held, "hedged") if warrant_held else "hedged"
    return _RANK.get(level, 0) <= _RANK.get(cap, 0)


def rank(level):
    return _RANK.get(level, 0)


def warrant_ceiling(code):
    return CEILING.get(code, "hedged") if code else "hedged"
