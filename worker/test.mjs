import assert from "node:assert/strict";
import test from "node:test";
import index from "../engine/retrieval_index.json" with { type: "json" };
import worker from "./index.js";

function post(text, extra = {}, env = {}) {
  return worker.fetch(new Request("https://taxonomy.test/v1/classify", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ text, ...extra }),
  }), env);
}

test("health", async () => {
  const res = await worker.fetch(new Request("https://taxonomy.test/v1/health"));
  assert.equal(res.status, 200);
  const body = await res.json();
  assert.equal(body.ok, true);
});

test("weak band does not call the model or the embedder", async () => {
  let ai = 0, embed = 0;
  const env = {
    embedQuery: async () => { embed += 1; return index.vectors[0]; },
    AI: { run: async () => { ai += 1; return { response: '{"codes":["MA"]}' }; } },
  };
  const res = await post("The particle has a gene.", {}, env);
  const body = await res.json();
  assert.equal(body.placement, null);
  assert.equal(body.reason, "low_confidence");
  assert.equal(ai, 0);
  assert.equal(embed, 0);
});

test("assist=1 may speak and must not change the owner", async () => {
  const ma = index.vectors[index.fields.indexOf("MA")];
  let model = null;
  const env = {
    embedQuery: async () => ma,
    AI: { run: async (name) => { model = name; return { response: '{"codes":["PH"]}' }; } },
  };
  const res = await post("Every bounded sequence of real numbers has a convergent subsequence.", { assist: 1 }, env);
  const body = await res.json();
  assert.equal(body.placement.owner, "MA");
  assert.equal(body.assist.codes[0], "PH");
  assert.equal(body.assist.agrees, false);
  assert.equal(model, "@cf/meta/llama-3.1-8b-instruct");
});

test("unknown assist codes are dropped", async () => {
  const ma = index.vectors[index.fields.indexOf("MA")];
  const env = {
    embedQuery: async () => ma,
    AI: { run: async () => ({ response: '{"codes":["ZZ","MA"]}' }) },
  };
  const res = await post("Every bounded sequence of real numbers has a convergent subsequence.", { assist: true }, env);
  const body = await res.json();
  assert.deepEqual(body.assist.codes, ["MA"]);
  assert.equal(body.placement.owner, "MA");
});

test("embed may run, and a disagreeing vector abstains without naming the field", async () => {
  let embed = 0;
  const ph = index.vectors[index.fields.indexOf("PH")];
  const env = {
    embedQuery: async () => { embed += 1; return ph; },
    AI: { run: async () => { throw new Error("model must not run"); } },
  };
  const res = await post("Every bounded sequence of real numbers has a convergent subsequence.", {}, env);
  const body = await res.json();
  assert.equal(embed, 1);
  assert.equal(body.placement, null);
  assert.equal(body.reason, "stages_disagree");
  assert.equal(body.retrieval, undefined);
  assert.equal(JSON.stringify(body).includes("\"PH\""), false);
});

test("input limit", async () => {
  const res = await post("a".repeat(1001), {}, {});
  assert.equal(res.status, 400);
});
