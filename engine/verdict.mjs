// Ordered verdicts. First match wins. The word true is never returned.
// SEVERITY is what summary.worst uses. It is not the first-match order.
// Same warrant strength on both sides is contested. A stronger contradicting
// span, or a contradicting span alone, is contradicted.
import { ceilingOk, rank, warrantCeiling } from "./certainty.mjs";

export const ORDER = ["out_of_scope", "contradicted", "contested", "overstated", "supported", "unverified"];
export const SEVERITY = ["contradicted", "overstated", "contested", "unverified", "out_of_scope", "supported"];

function ceil(code) {
  return rank(warrantCeiling(code));
}

function shown(evidence, checks) {
  for (const item of evidence || []) {
    if (item.by === "rule" && (item.relation === "entails" || item.relation === "contradicts")) {
      if (String(item.quote || item.ref || "").trim()) return true;
    }
  }
  for (const item of checks || []) {
    if (item.id && item.kind !== "missing_hypotheses" && (item.result === "consistent" || item.result === "contradicted")) {
      return true;
    }
  }
  return false;
}

function guardVerdict(out) {
  if ((out.verdict === "supported" || out.verdict === "contradicted") && !shown(out.evidence, out.checks)) {
    out.verdict = "unverified";
    out.qualifier = null;
    out.status = "unverified (model reasoning)";
    out.status_note = "downgraded: verdict without shown evidence";
  }
  return out;
}

export function combine(placement, wreq, cert, evidenceIn, checksIn, contested = false, flags = {}) {
  const reasons = [];
  const evidence = [...(evidenceIn || [])];
  const checks = [...(checksIn || [])];
  const level = (cert && cert.level) || "hedged";
  const code = wreq && wreq.code;
  const rule = evidence.filter((e) => e.by === "rule");
  const entails = rule.filter((e) => e.relation === "entails");
  const contradicts = rule.filter((e) => e.relation === "contradicts");
  const modelContra = evidence.filter((e) => e.by === "model" && e.relation === "contradicts");
  const held = [];
  for (const e of entails.concat(contradicts)) if (e.warrant_held) held.push(e.warrant_held);
  const passed = checks.filter((c) => c.result === "consistent" && c.kind !== "missing_hypotheses");
  const failed = checks.filter((c) => c.result === "contradicted" && c.kind !== "missing_hypotheses");
  const missingHyp = checks.filter((c) => c.kind === "missing_hypotheses");
  for (const c of passed.concat(failed)) if (c.warrant_held) held.push(c.warrant_held);
  let wheld = null;
  for (const item of held) {
    if (wheld == null || ceil(item) > ceil(wheld)) wheld = item;
  }

  function pack(verdict, qualifier, status) {
    const sources = rule.filter((e) => e.by === "rule").map((e) => String(e.quote || e.ref || "").slice(0, 200));
    for (const c of checks) if (c.id) sources.push(c.id);
    const out = guardVerdict({
      verdict, qualifier, reason: reasons, status, warrant_held: wheld,
      certainty_without_evidence: false, evidence, checks,
      sources: sources.filter(Boolean),
    });
    if (flags.ik && !["unverified", "contested", "out_of_scope"].includes(out.verdict)) {
      reasons.push("IK placements stay provisional until Māori-led review.");
      out.verdict = "unverified";
      out.qualifier = null;
      out.status = "proposed";
    }
    if (out.verdict === "true") {
      out.verdict = "unverified";
      reasons.push("R18: no verdict is true.");
    }
    return out;
  }

  if (failed.length) {
    const item = failed[0];
    reasons.push(`R21: check ${item.id} failed. ${item.note || ""}`.trim());
    const status = item.kind === "equation_small_cases" ? "contradicted (small cases)" : "tested";
    return pack("contradicted", null, status);
  }
  if (flags.instruction || flags.question || flags.w13) {
    if (flags.question) reasons.push("R18: the text is a question, not a claim.");
    else if (flags.instruction) reasons.push("R18: the text reads as an instruction, not a claim.");
    else reasons.push("W13 does not license a measurement, a date, a legal duty, or a word meaning.");
    return pack("out_of_scope", null, "proposed");
  }
  function strongest(items) {
    let best = null;
    for (const item of items) {
      if (!item.warrant_held) continue;
      if (best == null || ceil(item.warrant_held) > ceil(best)) best = item.warrant_held;
    }
    return best;
  }
  const bound = Boolean(entails.length || contradicts.length || passed.length);
  if (entails.length && contradicts.length) {
    const entailHeld = strongest(entails);
    const contraHeld = strongest(contradicts);
    if (ceil(contraHeld) > ceil(entailHeld)) {
      reasons.push(`R20: span ${contradicts[0].ref} contradicts the claim.`);
      return pack("contradicted", null, "source_found");
    }
    if (ceil(contraHeld) === ceil(entailHeld)) {
      reasons.push("R20: support and contradiction hold the same warrant, so the claim is contested.");
      return pack("contested", null, "source_found");
    }
    contradicts.length = 0;
  } else if (contradicts.length) {
    reasons.push(`R20: span ${contradicts[0].ref} contradicts the claim.`);
    return pack("contradicted", null, "source_found");
  }
  if (contested && (placement || bound)) {
    const cross = evidence.filter((e) => e.relation === "cross");
    if (cross.length) reasons.push(`R21: ${cross[0].ref} states the opposing claim, so the pair is contested.`);
    else reasons.push("R6: the claim is marked open or contested, or the evidence disagrees with itself.");
    return pack("contested", null, "proposed");
  }
  const small = passed.filter((c) => c.kind === "equation_small_cases");
  const onlyNone = small.some((c) => c.model_claim === "none" || c.model_claim === "only");
  const evidenceExists = Boolean(entails.length || passed.length || contradicts.length);
  const above = wheld != null && !ceilingOk(level, wheld);
  const weaker = wheld != null && code != null && ceil(wheld) < ceil(code);
  const establishedSoft = rule.some((e) => e.relation === "entails" && (e.status === "proposed" || e.status === "conditions_checked"));
  if (missingHyp.length) {
    reasons.push(missingHyp[0].note);
    return pack("overstated", null, "proposed");
  }
  if (onlyNone && small.length && !failed.length) {
    reasons.push("R19: an only or none claim rests on a small-case search alone.");
    return pack("overstated", "small cases", "proposed");
  }
  const smallOnly = Boolean(small.length) && !entails.length && passed.every((c) => c.kind === "equation_small_cases");
  if (smallOnly && above) {
    reasons.push(`R19: stated certainty ${level} exceeds what a small-case search can hold.`);
    return pack("overstated", "small cases", "proposed");
  }
  if (evidenceExists && !smallOnly && (above || weaker || establishedSoft)) {
    if (above) reasons.push(`R19: stated certainty ${level} exceeds the ${wheld} ceiling.`);
    if (weaker) reasons.push(`R19: warrant held ${wheld} is weaker than warrant required ${code}.`);
    if (establishedSoft) reasons.push("R15: the claim is stated as established while the evidence is not.");
    return pack("overstated", null, "proposed");
  }
  let meets = false;
  let checkMeet = [];
  const warrantOk = code == null || (wheld != null && ceil(wheld) >= ceil(code));
  if (entails.length && wheld && warrantOk && ceilingOk(level, wheld)) {
    meets = true;
    reasons.push(`R20: span ${entails[0].ref} entails the claim at ${wheld}.`);
  }
  checkMeet = passed.filter((c) => c.kind === "arithmetic" && (code == null || ceil(c.warrant_held) >= ceil(code)));
  if (checkMeet.length && ceilingOk(level, checkMeet[0].warrant_held)) {
    meets = true;
    reasons.push(`R18: check ${checkMeet[0].id} passed.`);
  }
  if (meets && !contradicts.length && !failed.length) {
    return pack("supported", null, checkMeet.length ? "tested" : "source_found");
  }
  if (small.length && !onlyNone && ceilingOk(level, "W9")) {
    reasons.push("R18: a small-case search found no counterexample in range. This is not a proof.");
    return pack("supported", "small cases", "tested");
  }
  if (!placement && !bound) {
    reasons.push("R18: the engine abstained, so the text is out of scope.");
    return pack("out_of_scope", null, "proposed");
  }
  if (modelContra.length) reasons.push("R22: a model noted a possible contradiction. That alone is not a verdict.");
  if (level !== "hedged" && !evidenceExists) {
    reasons.push("R19: certainty without evidence.");
    const out = pack("unverified", null, modelContra.length ? "unverified (model reasoning)" : "proposed");
    out.certainty_without_evidence = true;
    return out;
  }
  if (!reasons.length) reasons.push("R18: no evidence met the bar. The verdict is unverified.");
  return pack("unverified", null, modelContra.length ? "unverified (model reasoning)" : "proposed");
}
