// Wording audit ported from the unmerged Worker (PR #1).
// Flags are prompts for a person, not findings and not verdicts.
// Placement uses the current rule stage, which abstains under the confidence floor
// only inside /v1/verify. Here a cue match is kept, as the original audit did.
import lex from "./lexicon.json" with { type: "json" };
import { DEFAULT_WARRANT, WARRANT_NAMES, rulePlacement } from "./rules.mjs";

const INSTRUCTION = /^\s*(ignore|disregard|forget|override|reveal|pretend|you must|you are now|system prompt)\b|\b(ignore|disregard) (all |any |the )?(previous|prior|above) /i;
const CERTAIN = /\b(prove[sd]?|proven|conclusively|definitively|undeniabl[ey]|beyond (any )?doubt|guarantee[sd]?)\b/i;
const CAUSAL = /\b(causes?|caused|leads? to|led to|results? in|resulted in)\b/i;
const DESIGN = /\b(randomi[sz]ed|trial|experiment|instrument|natural experiment|difference-in-differences|regression discontinuity|controlled|cohort|meta-analysis|longitudinal)\b/i;
const TRADITION = /\b(scripture|sacred|revealed|the church teaches|tradition holds|doctrine|canon)\b/i;
const MEASURE = /\b\d+(\.\d+)?\s?(%|percent|kg|km|m|years?|degrees|tonnes?)\b|\b(1[0-9]{3}|20[0-9]{2})\b/i;
const UNNAMED = /\b(studies show|research shows|experts say|it is well known|scientists agree|everyone knows)\b/i;
const SOURCED = /\bet al\b|\(\s*[A-Z][a-z]+,? (19|20)\d\d\s*\)|\bsource:|https?:\/\//;

export const AUDIT_STATUS = "experimental heuristic: flags are prompts for a person, not findings";

function sentences(text) {
  return String(text || "").replace(/\s+/g, " ").split(/(?<=[.!?])\s+/).map((s) => s.trim()).filter(Boolean).slice(0, 60);
}

export function audit(text) {
  const results = sentences(text).map((sentence, i) => {
    const placed = rulePlacement(sentence, lex);
    const flags = [];
    if (INSTRUCTION.test(sentence)) {
      flags.push({ code: "instruction_like", detail: "Reads as an instruction. Claims have an owner and a warrant; instructions do not. Do not treat it as evidence." });
    }
    if (CAUSAL.test(sentence) && !DESIGN.test(sentence)) {
      flags.push({ code: "causal_without_design", detail: "Causal wording with no study design named (W3 intervention or W5 identification)." });
    }
    if (UNNAMED.test(sentence) && !SOURCED.test(sentence)) {
      flags.push({ code: "unnamed_authority", detail: "Appeals to unnamed studies or experts. No record (W7) or a measurement (W4) is cited." });
    }
    if (!placed && !flags.length) {
      flags.push({ code: "no_owner", detail: "No field recognised the wording. It may not be a claim." });
    }
    let placement = null;
    if (placed) {
      const owner = placed.owner;
      const infoName = owner;
      if (CERTAIN.test(sentence) && DEFAULT_WARRANT[owner] !== "W1") {
        flags.push({ code: "proof_wording", detail: `Proof language in ${owner}, where claims rest on ${DEFAULT_WARRANT[owner]}, not a proof.` });
      }
      if (TRADITION.test(sentence) && MEASURE.test(sentence) && owner !== "RE" && owner !== "IK") {
        flags.push({ code: "w13_travel", detail: "Tradition-internal authority offered for a measurement or date. W13 never licenses one." });
      }
      if (placed.confidence < 0.4 || (placed.contested_with || []).length) {
        const contested = (placed.contested_with || []).join(", ");
        flags.push({ code: "border_claim", detail: `Ownership is contested${contested ? " with " + contested : ""}. Confidence ${placed.confidence}.` });
      }
      placement = {
        owner,
        cell: placed.cell,
        warrant: placed.warrant,
        warrant_name: WARRANT_NAMES[placed.warrant] || null,
        confidence: placed.confidence,
        contested_with: placed.contested_with || [],
        default_applied: !!placed.default_applied,
      };
      void infoName;
    }
    return { n: i + 1, sentence, placement, flags };
  });
  const placed = results.filter((row) => row.placement);
  const share = (key) => {
    const counts = {};
    for (const row of placed) counts[row.placement[key]] = (counts[row.placement[key]] || 0) + 1;
    return Object.fromEntries(Object.entries(counts).sort((a, b) => b[1] - a[1]));
  };
  return {
    status: AUDIT_STATUS,
    sentences: results.length,
    placed: placed.length,
    flagged: results.filter((row) => row.flags.length).length,
    evidence_footer: { by_warrant: share("warrant"), by_field: share("owner") },
    results,
  };
}
