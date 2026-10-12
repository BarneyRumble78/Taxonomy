"""Free rebuild groundwork. These tests do not call a model or the network."""
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "engine" / "v3"))
from cost_cap import allow, empty_ledger, hybrid_estimate, record
from crosslinks import check as cross_check, dangling_uses
from field_rebuild import (
    classify_nodes,
    indigenous_route,
    is_fine,
    is_shelf,
    load_indigenous,
    load_rule,
    prepare,
    shared_queue,
    validate_rule,
)
from minto_check import BASIS_ORDERS
from question_pyramid import load, validate
from shortlist import ranked_shortlist

FIELDS = "AG AR BI BU CH CS DE EA EC ED EN HI IK IS LA LN MA MD MS PH PL PO RE ST".split()


def _queue_module():
    path = ROOT / "scripts" / "run_pyramid_queue.py"
    spec = importlib.util.spec_from_file_location("run_pyramid_queue_fields", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _rebuild_main():
    path = ROOT / "scripts" / "rebuild_classification.py"
    spec = importlib.util.spec_from_file_location("rebuild_classification", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.main


def test_every_field_rule_is_a_legal_minto_pair():
    for field in FIELDS:
        rule = load_rule(field, ROOT)
        assert rule["field"] == field
        assert validate_rule(rule) == []
        key = rule["key_line"]
        assert key["order"] in BASIS_ORDERS[key["basis"]]
        assert 2 <= len(key["members"]) <= 5
        assert rule["scope"].count(".") == 1
        if key["order"] == "degree":
            assert key["rank_note"]
        assert rule["depth_cap"] == (1 if field == "MA" else 2)
    maths = load_rule("MA", ROOT)
    assert maths["key_line"]["basis"] == "parts"
    assert maths["key_line"]["order"] == "structure"
    assert maths["objects"]["basis"] == "cause_effect"
    assert maths["objects"]["order"] == "time"
    assert maths["objects"]["rank_note"]
    economics = load_rule("EC", ROOT)
    assert economics["key_line"]["order"] == "degree"
    indigenous = load_rule("IK", ROOT)
    assert indigenous["provisional"] is True


def test_indigenous_routes_split_subject_claims_and_keep_custom_in_ik():
    table = load_indigenous(ROOT)
    assert "never licenses a measurement" in table["w13"]
    treaty = indigenous_route({"id": "ANZSRC:4505", "code": "4505", "name": "Te Tiriti o Waitangi duties"}, table)
    assert treaty["owner"] == "LA"
    assert treaty["cell"] == "LA.O.A4"
    law = indigenous_route({"id": "X", "code": "4512", "name": "tikanga as part of state law"}, table)
    assert law["owner"] == "LA"
    custom = indigenous_route({"id": "Y", "code": "4507", "name": "tikanga in social life"}, table)
    assert custom["owner"] == "IK"
    assert custom["cell"] == "IK.O.A3"
    plain = indigenous_route({
        "id": "ANZSRC:4501",
        "code": "4501",
        "name": "Aboriginal and Torres Strait Islander culture, language and history",
    }, table)
    assert plain["owner"] == "IK"
    assert plain["id"] == "indigenous-studies"
    integral = indigenous_route({
        "id": "MSC:45-XX",
        "code": "45-XX",
        "name": "Integral equations",
    }, table)
    assert integral is None


def test_fine_nodes_file_under_the_capped_parent_and_keep_an_override():
    assert not is_shelf({"code": "03B44"})
    assert not is_shelf({"code": "00-XX"})
    assert is_shelf({"code": "QA75.5-76.95"})
    assert is_fine({"code": "03B44", "level": 3}, 1)
    assert not is_fine({"code": "00-XX", "level": 1}, 1)
    assert not is_fine({"code": "QA75.5-76.95", "level": 2}, 2)
    assert is_fine({"code": "QA75.5-76.95", "level": 4}, 2)
    nodes = [
        {"id": "MSC:03-XX", "code": "03-XX", "name": "Logic", "level": 1, "parent": None, "taxonomy_cell": "MA.O.A1"},
        {"id": "MSC:03Bxx", "code": "03Bxx", "name": "General logic", "level": 2, "parent": "MSC:03-XX", "taxonomy_cell": "MA.O.A1"},
        {"id": "MSC:03B44", "code": "03B44", "name": "A fine topic", "level": 3, "parent": "MSC:03Bxx"},
        {"id": "MSC:03E05", "code": "03E05", "name": "An override", "level": 3, "parent": "MSC:03Bxx", "taxonomy_cell": "MA.O.A2"},
        {"id": "MSC:99-XX", "code": "99-XX", "name": "Unplaced", "level": 1, "parent": None},
    ]
    rows = {row["id"]: row for row in classify_nodes(nodes, "MA", 1, load_indigenous(ROOT))}
    assert rows["MSC:03B44"]["status"] == "filed"
    assert rows["MSC:03B44"]["cell"] == "MA.O.A1"
    assert rows["MSC:03B44"]["parent"] == "MSC:03-XX"
    assert rows["MSC:03E05"]["status"] == "kept_override"
    assert rows["MSC:03E05"]["cell"] == "MA.O.A2"
    assert rows["MSC:99-XX"]["status"] == "model"
    assert rows["MSC:03-XX"]["status"] == "ruled"


def test_mesh_ui_is_one_row_when_two_fields_share_it(tmp_path):
    def write(field, nodes):
        folder = tmp_path / "maps" / field
        folder.mkdir(parents=True)
        (folder / "mesh2026.json").write_text(json.dumps({"nodes": nodes}), encoding="utf-8")

    write("MD", [
        {"id": "MeSH:C01", "ui": "D001", "code": "C01", "name": "Shared term", "level": 2, "taxonomy_cell": "MD.O.A1"},
        {"id": "MeSH:C01.001", "ui": "D002", "code": "C01.001", "name": "Twice", "level": 3, "taxonomy_cell": "MD.O.A1"},
        {"id": "MeSH:C02.001", "ui": "D002", "code": "C02.001", "name": "Twice", "level": 3, "taxonomy_cell": "MD.O.A1"},
        {"id": "MeSH:plain-md", "ui": "D009", "code": "", "name": "No tree", "level": 2, "taxonomy_cell": "MD.O.A1"},
    ])
    write("BI", [
        {"id": "MeSH:G01", "ui": "D001", "code": "G01", "name": "Shared term", "level": 2, "taxonomy_cell": "BI.O.A3"},
        {"id": "MeSH:plain-bi", "ui": "D009", "code": "", "name": "No tree", "level": 2, "taxonomy_cell": "BI.O.A3"},
    ])
    summary = shared_queue(["MD", "BI"], tmp_path, include_rows=True)
    assert summary["descriptor_rows"] == 3
    assert summary["tree_copies"] == 6
    assert summary["shared_descriptors"] == 2
    assert summary["conflicts"] == 2
    assert summary["cross_field_conflicts"] == 2
    assert summary["resolved"] == 1
    assert summary["unresolved"] == 1
    shared = next(row for row in summary["rows"] if row["ui"] == "D001")
    assert shared["status"] == "ruled"
    assert shared["home"] == "MD"
    assert shared["primary_code"] == "C01"
    assert len(shared["copies"]) == 2
    open_row = next(row for row in summary["rows"] if row["ui"] == "D009")
    assert open_row["status"] == "model"
    twice = next(row for row in summary["rows"] if row["ui"] == "D002")
    assert twice["status"] == "home"
    assert len(twice["copies"]) == 2


def test_crosslink_resolves_a_defined_id_and_flags_an_unknown_one(tmp_path):
    folder = tmp_path / "pyramids"
    folder.mkdir()
    (folder / "MA.md").write_text("### MA.O.A1 Foundations\n", encoding="utf-8")
    (folder / "PH.md").write_text("The proof uses MA.O.A1. The other uses ZZ.O.A9.\n", encoding="utf-8")
    problems = dangling_uses(tmp_path)
    assert problems == ["PH cites undefined ZZ.O.A9"]
    queue = folder / "queues"
    queue.mkdir()
    (queue / "ZZ.routes.jsonl").write_text('{"field": "ZZ", "name": "nope"}\n', encoding="utf-8")
    found = cross_check(tmp_path)
    assert found["routes"] == ["ZZ.routes.jsonl routes to unknown field ZZ"]


def test_live_corpus_crosslinks_resolve():
    found = cross_check(ROOT)
    assert found["dangling"] == []
    assert found["routes"] == []


def test_question_builder_accepts_the_nitrogen_pyramid_and_rejects_six_issues():
    path = ROOT / "pyramids" / "questions" / "EV_Q1_nz_nitrogen_eutrophication.json"
    assert validate(load(path)) == []
    data = load(path)
    extra = dict(data["key_line"]["points"][0])
    extra["id"] = "Q1.9"
    data["key_line"]["points"] = list(data["key_line"]["points"]) + [extra, extra, extra]
    problems = validate(data)
    assert any("6 issues" in item for item in problems)


def test_cost_cap_stops_on_the_field_before_the_global_budget():
    ledger = empty_ledger()
    assert allow(ledger, "MA", 9, 10, 90)[0] is True
    allowed, scope, _, _ = allow(ledger, "MA", 11, 10, 90)
    assert allowed is False
    assert scope == "field"
    record(ledger, "PH", 85)
    allowed, scope, _, _ = allow(ledger, "MA", 6, 10, 90)
    assert allowed is False
    assert scope == "global"
    record(ledger, "MA", 9)
    allowed, scope, _, _ = allow(ledger, "MA", 2, 10, 90)
    assert allowed is False
    assert scope == "field"
    estimate = hybrid_estimate(1000, 4)
    assert estimate["ollama_items"] == 1000
    assert estimate["escalate_items"] == 4
    assert estimate["claude_usd"] == round(4 * 0.90 / 1000, 6)
    assert estimate["upper_if_all_model_items"] == round(1000 * 0.90 / 1000, 6)
    assert estimate["claude_usd"] != estimate["upper_if_all_model_items"]


def test_shortlist_keeps_key_line_cells_inside_the_width():
    catalog = [
        {"group_id": "MA.P.1", "statement": "Objects"},
        {"group_id": "MA.P.2", "statement": "Practices"},
        {"group_id": "MA.P.3", "statement": "Bridges"},
    ]
    catalog.extend(
        {"group_id": f"MA.P.1.{index}", "statement": f"topic {index} algebra"}
        for index in range(1, 20)
    )
    chosen = ranked_shortlist("algebra", catalog, width=12)
    assert len(chosen) == 12
    assert {row["group_id"] for row in chosen[:3]} == {"MA.P.1", "MA.P.2", "MA.P.3"}


def test_catalog_offers_a_deeper_hazard_group_and_the_old_choices_stay_exact():
    module = _queue_module()
    by_id = {row["group_id"]: row for row in module.cell_catalog("EV")}
    assert "EV.P.2.6.2.1" in by_id
    assert "EV.P.4.7.1.1" in by_id
    assert by_id["EV.P.1"]["cell"] == "EV.O.A1"
    assert "EV.P.2.8" not in by_id
    assert "EV.P.2.10" not in by_id
    catalog = [
        {"group_id": "EV.P.1", "statement": "Pressures are loads."},
        {"group_id": "EV.P.2", "statement": "States are conditions."},
    ]
    body = module.request_body({
        "node_id": "GEMET:1",
        "name": "acid rain",
        "cell": "EV.O.A1",
        "candidates": [
            {"facet": "emissions", "group_id": "EV.P.1.1", "statement": "Emissions are loads."},
            {"facet": "land", "group_id": "EV.P.1.2", "statement": "Land use is a load."},
        ],
    }, catalog=catalog)
    payload = json.loads(body["messages"][1]["content"])
    assert payload["items"][0]["choices"] == ["EV.P.1", "EV.P.2", "EV.P.1.1", "EV.P.1.2", "unsure", "out_of_scope"]


def _place_item(number):
    return {
        "task": "place",
        "node_id": f"N{number}",
        "name": f"concept {number}",
        "cell": "EV.O.A1",
        "candidates": [
            {"group_id": "EV.P.1", "statement": "Pressures are loads."},
            {"group_id": "EV.P.2", "statement": "States are conditions."},
        ],
    }


def _queue_root(tmp_path, items, previous=None):
    queue_dir = tmp_path / "pyramids" / "queues"
    queue_dir.mkdir(parents=True)
    (queue_dir / "EV.json").write_text(json.dumps({"field": "EV", "items": items}), encoding="utf-8")
    if previous is not None:
        (queue_dir / "EV.placed.json").write_text(
            json.dumps({"field": "EV", "items": previous}),
            encoding="utf-8",
        )
    return tmp_path


def test_hybrid_dry_run_prices_only_escalated_rows(tmp_path, capsys):
    module = _queue_module()
    previous = [{
        "node_id": "N0",
        "status": "unsure",
        "group_id": "unsure",
        "reason": "no home",
    }]
    root = _queue_root(tmp_path, [_place_item(0), _place_item(1)], previous)

    def post(body):
        raise AssertionError("dry-run must not call the model")

    args = module.parse_args(["--field", "EV", "--backend", "hybrid", "--dry-run"])
    assert args.global_max_cost == 60
    assert args.max_cost == 10
    result = module.run(args, post=post, root=root)
    assert result["cost"] == 0
    assert result["ollama_items"] == 1
    assert result["escalate_items"] == 1
    assert result["claude_usd"] == round(0.90 / 1000, 6)
    assert result["upper_if_all_model_items"] == round(0.90 / 1000, 6)
    output = capsys.readouterr().out
    assert "backend=hybrid" in output
    assert "No unsure rate is applied." in output


def test_hybrid_sends_only_unsure_rows_to_claude(tmp_path):
    module = _queue_module()
    root = _queue_root(tmp_path, [_place_item(0), _place_item(1)])
    calls = {"ollama": 0, "claude": 0}

    def ollama(body):
        calls["ollama"] += 1
        assert body["think"] is False
        assert body["stream"] is False
        payload = json.loads(body["messages"][1]["content"])
        rows = []
        for item in payload["items"]:
            if item["id"] == "N0":
                rows.append({"id": "N0", "group_id": "EV.P.1", "reason": "a load"})
            else:
                rows.append({"id": item["id"], "group_id": "unsure", "reason": "no home"})
        return {"message": {"content": json.dumps({"items": rows})}}

    def claude(payload):
        calls["claude"] += 1
        user = json.loads(payload["messages"][0]["content"])
        assert [item["id"] for item in user["items"]] == ["N1"]
        return {
            "content": [{"type": "tool_use", "name": "record_placements", "input": {"items": [
                {"id": "N1", "group_id": "EV.P.2", "reason": "a state"},
            ]}}],
            "usage": {"input_tokens": 100, "output_tokens": 20},
        }

    args = module.parse_args([
        "--field", "EV", "--backend", "hybrid", "--workers", "1", "--batch", "15", "--progress", "100",
    ])
    result = module.run(args, post=ollama, root=root, anthropic_post=claude)
    assert calls == {"ollama": 1, "claude": 1}
    assert result["stopped"] is False
    assert result["cost"] > 0
    text = (root / "pyramids" / "queues" / "EV.placed.jsonl").read_text(encoding="utf-8")
    rows = [json.loads(line) for line in text.splitlines()]
    by_id = {row["node_id"]: row for row in rows}
    assert by_id["N0"]["group_id"] == "EV.P.1"
    assert by_id["N1"]["status"] == "placed"
    assert by_id["N1"]["group_id"] == "EV.P.2"


def test_global_max_cost_stops_before_the_field_cap(tmp_path, capsys):
    module = _queue_module()
    root = _queue_root(tmp_path, [_place_item(number) for number in range(30)])
    calls = {"n": 0}

    def client(payload):
        calls["n"] += 1
        user = json.loads(payload["messages"][0]["content"])
        rows = [{"id": item["id"], "group_id": "unsure", "reason": "no home"} for item in user["items"]]
        return {
            "content": [{"type": "tool_use", "name": "record_placements", "input": {"items": rows}}],
            "usage": {"input_tokens": 1_000_000, "output_tokens": 100},
            "model": payload["model"],
        }

    args = module.parse_args([
        "--field", "EV", "--backend", "anthropic", "--batch", "15", "--workers", "1",
        "--max-cost", "1000", "--global-max-cost", "1", "--progress", "100",
    ])
    result = module.run(args, post=client, root=root)
    assert calls["n"] == 1
    assert result["stopped"] is True
    output = capsys.readouterr().out
    assert "stopped at global max-cost $1.00" in output
    assert "stopped at max-cost $1000.00" not in output


def test_ev_command_does_not_rewrite_the_pyramid():
    path = ROOT / "pyramids" / "EV.json"
    before = path.stat().st_mtime_ns
    code = _rebuild_main()(["--field", "EV"])
    assert code == 0
    assert path.stat().st_mtime_ns == before


def test_ma_prepare_prices_claude_only_for_rows_already_marked_unsure():
    report = prepare("MA", ROOT)
    assert report["depth_cap"] == 1
    assert report["nodes"] == (
        report["ruled"] + report["filed"] + report["kept_override"]
        + report["routed"] + report["unanchored"] + report["model"]
    )
    assert "msc2020.json" in report["by_map"]
    assert report["hybrid"]["ollama_items"] == report["model"]
    assert report["hybrid"]["escalate_items"] == 0
    assert report["hybrid"]["claude_usd"] == 0
    assert report["hybrid"]["upper_if_all_model_items"] == round(report["model"] * 0.90 / 1000, 6)
    assert report["upper_if_all_tops_escalated"] == round(report["tops"] * 0.90 / 1000, 6)
    assert report["upper_if_cap_not_applied"] == round(report["nodes"] * 0.90 / 1000, 6)
    assert report["tops"] > 0
