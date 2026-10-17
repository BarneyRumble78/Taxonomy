// Same fixtures through the Python verifier and the JavaScript port.
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { spawnSync } from "node:child_process";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import { verify } from "../engine/claimguard.mjs";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const fixtures = JSON.parse(readFileSync(join(root, "tests/claimguard_fixtures.json"), "utf8"));

function slim(out) {
  return out.claims.map((row) => ({
    verdict: row.verdict,
    qualifier: row.qualifier ?? null,
    status: row.status,
  }));
}

test("python and javascript verdicts match", async () => {
  const js = [];
  for (const row of fixtures) {
    js.push(slim(await verify(row.text, row.sources || [], row.tool_outputs || [])));
  }
  const py = spawnSync("python3", ["-c", `
import json, sys
sys.path.insert(0, "engine/v3")
from claimguard import verify
rows = json.load(sys.stdin)
out = []
for row in rows:
    result = verify(row["text"], row.get("sources") or [], row.get("tool_outputs") or [])
    out.append([{
        "verdict": c["verdict"],
        "qualifier": c.get("qualifier"),
        "status": c.get("status"),
    } for c in result["claims"]])
json.dump(out, sys.stdout)
`], { cwd: root, input: JSON.stringify(fixtures), encoding: "utf8" });
  assert.equal(py.status, 0, py.stderr);
  const parsed = JSON.parse(py.stdout);
  assert.equal(parsed.length, fixtures.length);
  for (let i = 0; i < fixtures.length; i++) {
    assert.deepEqual(js[i], parsed[i], fixtures[i].text);
  }
});
