import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "engine"))
import taxonomy_engine as te

CODES = "MA PH CH BI EA MD EN CS MS EC BU ST PO LA PL HI LN AR RE ED DE AG EV IS IK".split()

def test_all_fields_present():
    assert sorted(te.LEXICON["fields"]) == sorted(CODES)
    assert sorted(te.NAMES) == sorted(CODES)

def test_lexicon_cells_match_key_lines():
    for c in CODES:
        assert len(te.LEXICON["fields"][c]["cells"]) == len(te.CELLS[c]), c

def test_w13_never_travels():
    r = te.classify("According to tradition the sacred doctrine says the bridge deflection stays below span/800.")
    assert r["warrant"] != "W13" or r["owner"] in ("RE", "IK")

def test_known_border_cases():
    assert te.classify("The importer must pay GST at the border under the Goods and Services Tax Act 1985.")["owner"] == "LA"
    assert te.classify("Every bounded sequence of real numbers has a convergent subsequence.")["owner"] == "MA"

def test_pilot_regression():
    # NOTE: lexicon was written with these claims in view; this is a regression floor, not a validity measure.
    s = te.evaluate(ROOT / "pilot" / "key.tsv")
    assert s["owner"] >= 0.90 and s["cell"] >= 0.80


def test_short_cues_do_not_fire_inside_other_words():
    # "force" is physics; "forces" is not. "ion", "ring", "prime" and "sin" are not parts of ordinary words.
    assert te.classify("In an inertial frame, the net force on a particle equals its mass times its acceleration.")["owner"] == "PH"
    assert te.classify("The unemployment rate is the share of the labour force that is without work and seeking work.")["owner"] == "EC"
    assert te.classify("Prime numbers are infinite.")["owner"] == "MA"
    assert te.classify("A national mobilisation followed the invasion.")["owner"] == "ST"
    assert te.classify("Neighbouring states signed a ceasefire.")["owner"] != "MA"
    single = te.classify("Using a single press statement, the ministry described the withdrawal of its forces.")
    assert single["owner"] != "RE"
    assert single["warrant"] == "W7"
