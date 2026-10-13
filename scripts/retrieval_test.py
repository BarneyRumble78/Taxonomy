"""Deterministic top-down retrieval test (BM25 over pyramid nodes; no LLM).
Field score -> pillar -> section -> group. Used because the Mac's Qwen was unreachable."""
import json,glob,math,re,collections
from pathlib import Path
R=Path(__file__).resolve().parents[1]
STOP=set("a an the of and or in on to for is are be by with from how what why which who does do can its it as at that this their there into than more most about should when whether use used new zealand".split())
def stem(w):
    for s in ("ational","ations","ation","ities","ity","ings","ing","ies","es","ed","al","s"):
        if w.endswith(s) and len(w)-len(s)>=4: return w[:-len(s)]
    return w
def tok(t): return [stem(w) for w in re.findall(r"[a-zāēīōū]+",t.lower()) if w not in STOP and len(w)>2]
import os
ENRICH=os.environ.get("ENRICH")=="1"
_maps={}
def srcname(src):
    f=src.get("file")
    if not f: return ""
    if f not in _maps:
        try: _maps[f]={x["id"]:x.get("name","") for x in json.load(open(R/f)).get("nodes",[])}
        except Exception: _maps[f]={}
    return _maps[f].get(src.get("id"),"")
def text(n):
    t=n.get("statement","")
    if ENRICH: t+=" "+" ".join(srcname(x) for x in n.get("sources",[]) or [])
    return t
def kids(n):
    s=n.get("support"); return (s or {}).get("points",[]) if isinstance(s,dict) else []
def subtree(n):
    out=[text(n)]
    for c in kids(n): out+=subtree(c)
    return out
F={}
for f in sorted(glob.glob(str(R/"pyramids/??.json"))):
    d=json.load(open(f)); F[d["field"]]=d
docs={}  # id -> tokens
def add(i,txt): docs[i]=tok(txt)
for k,d in F.items():
    add(k," ".join([d["governing_thought"]]+sum([subtree(p) for p in d["key_line"]["points"]],[])))
    for p in d["key_line"]["points"]:
        add(p["id"]," ".join(subtree(p)))
        for s in kids(p):
            add(s["id"]," ".join(subtree(s)))
            for g in kids(s): add(g["id"]," ".join(subtree(g)))
N=len(docs); df=collections.Counter(w for t in docs.values() for w in set(t))
avg=sum(map(len,docs.values()))/N
def bm25(q,i,k1=1.2,b=0.75):
    t=docs[i]; c=collections.Counter(t); L=len(t); s=0
    for w in set(q):
        if w in c: s+=math.log(1+(N-df[w]+.5)/(df[w]+.5))*c[w]*(k1+1)/(c[w]+k1*(1-b+b*L/avg))
    return s
def rank(q,ids): return sorted(((bm25(q,i),i) for i in ids),reverse=True)
def retrieve(question):
    q=tok(question)
    fr=rank(q,F.keys())[:3]
    # strictly top-down: pillars ranked inside the top field only
    pil=rank(q,[p["id"] for p in F[fr[0][1]]["key_line"]["points"]])[:3]
    node={p["id"]:p for d in F.values() for p in d["key_line"]["points"]}
    best=node[pil[0][1]]
    sec=rank(q,[s["id"] for s in kids(best)])[:1]
    secn=next((s for s in kids(best) if sec and s["id"]==sec[0][1]),None)
    grp=rank(q,[g["id"] for g in kids(secn)])[:2] if secn else []
    return {"fields":[f for _,f in fr],"field_scores":[round(s,2) for s,_ in fr],"pillars":[p for _,p in pil],
            "section":sec[0][1] if sec else None,"groups":[g for _,g in grp]}
if __name__=="__main__":
    gold=json.load(open(R/"pyramids/tests/retrieval_gold.json"))["questions"]
    res=[];st=collections.Counter()
    for g in gold:
        r=retrieve(g["q"]); okF=[g["field"]]+g.get("alt_fields",[]); okP=[g["pillar"]]+g.get("alt_pillars",[])
        row=dict(id=g["id"],q=g["q"],gold_field=g["field"],gold_pillar=g["pillar"],**r,
          field_top1=r["fields"][0] in okF, field_top3=any(f in okF for f in r["fields"]),
          pillar_top1=r["pillars"][0] in okP, pillar_top3=any(p in okP for p in r["pillars"]))
        for k in ("field_top1","field_top3","pillar_top1","pillar_top3"): st[k]+=row[k]
        res.append(row)
    out={"method":"BM25 top-down (box, deterministic; Mac Qwen unreachable)"+(" + source topic names" if ENRICH else ", node statements only"),"n":len(gold),
         "accuracy":{k:f"{v}/{len(gold)}" for k,v in st.items()},"results":res}
    (R/("pyramids/tests/retrieval_results"+("_enriched" if ENRICH else "")+".json")).write_text(json.dumps(out,indent=1,ensure_ascii=False))
    print(out["accuracy"])
    for r in res: print(r["id"],"F" if r["field_top1"] else ("f" if r["field_top3"] else "-"),"P" if r["pillar_top1"] else ("p" if r["pillar_top3"] else "-"),r["gold_field"],r["gold_pillar"],"->",r["fields"],r["pillars"],r["section"])
