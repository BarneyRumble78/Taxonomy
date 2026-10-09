"""Registry, SKOS, retired-ID and held-out file checks. Generated files are read, not edited."""
import csv, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CODES = "MA PH CH BI EA MD EN CS MS EC BU ST PO LA PL HI LN AR RE ED DE AG EV IS IK".split()


def test_retired_ms_o_a1_5_5_points_at_education_and_is_not_taught_as_live():
    reg = json.loads((ROOT / "registry" / "registry.json").read_text(encoding="utf-8"))
    row = next(r for r in reg if r["id"] == "MS.O.A1.5.5")
    assert "RETIRED" in row["label"]
    assert "ED" in row["uses"]
    for code in CODES:
        text = (ROOT / "pyramids" / f"{code}.md").read_text(encoding="utf-8")
        if "MS.O.A1.5.5" not in text:
            continue
        for line in text.splitlines():
            if "MS.O.A1.5.5" in line:
                assert re.search(r"retir", line, re.I), line
    # The mechanism of learning stays on the live MS cell. The theorem home is not this retired ID.
    ms = (ROOT / "pyramids" / "MS.md").read_text(encoding="utf-8")
    assert "MS.O.A1.5" in ms and "mechanism" in ms.lower()
    ma = (ROOT / "pyramids" / "MA.md").read_text(encoding="utf-8")
    assert "MS.O.A1.5.5" not in ma or "retir" in ma.lower()


def test_skos_matches_the_registry():
    skos = json.loads((ROOT / "public" / "v1" / "skos.jsonld").read_text(encoding="utf-8"))
    reg = json.loads((ROOT / "registry" / "registry.json").read_text(encoding="utf-8"))
    ids = {r["id"] for r in reg}
    labels = []
    for node in skos["@graph"]:
        label = node.get("skos:prefLabel")
        if isinstance(label, str):
            labels.append(label)
        uri = node.get("@id", "")
        if not uri.startswith("urn:taxonomy:"):
            continue
        ident = uri.split("urn:taxonomy:", 1)[1]
        if ident in ("scheme",) or ident in CODES:
            continue
        assert ident in ids, ident
    for code in CODES:
        assert any(code == node.get("@id", "").split(":")[-1] for node in skos["@graph"])
    # No SKOS concept id outside the registry, apart from the scheme and the 25 fields.
    extras = []
    for node in skos["@graph"]:
        ident = node.get("@id", "").split("urn:taxonomy:")[-1]
        if ident in ("scheme",) or ident in CODES or ident in ids:
            continue
        extras.append(ident)
    assert extras == []
    scheme = next(n for n in skos["@graph"] if n.get("@id") == "urn:taxonomy:scheme")
    assert scheme["dct:license"] == "https://creativecommons.org/licenses/by/4.0/"
    assert scheme["dct:rightsHolder"] == "Chris Townsend"


def test_index_count_matches_registry_build():
    index = json.loads((ROOT / "public" / "v1" / "index.json").read_text(encoding="utf-8"))
    reg = json.loads((ROOT / "registry" / "registry.json").read_text(encoding="utf-8"))
    assert index["version"] == "2.2.0-api.1"
    assert index["ids"] == len(reg) == 984
    assert index["licence"]["spdx"] == "CC-BY-4.0"
    assert index["licence"]["copyright"] == "Chris Townsend, 2026"
    assert index["licence"]["code"] == "Apache-2.0"


def test_heldout_file_is_frozen_shape_and_not_the_pilot_set():
    rows = list(csv.DictReader(open(ROOT / "pilot" / "heldout.tsv", encoding="utf-8"), delimiter="\t"))
    assert len(rows) >= 200
    need = {"id", "claim", "source", "owner", "cell", "warrant", "method", "notes"}
    assert need <= set(rows[0])
    owners = {}
    borders = 0
    pilot = (ROOT / "pilot" / "claims.tsv").read_text(encoding="utf-8")
    for r in rows:
        owners[r["owner"]] = owners.get(r["owner"], 0) + 1
        if r["notes"].startswith("border") or r["notes"].startswith("core-border"):
            borders += 1
        assert r["claim"] not in pilot
        assert r["owner"] in CODES
        assert r["cell"].startswith(r["owner"] + ".O.A")
    assert set(owners) == set(CODES)
    assert min(owners.values()) >= 4
    assert borders >= 30


def test_model_assist_harness_does_not_call_the_network():
    import subprocess, sys
    out = subprocess.run([sys.executable, "scripts/model_assist_eval.py"], cwd=ROOT, capture_output=True, text=True, check=True)
    assert "local contract ok" in out.stdout
    assert "not called" in out.stdout
    assert "http" not in out.stdout.lower()


def test_named_register_is_traced_to_pyramid_lines():
    path = ROOT / "registry" / "named.json"
    assert path.exists(), "run scripts/build_api.py"
    doc = json.loads(path.read_text(encoding="utf-8"))
    assert "UNVERIFIED" in doc["note"] or "traced" in doc["note"]
    assert doc["names"], "register should contain names already in the pyramids"
    files = {}
    for row in doc["names"]:
        src = ROOT / row["source"]
        if row["source"] not in files:
            files[row["source"]] = src.read_text(encoding="utf-8").splitlines()
        line = files[row["source"]][row["line"] - 1]
        assert row["name"] in line, row
        assert row["trace"] == "traced"
        assert row["field"] in CODES
