"""Build subfield maps for all 25 fields from published taxonomies.

Sources (raw copies in sources/, retrieved 2026-10-12 unless noted):
  ANZSRC 2020 FoR   docs/anzsrc2020_for.xlsx (ABS)          -> maps/<FIELD>/anzsrc2020.json, every field
  PhySH             sources/physh.ttl (APS, GitHub)          -> maps/PH/physh.json
  JEL               sources/jel.xml (AEA)                    -> maps/EC/jel.json
  GCMD keywords     sources/gcmd_sciencekeywords.csv (NASA)  -> maps/EA/gcmd.json
MSC2020 (maps/MA/msc2020.json) was built earlier and is left as it is.
Placements under Taxonomy cells are editorial: see scripts/anzsrc_placement.py and the tables below.
Writes maps/index.json (primary map per field, node counts).
"""
import csv, json, sys, re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).parent))
from anzsrc_placement import GROUP, FIELD as FIELD6

FIELDS = "MA PH CH BI EA MD EN CS MS EC BU ST PO LA PL HI LN AR RE ED DE AG EV IS IK".split()
DATE = "2026-10-12"


def write(field, name, meta, nodes):
    d = ROOT / "maps" / field
    d.mkdir(parents=True, exist_ok=True)
    meta = dict(meta, nodes=len(nodes))
    (d / name).write_text(json.dumps(dict(meta, nodes=nodes), indent=0, ensure_ascii=False), encoding="utf-8")
    return meta


def fld(cell):
    return cell.split(".")[0]


# ---------- ANZSRC 2020 ----------
def anzsrc():
    import openpyxl
    ws = openpyxl.load_workbook(ROOT / "docs" / "anzsrc2020_for.xlsx", read_only=True)["Table 3"]
    per = defaultdict(list)
    div = grp = None
    for r in ws.iter_rows(values_only=True):
        if isinstance(r[0], (int, float)):
            div = (str(int(r[0])), str(r[1]).strip().capitalize())
        elif isinstance(r[1], (int, float)):
            code = str(int(r[1]))
            grp = code
            cell = GROUP[code]
            per[fld(cell)].append({"id": f"ANZSRC:{code}", "code": code, "name": str(r[2]).strip(), "level": 1,
                                   "parent": None, "division": div[0] + " " + div[1], "taxonomy_cell": cell})
        elif isinstance(r[2], (int, float)):
            code = str(int(r[2]))
            cell = FIELD6.get(code, GROUP[grp])
            node = {"id": f"ANZSRC:{code}", "code": code, "name": str(r[3]).strip(), "level": 2,
                    "parent": f"ANZSRC:{grp}", "taxonomy_cell": cell}
            f = fld(cell)
            if f != fld(GROUP[grp]):
                node["parent"] = None
                node["level"] = 1
                node["moved_from"] = f"ANZSRC:{grp}"
            per[f].append(node)
    meta = {"scheme": "ANZSRC 2020 Fields of Research", "source": "ABS 1297.0, docs/anzsrc2020_for.xlsx (Table 3)",
            "retrieved": DATE, "licence": "ABS publication; licence to be confirmed (UNVERIFIED)",
            "note": "Level 1 = 4-digit group, level 2 = 6-digit field. A field placed in a different Taxonomy field from its group appears there at level 1 with moved_from."}
    out = {}
    for f in FIELDS:
        if per[f]:
            out[f] = write(f, "anzsrc2020.json", meta, per[f])
    return out


# ---------- PhySH ----------
PHYSH_CELL = {
    "General Physics": "PH.O.A1", "Quantum Information, Science & Technology": "PH.O.A2",
    "Energy Science & Technology": "PH.O.A5", "Accelerators & Beams": "PH.O.A1",
    "Interdisciplinary Physics": "PH.O.A5", "Nonlinear Dynamics": "PH.O.A5",
    "Physics Education Research": "PH.O.A1", "Gravitation, Cosmology & Astrophysics": "PH.O.A3",
    "Nuclear Physics": "PH.O.A2", "Particles & Fields": "PH.O.A2", "Plasma Physics": "PH.O.A5",
    "Networks": "PH.O.A5", "Atomic, Molecular & Optical": "PH.O.A2", "Physics of Living Systems": "PH.O.A5",
    "Fluid Dynamics": "PH.O.A1", "Polymers & Soft Matter": "PH.O.A5",
    "Condensed Matter, Materials & Applied Physics": "PH.O.A4", "Statistical Physics & Thermodynamics": "PH.O.A4",
}


def physh():
    import rdflib
    from rdflib.namespace import SKOS, RDF, DCTERMS
    P = rdflib.Namespace("https://physh.org/rdf/2018/01/01/core#")
    g = rdflib.Graph()
    g.parse(ROOT / "sources" / "physh.ttl")
    short = lambda u: "PhySH:" + str(u).rsplit("/", 1)[-1]
    label = lambda u: str(g.value(u, SKOS.prefLabel) or g.value(u, DCTERMS.title) or "")
    disc = {}
    nodes = []
    for s in g.subjects(RDF.type, SKOS.ConceptScheme):
        name = label(s)
        if name in PHYSH_CELL:
            disc[s] = name
            nodes.append({"id": short(s), "code": short(s)[6:14], "name": name, "level": 1, "parent": None,
                          "kind": "discipline", "taxonomy_cell": PHYSH_CELL[name]})
    concepts = [c for c in g.subjects(RDF.type, SKOS.Concept) if not g.value(c, P.deprecated)]
    cset = set(concepts)
    for c in concepts:
        ds = [disc[d] for d in g.objects(c, P.inDiscipline) if d in disc]
        broader = [b for b in g.objects(c, SKOS.broader) if b in cset]
        facet = g.value(c, P.inFacet)
        n = {"id": short(c), "code": short(c)[6:14], "name": label(c), "level": 2 if not broader else 3,
             "parent": short(broader[0]) if broader else None, "disciplines": sorted(ds),
             "facet": label(facet) if facet else None,
             "taxonomy_cell": PHYSH_CELL[ds[0]] if ds else "PH.O.A1"}
        if not broader and ds:
            n["parent"] = short([d for d in disc if disc[d] == ds[0]][0])
        nodes.append(n)
    meta = {"scheme": "PhySH (Physics Subject Headings)", "source": "https://github.com/physh-org/PhySH physh.ttl",
            "retrieved": DATE, "licence": "CC0 1.0 (physh.org/licensing)",
            "note": "Level 1 = discipline; level 2 = concept with no broader concept, placed under its first discipline; level 3 = narrower concept. Deprecated concepts dropped."}
    return {"PH": write("PH", "physh.json", meta, nodes)}


# ---------- JEL ----------
JEL_CELL = {"A": "EC.O.A1", "B": "EC.O.A1", "C": "EC.O.A4", "D": "EC.O.A1", "E": "EC.O.A4", "F": "EC.O.A4",
            "G": "EC.O.A2", "H": "EC.O.A5", "I": "EC.O.A5", "J": "EC.O.A2", "K": "EC.O.A3", "L": "EC.O.A2",
            "M": "EC.O.A3", "N": "EC.O.A4", "O": "EC.O.A4", "P": "EC.O.A3", "Q": "EC.O.A2", "R": "EC.O.A2",
            "Y": "EC.O.A1", "Z": "EC.O.A5"}


def jel():
    import xml.etree.ElementTree as ET
    root = ET.parse(ROOT / "sources" / "jel.xml").getroot()
    nodes = []

    def walk(el, parent, level):
        for c in el.findall("classification"):
            code = c.findtext("code").strip()
            nodes.append({"id": f"JEL:{code}", "code": code, "name": (c.findtext("description") or "").strip(),
                          "level": level, "parent": parent, "taxonomy_cell": JEL_CELL.get(code[0], "EC.O.A1")})
            walk(c, f"JEL:{code}", level + 1)
    walk(root, None, 1)
    meta = {"scheme": "JEL Classification System", "source": "https://www.aeaweb.org/econlit/classificationTree.xml",
            "retrieved": DATE, "licence": "AEA: free for scholarly use"}
    return {"EC": write("EC", "jel.json", meta, nodes)}


# ---------- GCMD ----------
GCMD_CELL = {"ATMOSPHERE": "EA.O.A4", "BIOSPHERE": "EA.O.A4", "BIOLOGICAL CLASSIFICATION": "EA.O.A4",
             "CLIMATE INDICATORS": "EA.O.A4", "CRYOSPHERE": "EA.O.A4", "HUMAN DIMENSIONS": "EA.O.A5",
             "LAND SURFACE": "EA.O.A4", "OCEANS": "EA.O.A4", "PALEOCLIMATE": "EA.O.A3", "SOLID EARTH": "EA.O.A2",
             "SPECTRAL/ENGINEERING": "EA.O.A1", "SUN-EARTH INTERACTIONS": "EA.O.A4",
             "TERRESTRIAL HYDROSPHERE": "EA.O.A4", "AGRICULTURE": "EA.O.A5"}


def gcmd():
    rows = list(csv.reader(open(ROOT / "sources" / "gcmd_sciencekeywords.csv", encoding="utf-8")))[2:]
    nodes, seen = [], {}
    for r in rows:
        path = [x.strip() for x in r[1:7] if x.strip()]
        if not path:
            continue
        for i in range(len(path)):
            key = " > ".join(path[:i + 1])
            if key in seen:
                continue
            nid = f"GCMD:{r[7]}" if i == len(path) - 1 else f"GCMD:{key}"
            seen[key] = nid
            nodes.append({"id": nid, "code": key, "name": path[i].title(), "level": i + 1,
                          "parent": seen.get(" > ".join(path[:i])) if i else None,
                          "taxonomy_cell": GCMD_CELL.get(path[0], "EA.O.A4")})
    meta = {"scheme": "GCMD Science Keywords", "source": "https://gcmd.earthdata.nasa.gov/kms (sciencekeywords CSV, version 24.9)",
            "retrieved": DATE, "licence": "NASA GCMD: CC0 unless marked",
            "note": "Category EARTH SCIENCE dropped; level 1 = Topic, then Term and Variable levels."}
    return {"EA": write("EA", "gcmd.json", meta, nodes)}


PRIMARY = {"MA": "msc2020.json", "PH": "physh.json", "EC": "jel.json", "EA": "gcmd.json"}


def main():
    built = defaultdict(dict)
    for fn in (anzsrc, physh, jel, gcmd):
        for f, m in fn().items():
            built[f][m["scheme"]] = m["nodes"]
    msc = json.loads((ROOT / "maps" / "MA" / "msc2020.json").read_text(encoding="utf-8"))
    built["MA"][msc["scheme"]] = len(msc["nodes"])
    index = {f: {"primary": PRIMARY.get(f, "anzsrc2020.json"), "maps": built[f]} for f in FIELDS}
    (ROOT / "maps" / "index.json").write_text(json.dumps(index, indent=1, ensure_ascii=False), encoding="utf-8")
    for f in FIELDS:
        print(f, index[f]["primary"], index[f]["maps"])


if __name__ == "__main__":
    main()
