"""Correspondence edges (handover WP1): schema, validator, loader and seed."""
import copy
import json
import subprocess
import sys
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "engine" / "v3"))
import correspondences as corr  # noqa: E402


@pytest.fixture(scope="module")
def index():
    return corr.NodeIndex(ROOT)


@pytest.fixture(scope="module")
def validator():
    return Draft202012Validator(corr.load_schema(ROOT))


@pytest.fixture(scope="module")
def edges():
    return corr.load_edges(ROOT)


def good_edge():
    return {
        "id": corr.edge_id("PH.O.A1.1", "EN.O.A1.1", "transfer"),
        "source": "PH.O.A1.1", "target": "EN.O.A1.1",
        "kind": "transfer", "directed": True,
        "mapping": {"objects": [], "methods": [], "warrants": []},
        "holds_under": [], "breaks_where": [],
        "status": "asserted",
        "provenance": {"origin": "manual", "date": "2026-11-10", "generated_by": "test",
                       "locators": [{"file": "pyramids/EN.md", "line": 1}]},
    }


def test_every_seed_edge_validates():
    assert corr.check(ROOT) == []


def test_seed_is_not_empty_and_ids_are_unique(edges):
    assert len(edges) >= 80
    ids = [edge["id"] for edge in edges]
    assert len(ids) == len(set(ids))


def test_ids_are_deterministic(edges):
    for edge in edges:
        assert edge["id"] == corr.edge_id(edge["source"], edge["target"], edge["kind"])


def test_seed_rebuild_changes_nothing():
    """The committed seed equals what the script writes from the pyramids."""
    before = {p.name: p.read_text(encoding="utf-8") for p in (ROOT / "correspondences").glob("seed_*.json")}
    subprocess.run([sys.executable, str(ROOT / "scripts" / "build_correspondences.py")],
                   check=True, capture_output=True)
    after = {p.name: p.read_text(encoding="utf-8") for p in (ROOT / "correspondences").glob("seed_*.json")}
    assert before == after


def test_uses_edges_run_from_owner_to_user(edges, index):
    uses = [e for e in edges if e["provenance"]["origin"] == "pyramid-uses-citation"]
    assert uses
    for edge in uses:
        assert edge["directed"] and edge["kind"] == "transfer" and edge["status"] == "asserted"
        assert index.field_of(edge["source"]) != index.field_of(edge["target"])
        assert edge["provenance"]["locators"]


def test_seed_does_not_invent_mappings(edges):
    for edge in edges:
        if edge["provenance"].get("kind_assigned_by") == "seed-rule":
            assert edge["mapping"] == {"objects": [], "methods": [], "warrants": []}
            assert edge["holds_under"] == [] and edge["breaks_where"] == []


def test_ma_statuses_follow_the_table(edges):
    by_name = {}
    for edge in edges:
        if edge["provenance"]["origin"] == "ma-correspondence-table":
            by_name.setdefault(edge["provenance"]["name"], set()).add(edge["status"])
    assert by_name["Modularity theorem"] == {"proved"}
    assert by_name["Index theory"] == {"proved"}
    assert by_name["Langlands programme"] == {"conjectured"}
    assert by_name["Topos theory"] == {"programme"}
    assert by_name["Algebraic topology"] == {"asserted"}
    assert "Computation ↔ everything" not in by_name


def test_unconvertible_rows_are_recorded_not_dropped():
    data = json.loads((ROOT / "correspondences" / "seed_ma.json").read_text(encoding="utf-8"))
    assert any(item["name"] == "Computation ↔ everything" for item in data["skipped"])


def test_good_edge_passes(index, validator):
    assert corr.edge_problems(good_edge(), index, validator) == []


@pytest.mark.parametrize("change, expect", [
    (lambda e: e.update(kind="metaphor"), "schema"),
    (lambda e: e.update(status="true"), "schema"),
    (lambda e: e.pop("breaks_where"), "schema"),
    (lambda e: e.update(extra=1), "schema"),
    (lambda e: e.update(target="PH.O.A1.1"), "same node"),
    (lambda e: e.update(source="ZZ.O.A1"), "does not resolve"),
    (lambda e: e.update(source="PH.O.A99.99"), "does not resolve"),
    (lambda e: e.update(source="MSC:99Zxx"), "does not resolve"),
    (lambda e: e["provenance"].update(locators=[]), "needs at least one locator"),
    (lambda e: e["provenance"].update(origin="transfer-operator"), "must be generated-unverified"),
    (lambda e: e["provenance"].update(locators=[{"file": "pyramids/NOPE.md", "line": 1}]), "not found"),
])
def test_bad_edges_are_reported(index, validator, change, expect):
    edge = copy.deepcopy(good_edge())
    change(edge)
    problems = corr.edge_problems(edge, index, validator)
    assert problems and any(expect in p for p in problems), problems


def test_generated_edge_must_stay_unverified(index, validator):
    edge = good_edge()
    edge["status"] = "generated-unverified"
    edge["provenance"]["origin"] = "transfer-operator"
    edge["provenance"]["locators"] = []
    assert corr.edge_problems(edge, index, validator) == []
    edge["status"] = "proved"
    assert corr.edge_problems(edge, index, validator)


def test_node_forms_resolve(index):
    assert index.field_of("EN") == "EN"
    assert index.field_of("MA.O.A2.5") == "MA"
    assert index.field_of("MSC:11Gxx") == "MA"
    assert index.field_of("MA.TK.42") == "MA"
    assert index.field_of("MA.O.A9.9") is None


def test_missing_folder_is_an_error_not_an_empty_list(tmp_path):
    with pytest.raises(corr.CorrespondenceError):
        corr.load_edges(tmp_path)
    assert corr.check(tmp_path) == ["correspondences/ not found"]


def test_malformed_file_is_an_error(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text("[]", encoding="utf-8")
    with pytest.raises(corr.CorrespondenceError):
        corr.load_file(bad)


def test_neighbours_respect_direction(edges):
    table = corr.neighbours(edges)
    directed = next(e for e in edges if e["directed"])
    assert any(other == directed["target"] for other, _ in table[directed["source"]])
    undirected = next(e for e in edges if not e["directed"])
    assert any(other == undirected["source"] for other, _ in table[undirected["target"]])


def test_check_script_covers_edges():
    text = (ROOT / "scripts" / "check.py").read_text(encoding="utf-8")
    assert "correspondence_check" in text
