# Adjudicator

The rule stage and the retrieval stage still decide a placement when they agree. A model runs only when `TAXONOMY_ADJUDICATE=1`. With that flag off, which is the default in CI and in `wrangler.toml`, nothing is called and nothing is spent.

The default chain is a local Ollama model, then Workers AI inside its free daily allowance, then abstain. Anthropic and OpenAI are used only when `TAXONOMY_ADJUDICATE_PAID=1` and the chain names them.

## Local Ollama on a Mac

Install Ollama from [ollama.com](https://ollama.com), then:

```
brew install ollama
ollama serve
ollama pull gemma3:12b
```

`qwen3` models use the same request. From the repository root:

```
export TAXONOMY_ADJUDICATE=1
python3 engine/taxonomy_engine.py --detail "Russian forces control Zarichne."
```

Answers, the review queue, and the daily neuron count are written under `~/.taxonomy/` (`cache.json`, `review_queue.jsonl`, `quota.json`). `TAXONOMY_CACHE_PATH`, `TAXONOMY_REVIEW_PATH`, and `TAXONOMY_QUOTA_PATH` move a file. An empty value turns that file off.

The engine posts to `http://127.0.0.1:11434/api/chat`. Override the host with `OLLAMA_HOST`. The body sets `format` to the placement schema, `think` to false, and `keep_alive` to `10m`. Timeouts and HTTP 5xx are retried with backoff. A 4xx is not retried.

## Config

`engine/adjudicator.json` holds the chain:

```
ollama:gemma3:12b, workers-ai:@cf/meta/llama-3.1-8b-instruct-fp8, abstain
```

`TAXONOMY_ADJUDICATE_CHAIN` replaces that list. A Workers AI step needs `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID`. Once the recorded neurons for the UTC day reach 10,000, that step is skipped and the chain abstains instead of spending. Ollama has no quota.

Paid example, only after you mean to spend:

```
export TAXONOMY_ADJUDICATE_PAID=1
export TAXONOMY_ADJUDICATE_CHAIN="anthropic:claude-haiku-4-5,abstain"
export ANTHROPIC_API_KEY=...
```

## What a result carries

Each result has `model` and `prompt_version`. The version is the first 12 hex characters of the SHA-256 of the system prompt. The answer cache key is the normalised claim, that version, and the chain id. A different prompt or model misses the cache. The judge sees the top cue fields and the retrieval neighbours, not the full catalogue. An empty shortlist sends the full catalogue.

When samples disagree, the status is `needs_review` and a JSON line is appended to the review queue. Fold reviewed labels into a new file. The command refuses `heldout` and the frozen 203-claim file.

```
python3 scripts/fold_reviews.py ~/.taxonomy/review_queue.jsonl reviewed.tsv pilot/extra_labels.tsv
```

`reviewed.tsv` has the columns `claim`, `owner`, `cell`, `warrant`, and `method`.

## Costs

Ollama on your own machine is $0.

Workers AI is billed at $0.011 per 1,000 neurons, with 10,000 neurons a day free. The guard stops at that free allowance. Price list checked 10 Oct 2026: https://developers.cloudflare.com/workers-ai/platform/pricing/

Anthropic list prices, standard global tier, checked the same day: https://platform.claude.com/docs/en/about-claude/pricing

| Model | Input / MTok | Output / MTok |
|---|---:|---:|
| Haiku 5.5, prompts up to 100k | $0.10 | $0.50 |
| Haiku 4.5 | $1 | $5 |
| Sonnet 5.5 | $2 | $10 |
| Opus 5.5 | $4 | $20 |

`scripts/report_adjudication.py` adds those rates, counts cache read and cache write tokens, and keeps usage from disagree and error calls. The figures are list prices, not a bill.
