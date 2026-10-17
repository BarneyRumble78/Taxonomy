// Bind a claim to quoted spans. No fetching. Pyramid search is not evidence.
import registry from "../registry/registry.json" with { type: "json" };

const NUM = /-?\d+(?:\.\d+)?/g;
const NEG = /\b(?:not|no|never|none|false|didn't|does not|do not|did not)\b/i;
const ID = /\b[A-Z]{2}\.[OMWB]\.[A-Z]?\d+(?:\.\d+)*\b/g;
const STOP = new Set("that this with from have were been into over under than then they them their which what when where while there these those also only such said says about after before between through would could should claim claims".split(" "));
export const TOOL_WARRANT = {
  calculator: "W2", compute: "W2", arithmetic: "W2",
  test: "W11", test_runner: "W11", runner: "W11",
  sensor: "W4", reading: "W4", api: "W4",
  search: "W7", snippet: "W7",
};
const WARRANTS = new Set(Array.from({ length: 13 }, (_, i) => "W" + (i + 1)));
const ROWS = new Map(registry.filter((row) => row && row.id).map((row) => [row.id, row]));

export function numbers(text) {
  return String(text || "").match(NUM) || [];
}

export function numbersAgree(claim, quote, relTol = 0) {
  const wanted = numbers(claim);
  if (!wanted.length) return null;
  const have = numbers(quote);
  if (relTol) {
    return wanted.every((a) => {
      const fa = Number(a);
      return have.some((b) => Math.abs(Number(b) - fa) <= relTol * Math.max(1, Math.abs(fa)));
    });
  }
  return wanted.every((n) => have.includes(n));
}

export function warrantOf(doc, kind) {
  const declared = String((doc && doc.warrant) || "").toUpperCase();
  if (WARRANTS.has(declared)) return declared;
  if (kind === "source") return "W7";
  const tool = String((doc && doc.tool) || "").toLowerCase().replace(/ /g, "_");
  return TOOL_WARRANT[tool] || null;
}

function body(doc) {
  if (doc.output && typeof doc.output === "object") return JSON.stringify(doc.output);
  return String(doc.text || doc.output || "");
}

function words(text) {
  return (String(text || "").toLowerCase().match(/[a-z0-9]+/g) || []).filter((w) => w.length > 3 && !STOP.has(w));
}

function spanOf(hay, quote) {
  if (!quote) return [0, 0];
  const idx = hay.toLowerCase().indexOf(quote.toLowerCase().slice(0, 80));
  if (idx < 0) return [0, Math.min(hay.length, quote.length)];
  return [idx, Math.min(hay.length, idx + quote.length)];
}

export function matchSpans(claim, docs, kind) {
  const out = [];
  const tokens = words(claim);
  const claimNeg = NEG.test(claim || "");
  for (const doc of docs || []) {
    if (!doc || typeof doc !== "object") continue;
    const text = body(doc);
    if (!text.trim()) continue;
    const low = text.toLowerCase();
    const hits = tokens.reduce((n, w) => n + (low.includes(w) ? 1 : 0), 0);
    const overlap = tokens.length ? hits / tokens.length : 0;
    let quote = "";
    let relation = "neutral";
    const folded = String(claim || "").toLowerCase().split(/\s+/).filter(Boolean).join(" ");
    const hay = text.toLowerCase().split(/\s+/).filter(Boolean).join(" ");
    if (folded && hay.includes(folded)) {
      quote = claim.trim();
      relation = "entails";
    } else if (overlap >= 0.6) {
      quote = text.trim().slice(0, 240);
      relation = "entails";
    }
    const agreed = relation === "entails" || numbers(claim).length ? numbersAgree(claim, text) : null;
    if (relation === "entails" && agreed === false) {
      relation = "contradicts";
      quote = quote || text.trim().slice(0, 240);
    } else if (relation === "entails") {
      const docNeg = NEG.test(text);
      if (docNeg !== claimNeg && overlap >= 0.6) relation = "contradicts";
    }
    if (relation === "neutral") continue;
    out.push({
      kind,
      ref: String(doc.id || doc.url || kind),
      quote: quote.slice(0, 500),
      span: spanOf(text, quote),
      relation,
      warrant_held: warrantOf(doc, kind),
      by: "rule",
    });
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

export { NEG, words };
