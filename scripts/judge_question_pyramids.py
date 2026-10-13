"""Sonnet judges the 3 test question pyramids. Hard cap $1.00 for the whole run."""
import json,sys,os
from pathlib import Path
R=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(R/"scripts"))
import run_pyramid_queue as q
MODEL="claude-sonnet-5-5"; IN,OUT=2.0,10.0; CAP=1.00; MAXTOK=4000
SYS=("You are a strict reviewer of Minto question pyramids. Score each criterion pass/fail with a one-sentence reason. "
"Criteria: (1) governing_thought directly answers the question in one sentence; (2) introduction is a true Situation-Complication-Question leading to that question; "
"(3) key line has 2-5 points of one kind, MECE on the stated dimension, in the stated order; (4) each point supports the governing thought (summarises upward); "
"(5) each linked_node is a plausible classification home for its point given the node statements supplied; (6) factual claims are correct AND supported: since no sources are cited, list any claim you think is wrong or doubtful. "
"Be strict; unsupported claims are a fail on (6) unless they are textbook-standard. Give overall verdict pass only if all criteria pass.")
schema={"type":"object","properties":{"criteria":{"type":"array","items":{"type":"object","properties":{"n":{"type":"integer"},"pass":{"type":"boolean"},"reason":{"type":"string"}},"required":["n","pass","reason"],"additionalProperties":False}},
 "doubtful_claims":{"type":"array","items":{"type":"string"}},"overall_pass":{"type":"boolean"},"fix":{"type":"string"}},"required":["criteria","doubtful_claims","overall_pass","fix"],"additionalProperties":False}
sys.path.insert(0,str(R/"scripts")); import retrieval_test as r
idx={}
def w(n):
    idx[n["id"]]=n["statement"]; [w(c) for c in r.kids(n)]
for d in r.F.values():
    for p in d["key_line"]["points"]: w(p)
qps=json.load(open(R/"pyramids/tests/question_pyramids/qp.json")); used=0; out=[]
for p in qps:
    nodes={p2["linked_node"]:idx.get(p2["linked_node"]) for p2 in p["key_line"]["points"]}
    user="Question pyramid:\n"+json.dumps(p,ensure_ascii=False,indent=1)+"\n\nLinked node statements:\n"+json.dumps(nodes,ensure_ascii=False,indent=1)
    worst=(len(SYS)+len(user))/3.2/1e6*IN+MAXTOK/1e6*OUT
    if used+worst>CAP: print("cap would be passed; stop"); break
    ctl=q.anthropic_controls(MODEL)
    tdef={"name":"record","description":"Record the review.","input_schema":schema}
    if ctl.get("strict"): tdef["strict"]=True
    body={"model":MODEL,"max_tokens":MAXTOK,"system":SYS,"messages":[{"role":"user","content":user}],"tools":[tdef],"tool_choice":ctl["tool_choice"]}
    if ctl.get("thinking"): body["thinking"]=ctl["thinking"]
    if ctl.get("effort"): body["output_config"]={"effort":ctl["effort"]}
    try:
        d=q._post_anthropic(body,os.environ["ANTHROPIC_API_KEY"])
    except Exception as e:
        print("ERR",getattr(e,"read",lambda:b"")().decode()[:500]); raise
    u=d.get("usage") or {}
    if 0: d=q._post_anthropic(body,os.environ["ANTHROPIC_API_KEY"]); u=d.get("usage") or {}
    usd=u.get("input_tokens",0)/1e6*IN+u.get("output_tokens",0)/1e6*OUT; used+=usd
    res=next((b["input"] for b in d.get("content",[]) if b.get("type")=="tool_use"),None)
    out.append({"test_id":p["test_id"],"usd":round(usd,4),"review":res}); print(p["test_id"],round(usd,4),res and res.get("overall_pass"))
json.dump({"model":MODEL,"total_usd":round(used,4),"reviews":out},open(R/"pyramids/tests/question_pyramid_judgements.json","w"),indent=1,ensure_ascii=False)
print("total",round(used,4))
