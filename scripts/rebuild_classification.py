#!/usr/bin/env python3
"""Rebuild a field classification from its rule file. No model calls.

    python3 scripts/rebuild_classification.py --field MA --dry-run
    python3 scripts/rebuild_classification.py --field MA --write
    python3 scripts/rebuild_classification.py --shared MD,BI,CH,MS,AG --write

The dry run is the default. It files shelf numbers and deep thesaurus levels
under their parent and prints how many tops would still need a model.
--write stores that count in pyramids/queues/<FIELD>.cap.json. It does not
write the pyramid, and it does not call a model.

EV keeps its leaf rebuild in scripts/rebuild_ev_classification.py. This
script will not overwrite pyramids/EV.json.

Indigenous topics are routed by pyramids/rebuild/ANZSRC45.json.
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine" / "v3"))
from cost_cap import FIELD_BUDGET, GLOBAL_BUDGET
from crosslinks import check as cross_check
from field_rebuild import prepare, shared_queue

PYRAMID = {
    "EV": ROOT / "pyramids" / "EV.json",
}


def _print_report(report):
    hybrid = report["hybrid"]
    print(
        f"field={report['field']} nodes={report['nodes']} ruled={report['ruled']} "
        f"filed={report['filed']} kept_override={report['kept_override']} "
        f"routed={report['routed']} unanchored={report['unanchored']} "
        f"model={report['model']} tops={report['tops']} depth_cap={report['depth_cap']}"
    )
    print(
        f"hybrid ollama_items={hybrid['ollama_items']} escalate_items={hybrid['escalate_items']} "
        f"claude_usd={hybrid['claude_usd']:.6f} "
        f"upper_if_all_model_items={hybrid['upper_if_all_model_items']:.6f} "
        f"upper_if_all_tops_escalated={report['upper_if_all_tops_escalated']:.6f} "
        f"upper_if_cap_not_applied={report['upper_if_cap_not_applied']:.6f} "
        f"field_max_cost={FIELD_BUDGET:.2f} global_max_cost={GLOBAL_BUDGET:.2f}"
    )
    print(report["note"])
    for name, counts in sorted((report.get("by_map") or {}).items()):
        print(f"map {name} {json.dumps(counts, sort_keys=True)}")


def _print_links(root):
    found = cross_check(root)
    print(f"crosslinks dangling={len(found['dangling'])} route_problems={len(found['routes'])}")
    for item in found["dangling"]:
        print(f"dangling {item}")
    for item in found["routes"]:
        print(f"route {item}")
    return found


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="File a field's map nodes without a model.")
    parser.add_argument("--field", default="", help="Field code, for example MA.")
    parser.add_argument("--dry-run", action="store_true", help="Print counts and do not write. This is the default.")
    parser.add_argument("--write", action="store_true", help="Write pyramids/queues/<FIELD>.cap.json. Never writes the pyramid.")
    parser.add_argument("--shared", default="", help="Comma-separated fields whose MeSH terms share one queue.")
    parser.add_argument("--root", default="", help="Repository root. Tests pass a temporary directory.")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    root = Path(args.root) if args.root else ROOT
    wrote = False
    if args.field == "EV":
        print("EV leaf groups stay in scripts/rebuild_ev_classification.py. pyramids/EV.json is not written.")
        return 0
    if args.field:
        report = prepare(args.field, root)
        _print_report(report)
        if args.write:
            dest = root / "pyramids" / "queues" / f"{args.field}.cap.json"
            dest.parent.mkdir(parents=True, exist_ok=True)
            payload = {key: value for key, value in report.items() if key != "rows"}
            dest.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            print(f"wrote {dest}")
            wrote = True
            if dest.resolve() == PYRAMID.get("EV", Path("/none")).resolve():
                raise SystemExit("refusing to overwrite pyramids/EV.json")
    if args.shared:
        fields = [part.strip() for part in args.shared.split(",") if part.strip()]
        summary = shared_queue(fields, root, include_rows=False)
        print(
            f"shared fields={','.join(fields)} descriptors={summary['descriptor_rows']} "
            f"tree_copies={summary['tree_copies']} shared={summary['shared_descriptors']} "
            f"agreed={summary['agreed']} conflicts={summary['conflicts']} "
            f"cross_field_conflicts={summary['cross_field_conflicts']}"
        )
        if args.write:
            dest = root / "pyramids" / "queues" / "shared_mesh.json"
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            print(f"wrote {dest}")
            wrote = True
    if args.field or args.shared:
        found = _print_links(root)
        if found["dangling"] or found["routes"]:
            return 1
    elif not args.field:
        print("Pass --field MA or --shared MD,BI.")
        return 2
    if not args.write and args.field:
        print("dry-run only; no pyramid and no queue file written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
