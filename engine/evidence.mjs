// Bind a claim to an exact span. No fetching. Pyramid search is not evidence.
// Whitespace, case and Unicode quotes are normalised. Token overlap is not a match.
import registry from "../registry/registry.json" with { type: "json" };
import { rank, warrantCeiling } from "./certainty.mjs";

const NUM = /\d{1,2}:\d{2}|-?\d+(?:\.\d+)?/g;
const NEG = /\b(?:not|no|never|none|false|didn't|does not|do not|did not)\b/i;
const ID = /\b[A-Z]{2}\.[OMWB]\.[A-Z]?\d+(?:\.\d+)*\b/g;
const STOP = new Set("that this with from have were been into over under than then they them their which what when where while there these those also only such said says about after before between through would could should claim claims".split(" "));
const FRAME_STOP = new Set([...STOP, ..."the and for are was not but its his her you our has had who how any all can may per via out off does did doing done being".split(" ")]);
const TOKEN = /\d{1,2}:\d{2}|-?\d+(?:\.\d+)?|[a-z]+(?:'[a-z]+)?/g;
const LEAD = /^(?:(?:the|a|an|this)\s+)?(?:[\w']+\s+){0,3}?(?:conclusively\s+|definitely\s+)?(?:proves|shows|demonstrates|confirms|establishes)\s+/i;
const SPLIT = /\s+\bbut\b\s+|;\s*|(?<=[.?!])\s+/gi;
const TRIAL = /\b(?:randomi[sz]ed|controlled trial|clinical trial|cohort stud(?:y|ies)|meta-analysis|trial)\b/i;
const MEASURE = /\b(?:measured|measurement|sensor reading)\b|\bppb\b|\bppm\b|parts per (?:billion|million)/i;
const PROOF = /\b(?:qed|quod erat demonstrandum|we prove that|proof:)\b/i;
const QUOTES = { "\u2018": "'", "\u2019": "'", "\u2032": "'", "\u201c": '"', "\u201d": '"', "\u00ab": '"', "\u00bb": '"', "\u2033": '"' };
export const TOOL_WARRANT = {
  calculator: "W2", compute: "W2", arithmetic: "W2",
  test: "W11", test_runner: "W11", runner: "W11",
  sensor: "W4", reading: "W4", api: "W4",
  search: "W7", snippet: "W7",
};
const WARRANTS = new Set(Array.from({ length: 13 }, (_, i) => "W" + (i + 1)));
const ROWS = new Map(registry.filter((row) => row && row.id).map((row) => [row.id, row]));
const DOWN = new Set("lower decrease decreased decreases decreasing fell fall falling falls reduced reduce reduces reducing down".split(" "));
const UP = new Set("higher increase increased increases increasing rose rise rising rises raised raise raises raising up".split(" "));
const DAYS = new Set("monday tuesday wednesday thursday friday saturday sunday".split(" "));
const POLAR = new Set("not no never none false dont doesnt didnt isnt arent wasnt werent".split(" "));
const UNITS = new Set("ppb ppm percent degree degrees foot feet metre metres meter meters million billion kg km dollar dollars".split(" "));
const UNIT_ALIAS = { meter: "metre", meters: "metres", degree: "degrees", foot: "feet", dollar: "dollars" };

function ceil(code) {
  return rank(warrantCeiling(code));
}

export function numbers(text) {
  return String(text || "").match(NUM) || [];
}

function numKey(token) {
  if (/^\d{1,2}:\d{2}$/.test(token || "")) return token;
  const n = Number(token);
  return Number.isFinite(n) ? String(Number(n.toPrecision(10))) : token;
}

export function numbersAgree(claim, quote, relTol = 0) {
  const wanted = numbers(claim);
  if (!wanted.length) return null;
  const have = numbers(quote);
  if (relTol) {
    return wanted.every((a) => {
      if (String(a).includes(":")) return have.includes(a);
      const fa = Number(a);
      return have.some((b) => !String(b).includes(":") && Math.abs(Number(b) - fa) <= relTol * Math.max(1, Math.abs(fa)));
    });
  }
  const keys = new Set(have.map(numKey));
  return wanted.every((n) => keys.has(numKey(n)));
}

function flatten(obj) {
  const parts = [];
  function walk(node, key) {
    if (node && typeof node === "object" && !Array.isArray(node)) {
      for (const [k, v] of Object.entries(node)) walk(v, k);
    } else if (Array.isArray(node)) {
      for (const v of node) walk(v, key);
    } else {
      if (key != null) parts.push(String(key).replace(/_/g, " "));
      if (node != null && typeof node !== "boolean") parts.push(String(node));
    }
  }
  walk(obj, null);
  return parts.join(" ");
}

function rawText(doc) {
  if (doc.output && typeof doc.output === "object") return flatten(doc.output);
  if (doc.text && typeof doc.text === "object") return flatten(doc.text);
  return String(doc.text || doc.output || "");
}

function grade(doc, kind) {
  if (kind !== "source") {
    const tool = String((doc && doc.tool) || "").toLowerCase().replace(/ /g, "_");
    return TOOL_WARRANT[tool] || "W7";
  }
  const text = rawText(doc);
  if (PROOF.test(text)) return "W1";
  if (TRIAL.test(text)) return "W3";
  if (MEASURE.test(text)) return "W4";
  return "W7";
}

export function warrantFields(doc, kind) {
  const graded = grade(doc, kind);
  const declared = String((doc && doc.warrant) || "").toUpperCase();
  const caller = WARRANTS.has(declared);
  let held = graded;
  if (caller && graded && ceil(declared) < ceil(graded)) held = declared;
  return { warrant_held: held, warrant_graded: graded, warrant_declared_by_caller: caller };
}

export function warrantOf(doc, kind) {
  return warrantFields(doc, kind).warrant_held;
}

export function words(text) {
  return (String(text || "").toLowerCase().match(/[a-z0-9]+/g) || []).filter((w) => w.length > 3 && !STOP.has(w));
}

function normalize(text) {
  const raw = text || "";
  const out = [];
  const origin = [];
  let pending = false;
  let started = false;
  for (let i = 0; i < raw.length; i++) {
    let ch = QUOTES[raw[i]] || raw[i];
    const low = ch.toLowerCase();
    if (/\s/.test(low) || "?!;,".includes(low)) {
      if (started) pending = true;
      continue;
    }
    if (low === ".") {
      const prevDigit = i > 0 && /\d/.test(raw[i - 1]);
      const nextDigit = i + 1 < raw.length && /\d/.test(raw[i + 1]);
      if (!(prevDigit && nextDigit)) {
        if (started) pending = true;
        continue;
      }
    }
    if (low === ":") {
      const prevDigit = i > 0 && /\d/.test(raw[i - 1]);
      const nextDigit = i + 1 < raw.length && /\d/.test(raw[i + 1]);
      if (!(prevDigit && nextDigit)) {
        if (started) pending = true;
        continue;
      }
    }
    if (pending && out.length) {
      out.push(" ");
      origin.push(i);
      pending = false;
    }
    out.push(low);
    origin.push(i);
    started = true;
  }
  return [out.join(""), origin];
}

function sliceSpan(body, norm, origin, needle, claim = "") {
  if (!needle) return null;
  const idx = norm.indexOf(needle);
  if (idx < 0 || idx >= origin.length) return null;
  const last = idx + needle.length - 1;
  if (last >= origin.length) return null;
  const start = origin[idx];
  let end = origin[last] + 1;
  if (end < body.length && ".?!".includes(body[end]) && String(claim || "").trimEnd().endsWith(body[end])) end += 1;
  return [body.slice(start, end), [start, end]];
}

function atoms(norm) {
  const toks = String(norm || "").match(TOKEN) || [];
  const merged = [];
  for (let i = 0; i < toks.length; i++) {
    if (toks[i] === "parts" && toks[i + 1] === "per" && (toks[i + 2] === "billion" || toks[i + 2] === "million")) {
      merged.push(toks[i + 2] === "billion" ? "ppb" : "ppm");
      i += 2;
      continue;
    }
    if (toks[i] === "per" && toks[i + 1] === "cent") {
      merged.push("percent");
      i += 1;
      continue;
    }
    merged.push(toks[i].replace(/'/g, ""));
  }
  let polar = false;
  const seq = [];
  for (const token of merged) {
    if (POLAR.has(token)) { polar = true; continue; }
    if (DOWN.has(token)) { seq.push(["dir", "down"]); continue; }
    if (UP.has(token)) { seq.push(["dir", "up"]); continue; }
    if (DAYS.has(token)) { seq.push(["day", token]); continue; }
    if (/^\d{1,2}:\d{2}$/.test(token)) { seq.push(["time", token]); continue; }
    if (/^-?\d+(?:\.\d+)?$/.test(token)) { seq.push(["num", numKey(token)]); continue; }
    if (UNITS.has(token)) { seq.push(["unit", UNIT_ALIAS[token] || token]); continue; }
    if (FRAME_STOP.has(token) || token.length <= 2) continue;
    seq.push(["word", token]);
  }
  return [seq, polar];
}

function sameAtom(a, b) {
  return a[0] === b[0] && a[1] === b[1];
}

function conflict(claimNorm, windowNorm) {
  const [cseq, cpol] = atoms(claimNorm);
  const [wseq, wpol] = atoms(windowNorm);
  const cdays = new Set(cseq.filter((a) => a[0] === "day").map((a) => a[1]));
  const wdays = new Set(wseq.filter((a) => a[0] === "day").map((a) => a[1]));
  if (cdays.size && wdays.size && (cdays.size !== wdays.size || [...cdays].some((d) => !wdays.has(d)))) {
    const shared = cseq.filter((a) => a[0] === "word").some((a) => wseq.some((b) => b[0] === "word" && b[1] === a[1]));
    if (shared) return "day";
  }
  if (cseq.length < 3 || wseq.length < 2) return null;
  if (cseq.length === wseq.length && cseq.every((a, i) => sameAtom(a, wseq[i]))) {
    return cpol !== wpol ? "polarity" : null;
  }
  if (cseq.length === wseq.length) {
    const diffs = cseq.map((a, i) => sameAtom(a, wseq[i]) ? -1 : i).filter((i) => i >= 0);
    if (diffs.length === 1 && cseq[diffs[0]][0] === wseq[diffs[0]][0]) return cseq[diffs[0]][0];
  }
  const cwords = cseq.filter((a) => a[0] === "word");
  const wwords = wseq.filter((a) => a[0] === "word");
  const cdir = new Set(cseq.filter((a) => a[0] === "dir").map((a) => a[1]));
  const wdir = new Set(wseq.filter((a) => a[0] === "dir").map((a) => a[1]));
  const dirDiff = cdir.size && wdir.size && (cdir.size !== wdir.size || [...cdir].some((d) => !wdir.has(d)));
  if (dirDiff && cwords.length && wwords.length) {
    let i = 0;
    while (i < cwords.length && i < wwords.length && sameAtom(cwords[i], wwords[i])) i += 1;
    let j = 0;
    while (j < cwords.length - i && j < wwords.length - i && sameAtom(cwords[cwords.length - 1 - j], wwords[wwords.length - 1 - j])) j += 1;
    if (i >= 2 && j >= 2) return "dir";
  }
  if (cwords.length === wwords.length && cwords.every((a, i) => sameAtom(a, wwords[i]))) {
    const cnums = cseq.filter((a) => a[0] === "num" || a[0] === "time").map((a) => a[1]);
    const wnums = wseq.filter((a) => a[0] === "num" || a[0] === "time").map((a) => a[1]);
    if (cnums.length && wnums.length && cnums.join("|") !== wnums.join("|")) return "num";
    if (cpol !== wpol) return "polarity";
  }
  return null;
}

function windows(text) {
  const raw = text || "";
  const out = [];
  let start = 0;
  SPLIT.lastIndex = 0;
  for (const match of raw.matchAll(SPLIT)) {
    const chunk = raw.slice(start, match.index);
    if (chunk.trim()) {
      const lead = chunk.length - chunk.trimStart().length;
      const trimmed = chunk.trim();
      out.push([trimmed, start + lead, start + lead + trimmed.length]);
    }
    start = match.index + match[0].length;
  }
  const tail = raw.slice(start);
  if (tail.trim()) {
    const lead = tail.length - tail.trimStart().length;
    const trimmed = tail.trim();
    out.push([trimmed, start + lead, start + lead + trimmed.length]);
  }
  return out;
}

function supportSpan(claim, body) {
  const [norm, origin] = normalize(body);
  const [claimNorm] = normalize(claim);
  const found = sliceSpan(body, norm, origin, claimNorm, claim);
  if (found) return found;
  const remainder = String(claim || "").replace(LEAD, "").trim();
  const [restNorm] = normalize(remainder);
  if (restNorm && restNorm !== claimNorm && restNorm.length >= 24) {
    return sliceSpan(body, norm, origin, restNorm, remainder);
  }
  return null;
}

function jsonValues(obj) {
  const strings = [];
  const nums = [];
  function walk(node) {
    if (node && typeof node === "object" && !Array.isArray(node)) {
      for (const v of Object.values(node)) walk(v);
    } else if (Array.isArray(node)) {
      for (const v of node) walk(v);
    } else if (typeof node === "boolean" || node == null) {
      return;
    } else if (typeof node === "number") {
      nums.push(numKey(String(node)));
    } else {
      const text = String(node).trim();
      if (text) strings.push(text);
    }
  }
  walk(obj);
  return [strings, nums];
}

function jsonRelation(claim, obj) {
  const [strings, nums] = jsonValues(obj);
  if (!strings.length || !nums.length) return null;
  const [claimNorm] = normalize(claim);
  const [seq] = atoms(claimNorm);
  const claimNums = seq.filter((a) => a[0] === "num").map((a) => a[1]);
  const claimDays = new Set(seq.filter((a) => a[0] === "day").map((a) => a[1]));
  if (!claimNums.length) return null;
  const present = [];
  const valueDays = new Set();
  for (const item of strings) {
    const [itemNorm] = normalize(item);
    if (!itemNorm) continue;
    present.push(claimNorm.includes(itemNorm));
    for (const atom of atoms(itemNorm)[0]) if (atom[0] === "day") valueDays.add(atom[1]);
  }
  const daysDiffer = claimDays.size && valueDays.size && [...claimDays].some((d) => !valueDays.has(d));
  if (daysDiffer && present.some(Boolean)) return "contradicts";
  if (!present.every(Boolean)) return null;
  const sameNums = claimNums.length === nums.length && claimNums.every((n) => nums.includes(n)) && nums.every((n) => claimNums.includes(n));
  if (!sameNums) {
    if (claimNums.some((n) => nums.includes(n))) return "contradicts";
    return null;
  }
  return "entails";
}

function item(kind, doc, quote, span, relation, fields) {
  return {
    kind,
    ref: String(doc.id || doc.url || kind),
    quote: String(quote || "").slice(0, 500),
    span,
    relation,
    by: "rule",
    ...fields,
  };
}

export function matchSpans(claim, docs, kind) {
  const out = [];
  for (const doc of docs || []) {
    if (!doc || typeof doc !== "object") continue;
    let structured = doc.output && typeof doc.output === "object" ? doc.output : null;
    if (!structured && doc.text && typeof doc.text === "object") structured = doc.text;
    const body = rawText(doc);
    if (!body.trim()) continue;
    const fields = warrantFields(doc, kind);
    const support = supportSpan(claim, body);
    if (support) {
      out.push(item(kind, doc, support[0], support[1], "entails", fields));
    } else if (structured) {
      const relation = jsonRelation(claim, structured);
      if (relation) {
        out.push(item(kind, doc, body, [0, body.length], relation, fields));
        continue;
      }
    }
    const covered = support ? support[1] : null;
    const [claimNorm] = normalize(claim);
    for (const [window, start, end] of windows(body)) {
      if (covered && start >= covered[0] && end <= covered[1]) continue;
      if (covered && covered[0] >= start && covered[1] <= end) continue;
      const [windowNorm] = normalize(window);
      if (!conflict(claimNorm, windowNorm)) continue;
      out.push(item(kind, doc, window, [start, end], "contradicts", fields));
      break;
    }
  }
  return out;
}

export function registryHits(claim) {
  const text = claim || "";
  const ids = [...new Set(text.match(ID) || [])];
  if (!ids.length) return [];
  const neg = NEG.test(text);
  const out = [];
  for (const ident of ids.sort()) {
    const row = ROWS.get(ident);
    if (!row) continue;
    const label = String(row.label || "");
    if (label && !text.toLowerCase().includes(label.toLowerCase()) && !neg) continue;
    out.push({
      kind: "registry",
      ref: ident,
      quote: `${ident} ${label}`.trim(),
      span: [0, 0],
      relation: neg ? "contradicts" : "entails",
      warrant_held: "W12",
      by: "rule",
    });
  }
  return out;
}

export { NEG };
