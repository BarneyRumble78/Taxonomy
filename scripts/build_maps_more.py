"""Second batch of published taxonomies, split into each owning field by cell.

  MeSH 2026 trees   sources/mesh_trees_2026.json (from NLM desc2026.xml)  -> maps/<FIELD>/mesh2026.json
  ACM CCS 2012      sources/acm_ccs2012.xml (ACM)                          -> maps/<FIELD>/acm_ccs2012.json
  LCC outlines      sources/lcco_*.pdf (Library of Congress)               -> maps/<FIELD>/lcc.json
  PhilPapers        sources/philpapers_browse_20240924.html                -> maps/<FIELD>/philpapers.json
  APA PsycInfo      sources/apa_psycinfo_class.pdf                         -> maps/<FIELD>/psycinfo.json
  UNESCO Thesaurus  sources/unesco-thesaurus.rdf (Politics and government) -> maps/<FIELD>/unesco_politics.json
  GEMET             sources/gemet.rdf.gz                                   -> maps/<FIELD>/gemet.json
  Getty AAT         sources/aat_top.json (SPARQL, top levels)              -> maps/<FIELD>/aat.json
  ISKO IEKO         sources/isko_cyclo.html                                -> maps/<FIELD>/isko.json
  Glottolog         sources/glottolog_languages.csv + classification       -> maps/<FIELD>/glottolog.json
  ERIC Thesaurus    sources/eric_thesaurus.zip                             -> maps/<FIELD>/eric.json
  AGROVOC           sources/agrovoc_top.nt (top concepts from the core)    -> maps/<FIELD>/agrovoc.json
  ChEBI roles       sources/chebi_roles.obo                                -> maps/<FIELD>/chebi_roles.json
  IEEE Taxonomy     sources/ieee_taxonomy_jan2026.pdf                      -> maps/<FIELD>/ieee.json
Nodes whose parent sits in another field are re-rooted (level 1 in that field, with moved_from).
Run after scripts/build_maps.py; updates maps/index.json.
"""
import json, re, subprocess, gzip, csv, zipfile
from collections import defaultdict
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "sources"
DATE = "2026-10-12"
NEW = "2026-10-11"


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
# Rate and mechanism branches inside G02 Chemical Phenomena. The rest of G02
# stays on CH.O.A3 so equilibrium and structure are not emptied.
MESH_RATE = ("G02.111.490", "G02.130", "G02.380", "G02.607", "G02.700", "G02.740", "G02.750", "G02.785")


def mesh_cell(tn):
    cell = MESH_TOP.get(tn[:3], MESH_CAT[tn[0]][1])
    for pref in MESH_RATE:
        if tn == pref or tn.startswith(pref + "."):
            return "CH.O.A4"
    return cell


def mesh():
    trees = json.loads((SRC / "mesh_trees_2026.json").read_text())
    nodes = []
    for letter, (name, cell) in MESH_CAT.items():
        nodes.append({"id": f"MeSH:{letter}", "code": letter, "name": name, "level": 1, "parent": None, "taxonomy_cell": cell})
    for tn, ui, nm in sorted(trees):
        parent = f"MeSH:{tn.rsplit('.', 1)[0]}" if "." in tn else f"MeSH:{tn[0]}"
        cell = mesh_cell(tn)
        nodes.append({"id": f"MeSH:{tn}", "code": tn, "ui": ui, "name": nm, "level": tn.count(".") + 2,
                      "parent": parent, "taxonomy_cell": cell})
    meta = {"scheme": "MeSH 2026 (tree numbers)", "source": "https://nlmpubs.nlm.nih.gov/projects/mesh/MESH_FILES/xmlmesh/desc2026.gz",
            "retrieved": DATE, "licence": "NLM Terms and Conditions (free; acknowledge NLM)",
            "note": "One node per tree position, so a descriptor in two trees appears twice (same ui). "
                    "G02 Chemical Phenomena stays on CH.O.A3 except the rate and mechanism prefixes "
                    "kinetics, catalysis, hydrolysis, organic chemistry phenomena, oxidation-reduction, "
                    "photochemical processes, polymerization and pyrolysis (CH.O.A4)."}
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
    "D": "HI.O.A4", "E": "HI.O.A4", "F": "HI.O.A4",
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
# A node moves only when its own numeric span sits wholly inside the override.
LCC_SPAN = (("UB", 250, 277, "ST.O.A5"), ("UG", 570, 582, "ST.O.A5"), ("UG", 760, 765, "ST.O.A5"),
            ("CC", 72, 81, "HI.O.A3"))
LCC_BARE = {"E": "History: America", "F": "History of the Americas"}


def _lcc_span(code):
    m = re.match(r"^([A-Z]+)(\d+(?:\.\d+)?)(?:-(\d+(?:\.\d+)?))?$", code)
    if not m:
        return None
    return m.group(1), float(m.group(2)), float(m.group(3) or m.group(2))


def _lcc_place(nodes):
    """Span overrides, historiography by name, then pass those cells down to default descendants."""
    for n in nodes:
        got = _lcc_span(n["code"])
        if got:
            letters, lo, hi = got
            for sub, a, b, cell in LCC_SPAN:
                if letters == sub and lo >= a and hi <= b:
                    n["taxonomy_cell"] = cell
        if n["taxonomy_cell"].startswith("HI.") and re.search(r"historiograph|philosophy of history", n["name"], re.I):
            n["taxonomy_cell"] = "HI.O.A3"
    by = {n["id"]: n for n in nodes}
    special = {"HI.O.A3", "ST.O.A5"}
    for n in nodes:
        parent = by.get(n.get("parent") or "")
        if not parent or parent["taxonomy_cell"] not in special:
            continue
        letters = re.match(r"^([A-Z]+)", n["code"])
        default = LCC.get(letters.group(1)) if letters else None
        if n["taxonomy_cell"] == default:
            n["taxonomy_cell"] = parent["taxonomy_cell"]


def lcc():
    nodes = []
    for pdf in sorted(SRC.glob("lcco_*.pdf")):
        text = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True).stdout
        text = text.replace("\u2013", "-").replace("\u2014", "-")
        has_header = bool(re.search(r"(?m)^Subclass ", text))
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
            if not m or not m.group(2):
                continue
            letters = m.group(1)
            if not has_header:
                if letters not in LCC:
                    continue
                if letters != sub:
                    sub = letters
                    sid = f"LCC:{sub}"
                    if not any(n["id"] == sid for n in nodes):
                        nodes.append({"id": sid, "code": sub, "name": LCC_BARE.get(sub, sub), "level": 1,
                                      "parent": None, "taxonomy_cell": LCC[sub]})
                    stack = []
            if not sub or letters != sub:
                continue  # headings, scope notes and page furniture
            code = letters + m.group(2)
            name_col = len(letters + m.group(2) + m.group(3))
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
            n["name"] = names.get(n["code"], n["name"] or n["code"])
    _lcc_place(nodes)
    meta = {"scheme": "Library of Congress Classification outline",
            "source": "https://www.loc.gov/catdir/cpso/lcco/ (class PDFs A, B, C, D, G, H, J, K, L, M, N, P, Q, R, S, T, U, V, Z); E-F from https://www.loc.gov/aba/publications/FreeLCC/LCC_E-F2024OUT.pdf",
            "retrieved": DATE, "licence": "US government work (public domain)",
            "note": "E-F is the Free LCC outline (no subclass headers; retrieved 2026-10-11). "
                    "UB 250-277, UG 570-582 and UG 760-765 are ST.O.A5. CC 72-81 and headings that name historiography are HI.O.A3. "
                    "Those two cells pass to descendants still on the subclass default. Class W is not taken."}
    return split_write("lcc.json", meta, nodes)


# ---------- PhilPapers ----------
PP_CELL = {
    "metaphysics-and-epistemology": "PL.O.A1", "epistemology": "PL.O.A2", "metaphilosophy": "PL.O.A5",
    "metaphysics": "PL.O.A1", "philosophy-of-action": "PL.O.A1", "philosophy-of-language": "PL.O.A3",
    "philosophy-of-mind": "PL.O.A2", "philosophy-of-religion": "PL.O.A1", "me-misc": "PL.O.A1",
    "value-theory": "PL.O.A4", "science-logic-and-mathematics": "PL.O.A5", "logic-and-philosophy-of-logic": "PL.O.A3",
    "history-of-western-philosophy": "PL.O.A1", "philosophical-traditions": "PL.O.A1", "philosophy-misc": "PL.O.A1",
    "teaching-philosophy": "ED.O.A3", "other-academic-areas": "PL.O.A5",
}


class _Phil(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.divs, self.ids, self.nodes, self.seen = [], [], [], {}
        self.capture, self.buf, self.href = False, [], ""

    def handle_starttag(self, tag, attrs):
        ad = dict(attrs)
        if tag == "div":
            m = re.search(r"\bcat(\d+)\b", ad.get("class") or "")
            if m:
                self.divs.append("cat")
                self.ids.append(None)
            else:
                self.divs.append("x")
        elif tag == "a" and "tocCatName" in (ad.get("class") or ""):
            self.capture, self.buf, self.href = True, [], ad.get("href") or ""

    def handle_data(self, data):
        if self.capture:
            self.buf.append(data)

    def handle_endtag(self, tag):
        if tag == "a" and self.capture:
            self.capture = False
            slug = self.href.rstrip("/").rsplit("/", 1)[-1]
            if not slug or slug in self.seen or not self.ids:
                return
            name = "".join(self.buf).strip()
            if name.endswith("*"):
                name = name[:-1].strip()
            parent = next((i for i in reversed(self.ids[:-1]) if i), None)
            nid = "PP:" + slug
            self.seen[slug] = nid
            self.ids[-1] = nid
            own = slug in PP_CELL
            self.nodes.append({"id": nid, "code": slug, "name": name, "level": 1, "parent": parent,
                               "taxonomy_cell": PP_CELL.get(slug, "PL.O.A1"), "_own": own})
        elif tag == "div" and self.divs:
            if self.divs.pop() == "cat":
                self.ids.pop()


def philpapers():
    parser = _Phil()
    parser.feed((SRC / "philpapers_browse_20240924.html").read_text(encoding="utf-8", errors="replace"))
    by = {n["id"]: n for n in parser.nodes}

    def cell(n, seen=0):
        if n.get("_own") or not n.get("parent") or n["parent"] not in by or seen > 40:
            return n["taxonomy_cell"]
        return cell(by[n["parent"]], seen + 1)

    for n in parser.nodes:
        n["taxonomy_cell"] = cell(n)
        n.pop("_own", None)
    meta = {"scheme": "PhilPapers categories",
            "source": "https://web.archive.org/web/20240924181241/https://philpapers.org/browse/all",
            "retrieved": NEW, "licence": "PhilPapers category tree as published at philpapers.org/browse/all. "
            "Live curl to https://philpapers.org/browse/all and https://philpapers.org/categories.pl returned HTTP 403. "
            "Copied from the Internet Archive snapshot 20240924181241 (24 September 2024). "
            "The PhilPapers API asks for a free key and was not used.",
            "note": "First occurrence of each category is kept. Children take the cell of the nearest mapped ancestor. "
                    "History of philosophy stays on PL.O.A1. Teaching Philosophy is ED.O.A3. Aesthetics stays in philosophy (PL.O.A4)."}
    return split_write("philpapers.json", meta, parser.nodes)


# ---------- APA PsycInfo ----------
APA_MAJOR = {"21": "MS.O.A1", "22": "MS.O.A3", "23": "MS.O.A1", "24": "MS.O.A1", "25": "MS.O.A2",
             "26": "MS.O.A1", "27": "MS.O.A4", "28": "MS.O.A3", "29": "MS.O.A4", "30": "MS.O.A4",
             "31": "MS.O.A3", "32": "MS.O.A3", "33": "MS.O.A3", "34": "MS.O.A5", "36": "MS.O.A5",
             "37": "MS.O.A1", "38": "MS.O.A3", "39": "MS.O.A4", "40": "MS.O.A1", "41": "MS.O.A1",
             "42": "MS.O.A4"}
APA_CODE = {"2227": "ED.O.A4", "2720": "LN.O.A1", "2910": "MS.O.A5", "3500": "ED.O.A2", "3510": "ED.O.A5",
            "3530": "ED.O.A3", "3550": "ED.O.A2", "3560": "ED.O.A3", "3570": "ED.O.A2", "3575": "ED.O.A2",
            "3580": "ED.O.A2", "4120": "CS.O.A4", "4140": "CS.O.A4", "4160": "CS.O.A4"}


def psycinfo():
    text = subprocess.run(["pdftotext", "-layout", str(SRC / "apa_psycinfo_class.pdf"), "-"],
                          capture_output=True, text=True).stdout
    found = []
    pat = re.compile(r"(\d{4})\s+([A-Z][^\n]{0,110}?)(?=\s{2,}|\s+\d{4}\b|$)")
    for line in text.splitlines():
        for m in pat.finditer(line):
            name = re.sub(r"\s+", " ", m.group(2)).strip(" -")
            if len(name) >= 3:
                found.append((m.group(1), name))
    have = {c for c, _ in found}

    def parent(code):
        if code.endswith("00"):
            return None
        if code.endswith("0"):
            p = code[:2] + "00"
            return p if p in have else None
        p = code[:3] + "0"
        if p in have:
            return p
        p = code[:2] + "00"
        return p if p in have else None

    nodes = []
    for code, name in sorted(found):
        cell = APA_CODE.get(code, APA_MAJOR.get(code[:2], "MS.O.A1"))
        par = parent(code)
        nodes.append({"id": "APA:" + code, "code": code, "name": name, "level": 1,
                      "parent": ("APA:" + par) if par else None, "taxonomy_cell": cell})
    meta = {"scheme": "APA PsycInfo classification",
            "source": "https://www.apa.org/pubs/databases/training/class-codes",
            "retrieved": NEW,
            "licence": "APA PsycInfo Classification Code System, American Psychological Association, chart dated 12/2022. "
                       "No copyright or licence sentence is printed on the chart. Footer: For training and search help, email psycinfo@apa.org. 12/2022. "
                       "The HTML page returns HTTP 200 as a 212-byte Incapsula interstitial to curl; the printer-friendly PDF of the same chart was saved.",
            "note": "2227 Educational Measurement is ED.O.A4. 2720 Linguistics & Language & Speech is LN.O.A1. "
                    "The 3500 educational-psychology block is ED. 4120, 4140 and 4160 are CS.O.A4."}
    return split_write("psycinfo.json", meta, nodes)


# ---------- UNESCO politics ----------
def _word(name, words):
    n = name.lower()
    return any(re.search(r"\b" + re.escape(w) + r"\b", n) for w in words)


def unesco_politics():
    rdf = "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}"
    skos = "{http://www.w3.org/2004/02/skos/core#}"
    xml = "{http://www.w3.org/XML/1998/namespace}"
    root = ET.parse(SRC / "unesco-thesaurus.rdf").getroot()
    members, labels, broader = set(), {}, {}
    for desc in root.iter(rdf + "Description"):
        about = desc.get(rdf + "about") or ""
        if about.endswith("/mt6.15"):
            for mem in desc.findall(skos + "member"):
                members.add(mem.get(rdf + "resource"))
        if "/concept" in about:
            for lab in desc.findall(skos + "prefLabel"):
                if lab.get(xml + "lang") == "en" and lab.text:
                    labels[about] = lab.text.strip()
            b = desc.find(skos + "broader")
            if b is not None and b.get(rdf + "resource"):
                broader.setdefault(about, b.get(rdf + "resource"))
    members = {m for m in members if m and "/concept" in m}

    def cell_for(uri, seen=0):
        name = labels.get(uri, "")
        if _word(name, ("intelligence", "information", "propaganda", "censorship", "secrecy", "surveillance", "espionage")):
            return "ST.O.A5"
        if _word(name, ("peace", "disarmament", "armistice", "truce", "humanitarian", "neutrality")):
            return "ST.O.A4"
        if _word(name, ("defence", "defense", "military", "war", "weapon", "armed", "conflict", "army", "navy", "warfare")):
            return "ST.O.A3"
        if _word(name, ("party", "leader", "president", "minister")):
            return "ST.O.A1"
        parent = broader.get(uri)
        if parent in members and seen < 30:
            return cell_for(parent, seen + 1)
        return "ST.O.A2"

    nodes = []
    for uri in sorted(members):
        code = uri.rsplit("/", 1)[-1].replace("concept", "")
        parent = broader.get(uri)
        nodes.append({"id": "UNESCO:" + code, "code": code, "name": labels.get(uri, code), "level": 1,
                      "parent": ("UNESCO:" + parent.rsplit("/", 1)[-1].replace("concept", "")) if parent in members else None,
                      "taxonomy_cell": cell_for(uri)})
    meta = {"scheme": "UNESCO Thesaurus (Politics and government)",
            "source": "https://vocabularies.unesco.org/exports/thesaurus/latest/unesco-thesaurus.rdf",
            "retrieved": NEW, "licence": "http://creativecommons.org/licenses/by-sa/3.0/igo/ (dct:license). Rights holder UNESCO.",
            "note": "Microthesaurus mt6.15 Politics and government only. ANZSRC 440804 Defence studies and 440810 Peace studies were already placed (ST.O.A3 and ST.O.A4)."}
    return split_write("unesco_politics.json", meta, nodes)


# ---------- GEMET ----------
def _gemet_labels():
    groups = {
        "EV.O.A1": "accident|agriculture|animal husbandry|business|craft|crop residue|economy|energy|equipment|finances|firm|fishery|forestry|impact source|industrial process|industry|labour|military activities|military aspects|overburden|pollutant|pollution|product|recreation|resource utilisation|services|technology|tourism|trade (services)|trade activity|traffic|transportation|transportation mean|waste",
        "EV.O.A2": "atmosphere|biochemical process|biological diversity|biosphere|biota|blue infrastructure|border|built environment|chemical|chemical element|chemical process|chemical property|climate|culture (society)|demography|environment|environmental data|geological process|hydrosphere|land|land setup|lithosphere|material|nutrition|parameter|pedosphere|physical process|physical property|physicochemical process|radiation|society|space (interplanetary)|state of matter|statistics|subject|vibration",
        "EV.O.A3": "disaster|disease|effect|environmental impact|hazard|health|health-environment relationship",
        "EV.O.A4": "administration|analysis|education|environmental assessment|environmental awareness|environmental control|environmental management|environmental planning|environmental problem solving|environmental protection|evaluation|experiment|information|institutional structure|international relations|justice|law (corpus of rules)|law (individual)|legal form of organisations|legislation|management|medicine (practice)|methodology|monitoring|organisation of the legal system|planning|policy|politics|research|science|technical regulation",
        "EV.O.A5": "environmental economy issue|resource|risk|safety",
    }
    out = {}
    for cell, text in groups.items():
        for lab in text.split("|"):
            out[lab] = cell
    return out


def gemet():
    label_cell = _gemet_labels()
    tops, labels, broader = set(), {}, {}
    about = None
    with gzip.open(SRC / "gemet.rdf.gz", "rt", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if "hasTopConcept" in line:
                m = re.search(r'concept/(\d+)"', line)
                if m:
                    tops.add(m.group(1))
            m = re.search(r'<rdf:Description rdf:about="concept/(\d+)">', line)
            if m:
                about = m.group(1)
                continue
            if about and "</rdf:Description>" in line:
                about = None
                continue
            if not about:
                continue
            m = re.search(r'<skos:prefLabel xml:lang="en">([^<]*)</skos:prefLabel>', line)
            if m:
                labels[about] = unescape(m.group(1)).strip()
            m = re.search(r'<skos:broader rdf:resource="concept/(\d+)"/>', line)
            if m:
                broader.setdefault(about, m.group(1))
    missing = sorted(labels[t] for t in tops if labels.get(t) not in label_cell)
    if missing:
        raise SystemExit("unmapped GEMET tops: " + ", ".join(missing))

    def cell_of(cid, seen=0):
        if cid in tops:
            return label_cell[labels[cid]]
        parent = broader.get(cid)
        if parent and seen < 40:
            return cell_of(parent, seen + 1)
        return "EV.O.A2"

    nodes = []
    for cid, name in sorted(labels.items(), key=lambda kv: int(kv[0])):
        parent = None if cid in tops else broader.get(cid)
        if parent not in labels:
            parent = None
        nodes.append({"id": "GEMET:" + cid, "code": cid, "name": name, "level": 1,
                      "parent": ("GEMET:" + parent) if parent else None, "taxonomy_cell": cell_of(cid)})
    meta = {"scheme": "GEMET", "source": "https://www.eionet.europa.eu/gemet/latest/gemet.rdf.gz",
            "retrieved": NEW, "licence": "http://creativecommons.org/licenses/by/4.0/ (dcterms:licence). GEMET - Concepts, version 4.2.3, 2021-12-06.",
            "note": "Whole environmental thesaurus kept in EV. Top concepts placed on the DPSIR cells; descendants inherit. Impact, hazard, health and effect are EV.O.A3. Resource, risk and safety are EV.O.A5."}
    return split_write("gemet.json", meta, nodes)


# ---------- Getty AAT (top levels already extracted) ----------
AAT_CELL = {"physical": "AR.O.A2", "value": "AR.O.A5", "styles": "DE.O.A2", "activities": "DE.O.A1", "furnishings": "DE.O.A2"}


def aat():
    data = json.loads((SRC / "aat_top.json").read_text(encoding="utf-8"))
    nums = {n["id"].rstrip("/").rsplit("/", 1)[-1] for n in data["nodes"]}
    nodes = []
    for n in data["nodes"]:
        num = n["id"].rstrip("/").rsplit("/", 1)[-1]
        parent = None
        if n.get("parent"):
            pnum = n["parent"].rstrip("/").rsplit("/", 1)[-1]
            if pnum in nums:
                parent = "AAT:" + pnum
        nodes.append({"id": "AAT:" + num, "code": num, "name": n["name"], "level": 1, "parent": parent,
                      "taxonomy_cell": AAT_CELL[n["branch"]]})
    meta = {"scheme": "Getty AAT (top levels)", "source": "https://vocab.getty.edu/sparql",
            "retrieved": NEW, "licence": "No licence or rights triple on the AAT concept scheme returned by the SPARQL endpoint (UNVERIFIED).",
            "note": data.get("note", "Top levels only.") + " Physical Attributes is AR.O.A2. The critical-concepts branch is AR.O.A5. Styles, activities and furnishings are DE."}
    return split_write("aat.json", meta, nodes)


# ---------- ISKO ----------
ISKO_CELL = {"Knowledge organization: general and historical issues": "IS.O.A3", "Core concepts in KO": "IS.O.A1",
             "Knowledge organizing systems (KOS)": "IS.O.A3", "Knowledge organizing processes (KOP)": "IS.O.A2",
             "Methods, approaches & philosophies": "IS.O.A3", "KO in different contexts and applications": "IS.O.A5"}


class _Isko(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.on = self.done = self.in_h4 = self.in_a = False
        self.h4, self.abuf, self.nodes = [], [], []
        self.href, self.section, self.cell = "", None, "IS.O.A3"

    def handle_starttag(self, tag, attrs):
        ad = dict(attrs)
        if tag == "a" and ad.get("name") == "sys":
            self.on = True
        elif tag == "a" and ad.get("name") == "az":
            self.done = True
        if not self.on or self.done:
            return
        if tag == "h4":
            self.in_h4, self.h4 = True, []
        elif tag == "a" and "menu" in (ad.get("class") or ""):
            self.in_a, self.abuf, self.href = True, [], ad.get("href") or ""

    def handle_data(self, data):
        if self.in_h4:
            self.h4.append(data)
        if self.in_a:
            self.abuf.append(data)

    def handle_endtag(self, tag):
        if tag == "h4" and self.in_h4:
            self.in_h4 = False
            title = "".join(self.h4).strip()
            sid = "ISKO:" + re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
            self.section, self.cell = sid, ISKO_CELL.get(title, "IS.O.A3")
            self.nodes.append({"id": sid, "code": sid[5:], "name": title, "level": 1, "parent": None, "taxonomy_cell": self.cell})
        elif tag == "a" and self.in_a:
            self.in_a = False
            name = "".join(self.abuf).strip().rstrip(";").strip()
            code = self.href.replace(".htm", "")
            if not code or not self.section or not name:
                return
            self.nodes.append({"id": "ISKO:" + code, "code": code, "name": name, "level": 2, "parent": self.section,
                               "taxonomy_cell": self.cell})


def isko():
    parser = _Isko()
    parser.feed((SRC / "isko_cyclo.html").read_text(encoding="utf-8", errors="replace"))
    seen, nodes = set(), []
    for n in parser.nodes:
        if n["id"] in seen:
            continue
        seen.add(n["id"])
        nodes.append(n)
    meta = {"scheme": "ISKO Encyclopedia of Knowledge Organization", "source": "https://www.isko.org/cyclo/",
            "retrieved": NEW, "licence": "No licence statement on the page.",
            "note": "Systematic index only (the list between the sys and az anchors). Articles without a link are omitted."}
    return split_write("isko.json", meta, nodes)


# ---------- Glottolog families ----------
def glottolog():
    fams = {}
    with (SRC / "glottolog_languages.csv").open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("Level") == "family":
                fams[row["ID"]] = row["Name"]
    parents = {}
    with (SRC / "glottolog_classification.tsv").open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            path = (row.get("classification") or "").strip()
            if path:
                parents[row["Language_ID"]] = path.split("/")[-1]
    nodes = []
    for gid, name in sorted(fams.items()):
        parent = parents.get(gid)
        if parent not in fams:
            parent = None
        nodes.append({"id": "Glottolog:" + gid, "code": gid, "name": name, "level": 1,
                      "parent": ("Glottolog:" + parent) if parent else None, "taxonomy_cell": "LN.O.A5"})
    meta = {"scheme": "Glottolog families",
            "source": "https://github.com/glottolog/glottolog-cldf (cldf/languages.csv; classification from values.csv Parameter_ID=classification)",
            "retrieved": NEW, "licence": "This dataset is licensed under a CC-BY-4.0 license (Glottolog CLDF README).",
            "note": "Family-level languoids only. Parent is the last glottocode on the classification path. All nodes are LN.O.A5."}
    return split_write("glottolog.json", meta, nodes)


# ---------- ERIC ----------
ERIC_GROUP = {
    "110": "ED.O.A2", "120": "ED.O.A2", "210": "ED.O.A2", "220": "ED.O.A2", "230": "ED.O.A2", "240": "ED.O.A2",
    "310": "ED.O.A3", "320": "ED.O.A5", "330": "ED.O.A5", "340": "ED.O.A5", "350": "ED.O.A1", "360": "ED.O.A2",
    "400": "ED.O.A1", "410": "ED.O.A1", "420": "ED.O.A1", "430": "ED.O.A1", "440": "ED.O.A1", "450": "ED.O.A1",
    "460": "ED.O.A1", "470": "ED.O.A1", "480": "ED.O.A1", "490": "ED.O.A1", "510": "ED.O.A2", "520": "ED.O.A5",
    "530": "ED.O.A5", "540": "ED.O.A5", "550": "ED.O.A5", "560": "ED.O.A5", "610": "ED.O.A5", "620": "ED.O.A5",
    "630": "ED.O.A5", "640": "ED.O.A5", "650": "ED.O.A5", "710": "ED.O.A5", "720": "ED.O.A5", "730": "ED.O.A5",
    "810": "ED.O.A1", "820": "ED.O.A4", "830": "ED.O.A4", "910": "ED.O.A5", "920": "ED.O.A5",
}


def eric():
    xml = zipfile.ZipFile(SRC / "eric_thesaurus.zip").read("ERICthesaurus.xml")
    root = ET.fromstring(xml)
    mains = {}
    for term in root.findall("Terms/Term"):
        attrs = {a.get("name"): (a.text or "") for a in term.findall("Attributes/Attribute")}
        if attrs.get("RecType") != "Main":
            continue
        name = (term.findtext("Name") or "").strip()
        bts = []
        for rel in term.findall("Relationships/Relationship"):
            if rel.get("type") == "BT":
                bts = [(x.text or "").strip() for x in rel.findall("Is") if (x.text or "").strip()]
                break
        mains[name] = (attrs.get("GroupCode", "")[:3], bts[0] if bts else None)
    nodes = []
    for name, (group, bt) in sorted(mains.items()):
        parent = ("ERIC:" + bt) if bt in mains else None
        nodes.append({"id": "ERIC:" + name, "code": name, "name": name, "level": 1, "parent": parent,
                      "taxonomy_cell": ERIC_GROUP.get(group, "ED.O.A1")})
    meta = {"scheme": "ERIC Thesaurus", "source": "https://files.eric.ed.gov/xml/eric_thesaurus.zip",
            "retrieved": NEW, "licence": "US Department of Education, Institute of Education Sciences, ERIC Thesaurus XML (public download).",
            "note": "Main terms only. First broader term is the parent. Groups 820 Measurement and 830 Tests and Scales are ED.O.A4. The thesaurus stays in ED."}
    return split_write("eric.json", meta, nodes)


# ---------- AGROVOC top concepts ----------
AG_TOP = {"organisms": "AG.O.A1", "activities": "AG.O.A2", "methods": "AG.O.A2", "processes": "AG.O.A2",
          "technology": "AG.O.A2", "objects": "AG.O.A2", "phenomena": "AG.O.A3", "substances": "AG.O.A3",
          "products": "AG.O.A4"}


def agrovoc():
    labels, broader, tops = {}, {}, set()
    trip = re.compile(r'<([^>]+)>\s+<([^>]+)>\s+(?:<([^>]+)>|"((?:[^"\\]|\\.)*)"@en)\s+\.')
    for m in trip.finditer((SRC / "agrovoc_top.nt").read_text(encoding="utf-8")):
        s, p, o, lit = m.group(1), m.group(2), m.group(3), m.group(4)
        if p.endswith("prefLabel") and lit is not None:
            labels[s] = lit.replace('\\"', '"')
        elif p.endswith("broader") and o:
            broader.setdefault(s, o)
        elif p.endswith("hasTopConcept") and o:
            tops.add(o)
    top_name = {uri: labels[uri] for uri in tops if uri in labels}

    def cell_of(uri, seen=0):
        if uri in top_name:
            return AG_TOP.get(top_name[uri], "AG.O.A5")
        parent = broader.get(uri)
        if parent and seen < 10:
            return cell_of(parent, seen + 1)
        return "AG.O.A5"

    nodes = []
    for uri, name in sorted(labels.items(), key=lambda kv: kv[1].lower()):
        code = uri.rstrip("/").rsplit("/", 1)[-1]
        parent = broader.get(uri)
        if parent not in labels or uri in tops:
            parent = None
        nodes.append({"id": "AGROVOC:" + code, "code": code, "name": name, "level": 1,
                      "parent": ("AGROVOC:" + parent.rstrip("/").rsplit("/", 1)[-1]) if parent else None,
                      "taxonomy_cell": cell_of(uri)})
    meta = {"scheme": "AGROVOC top concepts",
            "source": "https://agrovoc.fao.org/latestAgrovoc/agrovoc_core.nt.zip",
            "retrieved": NEW,
            "licence": "No licence triple in the extracted top-concept slice of agrovoc_core.nt.zip (UNVERIFIED). The core zip is 74107876 bytes.",
            "note": "English labels of the 25 top concepts and their direct narrower concepts. Organisms is AG.O.A1; activities, methods, processes, technology and objects are AG.O.A2; phenomena and substances are AG.O.A3; products is AG.O.A4; the other tops are AG.O.A5."}
    return split_write("agrovoc.json", meta, nodes)


# ---------- ChEBI roles ----------
def chebi_roles():
    terms, cur = [], None
    for line in (SRC / "chebi_roles.obo").read_text(encoding="utf-8").splitlines():
        if line == "[Term]":
            if cur:
                terms.append(cur)
            cur = {"is_a": []}
            continue
        if cur is None:
            continue
        if line.startswith("["):
            terms.append(cur)
            cur = None
            continue
        if line.startswith("id:"):
            cur["id"] = line.split(":", 1)[1].strip()
        elif line.startswith("name:"):
            cur["name"] = line.split(":", 1)[1].strip()
        elif line.startswith("is_a:"):
            cur["is_a"].append(line.split()[1])
        elif line.startswith("is_obsolete:") and "true" in line:
            cur["obs"] = True
    if cur:
        terms.append(cur)
    keep = {t["id"]: t for t in terms if t.get("id") and not t.get("obs")}
    parent = {}
    for tid, t in keep.items():
        for isa in t["is_a"]:
            if isa in keep:
                parent[tid] = isa
                break

    def cell_of(tid, seen=0):
        if tid == "CHEBI:33232":
            return "CH.O.A5"
        p = parent.get(tid)
        if p and seen < 40:
            return cell_of(p, seen + 1)
        return "CH.O.A4"

    nodes = []
    for tid, t in sorted(keep.items()):
        nodes.append({"id": "ChEBI:" + tid, "code": tid, "name": t.get("name", tid), "level": 1,
                      "parent": ("ChEBI:" + parent[tid]) if tid in parent else None, "taxonomy_cell": cell_of(tid)})
    meta = {"scheme": "ChEBI role ontology",
            "source": "https://ftp.ebi.ac.uk/pub/databases/chebi/ontology/chebi.obo.gz",
            "retrieved": NEW, "licence": "https://creativecommons.org/licenses/by/4.0/ (property_value terms:license in the ChEBI OBO header).",
            "note": "Role branch CHEBI:50906 and its is_a descendants only (data-version 256). "
                    "Biological role and chemical role are CH.O.A4. Application is CH.O.A5. Molecules are not included."}
    return split_write("chebi_roles.json", meta, nodes)


# ---------- IEEE Taxonomy ----------
def ieee_cell(name):
    n = name.lower()
    if "computational and artificial" in n:
        return "CS.O.A4"
    if "computers and information processing" in n:
        return "CS.O.A3"
    if n.startswith("information theory"):
        return "CS.O.A2"
    if n == "education" or n.startswith("education "):
        return "ED.O.A1"
    if "geoscience" in n or "remote sensing" in n:
        return "EA.O.A4"
    if "professional communication" in n:
        return "EN.O.A1"
    if "power electronics" in n:
        return "EN.O.A4"
    if "power engineering" in n or "nuclear and plasma" in n:
        return "EN.O.A3"
    if any(k in n for k in ("aerospace", "oceanic", "marine technology", "vehicular", "robotics", "transportation")):
        return "EN.O.A2"
    if any(k in n for k in ("material", "nanotechnology", "compound", "packaging", "manufacturing", "dielectric")):
        return "EN.O.A5"
    if any(k in n for k in ("circuit", "antenna", "signal processing", "electromagnetic", "communication", "broadcast",
                           "microwave", "laser", "magnetics", "sensor", "imaging", "ultrasonic", "electron device",
                           "solid state", "consumer electronic", "industrial electronic", "instrumentation",
                           "superconduct", "resonance")):
        return "EN.O.A4"
    return "EN.O.A1"


def _ieee_terms(text):
    raw, started = [], False
    for line in text.splitlines():
        s = line.strip()
        if s == "Aerospace and electronic systems":
            started = True
        if not started or not s:
            continue
        if s.startswith(("This work is licensed", "International License", "Engineers (IEEE)", "Page ", "January ")):
            continue
        raw.append(line if line.startswith(".") else s)

    def ndots(s):
        return len(s) - len(s.lstrip("."))

    out, i = [], 0
    while i < len(raw):
        s = raw[i]
        i += 1
        while i < len(raw) and not raw[i].startswith("."):
            frag = raw[i]
            if frag[:1].islower():
                s = s.rstrip() + " " + frag
                i += 1
                continue
            nxt = raw[i + 1] if i + 1 < len(raw) else ""
            # "Change" continues "…Climate" when the next term is still deeply indented.
            # A real family is followed by a four-dot child, so it is not joined.
            if ndots(s) > 0 and nxt.startswith(".") and ndots(nxt) > 4:
                s = s.rstrip() + " " + frag
                i += 1
                continue
            break
        out.append(s.strip())
    return out


def ieee():
    text = subprocess.run(["pdftotext", str(SRC / "ieee_taxonomy_jan2026.pdf"), "-"], capture_output=True, text=True).stdout
    stack, nodes, seen = [], [], {}
    family = "EN.O.A1"
    for s in _ieee_terms(text):
        m = re.match(r"^(\.*)(.*\S)\s*$", s)
        if not m or not m.group(2).strip():
            continue
        dots, name = m.group(1), re.sub(r"\s+", " ", m.group(2)).strip()
        level = len(dots) // 4 + 1
        while stack and stack[-1][0] >= level:
            stack.pop()
        if level == 1:
            family = ieee_cell(name)
        parent = stack[-1][1] if stack else None
        path = (stack[-1][2] + "|" if stack else "") + name
        base = "IEEE:" + path
        seen[base] = seen.get(base, 0) + 1
        nid = base if seen[base] == 1 else base + "#" + str(seen[base])
        nodes.append({"id": nid, "code": name, "name": name, "level": level, "parent": parent, "taxonomy_cell": family})
        stack.append((level, nid, path))
    meta = {"scheme": "IEEE Taxonomy",
            "source": "https://ieee-org.widen.net/content/umbnbirtxs/original/ieee-taxonomy.pdf (January 2026, version 1.05; viewer https://ieee-org.widen.net/s/jwk9pcxxvd/ieee-taxonomy)",
            "retrieved": NEW,
            "licence": "This work is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License (CC BY-NC-ND 4.0). Created by The Institute of Electrical and Electronics Engineers (IEEE) for the benefit of humanity.",
            "note": "Direct ieee.org links returned HTTP 202 (CloudFront). The January 2026 widen share link returned HTTP 404. "
                    "The PDF was taken from the July 2025 viewer content URL, which serves the January 2026 file. "
                    "A repeated term keeps a path id. Families are placed by name; descendants inherit. Mathematics stays in EN, not MA."}
    return split_write("ieee.json", meta, nodes)


def main():
    index = json.loads((ROOT / "maps" / "index.json").read_text())
    batch = (
        ("mesh2026.json", mesh, "MeSH 2026"),
        ("acm_ccs2012.json", acm, "ACM CCS 2012"),
        ("lcc.json", lcc, "LCC outline"),
        ("philpapers.json", philpapers, "PhilPapers categories"),
        ("psycinfo.json", psycinfo, "APA PsycInfo classification"),
        ("unesco_politics.json", unesco_politics, "UNESCO Thesaurus (Politics and government)"),
        ("gemet.json", gemet, "GEMET"),
        ("aat.json", aat, "Getty AAT (top levels)"),
        ("isko.json", isko, "ISKO Encyclopedia of Knowledge Organization"),
        ("glottolog.json", glottolog, "Glottolog families"),
        ("eric.json", eric, "ERIC Thesaurus"),
        ("agrovoc.json", agrovoc, "AGROVOC top concepts"),
        ("chebi_roles.json", chebi_roles, "ChEBI role ontology"),
        ("ieee.json", ieee, "IEEE Taxonomy"),
    )
    for name, fn, scheme in batch:
        print("building", scheme, flush=True)
        for f, n in fn().items():
            index[f]["maps"][scheme] = n
            print(f"  {f} {n}", flush=True)
    for f, p in (("MD", "mesh2026.json"), ("CS", "acm_ccs2012.json"), ("RE", "lcc.json"), ("LA", "lcc.json"),
                 ("ST", "lcc.json"), ("PO", "lcc.json"), ("HI", "lcc.json"), ("LN", "lcc.json"), ("AR", "lcc.json"),
                 ("ED", "lcc.json")):
        index[f]["primary"] = p
    for f, p in (("EV", "gemet.json"), ("ED", "eric.json"), ("PL", "philpapers.json"), ("EN", "ieee.json"),
                 ("AG", "agrovoc.json")):
        index[f]["primary"] = p
    (ROOT / "maps" / "index.json").write_text(json.dumps(index, indent=1, ensure_ascii=False), encoding="utf-8")
    for f, v in index.items():
        print(f, v["primary"], v["maps"])


if __name__ == "__main__":
    main()
