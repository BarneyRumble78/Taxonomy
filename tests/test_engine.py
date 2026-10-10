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

def test_left_boundary():
    assert te.cue_hit(" forces ", "force")
    assert te.cue_hit(" topology ", "topolog")
    assert not te.cue_hit(" inflation ", "ion")
    assert not te.cue_hit(" defence ", "ce")
    assert not te.cue_hit(" assigned ", "signed")
    assert not te.cue_hit(" christchurch ", "church")
    assert te.cue_hit(" every bounded ", "every ")

def test_w13_never_travels():
    r = te.rule_placement("According to tradition the sacred doctrine says the bridge deflection stays below span/800.")
    assert r is None or r["warrant"] != "W13" or r["owner"] in ("RE", "IK")

def test_known_border_cases():
    # The rule stage still owns these. The public cascade may abstain if retrieval disagrees.
    gst = "The importer must pay GST at the border under the Goods and Services Tax Act 1985."
    assert te.rule_placement(gst)["owner"] == "LA"
    assert te.stage_rule(gst)["placement"]["owner"] == "LA"
    seq = "Every bounded sequence of real numbers has a convergent subsequence."
    assert te.rule_placement(seq)["owner"] == "MA"
    assert te.rule_placement(seq)["method"] == "M2"
    assert te.rule_placement("Every finite integral domain is a field")["cell"] == "MA.O.A2"

def test_warrant_only_when_a_cue_fired():
    r = te.rule_placement("Russian forces control Zarichne.")
    assert r["owner"] == "PH"
    assert r["warrant"] is None and r["method"] is None
    proved = te.rule_placement("Prove that every finite integral domain is a field.")
    assert proved["warrant"] == "W1" and proved["method"] == "M2"

def test_weak_band_abstains_before_retrieval(monkeypatch):
    def explode(texts):
        raise AssertionError("retrieval must not run under 0.40")
    monkeypatch.setattr(te, "embed_queries", explode)
    detail = te.place_detail("The particle has a gene.")
    assert detail["placement"] is None and detail["reason"] == "low_confidence"

def test_pilot_regression():
    # Lexicon was written with these claims in view. This is a rule-stage floor, not a validity measure.
    rows = list(__import__("csv").DictReader(open(ROOT / "pilot" / "key.tsv", encoding="utf-8"), delimiter="\t"))
    hit = {"owner": 0, "cell": 0}
    for r in rows:
        p = te.rule_placement(r["claim"]) or {}
        for k in hit:
            hit[k] += int(p.get(k) == r[k])
    n = len(rows)
    assert hit["owner"] / n >= 0.90 and hit["cell"] / n >= 0.80
