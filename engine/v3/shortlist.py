"""Candidate shortlists for a placement queue. No model calls.

Key-line cells are always offered. Other groups are added by word overlap,
up to the width. This does not replace the full catalog inside a prompt.
"""
import re

CELL = re.compile(r"^[A-Z]{2}\.P\.\d+$")
WORD = re.compile(r"[a-z0-9]+")


def ranked_shortlist(name, catalog, width=12):
    """Key-line cells first, then overlapping groups, capped at width."""
    words = set(WORD.findall((name or "").lower()))
    cells = []
    rest = []
    seen = set()
    for row in catalog or []:
        group_id = row.get("group_id") or ""
        if not group_id or group_id in seen:
            continue
        seen.add(group_id)
        if CELL.match(group_id):
            cells.append(row)
        else:
            rest.append(row)

    def score(row):
        text = f"{row.get('statement') or ''} {row.get('group_id') or ''}".lower()
        return len(words & set(WORD.findall(text)))

    rest.sort(key=lambda row: (-score(row), row.get("group_id") or ""))
    limit = int(width)
    if len(cells) >= limit:
        return cells
    chosen = list(cells)
    for row in rest:
        if len(chosen) >= limit:
            break
        if score(row) <= 0:
            continue
        chosen.append(row)
    return chosen
