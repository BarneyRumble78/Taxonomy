"""Export the abstention queue, or replay a Workers AI run and print the report.

The live model is not called from here. A run file is a cache of samples.
No provider is configured in CI, so the locked gates stay on the rule cascade.
"""
import csv, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "engine"))
import taxonomy_engine as te
from adjudicator import N_SAMPLES, message_id

# Published 9 Oct 2026. https://developers.cloudflare.com/workers-ai/platform/pricing/
# Billing is $0.011 per 1,000 neurons, including a free 10,000 neurons per day.
NEURON_USD_PER_THOUSAND = 0.011
BGE_USD_PER_M = 0.020
# Equivalents for @cf/meta/llama-3.1-8b-instruct-fp8, used only as a cross-check
# when the routed model is that id. Measured neurons are the bill.
FP8_IN_PER_M = 0.152
FP8_OUT_PER_M = 0.287
FROZEN = ROOT / "pilot" / "heldout.tsv"
HARD = {"MA", "PH", "CH", "BI", "EA", "MD", "EN", "CS"}
GEO = [
    ("Russian forces control Zarichne.", "PO"),
    ("Ukrainian units hold the village of Robotyne.", "PO"),
    ("The ceasefire line runs north of the river.", "PO"),
    ("China conducted drills in the waters around Taiwan.", "PO"),
    ("NATO members agreed to raise defence spending.", "PO"),
    ("The Security Council did not adopt the resolution.", "PO"),
    ("Israeli aircraft struck sites in Beirut.", "ST"),
    ("The Rafah crossing remained closed to civilians.", "PO"),
    ("North Korea launched a ballistic missile over the sea.", "PO"),
    ("Sudanese forces took the city of Wad Madani.", "PO"),
    ("The United States imposed sanctions on the oil trader.", "PO"),
    ("Peacekeepers deployed into the buffer zone.", "PO"),
    ("The occupied oblast is administered by the military.", "PO"),
]


def rows():
    return list(csv.DictReader(FROZEN.open(encoding="utf-8"), delimiter="\t"))


def export_jobs(path):
    table = rows()
    claims = [r["claim"] for r in table]
    groups = {"frozen": claims}
    groups["physics"] = ["A photon carries quantum energy. " + c for c in claims]
    groups["law"] = [c + " under the Goods and Services Tax Act 1985." for c in claims]
    groups["math"] = ["The theorem has a proof. " + c for c in claims]
    groups["geo"] = [text for text, _ in GEO]
    jobs = []
    for name, texts in groups.items():
        for job in te.adjudication_jobs(texts):
            job["set"] = name
            if name == "frozen":
                job["gold_id"] = table[job["index"]]["id"]
            jobs.append(job)
    path.write_text(json.dumps(jobs, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {path} jobs={len(jobs)} calls={len(jobs) * N_SAMPLES}")
    return jobs


class Replay:
    def __init__(self, items):
        self.by_id = {}
        for item in items:
            self.by_id[item["id"]] = {
                "samples": item["samples"],
                "usage": item.get("usage") or [],
                "i": 0,
            }
        self.missing = []

    def __call__(self, messages):
        key = message_id(messages)
        rec = self.by_id.get(key)
        if rec is None:
            self.missing.append(key)
            return "", {}
        i = rec["i"]
        rec["i"] += 1
        usage = rec["usage"][i] if i < len(rec["usage"]) else {}
        return rec["samples"][i], usage


def _print_block(title, report):
    n, answered = report["n"], report["answered_n"]
    print(f"\n{title}")
    print(f"n {n} answered {answered} abstain {report['abstain']} ({report['abstain'] / n:.1%})")
    print("reasons " + " ".join(f"{k}={v}" for k, v in sorted(report["reasons"].items())))
    for k in ("owner", "cell", "warrant", "method"):
        h, ans = report["headline_counts"][k], report["answered_counts"][k]
        rate = ans / answered if answered else 0
        print(f"  {k:8s} headline {h}/{n} ({report['headline'][k]:.1%})  answered {ans}/{answered} ({rate:.1%})")
    print(
        f"  warrant vs gold, default included: {report['headline_counts']['warrant']}/{n}"
        f"  default_applied {report['default_applied']}/{answered} answered,"
        f" {report['default_applied_matches']} of those match gold"
        f"  cue or agreed warrant {report['cue_warrant_matches']}/{report['cue_warrant_n']}"
    )


def _usage(items):
    prompt = completion = neurons = calls = 0
    models = {}
    for item in items:
        for u in item.get("usage") or []:
            calls += 1
            prompt += int(u.get("prompt_tokens") or 0)
            completion += int(u.get("completion_tokens") or 0)
            neurons += float(u.get("neurons") or 0)
            if u.get("model"):
                models[u["model"]] = models.get(u["model"], 0) + 1
    return {"calls": calls, "prompt_tokens": prompt, "completion_tokens": completion, "neurons": neurons, "models": models}


def _cost(neurons, n_claims):
    usd = neurons * NEURON_USD_PER_THOUSAND / 1000
    per_1000 = usd / n_claims * 1000 if n_claims else 0
    return usd, per_1000


def report(run_path):
    run = json.loads(Path(run_path).read_text(encoding="utf-8"))
    items = run["items"]
    table = rows()
    frozen_items = [i for i in items if i.get("set") == "frozen"]
    replay = Replay(frozen_items)
    frozen = te.evaluate(FROZEN, adjudicator=replay)
    if replay.missing:
        raise SystemExit(f"run file does not match the current prompts ({len(replay.missing)} missing)")
    bare = te.evaluate(FROZEN, adjudicator=False)
    _print_block("No model (rules and retrieval only)", bare)
    _print_block("With the adjudicator on the queue", frozen)
    print("\nDistractors, model on the queue (abstain or gold owner is the pass)")
    claims = [r["claim"] for r in table]
    variants = {
        "physics": ["A photon carries quantum energy. " + c for c in claims],
        "law": [c + " under the Goods and Services Tax Act 1985." for c in claims],
        "math": ["The theorem has a proof. " + c for c in claims],
    }
    for name, texts in variants.items():
        player = Replay([i for i in items if i.get("set") == name])
        wrong = []
        placed = 0
        for r, d in zip(table, te.place_many(texts, adjudicator=player)):
            p = d.get("placement")
            if p:
                placed += 1
            if p and p["owner"] != r["owner"]:
                wrong.append((r["id"], p["owner"], r["owner"]))
        print(f"  {name}: placed {placed}/{len(texts)}  gold-owner misses {len(wrong)}")
        if player.missing:
            print(f"  {name}: missing samples {len(player.missing)}")
        for row in wrong[:8]:
            print(f"    {row}")
    print("\nGeopolitics probe")
    geo_replay = Replay([i for i in items if i.get("set") == "geo"])
    for (text, preferred), d in zip(GEO, te.place_many([t for t, _ in GEO], adjudicator=geo_replay)):
        p = d.get("placement")
        owner = p["owner"] if p else None
        flag = ""
        if owner in HARD:
            flag = " HARD-SCIENCE"
        elif owner not in (None, preferred, "ST"):
            flag = " OFF-LIST"
        print(f"  {owner or 'abstain':8s} preferred {preferred:2s}{flag}  {text}")
    if geo_replay.missing:
        print(f"  missing samples {len(geo_replay.missing)}")
    frozen_usage = _usage(frozen_items)
    probe_usage = _usage([i for i in items if i.get("set") != "frozen"])
    embed = run.get("embed") or {}
    n = len(table)
    llm_usd, llm_per = _cost(frozen_usage["neurons"], n)
    embed_neurons = embed.get("neurons")
    if embed_neurons is None:
        embed_neurons = float(embed.get("neurons_from_token_table") or 0)
    embed_usd, embed_per = _cost(embed_neurons, n)
    print("\nCost (estimate from measured neurons, $0.011 per 1,000 neurons)")
    print(f"  requested {run.get('requested_model')}  routed {frozen_usage['models']}")
    print(
        f"  frozen llm calls {frozen_usage['calls']}  prompt_tokens {frozen_usage['prompt_tokens']}"
        f"  completion_tokens {frozen_usage['completion_tokens']}  neurons {frozen_usage['neurons']:.3f}"
    )
    print(f"  frozen llm on these {n} claims ${llm_usd:.4f}  per 1,000 claims ${llm_per:.4f}")
    if frozen_usage["prompt_tokens"]:
        cross = (frozen_usage["prompt_tokens"] * FP8_IN_PER_M + frozen_usage["completion_tokens"] * FP8_OUT_PER_M) / 1_000_000
        print(f"  fp8 token-table cross-check ${cross:.4f} on these {n} claims (published $0.152 / $0.287 per million)")
    print(
        f"  probe calls outside the frozen set {probe_usage['calls']}  neurons {probe_usage['neurons']:.3f}"
        f"  (distractors and the geopolitics list; not in the per-claim figure)"
    )
    print(f"  embed neurons {embed_neurons:.3f}  tokens {embed.get('prompt_tokens')}  claims {embed.get('claims')}  per 1,000 claims ${embed_per:.4f}")
    print(f"  combined per 1,000 claims ${llm_per + embed_per:.4f}")
    print("  Published price: https://developers.cloudflare.com/workers-ai/platform/pricing/ (checked 10 Oct 2026).")
    print("  Free allocation is 10,000 neurons per day, so a short run can sit inside that allotment.")
    print(f"  Embedding list price is ${BGE_USD_PER_M:.3f} per million input tokens for bge-small.")
    print(f"  frozen queue items {len(frozen_items)}/{n}  samples {N_SAMPLES}")


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "--export":
        export_jobs(Path(sys.argv[2]))
    elif len(sys.argv) >= 3 and sys.argv[1] == "--run":
        report(sys.argv[2])
    else:
        raise SystemExit("usage: report_adjudication.py --export jobs.json | --run run.json")
