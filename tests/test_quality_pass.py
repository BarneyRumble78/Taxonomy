"""Quality pass. A fake Anthropic client stands in for the network. No live call."""
import importlib.util
import json
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
import sys
sys.path.insert(0, str(ROOT / "engine" / "v3"))
from group_former import is_fallback_statement, loosely_related, read_log  # noqa: E402


def _script():
    path = ROOT / "scripts" / "quality_pass.py"
    spec = importlib.util.spec_from_file_location("quality_pass_test", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _usage():
    return {"input_tokens": 100, "output_tokens": 40}


def _tool(reply):
    return {"content": [{"type": "tool_use", "name": "record_groups", "input": reply}], "usage": _usage()}


def _leaf(node_id, name):
    return {"id": node_id, "anchor": f"node:{node_id}", "statement": name, "name": name}


def _group(group_id, statement, leaves, further=False):
    point = {
        "id": group_id,
        "anchor": f"group:{group_id}",
        "statement": statement,
        "name": statement,
        "support": {"basis": "kinds", "order": "structure", "rank_note": "", "points": leaves},
    }
    if further:
        point["further"] = True
    return point


def _cell(cell, statement, groups):
    return {
        "id": cell,
        "anchor": f"cell:{cell}",
        "statement": statement,
        "name": statement,
        "support": {"basis": "kinds", "order": "structure", "rank_note": "", "points": groups},
    }


def _write_log(root, field, rows):
    path = root / "pyramids" / "queues" / f"{field}.groups.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")
    return path


def _client(handler):
    def client(payload):
        user = json.loads(payload["messages"][0]["content"])
        return _tool(handler(user))
    return client


def test_a_numbered_heading_is_the_governing_thought():
    module = _script()
    text = "\n".join([
        "## 2. Governing thought",
        "Chemistry is exhausted by four faces of one pyramid.",
        "",
        "## 3. Key line",
        "1. Composition and identity",
        "",
        "## 4. Face O",
    ])
    assert module.pyramid_section(text, "Governing thought") == "Chemistry is exhausted by four faces of one pyramid."
    assert "Composition and identity" in module.pyramid_section(text, "Key line")


def test_fallback_template_and_loose_members():
    assert is_fallback_statement("The group covers rings as one kind of claim.")
    assert is_fallback_statement("The cell gathers the groups under one stated order.")
    assert not is_fallback_statement("Ring theory and field theory are two kinds of algebraic structure.")
    loose = _group(
        "CH.O.A3.G4",
        "Questions about change of state ask how a substance forms a solid.",
        [_leaf("a", "Crystallization"), _leaf("b", "Anisotropy")],
    )
    assert loosely_related(loose)
    close = _group(
        "MA.O.A2.G1",
        "Algebra topics are one kind of structural claim.",
        [_leaf("a", "Algebra one"), _leaf("b", "Algebra two")],
    )
    assert not loosely_related(close)


def test_a_blocked_short_cell_becomes_one_group(tmp_path):
    module = _script()
    nodes = [
        {"id": "MSC:65-XX", "name": "Numerical analysis"},
        {"id": "MSC:68-XX", "name": "Computer science"},
    ]
    module.cell_jobs = lambda field, root: [{
        "field": "MA", "cell": "MA.B.C3", "principle": "Bridges follow the structure.", "nodes": nodes,
    }]
    _write_log(tmp_path, "MA", [
        {"field": "MA", "part": "quality", "kind": "field", "status": "done"},
        {
            "field": "MA", "cell": "MA.B.C3", "part": "cell", "status": "blocked",
            "reason": "fewer than four admitted nodes", "member_ids": ["MSC:65-XX", "MSC:68-XX"],
        },
    ])

    def handler(user):
        if user["task"] == "head":
            return {
                "statement": "Computational bridges gather numerical analysis and computer science as one kind.",
                "basis": "kinds", "order": "structure", "rank_note": "", "groups": [],
            }
        if user["task"] == "sentence":
            return {
                "statement": "Numerical analysis and computer science are the two computational bridges.",
                "basis": "kinds", "order": "structure", "rank_note": "", "groups": [],
            }
        return {
            "statement": "",
            "basis": "kinds",
            "order": "structure",
            "rank_note": "",
            "groups": [
                {
                    "statement": node["name"],
                    "basis": "kinds",
                    "order": "structure",
                    "rank_note": "",
                    "members": [node["id"]],
                }
                for node in user["nodes"]
            ],
        }

    args = module.parse_args(["--field", "MA", "--max-cost", "5", "--global-max-cost", "60"])
    result = module.run(args, anthropic_post=_client(handler), root=tmp_path)
    assert result["stopped"] is False
    assert result["called"] >= 1
    placed = [row for row in read_log(module.log_path(tmp_path, "MA")) if row.get("status") == "placed"]
    assert placed
    groups = placed[-1]["point"]["support"]["points"]
    assert len(groups) == 1
    assert sorted(point["id"] for point in groups[0]["support"]["points"]) == ["MSC:65-XX", "MSC:68-XX"]
    again = module.run(args, anthropic_post=_client(handler), root=tmp_path)
    assert again["called"] == 0


def test_a_fallback_statement_is_rewritten(tmp_path):
    module = _script()
    leaves = [_leaf("a", "Ring theory"), _leaf("b", "Field theory")]
    group = _group("MA.O.A2.G1", "The group covers rings as one kind of claim.", leaves)
    group["review"] = True
    cell = _cell("MA.O.A2", "Structure gathers rings and fields as one kind of algebraic object.", [group])
    nodes = [{"id": "a", "name": "Ring theory"}, {"id": "b", "name": "Field theory"}]
    module.cell_jobs = lambda field, root: [{
        "field": "MA", "cell": "MA.O.A2", "principle": "Structure follows the operations.", "nodes": nodes,
    }]
    _write_log(tmp_path, "MA", [
        {"field": "MA", "part": "quality", "kind": "field", "status": "done"},
        {"field": "MA", "cell": "MA.O.A2", "part": "cell", "status": "placed", "point": cell, "member_ids": ["a", "b"]},
    ])
    seen = []

    def handler(user):
        seen.append(user)
        assert user["task"] == "sentence"
        assert "nodes" not in user
        return {
            "statement": "Ring theory and field theory are two kinds of algebraic structure.",
            "basis": "kinds", "order": "structure", "rank_note": "", "groups": [],
        }

    args = module.parse_args(["--field", "MA", "--max-cost", "5", "--global-max-cost", "60"])
    module.run(args, anthropic_post=_client(handler), root=tmp_path)
    assert len(seen) == 1
    point = [row for row in read_log(module.log_path(tmp_path, "MA")) if row.get("status") == "placed"][-1]["point"]
    rewritten = point["support"]["points"][0]
    assert rewritten["statement"] == "Ring theory and field theory are two kinds of algebraic structure."
    assert "review" not in rewritten


def test_a_further_group_and_an_oversized_group_are_reformed(tmp_path):
    module = _script()
    further = _group(
        "MA.O.A2.G1",
        "further",
        [_leaf(f"r{i}", f"Ring class {i}") for i in range(4)],
        further=True,
    )
    oversized = _group(
        "MA.O.A2.G2",
        "Algebra topics are one kind of structural claim.",
        [_leaf(f"a{i}", f"Algebra topic {i}") for i in range(6)],
    )
    cell = _cell(
        "MA.O.A2",
        "Structure gathers rings and algebra under one stated order.",
        [further, oversized],
    )
    nodes = [{"id": leaf["id"], "name": leaf["name"]} for leaf in further["support"]["points"] + oversized["support"]["points"]]
    module.cell_jobs = lambda field, root: [{
        "field": "MA", "cell": "MA.O.A2", "principle": "Structure follows the operations.", "nodes": nodes,
    }]
    _write_log(tmp_path, "MA", [
        {"field": "MA", "part": "quality", "kind": "field", "status": "done"},
        {"field": "MA", "cell": "MA.O.A2", "part": "cell", "status": "placed", "point": cell},
    ])

    def handler(user):
        if user["task"] == "sentence":
            return {
                "statement": "The named classes are one kind of algebraic structure.",
                "basis": "kinds", "order": "structure", "rank_note": "", "groups": [],
            }
        members = [node["id"] for node in user["nodes"]]
        return {
            "statement": "Algebraic classes divide by the operation they study.",
            "basis": "kinds",
            "order": "structure",
            "rank_note": "",
            "groups": [{
                "statement": "Algebraic classes share one structural operation.",
                "basis": "kinds",
                "order": "structure",
                "rank_note": "",
                "members": members,
            }],
        }

    args = module.parse_args(["--field", "MA", "--max-cost", "5", "--global-max-cost", "60"])
    module.run(args, anthropic_post=_client(handler), root=tmp_path)
    point = [row for row in read_log(module.log_path(tmp_path, "MA")) if row.get("status") == "placed"][-1]["point"]
    groups = point["support"]["points"]
    assert all(group["statement"].strip().lower() != "further" for group in groups)
    flat = []
    for group in groups:
        flat.extend(child["id"] for child in group["support"]["points"])
    assert sorted(flat) == sorted(node["id"] for node in nodes)
    assert all(2 <= len(group["support"]["points"]) <= 5 for group in groups)
    assert "MA.O.A2.G1" not in [group["id"] for group in groups]
    assert "MA.O.A2.G2" not in [group["id"] for group in groups]


def test_loose_members_are_reformed(tmp_path):
    module = _script()
    group = _group(
        "CH.O.A3.G4",
        "Questions about change of state ask how a substance forms a solid.",
        [_leaf("a", "Crystallization"), _leaf("b", "Anisotropy")],
    )
    cell = _cell(
        "CH.O.A3",
        "Equilibrium gathers change of state under one stated order.",
        [group, _group("CH.O.A3.G5", "Solvents dissolve a solute under one stated relation.", [_leaf("c", "Solvent"), _leaf("d", "Solute")])],
    )
    nodes = [
        {"id": "a", "name": "Crystallization"},
        {"id": "b", "name": "Anisotropy"},
        {"id": "c", "name": "Solvent"},
        {"id": "d", "name": "Solute"},
    ]
    module.cell_jobs = lambda field, root: [{
        "field": "CH", "cell": "CH.O.A3", "principle": "Change follows a stated order.", "nodes": nodes,
    }]
    _write_log(tmp_path, "CH", [
        {"field": "CH", "part": "quality", "kind": "field", "status": "done"},
        {"field": "CH", "cell": "CH.O.A3", "part": "cell", "status": "placed", "point": cell},
    ])
    asked = []

    def handler(user):
        asked.append([node["id"] for node in user.get("nodes") or []])
        return {
            "statement": "Crystallization and anisotropy are two kinds of change of state.",
            "basis": "kinds",
            "order": "structure",
            "rank_note": "",
            "groups": [{
                "statement": "Crystallization and anisotropy are two kinds of change of state.",
                "basis": "kinds",
                "order": "structure",
                "rank_note": "",
                "members": [node["id"] for node in user["nodes"]],
            }],
        }

    args = module.parse_args(["--field", "CH", "--max-cost", "5", "--global-max-cost", "60"])
    module.run(args, anthropic_post=_client(handler), root=tmp_path)
    assert ["a", "b"] in asked
    assert ["c", "d"] not in asked
    point = [row for row in read_log(module.log_path(tmp_path, "CH")) if row.get("status") == "placed"][-1]["point"]
    texts = [group["statement"] for group in point["support"]["points"]]
    assert "Crystallization and anisotropy are two kinds of change of state." in texts
    assert any("Solvents dissolve" in text for text in texts)


def test_field_check_stores_the_published_lines_and_does_not_edit_the_pyramid(tmp_path):
    module = _script()
    page = tmp_path / "pyramids" / "MA.md"
    page.parent.mkdir(parents=True)
    page.write_text(
        "\n".join([
            "# MA",
            "",
            "## Governing thought",
            "Mathematics is exhausted by objects and the practices that work them.",
            "",
            "## Key line",
            "1. Objects.",
            "2. Practices.",
            "",
        ]),
        encoding="utf-8",
    )
    before = page.read_bytes()
    group = _group(
        "MA.O.A5.G1",
        "Probability and statistics are two kinds of claim about chance.",
        [_leaf("a", "Probability"), _leaf("b", "Statistics")],
    )
    cell = _cell("MA.O.A5", "Chance gathers probability and statistics under one stated order.", [group])
    # A second group keeps the cell inside the ordinary size rule.
    cell["support"]["points"].append(_group(
        "MA.O.A5.G2",
        "Estimators and tests are two kinds of statistical claim.",
        [_leaf("c", "Estimators"), _leaf("d", "Tests")],
    ))
    module.cell_jobs = lambda field, root: [{
        "field": "MA", "cell": "MA.O.A5", "principle": "Chance follows the measure.",
        "nodes": [{"id": i, "name": i} for i in "abcd"],
    }]
    _write_log(tmp_path, "MA", [
        {"field": "MA", "cell": "MA.O.A5", "part": "cell", "status": "placed", "point": cell},
    ])

    def handler(user):
        assert user["task"] == "field"
        assert "Mathematics is exhausted" in user["governing_thought"]
        return {
            "holds": True,
            "note": "The cells answer the governing thought.",
            "statement": "",
            "basis": "kinds",
            "order": "structure",
            "rank_note": "",
            "groups": [],
        }

    args = module.parse_args(["--field", "MA", "--max-cost", "5", "--global-max-cost", "60"])
    module.run(args, anthropic_post=_client(handler), root=tmp_path)
    assert page.read_bytes() == before
    saved = json.loads((tmp_path / "pyramids" / "queues" / "MA.groups.json").read_text(encoding="utf-8"))
    assert saved["field_check"]["holds"] is True
    assert saved["field_check"]["governing_thought"].startswith("Mathematics is exhausted")
    assert saved["field_check"]["review"] is False


def test_spend_is_added_under_the_lock_without_dropping_another_field(tmp_path):
    module = _script()
    ledger_path = tmp_path / "pyramids" / "queues" / "cost_ledger.json"
    ledger_path.parent.mkdir(parents=True)
    ledger_path.write_text(json.dumps({"spent": 1.0, "fields": {"CH": 1.0}, "note": "keep"}) + "\n", encoding="utf-8")
    group = _group("MA.O.A2.G1", "The group covers rings as one kind of claim.", [_leaf("a", "Ring theory"), _leaf("b", "Field theory")])
    cell = _cell("MA.O.A2", "Structure gathers rings and fields as one kind of algebraic object.", [group])
    module.cell_jobs = lambda field, root: [{
        "field": "MA", "cell": "MA.O.A2", "principle": "Structure follows the operations.",
        "nodes": [{"id": "a", "name": "Ring theory"}, {"id": "b", "name": "Field theory"}],
    }]
    _write_log(tmp_path, "MA", [
        {"field": "MA", "part": "quality", "kind": "field", "status": "done"},
        {"field": "MA", "cell": "MA.O.A2", "part": "cell", "status": "placed", "point": cell},
    ])

    def client(payload):
        module.add_spend(ledger_path, "PH", 0.2)
        user = json.loads(payload["messages"][0]["content"])
        assert user["task"] == "sentence"
        return _tool({
            "statement": "Ring theory and field theory are two kinds of algebraic structure.",
            "basis": "kinds", "order": "structure", "rank_note": "", "groups": [],
        })

    args = module.parse_args(["--field", "MA", "--max-cost", "5", "--global-max-cost", "60"])
    result = module.run(args, anthropic_post=client, root=tmp_path)
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    assert ledger["note"] == "keep"
    assert ledger["fields"]["CH"] == 1.0
    assert ledger["fields"]["PH"] == 0.2
    assert abs(ledger["fields"]["MA"] - result["cost"]) < 1e-9
    assert abs(ledger["spent"] - (1.2 + result["cost"])) < 1e-9


def test_parallel_spend_keeps_every_field(tmp_path):
    module = _script()
    path = tmp_path / "cost_ledger.json"
    path.write_text(json.dumps({"spent": 0, "fields": {}, "note": "keep"}) + "\n", encoding="utf-8")
    errors = []

    def add(index):
        try:
            module.add_spend(path, f"F{index}", 1)
        except Exception as exc:
            errors.append(exc)

    threads = [threading.Thread(target=add, args=(index,)) for index in range(8)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert errors == []
    ledger = json.loads(path.read_text(encoding="utf-8"))
    assert ledger["note"] == "keep"
    assert ledger["spent"] == 8
    assert len(ledger["fields"]) == 8


def test_a_tiny_cap_does_not_call(tmp_path):
    module = _script()
    group = _group("MA.O.A2.G1", "The group covers rings as one kind of claim.", [_leaf("a", "Ring theory"), _leaf("b", "Field theory")])
    cell = _cell("MA.O.A2", "Structure gathers rings and fields as one kind of algebraic object.", [group])
    module.cell_jobs = lambda field, root: [{
        "field": "MA", "cell": "MA.O.A2", "principle": "Structure follows the operations.",
        "nodes": [{"id": "a", "name": "Ring theory"}, {"id": "b", "name": "Field theory"}],
    }]
    _write_log(tmp_path, "MA", [
        {"field": "MA", "part": "quality", "kind": "field", "status": "done"},
        {"field": "MA", "cell": "MA.O.A2", "part": "cell", "status": "placed", "point": cell},
    ])
    calls = []

    def client(payload):
        calls.append(payload)
        raise AssertionError("the cap should stop before the call")

    args = module.parse_args(["--field", "MA", "--max-cost", "0.0001", "--global-max-cost", "60"])
    result = module.run(args, anthropic_post=client, root=tmp_path)
    assert result["stopped"] is True
    assert result["called"] == 0
    assert calls == []


def test_dry_run_and_an_unfinished_field_do_not_call(tmp_path, capsys):
    module = _script()
    module.cell_jobs = lambda field, root: [
        {"field": "MA", "cell": "MA.O.A1", "principle": "Foundations.", "nodes": [{"id": "a", "name": "Logic"}]},
        {"field": "MA", "cell": "MA.O.A2", "principle": "Structure.", "nodes": [{"id": "b", "name": "Groups"}]},
    ]
    _write_log(tmp_path, "MA", [
        {"field": "MA", "cell": "MA.O.A1", "part": "cell", "status": "blocked", "reason": "fewer than four admitted nodes"},
    ])
    calls = []
    args = module.parse_args(["--field", "MA", "--dry-run", "--max-cost", "5"])
    result = module.run(args, anthropic_post=lambda payload: calls.append(payload), root=tmp_path)
    assert result["called"] == 0
    assert result["missing"] == ["MA.O.A2"]
    assert calls == []
    assert "no model was called" in capsys.readouterr().out
