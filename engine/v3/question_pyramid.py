"""Build and check one question pyramid. No model calls.

A question pyramid answers one question. The governing thought is the
answer, in one sentence of at most 25 words. The key line is two to five
yes/no issues (Minto, Chapter 9, p. 163). Each issue carries evidence.
The hypothesis states what would defeat the answer (Minto, Appendix A).
This is not a field classification.
"""
import json
import re
from pathlib import Path

WORD = re.compile(r"[A-Za-z0-9]+(?:[-–][A-Za-z0-9]+)?")


def word_count(text):
    return len(WORD.findall(text or ""))


def validate(data):
    """Problems that keep the pyramid from being filed. Empty means valid."""
    problems = []
    thought = (data.get("governing_thought") or "").strip()
    if thought.count(".") != 1:
        problems.append("governing thought must be one sentence")
    if not thought or word_count(thought) > 25:
        problems.append("governing thought must be at most 25 words")
    points = ((data.get("key_line") or {}).get("points") or [])
    if not 2 <= len(points) <= 5:
        problems.append(f"key line has {len(points)} issues; two to five are required")
    for point in points:
        label = point.get("id") or "issue"
        if point.get("answer") not in ("yes", "no"):
            problems.append(f"{label} answer must be yes or no")
        issue = (point.get("issue") or "").strip()
        if not issue.endswith("?"):
            problems.append(f"{label} issue must be a yes/no question")
        evidence = point.get("evidence") or []
        if not evidence:
            problems.append(f"{label} needs evidence")
        for item in evidence:
            if not item.get("source") or not item.get("retrieved"):
                problems.append(f"{label} evidence needs a source and a retrieved date")
    hypothesis = data.get("hypothesis") or {}
    for key in ("null", "alternative", "test", "result"):
        if not (hypothesis.get(key) or "").strip():
            problems.append(f"hypothesis needs {key}")
    return problems


def render(data):
    """Markdown for a valid question pyramid."""
    intro = data.get("introduction") or {}
    lines = [
        f"# Question pyramid: {data.get('question') or ''}",
        "",
        "This is one problem pyramid. It is not the field classification.",
        "",
        "A question pyramid has a governing thought, an SCQ introduction, a key line of yes/no issues (Minto, Chapter 9, p. 163), evidence leaves linked to classification nodes, and a hypothesis test (Appendix A).",
        "",
        "## Introduction",
        "",
        f"**Situation.** {intro.get('situation') or ''}",
        "",
        f"**Complication.** {intro.get('complication') or ''}",
        "",
        f"**Question.** {intro.get('question') or data.get('question') or ''}",
        "",
        "## Governing thought",
        "",
        data.get("governing_thought") or "",
        "",
        "## Key line",
        "",
    ]
    key = data.get("key_line") or {}
    lines.append(
        f"Group of issues. Basis: {key.get('basis') or ''}. "
        f"Dimension: {key.get('mece_dimension') or ''}. Order: {key.get('order') or ''}."
    )
    lines.append("")
    for index, point in enumerate(key.get("points") or [], start=1):
        answer = (point.get("answer") or "").capitalize()
        cite = point.get("classification_id") or ""
        cite_bit = f" Uses `{cite}`." if cite else ""
        lines.append(f"{index}. **{answer}.** {point.get('issue') or ''}{cite_bit}")
    lines.extend(["", "## Evidence", ""])
    seen = set()
    for point in key.get("points") or []:
        for item in point.get("evidence") or []:
            marker = (item.get("source"), item.get("url"), item.get("finding"))
            if marker in seen:
                continue
            seen.add(marker)
            url = f", {item['url']}" if item.get("url") else ""
            lines.append(
                f"- {item.get('source') or ''}{url}, retrieved {item.get('retrieved') or ''}. "
                f"{item.get('finding') or ''}"
            )
    hypothesis = data.get("hypothesis") or {}
    lines.extend([
        "",
        "## Hypothesis",
        "",
        f"**Null.** {hypothesis.get('null') or ''}",
        "",
        f"**Alternative.** {hypothesis.get('alternative') or ''}",
        "",
        f"**Test.** {hypothesis.get('test') or ''}",
        "",
        f"**Result.** {hypothesis.get('result') or ''}",
        "",
        f"**Defeat.** {hypothesis.get('defeat') or ''}",
        "",
    ])
    return "\n".join(lines)


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))
