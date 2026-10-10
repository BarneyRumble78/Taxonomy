// Compare the JavaScript rule stage with vectors produced by Python.
// Usage: node tests/parity_check.mjs payload.json
import { readFileSync } from "node:fs";
import lex from "../engine/lexicon.json" with { type: "json" };
import index from "../engine/retrieval_index.json" with { type: "json" };
import { adjudicate, retrieveField, rulePlacement, stageRule } from "../engine/rules.mjs";

const input = JSON.parse(readFileSync(process.argv[2], "utf8"));
const rules = input.claims.map((c) => rulePlacement(c, lex));
const staged = input.claims.map((c) => stageRule(c, lex));
const retrieved = (input.vectors || []).map((v) => (v ? retrieveField(v, index) : null));
const decided = staged.map((s, i) => adjudicate(s, input.vectors ? retrieved[i] : null));
process.stdout.write(JSON.stringify({ rules, staged, retrieved, decided }));
