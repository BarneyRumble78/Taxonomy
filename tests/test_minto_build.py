"""The free rebuild is not a Minto classification. No model and no network."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "engine" / "v3"))
from minto_build import audit_field, build_pyramid, min_new_groups
from minto_check import minto_counts


def _write_map(root, field, filename, nodes):
    folder = root / "maps" / field
    folder.mkdir(parents=True)
    (folder / filename).write_text(json.dumps({"nodes": nodes}), encoding="utf-8")


def _write_rule(root, field, members, cap=2, objects=None):
    rule = {
        "field": field,
        "source": "test",
        "scope": "The test field places each claim in one cell of its key line.",
        "organising_principle": "the test dimension",
        "key_line": {
            "basis": "kinds",
            "order": "structure",
            "dimension": "the test dimension",
            "members": members,
            "order_note": "structural",
        },
        "depth_cap": cap,
        "authority": "test",
        "indigenous_routes": "pyramids/rebuild/ANZSRC45.json",
    }
    if objects:
        rule["objects"] = objects
    folder = root / "pyramids" / "rebuild"
    folder.mkdir(parents=True)
    (folder / f"{field}.json").write_text(json.dumps(rule), encoding="utf-8")
    (folder / "ANZSRC45.json").write_text(json.dumps({
        "routes": [],
        "default_owner": "IK",
        "default_cell": "IK.O.A5",
        "default_reason": "test",
    }), encoding="utf-8")


def test_new_groups_cover_an_oversized_sibling_list():
    assert min_new_groups(5) == 0
    assert min_new_groups(6) == 2
    assert min_new_groups(22) == 5


def test_a_cell_of_names_fails_the_checker(tmp_path):
    _write_rule(tmp_path, "AG", ["One", "Two", "Three", "Four", "Five"])
    nodes = [
        {"id": f"N{i}", "code": str(i), "name": f"Topic {i}", "level": 1, "parent": None, "taxonomy_cell": "AG.O.A1"}
        for i in range(6)
    ]
    _write_map(tmp_path, "AG", "demo.json", nodes)
    pyramid, meta = build_pyramid("AG", tmp_path, catalogue=False)
    counts = minto_counts(pyramid)
    assert meta["admitted"] == 6
    assert counts["loose_topics"] == 6
    assert counts["missing_basis"] >= 1
    assert counts["missing_summaries"] >= 1
    assert counts["template_summaries"] == 0
    from minto_check import minto_issues
    assert "key line" not in minto_issues(pyramid)["missing_basis"]


def test_lcc_schedule_lines_are_filed_before_a_model_is_priced(tmp_path):
    _write_rule(tmp_path, "HI", ["Occurrence", "Time", "Cause", "Change and continuity", "Meaning and memory"])
    nodes = [
        {"id": "F", "code": "F", "name": "United States local history", "level": 1, "parent": None, "taxonomy_cell": "HI.O.A4"},
        {"id": "F1", "code": "F1", "name": "Periodicals", "level": 2, "parent": "F", "taxonomy_cell": "HI.O.A4"},
        {"id": "F1.5", "code": "F1.5", "name": "Museums", "level": 2, "parent": "F", "taxonomy_cell": "HI.O.A4"},
    ]
    _write_map(tmp_path, "HI", "lcc_full.json", nodes)
    literal, _ = build_pyramid("HI", tmp_path, catalogue=False)
    concept, meta = build_pyramid("HI", tmp_path, catalogue=True)
    assert minto_counts(literal)["loose_topics"] == 0
    assert minto_counts(literal)["group_size"] >= 1
    assert meta["lcc_filed"] == 2
    assert meta["admitted"] == 1
    assert minto_counts(concept)["loose_topics"] == 1


def test_a_flat_index_is_catalogued(tmp_path):
    _write_rule(tmp_path, "CH", ["One", "Two", "Three", "Four", "Five"])
    nodes = [
        {"id": f"G{i}", "code": str(i), "name": f"Term {i}", "level": 1, "parent": None, "taxonomy_cell": "CH.O.A1"}
        for i in range(12)
    ]
    _write_map(tmp_path, "CH", "iupac_goldbook.json", nodes)
    _pyramid, meta = build_pyramid("CH", tmp_path, catalogue=True, flat_min_nodes=10)
    assert meta["flat_filed"] == 12
    assert meta["admitted"] == 0
    assert "iupac_goldbook.json" in meta["flat_files"]


def test_live_mathematics_and_history_fail_the_checker_in_the_expected_shape():
    mathematics = audit_field("MA", ROOT)
    history = audit_field("HI", ROOT)
    raw = mathematics["literal"]
    assert raw["admitted"] == 71
    assert raw["loose_topics"] == 71
    assert raw["oversized_groups"] == 4
    assert raw["undersized_groups"] == 1
    assert raw["missing_basis"] == 10
    assert raw["missing_order"] == 10
    assert raw["template_summaries"] == 0
    assert raw["missing_summaries"] == 11
    assert raw["checker"]["loose_topics"] == raw["loose_topics"]
    assert raw["worst"]["children"] == 22
    hist = history["literal"]
    assert hist["admitted"] == 56002
    assert hist["loose_topics"] == 214
    assert hist["oversized_groups"] == 46
    assert hist["missing_basis"] == 80
    assert hist["missing_summaries"] == 80
    assert hist["template_summaries"] == 0
    assert hist["worst"]["children"] == 11557
    assert history["concept"]["lcc_filed"] == 55822
    assert history["concept"]["admitted"] == 180
