# Specification: a single-output state estimator

Status: fixed 10 November 2026, before any fault run. Code: `plants.py`, `campaign.py`, `verify.py`.

## Component
A discrete-time estimator. At each step it receives one measurement `z` (or none) and the known input `u`.
It returns an estimate of the measured quantity `y`.

## Plants
The same specification is applied to three plants (`plants.py`):

| Plant | State | Measured | Process noise | Measurement noise `sigma_v` |
|---|---|---|---|---|
| tracking | position, velocity (constant-velocity model) | position | random acceleration | 1.0 |
| thermal | temperature, with a known heater input | temperature | random heat flow | 0.5 |
| oscillator | position, velocity (lightly damped spring) | position | random forcing | 0.2 |

Each trial runs 400 steps. The first 50 are not scored.

## Requirements

| ID | Requirement | How it is checked |
|---|---|---|
| S1 Accuracy | The error `|estimate - y|` exceeds `2 sigma_v` in at most 5% of scored steps. | Simulation (`campaign.score`) |
| S2 Totality | Every output is a finite number, for any sequence of readings, including missing ones. | Property-based tests (Hypothesis) |
| S3 Safety bound | With disturbances inside `3 sigma`, the error stays within `5 sigma_v` once inside it. | z3 proof, thermal plant, three fixed-gain variants only |
| S4 Timing | Mean compute time per step is under 5 ms. | Timing test |

A trial **fails** when S1 or S2 is broken.

## What this is not
The variants are not proved equivalent to each other or to this specification.
S1 is statistical and is checked by simulation.
S3 is a proof about a mathematical model of the loop, not about the Python code.
This is verification-lite. It is not a machine-checked proof in Lean or Coq.
