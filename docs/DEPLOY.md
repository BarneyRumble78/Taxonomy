# Deploying the Taxonomy API on Cloudflare

The Worker serves `public/` (documentation page and static JSON) and the dynamic routes in `worker/index.js`.
The free plan is enough to start. Check Cloudflare's current limits before you rely on them.

## One-time setup (on your Mac)
```
cd ~/Downloads/taxonomy        # or wherever the clone lives
git pull
npm install
npx wrangler login             # opens a browser; no token is typed into any chat or file
npm run build                  # regenerates registry, public/v1 and worker/data.json
npm test                       # Worker tests (node); python3 -m pytest -q tests also checks JS/Python parity
npx wrangler deploy
```
Wrangler prints the address, in the form `https://taxonomy-api.<your-subdomain>.workers.dev`.
Check it with `curl -s https://<address>/v1/health`.

## Your own domain (later)
Cloudflare dashboard, Workers & Pages, taxonomy-api, Settings, Domains & Routes, add a custom domain on a zone in your account.

## Model assist
`wrangler.toml` binds Workers AI as `AI`. To run rules-only, delete the `[ai]` block and redeploy.
The model is set in `worker/index.js` (`MODEL`) and can be overridden by a `MODEL` variable.
Assist is a second opinion. It can only pick from a fixed list of codes. Output outside the list is dropped.
This path is covered by tests with a mock model. It has not been run against the live service.

## Abuse and cost controls
- Input limits: claim 1,000 characters, passage 8,000, subject 600.
- CORS is open (`*`) because every route is read-only and keyless. Restrict `access-control-allow-origin` in `worker/index.js` if you add anything private.
- Add a Cloudflare rate-limiting rule on `/v1/*` in the dashboard before you publicise the address, especially if model assist stays on.

## Updating
Change a pyramid, run `npm run build`, commit the regenerated `public/` and `worker/data.json`, then `npx wrangler deploy`.
