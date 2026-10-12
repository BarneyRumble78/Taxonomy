"""Section 12 checks for a built pyramid, plus the dedupe and queue-request units.

The EV file is the pilot. These checks do not call a model and do not embed.
"""
import importlib.util
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "engine" / "v3"))
from pyramid import IdBook, _walk_points, dedupe_nodes, dpsir_role, is_filler, kind_of, pack_concepts, summarise_names

WORD = re.compile(r"[A-Za-z0-9]+(?:[-–][A-Za-z0-9]+)?")
ORDERS = {"time", "structure", "degree"}
QUESTIONS = {"why", "how", "so_what", "which_ones"}
VERBS = re.compile(r"\b(is|are|places|holds|covers|follows|aims)\b")
ID_RE = re.compile(r"^EV\.P(\.\d+)+$")


def _load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def _queue_module():
    path = ROOT / "scripts" / "run_pyramid_queue.py"
    spec = importlib.util.spec_from_file_location("run_pyramid_queue", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _groups(pyramid):
    yield pyramid["key_line"]
    stack = list(pyramid["key_line"]["points"])
    while stack:
        point = stack.pop()
        support = point.get("support")
        if support:
            yield support
            stack.extend(support.get("points") or [])


def test_dedupe_keeps_the_primary_scheme():
    nodes = [
        {
            "id": "ANZ:1", "name": "Nitrate", "taxonomy_cell": "EV.O.A1", "parent": None,
            "_file": "maps/EV/anzsrc2020.json", "_scheme": "ANZSRC", "_primary": False,
        },
        {
            "id": "GEMET:9", "name": "nitrate", "taxonomy_cell": "EV.O.A2", "parent": "GEMET:1",
            "_file": "maps/EV/gemet.json", "_scheme": "GEMET", "_primary": True,
        },
    ]
    merged = dedupe_nodes(nodes)
    assert len(merged) == 1
    assert merged[0]["id"] == "GEMET:9"
    assert merged[0]["name"] == "nitrate"
    assert merged[0]["cell"] == "EV.O.A2"
    assert {src["id"] for src in merged[0]["sources"]} == {"ANZ:1", "GEMET:9"}


def test_retired_id_is_not_reused():
    previous = {
        "retired": [],
        "key_line": {"points": [{"id": "EV.P.1", "anchor": "cell:EV.O.A1", "statement": "Pressures are loads."}]},
    }
    book = IdBook("EV", previous)
    retired = book.finish()
    assert retired[0]["id"] == "EV.P.1"
    assert retired[0]["status"] == "RETIRED"
    again = IdBook("EV", {"retired": retired, "key_line": {"points": []}})
    assert again.get("EV.P", "cell:EV.O.A2") != "EV.P.1"


def test_pack_keeps_a_wide_facet():
    book = IdBook("EV", None)
    by_id = {}
    children = defaultdict(list)
    placed = {}

    def add(number, parent=None):
        cid = f"N{number}"
        by_id[cid] = {
            "id": cid,
            "name": f"Concept {number}",
            "cell": "EV.O.A1",
            "parent": parent,
            "sources": [{"scheme": "GEMET", "id": cid, "code": str(number), "file": "maps/EV/gemet.json"}],
        }
        placed[cid] = {"facet": "emissions", "method": "rule"}
        if parent:
            children[parent].append(cid)

    add(0)
    for number in range(1, 8):
        add(number, "N0")
    packed = pack_concepts(placed, by_id, children, "emissions", book, "EV.P.1.1", "pressure", {})
    assert 2 <= len(packed["points"]) <= 5
    assert packed["queued"] == []
    node_ids = {point["anchor"][5:] for point in _walk_points(packed["points"]) if point["anchor"].startswith("node:")}
    assert node_ids | set(packed["collapsed"]) == set(by_id)
    for point in _walk_points(packed["points"]):
        assert len(WORD.findall(point["statement"])) <= 25
        assert point["statement"].count(".") == 1


def _pressure_item(name, group_id, statement):
    return {
        "node_id": name,
        "name": name,
        "cell": "EV.O.A1",
        "candidates": [{"cell": "EV.O.A1", "group_id": group_id, "statement": statement}],
    }


def test_queue_request_disables_thinking():
    module = _queue_module()
    catalog = [
        {"group_id": "EV.P.1", "statement": "Pressures are loads."},
        {"group_id": "EV.P.2", "statement": "States are conditions."},
    ]
    body = module.request_body({
        "node_id": "GEMET:1",
        "name": "acid rain",
        "cell": "EV.O.A1",
        "reason": "embedding gap 0.0010 is below 0.0200",
        "candidates": [
            {"facet": "emissions", "group_id": "EV.P.1.1", "statement": "Emissions are loads."},
            {"facet": "land", "group_id": "EV.P.1.2", "statement": "Land use is a load."},
        ],
    }, catalog=catalog)
    assert body["model"] == "qwen3:30b-a3b"
    assert body["stream"] is False
    assert body["think"] is False
    assert body["format"] is module.PLACE_SCHEMA
    assert body["options"] == {"temperature": 0, "num_predict": 3000}
    assert "response_format" not in body
    schema = body["format"]
    assert "items" in schema["properties"]
    item_schema = schema["properties"]["items"]["items"]
    assert "group_id" in item_schema["properties"]
    assert "reason" in item_schema["required"]
    payload = json.loads(body["messages"][1]["content"])
    assert payload["items"][0]["choices"] == ["EV.P.1", "EV.P.2", "EV.P.1.1", "EV.P.1.2", "unsure", "out_of_scope"]
    assert body["messages"][0]["content"] == module.SYSTEM_PLACE
    assert "Do not force a fit." in module.SYSTEM_PLACE
    assert module.chat_url("http://localhost:11434").endswith("/api/chat")
    other = module.request_batch([{
        "node_id": "GEMET:2",
        "name": "restoration",
        "cell": "EV.O.A4",
        "candidates": [{"cell": "EV.O.A4", "group_id": "EV.P.4", "statement": "Responses are actions."}],
    }], catalog=catalog)
    assert other["messages"][0]["content"] == body["messages"][0]["content"]
    assert other["format"] == body["format"]
    assert module.message_content({"message": {"content": "{\"items\":[]}"}}) == "{\"items\":[]}"
    assert module.message_content({"choices": [{"message": {"content": "abc"}}]}) == "abc"
    unsure = module.request_body(
        {"node_id": "X", "name": "x", "cell": "EV.O.A1", "candidates": []},
        catalog=catalog,
    )
    assert unsure["think"] is False
    assert json.loads(unsure["messages"][1]["content"])["items"][0]["choices"] == [
        "EV.P.1", "EV.P.2", "unsure", "out_of_scope",
    ]


def test_openai_path_is_optional():
    module = _queue_module()
    item = _pressure_item("acid rain", "EV.P.1.1", "Emissions are loads.")
    body = module.request_batch([item], api="openai", catalog=[])
    assert body["think"] is False
    assert body["temperature"] == 0
    schema = body["response_format"]["json_schema"]["schema"]
    assert schema is module.PLACE_SCHEMA
    assert "format" not in body
    assert module.chat_url("http://localhost:11434", "openai").endswith("/v1/chat/completions")
    assert module.parse_args(["--field", "EV", "--api", "openai"]).api == "openai"
    assert module.parse_args(["--field", "EV", "--api", "native"]).api == "native"


def test_ev_section_12():
    pyramid = _load(ROOT / "pyramids" / "EV.json")
    queue = _load(ROOT / "pyramids" / "queues" / "EV.json")
    markdown = (ROOT / "pyramids" / "EV_minto.md").read_text(encoding="utf-8")
    lens = _load(ROOT / "cards" / "lens" / "EV.json")
    build = pyramid["build"]
    assert build["after_dedupe"] == build["placed_by_rules"] + build["placed_by_embeddings"] + build["queued"]
    assert build["placed"] == build["placed_by_rules"] + build["placed_by_embeddings"]

    thought = pyramid["governing_thought"]
    assert thought.endswith(".") and thought.count(".") == 1
    assert len(WORD.findall(thought)) <= 25
    intro = pyramid["introduction"]
    for key in ("situation", "complication", "question"):
        sentence = intro[key]
        assert sentence.endswith(".") or sentence.endswith("?")
        assert sentence.count(".") + sentence.count("?") == 1
        assert len(WORD.findall(sentence)) <= 25
    assert thought in markdown
    assert "**Situation.**" in markdown
    assert "**Complication.**" in markdown
    assert "**Question.**" in markdown
    assert "Chapter 8" in markdown

    key = pyramid["key_line"]
    assert key["logic_type"] == "inductive"
    assert key["order"] == "time"
    assert 2 <= len(key["points"]) <= 5
    expected = sorted(
        (card["id"] for card in lens if re.fullmatch(r"EV\.O\.A\d+", card["id"])),
        key=lambda item: int(item.rsplit("A", 1)[1]),
    )
    assert [point["cell"] for point in key["points"]] == expected
    state = next(point for point in key["points"] if point["id"] == "EV.P.2")
    assert [point["id"] for point in state["support"]["points"]] == [
        "EV.P.2.7", "EV.P.2.6", "EV.P.2.8", "EV.P.2.9", "EV.P.2.10",
    ]
    assert state["support"]["mece_dimension"] == (
        "whether the state is a medium, a hazard, a concept, a resource, or an earth science"
    )
    media, natural, concepts, resources, earth = state["support"]["points"]
    assert concepts["id"] == "EV.P.2.8"
    assert resources["id"] == "EV.P.2.9"
    assert earth["id"] == "EV.P.2.10"
    responses = next(point for point in key["points"] if point["id"] == "EV.P.4")
    assert [point["id"] for point in responses["support"]["points"]] == [
        "EV.P.4.1", "EV.P.4.2", "EV.P.4.3", "EV.P.4.7",
    ]
    assert [point["id"] for point in media["support"]["points"]] == [
        "EV.P.2.1", "EV.P.2.2", "EV.P.2.3", "EV.P.2.4", "EV.P.2.5",
    ]
    assert [point["id"] for point in natural["support"]["points"]] == [
        "EV.P.2.6.1", "EV.P.2.6.2", "EV.P.2.6.3",
    ]
    assert "Natural hazards and processes are geological, weather, and ecological events." in markdown

    ids = []
    catalogs = {}

    def source_ok(src):
        file_ids = catalogs.get(src["file"])
        if file_ids is None:
            data = _load(ROOT / src["file"])
            file_ids = {node["id"] for node in data["nodes"]}
            catalogs[src["file"]] = file_ids
        assert src["id"] in file_ids

    for group in _groups(pyramid):
        points = group["points"]
        assert 2 <= len(points) <= 5, group.get("mece_dimension")
        assert group["logic_type"] in ("inductive", "deductive")
        assert group["order"] in ORDERS
        assert group["question_raised"] in QUESTIONS
        if group["logic_type"] == "inductive":
            assert group.get("plural_noun")
            assert group.get("mece_dimension")
        else:
            assert len(points) == 3
        for point in points:
            ids.append(point["id"])
            assert ID_RE.match(point["id"])
            statement = point["statement"]
            assert not re.match(r"(?i)other\b|not elsewhere classified", statement)
            assert not re.search(r"(?i)\bthere are\b", statement)
            assert statement.endswith(".") and statement.count(".") == 1
            assert VERBS.search(statement)
            assert len(WORD.findall(statement)) <= 25
            assert point.get("sources")
            for src in point["sources"]:
                source_ok(src)
            if point.get("support"):
                assert point.get("question_raised") in QUESTIONS
    assert len(ids) == len(set(ids))
    live = set(ids)
    for item in pyramid.get("retired") or []:
        assert item["status"] == "RETIRED"
        assert item["id"] not in live

    place_items = [item for item in queue["items"] if item.get("task", "place") == "place"]
    summary_items = [item for item in queue["items"] if item.get("task") == "summarise"]
    queued_ids = [item["node_id"] for item in place_items]
    assert len(queued_ids) == len(set(queued_ids)) == build["queued"]
    assert len(summary_items) == build["needs_summary"]
    assert all(item.get("needs_summary") and item.get("point_id") for item in summary_items)
    placed_nodes = {
        point["anchor"][5:]
        for point in _walk_points(key["points"])
        if point.get("anchor", "").startswith("node:")
    }
    assert placed_nodes.isdisjoint(queued_ids)


def _concept(cid, name, parent=None):
    return {
        "id": cid,
        "name": name,
        "cell": "EV.O.A1",
        "parent": parent,
        "sources": [{"scheme": "GEMET", "id": cid, "code": cid, "file": "maps/EV/gemet.json"}],
    }


def test_filler_patterns_fail():
    assert is_filler("Alternative fuel is the class that holds the ideas grouped with it.")
    assert is_filler("Pest control is a pressure.")
    assert not is_filler("These substances are the sewage pressures.")
    assert not is_filler("Extraction is the load from taking water, fish, or minerals.")
    statement, needs, _feature = summarise_names(
        ["Nitrogenous fertiliser", "Nitrogenous waste"], "pressure", "substance",
    )
    assert needs is False
    assert not is_filler(statement)
    assert "nitrogenous" in statement
    weak, flagged, _feature = summarise_names(["Alpha", "Beta"], "pressure", "activity")
    assert flagged is True
    assert not is_filler(weak)
    assert weak.count(".") == 1
    assert len(WORD.findall(weak)) <= 25


def test_dpsir_role_and_kind():
    rules = _load(ROOT / "pyramids" / "rules" / "EV.json")
    assert dpsir_role("waste water treatment", rules) == "response"
    assert dpsir_role("pest control", rules) == "response"
    assert dpsir_role("grain", rules) == "state"
    assert dpsir_role("urban waste water", rules) == "ambiguous"
    assert dpsir_role("food processing", rules) == "driver"
    assert dpsir_role("food processing industry", rules) == "driver"
    assert dpsir_role("rubber processing", rules) == "driver"
    assert dpsir_role("waste processing industry", rules) == "driver"
    assert dpsir_role("data processing", rules) != "driver"
    assert kind_of("animal husbandry") == "activity"
    assert kind_of("working population engaged in agriculture") == "population"
    assert kind_of("urban flows") == "flow"
    assert kind_of("cities urban geography") == "place"


def test_pack_keeps_one_kind():
    book = IdBook("EV", None)
    by_id = {}
    children = defaultdict(list)
    placed = {}
    rows = [
        ("A", "Animal husbandry", None),
        ("B", "Crop farming", None),
        ("C", "Working population engaged in agriculture", None),
        ("D", "Urban flows", None),
    ]
    for cid, name, parent in rows:
        by_id[cid] = _concept(cid, name, parent)
        placed[cid] = {"facet": "land", "method": "rule"}
    packed = pack_concepts(placed, by_id, children, "land", book, "EV.P.1.2", "pressure", {})
    assert {point["kind"] for point in packed["points"]} == {"activity"}
    queued = {item["name"] for item in packed["queued"]}
    assert "Working population engaged in agriculture" in queued
    assert "Urban flows" in queued
    for point in packed["points"]:
        assert not is_filler(point["statement"]) or not point.get("support")


def test_parent_gets_a_summary():
    book = IdBook("EV", None)
    by_id = {}
    children = defaultdict(list)
    placed = {}
    rows = [
        ("P", "Animal husbandry", None),
        ("C1", "Livestock farming", "P"),
        ("C2", "Crop farming", "P"),
        ("Q", "Timber logging", None),
    ]
    for cid, name, parent in rows:
        by_id[cid] = _concept(cid, name, parent)
        placed[cid] = {"facet": "land", "method": "rule"}
        if parent:
            children[parent].append(cid)
    packed = pack_concepts(placed, by_id, children, "land", book, "EV.P.1.2", "pressure", {})
    parents = [point for point in packed["points"] if point.get("support")]
    assert parents
    assert {point["kind"] for point in packed["points"]} == {"activity"}
    for point in parents:
        assert not is_filler(point["statement"])
        kids = point["support"]["points"]
        assert len({kid["kind"] for kid in kids}) == 1
    assert any(item.get("needs_summary") for item in packed["summaries"]) or all(
        not point.get("needs_summary") for point in parents
    )


def test_resume_respects_task_and_candidates():
    module = _queue_module()
    item = {
        "task": "place",
        "node_id": "N1",
        "candidates": [{"group_id": "EV.P.1.1"}, {"group_id": "EV.P.1.2"}],
    }
    catalog = [{"group_id": "EV.P.1"}, {"group_id": "EV.P.2"}, {"group_id": "EV.P.4"}]
    assert module.result_matches(item, {"node_id": "N1", "group_id": "EV.P.1.1"})
    assert module.result_matches(item, {"node_id": "N1", "group_id": "unsure"})
    assert module.result_matches(item, {"node_id": "N1", "group_id": "out_of_scope", "status": "out_of_scope"})
    assert module.result_matches(item, {"node_id": "N1", "group_id": "EV.P.2", "status": "placed"}, catalog)
    assert not module.result_matches(item, {"node_id": "N1", "group_id": "EV.P.9.9"}, catalog)
    assert not module.result_matches(
        item,
        {"node_id": "N1", "group_id": "unsure", "status": "unsure", "reason": "the model reply was not usable"},
    )
    assert module.result_matches(
        item,
        {"node_id": "N1", "group_id": "unsure", "status": "unsure", "reason": "medicine is not a pressure"},
    )
    summary = {
        "task": "summarise",
        "needs_summary": True,
        "node_id": "EV.P.1.1",
        "point_id": "EV.P.1.1",
    }
    assert not module.result_matches(summary, {"node_id": "EV.P.1.1", "group_id": "EV.P.1.1"})
    assert module.result_matches(summary, {"task": "summarise", "point_id": "EV.P.1.1", "node_id": "EV.P.1.1"})


def test_summary_request_asks_for_a_sentence():
    module = _queue_module()
    body = module.request_body({
        "task": "summarise",
        "needs_summary": True,
        "node_id": "EV.P.1.1.1",
        "point_id": "EV.P.1.1.1",
        "cell": "EV.O.A1",
        "children": ["Alpha is a pressure.", "Beta is a pressure."],
    })
    assert body["think"] is False
    assert body["stream"] is False
    schema = body["format"]
    item_schema = schema["properties"]["items"]["items"]
    assert "summary" in item_schema["properties"]
    assert "group_id" not in item_schema["properties"]
    assert "is the class that holds" not in body["messages"][0]["content"]
    assert "Both are" in body["messages"][0]["content"]
    assert body["messages"][0]["content"] == module.SYSTEM_SUMMARY
    weak = module.row_from_model(
        {"task": "summarise", "point_id": "EV.P.2.2.2", "node_id": "EV.P.2.2.2", "cell": "EV.O.A2"},
        {"summary": "Both are freshwater bodies that are measured as states.", "reason": "same"},
    )
    assert weak["status"] == "needs_review"
    assert not module.result_matches(
        {"task": "summarise", "point_id": "EV.P.2.2.2", "node_id": "EV.P.2.2.2"},
        weak,
    )
    kept = {
        "task": "summarise",
        "point_id": "EV.P.2.2.2",
        "node_id": "EV.P.2.2.2",
        "status": "placed",
        "summary": "Both are freshwater bodies or their beds that are measured as environmental states.",
    }
    assert module.result_matches(
        {"task": "summarise", "point_id": "EV.P.2.2.2", "node_id": "EV.P.2.2.2"},
        kept,
    )
    assert module.row_status(kept) == "placed"


def _blob(point):
    parts = [point.get("statement") or "", point.get("name") or ""]
    for child in (point.get("support") or {}).get("points") or []:
        parts.append(_blob(child))
    return "\n".join(parts)


def test_parents_are_not_filler():
    pyramid = _load(ROOT / "pyramids" / "EV.json")
    markdown = (ROOT / "pyramids" / "EV_minto.md").read_text(encoding="utf-8")
    assert "is the class that holds" not in markdown
    for point in _walk_points(pyramid["key_line"]["points"]):
        if point.get("support"):
            assert not is_filler(point["statement"]), point["statement"]


def test_facet_groups_are_one_kind():
    pyramid = _load(ROOT / "pyramids" / "EV.json")
    for cell in pyramid["key_line"]["points"]:
        for facet in (cell.get("support") or {}).get("points") or []:
            _assert_one_kind(facet)


def _assert_one_kind(point):
    support = point.get("support") or {}
    kids = support.get("points") or []
    if not kids:
        return
    kinds = {kid.get("kind") for kid in kids}
    assert len(kinds) == 1, point.get("statement")
    for kid in kids:
        if kid.get("support"):
            _assert_one_kind(kid)


def test_dpsir_placement_on_ev():
    pyramid = _load(ROOT / "pyramids" / "EV.json")
    queue = _load(ROOT / "pyramids" / "queues" / "EV.json")
    by_cell = {point["cell"]: point for point in pyramid["key_line"]["points"]}
    pressures = _blob(by_cell["EV.O.A1"]).lower()
    assert "waste water treatment" not in pressures
    assert "pest control" not in pressures
    assert not re.search(r"\bgrain\b", pressures)
    assert "urban waste water" not in pressures
    assert "waste processing" not in pressures
    placed_names = {
        (point.get("name") or "").lower()
        for point in _walk_points(pyramid["key_line"]["points"])
        if str(point.get("anchor") or "").startswith("node:")
    }
    assert "urban waste water" not in placed_names
    assert "waste processing industry" not in placed_names
    place_items = [item for item in queue["items"] if item.get("task", "place") == "place"]
    ambiguous = [item["name"].lower() for item in place_items if item.get("reason") == "the DPSIR role is ambiguous"]
    assert any("urban waste water" in name for name in ambiguous)
    assert not any("waste processing" in name for name in ambiguous)
    drivers = [item for item in place_items if item.get("dpsir") == "driver"]
    driver_names = {item["name"].lower() for item in drivers}
    assert {"food processing industry", "rubber processing industry", "waste processing industry", "rubber processing"} <= driver_names
    assert {item["cell"] for item in drivers} == {"EV.O.A1"}
    assert {item["candidates"][0]["group_id"] for item in drivers} == {"EV.P.1"}
    assert len({item.get("note") for item in drivers}) == 1
    responses = _blob(by_cell["EV.O.A4"]).lower()
    states = _blob(by_cell["EV.O.A2"]).lower()
    queued_names = "\n".join(item["name"].lower() for item in place_items)
    assert "pest control" in responses
    assert "waste water treatment" in responses
    assert re.search(r"\bgrain\b", states) or re.search(r"\bgrain\b", queued_names)


def _queue_root(tmp_path, items, previous=None):
    queue_dir = tmp_path / "pyramids" / "queues"
    queue_dir.mkdir(parents=True)
    (queue_dir / "EV.json").write_text(json.dumps({"field": "EV", "items": items}), encoding="utf-8")
    if previous is not None:
        (queue_dir / "EV.placed.json").write_text(
            json.dumps({"field": "EV", "model": "qwen3:30b-a3b", "items": previous}),
            encoding="utf-8",
        )
    return tmp_path


def _place_item(number):
    return {
        "task": "place",
        "node_id": f"N{number}",
        "name": f"concept {number}",
        "cell": "EV.O.A1",
        "candidates": [
            {"facet": "emissions", "group_id": "EV.P.1.1", "statement": "Emissions are loads."},
            {"cell": "EV.O.A4", "group_id": "EV.P.4", "statement": "Responses are actions."},
        ],
    }


def _model_reply(body):
    payload = json.loads(body["messages"][1]["content"])
    rows = []
    for item in payload["items"]:
        if "children" in item:
            rows.append({"id": item["id"], "summary": "These ideas share a feature.", "reason": "shared"})
        else:
            choice = (item.get("choices") or ["unsure"])[0]
            rows.append({"id": item["id"], "group_id": choice, "reason": "fit"})
    return {"choices": [{"message": {"content": json.dumps({"items": rows})}}]}


def test_batch_size_stays_between_15_and_25():
    module = _queue_module()
    assert module.BATCH_SIZE == 20
    assert module.clamp_batch(5) == 15
    assert module.clamp_batch(20) == 20
    assert module.clamp_batch(100) == 25
    assert module.clamp_workers(8) == 4
    assert module.clamp_workers(3) == 3
    assert len(module.SYSTEM_PLACE) < 1200
    assert "natural-hazards group" in module.SYSTEM_PLACE
    assert "raster" in module.SYSTEM_PLACE


def test_prompt_offers_every_cell_and_an_escape():
    module = _queue_module()
    catalog = module.cell_catalog("EV")
    by_id = {row["group_id"]: row for row in catalog}
    assert by_id["EV.P.1"]["cell"] == "EV.O.A1"
    assert by_id["EV.P.2.4"]["cell"] == "EV.O.A2"
    assert by_id["EV.P.3.1"]["cell"] == "EV.O.A3"
    assert by_id["EV.P.4.3"]["cell"] == "EV.O.A4"
    assert by_id["EV.P.5.1"]["cell"] == "EV.O.A5"
    forced = [
        ("drug (medicine)", "EV.P.1.4", "Introduced species are the loads from pests."),
        ("dust removal", "EV.P.1.3", "Extraction is the load from taking a resource."),
        ("East-West trade", "EV.P.1.2", "Land and sea use changes are loads."),
        ("dual economy", "EV.P.1.2", "Land and sea use changes are loads."),
        ("dry deposition", "EV.P.1.1", "Emissions are the loads from pollutants."),
        ("seismic activity", "EV.P.1.1", "Emissions are the loads from pollutants."),
    ]
    top_groups = {"EV.P.1.1", "EV.P.2.1", "EV.P.2.4", "EV.P.3.1", "EV.P.4.2", "EV.P.5.3"}
    for name, group_id, statement in forced:
        body = module.request_batch([_pressure_item(name, group_id, statement)], catalog=catalog)
        choices = json.loads(body["messages"][1]["content"])["items"][0]["choices"]
        assert {"EV.P.1", "EV.P.2", "EV.P.3", "EV.P.4", "EV.P.5"} <= set(choices)
        assert top_groups <= set(choices)
        assert group_id in choices
        assert choices[-2:] == ["unsure", "out_of_scope"]
        assert "natural-hazards group" in body["messages"][0]["content"]
        assert "Do not force a fit." in body["messages"][0]["content"]


def test_fake_model_batches_concurrently_and_appends_jsonl(tmp_path, capsys):
    import threading
    import time
    module = _queue_module()
    items = [_place_item(number) for number in range(40)]
    items.extend([
        {
            "task": "place",
            "node_id": "FOOD",
            "name": "food processing industry",
            "cell": "EV.O.A1",
            "candidates": [
                {"cell": "EV.O.A1", "group_id": "EV.P.1", "statement": "Pressures are loads."},
                {"cell": "EV.O.A4", "group_id": "EV.P.4", "statement": "Responses are actions."},
            ],
        },
        {
            "task": "place",
            "node_id": "RUBBER",
            "name": "rubber processing",
            "cell": "EV.O.A1",
            "candidates": [{"facet": "extraction", "group_id": "EV.P.1.3", "statement": "Extraction is a load."}],
        },
        {
            "task": "place",
            "node_id": "WASTE",
            "name": "waste processing industry",
            "cell": "EV.O.A2",
            "candidates": [
                {"cell": "EV.O.A1", "group_id": "EV.P.1", "statement": "Pressures are loads."},
                {"cell": "EV.O.A2", "group_id": "EV.P.2", "statement": "States are conditions."},
            ],
        },
    ])
    root = _queue_root(tmp_path, items, previous=[{"node_id": "N0", "group_id": "EV.P.1.1", "name": "concept 0"}])
    calls = []
    inflight = {"n": 0, "max": 0}
    lock = threading.Lock()

    def post(body):
        with lock:
            inflight["n"] += 1
            inflight["max"] = max(inflight["max"], inflight["n"])
        time.sleep(0.1)
        with lock:
            inflight["n"] -= 1
            calls.append(body)
        text = body["messages"][1]["content"]
        assert body["stream"] is False
        assert body["think"] is False
        assert body["format"] is module.PLACE_SCHEMA
        assert body["options"]["num_predict"] == 3000
        for row in json.loads(text)["items"]:
            assert "unsure" in row["choices"]
            assert "out_of_scope" in row["choices"]
            assert "EV.P.2" in row["choices"]
            assert "EV.P.4" in row["choices"]
        assert "Do not force a fit." in body["messages"][0]["content"]
        assert len(json.loads(text)["items"]) <= 20
        return _model_reply(body)

    args = module.parse_args(["--field", "EV", "--batch", "20", "--workers", "2", "--progress", "20"])
    result = module.run(args, post=post, root=root)
    path = root / "pyramids" / "queues" / "EV.placed.jsonl"
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    assert result["wrote"] == 42
    assert len(rows) == 42
    assert inflight["max"] >= 2
    assert any(len(json.loads(call["messages"][1]["content"])["items"]) == 20 for call in calls)
    drivers = [row for row in rows if row.get("dpsir") == "driver"]
    assert {row["name"] for row in drivers} == {
        "food processing industry", "rubber processing", "waste processing industry",
    }
    assert {row["group_id"] for row in drivers} == {"EV.P.1"}
    assert {row["status"] for row in drivers} == {"placed"}
    assert {row["note"] for row in drivers} == {drivers[0]["note"]}
    asked = [item["name"] for call in calls for item in json.loads(call["messages"][1]["content"])["items"]]
    assert "food processing industry" not in asked
    assert "rubber processing" not in asked
    assert "waste processing industry" not in asked
    assert "eta " in capsys.readouterr().out
    before = path.read_text(encoding="utf-8")
    again = module.run(args, post=post, root=root)
    assert again["wrote"] == 0
    assert path.read_text(encoding="utf-8") == before


def test_bad_json_retries_splits_and_marks_unsure(tmp_path):
    module = _queue_module()
    items = [_place_item(number) for number in range(4)]
    root = _queue_root(tmp_path, items)
    calls = {"n": 0}

    def post(body):
        calls["n"] += 1
        return {"choices": [{"message": {"content": "not json"}}]}

    args = module.parse_args(["--field", "EV", "--batch", "15", "--workers", "1", "--progress", "100"])
    module.run(args, post=post, root=root)
    rows = [json.loads(line) for line in (root / "pyramids" / "queues" / "EV.placed.jsonl").read_text().splitlines()]
    assert len(rows) == 4
    assert {row["status"] for row in rows} == {"unsure"}
    assert {row["group_id"] for row in rows} == {"unsure"}
    assert calls["n"] > 4


def test_native_reply_can_leave_the_pressure_facets(tmp_path):
    module = _queue_module()
    item = _pressure_item("drug (medicine)", "EV.P.1.4", "Introduced species are the loads from pests.")
    root = _queue_root(tmp_path, [item])

    def post(body):
        assert body["stream"] is False
        assert body["think"] is False
        assert body["format"]["required"] == ["items"]
        assert body["options"] == {"temperature": 0, "num_predict": 3000}
        return {"message": {"content": json.dumps({"items": [
            {"id": "drug (medicine)", "group_id": "out_of_scope", "reason": "a medicine is not an environmental load"},
        ]})}}

    args = module.parse_args(["--field", "EV", "--api", "native", "--workers", "1", "--progress", "100"])
    module.run(args, post=post, root=root)
    row = json.loads((root / "pyramids" / "queues" / "EV.placed.jsonl").read_text().strip())
    assert row["status"] == "out_of_scope"
    assert row["group_id"] == "out_of_scope"
    again = module.run(args, post=post, root=root)
    assert again["wrote"] == 0


def test_unusable_reply_is_asked_again(tmp_path):
    module = _queue_module()
    item = _pressure_item("dry deposition", "EV.P.1.1", "Emissions are the loads from pollutants.")
    item["node_id"] = "N1"
    previous = [{
        "node_id": "N1",
        "group_id": "unsure",
        "status": "unsure",
        "reason": "the model reply was not usable",
    }]
    root = _queue_root(tmp_path, [item], previous=previous)

    def post(body):
        return {"message": {"content": json.dumps({"items": [
            {"id": "N1", "group_id": "EV.P.2", "reason": "a measured transfer, not a load"},
        ]})}}

    args = module.parse_args(["--field", "EV", "--api", "native", "--workers", "1", "--progress", "100"])
    result = module.run(args, post=post, root=root)
    assert result["wrote"] == 1
    row = json.loads((root / "pyramids" / "queues" / "EV.placed.jsonl").read_text().strip())
    assert row["status"] == "placed"
    assert row["group_id"] == "EV.P.2"


def test_unknown_group_needs_review(tmp_path):
    module = _queue_module()
    root = _queue_root(tmp_path, [_place_item(1)])

    def post(body):
        payload = json.loads(body["messages"][1]["content"])
        rows = [{"id": item["id"], "group_id": "NOPE", "reason": "guess"} for item in payload["items"]]
        return {"choices": [{"message": {"content": json.dumps({"items": rows})}}]}

    args = module.parse_args(["--field", "EV", "--workers", "1", "--progress", "100"])
    module.run(args, post=post, root=root)
    row = json.loads((root / "pyramids" / "queues" / "EV.placed.jsonl").read_text().strip())
    assert row["status"] == "needs_review"
    assert row["group_id"] == "NOPE"


def test_limit_and_dry_run_do_not_call_the_model(tmp_path, capsys):
    module = _queue_module()
    root = _queue_root(tmp_path, [_place_item(number) for number in range(10)])

    def post(body):
        raise AssertionError("dry-run must not call the model")

    args = module.parse_args(["--field", "EV", "--limit", "5", "--dry-run", "--batch", "20", "--workers", "3"])
    result = module.run(args, post=post, root=root)
    assert result["wrote"] == 0
    assert result["pending"] == 5
    assert result["batch"] == 20
    output = capsys.readouterr().out
    assert "dry-run" in output
    assert "OLLAMA_NUM_PARALLEL=3" in output
    assert not (root / "pyramids" / "queues" / "EV.placed.jsonl").exists()

    seen = []

    def limited(body):
        seen.append(body)
        return _model_reply(body)

    limited_args = module.parse_args(["--field", "EV", "--limit", "2", "--workers", "1", "--progress", "100"])
    module.run(limited_args, post=limited, root=root)
    assert len(seen) == 1
    assert len(json.loads(seen[0]["messages"][1]["content"])["items"]) == 2


def test_sonnet_list_price_per_thousand_items():
    module = _queue_module()
    assert module.parse_args(["--field", "EV"]).backend == "ollama"
    assert module.parse_args(["--field", "EV"]).max_cost == 10
    assert module.resolve_model("ollama", "") == "qwen3:30b-a3b"
    assert module.resolve_model("anthropic", "") == "claude-sonnet-5-5"
    assert module.resolve_model("anthropic", "claude-sonnet-4-5") == "claude-sonnet-4-5"
    assert module.price_rates("claude-sonnet-5-5") == (2.0, 10.0, 2.5, 0.10)
    assert module.price_rates("claude-sonnet-4-5") == (3.0, 15.0, 3.75, 0.30)
    assert module.price_rates("claude-sonnet-5")[3] == 0.20
    per_thousand = module.expected_usd_per_thousand("claude-sonnet-5-5")
    assert abs(per_thousand - 0.90) < 1e-9
    assert abs(module.output_cap_usd_per_thousand("claude-sonnet-5-5") - 1.80) < 1e-9
    assert module.expected_usd_per_thousand("claude-sonnet-4-5") > per_thousand


def test_ev_place_prefix_can_clear_the_cache_minimum():
    module = _queue_module()
    queue = _load(ROOT / "pyramids" / "queues" / "EV.json")
    items = [item for item in queue["items"] if module.item_task(item) == "place"]
    prefix = module.stable_prefix(module.cell_catalog("EV"), items)
    assert "Do not force a fit." in prefix
    assert "EV.P.1" in prefix and "EV.P.5" in prefix
    assert len(prefix) >= 2048


def test_anthropic_dry_run_prints_the_cached_request(tmp_path, capsys, monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    module = _queue_module()
    root = _queue_root(tmp_path, [_place_item(number) for number in range(5)])

    def post(body):
        raise AssertionError("dry-run must not call the model")

    args = module.parse_args([
        "--field", "EV", "--backend", "anthropic", "--dry-run", "--limit", "5", "--max-cost", "10",
    ])
    result = module.run(args, post=post, root=root)
    output = capsys.readouterr().out
    assert result["wrote"] == 0
    assert "backend=anthropic" in output
    assert "model=claude-sonnet-5-5" in output
    assert "expected $0.90 per 1000 items" in output
    assert '"cache_control": {"type": "ephemeral"}' in output
    assert "Do not force a fit." in output
    assert not (root / "pyramids" / "queues" / "EV.placed.jsonl").exists()


def test_anthropic_requires_a_key(tmp_path, monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    module = _queue_module()
    root = _queue_root(tmp_path, [_place_item(1)])
    args = module.parse_args(["--field", "EV", "--backend", "anthropic", "--workers", "1"])
    try:
        module.run(args, root=root)
    except SystemExit as exc:
        assert "ANTHROPIC_API_KEY" in str(exc)
    else:
        raise AssertionError("a live Anthropic run without a key must stop")
    assert not (root / "pyramids" / "queues" / "EV.placed.jsonl").exists()


def _anthropic_client(group_id, usage):
    def client(payload):
        assert payload["model"]
        assert "temperature" not in payload
        user = json.loads(payload["messages"][0]["content"])
        rows = [
            {"id": item["id"], "group_id": group_id, "reason": "not a load"}
            for item in user["items"]
        ]
        return {
            "content": [{"type": "tool_use", "name": payload["tools"][0]["name"], "input": {"items": rows}}],
            "usage": usage,
            "model": payload["model"],
        }
    return client


def test_anthropic_fake_client_places_and_caches(tmp_path, capsys):
    module = _queue_module()
    root = _queue_root(tmp_path, [_pressure_item("drug (medicine)", "EV.P.1.4", "Introduced species are loads.")])
    seen = []

    def client(payload):
        seen.append(payload)
        assert payload["model"] == "claude-sonnet-5-5"
        assert payload["max_tokens"] == 3000
        assert "temperature" not in payload
        assert payload["thinking"] == {"type": "between_tools"}
        assert payload["output_config"] == {"effort": "high"}
        assert payload["tool_choice"] == {"type": "auto"}
        tool = payload["tools"][0]
        assert tool["name"] == "record_placements"
        assert tool["strict"] is True
        assert tool["cache_control"] == {"type": "ephemeral"}
        assert "items" in tool["input_schema"]["properties"]
        assert payload["system"][0]["cache_control"] == {"type": "ephemeral"}
        assert "Do not force a fit." in payload["system"][0]["text"]
        user = payload["messages"][0]["content"]
        choices = json.loads(user)["items"][0]["choices"]
        assert {"EV.P.1", "EV.P.2", "EV.P.3", "EV.P.4", "EV.P.5", "EV.P.1.1", "EV.P.2.4"} <= set(choices)
        assert choices[-2:] == ["unsure", "out_of_scope"]
        return _anthropic_client("out_of_scope", {
            "input_tokens": 1000,
            "output_tokens": 400,
            "cache_read_input_tokens": 500,
            "cache_creation_input_tokens": 80,
        })(payload)

    args = module.parse_args([
        "--field", "EV", "--backend", "anthropic", "--workers", "1", "--progress", "1", "--max-cost", "10",
    ])
    result = module.run(args, post=client, root=root)
    assert len(seen) == 1
    assert result["stopped"] is False
    assert abs(result["cost"] - module.list_usd(
        "claude-sonnet-5-5", input_tokens=1000, output_tokens=400, cache_read=500, cache_write=80,
    )) < 1e-9
    row = json.loads((root / "pyramids" / "queues" / "EV.placed.jsonl").read_text().strip())
    assert row["status"] == "out_of_scope"
    output = capsys.readouterr().out
    assert "cost $" in output
    assert "cache_read 500" in output
    again = module.run(args, post=client, root=root)
    assert again["wrote"] == 0
    assert len(seen) == 1


def test_anthropic_accepts_json_text_and_sonnet_45_forces_the_tool():
    module = _queue_module()
    item = _pressure_item("dust removal", "EV.P.1.3", "Extraction is a load.")
    older = module.to_anthropic(
        module.request_batch([item], catalog=[]),
        "claude-sonnet-4-5",
        module.stable_prefix([], [item]),
    )
    assert older["model"] == "claude-sonnet-4-5"
    assert older["tool_choice"] == {"type": "tool", "name": "record_placements"}
    assert "thinking" not in older
    assert "temperature" not in older
    text = json.dumps({"items": [{"id": "dust removal", "group_id": "unsure", "reason": "not a load"}]})
    assert module.anthropic_content({"content": [{"type": "text", "text": text}]}) == text
    parsed = module.parse_model_json(module.anthropic_content({
        "content": [{"type": "tool_use", "name": "record_placements", "input": {"items": [
            {"id": "dust removal", "group_id": "EV.P.4", "reason": "an action"},
        ]}}],
    }))
    assert parsed[0]["group_id"] == "EV.P.4"


def test_max_cost_stops_before_the_next_batch(tmp_path, capsys):
    module = _queue_module()
    items = [_place_item(number) for number in range(30)]
    root = _queue_root(tmp_path, items)
    calls = {"n": 0}

    def client(payload):
        calls["n"] += 1
        user = json.loads(payload["messages"][0]["content"])
        rows = [
            {"id": item["id"], "group_id": "unsure", "reason": "no home"}
            for item in user["items"]
        ]
        return {
            "content": [{"type": "tool_use", "name": "record_placements", "input": {"items": rows}}],
            "usage": {"input_tokens": 1_000_000, "output_tokens": 100},
            "model": payload["model"],
        }

    args = module.parse_args([
        "--field", "EV", "--backend", "anthropic", "--batch", "15", "--workers", "1",
        "--max-cost", "1", "--progress", "100",
    ])
    result = module.run(args, post=client, root=root)
    assert calls["n"] == 1
    assert result["stopped"] is True
    assert result["wrote"] == 15
    assert result["cost"] > 1
    rows = [json.loads(line) for line in (root / "pyramids" / "queues" / "EV.placed.jsonl").read_text().splitlines()]
    assert {row["node_id"] for row in rows} == {f"N{number}" for number in range(15)}
    assert "the model reply was not usable" not in (root / "pyramids" / "queues" / "EV.placed.jsonl").read_text()
    assert "stopped at max-cost $1.00" in capsys.readouterr().out


def test_cell_comes_from_the_chosen_group():
    module = _queue_module()
    catalog = module.cell_catalog("EV")
    item = _pressure_item("compaction", "EV.P.1.1", "Emissions are loads.")
    item["cell"] = "EV.O.A1"
    row = module.row_from_model(item, {"group_id": "EV.P.2.4", "reason": "a soil condition"}, catalog)
    assert row["status"] == "placed"
    assert row["group_id"] == "EV.P.2.4"
    assert row["cell"] == "EV.O.A2"
    hazard = module.row_from_model(
        _pressure_item("seismic activity", "EV.P.1.1", "Emissions are loads."),
        {"group_id": "EV.P.3.1", "reason": "a natural harm"},
        catalog,
    )
    assert hazard["status"] == "placed"
    assert hazard["cell"] == "EV.O.A3"


def test_resume_drops_duplicate_jsonl_rows(tmp_path):
    module = _queue_module()
    item = _place_item(1)
    root = _queue_root(tmp_path, [item])
    path = root / "pyramids" / "queues" / "EV.placed.jsonl"
    first = {"node_id": "N1", "name": "concept 1", "group_id": "EV.P.1.1", "status": "needs_review", "cell": "EV.O.A1", "reason": "first"}
    second = {"node_id": "N1", "name": "concept 1", "group_id": "EV.P.1.1", "status": "needs_review", "cell": "EV.O.A1", "reason": "second"}
    path.write_text(json.dumps(first) + "\n" + json.dumps(second) + "\n", encoding="utf-8")
    assert module.compact_jsonl(path) == 1
    kept = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    assert len(kept) == 1
    assert kept[0]["reason"] == "second"
    saved = module.load_previous(root / "pyramids" / "queues" / "EV.placed.json", path)
    assert len(saved) == 1
    assert saved[0]["reason"] == "second"


def test_only_status_reruns_the_named_rows(tmp_path):
    module = _queue_module()
    items = [
        _pressure_item("trade fair", "EV.P.1.1", "Emissions are loads."),
        _pressure_item("banking", "EV.P.1.2", "Land use is a load."),
        _place_item(3),
    ]
    items[0]["node_id"] = "TRADE"
    items[1]["node_id"] = "BANK"
    items[2]["node_id"] = "N3"
    previous = [
        {"node_id": "TRADE", "name": "trade fair", "group_id": "out_of_scope", "status": "out_of_scope", "cell": "EV.O.A1", "reason": "not environmental"},
        {"node_id": "BANK", "name": "banking", "group_id": "EV.P.4.3", "status": "needs_review", "cell": "EV.O.A1", "reason": "outside the list"},
        {"node_id": "N3", "name": "concept 3", "group_id": "EV.P.1.1", "status": "placed", "cell": "EV.O.A1", "reason": "kept"},
    ]
    root = _queue_root(tmp_path, items, previous=previous)
    # The runner reads placed.json and the jsonl. Put the duplicate only in the jsonl.
    jsonl = root / "pyramids" / "queues" / "EV.placed.jsonl"
    jsonl.write_text(
        json.dumps({"node_id": "BANK", "name": "banking", "group_id": "unsure", "status": "unsure", "cell": "EV.O.A1", "reason": "older"}) + "\n",
        encoding="utf-8",
    )
    asked = []

    def post(body):
        payload = json.loads(body["messages"][1]["content"])
        asked.extend(item["id"] for item in payload["items"])
        rows = []
        for item in payload["items"]:
            group = "EV.P.3.1" if item["id"] == "TRADE" else "out_of_scope"
            rows.append({"id": item["id"], "group_id": group, "reason": "again"})
        return {"choices": [{"message": {"content": json.dumps({"items": rows})}}]}

    args = module.parse_args([
        "--field", "EV", "--workers", "1", "--progress", "100",
        "--only-status", "out_of_scope,needs_review,unsure",
    ])
    result = module.run(args, post=post, root=root)
    assert set(asked) == {"TRADE", "BANK"}
    assert "N3" not in asked
    assert result["wrote"] == 2
    rows = [json.loads(line) for line in jsonl.read_text(encoding="utf-8").splitlines()]
    by_id = {row["node_id"]: row for row in rows}
    assert len(rows) == len(by_id)
    assert by_id["TRADE"]["status"] == "placed"
    assert by_id["TRADE"]["cell"] == "EV.O.A3"
    assert by_id["TRADE"]["group_id"] == "EV.P.3.1"
    assert by_id["BANK"]["status"] == "out_of_scope"
    assert by_id["BANK"]["reason"] == "again"
    again = module.run(args, post=post, root=root)
    assert again["wrote"] == 1
    assert again["pending"] == 1


def test_natural_hazards_and_technical_terms_are_ruled():
    module = _queue_module()
    rules = module.load_rules("EV")
    quake = module.natural_row(
        {"task": "place", "node_id": "GEMET:2402", "name": "earthquake"},
        rules,
    )
    assert quake["group_id"] == "EV.P.2.6.1"
    assert quake["cell"] == "EV.O.A2"
    assert quake["status"] == "placed"
    assert quake["dpsir"] == "natural"
    assert module.natural_row({"task": "place", "node_id": "X", "name": "volcano"}, rules) is None
    assert module.natural_row({"task": "place", "node_id": "N", "name": "nutrient cycle"}, rules) is None
    flood = module.natural_row({"task": "place", "node_id": "GEMET:3298", "name": "flood"}, rules)
    assert flood["group_id"] == "EV.P.2.6.2"
    assert flood["cell"] == "EV.O.A2"
    assert flood["status"] == "placed"
    for name in ("storm", "drought", "heat wave", "natural disaster", "cyclone"):
        row = module.natural_row({"task": "place", "node_id": name, "name": name}, rules)
        assert row["group_id"] == "EV.P.2.6.2", name
    assert module.natural_row({"task": "place", "node_id": "F", "name": "flood prevention"}, rules) is None
    assess = module.grouped_row(
        {"task": "place", "node_id": "GEMET:2774", "name": "environmental assessment"},
        rules,
    )
    assert assess["group_id"] == "EV.P.4.7.1"
    assert assess["cell"] == "EV.O.A4"
    assert assess["status"] == "placed"
    econ = module.scoped_row(
        {"task": "place", "node_id": "E", "name": "environmental economics"},
        rules,
    )
    assert econ["status"] == "out_of_scope"
    assert econ["group_id"] == "out_of_scope"
    raster = module.technical_row(
        {"task": "place", "node_id": "GEMET:14922", "name": "raster", "cell": "EV.O.A2"},
        rules,
    )
    assert raster["status"] == "out_of_scope"
    assert raster["group_id"] == "out_of_scope"
    assert module.technical_row({"task": "place", "node_id": "Y", "name": "land register"}, rules) is None
    assert module.technical_row({"task": "place", "node_id": "Z", "name": "legislative"}, rules) is None
    catalog = module.cell_catalog("EV")
    by_id = {row["group_id"]: row for row in catalog}
    assert by_id["EV.P.2.6.1"]["cell"] == "EV.O.A2"
    assert by_id["EV.P.2.6.2"]["cell"] == "EV.O.A2"
    assert by_id["EV.P.2.6.3"]["cell"] == "EV.O.A2"
    assert by_id["EV.P.2.1"]["cell"] == "EV.O.A2"
    assert by_id["EV.P.2.8"]["cell"] == "EV.O.A2"
    assert by_id["EV.P.2.10"]["cell"] == "EV.O.A2"
    assert by_id["EV.P.4.7.1"]["cell"] == "EV.O.A4"
    assert by_id["EV.P.4.7.2"]["cell"] == "EV.O.A4"
    item = {"task": "place", "node_id": "GEMET:2402", "name": "earthquake"}
    assert not module.result_matches(
        item,
        {"node_id": "GEMET:2402", "group_id": "EV.P.3.1", "status": "placed", "cell": "EV.O.A3"},
        catalog,
    )
    assert module.result_matches(item, quake, catalog)


def test_only_status_keeps_a_placed_summary(tmp_path):
    module = _queue_module()
    item = {
        "task": "summarise",
        "needs_summary": True,
        "node_id": "EV.P.2.2.2",
        "point_id": "EV.P.2.2.2",
        "name": "These places are alike as measured states.",
        "cell": "EV.O.A2",
        "children": ["Lake is a state.", "A river bed is a state."],
    }
    saved = {
        "task": "summarise",
        "node_id": "EV.P.2.2.2",
        "name": "These places are alike as measured states.",
        "cell": "EV.O.A2",
        "reason": "Lake and river bed are inland water features recorded as states.",
        "needs_summary": True,
        "point_id": "EV.P.2.2.2",
        "summary": "Both are freshwater bodies or their beds that are measured as environmental states.",
        "status": "placed",
    }
    root = _queue_root(tmp_path, [item], previous=[saved])
    asked = []

    def post(body):
        payload = json.loads(body["messages"][1]["content"])
        asked.extend(row["id"] for row in payload["items"])
        return {"choices": [{"message": {"content": json.dumps({"items": []})}}]}

    args = module.parse_args([
        "--field", "EV", "--workers", "1", "--progress", "100",
        "--only-status", "unsure,needs_review,out_of_scope",
    ])
    result = module.run(args, post=post, root=root)
    assert asked == []
    assert result["wrote"] == 0
    assert result["pending"] == 0
