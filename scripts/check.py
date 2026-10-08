"""Conformance checks across pyramids/: key-line agreement (R7), stated sub-cell counts (R2), dangling IDs (R1/R12)."""
import re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
CODES = "MA PH CH BI EA MD EN CS MS EC BU ST PO LA PL HI LN AR RE ED DE AG EV IS IK".split()
IDRE = re.compile(r"\b(%s)\.([OMWB])\.([A-Z]?[0-9]+(?:\.[0-9]+)*)" % "|".join(CODES))
defined, refs, problems = set(), [], []
for f in sorted((ROOT / "pyramids").glob("*.md")):
    code, s = f.stem, f.read_text(encoding="utf-8")
    for m in IDRE.finditer(s):
        i = m.group(0)
        (defined.add(i) if m.group(1) == code else refs.append((code, i)))
    if code in ("MA", "ANZSRC45"):
        continue
    sec3 = re.search(r"## 3\..*?\n(.*?)\n## 4", s, re.S)
    mem = re.findall(r"^\d+\.\s+\*{0,2}(?:[A-Z]{2}\.O\.A\d\s*)?([^*\n(]+?)\*{0,2}(?:\s*\(.*)?\s*$", sec3.group(1), re.M) if sec3 else []
    v = (re.search(r"## 11\..*?(?=\n## 12|\Z)", s, re.S) or [""])[0]
    for x in mem:
        if x.strip().rstrip(".:").lower() not in v.lower():
            problems.append(f"R7 {code}: key-line member '{x.strip()}' not repeated in Validation")
    body = s.split("## 5.")[0]
    sub = set(re.findall(r"\b%s\.O\.A\d\.\d+\b(?!\.\d)" % code, body))
    m = re.search(r"Face O[^.\n]*?(\d+)\s*(?:cells)?\s*\+\s*(\d+)\s*sub-cells", s)
    if m and int(m.group(2)) != len(sub):
        problems.append(f"R2 {code}: states {m.group(2)} sub-cells, file defines {len(sub)}")
for c in ("MA.B.C1", "MA.B.C2", "MA.B.C3", "MA.B.C4", "MA.B.C5"):
    defined.add(c)
for code, r in refs:
    r = r.rstrip(".")
    if r not in defined and not any(d.startswith(r + ".") for d in defined):
        problems.append(f"R1 {code}: cites undefined {r}")
print("\n".join(sorted(set(problems))) or "All checks pass.")
sys.exit(1 if problems else 0)
