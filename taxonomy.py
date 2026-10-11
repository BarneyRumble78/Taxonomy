"""Taxonomy command line (v3).

  python3 taxonomy.py frame   "problem in plain words"
  python3 taxonomy.py survey  "subject or problem"            [--fields MA,PH,LA]
  python3 taxonomy.py consult "problem" --field MA            [--deepen 3]
  python3 taxonomy.py connect "problem" --field MA            [--top 8]
  python3 taxonomy.py check   "a single claim"                (v2 classifier)

Backend: set TAXONOMY_LLM=anthropic|ollama|manual (see engine/v3/llm.py).
Results print as JSON and are saved in runs/.
"""
import argparse, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "engine" / "v3"))
sys.path.insert(0, str(ROOT / "engine"))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", choices=["frame", "survey", "consult", "connect", "check"])
    ap.add_argument("text")
    ap.add_argument("--field", default="MA")
    ap.add_argument("--fields")
    ap.add_argument("--deepen", type=int, default=3)
    ap.add_argument("--top", type=int, default=8)
    ap.add_argument("--llm")
    a = ap.parse_args()
    if a.mode == "check":
        import taxonomy_engine as te
        print(json.dumps(te.classify(a.text), indent=1, ensure_ascii=False))
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
