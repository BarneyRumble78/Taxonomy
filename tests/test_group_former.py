"""Group former. A fake model stands in for Ollama and Anthropic. No network."""
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "engine" / "v3"))
import group_former as gf
from group_former import (
    PASS_KEYS,
    SYSTEM,
    assign_members,
    batches,
    cell_jobs,
    form_batch,
    form_cell,
    log_path,
    read_log,
    repair_groups,
    target_groups,
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


def test_an_oversized_group_is_split_to_the_target_count():
    nodes = _nodes(6)
    asked = []

    def ask(task, payload):
        if task == "head":
            return _head()
        if task == "sentence":
            return {"statement": "The group covers the split members as one kind of claim."}
        asked.append(payload)
        return _one([node["id"] for node in payload["nodes"]])

    outcome = form_cell("MA.O.A1", nodes, ask)
    assert outcome["status"] == "placed"
    assert len(asked) == 1
    assert asked[0]["group_count"] == 2
    assert asked[0]["min_groups"] == 2
    sizes = [len(group["support"]["points"]) for group in outcome["point"]["support"]["points"]]
    assert sum(sizes) == 6
    assert all(2 <= size <= 5 for size in sizes)
    _clean(outcome["point"])


def test_target_group_count_is_ceil_of_n_over_4():
    assert target_groups(3) == 1
    assert target_groups(4) == 2
    assert target_groups(6) == 2
    assert target_groups(9) == 3
    assert target_groups(16) == 4
    assert target_groups(17) == 5
    assert target_groups(21) == 5


def test_fewer_than_four_nodes_become_one_group():
    nodes = [
        {"id": "a", "name": "Alpha rite"},
        {"id": "b", "name": "Beta rite"},
        {"id": "c", "name": "Gamma rite"},
    ]
    calls = []

    def ask(task, payload):
        calls.append(task)
        if task == "head":
            return _head()
        if task == "sentence":
            return {"statement": "The group covers the three rites as one kind of claim."}
        assert payload["group_count"] == 1
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
                for node in payload["nodes"]
            ],
        }

    outcome = form_cell("RE.O.A1", nodes, ask)
    assert outcome["status"] == "placed"
    assert "form" in calls
    groups = outcome["point"]["support"]["points"]
    assert len(groups) == 1
    assert sorted(point["id"] for point in groups[0]["support"]["points"]) == ["a", "b", "c"]
    assert is_definition(groups[0]["statement"])


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
    live = ROOT / "pyramids" / "queues" / "cost_ledger.json"
    before_ledger = live.read_bytes() if live.exists() else None
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
    after_ledger = live.read_bytes() if live.exists() else None
    assert after_ledger == before_ledger


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


def test_a_short_cell_is_one_group_and_is_not_asked_again(tmp_path):
    module = _script()
    module.cell_jobs = lambda field, root: [{
        "field": field, "cell": "LA.O.A1", "principle": "Cause precedes effect.", "nodes": _nodes(3),
    }]
    calls = []

    def post(body):
        calls.append(body)
        payload = json.loads(body["messages"][1]["content"])
        if payload["task"] == "head":
            reply = _head()
        elif payload["task"] == "sentence":
            reply = {"statement": "The group covers the three notions as one kind of claim."}
        else:
            reply = {
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
                    for node in payload["nodes"]
                ],
            }
        return {"message": {"content": json.dumps(reply)}}

    args = module.parse_args(["--field", "LA", "--backend", "ollama", "--max-cost", "0"])
    result = module.run(args, post=post, root=tmp_path)
    assert result["wrote"] == 1
    assert result["stopped"] is False
    assert calls
    rows = read_log(log_path(tmp_path, "LA"))
    assert rows[-1]["part"] == "cell"
    assert rows[-1]["status"] == "placed"
    assert len(rows[-1]["point"]["support"]["points"]) == 1
    made = len(calls)
    again = module.run(args, post=post, root=tmp_path)
    assert again["wrote"] == 0
    assert len(calls) == made


def _traditions(count=16):
    families = ["Buddhist", "Christian", "Islamic", "Jewish", "Hindu", "Sikh", "Taoist", "Shinto"]
    nodes = []
    for index in range(count):
        family = families[index % len(families)]
        nodes.append({"id": f"t{index}", "name": f"{family} tradition {index}"})
    return nodes


def _singleton_reply(nodes):
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
            for node in nodes
        ],
    }


def test_missing_ids_join_the_nearest_group_and_unknown_ids_are_dropped():
    nodes = [
        {"id": "c1", "name": "Christian rite"},
        {"id": "c2", "name": "Christian liturgy"},
        {"id": "b1", "name": "Buddhist temple"},
        {"id": "b2", "name": "Buddhist monk"},
    ]
    proposal = {
        "groups": [
            {
                "statement": "Christian churches",
                "basis": "kinds",
                "order": "structure",
                "rank_note": "",
                "members": ["c1", "not-a-real-id"],
            },
            {
                "statement": "Buddhist temples",
                "basis": "kinds",
                "order": "structure",
                "rank_note": "",
                "members": ["b1", "b2"],
            },
        ]
    }
    assigned = assign_members(nodes, proposal)
    flat = [member for group in assigned for member in group["members"]]
    assert "not-a-real-id" not in flat
    assert sorted(flat) == ["b1", "b2", "c1", "c2"]
    christian = next(group for group in assigned if "c1" in group["members"])
    assert "c2" in christian["members"]
    assert "b1" not in christian["members"]


def test_a_name_with_no_overlap_joins_the_further_group():
    nodes = [
        {"id": "c1", "name": "Christian rite"},
        {"id": "b1", "name": "Buddhist temple"},
        {"id": "q1", "name": "Quantum platypus"},
    ]
    proposal = {
        "groups": [
            {
                "statement": "Christian churches",
                "basis": "kinds",
                "order": "structure",
                "rank_note": "",
                "members": ["c1"],
            },
            {
                "statement": "Buddhist temples",
                "basis": "kinds",
                "order": "structure",
                "rank_note": "",
                "members": ["b1"],
            },
        ]
    }
    assigned = assign_members(nodes, proposal)
    further = next(group for group in assigned if group.get("further"))
    assert further["members"] == ["q1"]


def test_fifteen_singletons_for_sixteen_traditions_stay_inside_two_to_five():
    nodes = _traditions(16)
    dropped = nodes[-1]
    proposal = _singleton_reply(nodes[:-1])
    assigned = assign_members(nodes, proposal)
    home = next(group for group in assigned if dropped["id"] in group["members"])
    shinto = [node["id"] for node in nodes if node["name"].startswith("Shinto") and node["id"] != dropped["id"]]
    assert any(member in shinto for member in home["members"])
    packed = repair_groups(nodes, proposal)
    assert packed is not None
    sizes = [len(group["members"]) for group in packed]
    assert all(2 <= size <= 5 for size in sizes)
    assert 2 <= len(packed) <= 5
    assert len(packed) == target_groups(16)
    seen = [member for group in packed for member in group["members"]]
    assert sorted(seen) == sorted(node["id"] for node in nodes)
    calls = []

    def ask(task, payload):
        calls.append((task, payload.get("group_count")))
        if task == "head":
            return _head()
        if task == "sentence":
            assert "nodes" not in payload
            assert payload["members"]
            return {"statement": "The group covers these traditions as one kind of claim."}
        assert payload["group_count"] == 4
        return proposal

    outcome = form_cell("RE.O.A4", nodes, ask)
    assert outcome["status"] == "placed"
    assert calls[0] == ("form", 4)
    _clean(outcome["point"])
    leaves = [
        point["id"]
        for group in outcome["point"]["support"]["points"]
        for point in group["support"]["points"]
    ]
    assert sorted(leaves) == sorted(node["id"] for node in nodes)


def test_a_bare_label_asks_for_one_sentence_then_uses_a_flagged_template():
    nodes = _nodes(4)
    ids = [node["id"] for node in nodes]
    calls = []

    def ask(task, payload):
        calls.append(task)
        if task == "head":
            return _head()
        if task == "sentence":
            assert "nodes" not in payload
            if payload["label"] == "Abrahamic":
                return {"statement": "The group covers Abrahamic rites as one kind of claim."}
            return {"statement": "Dharmic"}
        return {
            "statement": "",
            "basis": "kinds",
            "order": "structure",
            "rank_note": "",
            "groups": [
                {
                    "statement": "Abrahamic",
                    "basis": "kinds",
                    "order": "structure",
                    "rank_note": "",
                    "members": ids[:2],
                },
                {
                    "statement": "Dharmic",
                    "basis": "kinds",
                    "order": "structure",
                    "rank_note": "",
                    "members": ids[2:],
                },
            ],
        }

    outcome = form_cell("RE.O.A1", nodes, ask)
    assert outcome["status"] == "placed"
    assert calls.count("sentence") == 2
    points = outcome["point"]["support"]["points"]
    by_members = {tuple(point["id"] for point in group["support"]["points"]): group for group in points}
    abrahamic = by_members[("n0", "n1")]
    dharmic = by_members[("n2", "n3")]
    assert abrahamic["statement"] == "The group covers Abrahamic rites as one kind of claim."
    assert "review" not in abrahamic
    assert dharmic["statement"] == "The group covers Dharmic as one kind of claim."
    assert dharmic["review"] is True
    assert is_definition(dharmic["statement"])
    assert outcome["statement_review"] == [dharmic["id"]]


def test_split_keeps_the_passing_half(monkeypatch):
    real = gf.repair_groups

    def wrapped(nodes, proposal):
        ids = [node["id"] for node in nodes]
        if len(ids) == 6 or ids == ["n3", "n4", "n5"]:
            return None
        return real(nodes, proposal)

    monkeypatch.setattr(gf, "repair_groups", wrapped)
    nodes = _nodes(6)
    asked = []

    def ask(task, payload):
        if task == "sentence":
            return {"statement": "The group covers the named members as one kind of claim."}
        asked.append([node["id"] for node in payload["nodes"]])
        return _one([node["id"] for node in payload["nodes"]])

    ident = iter(f"RE.O.A1.G{index}" for index in range(1, 100))
    result = form_batch(nodes, ask, ident)
    assert result["status"] == "placed"
    assert result["review_ids"] == ["n3", "n4", "n5"]
    placed = [member for group in result["groups"] for member in group["members"]]
    assert placed == ["n0", "n1", "n2"]
    assert ["n0", "n1", "n2"] in asked
    assert ["n3", "n4", "n5"] in asked


def test_a_blocked_line_does_not_finish_a_short_cell():
    rows = [{
        "part": "cell",
        "cell": "MA.B.C3",
        "status": "blocked",
        "reason": "fewer than four admitted nodes",
        "member_ids": ["MSC:65-XX", "MSC:68-XX"],
    }]
    assert "MA.B.C3" not in gf.finished_cells(rows)
    rows.append({"part": "cell", "cell": "MA.B.C3", "status": "placed", "point": {"id": "MA.B.C3"}})
    assert gf.finished_cells(rows)["MA.B.C3"]["status"] == "placed"


def test_write_result_keeps_the_later_placed_point(tmp_path):
    rows = [
        {"part": "cell", "cell": "MA.B.C3", "status": "blocked"},
        {
            "part": "cell",
            "cell": "MA.B.C3",
            "status": "placed",
            "point": {"id": "MA.B.C3", "statement": "One group holds the two classes as one kind of claim."},
        },
        {"part": "cell", "cell": "MA.O.A2", "status": "placed", "point": {"id": "MA.O.A2", "statement": "First."}},
        {"part": "cell", "cell": "MA.O.A2", "status": "placed", "point": {"id": "MA.O.A2", "statement": "Second."}},
        {"part": "field", "check": {"holds": True, "note": "The cells answer the governing thought."}},
    ]
    payload = gf.write_result(tmp_path, "MA", rows)
    assert [cell["id"] for cell in payload["cells"]] == ["MA.B.C3", "MA.O.A2"]
    assert payload["cells"][1]["statement"] == "Second."
    assert payload["field_check"]["holds"] is True


def test_a_blocked_short_cell_is_placed_on_the_next_run(tmp_path):
    module = _script()
    nodes = [
        {"id": "MSC:65-XX", "name": "Numerical analysis"},
        {"id": "MSC:68-XX", "name": "Computer science"},
    ]
    module.cell_jobs = lambda field, root: [{
        "field": field,
        "cell": "MA.B.C3",
        "principle": "Bridges follow the structure.",
        "nodes": nodes,
    }]
    path = log_path(tmp_path, "MA")
    gf.append_log(path, {
        "field": "MA",
        "cell": "MA.B.C3",
        "part": "cell",
        "status": "blocked",
        "reason": "fewer than four admitted nodes",
        "member_ids": ["MSC:65-XX", "MSC:68-XX"],
    })
    calls = []

    def post(body):
        calls.append(json.loads(body["messages"][1]["content"]))
        payload = calls[-1]
        if payload["task"] == "head":
            reply = _head()
        elif payload["task"] == "sentence":
            reply = {"statement": "Numerical analysis and computer science are the two computational bridges."}
        else:
            reply = {
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
                    for node in payload["nodes"]
                ],
            }
        return {"message": {"content": json.dumps(reply)}}

    args = module.parse_args(["--field", "MA", "--backend", "ollama", "--max-cost", "0"])
    result = module.run(args, post=post, root=tmp_path)
    assert result["wrote"] == 1
    assert calls
    rows = read_log(path)
    assert rows[-1]["status"] == "placed"
    groups = rows[-1]["point"]["support"]["points"]
    assert len(groups) == 1
    assert sorted(point["id"] for point in groups[0]["support"]["points"]) == ["MSC:65-XX", "MSC:68-XX"]
    made = len(calls)
    again = module.run(args, post=post, root=tmp_path)
    assert again["wrote"] == 0
    assert len(calls) == made


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
