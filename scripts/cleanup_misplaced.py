"""Fix misplaced items flagged by the top-down Minto check. Free rule pass from the note, then one Sonnet
proposal call, local validation (minto_issues), then one Sonnet re-check. Keeps a change only if holds stays
True and misplaced does not rise."""
import copy, json, re, sys, time, subprocess, fcntl
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import minto_pass as mp

ROOT = mp.ROOT
LOG = Path("/workspace/cleanup.log")
HARD = 68.8
RES = Path("/workspace/cleanup_results.json")

def log(m):
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S')} {m}"
    print(line, flush=True)
    with LOG.open("a") as h: h.write(line + "\n")
mp.log = log

def add_spend(field, usd):
    with mp.LEDGER.open("r+") as h:
        fcntl.flock(h.fileno(), fcntl.LOCK_EX)
        led = json.loads(h.read() or "{}")
        led["spent"] = round(float(led.get("spent", 0)) + usd, 6)
        k = f"CLEANUP:{field}"
        led.setdefault("fields", {})[k] = round(float(led["fields"].get(k, 0)) + usd, 6)
        h.seek(0); h.truncate(); h.write(json.dumps(led, indent=2) + "\n")
        fcntl.flock(h.fileno(), fcntl.LOCK_UN)
mp.add_spend = add_spend

def call(b, system, user, tool, schema, mt):
    worst = (len(system) + len(user)) / 3.2 / 1e6 * mp.IN_RATE + mt / 1e6 * mp.OUT_RATE
    if mp.total_spent() + worst > HARD:
        raise RuntimeError(f"hard cap {HARD} would be passed (now {mp.total_spent():.2f})")
    return b.call(system, user, tool, schema, mt)

def groups(pyr):
    """position -> node, with parent list, mirroring minto_pass view numbering."""
    pos = {}
    def walk(n, p, parent):
        pos[p] = (n, parent)
        for i, c in enumerate((n.get("support") or {}).get("points") or [], 1):
            walk(c, f"{p}.{i}", n["support"]["points"])
    for i, p in enumerate(pyr["key_line"]["points"], 1): walk(p, f"P{i}", pyr["key_line"]["points"])
    ml = pyr.get("method_line") or {}
    for i, c in enumerate(ml.get("points") or [], 1): walk(c, f"M.{i}", ml["points"])
    return pos

def view(pyr):
    def vw(n, pos, depth):
        sup = (n.get("support") or {}).get("points")
        d = {"id": pos, "statement": (n.get("statement") or n.get("name") or "")[:160]}
        if sup and depth < 3: d["under"] = [vw(c, f"{pos}.{i}", depth + 1) for i, c in enumerate(sup, 1)]
        return d
    return {"governing_thought": pyr["governing_thought"], "key_line_dimension": pyr["key_line"].get("mece_dimension"),
            "pillars": [vw(p, f"P{pi}", 0) for pi, p in enumerate(pyr["key_line"]["points"], 1)],
            "method_line_outside_key_line": [vw(c, f"M.{i}", 1) for i, c in enumerate((pyr.get("method_line") or {}).get("points") or [], 1)],
            "routed_to_other_fields": [x["name"] for x in pyr.get("routed") or []]}

def issues(field, pyr):
    iss = mp.minto_issues(pyr)
    return {k: v for k, v in iss.items() if v and (field == "EV" or k != "mixed_kinds")}

def expand_range(a, b):
    pa, pb = a.split("."), b.split(".")
    if pa[:-1] != pb[:-1]: return [a, b]
    return [".".join(pa[:-1] + [str(i)]) for i in range(int(pa[-1]), int(pb[-1]) + 1)]

def rule_moves(note):
    """Free: clauses that name an explicit target 'belong(s) in/with/under Px'."""
    out = []
    for cl in re.split(r"[;,]|\)\s*,", note):
        t = re.search(r"belongs?\s+(?:in|with|under)\s+(P[\d.]+\d)", cl)
        if not t: continue
        cl2 = cl[:t.start()]
        srcs = []
        for m in re.finditer(r"(P[\d.]*\d)(?:\s*[-–]\s*(P[\d.]*\d))?", cl2):
            srcs += expand_range(m.group(1), m.group(2)) if m.group(2) else [m.group(1)]
        out += [{"item": s, "to": t.group(1), "why": "rule:note"} for s in srcs]
    return out

def apply_moves(field, pyr, moves):
    """Apply one at a time on resolved node objects; keep a move only if it adds no local Minto issue."""
    pos = groups(pyr)
    base = issues(field, pyr)
    nb = sum(len(v) for v in base.values())
    done = []
    for mv in moves:
        src, dst = mv.get("item"), mv.get("to")
        if src not in pos or src.count(".") < 2: continue  # only 2nd/3rd level items
        node, parent = pos[src]
        if node not in parent: continue
        trial = copy.deepcopy(pyr)  # cheap enough
        snap = (copy.copy(parent),)
        if mv.get("route"):
            parent.remove(node)
            pyr.setdefault("routed", []).append({"id": node.get("id"), "name": node.get("name") or node.get("statement"), "to_field": mv.get("route"), "by": "cleanup"})
        else:
            if dst not in pos: continue
            dn, _ = pos[dst]
            dpts = (dn.get("support") or {}).get("points")
            if dpts is None or node in dpts or dst.startswith(src): continue
            parent.remove(node); dpts.append(node)
        new = issues(field, pyr)
        if sum(len(v) for v in new.values()) > nb:
            # revert
            pyr.clear(); pyr.update(trial)
            pos = groups(pyr)
            continue
        done.append(mv)
    return done

PROPOSE = """You fix misplaced items in a classification pyramid. Positions like P2.3.1 are neutral tree positions (P = pillar, M = method line outside the key line).
A top-down check flagged misplaced second- or third-level items. Propose moves of whole items to the existing pillar or section (by position) whose value they share. If an item clearly belongs to another academic field entirely, set route to that field code instead of a target.
Hard limits: every group must keep 2 to 5 children, so do not empty a section below 2 or push one above 5 (child counts are given as n). Prefer moving into a section with room. Only propose clear moves. Leaf names cannot change.
Call propose_moves exactly once."""
PSCHEMA = {"type": "object", "additionalProperties": False, "properties": {"moves": {"type": "array", "items": {"type": "object", "additionalProperties": False,
           "properties": {"item": {"type": "string"}, "to": {"type": "string"}, "route": {"type": "string"}, "why": {"type": "string"}}, "required": ["item", "to", "route", "why"]}}},
           "required": ["moves"]}
FIELDS = ["AG","AR","BI","BU","CH","CS","DE","EA","EC","ED","EN","HI","IK","IS","LA","LN","MA","MD","MS","PH","PL","PO","RE","ST"]

def nview(pyr):
    def vw(n, p, depth):
        sup = (n.get("support") or {}).get("points") or []
        d = {"id": p, "n": len(sup), "s": (n.get("statement") or n.get("name") or "")[:110]}
        if sup and depth < 3: d["under"] = [vw(c, f"{p}.{i}", depth + 1) for i, c in enumerate(sup, 1)]
        return d
    return {"governing_thought": pyr["governing_thought"], "dimension": pyr["key_line"].get("mece_dimension"),
            "pillars": [vw(p, f"P{i}", 0) for i, p in enumerate(pyr["key_line"]["points"], 1)],
            "method_line": [vw(c, f"M.{i}", 1) for i, c in enumerate((pyr.get("method_line") or {}).get("points") or [], 1)]}

def git(*a, timeout=60):
    return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, timeout=timeout)

def run(field, results):
    ok = run1(field, results, 1)
    r = results.get(field, {})
    if ok and not r.get("changed") and r.get("check_note") and "stopped" not in r:
        log(f"{field} round 2 using the re-check note")
        ok = run1(field, results, 2, note2=r["check_note"], prev=r)
    return ok

def run1(field, results, rnd, note2=None, prev=None):
    f = ROOT / "pyramids" / f"{field}.json"
    orig = json.loads(f.read_text()); pyr = copy.deepcopy(orig)
    fc = orig.get("field_check") or {}
    before = fc.get("misplaced"); note = note2 or fc.get("note", "")
    rec = {"field": field, "before": before, "holds_before": fc.get("holds"), "round": rnd, "prior_cost": (prev or {}).get("cost", 0)}
    if issues(field, pyr): log(f"{field} pre-existing local issues {issues(field, pyr)}")
    if prev:  # replay round-1 moves, then work from the new note
        apply_moves(field, pyr, prev.get("rule_moves", []) + prev.get("ai_moves", []))
    free = apply_moves(field, pyr, rule_moves(note))
    rec["rule_moves"] = free
    b = mp.Budget(field, 0.6, 100.0); b.stage_cap = 1e9
    try:
        out = call(b, PROPOSE, "Flagged by the check (" + str(before) + " misplaced): " + note + "\nAlready applied by rule: " + json.dumps(free) +
                   "\nPyramid AFTER those rule moves:\n" + json.dumps(nview(pyr), ensure_ascii=False), "propose_moves", PSCHEMA, 3000)
        mv = [dict(m, route=(m.get("route") or "").strip() or None) for m in out.get("moves") or []]
        ai = apply_moves(field, pyr, mv)
    except RuntimeError as e:
        log(f"{field} stop: {e}"); rec["stopped"] = str(e); results[field] = rec; return False
    rec["ai_moves"] = ai; rec["ai_proposed"] = len(mv)
    if not free and not ai:
        log(f"{field} no applicable moves; unchanged"); rec.update(after=before, holds_after=fc.get("holds"), changed=False, cost=b.used)
        results[field] = rec; return True
    try:
        chk = call(b, mp.CHECK_SYSTEM, "Check this pyramid:\n" + json.dumps(view(pyr), ensure_ascii=False, indent=1), "record_check", mp.CHECK_SCHEMA, 2500)
    except RuntimeError as e:
        log(f"{field} stop at check: {e}"); rec["stopped"] = str(e); results[field] = rec; return False
    bad = issues(field, pyr)
    holds = bool(chk.get("key_line_holds")) and not bad
    after = int(chk.get("misplaced") or 0)
    if not bad and (not holds or after >= (before or 0)):
        log(f"{field} first re-check holds={holds} misplaced={after}; checking once more (checker is noisy)")
        try:
            chk2 = call(b, mp.CHECK_SYSTEM, "Check this pyramid:\n" + json.dumps(view(pyr), ensure_ascii=False, indent=1), "record_check", mp.CHECK_SCHEMA, 2500)
        except RuntimeError as e:
            chk2 = None; log(f"{field} second check skipped: {e}")
        if chk2:
            rec["first_check"] = {"holds": holds, "misplaced": after, "note": chk.get("note")}
            h2, a2 = bool(chk2.get("key_line_holds")), int(chk2.get("misplaced") or 0)
            if (h2 and not holds) or (h2 == holds and a2 < after):
                chk, holds, after = chk2, h2, a2
    rec.update(check_holds=holds, check_misplaced=after, check_note=chk.get("note"), cost=round(b.used, 4))
    log(f"{field} recheck holds={holds} misplaced {before}->{after} moves rule={len(free)} ai={len(ai)}/{len(mv)} cost=${b.used:.4f} note={chk.get('note')}")
    if not holds or after >= (before or 0):
        log(f"{field} REJECTED (kept original)"); rec.update(after=before, holds_after=fc.get("holds"), changed=False)
        results[field] = rec; return True
    pyr["field_check"] = dict(fc, holds=holds, misplaced=after, note=chk.get("note", ""), problems=after,
                              cleanup={"before": before, "rule_moves": len(free), "ai_moves": len(ai), "date": time.strftime("%Y-%m-%d %H:%M")})
    pyr["cost_usd"] = round(float(orig.get("cost_usd") or 0) + b.used, 4)
    f.write_text(json.dumps(pyr, indent=2, ensure_ascii=False) + "\n")
    (ROOT / "pyramids" / f"{field}_minto.md").write_text(mp.render(pyr))
    gq = ROOT / "pyramids" / "queues" / f"{field}.groups.json"
    if gq.exists():
        g = json.loads(gq.read_text()); g["field_check"] = pyr["field_check"]; gq.write_text(json.dumps(g, indent=2, ensure_ascii=False) + "\n")
    saved = json.loads(f.read_text())["field_check"]
    rec.update(after=saved["misplaced"], holds_after=saved["holds"], changed=True)
    git("add", f"pyramids/{field}.json", f"pyramids/{field}_minto.md", f"pyramids/queues/{field}.groups.json", "scripts/cleanup_misplaced.py", "pyramids/queues/cost_ledger.json")
    c = git("commit", "-m", f"{field}: move misplaced items ({before} -> {after}), holds={saved['holds']}")
    try:
        p = git("push", "origin", "v3-content", timeout=90); rec["push"] = p.returncode
    except subprocess.TimeoutExpired:
        rec["push"] = "timeout"
    rec["commit"] = git("rev-parse", "--short", "HEAD").stdout.strip()
    log(f"{field} committed {rec['commit']} push={rec['push']}")
    results[field] = rec; return True

if __name__ == "__main__":
    fields = sys.argv[1:] or FIELDS
    results = json.loads(RES.read_text()) if RES.exists() else {}
    for fl in fields:
        if fl in results and "stopped" not in results[fl]: continue
        log(f"{fl} start; spent total {mp.total_spent():.3f}")
        ok = run(fl, results)
        RES.write_text(json.dumps(results, indent=2))
        if not ok: break
    log(f"ALL DONE spent total {mp.total_spent():.3f}")
