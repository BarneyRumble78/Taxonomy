"""Retrieval v2: BM25 over section-sized docs (statement + keywords + member labels), field score = best section
(max-section scoring removes the field-size bias), pillar top-3 allowed across fields. Deterministic, no LLM."""
import json,glob,math,re,collections,os,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from retrieval_test import tok,kids,R
PR=Path(os.environ.get("PYR_ROOT",R))
def own(n): return " ".join([n.get("statement","")]+n.get("keywords",[]))
def sub(n): return [own(n)]+sum((sub(c) for c in kids(n)),[])
F={json.load(open(f))["field"]:json.load(open(f)) for f in sorted(glob.glob(str(PR/"pyramids/??.json")))}
docs={};owner={}
for fk,d in F.items():
    for p in d["key_line"]["points"]:
        docs[p["id"]]=tok(own(p)+" "+fk_name if (fk_name:=d["governing_thought"].split(" is ")[0].split(" are ")[0]) else own(p)); owner[p["id"]]=(fk,p["id"])
        for s in kids(p):
            docs[s["id"]]=tok(" ".join(sub(s))); owner[s["id"]]=(fk,p["id"])
N=len(docs); df=collections.Counter(w for t in docs.values() for w in set(t)); avg=sum(map(len,docs.values()))/N
def bm25(q,i,k1=1.2,b=0.9):
    t=docs[i];c=collections.Counter(t);L=len(t);s=0
    for w in set(q):
        if w in c: s+=math.log(1+(N-df[w]+.5)/(df[w]+.5))*c[w]*(k1+1)/(c[w]+k1*(1-b+b*L/avg))
    return s
def retrieve(question):
    q=tok(question); ps=collections.defaultdict(float); best_sec={}
    for i in docs:
        sc=bm25(q,i); fk,pid=owner[i]
        if i==pid: ps[pid]+=0.5*sc            # pillar's own label+keywords
        else:
            if sc>best_sec.get(pid,(0,None))[0]: best_sec[pid]=(sc,i)
    for pid,(sc,_) in best_sec.items(): ps[pid]+=sc
    pil=sorted(ps.items(),key=lambda x:-x[1])
    fs=collections.OrderedDict()
    for pid,sc in pil:
        fs.setdefault(pid.split(".")[0],sc)
    fields=list(fs)[:3]
    top=pil[0][0]; sec=best_sec.get(top,(0,None))[1]
    secn=next((s for p in F[top.split(".")[0]]["key_line"]["points"] if p["id"]==top for s in kids(p) if s["id"]==sec),None)
    grp=[]
    if secn:
        gd={g["id"]:tok(" ".join(sub(g))) for g in kids(secn)}
        def sc(t): return sum(1 for w in set(q) if w in t)
        grp=sorted(gd,key=lambda g:-sc(gd[g]))[:2]
    return {"fields":fields,"pillars":[p for p,_ in pil[:3]],"pillar_scores":[round(s,2) for _,s in pil[:3]],"section":sec,"groups":grp}
if __name__=="__main__":
    GOLD=os.environ.get("GOLD","retrieval_gold"); gold=json.load(open(R/f"pyramids/tests/{GOLD}.json"))["questions"]
    res=[];st=collections.Counter()
    for g in gold:
        r=retrieve(g["q"]); okF=[g["field"]]+g.get("alt_fields",[]); okP=[g["pillar"]]+g.get("alt_pillars",[])
        row=dict(id=g["id"],q=g["q"],gold_field=g["field"],gold_pillar=g["pillar"],**r,
          field_top1=r["fields"][0] in okF,field_top3=any(f in okF for f in r["fields"]),
          pillar_top1=r["pillars"][0] in okP,pillar_top3=any(p in okP for p in r["pillars"]))
        for k in ("field_top1","field_top3","pillar_top1","pillar_top3"): st[k]+=row[k]
        res.append(row)
    out={"method":"v2: max-section BM25, keywords, cross-field pillar top-3 (box, deterministic; Mac offline)","n":len(gold),"accuracy":{k:f"{st[k]}/{len(gold)}" for k in ("field_top1","field_top3","pillar_top1","pillar_top3")},"results":res}
    (R/("pyramids/tests/"+os.environ.get("OUT","retrieval_results_v2")+".json")).write_text(json.dumps(out,indent=1,ensure_ascii=False))
    print(out["accuracy"])
    for r in res: print(r["id"],"F" if r["field_top1"] else ("f" if r["field_top3"] else "-"),"P" if r["pillar_top1"] else ("p" if r["pillar_top3"] else "-"),r["gold_pillar"],"->",r["fields"],r["pillars"],r["section"])
