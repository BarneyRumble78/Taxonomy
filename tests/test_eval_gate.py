"""Locked checks for the cascade. Gold counts are not a growth target.

Parity is exact. Distractors must abstain or keep the gold owner.
The geopolitics probe must not be filed under a hard-science field.
The frozen file is an evaluation input only.
"""
import csv, hashlib, json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "engine"))
import taxonomy_engine as te

FROZEN = ROOT / "pilot" / "heldout.tsv"
FROZEN_SHA256 = "e6826cf6f46b69371f17c95c1aab9c771885bbbecc233e28f95b6f3577a4b856"
HARD_SCIENCE = {"MA", "PH", "CH", "BI", "EA", "MD", "EN", "CS"}
GEO = [
    ("Russian forces control Zarichne.", "PO"),
    ("Ukrainian units hold the village of Robotyne.", "PO"),
    ("The ceasefire line runs north of the river.", "PO"),
    ("China conducted drills in the waters around Taiwan.", "PO"),
    ("NATO members agreed to raise defence spending.", "PO"),
    ("The Security Council did not adopt the resolution.", "PO"),
    ("Israeli aircraft struck sites in Beirut.", "ST"),
    ("The Rafah crossing remained closed to civilians.", "PO"),
    ("North Korea launched a ballistic missile over the sea.", "PO"),
    ("Sudanese forces took the city of Wad Madani.", "PO"),
    ("The United States imposed sanctions on the oil trader.", "PO"),
    ("Peacekeepers deployed into the buffer zone.", "PO"),
    ("The occupied oblast is administered by the military.", "PO"),
]


def _rows():
    return list(csv.DictReader(FROZEN.open(encoding="utf-8"), delimiter="\t"))


def _core(p):
    if not p:
        return None
    return {k: p.get(k) for k in ("owner", "cell", "warrant", "method", "confidence", "contested_with")}


def _js(claims, vectors=None):
    payload = ROOT / "tests" / "_parity_payload.json"
    payload.write_text(json.dumps({"claims": claims, "vectors": vectors}), encoding="utf-8")
    try:
        out = subprocess.check_output(["node", str(ROOT / "tests" / "parity_check.mjs"), str(payload)], cwd=ROOT)
    finally:
        payload.unlink(missing_ok=True)
    return json.loads(out)


def test_frozen_file_unchanged():
    assert hashlib.sha256(FROZEN.read_bytes()).hexdigest() == FROZEN_SHA256
    assert len(_rows()) == 203


def test_index_matches_pyramid_text():
    digest, chunks = te.chunks_sha256()
    index = te.load_index()
    assert index["chunks_sha256"] == digest
    assert index["model"] == "BAAI/bge-small-en-v1.5"
    assert len(index["fields"]) == len(chunks) == 332
    assert all(len(v) == 384 for v in index["vectors"])


def test_rule_and_browser_parity_on_frozen_set():
    rows = _rows()
    claims = [r["claim"] for r in rows]
    js = _js(claims)
    for r, rule, stage in zip(rows, js["rules"], js["staged"]):
        assert _core(te.rule_placement(r["claim"])) == _core(rule), r["id"]
        py = te.stage_rule(r["claim"])
        assert py["reason"] == stage["reason"], r["id"]
        assert _core(py["placement"]) == _core(stage["placement"]), r["id"]


def test_place_parity_with_injected_vectors():
    rows = _rows()
    claims = [r["claim"] for r in rows]
    staged = [te.stage_rule(c) for c in claims]
    need = [c for c, s in zip(claims, staged) if s["reason"] is None]
    vectors = {c: v for c, v in zip(need, te.embed_queries(need))}
    packed = [vectors.get(c) for c in claims]
    js = _js(claims, packed)
    for r, decided, field in zip(rows, js["decided"], js["retrieved"]):
        stage = te.stage_rule(r["claim"])
        raw = vectors[r["claim"]] if stage["reason"] is None else None
        py_field = te.retrieve_field(json.loads(json.dumps(raw))) if raw is not None else None
        assert field == py_field, r["id"]
        py = te.adjudicate(stage, py_field)
        assert py["reason"] == decided["reason"], r["id"]
        assert _core(py.get("placement")) == _core(decided.get("placement")), r["id"]


def test_page_inlines_the_rule_stage():
    subprocess.check_call([sys.executable, str(ROOT / "scripts" / "build_site.py")], cwd=ROOT)
    page = (ROOT / "site" / "dist" / "minerva" / "index.html").read_text(encoding="utf-8")
    src = (ROOT / "engine" / "rules.mjs").read_text(encoding="utf-8")
    body = __import__("re").sub(r"^export ", "", src, flags=__import__("re").M)
    assert body in page
    assert "function classify(" in page
    assert "(?<![a-z0-9])" in page


def test_distractors_abstain_or_keep_gold_owner():
    rows = _rows()
    claims = [r["claim"] for r in rows]
    variants = {
        "physics": ["A photon carries quantum energy. " + c for c in claims],
        "law": [c + " under the Goods and Services Tax Act 1985." for c in claims],
        "math": ["The theorem has a proof. " + c for c in claims],
    }
    for name, texts in variants.items():
        for r, d in zip(rows, te.place_many(texts)):
            p = d.get("placement")
            assert p is None or p["owner"] == r["owner"], (name, r["id"], p["owner"] if p else None)


def test_geopolitics_probe_is_not_hard_science():
    details = te.place_many([text for text, _ in GEO])
    for (text, preferred), d in zip(GEO, details):
        p = d.get("placement")
        owner = p["owner"] if p else None
        assert owner is None or owner not in HARD_SCIENCE, (text, owner)
        assert owner is None or owner == preferred or owner == "ST", (text, owner, preferred)
    # A later cue list may place this as Politics. It must not come back as Physics.
    zarichne = details[0].get("placement")
    assert zarichne is None or zarichne["owner"] == "PO"


def test_answered_owner_accuracy():
    rows = _rows()
    placed = te.place_many([r["claim"] for r in rows])
    answered = [(r, d["placement"]) for r, d in zip(rows, placed) if d.get("placement")]
    assert answered, "cascade abstained on every claim"
    hit = sum(p["owner"] == r["owner"] for r, p in answered)
    assert hit / len(answered) >= 0.90


def test_growth_does_not_read_the_frozen_set():
    src = (ROOT / "scripts" / "grow_lexicon.py").read_text(encoding="utf-8")
    assert "pilot/heldout.tsv" not in src
    assert "heldout.tsv" not in src
    import importlib.util
    spec = importlib.util.spec_from_file_location("grow_lexicon", ROOT / "scripts" / "grow_lexicon.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    try:
        mod.refuse_frozen(FROZEN)
    except SystemExit:
        pass
    else:
        raise AssertionError("growth accepted the frozen file")
    acc, ok = mod.score()
    assert ok and acc >= 0.90
