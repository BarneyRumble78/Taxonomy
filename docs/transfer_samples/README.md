# Transfer operator: five sample runs

Run 10 November 2026 with `python3 taxonomy.py transfer CORE FIELD --fill`.
Model: `qwen3.6:27b` on local Ollama, with `TAXONOMY_OLLAMA_FORMAT=none`. Cost: USD 0.

Each file is one run record. Every record is `generated-unverified`: a model's proposal, with no source consulted and no person's check.

| Core | Target field | File |
|---|---|---|
| Branching-process threshold | Economics | `RC-branching-threshold__EC.json` |
| Replicator dynamics | Language | `RC-replicator-dynamics__LN.json` |
| Markov-chain convergence | Mind, brain and society | `RC-markov-stationary__MS.json` |
| Lyapunov stability | Medicine | `RC-lyapunov-stability__MD.json` |
| Network Laplacian | Earth | `RC-network-laplacian__EA.json` |

## How to read a record
- `proposal.roles`: what the model says would play each role in the target field.
- `proposal.assumptions`: for each assumption, whether it holds there and why.
- `proposal.mismatches`: where the analogy fails. These are the main output.
- `proposal.ideas`: questions or methods the mismatches suggest.
- `proposal.already_known`: whether the model believes the transfer already exists in the literature.
- `guarantee_carries`: true only when every role is filled and every assumption is marked as holding.

## What the five runs show
These are observations on five runs, not an evaluation.
- The operator ran end to end, and each answer passed validation.
- In all five runs the model judged the transfer to be already known in the target field.
  So these empty cells are unrecorded in the seed, not undiscovered. The seed is too small for its gaps to mean much yet.
- In no run did the guarantee carry. The model named violated assumptions each time.
- No claim in these files has been checked against a source.
