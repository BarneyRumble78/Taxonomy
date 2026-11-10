"""Transfer operator: carry a formal core into a field that does not bind it.

Two stages.

brief(core, field)   No model. States what a transfer would have to show:
                     which sources to learn from (most distant first), a
                     question for every role, a check for every assumption,
                     and the guarantee that follows only if all checks pass.

fill(brief, llm)     A model proposes answers. The proposal is validated and
                     always marked generated-unverified. A malformed answer is
                     an error, never a silent empty result.

The mismatches are the product. Each one is either a reason the transfer
fails or a place where something new would be needed.

    python3 taxonomy.py transfer RC-branching-threshold EC
    python3 taxonomy.py transfer RC-branching-threshold EC --fill --out run.json
"""
import argparse
import hashlib
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rosetta  # noqa: E402
from crosslinks import FIELDS  # noqa: E402
from rosetta import ROOT, RosettaError  # noqa: E402

MET = ("y", "~", "n", "?")
KNOWN = ("yes", "no", "unsure")


def field_card(field, root=ROOT):
    """The field's own lens card: its name and the question it asks."""
    path = Path(root) / "cards" / "lens" / f"{field}.json"
    try:
        cards = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise RosettaError(f"no lens card for {field}: {error}") from error
    for card in cards:
        if card.get("id") == field:
            return {"name": card["name"], "question": card["question"]}
    raise RosettaError(f"cards/lens/{field}.json has no field-level card")


def brief(core, field, graph, root=ROOT):
    """What a transfer of this core into this field would have to show."""
    if field not in FIELDS:
        raise RosettaError(f"unknown field {field}")
    if field == "MA":
        raise RosettaError("mathematics owns the cores; it is not a transfer target")
    if rosetta.bindings_in(core, field):
        raise RosettaError(f"{core['id']} is already bound in {field}; use translate")
    card = field_card(field, root)
    sources = []
    for binding in core["bindings"]:
        sources.append({
            "field": binding["field"], "cell": binding["cell"], "tool": binding["tool"],
            "maturity": binding["maturity"], "roles": binding["roles"],
            "assumptions_met": binding["assumptions_met"], "breaks": binding["breaks"],
            "lineage_distance": graph.distance(binding["cell"], field)})
    sources.sort(key=lambda s: (-s["lineage_distance"], s["field"], s["tool"]))
    return {
        "kind": "transfer-brief", "core": core["id"], "name": core["name"],
        "structure": core["structure"], "ma_node": core["ma_node"],
        "target": {"field": field, "name": card["name"], "question": card["question"]},
        "provisional": field == "IK",
        "sources": sources,
        "roles": [{"role": role, "meaning": meaning,
                   "question": f"In {card['name']}, what plays the role of '{role}' ({meaning})?"}
                  for role, meaning in core["roles"].items()],
        "assumptions": [{"id": a["id"], "text": a["text"],
                         "question": f"In {card['name']}, does this hold? {a['text']}"}
                        for a in core["assumptions"]],
        "guarantee": core["guarantee"],
        "status": "open question",
    }


def prompt_for(doc):
    """The model prompt. It contains the brief and nothing from bench/."""
    lines = [
        "You test whether one mathematical structure can be carried into a field that has not used it.",
        "Be sceptical. A transfer that fails is a useful answer. Do not invent citations.",
        "",
        f"STRUCTURE: {doc['name']}. {doc['structure']}",
        f"GUARANTEE if every assumption holds: {doc['guarantee']}",
        "",
        f"TARGET FIELD: {doc['target']['name']}. Its question: {doc['target']['question']}",
        "",
        "HOW OTHER FIELDS USE IT:",
    ]
    for source in doc["sources"]:
        roles = "; ".join(f"{role} = {value}" for role, value in source["roles"].items())
        lines.append(f"- {source['field']}: {source['tool']}. {roles}. Breaks: {' '.join(source['breaks'])}")
    lines += ["", "ROLES TO FILL:"]
    lines += [f"- {item['role']}: {item['meaning']}" for item in doc["roles"]]
    lines += ["", "ASSUMPTIONS TO CHECK:"]
    lines += [f"- {item['id']}: {item['text']}" for item in doc["assumptions"]]
    role_keys = ", ".join(f'"{item["role"]}": "what plays it, or null"' for item in doc["roles"])
    assumption_keys = ", ".join(
        f'"{item["id"]}": {{"met": "y|~|n|?", "reason": "one sentence"}}' for item in doc["assumptions"])
    lines += [
        "", "Reply with JSON only, in this shape:",
        "{",
        f' "roles": {{{role_keys}}},',
        f' "assumptions": {{{assumption_keys}}},',
        ' "candidate_tool": "a short name for the technique in the target field",',
        ' "mismatches": ["each place the analogy fails in the target field"],',
        ' "ideas": ["each new question or method the mismatches suggest"],',
        ' "already_known": "yes|no|unsure",',
        ' "already_known_note": "what you believe exists already, without citations"',
        "}",
        "met codes: y = normally holds, ~ = approximately, n = normally violated, ? = not known.",
    ]
    return "\n".join(lines)


def validate_proposal(doc, answer):
    """Problems with a model's answer. An empty list means it is well formed."""
    if not isinstance(answer, dict):
        return ["the answer is not a JSON object"]
    problems = []
    roles = answer.get("roles")
    wanted = {item["role"] for item in doc["roles"]}
    if not isinstance(roles, dict) or set(roles) != wanted:
        problems.append(f"roles must have exactly the keys: {', '.join(sorted(wanted))}")
    elif not all(value is None or (isinstance(value, str) and value.strip()) for value in roles.values()):
        problems.append("each role must be a non-empty string or null")
    assumptions = answer.get("assumptions")
    wanted = {item["id"] for item in doc["assumptions"]}
    if not isinstance(assumptions, dict) or set(assumptions) != wanted:
        problems.append(f"assumptions must have exactly the keys: {', '.join(sorted(wanted))}")
    else:
        for key, value in assumptions.items():
            if not isinstance(value, dict) or value.get("met") not in MET:
                problems.append(f"assumption {key}: met must be one of {', '.join(MET)}")
            elif not isinstance(value.get("reason"), str) or not value["reason"].strip():
                problems.append(f"assumption {key}: a reason is required")
    for key in ("mismatches", "ideas"):
        value = answer.get(key)
        if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
            problems.append(f"{key} must be a list of non-empty strings")
    if not answer.get("mismatches"):
        problems.append("at least one mismatch is required: no analogy is perfect")
    if answer.get("already_known") not in KNOWN:
        problems.append(f"already_known must be one of {', '.join(KNOWN)}")
    if not isinstance(answer.get("candidate_tool"), str) or not answer["candidate_tool"].strip():
        problems.append("candidate_tool must be a non-empty string")
    return problems


def fill(doc, llm, model_name="unknown", max_tokens=1500):
    """Ask a model to attempt the transfer. Returns a run record."""
    prompt = prompt_for(doc)
    answer = llm(prompt, max_tokens=max_tokens)
    problems = validate_proposal(doc, answer)
    if problems:
        raise RosettaError("the model's answer was rejected: " + "; ".join(problems))
    met = {key: value["met"] for key, value in answer["assumptions"].items()}
    unfilled = [role for role, value in answer["roles"].items() if value is None]
    return {
        "kind": "transfer-run", "core": doc["core"], "name": doc["name"], "ma_node": doc["ma_node"],
        "target": doc["target"], "provisional": doc["provisional"],
        "proposal": {
            "candidate_tool": answer["candidate_tool"].strip(),
            "roles": answer["roles"], "assumptions": answer["assumptions"],
            "mismatches": answer["mismatches"], "ideas": answer["ideas"],
            "already_known": answer["already_known"],
            "already_known_note": str(answer.get("already_known_note") or "")},
        "guarantee": doc["guarantee"],
        "guarantee_carries": not unfilled and all(code == "y" for code in met.values()),
        "unfilled_roles": unfilled,
        "status": "generated-unverified",
        "provenance": {
            "sources": [{"field": s["field"], "cell": s["cell"], "tool": s["tool"],
                         "lineage_distance": s["lineage_distance"]} for s in doc["sources"]],
            "model": model_name, "date": date.today().isoformat(),
            "prompt_sha1": hashlib.sha1(prompt.encode("utf-8")).hexdigest(),
            "conditions_checked_by": "model only",
            "note": "A model's proposal. No source was consulted and no person has checked it."},
    }


def main(argv=None):
    parser = argparse.ArgumentParser(prog="transfer", description=__doc__.split("\n")[0])
    parser.add_argument("core")
    parser.add_argument("field")
    parser.add_argument("--fill", action="store_true", help="ask the local model to attempt the transfer")
    parser.add_argument("--out", help="write the record to this file as well")
    args = parser.parse_args(argv)
    try:
        cores = rosetta.load()
        doc = brief(rosetta.core_by_id(cores, args.core), args.field, rosetta.Graph(cores=cores))
        if args.fill:
            from llm import LLMError, get_llm
            llm = get_llm()
            try:
                doc = fill(doc, llm, model_name=getattr(llm, "model", type(llm).__name__))
            except LLMError as error:
                raise RosettaError(f"model call failed: {error}") from error
    except RosettaError as error:
        print(f"transfer: {error}", file=sys.stderr)
        return 2
    text = json.dumps(doc, indent=1, ensure_ascii=False)
    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
