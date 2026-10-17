# Deploy Minerva (do not run this until Chris approves)

Checked 17 October 2026 against the Cloudflare API (account `da8e60e960a723c40792c8afaaddc3af`). Nothing in this file has been deployed.

## Pages

The site on `taxonomy.co.nz` and `www.taxonomy.co.nz` is the Pages project **`taxonomy-site`**.

- Source: GitHub `BarneyRumble78/Taxonomy`, production branch `main`
- Build command: empty
- Output directory: `site/dist`
- A merge to `main` publishes `site/dist` by itself. There is no build step on Pages.

The other project, `taxonomy` (`taxonomy-cwr.pages.dev`), does not hold the custom domain. Do not upload there.

`site/dist` is committed, including `site/dist/minerva/data/*.json` (the full pyramids, about 11 MB). Pages will not regenerate it.

## Worker

The Worker name is **`taxonomy-api`**. It does not deploy when `main` moves. From the repository root, after approval:

```
npx wrangler deploy
```

`wrangler.toml` sets `name = "taxonomy-api"` and `main = "worker/index.js"`. Leave these unset: `VERIFY_MODEL`, `ADJUDICATE`, `RETRIEVE`. Do not add an AI binding until that spend is intended.

The only public host is **api.taxonomy.co.nz**. `workers_dev` and `preview_urls` are both false, so `npx wrangler deploy` does not re-enable the workers.dev address or preview URLs. Chris turned the workers.dev address off on 17 October 2026.

`GET /v1/health` should then report `version` `3.0.0-minerva.1` and `verify` `rules only unless VERIFY_MODEL=1`.

## Optional stores (not created here)

Full pyramids are not inside the Worker. Until one of these is bound, `GET /v1/pyramids/FIELD/full` returns 404 with `static_url` `/minerva/data/FIELD.json`.

- R2 binding `PYRAMID_BUCKET`, object key `pyramids/FIELD.json`
- KV binding `PYRAMIDS`, key `pyramid:FIELD`

Commented sketches for R2, KV and the model flags are in `wrangler.toml`. The rate limit is on. `[[ratelimits]]` binds `VERIFY_LIMITER` at 60 requests a minute (`namespace_id` `1001`). The Worker applies it per IP on each of `/v1/verify`, `/v1/classify` and `/v1/audit`, and returns 429 with `Retry-After: 60`. `workers_dev` and `preview_urls` stay false. Keys, if used, go in KV `VERIFY_KEYS` as `key:` plus the SHA-256 of the bearer token. Raw keys are not stored.

## What a merge changes

Merging this branch to `main` publishes the site, including the draft Standard v3 banner. The Worker stays on the old script until `npx wrangler deploy`.
