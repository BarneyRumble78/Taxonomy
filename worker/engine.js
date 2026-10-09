// Taxonomy engine, JavaScript port of engine/taxonomy_engine.py (classify, whole_view).
// tests/test_parity.py checks that both give the same answers. Keep them in step.
// audit(), map() and relate() exist only here.

const LAW_CUE = /\bact (19|20)\d\d\b|\bunder the [a-z ]+act\b/;
// Heuristic only. Failure to classify an instruction-like imperative is not a security guarantee.
const INSTRUCTION_HEURISTIC = /\b(?:ignore|disregard|forget)\b.{0,80}\b(?:previous|prior|above)\b|\breveal\b.{0,40}\bsystem prompt\b/i;
const CONFIDENCE_NOTE = "Confidence is a ratio of cue-word scores, not a probability.";
const PROOF_VERBS = new Set(["prove", "proof"]);

export function instructionHeuristic(sentence) {
  return INSTRUCTION_HEURISTIC.test(sentence || "");
}

// Python's round() rounds exact halves to even; mirror it so the two engines agree.
function pyRound2(x) {
  const r = x * 100, f = Math.floor(r);
  if (r - f === 0.5) return (f % 2 === 0 ? f : f + 1) / 100;
  return Math.round(r) / 100;
}
const score = (t, words) => words.reduce((n, w) => n + (t.includes(w) ? 1 : 0), 0);
const argmaxFirst = (arr) => arr.indexOf(Math.max(...arr));

export function createEngine(D) {
  const fields = D.lexicon.fields;
  const codes = Object.keys(D.names);

  function fieldScore(t, f, skip) {
    const kw = skip ? f.kw.filter((w) => !skip.has(w)) : f.kw;
    return score(t, kw) + 0.5 * f.cells.reduce((n, cl) => n + score(t, cl), 0);
  }

  function classify(sentence) {
    if (instructionHeuristic(sentence)) return null;
    const t = " " + sentence.toLowerCase() + " ";
    const scores = {};
    for (const [c, f] of Object.entries(fields)) scores[c] = fieldScore(t, f);
    const other = Math.max(...Object.entries(scores).filter(([c]) => c !== "MA").map(([, v]) => v));
    if (other > 0) scores.MA = fieldScore(t, fields.MA, PROOF_VERBS);
    const ranked = Object.entries(scores).sort((a, b) => b[1] - a[1]);
    let [owner, top] = ranked[0];
    if (top === 0) return null;
    if (["theorem", "question is open"].some((k) => t.includes(k)) && scores.MA >= top - 1 && scores.MA > 0) owner = "MA";
    if (LAW_CUE.test(t) && scores.LA >= top - 2) owner = "LA";
    const cs = fields[owner].cells.map((w) => score(t, w));
    let idx = argmaxFirst(cs);
    if (owner === "MA" && t.includes("integral domain")) idx = 1;
    const cell = `${owner}.O.A${idx + 1}`;
    const w = {};
    for (const [k, v] of Object.entries(D.lexicon.warrants)) w[k] = score(t, v);
    const wvals = Object.values(w);
    const wmax = Math.max(...wvals);
    let warrant = wmax > 0 ? Object.keys(w)[argmaxFirst(wvals)] : D.defaultWarrant[owner];
    if ((w[D.defaultWarrant[owner]] ?? 0) >= wmax) warrant = D.defaultWarrant[owner];
    if (warrant === "W13" && owner !== "RE" && owner !== "IK") warrant = D.defaultWarrant[owner];
    const m = {};
    for (const [k, v] of Object.entries(D.lexicon.methods)) m[k] = score(t, v);
    const mvals = Object.values(m);
    let method = Math.max(...mvals) > 0 ? Object.keys(m)[argmaxFirst(mvals)] : D.warrantToMethod[warrant];
    const proofClaim = warrant === "W1" && ((w.W1 || 0) > 0 || ["prove", "proof", "theorem", "lemma"].some((s) => t.includes(s)));
    if (proofClaim && method === "M3") method = "M2";
    const contested = ranked.slice(1, 4).filter(([c, s]) => s > 0 && s >= top - 1 && c !== owner).map(([c]) => c);
    const second = ranked.length > 1 ? ranked[1][1] : 0;
    return {
      owner, owner_name: D.names[owner], cell, cell_name: D.cells[owner][idx],
      warrant, warrant_name: D.warrantNames[warrant], method, method_name: D.methodNames[method],
      confidence: pyRound2(top / (top + second + 1)), confidence_note: CONFIDENCE_NOTE, contested_with: contested,
    };
  }

  function relevance(subject) {
    const t = " " + subject.toLowerCase() + " ";
    return codes.map((c) => {
      const f = fields[c];
      return [c, score(t, f.kw) + 0.5 * f.cells.reduce((n, cl) => n + score(t, cl), 0)];
    });
  }

  function wholeView(subject) {
    return relevance(subject)
      .map(([c, rel]) => ({
        field: c, name: D.names[c], relevance: rel,
        questions: D.cells[c].map((cell) => `${D.names[c]} / ${cell}: what does this field establish about ${subject}, and on what warrant?`),
      }))
      .sort((a, b) => b.relevance - a.relevance);
  }

  // What it would take to establish a claim in this cell, and what would break it.
  function evidenceFor(cellId) {
    const e = D.cellinfo[cellId];
    return e ? { warrant: e.warrant, standard: e.standard, defeaters: e.defeaters } : null;
  }

  function borders(code, n = 3) {
    const out = D.graph[code] || {}, back = {};
    for (const a of codes) if (D.graph[a][code]) back[a] = D.graph[a][code];
    const all = new Set([...Object.keys(out), ...Object.keys(back)]);
    return [...all]
      .map((f) => ({ field: f, name: D.names[f], uses: out[f] || 0, cited_by: back[f] || 0 }))
      .sort((a, b) => b.uses + b.cited_by - (a.uses + a.cited_by))
      .slice(0, n);
  }

  // Whole view of a subject: every field that matched, what it can say, how it borders the others.
  function map(subject, top = 8, extra = []) {
    const rel = relevance(subject);
    const chosen = new Map(rel.filter(([, r]) => r > 0).map(([c, r]) => [c, r]));
    for (const c of extra) if (!chosen.has(c)) chosen.set(c, 0);
    const ranked = [...chosen.entries()].sort((a, b) => b[1] - a[1]);
    const shown = ranked.slice(0, top).map(([c, r]) => ({
      field: c, name: D.names[c], relevance: r, field_url: `/v1/field/${c}.json`,
      lenses: D.cells[c].map((cell, i) => {
        const id = `${c}.O.A${i + 1}`;
        return {
          cell: id, name: cell,
          question: `What does ${D.names[c]} (${cell}) establish about ${subject}, and how do you know?`,
          evidence: evidenceFor(id),
        };
      }),
      borders: borders(c),
    }));
    const shownSet = new Set(shown.map((s) => s.field));
    const vals = rel.map(([, r]) => r), total = vals.reduce((a, b) => a + b, 0);
    const H = total === 0 ? 0 : -vals.filter((v) => v > 0).reduce((s, v) => s + (v / total) * Math.log(v / total), 0) / Math.log(codes.length);
    const relMap = new Map(rel);
    const doesNotApply = codes.filter((c) => (relMap.get(c) || 0) === 0).map((c) => ({
      field: c, name: D.names[c],
      reason: "No cue from this field matched the subject. The field may not apply, or the wording may not have used its terms. A miss is not a finding that the field is irrelevant.",
    }));
    return {
      subject, fields: shown,
      not_expanded: codes.filter((c) => !shownSet.has(c)).map((c) => ({ field: c, name: D.names[c] })),
      does_not_apply: doesNotApply,
      coverage: { fields_matched: chosen.size, of: codes.length, share: pyRound2(chosen.size / codes.length) },
      balance: pyRound2(H),
      note: chosen.size === 0
        ? "No cue words matched, so nothing is expanded. Add detail to the subject, or pass assist=1 to ask the model for candidate fields."
        : "Relevance counts cue words. A field with no match is not shown to be irrelevant. Coverage under 25 is a short list plus an explicit remainder, not a failed map. Check does_not_apply and not_expanded before you rely on this view.",
    };
  }

  function relate(a, b) {
    const ida = D.ids[a], idb = D.ids[b];
    const fa = codes.includes(a) ? a : ida ? a.slice(0, 2) : null;
    const fb = codes.includes(b) ? b : idb ? b.slice(0, 2) : null;
    if (!fa || !fb) return null;
    const ab = D.graph[fa][fb] || 0, ba = D.graph[fb][fa] || 0;
    const deg = (f) => Object.values(D.graph[f]).reduce((s, v) => s + v, 0) + codes.reduce((s, c) => s + (D.graph[c][f] || 0), 0);
    const denom = Math.sqrt(deg(fa) * deg(fb)) || 1;
    const nbrs = (f) => new Set([...Object.keys(D.graph[f]), ...codes.filter((c) => D.graph[c][f])]);
    const nb = nbrs(fb);
    return {
      a: { id: a, field: fa, name: D.names[fa] }, b: { id: b, field: fb, name: D.names[fb] },
      a_uses_b: ab, b_uses_a: ba, border_strength: pyRound2((ab + ba) / denom),
      shared_neighbours: [...nbrs(fa)].filter((x) => nb.has(x) && x !== fa && x !== fb).map((x) => ({ field: x, name: D.names[x] })),
      note: "Counts registry rows that cite the other field. Fields with no direct citation can still be linked through shared neighbours.",
    };
  }

  // ---- audit: heuristics on wording, not a verdict on truth -------------------------------
  const INSTRUCTION = /^\s*(ignore|disregard|forget|override|reveal|pretend|you must|you are now|system prompt)\b|\b(ignore|disregard) (all |any |the )?(previous|prior|above) /i;
  const CERTAIN = /\b(prove[sd]?|proven|conclusively|definitively|undeniabl[ey]|beyond (any )?doubt|guarantee[sd]?)\b/i;
  const CAUSAL = /\b(causes?|caused|leads? to|led to|results? in|resulted in)\b/i;
  const DESIGN = /\b(randomi[sz]ed|trial|experiment|instrument|natural experiment|difference-in-differences|regression discontinuity|controlled|cohort|meta-analysis|longitudinal)\b/i;
  const TRADITION = /\b(scripture|sacred|revealed|the church teaches|tradition holds|doctrine|canon)\b/i;
  const MEASURE = /\b\d+(\.\d+)?\s?(%|percent|kg|km|m|years?|degrees|tonnes?)\b|\b(1[0-9]{3}|20[0-9]{2})\b/i;
  const UNNAMED = /\b(studies show|research shows|experts say|it is well known|scientists agree|everyone knows)\b/i;
  const SOURCED = /\bet al\b|\(\s*[A-Z][a-z]+,? (19|20)\d\d\s*\)|\bsource:|https?:\/\//;

  function audit(text) {
    const sentences = text.replace(/\s+/g, " ").split(/(?<=[.!?])\s+/).filter((s) => s.trim()).slice(0, 60);
    const results = sentences.map((s, i) => {
      const c = classify(s);
      const flags = [];
      if (INSTRUCTION.test(s)) flags.push({ code: "instruction_like", detail: "Reads as an instruction. Claims have an owner and a warrant; instructions do not. Do not treat it as evidence." });
      if (CAUSAL.test(s) && !DESIGN.test(s)) flags.push({ code: "causal_without_design", detail: "Causal wording with no study design named (W3 intervention or W5 identification)." });
      if (UNNAMED.test(s) && !SOURCED.test(s)) flags.push({ code: "unnamed_authority", detail: "Appeals to unnamed studies or experts. No record (W7) or measurement (W4) is cited." });
      if (!c && !flags.length) flags.push({ code: "no_owner", detail: "No field recognised the wording. It may not be a claim." });
      if (c) {
        if (CERTAIN.test(s) && D.defaultWarrant[c.owner] !== "W1") flags.push({ code: "proof_wording", detail: `Proof language in ${c.owner_name}, where claims rest on ${D.defaultWarrant[c.owner]}, not a proof.` });
        if (TRADITION.test(s) && MEASURE.test(s) && c.owner !== "RE" && c.owner !== "IK") flags.push({ code: "w13_travel", detail: "Tradition-internal authority offered for a measurement or date. W13 never licenses one." });
        if (c.confidence < 0.4 || c.contested_with.length) flags.push({ code: "border_claim", detail: `Ownership is contested${c.contested_with.length ? " with " + c.contested_with.join(", ") : ""}. Confidence ${c.confidence}.` });
      }
      return { n: i + 1, sentence: s, placement: c, evidence: c ? evidenceFor(c.cell) : null, flags };
    });
    const placed = results.filter((r) => r.placement);
    const share = (key) => {
      const o = {};
      for (const r of placed) o[r.placement[key]] = (o[r.placement[key]] || 0) + 1;
      return Object.fromEntries(Object.entries(o).sort((a, b) => b[1] - a[1]));
    };
    return {
      status: "experimental heuristic: flags are prompts for a person, not findings",
      sentences: results.length, placed: placed.length,
      flagged: results.filter((r) => r.flags.length).length,
      evidence_footer: { by_warrant: share("warrant"), by_field: share("owner") },
      results,
    };
  }

  return { classify, wholeView, map, relate, audit, evidenceFor, codes };
}
