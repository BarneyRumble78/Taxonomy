"""Group former. A fake model stands in for Ollama and Anthropic. No network."""
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "engine" / "v3"))
from group_former import (
    PASS_KEYS,
    SYSTEM,
    batches,
    cell_jobs,
    form_cell,
    log_path,
    read_log,
)
from minto_check import is_definition, minto_counts

SENT = "The group covers alpha and beta as one kind of claim."
HEAD = "The cell gathers both groups under one stated order."


def _nodes(count, prefix="n"):
    return [{"id": f"{prefix}{index}", "name": f"Notion {prefix}{index}"} for index in range(count)]


def _group(members, label="alpha"):
    return {
        "statement": f"The group covers {label} as one kind of claim.",
        "basis": "kinds",
        "order": "structure",
        "rank_note": "",
        "members": list(members),
    }


def _head():
    return {
        "statement": HEAD,
        "basis": "kinds",
        "order": "structure",
        "rank_note": "",
        "groups": [],
    }


def _pair(members):
    """Two groups. A cell of four or five admits nothing smaller."""
    mid = max(2, len(members) // 2)
    if len(members) - mid < 2:
        mid = len(members) - 2
    return {
        "statement": HEAD,
        "basis": "kinds",
        "order": "structure",
        "rank_note": "",
        "groups": [_group(members[:mid], "the first pair"), _group(members[mid:], "the second pair")],
    }


def _one(members):
    return {
        "statement": HEAD,
        "basis": "kinds",
        "order": "structure",
        "rank_note": "",
        "groups": [_group(members, "the whole batch")],
    }


def _clean(point):
    counts = minto_counts({"key_line": point["support"]})
    for key in PASS_KEYS:
        assert counts[key] == 0, counts
    assert is_definition(point["statement"])
    assert is_definition(SENT)


def _script():
    path = ROOT / "scripts" / "run_group_former.py"
    spec = importlib.util.spec_from_file_location("run_group_former_test", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_batches_keep_a_leftover_with_the_previous_chunk():
    assert [len(chunk) for chunk in batches(range(3), 2)] == [3]
    assert [len(chunk) for chunk in batches(range(5), 2)] == [2, 3]
    assert [len(chunk) for chunk in batches(range(21), 20)] == [21]
    assert [len(chunk) for chunk in batches(range(22), 20)] == [20, 2]
    assert [len(chunk) for chunk in batches(range(40), 20)] == [20, 20]
    assert [len(chunk) for chunk in batches(range(41), 20)] == [20, 21]
    assert all(len(chunk) >= 2 for chunk in batches(range(41), 20))


def test_a_valid_proposal_passes_the_checker():
    nodes = _nodes(6)
    calls = []

    def ask(task, payload):
        calls.append(task)
        if task == "head":
            return _head()
        return _pair([node["id"] for node in payload["nodes"]])

    outcome = form_cell("MA.O.A1", nodes, ask)
    assert outcome["status"] == "placed"
    assert calls == ["form", "head"]
    _clean(outcome["point"])
    assert outcome["point"]["anchor"] == "cell:MA.O.A1"
    leaves = []
    for group in outcome["point"]["support"]["points"]:
        assert group["anchor"].startswith("group:")
        assert 2 <= len(group["support"]["points"]) <= 5
        leaves.extend(point["id"] for point in group["support"]["points"])
    assert leaves == [node["id"] for node in nodes]


def test_four_nodes_ask_for_two_groups():
    nodes = _nodes(4)
    seen = []

    def ask(task, payload):
        if task == "head":
            return _head()
        seen.append(payload["min_groups"])
        return _pair([node["id"] for node in payload["nodes"]])

    outcome = form_cell("MA.O.A1", nodes, ask)
    assert seen == [2]
    assert outcome["status"] == "placed"
    _clean(outcome["point"])


def test_an_oversized_group_is_retried_and_then_split():
    nodes = _nodes(6)
    asked = []

    def ask(task, payload):
        if task == "head":
            return _head()
        ids = [node["id"] for node in payload["nodes"]]
        asked.append((ids, list(payload["problems"]), payload["min_groups"]))
        if len(ids) == 6:
            return _one(ids)
        return _one(ids)

    outcome = form_cell("MA.O.A1", nodes, ask)
    assert outcome["status"] == "placed"
    assert asked[0][0] == [node["id"] for node in nodes]
    assert asked[0][1] == []
    assert asked[1][0] == asked[0][0]
    assert any("6 members" in item for item in asked[1][1])
    assert asked[2][0] == ["n0", "n1", "n2"]
    assert asked[3][0] == ["n3", "n4", "n5"]
    assert asked[2][2] == 1
    _clean(outcome["point"])


def test_fewer_than_four_nodes_does_not_ask():
    calls = []
    outcome = form_cell("MA.O.A1", _nodes(3), lambda task, payload: calls.append(task))
    assert outcome["status"] == "blocked"
    assert outcome["reason"] == "fewer than four admitted nodes"
    assert calls == []


def test_a_resumed_cell_keeps_placed_ids_and_does_not_reuse_them():
    nodes = _nodes(4)
    seed = [{
        "id": "MA.O.A1.G1",
        "statement": SENT,
        "basis": "kinds",
        "order": "structure",
        "rank_note": "",
        "members": ["n0", "n1"],
    }]
    asked = []

    def ask(task, payload):
        asked.append((task, [node["id"] for node in payload.get("nodes") or []]))
        if task == "head":
            return _head()
        return _one([node["id"] for node in payload["nodes"]])

    pending = nodes[2:]
    outcome = form_cell(
        "MA.O.A1", pending, ask, seed_groups=seed, known=nodes,
    )
    assert outcome["status"] == "placed"
    assert asked[0] == ("form", ["n2", "n3"])
    assert asked[1][0] == "head"
    ids = [point["id"] for point in outcome["point"]["support"]["points"]]
    assert ids == ["MA.O.A1.G1", "MA.O.A1.G2"]
    leaves = {
        point["id"]: point["statement"]
        for group in outcome["point"]["support"]["points"]
        for point in group["support"]["points"]
    }
    assert leaves["n0"] == "Notion n0"
    assert leaves["n2"] == "Notion n2"


def test_the_system_prefix_does_not_carry_the_cell():
    assert "MA.O" not in SYSTEM
    assert "Notion" not in SYSTEM
    again = SYSTEM
    assert again == SYSTEM


def test_ma_admitted_nodes_are_the_catalogue_count():
    jobs = cell_jobs("MA", ROOT)
    assert sum(len(job["nodes"]) for job in jobs) == 71
    assert all(job["nodes"] for job in jobs)


def test_dry_run_does_not_call_the_model(capsys):
    module = _script()

    def post(body):
        raise AssertionError("dry-run called the model")

    args = module.parse_args(["--field", "MA", "--backend", "ollama", "--dry-run"])
    result = module.run(args, post=post, root=ROOT)
    assert result["stopped"] is False
    assert result["cost"] == 0.0
    assert result["system"] == SYSTEM
    assert result["cells"] > 0
    output = capsys.readouterr().out
    assert "system prefix cached" in output
    assert "backend=ollama" in output
    assert "dry-run field=MA" in output


def test_ollama_body_turns_thinking_off_and_a_second_run_skips_the_cell(tmp_path):
    module = _script()
    nodes = _nodes(4)
    module.cell_jobs = lambda field, root: [{
        "field": field, "cell": "MA.O.A1", "principle": "Parts follow the structure.", "nodes": nodes,
    }]
    bodies = []

    def post(body):
        bodies.append(body)
        payload = json.loads(body["messages"][1]["content"])
        if payload["task"] == "head":
            reply = _head()
        else:
            reply = _pair([node["id"] for node in payload["nodes"]])
        return {"message": {"content": json.dumps(reply)}}

    args = module.parse_args([
        "--field", "MA", "--backend", "ollama", "--model", "qwen3:30b-a3b", "--max-cost", "0",
        "--global-max-cost", "60",
    ])
    result = module.run(args, post=post, root=tmp_path)
    assert result["stopped"] is False
    assert result["wrote"] == 1
    assert len(bodies) == 2
    for body in bodies:
        assert body["think"] is False
        assert body["stream"] is False
        assert body["format"]["properties"]["groups"]["type"] == "array"
        assert body["options"]["temperature"] == 0
        assert body["model"] == "qwen3:30b-a3b"
        assert body["messages"][0]["content"] == SYSTEM
    users = [json.loads(body["messages"][1]["content"]) for body in bodies]
    assert users[0]["task"] == "form"
    assert users[0]["cell"] == "MA.O.A1"
    assert "principle" in users[0]
    assert "Notion n0" in users[0]["nodes"][0]["name"]
    assert users[1]["task"] == "head"
    assert bodies[0]["messages"][0]["content"] == bodies[1]["messages"][0]["content"]
    rows = read_log(log_path(tmp_path, "MA"))
    assert [row["part"] for row in rows] == ["batch", "cell"]
    assert rows[-1]["status"] == "placed"
    again = module.run(args, post=post, root=tmp_path)
    assert again["wrote"] == 0
    assert len(bodies) == 2


def test_anthropic_caches_the_prefix_and_records_the_cost(tmp_path):
    module = _script()
    nodes = _nodes(4)
    module.cell_jobs = lambda field, root: [{
        "field": field, "cell": "PH.O.A1", "principle": "Kinds follow the structure.", "nodes": nodes,
    }]
    seen = []

    def client(payload):
        seen.append(payload)
        user = json.loads(payload["messages"][0]["content"])
        if user["task"] == "head":
            reply = _head()
        else:
            reply = _pair([node["id"] for node in user["nodes"]])
        return {
            "content": [{"type": "tool_use", "name": "record_groups", "input": reply}],
            "usage": {
                "input_tokens": 100,
                "output_tokens": 40,
                "cache_read_input_tokens": 80,
                "cache_creation_input_tokens": 10,
            },
        }

    args = module.parse_args([
        "--field", "PH", "--backend", "anthropic", "--max-cost", "5.57", "--global-max-cost", "60",
    ])
    result = module.run(args, anthropic_post=client, root=tmp_path)
    assert len(seen) == 2
    assert result["stopped"] is False
    per_call = module.queue.list_usd(
        "claude-sonnet-5-5", input_tokens=100, output_tokens=40, cache_read=80, cache_write=10,
    )
    assert abs(result["cost"] - 2 * per_call) < 1e-9
    for payload in seen:
        assert payload["model"] == "claude-sonnet-5-5"
        assert payload["system"][0]["text"] == SYSTEM
        assert payload["system"][0]["cache_control"] == {"type": "ephemeral"}
        tool = payload["tools"][0]
        assert tool["name"] == "record_groups"
        assert tool["cache_control"] == {"type": "ephemeral"}
        assert tool["strict"] is True
        assert "temperature" not in payload
    assert seen[0]["system"][0]["text"] == seen[1]["system"][0]["text"]
    assert "Notion" not in seen[0]["system"][0]["text"]
    ledger = json.loads((tmp_path / "pyramids" / "queues" / "cost_ledger.json").read_text(encoding="utf-8"))
    assert ledger["fields"]["PH"] == result["cost"]
    assert not (ROOT / "pyramids" / "queues" / "cost_ledger.json").exists()


def test_max_cost_stops_before_the_cell_line_and_resume_skips_the_batch(tmp_path):
    module = _script()
    nodes = _nodes(4)
    module.cell_jobs = lambda field, root: [{
        "field": field, "cell": "CS.O.A1", "principle": "Kinds follow the structure.", "nodes": nodes,
    }]
    calls = []

    def client(payload):
        calls.append(json.loads(payload["messages"][0]["content"]))
        user = calls[-1]
        reply = _pair([node["id"] for node in user["nodes"]]) if user["task"] == "form" else _head()
        return {
            "content": [{"type": "tool_use", "name": "record_groups", "input": reply}],
            "usage": {"input_tokens": 100, "output_tokens": 2500},
        }

    args = module.parse_args([
        "--field", "CS", "--backend", "anthropic", "--max-cost", "0.05", "--global-max-cost", "60",
    ])
    result = module.run(args, anthropic_post=client, root=tmp_path)
    assert result["stopped"] is True
    assert len(calls) == 1
    assert calls[0]["task"] == "form"
    rows = read_log(log_path(tmp_path, "CS"))
    assert [row["part"] for row in rows] == ["batch"]
    assert rows[0]["status"] == "placed"
    assert "n0" in rows[0]["member_ids"]

    def later(payload):
        calls.append(json.loads(payload["messages"][0]["content"]))
        return {
            "content": [{"type": "tool_use", "name": "record_groups", "input": _head()}],
            "usage": {"input_tokens": 10, "output_tokens": 10},
        }

    resume = module.parse_args([
        "--field", "CS", "--backend", "anthropic", "--max-cost", "10", "--global-max-cost", "60",
    ])
    second = module.run(resume, anthropic_post=later, root=tmp_path)
    assert second["stopped"] is False
    assert calls[1]["task"] == "head"
    assert "nodes" not in calls[1]
    finished = read_log(log_path(tmp_path, "CS"))
    assert finished[-1]["part"] == "cell"
    assert finished[-1]["status"] == "placed"
    group_ids = [point["id"] for point in finished[-1]["point"]["support"]["points"]]
    assert group_ids == ["CS.O.A1.G1", "CS.O.A1.G2"]


def test_a_blocked_cell_is_finished_and_not_asked_again(tmp_path):
    module = _script()
    module.cell_jobs = lambda field, root: [{
        "field": field, "cell": "LA.O.A1", "principle": "Cause precedes effect.", "nodes": _nodes(3),
    }]

    def post(body):
        raise AssertionError("a short cell does not call the model")

    args = module.parse_args(["--field", "LA", "--backend", "ollama", "--max-cost", "0"])
    result = module.run(args, post=post, root=tmp_path)
    assert result["wrote"] == 1
    assert result["stopped"] is False
    rows = read_log(log_path(tmp_path, "LA"))
    assert rows[0]["part"] == "cell"
    assert rows[0]["status"] == "blocked"
    again = module.run(args, post=post, root=tmp_path)
    assert again["wrote"] == 0
    assert len(read_log(log_path(tmp_path, "LA"))) == 1


def test_a_tiny_cap_does_not_call_and_writes_no_cell_line(tmp_path):
    module = _script()
    module.cell_jobs = lambda field, root: [{
        "field": field, "cell": "MD.O.A1", "principle": "Cause precedes effect.", "nodes": _nodes(4),
    }]
    calls = []

    def client(payload):
        calls.append(payload)
        raise AssertionError("the cap should stop before the call")

    args = module.parse_args([
        "--field", "MD", "--backend", "anthropic", "--max-cost", "0.0001", "--global-max-cost", "60",
    ])
    result = module.run(args, anthropic_post=client, root=tmp_path)
    assert result["stopped"] is True
    assert calls == []
    assert read_log(log_path(tmp_path, "MD")) == []
    assert not (tmp_path / "pyramids" / "queues" / "cost_ledger.json").exists()
