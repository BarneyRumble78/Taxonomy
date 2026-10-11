"""Taxonomy command line (v3).

  python3 taxonomy.py frame   "problem in plain words"
  python3 taxonomy.py survey  "subject or problem"            [--fields MA,PH,LA]
  python3 taxonomy.py consult "problem" --field MA            [--deepen 3]
  python3 taxonomy.py connect "problem" --field MA            [--top 8]
  python3 taxonomy.py check   "a single claim"                (v2 classifier)

Backend: TAXONOMY_LLM=ollama (default, local) | manual | anthropic.
Anthropic also needs TAXONOMY_ADJUDICATE_PAID=1 (see engine/v3/llm.py).
check uses the same adjudicator switch as the engine: a model runs only when
TAXONOMY_ADJUDICATE=1, and the default chain is local. Paid models still need
TAXONOMY_ADJUDICATE_PAID=1. survey, consult and connect save a run record in runs/.
A failed run is saved before the error is reported, and the message is one line plus that path.
"""
import argparse, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "engine" / "v3"))
sys.path.insert(0, str(ROOT / "engine"))

# Queue reasons are the ones a reviewer would see. The phrase is the public line.
_REVIEW = {"low_confidence", "stages_disagree", "no_cue"}
_OTHER = {
    "instruction": "This reads as an instruction, not a claim.",
    "multi_sentence": "These sentences do not share one owner.",
}


def abstain_line(reason):
    if reason in _OTHER:
        return _OTHER[reason]
    return "unsure, sent to review"


def main(argv=None):
    try:
        _main(argv)
    except SystemExit:
        raise
    except Exception as exc:
        line = str(exc).strip().splitlines()[0] if str(exc).strip() else exc.__class__.__name__
        path = getattr(exc, "path", None)
        print(f"{line} ({path})" if path else line, file=sys.stderr)
        sys.exit(1)


def _main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", choices=["frame", "survey", "consult", "connect", "check"])
    ap.add_argument("text")
    ap.add_argument("--field", default="MA")
    ap.add_argument("--fields")
    ap.add_argument("--deepen", type=int, default=3)
    ap.add_argument("--top", type=int, default=8)
    ap.add_argument("--llm")
    a = ap.parse_args(argv)
    if a.mode == "check":
        import taxonomy_engine as te
        # None follows TAXONOMY_ADJUDICATE. Off, the default, calls no model.
        detail = te.place_detail(a.text)
        placed = detail.get("placement")
        if not placed:
            print(abstain_line(detail.get("reason")))
            return
        print(json.dumps(placed, indent=1, ensure_ascii=False))
        return
    import core
    from llm import get_llm
    llm = get_llm(a.llm)
    if a.mode == "frame":
        out = core.frame(a.text, llm)
    elif a.mode == "survey":
        out = core.survey(a.text, llm, fields=a.fields.split(",") if a.fields else None)
    elif a.mode == "consult":
        out = core.consult(a.text, a.field, llm, deepen=a.deepen)
    else:
        out = core.connect_run(a.text, a.field, llm, top=a.top)
    print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
