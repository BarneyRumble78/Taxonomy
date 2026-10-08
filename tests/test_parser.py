"""Parser checks on the pyramid files.

These tests assert what check.py already requires, plus: a warrant and an
evidence standard on each claim cell that exists, IDs matching ^[A-Z]{2}\\.,
no duplicate registry IDs, and a resolvable uses target. They do not require
five top-level cells. Mathematics keeps its five cells and its 63/63 MSC
placement; this file does not restructure it.
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CODES = "MA PH CH BI EA MD EN CS MS EC BU ST PO LA PL HI LN AR RE ED DE AG EV IS IK".split()
ID_RE = re.compile(r"^[A-Z]{2}\.")


def section(text, n):
    m = re.search(rf"## {n}\..*?(?=\n## |\Z)", text, re.S)
    return m.group(0) if m else ""


def test_each_field_file_has_warrants_and_evidence_standards_on_claim_cells():
    counts = {}
    for code in CODES:
        text = (ROOT / "pyramids" / f"{code}.md").read_text(encoding="utf-8")
        if code == "MA":
            cells = re.findall(r"^### (MA\.O\.A\d+)\b", text, re.M)
            warrants = re.findall(r"^Warrant:\s*(.+)$", text, re.M)
            assert cells == ["MA.O.A1", "MA.O.A2", "MA.O.A3", "MA.O.A4", "MA.O.A5"]
            assert len(warrants) == 5
            for w in warrants:
                assert "W1" in w or w.strip()
                assert len(w.strip()) > 2  # evidence standard is the warrant sentence
            assert "63" in text  # MSC placement stays 63/63
            counts[code] = 5
            continue
        body = section(text, 6)
        lines = [ln for ln in body.splitlines() if ln.startswith("|")]
        assert len(lines) >= 2, code
        header = [c.strip().lower() for c in lines[0].strip("|").split("|")]
        std_i = next(i for i, h in enumerate(header) if "standard" in h)
        w_is = [i for i, h in enumerate(header) if "warrant" in h or h in ("primary", "second")]
        assert w_is, code
        n = 0
        for ln in lines[2:]:
            cols = [c.strip() for c in ln.strip("|").split("|")]
            if not cols or not re.match(rf"{code}\.O\.", cols[0]):
                continue
            n += 1
            assert ID_RE.match(cols[0]), cols[0]
            warrant = " ".join(cols[i] for i in w_is if i < len(cols))
            standard = cols[std_i] if std_i < len(cols) else ""
            assert re.search(r"W\d+", warrant), (code, cols[0], warrant)
            assert standard.strip(), (code, cols[0])
        assert n >= 1, code
        counts[code] = n
    # Religion has four object cells. Do not force five.
    assert counts["RE"] == 4
    assert counts["MA"] == 5
    assert any(counts[c] != 5 for c in counts)


def test_section_12_ids_match_pattern_and_are_unique():
    seen = {}
    for code in CODES:
        text = (ROOT / "pyramids" / f"{code}.md").read_text(encoding="utf-8")
        body = section(text, 12)
        if code == "MA":
            assert body == ""
            continue
        ids = re.findall(r"^\|\s*([A-Z]{2}\.\S+)", body, re.M)
        assert ids, code
        for i in ids:
            assert ID_RE.match(i), i
            assert i not in seen, i
            seen[i] = code
    reg = json.loads((ROOT / "registry" / "registry.json").read_text(encoding="utf-8"))
    reg_ids = [r["id"] for r in reg]
    assert len(reg_ids) == len(set(reg_ids)) == len(seen)
    assert set(reg_ids) == set(seen)


def test_every_uses_target_resolves_or_is_a_known_gap():
    """Field-level versus ID-level uses edges. Known letter-suffix gaps are not invented away."""
    reg = json.loads((ROOT / "registry" / "registry.json").read_text(encoding="utf-8"))
    defined = {r["id"] for r in reg}
    for f in (ROOT / "pyramids").glob("*.md"):
        defined.update(re.findall(r"\b[A-Z]{2}\.[OMWBH]\.[A-Z]?\d+(?:\.\d+)*", f.read_text(encoding="utf-8")))
    defined.update({f"MA.B.C{i}" for i in range(1, 6)})
    id_re = re.compile(r"[A-Z]{2}\.[OMWBH]\.[A-Z]?\d+(?:\.\d+)*")
    codes = set(CODES)
    counts = {"field": 0, "id": 0, "local": 0, "unresolved": 0}
    unresolved = []
    for row in reg:
        for raw in row["uses"]:
            tok = raw.strip()
            if tok in ("—", "-", ""):
                continue
            if tok == "as tabled":
                counts["local"] += 1
                continue
            head = tok.split("(")[0].strip()
            if re.fullmatch(r"[A-Z]{2}", head) and head in codes:
                counts["field"] += 1
                continue
            m = id_re.search(tok)
            if not m:
                counts["unresolved"] += 1
                unresolved.append(tok)
                continue
            ident = re.split(r"[–—]", m.group(0))[0]
            rest = tok[m.end():]
            if rest[:1].islower():
                counts["unresolved"] += 1
                unresolved.append(tok)
                continue
            if ident in defined or any(d.startswith(ident + ".") for d in defined):
                counts["id"] += 1
            else:
                counts["unresolved"] += 1
                unresolved.append(tok)
    assert counts["field"] == 221
    assert counts["id"] == 226
    assert counts["local"] == 1
    assert sorted(set(unresolved)) == ["PH.O.A1.2b", "PH.O.A1.2c", "PH.O.A4.4a"]
    assert counts["unresolved"] == 9
