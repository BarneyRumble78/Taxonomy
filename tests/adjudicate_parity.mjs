// Print agreed samples for the shared fixture file.
import { readFileSync } from "node:fs";
import { SYSTEM, agreeSamples } from "../engine/adjudicate.mjs";

const cases = JSON.parse(readFileSync(process.argv[2], "utf8"));
const keys = ["owner", "cell", "warrant", "default_applied", "method"];
const agreed = cases.map((c) => {
  const got = agreeSamples(c.samples);
  if (!got) return null;
  return Object.fromEntries(keys.map((k) => [k, got[k]]));
});
process.stdout.write(JSON.stringify({ system: SYSTEM, agreed }));
