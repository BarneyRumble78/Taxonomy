"""Rebuild sections under a fixed, passing key line with Opus 5.5; judge with 3 independent Sonnet checks (2 of 3 must hold)."""
import copy, json, os, re, sys, time, subprocess, fcntl, statistics
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import minto_pass as mp
import cleanup_misplaced as cm

ROOT = mp.ROOT
HARD = 79.2
FIELD_CAP = 1.70
OPUS, SONNET = "claude-opus-5-5", "claude-sonnet-5-5"
RATES = {OPUS: (4.0, 20.0), SONNET: (2.0, 10.0)}
RES = Path("/workspace/rebuild_results.json")
log = cm.log; mp.log = log

# Free rule-based stripping: catalogue-scheme and residual groups are dissolved into their children before the model sees them.
mp.EXPAND = re.compile(mp.EXPAND.pattern + r"|ISIC|NAICS|\bDDC\b|Dewey|\bICD\b|\bLCC\b|Library of Congress|not elsewhere classified|\bn\.?e\.?c\.?\b|thesaur|hierarchy name|subject heading|\bFOR\b|\bSEO\b|catch-all|miscellan", re.I)
mp.SYSTEM += ("\n16. STRICT for this rebuild: no section or subsection may follow ISIC, NAICS, DDC, ICD, LCC, FOR/SEO codes, thesaurus facets or subject-heading lists, "
              "and none may be a 'not elsewhere classified', 'other', 'general' or mixed bucket. Sections inside a pillar split that pillar on ONE subject-matter dimension of its own; "
              "dissolve any input group that is a catalogue class or residual bucket and place its topics individually.")

def add(field, model, usd):
    with mp.LEDGER.open("r+") as h:
        fcntl.flock(h.fileno(), fcntl.LOCK_EX)
        led = json.loads(h.read() or "{}")
        led["spent"] = round(float(led.get("spent", 0)) + usd, 6)
        k = f"REBUILD-{'OPUS' if model == OPUS else 'SONNET'}:{field}"
        led.setdefault("fields", {})[k] = round(float(led["fields"].get(k, 0)) + usd, 6)
        h.seek(0); h.truncate(); h.write(json.dumps(led, indent=2) + "\n")
        fcntl.flock(h.fileno(), fcntl.LOCK_UN)

SPLIT = {}
def call(self, system, user, tool, schema, max_tokens):
    model = OPUS if tool == "record_pyramid" else SONNET
    ir, orr = RATES[model]
    worst = (len(system) + len(user)) / 3.0 / 1e6 * ir + max_tokens / 1e6 * orr
    if self.used + worst > self.field_cap:
        raise RuntimeError(f"field cap ${self.field_cap} would be passed (used {self.used:.3f})")
    if mp.total_spent() + worst > HARD:
        raise RuntimeError(f"hard cap {HARD} would be passed (now {mp.total_spent():.3f})")
    ctl = mp.q.anthropic_controls(SONNET)  # Opus 5.5 takes the same controls (auto tool choice, strict)
    tdef = {"name": tool, "description": "Record the result.", "input_schema": schema, "strict": True}
    body = {"model": model, "max_tokens": max_tokens, "system": system, "messages": [{"role": "user", "content": user}],
            "tools": [tdef], "tool_choice": ctl["tool_choice"], "output_config": {"effort": ctl["effort"]}}
    if model == SONNET: body["thinking"] = ctl["thinking"]  # Opus 5.5 rejects between_tools/disabled; default adaptive
    data = mp.q._post_anthropic(body, os.environ["ANTHROPIC_API_KEY"])
    u = data.get("usage") or {}
    usd = (u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0) * 1.25 + u.get("cache_read_input_tokens", 0) * 0.05) / 1e6 * ir + u.get("output_tokens", 0) / 1e6 * orr
    self.used += usd; add(self.field, model, usd)
    SPLIT.setdefault(self.field, {OPUS: 0.0, SONNET: 0.0})[model] += usd
    log(f"{self.field} call {model} {tool} in={u.get('input_tokens')} out={u.get('output_tokens')} usd={usd:.4f}")
    for b in data.get("content") or []:
        if b.get("type") == "tool_use" and b.get("name") == tool:
            return b.get("input") or {}
    raise RuntimeError("no tool_use in reply: " + str(data.get("stop_reason")))
mp.Budget.call = call

def keyline_from(pyr):
    kl = pyr["key_line"]; ml = pyr.get("method_line") or {}
    return {"governing_thought": pyr["governing_thought"], "dimension": kl["mece_dimension"], "plural_noun": kl["plural_noun"],
            "basis": kl["basis"], "order": kl["order"], "rank_note": kl["rank_note"],
            "pillars": [{"title": p.get("title") or p["statement"][:40], "statement": p["statement"]} for p in kl["points"]],
            "method_line": {"title": "Method line", "covers": ml.get("statement") or "how the discipline is studied, taught and recorded"}, "route_note": ""}

def three_checks(field, pyr, b):
    out = []
    for i in range(3):
        try:
            c = b.call(mp.CHECK_SYSTEM, "Check this pyramid:\n" + json.dumps(cm.view(pyr), ensure_ascii=False, indent=1), "record_check", mp.CHECK_SCHEMA, 2500)
        except RuntimeError as e:
            log(f"{field} check {i+1} skipped: {e}"); break
        out.append({"holds": bool(c.get("key_line_holds")), "misplaced": int(c.get("misplaced") or 0), "note": c.get("note", "")})
        log(f"{field} check {i+1}: holds={out[-1]['holds']} misplaced={out[-1]['misplaced']} note={out[-1]['note'][:160]}")
        if sum(x["holds"] for x in out) >= 2 or sum(not x["holds"] for x in out) >= 2: break
    return out

def git(*a, timeout=60):
    return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, timeout=timeout)

def run(field, results):
    paths = [ROOT / "pyramids" / f"{field}.json", ROOT / "pyramids" / f"{field}_minto.md", ROOT / "pyramids" / "queues" / f"{field}.groups.json"]
    backup = {p: p.read_text() for p in paths}
    orig = json.loads(backup[paths[0]])
    kf = ROOT / "pyramids" / "keylines" / f"{field}.json"
    kl_new = keyline_from(orig)
    if kf.exists():
        old = json.loads(kf.read_text())
        if old.get("governing_thought") != kl_new["governing_thought"]:
            log(f"{field} keylines file differs from saved pyramid; using the saved pyramid's key line")
            old = None
    else:
        old = None
    kf_backup = kf.read_text() if kf.exists() else None
    kf.write_text(json.dumps(old or kl_new, indent=1, ensure_ascii=False) + "\n")
    rec = {"field": field, "misplaced_before": orig["field_check"].get("misplaced")}
    mp.FIXED_MODE[0] = True; mp.ATTEMPTS[0] = 3
    try:
        res = mp.run(field, FIELD_CAP - 0.30, 1e9)   # keep ~$0.30 of the field cap for the 3 checks
    except Exception as e:
        res = {"error": str(e)}; log(f"{field} build error {e}")
    new = json.loads(paths[0].read_text())
    built = new is not orig and json.dumps(new) != backup[paths[0]]
    b = mp.Budget(field, 10, 1e9); b.field_cap = FIELD_CAP - SPLIT.get(field, {}).get(OPUS, 0) - SPLIT.get(field, {}).get(SONNET, 0) + 0.0
    bad = cm.issues(field, new) if built else {"not built": [1]}
    checks = three_checks(field, new, b) if built and not bad else []
    nh = sum(c["holds"] for c in checks)
    ok = built and not bad and nh >= 2
    rec.update(built=built, local_issues=bad if built else None, checks=checks, holds_2of3=ok)
    if ok:
        mis = int(statistics.median([c["misplaced"] for c in checks if c["holds"]]))
        new["field_check"].update(holds=True, misplaced=mis, problems=mis, note=next(c["note"] for c in checks if c["holds"]),
                                  checks_2of3=checks, rebuild={"builder": OPUS, "checker": SONNET, "date": time.strftime("%Y-%m-%d %H:%M")})
        paths[0].write_text(json.dumps(new, indent=2, ensure_ascii=False) + "\n")
        paths[1].write_text(mp.render(new))
        g = json.loads(paths[2].read_text()); g["field_check"] = new["field_check"]; paths[2].write_text(json.dumps(g, indent=2, ensure_ascii=False) + "\n")
        saved = json.loads(paths[0].read_text())["field_check"]
        rec.update(misplaced_after=saved["misplaced"], holds_saved=saved["holds"])
        git("add", *[str(p.relative_to(ROOT)) for p in paths], str(kf.relative_to(ROOT)), "scripts/rebuild_sections_opus.py", "pyramids/queues/cost_ledger.json")
        git("commit", "-m", f"{field}: rebuild sections under fixed key line (Opus 5.5), 2-of-3 Sonnet checks hold, misplaced {rec['misplaced_before']} -> {saved['misplaced']}")
        try: rec["push"] = git("push", "origin", "v3-content", timeout=90).returncode
        except subprocess.TimeoutExpired: rec["push"] = "timeout"
        rec["commit"] = git("rev-parse", "--short", "HEAD").stdout.strip()
        log(f"{field} ACCEPTED committed {rec['commit']} push={rec['push']}")
    else:
        for p, t in backup.items(): p.write_text(t)
        if kf_backup is None: kf.unlink()
        else: kf.write_text(kf_backup)
        log(f"{field} REJECTED rebuild (built={built} issues={bad} holds {nh}/{len(checks)}); original restored")
        rec["misplaced_after"] = rec["misplaced_before"]
    rec["spend"] = {k.split('-')[1]: round(v, 4) for k, v in SPLIT.get(field, {}).items()}
    results[field] = rec

if __name__ == "__main__":
    fields = sys.argv[1:] or ["AG", "AR", "BU", "EA", "IS", "LN", "PH"]
    results = json.loads(RES.read_text()) if RES.exists() else {}
    log(f"REBUILD start {fields}; spent total {mp.total_spent():.3f}")
    for f in fields:
        if f in results: continue
        if mp.total_spent() > HARD - 0.5:
            log(f"stop before {f}: total {mp.total_spent():.3f}"); break
        log(f"{f} rebuild start; spent total {mp.total_spent():.3f}")
        run(f, results); RES.write_text(json.dumps(results, indent=2))
    log(f"REBUILD ALL DONE spent total {mp.total_spent():.3f}")
