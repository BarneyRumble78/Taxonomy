"""Budget split and the all-fields runner. No model and no network."""
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "engine" / "v3"))
from budget import (
    ALLOCATION,
    CLAUDE_IDS,
    GLOBAL_BUDGET,
    MESH,
    PRIORITY,
    RESERVE,
    _scale_caps,
    estimate_escalation,
    load_plan,
    render_markdown,
)
from cost_cap import UNSURE_RATE


def _runner():
    path = ROOT / "scripts" / "run_all_fields.py"
    spec = importlib.util.spec_from_file_location("run_all_fields", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_escalation_rate_is_zero_when_the_rules_place_every_node():
    rate, items, usd = estimate_escalation(0, UNSURE_RATE)
    assert rate == 0
    assert items == 0
    assert usd == 0
    rate, items, usd = estimate_escalation(1000, UNSURE_RATE)
    assert rate == 0.25
    assert items == 250
    assert abs(usd - 0.225) < 1e-9


def test_claude_caps_scale_down_to_the_allocation_in_priority_order():
    entries = [{"id": name, "mode": "claude", "estimate_usd": 20} for name in CLAUDE_IDS]
    entries.append({"id": "AG", "mode": "qwen", "estimate_usd": 40})
    _scale_caps(entries)
    assert sum(entry["cap_cents"] for entry in entries) == 5500
    assert entries[-1]["cap_cents"] == 0
    funded = [entry["cap_cents"] for entry in entries if entry["mode"] == "claude"]
    assert funded[0] >= funded[-1]


def test_saved_plan_keeps_the_split_and_the_mesh_queue():
    plan = load_plan(ROOT)
    assert plan["global_cap"] == GLOBAL_BUDGET == 60
    assert plan["allocation"] == ALLOCATION == 55
    assert plan["reserve"] == RESERVE == 5
    assert abs(plan["assigned"] + plan["headroom"] - 55) < 1e-9
    assert plan["assigned"] <= 55
    ids = [entry["id"] for entry in plan["order"]]
    assert ids[:6] == PRIORITY + [MESH]
    assert len([entry for entry in plan["order"] if entry["kind"] == "field"]) == 24
    assert sum(entry["cap"] for entry in plan["order"]) == plan["assigned"]
    for entry in plan["order"]:
        if entry["mode"] == "qwen":
            assert entry["cap"] == 0
        if entry["model"] == 0:
            assert entry["unsure_rate"] == 0
        if entry["mode"] == "qwen" or entry["id"] == MESH:
            assert entry["estimate_usd"] == 0
        elif entry.get("minto_items"):
            assert entry["estimate_usd"] > 0
            assert entry["cap"] > 0
    mesh = next(entry for entry in plan["order"] if entry["id"] == MESH)
    assert mesh["kind"] == "mesh"
    assert plan["totals"]["focus_resolved"] == mesh["focus_resolved"]
    assert plan["totals"]["focus_cross_conflicts"] == mesh["focus_cross_conflicts"]
    text = render_markdown(plan)
    assert "MESH" in text
    assert "$60" in text
    assert "$55" in text
    assert "25 percent" in text
    assert "loose" in text
    assert f"{mesh['focus_cross_conflicts']:,}" in text
    assert f"{mesh['focus_resolved']:,}" in text
    if plan["assigned"] == 0:
        assert "Their caps are zero" in text
    else:
        assert plan["totals"]["claude_items"] > 0
        assert plan["headroom"] > 0


def test_dry_run_does_not_call_the_queue_and_resume_skips(tmp_path):
    module = _runner()
    plan = {
        "assigned": 1.0,
        "global_cap": 60,
        "reserve": 5,
        "order": [
            {"id": "MA", "mode": "claude", "model": 0, "cap": 0, "estimate_usd": 0, "kind": "field"},
            {"id": "PH", "mode": "claude", "model": 4, "cap": 1, "estimate_usd": 0.01, "kind": "field"},
            {"id": "AG", "mode": "qwen", "model": 8, "cap": 0, "estimate_usd": 0.02, "kind": "field"},
        ],
    }
    calls = []

    def queue_run(entry, root):
        calls.append(entry["id"])
        return {"cost": 0, "wrote": 0, "stopped": False}

    result = module.run_all(tmp_path, plan=plan, execute=False, queue_run=queue_run)
    assert calls == []
    assert [row["result"] for row in result["steps"]] == ["no-model", "dry-run", "dry-run"]
    module.save_state(tmp_path, {"done": ["PH"], "stopped": None})
    again = module.run_all(tmp_path, plan=plan, execute=True, queue_run=queue_run)
    assert calls == ["AG"]
    assert [row["result"] for row in again["steps"]] == ["no-model", "resume", "ran"]
    saved = json.loads(module.state_path(tmp_path).read_text(encoding="utf-8"))
    assert saved["done"] == ["PH", "MA", "AG"]


def test_minto_items_stay_pending_and_do_not_call_a_model(tmp_path):
    module = _runner()
    plan = {
        "assigned": 1.0,
        "global_cap": 60,
        "reserve": 5,
        "order": [
            {"id": "MA", "mode": "claude", "model": 0, "cap": 1, "estimate_usd": 0.2, "kind": "field", "minto_items": 40},
        ],
    }
    calls = []

    def queue_run(entry, root):
        calls.append(entry["id"])
        return {"cost": 1, "wrote": 1, "stopped": False}

    result = module.run_all(tmp_path, plan=plan, execute=True, queue_run=queue_run)
    assert calls == []
    assert result["steps"][0]["result"] == "minto-pending"
    assert not module.state_path(tmp_path).exists()


def test_a_cap_stop_leaves_the_queue_unfinished(tmp_path):
    module = _runner()
    plan = {
        "assigned": 2,
        "global_cap": 60,
        "reserve": 5,
        "order": [
            {"id": "MA", "mode": "claude", "model": 10, "cap": 1, "estimate_usd": 0.1, "kind": "field"},
            {"id": "PH", "mode": "claude", "model": 10, "cap": 1, "estimate_usd": 0.1, "kind": "field"},
        ],
    }

    def queue_run(entry, root):
        return {"cost": 1, "wrote": 1, "stopped": entry["id"] == "MA"}

    result = module.run_all(tmp_path, plan=plan, execute=True, queue_run=queue_run)
    assert result["stopped"] is True
    assert [row["id"] for row in result["steps"]] == ["MA"]
    saved = json.loads(module.state_path(tmp_path).read_text(encoding="utf-8"))
    assert "MA" not in saved["done"]
    assert saved["stopped"] == "MA"
