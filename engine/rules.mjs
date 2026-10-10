// Rule stage for Taxonomy. Python engine/taxonomy_engine.py must match this file.
// scripts/build_site.py inlines it into the Minerva page. The Worker imports it.
// Retrieval and the model are not in this file. The page cannot run them.

export const CONFIDENCE_FLOOR = 0.4;
export const CONFIDENCE_NOTE = "Confidence is a ratio of cue-word scores, not a probability.";
export const LAW_CUE = /\bact (19|20)\d\d\b|\bunder the [a-z ]+act\b/;
// Heuristic only. Failure to classify an instruction-like imperative is not a security guarantee.
export const INSTRUCTION_HEURISTIC = /\b(?:ignore|disregard|forget)\b.{0,80}\b(?:previous|prior|above)\b|\breveal\b.{0,40}\bsystem prompt\b/i;
export const PROOF_VERBS = new Set(["prove", "proof"]);
export const WARRANT_ORDER = ["W1", "W2", "W3", "W4", "W5", "W6", "W7", "W8", "W9", "W10", "W11", "W12", "W13"];
export const DEFAULT_WARRANT = {MA:"W1",PH:"W4",CH:"W3",BI:"W3",EA:"W4",MD:"W3",EN:"W11",CS:"W1",MS:"W3",EC:"W5",BU:"W12",ST:"W9",PO:"W6",LA:"W10",PL:"W9",HI:"W7",LN:"W4",AR:"W8",RE:"W8",ED:"W3",DE:"W4",AG:"W3",EV:"W5",IS:"W4",IK:"W13"};
export const WARRANT_TO_METHOD = {W1:"M2",W2:"M5",W3:"M4",W4:"M3",W5:"M3",W6:"M6",W7:"M3",W8:"M6",W9:"M2",W10:"M2",W11:"M7",W12:"M1",W13:"M1"};
export const WARRANT_NAMES = {W1:"Proof",W2:"Computation with error bound",W3:"Controlled intervention",W4:"Measurement with uncertainty",W5:"Causal identification",W6:"Comparative inference",W7:"Source criticism of a dated record",W8:"Interpretation traced to a record",W9:"Argument",W10:"Source and proof before a forum",W11:"Verification against a specification",W12:"Stipulation or convention",W13:"Tradition-internal authority"};
export const METHOD_NAMES = {M1:"Represent",M2:"Derive",M3:"Observe",M4:"Intervene",M5:"Compute",M6:"Compare and reconstruct",M7:"Verify"};

const CUE_RE = new Map();
const STEMS = new Set(["topolog","diagnos","electromagnet","bacteri","mitochondri","descend","phylogen","geolog","manufactur","simulat","randomi","catalogu","morpholog","theolog","religio","pedagog","classif","certif","turbulen","concurren","serialis","hippocamp","ontolog","epistem","commemorat","revitalis","accessib","purif","chromatograph","spectroscop","electr","cosmolog","vaccin","escalat","kaitiaki","depress","axiom","reconstruct","interpret","convention"]);
const EXACT = new Set(["force"]);
const SUFFIX = "(?:led|ies|ing|ers|ally|es|ed|er|s)";
const MILITARY = /\b(?:armed forces|air force|ground forces|military|troops?|soldiers?|armies|army|navies|navy|brigades?|battalions?|artillery|missiles?|airstrikes?|air strikes?|warships?|naval mines?|sea mines?|minefields?|minelaying|battlefield|invasions?|invaded|bombard(?:ment|ed|ing)?|casualt(?:y|ies)|enem(?:y|ies)|offensives?|garrisons?|warplanes?|drone strikes?|shelling|blockades?|weapons?|flanks?|munitions?)\b/;
const NAVAL_MINE = /\b(?:naval mines?|sea mines?|minefields?|minelaying)\b|\b(?:naval|sea|harbour|harbor|strait|shipping|waterway|channel)\b(?:\W+\w+){0,6}?\W+\bmines?\b|\bmines?\b(?:\W+\w+){0,6}?\W+\b(?:strait|shipping|harbour|harbor|naval|waterway|laid)\b/;
const PHYSICS_FORCE = /\b(?:newtons?|particles?|mass|gravity|gravitational|momentum|acceleration|electromagnetic|intermolecular|net force|inertial|torque|vectors?)\b/;
const NOT_ARMED = /\b(?:labour|labor|work)\s+forces?\b|\bworkforce\b|\bmarket forces\b|\bcompetitive forces\b|\beconomic forces\b|\bsocial forces\b|\bdriving forces\b/;
const CYBER = /\b(?:malware|ransomware|phishing|phish|zero-day|passwords?|encrypt(?:ion|ed)?)\b/;
const YEAR = /\b(?:1[0-9]{3}|20[0-9]{2})\b/;
const MINE_CUES = ["naval mine", "sea mine", "minefield", "minelaying"];

// Python round(x, 2): exact halves go to even.
export function pyRound2(x) {
  const r = x * 100;
  const f = Math.floor(r + 1e-10);
  if (Math.abs(r - f - 0.5) < 1e-8) return ((f % 2 === 0 ? f : f + 1) / 100);
  return Math.round(r) / 100;
}

function escapeRe(s) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

// Left boundary, then a word boundary or a light inflection. Stems may continue
// the word. "force" is exact, so it does not match "forces".
export function cueHit(text, cue) {
  let re = CUE_RE.get(cue);
  if (!re) {
    const raw = cue.toLowerCase();
    let body;
    if (raw.endsWith(" ")) body = "(?<![a-z0-9])" + escapeRe(raw);
    else if (/^[a-z0-9]+$/.test(raw)) {
      if (STEMS.has(raw)) body = "(?<![a-z0-9])" + escapeRe(raw);
      else if (EXACT.has(raw)) body = "(?<![a-z0-9])" + escapeRe(raw) + "(?![a-z0-9])";
      else body = "(?<![a-z0-9])" + escapeRe(raw) + SUFFIX + "?(?![a-z0-9])";
    } else {
      const parts = raw.split(" ");
      const head = parts.slice(0, -1);
      const last = parts[parts.length - 1];
      let prefix = head.map(escapeRe).join("\\s+");
      if (prefix) prefix += "\\s+";
      let lastRe;
      if (/^\d+$/.test(last)) lastRe = escapeRe(last) + "(?![a-z])";
      else if (STEMS.has(last)) lastRe = escapeRe(last);
      else lastRe = escapeRe(last) + SUFFIX + "?(?![a-z0-9])";
      body = "(?<![a-z0-9])" + prefix + lastRe;
    }
    re = new RegExp(body);
    CUE_RE.set(cue, re);
  }
  return re.test(text);
}

export function scoreCues(text, words, skip) {
  let n = 0;
  for (const w of words) {
    if (skip && skip.has(w)) continue;
    if (cueHit(text, w)) n += 1;
  }
  return n;
}

function fieldScore(text, field, skip) {
  const cells = field.cells.map((cl) => scoreCues(text, cl, skip));
  const score = scoreCues(text, field.kw, skip) + 0.5 * cells.reduce((a, b) => a + b, 0);
  return { score, cells };
}

function sense(text, lex, scores, cells) {
  const fields = lex.fields;
  if (/\bprime ministers?\b/.test(text)) {
    const skip = new Set(["prime"]);
    const other = Math.max(...Object.entries(scores).filter(([c]) => c !== "MA").map(([, v]) => v));
    if (other > 0) for (const w of PROOF_VERBS) skip.add(w);
    const again = fieldScore(text, fields.MA, skip);
    scores.MA = again.score;
    cells.MA = again.cells;
  }
  const physics = PHYSICS_FORCE.test(text);
  const labour = NOT_ARMED.test(text);
  const military = MILITARY.test(text) || NAVAL_MINE.test(text);
  const pluralForces = /\bforces\b/.test(text);
  if (!physics && !labour && (pluralForces || (military && /\bforce\b/.test(text)))) {
    const again = fieldScore(text, fields.PH, new Set(["force"]));
    scores.PH = again.score;
    cells.PH = again.cells;
  }
  const foreignAct = /\bforeign (?:state|power|government|military|attack|forces)\b/.test(text) || (
    /\b(?:prime ministers?|foreign ministers?|government)\b/.test(text) && /\b(?:foreign|attacked|attack)\b/.test(text)
  );
  const claimed = /\bclaimed responsibility\b/.test(text) && /\battacks?\b/.test(text);
  const computerish = CYBER.test(text) || /\b(?:software|computer|server|cyber|database|network)\b/.test(text);
  if ((military || foreignAct || claimed) && !CYBER.test(text)) {
    const again = fieldScore(text, fields.CS, new Set(["attack"]));
    scores.CS = again.score;
    cells.CS = again.cells;
  }
  if (claimed && scores.ST === 0 && !computerish) {
    cells.ST[3] += 1;
    scores.ST += 1.5;
  }
  if (NAVAL_MINE.test(text) && !MINE_CUES.some((cue) => cueHit(text, cue))) {
    cells.ST[3] += 1;
    scores.ST += 1.5;
  }
  if (military && scores.ST === 0) {
    cells.ST[3] += 1;
    scores.ST += 1.5;
  }
  if (/\b(?:prime ministers?|foreign ministers?|the government)\b/.test(text) && /\bforeign\b/.test(text)) scores.PO += 0.5;
  if (/\bland court\b/.test(text)) {
    const again = fieldScore(text, fields.IK, new Set(["land"]));
    scores.IK = again.score;
    cells.IK = again.cells;
  }
  if (YEAR.test(text) && scores.HI > 0 && !military && !pluralForces) {
    const again = fieldScore(text, fields.ST, new Set(["war"]));
    scores.ST = again.score;
    cells.ST = again.cells;
  }
}

function scoreAll(text, lex) {
  const scores = {};
  const cells = {};
  for (const [c, f] of Object.entries(lex.fields)) {
    const got = fieldScore(text, f);
    scores[c] = got.score;
    cells[c] = got.cells;
  }
  const others = Object.entries(scores).filter(([c]) => c !== "MA").map(([, v]) => v);
  const other = others.length ? Math.max(...others) : 0;
  if (other > 0) {
    const again = fieldScore(text, lex.fields.MA, PROOF_VERBS);
    scores.MA = again.score;
    cells.MA = again.cells;
  }
  sense(text, lex, scores, cells);
  return { scores, cells };
}

export function instructionHeuristic(sentence) {
  return INSTRUCTION_HEURISTIC.test(sentence || "");
}

// A trailing "under the … Act 1985" is its own segment. A statute glued onto
// another claim must not keep the whole sentence.
const TRAIL_ACT = /\s+under the [a-z ]+act (?:19|20)\d\d\.?$/i;

export function splitSentences(sentence) {
  let text = String(sentence || "");
  const pieces = [];
  while (true) {
    const m = text.match(TRAIL_ACT);
    if (!m || m.index === 0) {
      pieces.push(text);
      break;
    }
    pieces.push(text.slice(m.index));
    text = text.slice(0, m.index);
  }
  pieces.reverse();
  const parts = [];
  for (const chunk of pieces) {
    for (const bit of String(chunk).split(/(?<=[.!?])\s+(?=[A-Z])/)) {
      const s = bit.trim();
      if (s) parts.push(s);
    }
  }
  return parts.length ? parts : [String(sentence || "")];
}

function warrantKeys(lex) {
  const extra = Object.keys(lex.warrants || {}).filter((k) => !WARRANT_ORDER.includes(k));
  return WARRANT_ORDER.concat(extra);
}

// One sentence. No confidence gate and no retrieval. Null when nothing matched
// or the wording is an instruction-like imperative.
export function rulePlacement(sentence, lex) {
  if (instructionHeuristic(sentence)) return null;
  const t = " " + String(sentence || "").toLowerCase() + " ";
  const fields = lex.fields;
  const scored = scoreAll(t, lex);
  const scores = scored.scores;
  const cells = scored.cells;
  const ranked = Object.entries(scores).sort((a, b) => b[1] - a[1]);
  let owner = ranked[0][0];
  const top = ranked[0][1];
  if (top === 0) return null;
  if ((cueHit(t, "theorem") || cueHit(t, "question is open")) && scores.MA >= top - 1 && scores.MA > 0) owner = "MA";
  if (LAW_CUE.test(t) && scores.LA >= top - 2) owner = "LA";
  const cellScores = cells[owner] || [];
  const cellMax = cellScores.length ? Math.max(...cellScores) : 0;
  let idx = cellScores.indexOf(cellMax);
  let cell = null;
  if (owner === "MA" && t.includes("integral domain")) {
    idx = 1;
    cell = "MA.O.A2";
  } else if (cellMax > 0) {
    cell = owner + ".O.A" + (idx + 1);
  } else {
    idx = null;
  }
  const keys = warrantKeys(lex);
  const wvals = keys.map((k) => scoreCues(t, lex.warrants[k] || []));
  const wmax = Math.max(...wvals);
  const fallback = DEFAULT_WARRANT[owner] || null;
  let warrant;
  let defaultApplied;
  if (wmax > 0) {
    warrant = keys[wvals.indexOf(wmax)];
    const di = keys.indexOf(fallback);
    if (di >= 0 && wvals[di] >= wmax) warrant = fallback;
    defaultApplied = false;
    if (warrant === "W13" && owner !== "RE" && owner !== "IK") {
      warrant = fallback;
      defaultApplied = true;
    }
  } else {
    warrant = fallback;
    defaultApplied = true;
  }
  const method = warrant ? (WARRANT_TO_METHOD[warrant] || null) : null;
  const second = ranked.length > 1 ? ranked[1][1] : 0;
  const contested = ranked.slice(1, 4).filter(([c, s]) => s > 0 && s >= top - 1 && c !== owner).map(([c]) => c);
  return {
    owner, cell, cell_index: cell ? idx : null, warrant, default_applied: defaultApplied, method,
    confidence: pyRound2(top / (top + second + 1)),
    contested_with: contested,
  };
}

// Browser path: rules, then abstain under 0.40, and abstain when sentences do not share an owner.
// No retrieval. A placement here can still be one the API withholds.
export function stageRule(sentence, lex) {
  if (instructionHeuristic(sentence)) return { placement: null, reason: "instruction" };
  const parts = splitSentences(sentence);
  if (parts.length > 1) {
    const placed = parts.map((p) => rulePlacement(p, lex));
    const owners = placed.map((p) => (p ? p.owner : null));
    if (owners.some((o) => !o) || new Set(owners).size !== 1) return { placement: null, reason: "multi_sentence" };
    if (placed.some((p) => p.confidence < CONFIDENCE_FLOOR)) return { placement: null, reason: "low_confidence" };
    const full = rulePlacement(sentence, lex);
    if (!full || full.owner !== owners[0]) return { placement: null, reason: "multi_sentence" };
    if (full.confidence < CONFIDENCE_FLOOR) return { placement: null, reason: "low_confidence" };
    return { placement: full, reason: null };
  }
  const full = rulePlacement(sentence, lex);
  if (!full) return { placement: null, reason: "no_cue" };
  if (full.confidence < CONFIDENCE_FLOOR) return { placement: null, reason: "low_confidence" };
  return { placement: full, reason: null };
}

// retrievedField null means the embedding stage did not run. Disagreement abstains.
// The rejected field is not a placement.
export function adjudicate(staged, retrievedField) {
  if (staged.reason) return { placement: null, reason: staged.reason };
  if (retrievedField == null) return { placement: staged.placement, reason: null, retrieval: { status: "unavailable" } };
  if (retrievedField !== staged.placement.owner) return { placement: null, reason: "stages_disagree" };
  return { placement: staged.placement, reason: null, retrieval: { status: "agree", field: retrievedField } };
}

export function vectorNorm(vector) {
  let s = 0;
  for (const x of vector) s += x * x;
  return Math.sqrt(s);
}

// First field in index order wins an exact tie. Vectors may be unnormalised.
export function retrieveField(vector, index) {
  if (!vector || !vector.length || !index) return null;
  const qn = vectorNorm(vector);
  if (qn === 0) return null;
  let best = -Infinity;
  let field = null;
  const fields = index.fields;
  const vectors = index.vectors;
  for (let i = 0; i < fields.length; i++) {
    const v = vectors[i];
    let dot = 0;
    let cn = 0;
    for (let k = 0; k < v.length; k++) {
      dot += vector[k] * v[k];
      cn += v[k] * v[k];
    }
    const s = dot / (qn * Math.sqrt(cn));
    if (s > best) {
      best = s;
      field = fields[i];
    }
  }
  return field;
}
