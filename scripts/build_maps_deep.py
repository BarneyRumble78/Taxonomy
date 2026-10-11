"""Deeper and balancing maps. Called from build_maps_more.main.

Sources are free public files already saved under sources/. Blocked URLs are
recorded in docs/INTEGRATION_PLAN.md, not raised here.
"""
import csv
import gzip
import html
import json
import re
import subprocess
from pathlib import Path

import build_maps_more as more

ROOT = more.ROOT
SRC = more.SRC
NEW = more.NEW
split_write = more.split_write


def _word(name, words):
    n = name.lower()
    return any(w in n for w in words)


# ---------- PACS 2010 ----------
def _pacs_cell(code):
    """The tens digit is the PACS section. 87 is section 80, not a section of its own."""
    n = int(code[:2])
    if n == 4 or 90 <= n <= 99:
        return "PH.O.A3"
    if 10 <= n <= 39:
        return "PH.O.A2"
    if n == 5:
        return "PH.O.A4"
    if 50 <= n <= 59:
        return "PH.O.A5"
    if 60 <= n <= 89:
        return "PH.O.A4"
    return "PH.O.A1"
_PACS_CODE = re.compile(r"^\d{2}(?:\.\d{2}(?:\.[-A-Za-z0-9]+)?)?$")


def pacs():
    found = {}
    for path in sorted((SRC / "pacs2010").glob("pacs-reg*.html")):
        raw = path.read_text(encoding="utf-8", errors="replace")
        cells = re.findall(r"<td[^>]*>(.*?)</td>", raw, re.S | re.I)
        texts = [html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", c))).strip() for c in cells]
        i = 0
        while i + 1 < len(texts):
            code = texts[i].rstrip(".")
            name = texts[i + 1].strip(" .")
            if _PACS_CODE.match(code) and name and not name[:1].isdigit():
                found.setdefault(code, name)
                i += 2
            else:
                i += 1
    have = set(found)

    def parent(code):
        if len(code) == 2:
            return None
        if re.fullmatch(r"\d{2}\.\d{2}", code):
            return code[:2] if code[:2] in have else None
        two = code[:5]
        if two in have:
            return two
        return code[:2] if code[:2] in have else None

    nodes = []
    for code in sorted(found):
        nodes.append({"id": "PACS:" + code, "code": code, "name": found[code], "level": 1,
                      "parent": ("PACS:" + parent(code)) if parent(code) else None,
                      "taxonomy_cell": _pacs_cell(code)})
    meta = {"scheme": "PACS 2010",
            "source": "https://web.archive.org/web/20160213071835/http://www.aip.org/publishing/pacs/pacs-2010-regular-edition",
            "retrieved": NEW,
            "licence": "PACS is a scheme of the American Institute of Physics. The regular edition was copied from the Internet Archive snapshot 20160213071835. The live AIP site no longer serves the edition (UNVERIFIED as to the current licence).",
            "note": "Placement follows the section, not only the two codes 10 or 20. "
                    "00-03, 06-09 and 40-49 are PH.O.A1. 04 and 90-99 are PH.O.A3. 10-39 are PH.O.A2. "
                    "05 and 60-89 are PH.O.A4. 50-59 are PH.O.A5."}
    return split_write("pacs2010.json", meta, nodes)


# ---------- IUPAC Gold Book index ----------
def _chem_cell(name):
    n = name.lower()
    if any(k in n for k in ("kinetic", "cataly", "mechanism", "rate constant", "reaction rate", "half-life", "activation energy")):
        return "CH.O.A4"
    if any(k in n for k in ("equilibrium", "thermodynamic", "enthalpy", "entropy", "gibbs", "heat capacity", "chemical potential", "free energy")):
        return "CH.O.A3"
    if any(k in n for k in ("bond", "isomer", "conformation", "stereochem", "hybridis", "hybridiz", "crystal", "orbital", "ligand", "chirality", "aromatic")):
        return "CH.O.A2"
    if any(k in n for k in ("synthes", "chromatograph", "spectr", "assay", "titr", "analytical", "nmr", "infrared", "ultraviolet")):
        return "CH.O.A5"
    return "CH.O.A1"


def goldbook():
    data = json.loads((SRC / "iupac_goldbook_terms.json").read_text(encoding="utf-8"))
    terms = data["terms"]["list"]
    nodes = []
    for code in sorted(terms):
        title = (terms[code].get("title") or "").strip()
        if not title or terms[code].get("status") == "retired":
            continue
        nodes.append({"id": "GOLD:" + code, "code": code, "name": title, "level": 1, "parent": None,
                      "taxonomy_cell": _chem_cell(title)})
    meta = {"scheme": "IUPAC Gold Book",
            "source": "https://web.archive.org/web/20240315000000/https://goldbook.iupac.org/terms/index/all/json",
            "retrieved": NEW,
            "licence": "The IUPAC Gold Book is licensed under Creative Commons Attribution-ShareAlike CC BY-SA 4.0 International for individual terms (stated in the JSON).",
            "note": "The live site returned HTTP 403. This is the term index, which has titles and no broader links, so every term is level 1. "
                    "Titles that name rates, equilibrium, structure or analysis are placed on those cells. The rest stay on CH.O.A1."}
    return split_write("iupac_goldbook.json", meta, nodes)


def chebi_entities():
    path = SRC / "chebi_entities.json"
    if not path.exists():
        gz = Path("/tmp/taxdl/chebi.obo.gz")
        if not gz.exists():
            print("  ChEBI chemical-entity extract missing", flush=True)
            return {}
        _write_chebi_entities(gz, path)
    rows = json.loads(path.read_text(encoding="utf-8"))
    by = {r["id"]: r for r in rows}
    nodes = []
    for row in rows:
        parent = row.get("parent") if row.get("parent") in by else None
        nodes.append({"id": "ChEBI:" + row["id"], "code": row["id"], "name": row["name"], "level": 1,
                      "parent": ("ChEBI:" + parent) if parent else None,
                      "taxonomy_cell": _chem_cell(row["name"])})
    meta = {"scheme": "ChEBI chemical entity (top branches)",
            "source": "https://ftp.ebi.ac.uk/pub/databases/chebi/ontology/chebi.obo.gz",
            "retrieved": NEW,
            "licence": "ChEBI is licensed under CC BY 4.0 (ftp.ebi.ac.uk/pub/databases/chebi/license.txt).",
            "note": "CHEBI:24431 chemical entity and its is_a descendants to depth 2. Not the molecule leaves. "
                    "Role terms stay in chebi_roles.json. The same title rules as the Gold Book place structure, equilibrium, rates and analysis."}
    return split_write("chebi_entities.json", meta, nodes)


def _write_chebi_entities(gz, dest):
    parents = {}
    names = {}
    obsolete = set()
    cur = None
    with gzip.open(gz, "rt", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            line = line.rstrip("\n")
            if line == "[Term]":
                cur = {}
            elif cur is None:
                continue
            elif line.startswith("id: "):
                cur["id"] = line[4:]
            elif line.startswith("name: "):
                cur["name"] = line[6:]
            elif line.startswith("is_a: "):
                cur.setdefault("is_a", []).append(line[6:].split()[0])
            elif line.startswith("is_obsolete: true"):
                cur["obs"] = True
            elif line == "" and cur.get("id"):
                if cur.get("obs"):
                    obsolete.add(cur["id"])
                else:
                    names[cur["id"]] = cur.get("name", cur["id"])
                    if cur.get("is_a"):
                        parents[cur["id"]] = cur["is_a"][0]
                cur = None
    children = {}
    for child, parent in parents.items():
        children.setdefault(parent, []).append(child)
    root = "CHEBI:24431"
    keep = {root}
    frontier = [root]
    for _ in range(2):
        nxt = []
        for node in frontier:
            for child in children.get(node, []):
                if child not in keep and child not in obsolete:
                    keep.add(child)
                    nxt.append(child)
        frontier = nxt
    rows = []
    for cid in sorted(keep):
        parent = parents.get(cid)
        rows.append({"id": cid, "name": names.get(cid, cid),
                     "parent": parent if parent in keep else None})
    dest.write_text(json.dumps(rows, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


# ---------- NAICS 2022 and ISIC Rev. 4 ----------
def _naics_cell(code):
    if code.startswith("5418"):
        return "BU.O.A4"
    sector = code[:2]
    if sector in {"52", "53"}:
        return "BU.O.A2"
    if sector in {"42", "44", "45"}:
        return "BU.O.A5"
    if sector == "72":
        return "BU.O.A4"
    return "BU.O.A3"


def naics():
    import openpyxl
    ws = openpyxl.load_workbook(SRC / "naics2022.xlsx", read_only=True).active
    rows = []
    for rec in ws.iter_rows(values_only=True):
        code, name = rec[1], rec[2]
        if code is None or name is None or not str(name).strip():
            continue
        text = str(code).strip()
        if not re.fullmatch(r"\d{2,6}", text):
            continue
        rows.append((text, str(name).strip()))
    have = {c for c, _ in rows}

    def parent(code):
        for n in range(len(code) - 1, 1, -1):
            if code[:n] in have:
                return code[:n]
        return None

    nodes = [{"id": "NAICS:" + c, "code": c, "name": n, "level": 1,
              "parent": ("NAICS:" + parent(c)) if parent(c) else None,
              "taxonomy_cell": _naics_cell(c)} for c, n in rows]
    meta = {"scheme": "NAICS 2022",
            "source": "https://www.census.gov/naics/2022NAICS/2-6%20digit_2022_Codes.xlsx",
            "retrieved": NEW,
            "licence": "US Census Bureau NAICS 2022 structure (public download).",
            "note": "Finance and real estate are BU.O.A2. Wholesale and retail are BU.O.A5. Advertising (5418) and accommodation (72) are BU.O.A4. The other industries are BU.O.A3."}
    return split_write("naics2022.json", meta, nodes)


_ISIC_BANDS = (
    (1, 3, "A"), (5, 9, "B"), (10, 33, "C"), (35, 35, "D"), (36, 39, "E"), (41, 43, "F"),
    (45, 47, "G"), (49, 53, "H"), (55, 56, "I"), (58, 63, "J"), (64, 66, "K"), (68, 68, "L"),
    (69, 75, "M"), (77, 82, "N"), (84, 84, "O"), (85, 85, "P"), (86, 88, "Q"), (90, 93, "R"),
    (94, 96, "S"), (97, 98, "T"), (99, 99, "U"),
)


def _isic_section(code):
    if code.isalpha():
        return code
    n = int(code[:2])
    for lo, hi, sec in _ISIC_BANDS:
        if lo <= n <= hi:
            return sec
    return "C"


def isic():
    rows = []
    with (SRC / "isic_rev4.csv").open(encoding="utf-8", newline="") as handle:
        for rec in csv.DictReader(handle):
            code = (rec.get("Code") or "").strip()
            name = (rec.get("Description") or "").strip()
            if code and name:
                rows.append((code, name))
    have = {c for c, _ in rows}

    def parent(code):
        if code.isalpha():
            return None
        for n in range(len(code) - 1, 1, -1):
            if code[:n] in have:
                return code[:n]
        sec = _isic_section(code)
        return sec if sec in have else None

    def cell(code):
        sec = _isic_section(code)
        return {"G": "BU.O.A5", "K": "BU.O.A2", "I": "BU.O.A4"}.get(sec, "BU.O.A3")

    nodes = [{"id": "ISIC:" + c, "code": c, "name": n, "level": 1,
              "parent": ("ISIC:" + parent(c)) if parent(c) else None,
              "taxonomy_cell": cell(c)} for c, n in rows]
    meta = {"scheme": "ISIC Rev. 4",
            "source": "https://unstats.un.org/unsd/classifications/Econ/Download/In%20Text/ISIC_Rev_4_english_structure.txt",
            "retrieved": NEW,
            "licence": "United Nations Statistics Division, ISIC Rev. 4 English structure (public download, file dated 2008-08-13).",
            "note": "Section G (trade) is BU.O.A5. Section K (finance) is BU.O.A2. Section I (accommodation and food) is BU.O.A4. The other sections are BU.O.A3."}
    return split_write("isic_rev4.json", meta, nodes)


# ---------- LCC full schedules ----------
_HEADER = re.compile(r"^([A-Z]{1,3})\s{2,}(.+?)\s+\1\s*$")
_NUM = re.compile(r"^(\s*)(\d[\d.]*(?:\.[A-Z][\dA-Z]*)?(?:-[\dA-Z.]+)?)(\s{2,})(\S.*?)\s*$")
_CAP = re.compile(r"^(\s{8,})([A-Za-z(][^\d].{2,})\s*$")
_SKIP = re.compile(r"^(see |cf\.|for |class here|under each|including )", re.I)


def lcc_full():
    nodes = []
    seen = set()
    files = (
        ("lcc_text_c.pdf", "C"), ("lcc_text_d.pdf", "D"), ("lcc_text_ds.pdf", "D"),
        ("lcc_text_ef.pdf", "E"), ("lcc_text_uv.pdf", "U"), ("lcc_text_k.pdf", "K"),
        ("lcc_text_z.pdf", "Z"),
    )
    for name, _fallback in files:
        text = subprocess.run(["pdftotext", "-layout", str(SRC / name), "-"], capture_output=True, text=True).stdout
        text = text.replace("\u2013", "-").replace("\u2014", "-")
        sub = None
        stack = []
        for raw in text.splitlines():
            line = raw.rstrip()
            head = _HEADER.match(line.strip())
            if head and len(line.strip()) < 120 and head.group(1) in more.LCC:
                letters = head.group(1)
                if letters != sub:
                    sub = letters
                    sid = "LCCf:" + sub
                    if sid not in seen:
                        seen.add(sid)
                        nodes.append({"id": sid, "code": sub, "name": head.group(2).strip(" ."),
                                      "level": 1, "parent": None, "taxonomy_cell": more.LCC[sub]})
                    stack = [(0, sid)]
                continue
            if sub is None:
                continue
            num = _NUM.match(line)
            cap = None if num else _CAP.match(line)
            if not num and not cap:
                continue
            if cap and (_SKIP.match(cap.group(2).strip()) or len(cap.group(2).strip()) > 140):
                continue
            indent = len((num or cap).group(1))
            if num:
                code = sub + num.group(2)
                label = num.group(4).strip(" .")
            else:
                label = cap.group(2).strip(" .")
                code = sub + ":" + re.sub(r"[^A-Za-z0-9]+", "-", label.lower())[:40].strip("-")
            if len(label) <= 2 or re.fullmatch(r"e\.?g\.?", label, re.I):
                continue
            while stack and stack[-1][0] >= indent:
                stack.pop()
            parent = stack[-1][1] if stack else ("LCCf:" + sub)
            base = "LCCf:" + code
            nid = base
            n = 2
            while nid in seen:
                nid = base + "#" + str(n)
                n += 1
            seen.add(nid)
            nodes.append({"id": nid, "code": code if num else sub, "name": label, "level": 2,
                          "parent": parent, "taxonomy_cell": more.LCC[sub]})
            stack.append((indent, nid))
    more._lcc_place(nodes)
    meta = {"scheme": "LCC full schedules (C, D, E-F, K, U-V, Z)",
            "source": "https://www.loc.gov/aba/publications/FreeLCC/freelcc.html (2024 TEXT PDFs)",
            "retrieved": NEW,
            "licence": "Library of Congress Classification schedules, published as Free LCC PDFs.",
            "note": "Numbered captions from the full text schedules, plus unnumbered headings. "
                    "The outline maps stay in lcc.json. Span overrides for intelligence and historiography are the same as the outline. "
                    "K subclass outlines (KB, KD, KE, KF, KZ) are in lcc.json."}
    return split_write("lcc_full.json", meta, nodes)


# ---------- DTIC military subject categories ----------
_DTIC_CELL = {"15": "ST.O.A1", "16": "ST.O.A3", "17": "ST.O.A5", "19": "ST.O.A3"}


def dtic():
    nodes = []
    for path in sorted((SRC / "dtic").glob("[0-9]*.html")):
        major = path.stem
        raw = path.read_text(encoding="utf-8", errors="replace")
        title = re.search(r'class="fl-heading-text">\s*([^<]+)', raw)
        name = html.unescape(title.group(1)).strip() if title else major
        name = re.sub(r"^\d+\s*-\s*", "", name)
        cell = _DTIC_CELL.get(major, "ST.O.A3")
        nodes.append({"id": "DTIC:" + major, "code": major, "name": name, "level": 1,
                      "parent": None, "taxonomy_cell": cell})
        for code, label in re.findall(r'<td><a name="[^"]+"></a>(\d{2})</td>\s*(?:<p></p>\s*)?<td>([^<]+)</td>', raw):
            label = html.unescape(label).strip()
            label = re.sub(r"([a-z])([A-Z])", r"\1 \2", label)
            sub = major + "." + code
            subcell = cell
            if _word(label, ("intelligence", "information", "detection", "surveillance", "reconnaissance")):
                subcell = "ST.O.A5"
            elif _word(label, ("law", "conduct", "ethics", "treaty")):
                subcell = "ST.O.A4"
            elif _word(label, ("weapon", "ordnance", "missile", "ammunition", "defense", "defence", "operations")):
                subcell = "ST.O.A3"
            nodes.append({"id": "DTIC:" + sub, "code": sub, "name": label, "level": 2,
                          "parent": "DTIC:" + major, "taxonomy_cell": subcell})
    meta = {"scheme": "DTIC subject categories (military)",
            "source": "https://discover.dtic.mil/thesaurus/subject-categories/ (categories 15, 16, 17 and 19)",
            "retrieved": NEW,
            "licence": "Defense Technical Information Center thesaurus subject categories (public web pages). The full term list is sources/dtic_thesaurus.xlsx.",
            "note": "Only the military categories are mapped here. The other 21 DTIC categories are technical fields owned elsewhere. "
                    "The full term spreadsheet is a general technical thesaurus and is not dumped into strategy."}
    return split_write("dtic_military.json", meta, nodes)


# ---------- APSA organized sections ----------
def _apsa_cell(name):
    n = name.lower()
    if _word(n, ("conflict", "security", "peace", "war")):
        return "ST.O.A2"
    if _word(n, ("theory", "political thought", "ideas")):
        return "PL.O.A4"
    if _word(n, ("policy", "administration", "public admin")):
        return "PO.O.A4"
    if _word(n, ("election", "voting", "behavior", "behaviour", "opinion", "gender", "race", "psychology", "communication")):
        return "PO.O.A3"
    if _word(n, ("international", "foreign", "comparative politics", "relations")):
        return "PO.O.A5"
    return "PO.O.A2"


def apsa():
    raw = (SRC / "apsa_sections.html").read_text(encoding="utf-8", errors="replace")
    seen = []
    for num, name in re.findall(r"<strong>(\d+)\.\s+([^<]+)</strong>", raw):
        name = html.unescape(re.sub(r"\s+", " ", name)).strip()
        if (num, name) not in seen:
            seen.append((num, name))
    nodes = [{"id": "APSA:" + num, "code": num, "name": name, "level": 1, "parent": None,
              "taxonomy_cell": _apsa_cell(name)} for num, name in seen]
    meta = {"scheme": "APSA organized sections",
            "source": "https://www.apsanet.org/membership/organized-sections",
            "retrieved": NEW,
            "licence": "Section titles as published by the American Political Science Association on its organized-sections page.",
            "note": "Conflict, security and peace sections are ST.O.A2. Political theory is PL.O.A4. Policy and administration are PO.O.A4. Behaviour sections are PO.O.A3. International sections are PO.O.A5. The rest are PO.O.A2."}
    return split_write("apsa_sections.json", meta, nodes)


# ---------- Further UNESCO microthesauri ----------
def unesco_more():
    rdf = "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}"
    skos = "{http://www.w3.org/2004/02/skos/core#}"
    xml = "{http://www.w3.org/XML/1998/namespace}"
    root = __import__("xml.etree.ElementTree", fromlist=["ET"]).parse(SRC / "unesco-thesaurus.rdf").getroot()
    members = {}
    labels, broader = {}, {}
    for desc in root.iter(rdf + "Description"):
        about = desc.get(rdf + "about") or ""
        mt = about.rsplit("/", 1)[-1]
        if mt.startswith("mt"):
            members[mt] = [m.get(rdf + "resource") for m in desc.findall(skos + "member")]
        if "/concept" in about:
            for lab in desc.findall(skos + "prefLabel"):
                if lab.get(xml + "lang") == "en" and lab.text:
                    labels[about] = lab.text.strip()
            b = desc.find(skos + "broader")
            if b is not None and b.get(rdf + "resource"):
                broader.setdefault(about, b.get(rdf + "resource"))

    written = []

    def pack(mts, cell_of, scheme, filename, note):
        wanted = set()
        for mt in mts:
            for uri in members.get(mt, []):
                if uri and "/concept" in uri:
                    wanted.add(uri)
        nodes = []
        for uri in sorted(wanted):
            code = uri.rsplit("/", 1)[-1].replace("concept", "")
            parent = broader.get(uri)
            name = labels.get(uri, code)
            nodes.append({"id": "UNESCO:" + code, "code": code, "name": name, "level": 1,
                          "parent": ("UNESCO:" + parent.rsplit("/", 1)[-1].replace("concept", "")) if parent in wanted else None,
                          "taxonomy_cell": cell_of(name)})
        meta = {"scheme": scheme,
                "source": "https://vocabularies.unesco.org/exports/thesaurus/latest/unesco-thesaurus.rdf",
                "retrieved": NEW,
                "licence": "http://creativecommons.org/licenses/by-sa/3.0/igo/ (dct:license). Rights holder UNESCO.",
                "note": note}
        counts = split_write(filename, meta, nodes)
        written.append((scheme, counts))
        return counts

    def history(name):
        if _word(name, ("historiograph", "cause", "causation", "origin", "determin", "explanation")):
            return "HI.O.A3"
        if _word(name, ("chronolog", "periodization", "calendar", "dating", "century")):
            return "HI.O.A2"
        if _word(name, ("memory", "heritage", "commemorat", "oral tradition", "myth")):
            return "HI.O.A5"
        if _word(name, ("event", "fact", "occurrence", "source", "archive", "document")):
            return "HI.O.A1"
        return "HI.O.A4"

    def lingu(name):
        if _word(name, ("phonet", "phonolog", "speech", "acoustic", "pronunciation", "sound")):
            return "LN.O.A1"
        if _word(name, ("semantic", "meaning", "pragmat", "discourse", "lexic")):
            return "LN.O.A3"
        if _word(name, ("sociolingu", "dialect", "register", "variation")):
            return "LN.O.A4"
        if _word(name, ("family", "typolog", "language")):
            return "LN.O.A5"
        return "LN.O.A2"

    def law(name):
        if _word(name, ("court", "procedure", "evidence", "tribunal", "jurisdiction")):
            return "LA.O.A5"
        if _word(name, ("constitution", "administrative", "public law", "human right")):
            return "LA.O.A4"
        if _word(name, ("crime", "criminal", "tort", "delict", "remedy", "sanction")):
            return "LA.O.A3"
        if _word(name, ("contract", "obligation", "property", "liability")):
            return "LA.O.A2"
        return "LA.O.A1"

    def info(name):
        if _word(name, ("preserv", "archiv", "conservation", "digitisation", "digitization")):
            return "IS.O.A5"
        if _word(name, ("retriev", "search", "database", "index")):
            return "IS.O.A4"
        if _word(name, ("classif", "arrangement", "shelf", "taxonomy")):
            return "IS.O.A3"
        if _word(name, ("catalog", "metadata", "descri", "abstract")):
            return "IS.O.A2"
        return "IS.O.A1"

    pack(["mt3.25"], history, "UNESCO Thesaurus (History)", "unesco_history.json",
         "Microthesaurus mt3.25 History. Historiography and causation terms are HI.O.A3.")
    pack(["mt3.30"], lingu, "UNESCO Thesaurus (Linguistics)", "unesco_linguistics.json",
         "Microthesaurus mt3.30 Linguistics. Phonetics and speech are LN.O.A1. Semantics, pragmatics and lexicography are LN.O.A3.")
    pack(["mt3.35"], lambda _n: "LN.O.A5", "UNESCO Thesaurus (Languages)", "unesco_languages.json",
         "Microthesaurus mt3.35 Languages. All nodes are LN.O.A5.")
    pack(["mt6.05"], law, "UNESCO Thesaurus (Legal systems)", "unesco_law.json",
         "Microthesaurus mt6.05 Legal systems.")
    pack(["mt5.05", "mt5.15", "mt5.20", "mt5.25", "mt5.30", "mt5.35"], info,
         "UNESCO Thesaurus (Information)", "unesco_information.json",
         "Information microthesauri mt5.05, mt5.15, mt5.20, mt5.25, mt5.30 and mt5.35. Software and hardware microthesauri are left out.")

    # Indigenous terms scattered through the thesaurus. Provisional until Māori-led review.
    ik = []
    for uri, name in labels.items():
        if not re.search(r"\b(indigenous|aboriginal|first peoples|m[aā]ori)\b", name, re.I):
            continue
        code = uri.rsplit("/", 1)[-1].replace("concept", "")
        if _word(name, ("land", "water", "territor", "environment")):
            cell = "IK.O.A2"
        elif _word(name, ("educat", "language", "tradition", "knowledge")):
            cell = "IK.O.A4"
        elif _word(name, ("research", "data")):
            cell = "IK.O.A5"
        else:
            cell = "IK.O.A3"
        ik.append({"id": "UNESCO:" + code, "code": code, "name": name, "level": 1, "parent": None,
                   "taxonomy_cell": cell})
    meta = {"scheme": "UNESCO Thesaurus (Indigenous terms)",
            "source": "https://vocabularies.unesco.org/exports/thesaurus/latest/unesco-thesaurus.rdf",
            "retrieved": NEW,
            "licence": "http://creativecommons.org/licenses/by-sa/3.0/igo/ (dct:license). Rights holder UNESCO.",
            "note": "PROVISIONAL. English prefLabels matching indigenous, aboriginal, first peoples or Māori. "
                    "Not a Māori-led classification. Do not mark final. See docs/MAORI_REVIEW_PACK.md."}
    written.append(("UNESCO Thesaurus (Indigenous terms)", split_write("unesco_indigenous.json", meta, ik)))
    return written


def deepen(index):
    batch = (
        ("pacs2010.json", pacs, "PACS 2010"),
        ("iupac_goldbook.json", goldbook, "IUPAC Gold Book"),
        ("chebi_entities.json", chebi_entities, "ChEBI chemical entity"),
        ("naics2022.json", naics, "NAICS 2022"),
        ("isic_rev4.json", isic, "ISIC Rev. 4"),
        ("lcc_full.json", lcc_full, "LCC full schedules"),
        ("dtic_military.json", dtic, "DTIC military categories"),
        ("apsa_sections.json", apsa, "APSA sections"),
        ("unesco_more", unesco_more, "UNESCO further microthesauri"),
    )
    for _name, fn, scheme in batch:
        print("building", scheme, flush=True)
        result = fn()
        if _name == "unesco_more":
            pieces = result
        else:
            pieces = [(scheme, result)]
        for sch, counts in pieces:
            for field, count in counts.items():
                index[field]["maps"][sch] = count
                print(f"  {field} {sch} {count}", flush=True)
    return index
