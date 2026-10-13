"""Free fix: add curated everyday leaf topics and plain-English keywords to all 25 pyramids. No LLM."""
import json,glob,re,collections
from pathlib import Path
R=Path(__file__).resolve().parents[1]
A=json.load(open(R/"pyramids/curated/added_topics.json"))["additions"]
PK=json.load(open(R/"pyramids/curated/pillar_keywords.json"))
SYN={"security":["protection","safety"],"law":["legal","rules"],"regulation":["rules","regulator","approval"],"disease":["illness","sickness"],
"therapy":["treatment"],"pharmacology":["drugs","medicines"],"economics":["economy"],"education":["schooling"],"military":["armed forces","defence"],
"vehicles":["cars"],"structures":["buildings"],"computing":["computers"],"environment":["nature"],"psychology":["mind","behaviour"]}
STOP=set("and the of in for to a an on general other its their with by from as or".split())
def kids(n):
    s=n.get("support"); return s.get("points",[]) if isinstance(s,dict) else []
def leaves(n):
    k=kids(n)
    return [n.get("name") or n.get("statement","")] if not k else sum((leaves(c) for c in k),[])
def derive(n,cap=15):
    c=collections.Counter()
    for l in leaves(n):
        for w in re.findall(r"[A-Za-zāēīōū'-]+",l.lower()):
            if w not in STOP and len(w)>3: c[w]+=1
    kw=[w for w,_ in c.most_common(cap)]
    for w in list(kw):
        kw+= [s for s in SYN.get(w,[]) if s not in kw]
    return kw
def slug(s): return re.sub(r"[^a-z0-9]+","-",s.lower()).strip("-")[:48]
def leafnode(l):
    return {"id":"MINERVA:"+slug(l),"anchor":"node:MINERVA:"+slug(l),"statement":l,"name":l,"added":True,"source":"minerva-curated"}
def find(points,i):
    for p in points:
        if p["id"]==i: return p
        r=find(kids(p),i)
        if r: return r
F={}
for f in sorted(glob.glob(str(R/"pyramids/??.json"))):
    d=json.load(open(f)); F[d["field"]]=(f,d)
log=[]
for a in A:
    fld=a["parent"].split(".")[0]; f,d=F[fld]
    par=find(d["key_line"]["points"],a["parent"]); sp=par["support"]["points"]
    gid=f'{a["parent"]}.M{1+sum(1 for x in sp if ".M" in x["id"])}'
    if any(x.get("added") for x in sp if x.get("statement")==a["statement"]): continue
    assert len(sp)<5, f"{a['parent']} full"
    node={"id":gid,"anchor":("section:" if a.get("as_section") else "group:")+gid,"statement":a["statement"],"name":a["statement"],
          "added":True,"source":"minerva-curated",
          "support":{"logic_type":"inductive","plural_noun":"members","basis":"kinds","order":"structure","points":[leafnode(l) for l in a["leaves"]]}}
    sp.append(node); log.append(f'{gid}: +{len(a["leaves"])} leaves')
for fld,(f,d) in F.items():
    for p in d["key_line"]["points"]:
        cur=[x.strip() for x in PK.get(p["id"],"").split(",") if x.strip()]
        p["keywords"]=cur+[w for w in derive(p,10) if w not in cur]
        p["keywords_source"]="minerva-curated + member labels"
        for s in kids(p):
            if kids(s):
                s["keywords"]=derive(s); s["keywords_source"]="member labels + synonyms"
    Path(f).write_text(json.dumps(d,indent=2,ensure_ascii=False)+"\n")
print("\n".join(log))
