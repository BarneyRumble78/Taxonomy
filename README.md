# Taxonomy

A standard classification of human knowledge, built on mathematics: 25 fields, one standard, 984 linked identifiers. Each claim is placed by the field whose evidence can establish it, the cell it concerns, the warrant it owes and the method that produced it.

- Standard: `standard/STANDARD_V2.md`
- Fields: `pyramids/`
- Engine: `python3 engine/taxonomy_engine.py "a sentence"`
- API: `npm run build && npm test`, then `npx wrangler deploy` (see `docs/DEPLOY.md`). Docs page and static JSON are in `public/`.
- Website: `python3 scripts/build_site.py`, then open `site/dist/index.html`

## Licence

Copyright 2026 Chris Townsend.

- Apache-2.0 (`LICENSE`): code in `engine/`, `worker/`, `scripts/`, `tests/`, and the site build (`site/template.html`, `scripts/build_site.py`).
- CC BY 4.0 (`LICENSE-CC-BY-4.0`): the standard, registry, pyramid and documentation text in `standard/`, `registry/`, `public/v1/` data, `docs/`, and `pyramids/`.

See `NOTICE`.

