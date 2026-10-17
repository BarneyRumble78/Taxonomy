// ClaimGuard for the Worker. A port of engine/v3/claimguard.py. Rules only unless llm is passed.
import lex from "./lexicon.json" with { type: "json" };
import { certainty } from "./certainty.mjs";
import { matchSpans, registryHits, numbersAgree, words, NEG } from "./evidence.mjs";
import { combine, ORDER } from "./verdict.mjs";
import { rank, warrantCeiling } from "./certainty.mjs";
import {
  CONFIDENCE_FLOOR, instructionHeuristic, rulePlacement, splitSentences,
} from "./rules.mjs";
import { classifyClaimType, DEFAULT_WARRANT, REQUIRED_WARRANT } from "./adjudicate.mjs";

const TRAD = /\b(?:scripture|sacred|revealed|tradition holds|the church teaches|doctrine|canon)\b/i;
const DATED = /\b(?:1[0-9]{3}|20[0-9]{2})\b|\b\d+(?:\.\d+)?\s?(?:%|kg|km)\b/i;
const DUTY = /\bmust\b|\blegal duty\b|\bact (?:19|20)\d\d\b/i;
const SENSE = /\bmeans\b|\bdefinition of the word\b/i;
const QUESTION = /\?\s*$/;
const HYP = /\b(?:if|assume|assumed|hypothesis|hypotheses|given|let|where|provided that|suppose)\b/i;
const THEOREM = /\btheorem\b/i;
const OPEN = /\b(?:open problem|remains open|is open|still open|contested|unresolved)\b/i;
const EQ = /(?<a>-?\d*)\s*\*?\s*(?<x>[a-z])\s*(?:\^|\*\*|²)\s*2?\s*(?<sign>[+-])\s*(?<b>\d*)\s*\*?\s*(?<y>[a-z])\s*(?:\^|\*\*|²)\s*2?\s*=\s*(?<c>-?\d+)/gi;
const NONE = /\bno\b.{0,40}\bsolutions?\b/i;
const ONLY = /\bonly\b|\bunique\b/i;
const PAIR = /\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)/g;
const ARITH = /(-?\d+(?:\.\d+)?)\s*(×|\*|x|times|\+|-|\/|÷|divided by)\s*(-?\d+(?:\.\d+)?)\s*=\s*(-?\d+(?:\.\d+)?)/gi;

function coef(raw) {
  raw = (raw || "").trim();
  if (raw === "" || raw === "+") return 1;
  if (raw === "-") return -1;
  return parseInt(raw, 10);
}

function checkEquations(text, limit = 40) {
  if (!text) return [];
  const seen = new Set();
  const reports = [];
  EQ.lastIndex = 0;
  for (const m of text.matchAll(EQ)) {
    const a = coef(m.groups.a);
    const sign = m.groups.sign === "+" ? 1 : -1;
    const b = sign * (m.groups.b ? parseInt(m.groups.b, 10) : 1);
    const c = parseInt(m.groups.c, 10);
    const key = `${a},${b},${c}`;
    if (seen.has(key) || (a === 0 && b === 0)) continue;
    seen.add(key);
    const found = [];
    for (let x = -limit; x <= limit; x++) {
      for (let y = -limit; y <= limit; y++) {
        if (a * x * x + b * y * y === c) {
          found.push([x, y]);
          if (found.length >= 32) break;
        }
      }
      if (found.length >= 32) break;
    }
    reports.push({ equation: `${a}*x^2 + (${b})*y^2 = ${c}`, range: limit, solutions: found, truncated: found.length >= 32 });
  }
  if (!reports.length) return [];
  const claimedNone = NONE.test(text);
  PAIR.lastIndex = 0;
  const pairs = new Set([...text.matchAll(PAIR)].map((m) => `${parseInt(m[1], 10)},${parseInt(m[2], 10)}`));
  const claimedOnly = ONLY.test(text) && pairs.size ? pairs : null;
  const found = new Set();
  for (const rep of reports) for (const p of rep.solutions) found.add(`${p[0]},${p[1]}`);
  let consistent = true;
  if (claimedNone && found.size) consistent = false;
  if (claimedOnly) {
    for (const item of found) if (!claimedOnly.has(item)) consistent = false;
    if (!found.size) consistent = false;
  }
  const note = "Small integers were searched. That can catch a false 'none' or 'only' claim. It does not prove how many solutions exist.";
  const modelClaim = claimedNone ? "none" : (claimedOnly ? "only" : null);
  return [{
    id: "eq1",
    kind: "equation_small_cases",
    result: consistent ? "consistent" : "contradicted",
    note,
    model_claim: modelClaim,
    warrant_held: "W2",
  }];
}

function applyOp(op, a, b) {
  if (op === "×" || op === "*" || op === "x" || op === "times") return a * b;
  if (op === "+") return a + b;
  if (op === "-") return a - b;
  if (op === "/" || op === "÷" || op === "divided by") return b === 0 ? null : a / b;
  return null;
}

function checkArithmetic(claim) {
  const reports = [];
  ARITH.lastIndex = 0;
  let i = 0;
  for (const m of String(claim || "").matchAll(ARITH)) {
    if (m[0].includes("^") || m[0].includes("²")) continue;
    i += 1;
    const got = applyOp(m[2].toLowerCase(), Number(m[1]), Number(m[3]));
    if (got == null) continue;
    const ok = Math.abs(got - Number(m[4])) <= 1e-9;
    reports.push({
      id: `arith${i}`,
      kind: "arithmetic",
      result: ok ? "consistent" : "contradicted",
      note: `${m[0]} ${ok ? "holds" : "does not hold"} as arithmetic.`,
      warrant_held: "W2",
    });
  }
  return reports;
}

function checkHypotheses(claim) {
  if (!THEOREM.test(claim || "")) return [];
  if (HYP.test(claim || "")) return [];
  return [{
    id: "hyp1", kind: "missing_hypotheses", result: "contradicted",
    note: "R5: a named theorem does not state its hypotheses.", warrant_held: null,
  }];
}

function runChecks(claim) {
  return checkArithmetic(claim).concat(checkEquations(claim), checkHypotheses(claim));
}

export function requiredWarrant(placement, text) {
  const kind = classifyClaimType(text);
  if (kind && REQUIRED_WARRANT[kind]) return { code: REQUIRED_WARRANT[kind], from: "claim_type", claim_type: kind };
  const owner = placement && placement.owner;
  return { code: owner ? (DEFAULT_WARRANT[owner] || null) : null, from: "owner", claim_type: null };
}

function andSplit(sentence) {
  const bits = sentence.split(" and ");
  if (bits.length === 2 && bits.every((b) => (b.match(/[A-Za-z0-9]+/g) || []).length >= 6)) {
    return bits.map((b) => b.trim()).filter(Boolean);
  }
  return [sentence.trim()].filter(Boolean);
}

export async function splitClaims(text, llm = null, maxClaims = 20) {
  const raw = text || "";
  let pieces = [];
  for (const sentence of splitSentences(raw)) pieces.push(...andSplit(sentence));
  if (llm) {
    try {
      const proposed = await Promise.resolve(llm(`Split into atomic claims. Reply JSON {"claims": [...]} of substrings.\n${raw.slice(0, 4000)}`));
      const extra = proposed && proposed.claims;
      if (Array.isArray(extra)) {
        const low = raw.toLowerCase();
        const kept = extra.map((item) => String(item).trim()).filter((bit) => bit && low.includes(bit.toLowerCase()));
        if (kept.length) pieces = kept;
      }
    } catch { /* a model split that fails is ignored */ }
  }
  let cursor = 0;
  const out = [];
  for (const bit of pieces.slice(0, maxClaims)) {
    let idx = raw.indexOf(bit, cursor);
    if (idx < 0) idx = raw.toLowerCase().indexOf(bit.toLowerCase(), cursor);
    const span = idx >= 0 ? [idx, idx + bit.length] : [0, 0];
    if (idx >= 0) cursor = span[1];
    out.push({ id: `c${out.length + 1}`, text: bit, span });
  }
  return out.length ? out : [{ id: "c1", text: raw.trim(), span: [0, raw.length] }];
}

function w13(text, placement) {
  const owner = placement && placement.owner;
  if (owner === "RE" || owner === "IK") return false;
  if (!TRAD.test(text || "")) return false;
  return DATED.test(text || "") || DUTY.test(text || "") || SENSE.test(text || "");
}

function siblings(rows) {
  const flags = {};
  for (const a of rows) {
    for (const b of rows) {
      if (a === b) continue;
      if (!NEG.test(b.text) || NEG.test(a.text)) continue;
      const wa = words(a.text);
      const wb = new Set(words(b.text));
      if (!wa.length || wa.filter((w) => wb.has(w)).length / wa.length < 0.6) continue;
      if (numbersAgree(a.text, b.text) === false) continue;
      const sa = rank(warrantCeiling(a.warrant_required && a.warrant_required.code));
      const sb = rank(warrantCeiling(b.warrant_required && b.warrant_required.code));
      if (!flags[a.id]) flags[a.id] = sb > sa ? "stronger" : "same";
    }
  }
  return flags;
}

export async function verify(text, sources = null, toolOutputs = null, options = {}) {
  const llm = options.llm || null;
  const split = options.split || "rule";
  const maxClaims = options.max_claims || 20;
  const claims = await splitClaims(text, split === "model" ? llm : null, maxClaims);
  const built = await Promise.all(claims.map(async (claim) => {
    const sentence = claim.text;
    const instruction = instructionHeuristic(sentence) || QUESTION.test(sentence || "");
    let placement = instruction ? null : rulePlacement(sentence, lex);
    if (placement && placement.confidence != null && placement.confidence < CONFIDENCE_FLOOR) placement = null;
    const wreq = requiredWarrant(placement, sentence);
    let evidence = []
      .concat(matchSpans(sentence, sources || [], "source"))
      .concat(matchSpans(sentence, toolOutputs || [], "tool_output"))
      .concat(registryHits(sentence));
    if (llm && ((sources && sources.length) || (toolOutputs && toolOutputs.length))) {
      try {
        const blob = JSON.stringify({ claim: sentence, sources: sources || [], tools: toolOutputs || [] }).slice(0, 8000);
        const reply = (await Promise.resolve(llm(`Label entailment. Reply JSON {"relation":"entails|contradicts|neutral","quote":""}.\n${blob}`))) || {};
        const rel = String(reply.relation || "neutral");
        if (rel === "entails" || rel === "contradicts") {
          evidence.push({
            kind: "source", ref: "model", quote: String(reply.quote || "").slice(0, 240),
            span: [0, 0], relation: rel, warrant_held: null, by: "model",
          });
        }
      } catch { /* advisory model failure stays rules-only */ }
    }
    return {
      claim, text: sentence, placement, wreq, evidence,
      checks: instruction ? [] : runChecks(sentence),
      instruction, open: OPEN.test(sentence), w13: w13(sentence, placement),
      cert: certainty(sentence),
    };
  }));
  const prepared = built.map((row) => ({ id: row.claim.id, text: row.text, warrant_required: row.wreq }));
  const sibling = siblings(prepared);
  const results = built.map((row) => {
    const contested = row.open || sibling[row.claim.id] === "same";
    if (sibling[row.claim.id] === "stronger") {
      row.evidence.push({
        kind: "source", ref: "sibling", quote: "another claim in this text",
        span: [0, 0], relation: "contradicts", warrant_held: row.wreq.code, by: "rule",
      });
    }
    const decided = combine(row.placement, row.wreq, row.cert, row.evidence, row.checks, contested, {
      instruction: row.instruction, w13: row.w13, ik: row.placement && row.placement.owner === "IK",
    });
    const mismatch = Boolean(
      row.placement && row.wreq.code && row.placement.warrant && row.wreq.code !== row.placement.warrant
    );
    return {
      id: row.claim.id,
      text: row.text,
      span: row.claim.span,
      placement: row.placement ? {
        owner: row.placement.owner, cell: row.placement.cell, warrant: row.placement.warrant,
        method: row.placement.method, confidence: row.placement.confidence,
      } : null,
      warrant_required: row.wreq,
      warrant_mismatch: mismatch,
      certainty: { level: row.cert.level, cues: row.cert.cues, ceiling_ok: decided.verdict !== "overstated" },
      evidence: decided.evidence || [],
      checks: decided.checks || [],
      verdict: decided.verdict,
      qualifier: decided.qualifier,
      reason: decided.reason || [],
      status: decided.status,
      certainty_without_evidence: Boolean(decided.certainty_without_evidence),
    };
  });
  const counts = Object.fromEntries(ORDER.map((name) => [name, 0]));
  for (const row of results) counts[row.verdict] = (counts[row.verdict] || 0) + 1;
  const worst = ORDER.find((name) => counts[name]) || "unverified";
  return {
    version: "claimguard-0.1",
    engine: "3.0.0",
    claims: results,
    summary: { worst, counts },
  };
}
