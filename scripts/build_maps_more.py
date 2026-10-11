"""Second batch of published taxonomies, split into each owning field by cell.

  MeSH 2026 trees   sources/mesh_trees_2026.json (from NLM desc2026.xml)  -> maps/<FIELD>/mesh2026.json
  ACM CCS 2012      sources/acm_ccs2012.xml (ACM)                          -> maps/<FIELD>/acm_ccs2012.json
  LCC outlines      sources/lcco_*.pdf (Library of Congress)               -> maps/<FIELD>/lcc.json
Nodes whose parent sits in another field are re-rooted (level 1 in that field, with moved_from).
Run after scripts/build_maps.py; updates maps/index.json.
"""
import json, re, subprocess
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "sources"
DATE = "2026-10-12"


def split_write(name, meta, nodes):
    """nodes: dicts with id, parent, level, taxonomy_cell. Write one file per owning field."""
    owner = {n["id"]: n["taxonomy_cell"].split(".")[0] for n in nodes}
    per = defaultdict(list)
    for n in nodes:
        f = owner[n["id"]]
        p = n.get("parent")
        if p and owner.get(p) != f:
            n = dict(n, parent=None, moved_from=p)
        per[f].append(n)
    for f, ns in per.items():
        # recompute levels inside the field
        by = {n["id"]: n for n in ns}
        def depth(n, seen=0):
            return 1 if not n.get("parent") or n["parent"] not in by or seen > 30 else 1 + depth(by[n["parent"]], seen + 1)
        for n in ns:
            n["level"] = depth(n)
        d = ROOT / "maps" / f
        d.mkdir(parents=True, exist_ok=True)
        (d / name).write_text(json.dumps(dict(meta, nodes=ns), ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    return {f: len(ns) for f, ns in per.items()}


# ---------- MeSH ----------
MESH_CAT = {"A": ("Anatomy", "BI.O.A3"), "B": ("Organisms", "BI.O.A3"), "C": ("Diseases", "MD.O.A1"),
            "D": ("Chemicals and Drugs", "CH.O.A1"), "E": ("Analytical, Diagnostic and Therapeutic Techniques, and Equipment", "MD.O.A3"),
            "F": ("Psychiatry and Psychology", "MS.O.A1"), "G": ("Phenomena and Processes", "BI.O.A2"),
            "H": ("Disciplines and Occupations", "IS.O.A3"), "I": ("Anthropology, Education, Sociology, and Social Phenomena", "MS.O.A5"),
            "J": ("Technology, Industry, and Agriculture", "EN.O.A1"), "K": ("Humanities", "AR.O.A4"),
            "L": ("Information Science", "IS.O.A4"), "M": ("Named Groups", "MS.O.A5"), "N": ("Health Care", "MD.O.A5"),
            "V": ("Publication Characteristics", "IS.O.A2"), "Z": ("Geographicals", "EA.O.A5")}
MESH_TOP = {  # tree-number prefixes that belong elsewhere than their category
    "A11": "BI.O.A2", "A15": "MD.O.A2", "B04": "MD.O.A2", "C23": "MD.O.A3", "C26": "MD.O.A1",
    "D27": "MD.O.A4", "D20": "BI.O.A2", "D12": "BI.O.A2", "D13": "BI.O.A1", "D23": "BI.O.A2",
    "E02": "MD.O.A4", "E04": "MD.O.A4", "E05": "MD.O.A3", "E07": "EN.O.A1",
    "F01": "MS.O.A3", "F02": "MS.O.A1", "F03": "MD.O.A1", "F04": "MS.O.A4",
    "G01": "PH.O.A1", "G02": "CH.O.A3", "G03": "BI.O.A2", "G04": "BI.O.A2", "G05": "BI.O.A1",
    "G06": "BI.O.A3", "G07": "BI.O.A3", "G08": "BI.O.A3", "G09": "MD.O.A2", "G10": "BI.O.A3",
    "G11": "BI.O.A3", "G12": "MD.O.A2", "G13": "BI.O.A2", "G14": "BI.O.A3", "G15": "BI.O.A1",
    "G16": "BI.O.A4", "G17": "IS.O.A4",
    "I01": "MS.O.A5", "I02": "ED.O.A5", "I03": "MS.O.A3", "J01": "EN.O.A1", "J02": "AG.O.A4", "J03": "EN.O.A1",
    "K01": "AR.O.A4", "N01": "MD.O.A5", "N02": "MD.O.A5", "N03": "BU.O.A3", "N04": "MD.O.A5", "N05": "MD.O.A5", "N06": "MD.O.A5",
    "Z01": "EA.O.A5",
}


def mesh():
    trees = json.loads((SRC / "mesh_trees_2026.json").read_text())
    nodes = []
    for letter, (name, cell) in MESH_CAT.items():
        nodes.append({"id": f"MeSH:{letter}", "code": letter, "name": name, "level": 1, "parent": None, "taxonomy_cell": cell})
    for tn, ui, nm in sorted(trees):
        parent = f"MeSH:{tn.rsplit('.', 1)[0]}" if "." in tn else f"MeSH:{tn[0]}"
        cell = MESH_TOP.get(tn[:3], MESH_CAT[tn[0]][1])
        nodes.append({"id": f"MeSH:{tn}", "code": tn, "ui": ui, "name": nm, "level": tn.count(".") + 2,
                      "parent": parent, "taxonomy_cell": cell})
    meta = {"scheme": "MeSH 2026 (tree numbers)", "source": "https://nlmpubs.nlm.nih.gov/projects/mesh/MESH_FILES/xmlmesh/desc2026.gz",
            "retrieved": DATE, "licence": "NLM Terms and Conditions (free; acknowledge NLM)",
            "note": "One node per tree position, so a descriptor in two trees appears twice (same ui)."}
    return split_write("mesh2026.json", meta, nodes)


# ---------- ACM CCS ----------
ACM_TOP = {"General and reference": "CS.O.A1", "Hardware": "EN.O.A4", "Computer systems organization": "CS.O.A3",
           "Networks": "CS.O.A3", "Software and its engineering": "CS.O.A1", "Theory of computation": "CS.O.A2",
           "Mathematics of computing": "CS.O.A2", "Information systems": "IS.O.A4", "Security and privacy": "CS.O.A5",
           "Human-centered computing": "CS.O.A3", "Computing methodologies": "CS.O.A4", "Applied computing": "CS.O.A3",
           "Social and professional topics": "CS.O.A5"}


def acm():
    import rdflib
    from rdflib.namespace import SKOS, RDF
    g = rdflib.Graph()
    g.parse(SRC / "acm_ccs2012.xml", format="xml")
    lab = {s: str(o) for s, o in g.subject_objects(SKOS.prefLabel)}
    sid = lambda u: "ACM:" + str(u).rsplit("/", 1)[-1].rsplit("#", 1)[-1]
    tops = {c for s in g.subjects(RDF.type, SKOS.ConceptScheme) for c in g.objects(s, SKOS.hasTopConcept)}
    parent = {}
    for c, b in g.subject_objects(SKOS.broader):
        parent.setdefault(c, b)  # polyhierarchy: keep first broader
    def top_of(c, k=0):
        return c if c in tops or c not in parent or k > 20 else top_of(parent[c], k + 1)
    nodes = []
    for c in lab:
        t = top_of(c)
        nodes.append({"id": sid(c), "code": sid(c)[4:], "name": lab[c], "level": 1,
                      "parent": sid(parent[c]) if c in parent and c not in tops else None,
                      "taxonomy_cell": ACM_TOP.get(lab.get(t, ""), "CS.O.A1")})
    meta = {"scheme": "ACM Computing Classification System 2012", "source": "https://dl.acm.org/ccs (acm_ccs2012 SKOS XML)",
            "retrieved": DATE, "licence": "ACM: free for non-commercial and educational use",
            "note": "Poly-hierarchy reduced to the first broader concept."}
    return split_write("acm_ccs2012.json", meta, nodes)


# ---------- LCC outlines ----------
LCC = {
    "B": "PL.O.A1", "BC": "PL.O.A3", "BD": "PL.O.A1", "BF": "MS.O.A1", "BH": "PL.O.A4", "BJ": "PL.O.A4",
    "BL": "RE.O.A1", "BM": "RE.O.A4", "BP": "RE.O.A4", "BQ": "RE.O.A4", "BR": "RE.O.A4", "BS": "RE.O.A2",
    "BT": "RE.O.A1", "BV": "RE.O.A3", "BX": "RE.O.A4",
    "C": "HI.O.A1", "CB": "HI.O.A4", "CC": "HI.O.A1", "CD": "IS.O.A5", "CE": "HI.O.A2", "CJ": "HI.O.A1",
    "CN": "HI.O.A1", "CR": "HI.O.A5", "CS": "HI.O.A1", "CT": "HI.O.A1",
    "H": "MS.O.A5", "HA": "MA.O.A5", "HB": "EC.O.A1", "HC": "EC.O.A4", "HD": "EC.O.A2", "HE": "EC.O.A2",
    "HF": "BU.O.A4", "HG": "BU.O.A2", "HJ": "EC.O.A5", "HM": "MS.O.A5", "HN": "MS.O.A5", "HQ": "MS.O.A4",
    "HS": "MS.O.A5", "HT": "MS.O.A5", "HV": "MS.O.A5", "HX": "PO.O.A1",
    "J": "PO.O.A2", "JA": "PO.O.A2", "JC": "PO.O.A1", "JF": "PO.O.A2", "JJ": "PO.O.A2", "JK": "PO.O.A2",
    "JL": "PO.O.A2", "JN": "PO.O.A2", "JQ": "PO.O.A2", "JS": "PO.O.A4", "JV": "PO.O.A4", "JX": "LA.O.A1",
    "JZ": "PO.O.A5",
    "K": "LA.O.A1", "KB": "RE.O.A2", "KBM": "RE.O.A2", "KBP": "RE.O.A2", "KBR": "RE.O.A4", "KBU": "RE.O.A4",
    "KDZ": "LA.O.A1", "KE": "LA.O.A1", "KF": "LA.O.A1", "KG": "LA.O.A1", "KH": "LA.O.A1", "KZ": "LA.O.A1",
    "L": "ED.O.A1", "LA": "ED.O.A5", "LB": "ED.O.A3", "LC": "ED.O.A2", "LD": "ED.O.A5", "LE": "ED.O.A5",
    "LF": "ED.O.A5", "LG": "ED.O.A5", "LH": "ED.O.A5", "LJ": "ED.O.A5", "LT": "ED.O.A1",
    "M": "AR.O.A1", "ML": "AR.O.A4", "MT": "AR.O.A1",
    "N": "AR.O.A1", "NA": "DE.O.A2", "NB": "AR.O.A1", "NC": "AR.O.A1", "ND": "AR.O.A1", "NE": "AR.O.A1",
    "NK": "DE.O.A2", "NX": "AR.O.A4",
    "P": "LN.O.A2", "PA": "LN.O.A5", "PB": "LN.O.A5", "PC": "LN.O.A5", "PD": "LN.O.A5", "PE": "LN.O.A5",
    "PF": "LN.O.A5", "PG": "LN.O.A5", "PH": "LN.O.A5", "PJ": "LN.O.A5", "PK": "LN.O.A5", "PL": "LN.O.A5",
    "PM": "LN.O.A5", "PN": "AR.O.A3", "PQ": "AR.O.A3", "PR": "AR.O.A3", "PS": "AR.O.A3", "PT": "AR.O.A3",
    "PZ": "AR.O.A3",
    "Q": "PL.O.A5", "QA": "MA.O.A2", "QB": "PH.O.A3", "QC": "PH.O.A1", "QD": "CH.O.A1", "QE": "EA.O.A1",
    "QH": "BI.O.A3", "QK": "BI.O.A3", "QL": "BI.O.A3", "QM": "BI.O.A3", "QP": "BI.O.A2", "QR": "BI.O.A3",
    "Z": "IS.O.A1", "ZA": "IS.O.A4",
    "D": "HI.O.A4",
    # G Geography, anthropology, recreation
    "G": "EA.O.A5", "GA": "EA.O.A5", "GB": "EA.O.A4", "GC": "EA.O.A4", "GE": "EV.O.A2", "GF": "EV.O.A1",
    "GN": "MS.O.A5", "GR": "AR.O.A4", "GT": "MS.O.A5", "GV": "MS.O.A4",
    # R Medicine
    "R": "MD.O.A5", "RA": "MD.O.A5", "RB": "MD.O.A2", "RC": "MD.O.A1", "RD": "MD.O.A4", "RE": "MD.O.A1",
    "RF": "MD.O.A1", "RG": "MD.O.A1", "RJ": "MD.O.A1", "RK": "MD.O.A4", "RL": "MD.O.A1", "RM": "MD.O.A4",
    "RS": "MD.O.A4", "RT": "MD.O.A4", "RV": "MD.O.A4", "RX": "MD.O.A4", "RZ": "MD.O.A4",
    # S Agriculture
    "S": "AG.O.A5", "SB": "AG.O.A2", "SD": "AG.O.A2", "SF": "AG.O.A2", "SH": "AG.O.A2", "SK": "AG.O.A5",
    # T Technology
    "T": "EN.O.A1", "TA": "EN.O.A1", "TC": "EN.O.A2", "TD": "EV.O.A4", "TE": "EN.O.A1", "TF": "EN.O.A1",
    "TG": "EN.O.A1", "TH": "DE.O.A5", "TJ": "EN.O.A3", "TK": "EN.O.A4", "TL": "EN.O.A2", "TN": "EN.O.A5",
    "TP": "EN.O.A5", "TR": "AR.O.A1", "TS": "EN.O.A5", "TT": "AR.O.A1", "TX": "DE.O.A1",
    # U Military science, V Naval science: strategy
    "U": "ST.O.A2", "UA": "ST.O.A1", "UB": "ST.O.A1", "UC": "ST.O.A4", "UD": "ST.O.A3", "UE": "ST.O.A3",
    "UF": "ST.O.A3", "UG": "ST.O.A3", "UH": "ST.O.A4",
    "V": "ST.O.A2", "VA": "ST.O.A1", "VB": "ST.O.A1", "VC": "ST.O.A4", "VD": "ST.O.A4", "VE": "ST.O.A3",
    "VF": "ST.O.A3", "VG": "ST.O.A4", "VK": "EN.O.A2", "VM": "EN.O.A2",
    # A General works
    "A": "IS.O.A1", "AC": "IS.O.A1", "AE": "IS.O.A1", "AG": "IS.O.A1", "AI": "IS.O.A4", "AM": "HI.O.A5",
    "AN": "IS.O.A1", "AP": "IS.O.A1", "AS": "IS.O.A3", "AY": "IS.O.A1", "AZ": "HI.O.A4",
}
for _s in ("DA DAW DB DC DD DE DF DG DH DJ DJK DK DL DP DQ DR DS DT DU DX").split():
    LCC[_s] = "HI.O.A4"
LINE = re.compile(r"^([A-Z]{1,3})([\d.]+(?:-[\d.]+)?)?(\s+)(\S.*)$")


def lcc():
    nodes = []
    for pdf in sorted(SRC.glob("lcco_*.pdf")):
        text = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True).stdout
        stack = []  # (indent, id)
        sub = None
        for raw in text.splitlines():
            m = re.match(r"^Subclass ([A-Z]{1,3})\s*$", raw.strip())
            if m:
                sub = m.group(1)
                if sub not in LCC:
                    sub = None
                    continue
                sid = f"LCC:{sub}"
                if not any(n["id"] == sid for n in nodes):
                    nodes.append({"id": sid, "code": sub, "name": "", "level": 1, "parent": None, "taxonomy_cell": LCC[sub]})
                stack = []
                continue
            m = LINE.match(raw)
            if not sub or not m or not m.group(2) or m.group(1) != sub:
                continue  # headings, scope notes and page furniture
            code = m.group(1) + m.group(2)
            name_col = len(m.group(1) + m.group(2) + m.group(3))
            name = m.group(4).strip()
            while stack and stack[-1][0] >= name_col:
                stack.pop()
            nid = f"LCC:{code}"
            if any(n["id"] == nid for n in nodes[-50:]):
                continue
            parent = stack[-1][1] if stack else f"LCC:{sub}"
            nodes.append({"id": nid, "code": code, "name": name, "level": len(stack) + 2, "parent": parent,
                          "taxonomy_cell": LCC[sub]})
            stack.append((name_col, nid))
    names = {}
    for pdf in sorted(SRC.glob("lcco_*.pdf")):
        text = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True).stdout
        for m in re.finditer(r"^Subclass ([A-Z]{1,3}) {2,}(\S.*)$", text, re.M):
            names[m.group(1)] = m.group(2).strip()
    for n in nodes:
        if n["level"] == 1:
            n["name"] = names.get(n["code"], n["code"])
    meta = {"scheme": "Library of Congress Classification outline", "source": "https://www.loc.gov/catdir/cpso/lcco/ (class PDFs A, B, C, D, G, H, J, K, L, M, N, P, Q, R, S, T, U, V, Z)",
            "retrieved": DATE, "licence": "US government work (public domain)",
            "note": "Classes E-F (history of the Americas) were not downloadable; W and the rest of Q-level detail not taken."}
    return split_write("lcc.json", meta, nodes)


def main():
    index = json.loads((ROOT / "maps" / "index.json").read_text())
    for name, fn, scheme in (("mesh2026.json", mesh, "MeSH 2026"), ("acm_ccs2012.json", acm, "ACM CCS 2012"), ("lcc.json", lcc, "LCC outline")):
        for f, n in fn().items():
            index[f]["maps"][scheme] = n
    for f, p in (("MD", "mesh2026.json"), ("CS", "acm_ccs2012.json"), ("RE", "lcc.json"), ("LA", "lcc.json"), ("ST", "lcc.json"), ("PO", "lcc.json"), ("HI", "lcc.json"), ("LN", "lcc.json"), ("AR", "lcc.json"), ("ED", "lcc.json")):
        index[f]["primary"] = p
    (ROOT / "maps" / "index.json").write_text(json.dumps(index, indent=1, ensure_ascii=False), encoding="utf-8")
    for f, v in index.items():
        print(f, v["primary"], v["maps"])


if __name__ == "__main__":
    main()
