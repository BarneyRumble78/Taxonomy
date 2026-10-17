// Stated certainty and the R19 ceiling. Cues live in engine/certainty_lexicon.json.
import lex from "./certainty_lexicon.json" with { type: "json" };

export const LEVELS = lex.levels;
export const CEILING = lex.ceiling;
const RANK = Object.fromEntries(LEVELS.map((name, i) => [name, i]));
function cueRe(cue) {
  const body = cue.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const lead = /^\w/.test(cue) ? "\\b" : "";
  const trail = /\w$/.test(cue) ? "\\b" : "(?!\\w)";
  return new RegExp(lead + body + trail, "i");
}

const CUES = [];
for (const level of [...LEVELS].reverse()) {
  const cues = [...(lex.cues[level] || [])].sort((a, b) => b.length - a.length);
  for (const cue of cues) CUES.push([level, cue, cueRe(cue)]);
}

export function certainty(text) {
  const found = [];
  let best = "hedged";
  const raw = text || "";
  for (const [level, cue, pat] of CUES) {
    if (pat.test(raw)) {
      found.push(cue);
      if (RANK[level] > RANK[best]) best = level;
    }
  }
  return { level: best, cues: found };
}

export function rank(level) {
  return RANK[level] || 0;
}

export function warrantCeiling(code) {
  return (code && CEILING[code]) || "hedged";
}

export function ceilingOk(level, warrantHeld) {
  const cap = warrantHeld ? warrantCeiling(warrantHeld) : "hedged";
  return rank(level) <= rank(cap);
}
