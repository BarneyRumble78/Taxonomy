#!/usr/bin/env python3
"""Second pass over a finished field. Anthropic only. No call unless asked.

    python3 scripts/quality_pass.py --field MA --max-cost 1 --global-max-cost 60

Rewrites a statement flagged for review, or written from the fallback template.
Re-forms a group that minto_check flags, a further group, or a group whose
members share no word with each other or with that statement. A cell the
former blocked, including one with fewer than four nodes, becomes one group.
One top-down check then compares the cell statements with the governing
thought and the key line in the field file.

Spend is added to pyramids/queues/cost_ledger.json under a file lock, after
re-reading the ledger, so another field's spend is kept. --max-cost is the
field total, including what the ledger already holds. 0 leaves the field cap
off. The global cap still applies.
"""
import argparse
import copy
import fcntl
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine" / "v3"))
sys.path.insert(0, str(ROOT / "scripts"))

from cost_cap import record as record_spend  # noqa: E402
from group_former import (  # noqa: E402
    _ident,
    _to_point,
    append_log,
    cell_jobs,
    checker_problems,
    form_batch,
    form_cell,
    is_fallback_statement,
    log_path,
    loosely_related,
    read_log,
    write_result,
)
from minto_check import WORD, is_definition  # noqa: E402
import run_group_former as former  # noqa: E402
import run_pyramid_queue as queue  # noqa: E402

FIELD_SYSTEM = "\n".join([
    "You check a classification from the top down.",
    "The governing thought is the one answer.",
    "The key line is two to five points under that answer.",
    "holds is true when the cell statements answer that thought and that key line.",
    "note is one sentence of at most twenty-five words.",
    "groups is an empty array.",
    "Do not invent a citation.",
    "Return JSON matching the schema.",
])

FIELD_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "holds": {"type": "boolean"},
        "note": {"type": "string"},
        "statement": {"type": "string"},
        "basis": {"type": "string", "enum": ["cause_effect", "parts", "kinds"]},
        "order": {"type": "string", "enum": ["time", "structure", "degree"]},
        "rank_note": {"type": "string"},
        "groups": former.SCHEMA["properties"]["groups"],
    },
    "required": ["holds", "note", "statement", "basis", "order", "rank_note", "groups"],
}


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Quality pass for one finished field.")
    parser.add_argument("--field", required=True)
    parser.add_argument("--dry-run", action="store_true", help="Print the work and do not call a model.")
    parser.add_argument("--model", default="")
    parser.add_argument("--max-cost", type=float, default=0.0, help="Field cap in USD, including the ledger. 0 means no field cap.")
    parser.add_argument("--global-max-cost", type=float, default=queue.DEFAULT_GLOBAL_MAX_COST)
    parser.add_argument("--root", default="")
    return parser.parse_args(argv)


def _locked(path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = path.open("a+", encoding="utf-8")
    fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
    return handle


def _unlock(handle):
    fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
    handle.close()


def read_ledger(path):
    """Read the shared ledger while holding its lock."""
    handle = _locked(path)
    try:
        handle.seek(0)
        raw = handle.read()
        if not raw.strip():
            return {"spent": 0.0, "fields": {}}
        data = json.loads(raw)
        data.setdefault("spent", 0.0)
        data.setdefault("fields", {})
        return data
    finally:
        _unlock(handle)


def add_spend(path, field, usd):
    """Re-read the ledger under the lock, then add this field's delta.

    A concurrent writer that also locks cannot lose this update, and this
    update cannot drop spend that landed after the run started.
    """
    amount = float(usd)
    if amount <= 0:
        return read_ledger(path)
    handle = _locked(path)
    try:
        handle.seek(0)
        raw = handle.read()
        if raw.strip():
            ledger = json.loads(raw)
        else:
            ledger = {"spent": 0.0, "fields": {}}
        ledger.setdefault("spent", 0.0)
        ledger.setdefault("fields", {})
        record_spend(ledger, field, amount)
        handle.seek(0)
        handle.truncate()
        handle.write(json.dumps(ledger, indent=2) + "\n")
        handle.flush()
        os.fsync(handle.fileno())
        return ledger
    finally:
        _unlock(handle)


def pyramid_section(text, name):
    """The body under a heading, with or without a section number."""
    lines = (text or "").splitlines()
    start = None
    for index, line in enumerate(lines):
        heading = line.strip()
        if heading.lower() == f"## {name}".lower():
            start = index + 1
            break
        if heading.lower().endswith(name.lower()) and heading.startswith("## "):
            rest = heading[3:].strip()
            number, _, title = rest.partition(".")
            if number.strip().isdigit() and title.strip().lower() == name.lower():
                start = index + 1
                break
    if start is None:
        return ""
    body = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        body.append(line)
    return "\n".join(body).strip()


def _words(text):
    return len(WORD.findall(text or ""))


def _direct(point):
    return list((point.get("support") or {}).get("points") or [])


def _leaves(point):
    found = []
    for child in _direct(point):
        if _direct(child):
            found.extend(_leaves(child))
        else:
            found.append({
                "id": child.get("id"),
                "name": child.get("name") or child.get("statement") or child.get("id"),
            })
    return found


def _leaf_count(point):
    return len(_leaves(point))


def own_problems(point, allow_single=False):
    """minto_check on this group only. mixed_kinds is the EV name heuristic."""
    kids = _direct(point)
    if not kids:
        return []
    support = point.get("support") or {}
    flat_points = []
    for child in kids:
        anchor = child.get("anchor") or ""
        if not anchor:
            anchor = f"group:{child.get('id')}" if _direct(child) else f"node:{child.get('id')}"
        flat_points.append({
            "id": child.get("id"),
            "anchor": anchor,
            "statement": child.get("statement") or "",
            "name": child.get("name") or child.get("statement") or "",
        })
    flat = {
        "basis": support.get("basis"),
        "order": support.get("order"),
        "rank_note": support.get("rank_note") or "",
        "points": flat_points,
    }
    found = [item for item in checker_problems({"key_line": flat}) if not item.startswith("mixed_kinds")]
    if allow_single:
        found = [
            item for item in found
            if not item.startswith("group_size") and not item.startswith("single_child")
        ]
    return found


def _is_further(point, further_ids):
    if point.get("id") in further_ids or point.get("further"):
        return True
    return (point.get("statement") or "").strip().lower() == "further"


def weak_points(point, further_ids, allow_single=False):
    """Groups to re-form. A weak parent is not also split into its children.

    One child group makes the parent a single child. The failure is in the
    child, so the child is the group that is re-formed.
    """
    problems = own_problems(point, allow_single=allow_single)
    size_only = bool(problems) and all(
        item.startswith("group_size") or item.startswith("single_child") for item in problems
    )
    kids = _direct(point)
    nested = [child for child in kids if _direct(child)]
    if _is_further(point, further_ids) or loosely_related(point) or (problems and not (size_only and len(nested) == 1 and len(kids) == 1)):
        return [point]
    found = []
    for child in kids:
        if _direct(child):
            found.extend(weak_points(child, further_ids, allow_single=False))
    return found


def statements_to_rewrite(point):
    """Review flags and fallback sentences, including the cell head."""
    found = []
    if _direct(point) and (point.get("review") or is_fallback_statement(point.get("statement") or "")):
        found.append(point)
    for child in _direct(point):
        if _direct(child):
            found.extend(statements_to_rewrite(child))
    return found


def further_ids(rows, cell):
    found = set()

    def walk(groups):
        for group in groups or []:
            if group.get("further") or (group.get("statement") or "").strip().lower() == "further":
                if group.get("id"):
                    found.add(group["id"])
            walk(group.get("children"))

    for row in rows:
        if row.get("cell") != cell:
            continue
        if row.get("part") == "batch":
            walk(row.get("groups"))
        point = row.get("point")
        if isinstance(point, dict):
            stack = [point]
            while stack:
                item = stack.pop()
                if _is_further(item, set()):
                    if item.get("id"):
                        found.add(item["id"])
                stack.extend(_direct(item))
    return found


def quality_done(rows):
    done = {"statement": set(), "reform": set(), "cell": set(), "field": False}
    for row in rows:
        if row.get("part") != "quality":
            continue
        kind = row.get("kind")
        if kind == "field" and row.get("status") == "done":
            done["field"] = True
        elif kind in ("statement", "reform", "cell") and row.get("id"):
            done[kind].add(row["id"])
    return done


def latest_placed(rows):
    found = {}
    order = []
    for row in rows:
        if row.get("part") == "cell" and row.get("status") == "placed" and row.get("point"):
            cell = row.get("cell") or row["point"].get("id")
            if cell not in found:
                order.append(cell)
            found[cell] = row
    return [(cell, found[cell]) for cell in order]


def last_cell_status(rows, cell):
    status = ""
    for row in rows:
        if row.get("part") == "cell" and row.get("cell") == cell:
            status = row.get("status") or ""
    return status


def _find(point, target):
    if point.get("id") == target:
        return point
    for child in _direct(point):
        found = _find(child, target)
        if found is not None:
            return found
    return None


def _splice(points, target, made):
    out = []
    for point in points:
        if point.get("id") == target:
            out.extend(made)
            continue
        if _direct(point):
            point = dict(point)
            support = dict(point.get("support") or {})
            support["points"] = _splice(support.get("points") or [], target, made)
            point["support"] = support
        out.append(point)
    return out


def _apply(cell_point, target, made):
    if cell_point.get("id") == target:
        point = copy.deepcopy(cell_point)
        support = dict(point.get("support") or {})
        support["points"] = made
        point["support"] = support
        return point
    point = copy.deepcopy(cell_point)
    support = dict(point.get("support") or {})
    support["points"] = _splice(support.get("points") or [], target, made)
    point["support"] = support
    return point


def _set_statement(point, target, text):
    if point.get("id") == target:
        point["statement"] = text
        point["name"] = text
        point.pop("review", None)
        return True
    for child in _direct(point):
        if _set_statement(child, target, text):
            return True
    return False


def _mark_review(point, target):
    if point.get("id") == target:
        point["review"] = True
        return True
    for child in _direct(point):
        if _mark_review(child, target):
            return True
    return False


def _acceptable(point, allow_single):
    problems = []

    def walk(node, single):
        problems.extend(own_problems(node, allow_single=single))
        for child in _direct(node):
            if _direct(child):
                walk(child, False)

    walk(point, allow_single)
    return not problems


def _reform_nodes(point):
    kids = _direct(point)
    if kids and all(_direct(child) for child in kids):
        return [{"id": child.get("id"), "name": child.get("statement") or child.get("id"), "_point": child} for child in kids]
    return _leaves(point)


def _made_points(groups, nodes):
    leaves = {node["id"]: node["name"] for node in nodes}
    made = [_to_point(group, leaves) for group in groups]
    nested = {node["id"]: node["_point"] for node in nodes if node.get("_point")}
    if not nested:
        return made
    for group in made:
        support = group.get("support") or {}
        support["points"] = [nested[child["id"]] for child in support.get("points") or [] if child.get("id") in nested]
        group["support"] = support
    return made


def _member_ids(point):
    return [node["id"] for node in _leaves(point)]


def missing_cells(jobs, rows):
    have = {row.get("cell") for row in rows if row.get("part") == "cell" and row.get("cell")}
    return [job["cell"] for job in jobs if job["cell"] not in have]


def plan_work(jobs, rows):
    """What this pass would ask, without calling a model."""
    done = quality_done(rows)
    blocked = []
    reform = []
    rewrite = []
    for job in jobs:
        cell = job["cell"]
        if last_cell_status(rows, cell) == "blocked" and cell not in done["cell"]:
            blocked.append(cell)
            continue
        placed = None
        for name, row in latest_placed(rows):
            if name == cell:
                placed = row.get("point")
        if not placed:
            continue
        single = _leaf_count(placed) < 4
        ids = further_ids(rows, cell)
        for point in weak_points(placed, ids, allow_single=single):
            if point.get("id") not in done["reform"]:
                reform.append(point.get("id"))
        for point in statements_to_rewrite(placed):
            if point.get("id") not in done["statement"]:
                rewrite.append(point.get("id"))
    return {
        "blocked": blocked,
        "reform": reform,
        "rewrite": rewrite,
        "field": not done["field"],
    }


def run(args, anthropic_post=None, root=None):
    """One finished field. anthropic_post stands in for the network in tests."""
    field = args.field
    root = Path(root) if root else ROOT
    path = log_path(root, field)
    rows = read_log(path)
    jobs = cell_jobs(field, root)
    missing = missing_cells(jobs, rows)
    work = plan_work(jobs, rows)
    if args.dry_run or missing:
        print(
            f"quality field={field} blocked={len(work['blocked'])} "
            f"reform={len(work['reform'])} rewrite={len(work['rewrite'])} "
            f"field-check={int(work['field'])} missing={len(missing)}",
            flush=True,
        )
        if missing:
            print("field is not finished; no model was called", flush=True)
        return {
            "field": field,
            "stopped": False,
            "cost": 0.0,
            "called": 0,
            "missing": missing,
            "work": work,
        }

    model = queue.resolve_model("anthropic", args.model or "")
    key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if anthropic_post is None and not key:
        raise SystemExit("ANTHROPIC_API_KEY is not set")
    ledger_path = queue.ledger_file(root)
    ledger = read_ledger(ledger_path)
    tracker = queue.CostTracker(
        model,
        float(args.max_cost),
        float(args.global_max_cost),
        float((ledger.get("fields") or {}).get(field) or 0),
        float(ledger.get("spent") or 0),
    )
    saved = [0.0]
    called = [0]
    stopped = False

    def _save():
        delta = tracker.usd() - saved[0]
        if delta > 0:
            add_spend(ledger_path, field, delta)
            saved[0] += delta

    def send(task, payload, schema=None, system=None):
        if schema is None:
            body = former.request_body(task, payload, model, "native")
            system_text = former.SYSTEM
        else:
            body = queue._schema_body(schema, "groups", system, payload, "native")
            body["model"] = model
            system_text = system
        reply = queue.anthropic_send(body, model, system_text, tracker, anthropic_post, key)
        called[0] += 1
        _save()
        parsed = former.parse_reply(queue.message_content(reply))
        if not parsed:
            return {"statement": "", "basis": "kinds", "order": "structure", "rank_note": "", "groups": []}
        return parsed

    def ask_for(job):
        def ask(task, payload, job=job):
            return send(task, {"cell": job["cell"], "principle": job["principle"], **payload})
        return ask

    jobs_by_cell = {job["cell"]: job for job in jobs}
    try:
        for job in jobs:
            cell = job["cell"]
            done = quality_done(read_log(path))
            if last_cell_status(read_log(path), cell) != "blocked" or cell in done["cell"]:
                continue
            outcome = form_cell(cell, job["nodes"], ask_for(job), known=job["nodes"])
            append_log(path, {
                "field": field,
                "part": "quality",
                "kind": "cell",
                "id": cell,
                "status": "done",
            })
            if outcome.get("status") == "placed" and outcome.get("point"):
                append_log(path, {
                    "field": field,
                    "cell": cell,
                    "part": "cell",
                    "status": "placed",
                    "reason": "",
                    "member_ids": outcome.get("member_ids") or _member_ids(outcome["point"]),
                    "point": outcome["point"],
                    "statement_review": outcome.get("statement_review") or [],
                })

        for cell, row in latest_placed(read_log(path)):
            job = jobs_by_cell.get(cell)
            if not job:
                continue
            point = copy.deepcopy(row["point"])
            single = _leaf_count(point) < 4
            done = quality_done(read_log(path))
            ids = further_ids(read_log(path), cell)
            changed = False
            targets = [item.get("id") for item in weak_points(point, ids, allow_single=single)]
            ident = _ident(cell, [point])
            pending = []
            for target in targets:
                if not target or target in done["reform"]:
                    continue
                current = _find(point, target)
                if current is None:
                    continue
                nodes = _reform_nodes(current)
                if len(nodes) < 2:
                    append_log(path, {"field": field, "part": "quality", "kind": "reform", "id": target, "status": "done"})
                    continue
                formed = form_batch(nodes, ask_for(job), ident)
                append_log(path, {"field": field, "part": "quality", "kind": "reform", "id": target, "status": "done"})
                if formed.get("status") != "placed" or not formed.get("groups"):
                    continue
                pending.append((target, _made_points(formed["groups"], nodes)))
            trial = point
            for target, made in pending:
                trial = _apply(trial, target, made)
            if pending and _acceptable(trial, single):
                point = trial
                changed = True
            done = quality_done(read_log(path))
            for item in statements_to_rewrite(point):
                target = item.get("id")
                if not target or target in done["statement"]:
                    continue
                reply = send("sentence", {
                    "cell": cell,
                    "principle": job["principle"],
                    "label": item.get("statement") or "",
                    "members": [
                        {"id": child.get("id"), "name": child.get("name") or child.get("statement") or child.get("id")}
                        for child in _direct(item)
                    ],
                })
                text = (reply.get("statement") or "").strip()
                append_log(path, {"field": field, "part": "quality", "kind": "statement", "id": target, "status": "done"})
                if is_definition(text) and not is_fallback_statement(text):
                    _set_statement(point, target, text)
                    changed = True
                else:
                    _mark_review(point, target)
                    changed = True
            if changed:
                append_log(path, {
                    "field": field,
                    "cell": cell,
                    "part": "cell",
                    "status": "placed",
                    "reason": "",
                    "member_ids": _member_ids(point),
                    "point": point,
                })

        done = quality_done(read_log(path))
        if not done["field"]:
            page = root / "pyramids" / f"{field}.md"
            text = page.read_text(encoding="utf-8") if page.exists() else ""
            governing = pyramid_section(text, "Governing thought")
            key_line = pyramid_section(text, "Key line")
            points = [row["point"] for _, row in latest_placed(read_log(path))]
            check = {
                "governing_thought": governing,
                "key_line": key_line,
                "holds": False,
                "note": "",
                "review": True,
            }
            if governing and key_line and points:
                reply = send("field", {
                    "task": "field",
                    "field": field,
                    "governing_thought": governing,
                    "key_line": key_line,
                    "cells": [{"id": point.get("id"), "statement": point.get("statement") or ""} for point in points],
                }, schema=FIELD_SCHEMA, system=FIELD_SYSTEM)
                note = " ".join((reply.get("note") or "").split())
                holds = bool(reply.get("holds"))
                check["holds"] = holds
                check["note"] = note
                check["review"] = (not holds) or (not note) or _words(note) > 25
            elif not governing or not key_line:
                check["note"] = "The pyramid file has no governing thought or no key line."
            append_log(path, {"field": field, "part": "quality", "kind": "field", "status": "done"})
            append_log(path, {"field": field, "part": "field", "check": check})
    except queue.CostCap:
        stopped = True
    rows = read_log(path)
    write_result(root, field, rows)
    cost = tracker.usd()
    _save()
    if stopped or tracker.stopped:
        stopped = True
        limit = float(args.global_max_cost) if tracker.stop_scope == "global" else float(args.max_cost)
        scope = tracker.stop_scope or "field"
        print(f"stopped at {scope} max-cost ${limit:.2f}", flush=True)
    print(f"quality field={field} called={called[0]} cost=${cost:.4f} stopped={stopped}", flush=True)
    return {
        "field": field,
        "stopped": stopped,
        "cost": cost,
        "called": called[0],
        "missing": [],
        "work": work,
    }


def main(argv=None):
    args = parse_args(argv)
    result = run(args, root=Path(args.root) if args.root else None)
    if args.dry_run:
        print("dry-run only; no model was called")
    return 0 if not result.get("stopped") else 0


if __name__ == "__main__":
    sys.exit(main())
