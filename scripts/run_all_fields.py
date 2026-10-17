#!/usr/bin/env python3
"""Run the budget plan in order. No model call unless --execute is set.

    python3 scripts/run_all_fields.py
    python3 scripts/run_all_fields.py --write-plan
    python3 scripts/run_all_fields.py --execute --fields MA,PH,CH,CS,MD
    python3 scripts/run_all_fields.py --execute --fields AG,AR,BI,BU,DE,EA,EC,ED,EN,HI,IK,IS,LA,LN,MS,PL,PO,RE,ST

The default is a dry run. It prints the plan and does not call Ollama or
Claude. --write-plan refreshes pyramids/rebuild/BUDGET_PLAN.md from the maps.
--execute resumes from pyramids/queues/all_fields_state.json. A field with
Minto items is sent to the group former. Claude fields use Anthropic and
the field cap. Qwen fields use Ollama with the field cap off. The cell
placer is not used for that work. A stopped run leaves the field unfinished
so the next run continues it. --fields limits the run to those ids.
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine" / "v3"))
from budget import build_plan, load_plan, render_markdown, write_plan


def state_path(root):
    return Path(root) / "pyramids" / "queues" / "all_fields_state.json"


def load_state(root):
    path = state_path(root)
    if not path.exists():
        return {"done": [], "stopped": None}
    data = json.loads(path.read_text(encoding="utf-8"))
    data.setdefault("done", [])
    data.setdefault("stopped", None)
    return data


def save_state(root, state):
    path = state_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def _load_script(root, filename, module_name):
    import importlib.util

    path = Path(root) / "scripts" / filename
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def group_command(entry):
    """Argv for the group former. Claude uses the field cap. Qwen leaves it off."""
    claude = entry.get("mode") == "claude" and float(entry.get("cap") or 0) > 0
    backend = "anthropic" if claude else "ollama"
    cap = f"{float(entry['cap']):.2f}" if claude else "0"
    return [
        "--field", entry["id"],
        "--backend", backend,
        "--max-cost", cap,
        "--global-max-cost", "60",
    ]


def _queue_runner(entry, root):
    """Place one cell queue under its cap. Imported only when a run is executing."""
    if entry["id"] == "MESH":
        raise SystemExit("The MeSH queue is one shared list. Resolve it before any model.")
    module = _load_script(root, "run_pyramid_queue.py", "run_pyramid_queue")
    backend = "hybrid" if entry["mode"] == "claude" and entry["cap"] > 0 else "ollama"
    args = module.parse_args([
        "--field", entry["id"],
        "--backend", backend,
        "--max-cost", str(entry["cap"] if backend == "hybrid" else 0),
        "--global-max-cost", "60",
    ])
    return module.run(args, root=root)


def _group_runner(entry, root):
    """Form Minto groups for one field. Imported only when a run is executing."""
    if entry["id"] == "MESH":
        raise SystemExit("The MeSH queue is one shared list. Resolve it before any model.")
    module = _load_script(root, "run_group_former.py", "run_group_former")
    args = module.parse_args(group_command(entry))
    return module.run(args, root=root)


def _apply_outcome(entry, outcome, root, state, summary, row, spent):
    """Record a model step. A stop leaves the field out of done."""
    cost = float(outcome.get("cost") or 0)
    spent = round(spent + cost, 6)
    row["cost"] = cost
    row["wrote"] = outcome.get("wrote")
    if outcome.get("stopped"):
        row["result"] = "stopped"
        state["stopped"] = entry["id"]
        save_state(root, state)
        summary.append(row)
        return spent, True
    row["result"] = "ran"
    state["done"].append(entry["id"])
    state["stopped"] = None
    save_state(root, state)
    summary.append(row)
    return spent, False


def run_all(root, plan=None, execute=False, queue_run=None, group_run=None, refresh=False, fields=None):
    """Walk the plan. A dry run does not write state and does not call a model."""
    root = Path(root)
    plan_path = root / "pyramids" / "rebuild" / "budget_plan.json"
    if plan is None:
        if refresh or not plan_path.exists():
            plan = build_plan(root)
        else:
            plan = load_plan(root)
    wanted = None
    if fields:
        wanted = {item.strip() for item in fields if str(item).strip()}
    state = load_state(root)
    summary = []
    spent = 0.0
    stopped = False
    for entry in plan["order"]:
        if wanted is not None and entry["id"] not in wanted:
            continue
        row = {
            "id": entry["id"],
            "mode": entry["mode"],
            "model": entry["model"],
            "cap": entry["cap"],
            "estimate_usd": entry["estimate_usd"],
        }
        if entry["id"] in state["done"]:
            row["result"] = "resume"
            summary.append(row)
            continue
        if entry.get("minto_items"):
            if not execute:
                row["result"] = "minto-pending"
                summary.append(row)
                continue
            outcome = (group_run or _group_runner)(entry, root)
            spent, stopped = _apply_outcome(entry, outcome, root, state, summary, row, spent)
            if stopped:
                break
            continue
        if not entry["model"]:
            row["result"] = "no-model"
            if execute:
                state["done"].append(entry["id"])
                state["stopped"] = None
                save_state(root, state)
            summary.append(row)
            continue
        if not execute:
            row["result"] = "dry-run"
            summary.append(row)
            continue
        outcome = (queue_run or _queue_runner)(entry, root)
        spent, stopped = _apply_outcome(entry, outcome, root, state, summary, row, spent)
        if stopped:
            break
    return {
        "execute": execute,
        "stopped": stopped,
        "spent": spent,
        "assigned": plan["assigned"],
        "global_cap": plan["global_cap"],
        "reserve": plan["reserve"],
        "steps": summary,
    }


def format_summary(result):
    lines = []
    for row in result["steps"]:
        extra = f" cost={row['cost']:.4f}" if "cost" in row else ""
        lines.append(
            f"{row['id']} mode={row['mode']} model={row['model']} "
            f"cap={row['cap']:.2f} result={row['result']}{extra}"
        )
    lines.append(
        f"steps={len(result['steps'])} spent={result['spent']:.4f} "
        f"assigned={result['assigned']:.2f} global_cap={result['global_cap']:.2f} "
        f"reserve={result['reserve']:.2f} stopped={result['stopped']}"
    )
    return "\n".join(lines)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Run the field plan in order, without a model unless asked.")
    parser.add_argument("--execute", action="store_true", help="Call the group former or the cell queue. The default is a dry run.")
    parser.add_argument("--fields", default="", help="Comma-separated ids. Omit to walk the whole plan.")
    parser.add_argument("--write-plan", action="store_true", help="Rebuild the budget files from the maps. No model call.")
    parser.add_argument("--refresh", action="store_true", help="Recompute the plan before this run.")
    parser.add_argument("--root", default="", help="Repository root. Tests pass a temporary directory.")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    root = Path(args.root) if args.root else ROOT
    if args.write_plan:
        plan = write_plan(root)
        print(render_markdown(plan))
        print(f"wrote {root / 'pyramids' / 'rebuild' / 'BUDGET_PLAN.md'}")
        return 0
    fields = [item.strip() for item in args.fields.split(",") if item.strip()]
    result = run_all(root, execute=args.execute, refresh=args.refresh, fields=fields or None)
    print(format_summary(result))
    if not args.execute:
        print("dry-run only; no model was called")
    return 0


if __name__ == "__main__":
    sys.exit(main())
