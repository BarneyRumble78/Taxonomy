"""Draft lens cards from the pyramids (Roadmap D1).

Writes cards/lens/<FIELD>.json: one field card plus one card per key-line cell.
Cards are drafts (status "draft"): parsed from existing text, then reviewed.
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "cards" / "lens"
CODES = "PH CH BI EA MD EN CS MS EC BU ST PO LA PL HI LN AR RE ED DE AG EV IS IK".split()


def section(s, n):
    m = re.search(rf"^##+ {n}\.[^\n]*\n(.*?)(?=^##+ \d+\.|\Z)", s, re.S | re.M)
    return m.group(1) if m else ""


def clean(t):
    t = re.sub(r"\*\*|`", "", t)
    return re.sub(r"\s+", " ", t).strip()


def first_sentence(t, limit=260):
    t = clean(t)
    m = re.match(r"(.+?[.?!])(\s|$)", t)
    return (m.group(1) if m else t)[:limit]


def table_rows(text):
    rows = []
    for line in text.splitlines():
        if line.startswith("|") and not re.match(r"^\|\s*-", line):
            cells = [clean(c) for c in line.strip().strip("|").split("|")]
            rows.append(cells)
    return rows[1:] if rows else []


def bullets(text):
    return [clean(m) for m in re.findall(r"^\s*[-*]\s+(.+)$", text, re.M)]


def scqa_question(text):
    m = re.search(r"(?:\*\*)?Question\.?(?:\*\*)?\s*(.+?)(?:\n|\*\*Answer|$)", text)
    if m:
        return first_sentence(m.group(1))
    m = re.search(r"SCQA[^\n]*?([A-Z][^.?]*\?)", text)
    if m:
        return clean(m.group(1))
    qs = re.findall(r"([A-Z][^.?\n]{10,200}\?)", text)
    return clean(qs[0]) if qs else ""


def build(code):
    s = (ROOT / "pyramids" / f"{code}.md").read_text(encoding="utf-8")
    name = s.splitlines()[0].split("—", 1)[-1].strip()
    sec1, sec3, sec4 = section(s, 1), section(s, 3), section(s, 4)
    sec5, sec6, sec8, sec9 = section(s, 5), section(s, 6), section(s, 8), section(s, 9)
    sec11 = section(s, 11)
    dim = re.search(r"[Dd]imension:?\s*\*{0,2}([^*\n.]+)", sec3)
    methods = [f"{r[1]} ({r[2]})" for r in table_rows(sec5.split("Heuristics")[0]) if len(r) >= 3]
    heur_txt = sec5.split("Heuristics", 1)[1] if "Heuristics" in sec5 else ""
    heur = bullets(heur_txt) or [clean(x) for x in re.split(r";\s*", clean(heur_txt.split("\n", 1)[-1])) if x.strip()][:12]
    wrows = {r[0].split()[0]: r for r in table_rows(sec6) if r and re.match(rf"{code}\.O\.A\d", r[0])}
    refused = [f"{r[0]} → {r[1]}" for r in table_rows(sec9) if len(r) >= 2]
    rules = [clean(x) for x in re.findall(r"^\s*\d+\.\s+(.+)$", sec8, re.M)]
    opens = [clean(x) for x in re.findall(r"OPEN:?\s*([^\n]+)", sec11)]
    contested = [clean(x) for x in re.findall(r"CONTESTED:?\s*([^\n]+)", sec11)]
    cards = [{
        "id": code, "field": code, "name": name,
        "question": f"What does {name.lower()} establish about this subject, divided by {clean(dim.group(1)) if dim else 'its key line'}?",
        "scqa_question": scqa_question(sec1),
        "look_for": [], "find_out": methods, "settles": [], "breaks": [],  # filled from cells below
        "rules_of_thumb": heur[:12], "collisions": rules[:12] + refused[:8],
        "open": opens + contested, "status": "draft", "source": f"pyramids/{code}.md",
    }]
    blocks = re.split(rf"^#+\s+(?:\*\*)?({code}\.O\.A\d)\b", sec4, flags=re.M)
    for i in range(1, len(blocks), 2):
        cid, body = blocks[i], blocks[i + 1]
        title = clean(body.split("\n", 1)[0]).strip(" .*")
        objs = [b for b in bullets(body) if re.match(rf"{code}\.O\.A\d\.\d", b)]
        look = [re.sub(rf"^{code}\.O\.A[\d.]+\s*", "", o)[:240] for o in objs]
        w = wrows.get(cid, [])
        settles = re.findall(r"W\d+", " ".join(w[1:3])) if w else []
        breaks = [w[-1]] if w else []
        cards.append({
            "id": cid, "field": code, "name": title,
            "question": scqa_question(body) or f"What does this subject show about {title.lower()}?",
            "look_for": look, "find_out": methods, "settles": sorted(set(settles), key=lambda x: int(x[1:])),
            "breaks": breaks, "rules_of_thumb": [], "collisions": [r for r in rules if cid in r][:6],
            "open": [o for o in opens + contested if cid in o], "status": "draft", "source": f"pyramids/{code}.md",
        })
    cards[0]["look_for"] = [f"{c['id']} {c['name']}" for c in cards[1:]]
    cards[0]["settles"] = sorted({w for c in cards[1:] for w in c["settles"]}, key=lambda x: int(x[1:]))
    for c in cards[1:]:
        # Questions written for filing ("which claims ... own", "placed once") are rewritten for applying.
        if re.search(r"\b(own|owns|placed|place|placement|home|classif)", c["question"], re.I):
            c["question"] = f"What does this subject show about {c['name'].lower()}, and what would settle it?"
    return cards


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    total = 0
    for code in CODES:
        cards = build(code)
        (OUT / f"{code}.json").write_text(json.dumps(cards, indent=1, ensure_ascii=False), encoding="utf-8")
        total += len(cards)
        empty = [c["id"] for c in cards[1:] if not c["look_for"]]
        print(f"{code}: {len(cards)-1} cells" + (f"  (no named objects parsed: {', '.join(empty)})" if empty else ""))
    print("total cards", total)


if __name__ == "__main__":
    main()
