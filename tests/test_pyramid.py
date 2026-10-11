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


def test_queue_request_disables_thinking():
    module = _queue_module()
    body = module.request_body({
        "node_id": "GEMET:1",
        "name": "acid rain",
        "cell": "EV.O.A1",
        "reason": "embedding gap 0.0010 is below 0.0200",
        "candidates": [
            {"facet": "emissions", "group_id": "EV.P.1.1", "statement": "Emissions are loads."},
            {"facet": "land", "group_id": "EV.P.1.2", "statement": "Land use is a load."},
        ],
    })
    assert body["model"] == "qwen3:30b-a3b"
    assert body["think"] is False
    schema = body["response_format"]["json_schema"]["schema"]
    assert schema["properties"]["group_id"]["enum"] == ["EV.P.1.1", "EV.P.1.2", "unsure"]
    assert "reason" in schema["required"]
    unsure = module.request_body({"node_id": "X", "name": "x", "cell": "EV.O.A1", "candidates": []})
    assert unsure["think"] is False
    assert unsure["response_format"]["json_schema"]["schema"]["properties"]["group_id"]["enum"] == ["unsure"]


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
    assert dpsir_role("waste processing industry", rules) == "ambiguous"
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
    assert module.result_matches(item, {"node_id": "N1", "group_id": "EV.P.1.1"})
    assert module.result_matches(item, {"node_id": "N1", "group_id": "unsure"})
    assert not module.result_matches(item, {"node_id": "N1", "group_id": "EV.P.9.9"})
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
    schema = body["response_format"]["json_schema"]["schema"]
    assert "summary" in schema["properties"]
    assert "group_id" not in schema["properties"]
    assert "is the class that holds" not in body["messages"][0]["content"]


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
    assert any("waste processing" in name for name in ambiguous)
    responses = _blob(by_cell["EV.O.A4"]).lower()
    states = _blob(by_cell["EV.O.A2"]).lower()
    queued_names = "\n".join(item["name"].lower() for item in place_items)
    assert "pest control" in responses
    assert "waste water treatment" in responses
    assert re.search(r"\bgrain\b", states) or re.search(r"\bgrain\b", queued_names)
