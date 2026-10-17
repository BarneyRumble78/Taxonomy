"""Free, rule-based PH fix (no API calls): earth-science groups to EA, network leaves to one condensed-matter
section, learning theory to the method line. Validated with local minto_issues and id-uniqueness only."""
import json, sys, collections
sys.path.insert(0, "scripts"); import cleanup_misplaced as cm
PH = json.load(open("pyramids/PH.json")); EA = json.load(open("pyramids/EA.json"))
ph, ea = cm.groups(PH), cm.groups(EA)
before = {"PH": cm.issues("PH", PH), "EA": cm.issues("EA", EA)}
def node(t, p): return t[p][0]
def kids(n): return n["support"]["points"]
def name(n): return (n.get("name") or n.get("statement") or "")[:70]
# resolve every node first, then move by object (positions shift as we go)
to_ea = [("P5.1.1.3", "P2.2"), ("P5.1.2.3", "P2.2"), ("P5.1.2.4", "P2.3"), ("P5.1.2.5", "P2.1"),
         ("P5.1.1.4", "P4.2"), ("P5.1.1.5", "P3.1"), ("P5.1.3.1", "P4.1")]
moves = [(ph[s], node(ea, d), f"PH {s} -> EA {d}") for s, d in to_ea]
moves.append((ph["P5.1.3.5"], node(ph, "M.1.2"), "PH P5.1.3.5 -> PH M.1.2 (method line)"))
net_src = ["P2.1.3.1", "P2.1.3.3", "P2.1.3.4", "P2.3.1.4", "P2.3.1.5"]
net_nodes = [ph[s] for s in net_src]
log = []
for (n, parent), dest, why in moves:
    parent.remove(n); kids(dest).append(n); log.append(f"{why}: {name(n)}")
net = {"id": "PH.K3.NET", "anchor": "section:PH.K3.NET",
       "statement": "Network structure topics describe many connected elements whose collective behaviour is set by how the links are arranged.",
       "support": {"logic_type": "inductive", "basis": "kinds", "order": "structure",
                   "rank_note": "Ordered from quantum and general network structure to layered, uncorrelated and tree networks.", "points": []}}
net["name"] = net["statement"]
for s, (n, parent) in zip(net_src, net_nodes):
    parent.remove(n); net["support"]["points"].append(n); log.append(f"PH {s} -> PH P3.1.3 (new network-structure section): {name(n)}")
kids(node(ph, "P3.1.3")).append(net)
PH.setdefault("moved_out", []).extend([{"id": n.get("id"), "name": n.get("name"), "to_field": "EA", "to_section": d} for (m, (s, d)) in zip(moves[:7], to_ea) for n in [m[0][0]]])
after = {"PH": cm.issues("PH", PH), "EA": cm.issues("EA", EA)}
def ids(t):
    c = collections.Counter()
    def w(n):
        c[n.get("id") or n.get("anchor")] += 1
        for k in (n.get("support") or {}).get("points") or []: w(k)
    for p in t["key_line"]["points"]: w(p)
    for p in (t.get("method_line") or {}).get("points") or []: w(p)
    return c
cp, ce = ids(PH), ids(EA)
dup = {k: v for k, v in (cp + ce).items() if v > 1}
def sizes(t):  # 2-5 rule on every group
    bad = []
    for p, (n, _) in cm.groups(t).items():
        k = (n.get("support") or {}).get("points")
        if k is not None and k and not 2 <= len(k) <= 5: bad.append((p, len(k)))
    return bad
rep = {"moves": log, "issues_before": before, "issues_after": after, "duplicate_ids": dup, "size_violations": {"PH": sizes(PH), "EA": sizes(EA)},
       "dropped_ids_present": {i: cp[i] for i in ["PhySH:63764576-5e03-40cf-9680-5796e144da49", "PhySH:7656e510-f579-4768-9a96-51bb544218eb"]},
       "n_ids": {"PH": sum(cp.values()), "EA": sum(ce.values())}}
print(json.dumps(rep, indent=1))
ok = not any(after.values()) and not dup and not any(rep["size_violations"].values()) and all(v == 1 for v in rep["dropped_ids_present"].values())
if ok and "--write" in sys.argv:
    import minto_pass as mp
    for f, t in (("PH", PH), ("EA", EA)):
        open(f"pyramids/{f}.json", "w").write(json.dumps(t, indent=2, ensure_ascii=False) + "\n")
        open(f"pyramids/{f}_minto.md", "w").write(mp.render(t))
    print("WRITTEN")
print("VALID" if ok else "INVALID")
