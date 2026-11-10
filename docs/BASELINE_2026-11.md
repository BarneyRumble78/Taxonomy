# Baseline, November 2026

Recorded 10 November 2026 on branch `v4-generative`, cut from `main` at `aa91ae5` (7 November 2026).
Every figure below was measured on that commit. Nothing here is a result.

## Environment
- Python 3.12.13 in a local `.venv` (CI uses Python 3.12).
- Installed with `pip install -r requirements.txt`. Key versions: pytest 9.2.0, fastembed 0.9.1, onnxruntime 1.31.1, numpy 2.5.4, jsonschema 4.26.0.
- Versions are not yet pinned in `requirements.txt`. Pinning is planned for WP5 (reproducibility).

## Checks
- `python3 scripts/check.py`: "All checks pass."
- `python3 -m pytest -q tests`: 208 passed, 0 failed, in 24 s.

## The three failing tests
The handover reported 205 passed and 3 failed. The cause is confirmed: `fastembed` was not installed.

With `fastembed` blocked from import, the same three tests fail and 205 pass:
- `tests/test_eval_gate.py::test_place_parity_with_injected_vectors`
- `tests/test_eval_gate.py::test_distractors_abstain_or_keep_gold_owner`
- `tests/test_eval_gate.py::test_answered_owner_accuracy`

`fastembed` was already listed in `requirements.txt`, so no code was wrong.
`numpy` was installed only by the CI workflow. It is now listed in `requirements.txt` as well.

## Content counts
| Item | Count | Note |
|---|---|---|
| Pyramid files in `pyramids/*.md` | 75 | 4.17 MB of Markdown at top level; `pyramids/` is 38 MB on disk in total |
| Registry entries, `registry/registry.json` | 990 | The handover says 984 stable IDs; the difference is not yet explained |
| Map nodes, all `maps/<FIELD>/*.json` | 307,561 | 25 field directories |
| Lens cards, `cards/lens/` | 149 | 25 files |
| Toolkit cards | 63 | Mathematics only (`cards/toolkit/MA.json`); all `draft` |
| Toolkit cards with tools | 60 | 109 tools in total |
| Fields with toolkit cards | 1 of 25 | |
| Signature facets | 14 | `signatures/vocabulary.json` |
| Retrodiction problems | 50 | `bench/retrodiction_problems.json` |
| Cross-connection cases | 100 | Counted only; the file was not read into any prompt |
| Engine v3 | 6,334 lines | 18 modules in `engine/v3/` |
| Test files | 27 | in `tests/` |

## Cross-field edges
The pattern `uses XX.<face>` occurs 84 times in `pyramids/*.md`. The handover says 83.

| Field | Citations |
|---|---|
| EN | 38 |
| ST | 11 |
| BI | 10 |
| MS | 7 |
| CS | 4 |
| PL | 4 |
| EA | 3 |
| AR | 2 |
| PH | 2 |
| CH | 1 |
| EC | 1 |
| ED | 1 |

Thirteen fields cite no other field in this form. There are no typed correspondence edges yet.

## Local models
Ollama answers at `127.0.0.1:11434`. The models named in `CLAUDE.md` (`qwen3:30b-a3b`, `gemma3:12b`) are not installed.
Installed on 10 November 2026: `qwen3.6:35b`, `qwen3.6:27b`, `qwen2.5:14b-instruct`, and one security model.
No model run has been made on this branch.

## Not yet done
- The branch has not been pushed, so CI has not run on it.
- No scored benchmark run exists.
