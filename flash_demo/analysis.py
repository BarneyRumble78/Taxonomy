"""Analysis of the fault campaign. Reads results/campaign.csv; writes RESULTS.md and results.json.

Question: do variants that are further apart fail together less often?

Outcome     phi coefficient between two variants' pass/fail records over scenarios.
Predictors  lineage_tree   path length between the variants' MSC nodes, tree links only
            lineage_full   the same with formal cores and correspondence edges added
            assumption     1 - Jaccard overlap of the assumptions the variants rely on
            code           normalised compression distance of the variants' source (a null)
Test        Mantel test: Spearman correlation between distance and phi over variant
            pairs, one-sided (negative), by permuting variant labels.

Everything here was fixed in PREREGISTRATION.md before the campaign ran.

Run: python3 -m flash_demo.analysis
"""
import csv
import inspect
import json
import sys
import zlib
from itertools import combinations
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

from .faults import KINDS
from .plants import PLANTS
from .variants import NAMES, VARIANTS

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CSV = HERE / "results" / "campaign.csv"
PERMUTATIONS = 9999
BOOTSTRAPS = 2000
RNG_SEED = 7
PREDICTORS = ("lineage_tree", "lineage_full", "assumption", "code")
PAIRS = list(combinations(range(len(VARIANTS)), 2))


# ---------------------------------------------------------------- predictors

def assumption_distance(a, b):
    union = a.assumptions | b.assumptions
    return 1.0 - len(a.assumptions & b.assumptions) / len(union)


def code_distance(a, b):
    """Normalised compression distance between two classes' source text."""
    def size(text):
        return len(zlib.compress(text.encode("utf-8"), 9))
    x, y = inspect.getsource(a), inspect.getsource(b)
    cx, cy = size(x), size(y)
    return (size(x + y) - min(cx, cy)) / max(cx, cy)


def distance_matrices():
    sys.path.insert(0, str(ROOT / "engine" / "v3"))
    import rosetta
    cores = rosetta.load(ROOT)
    tree = rosetta.Graph(ROOT, cores=cores, use_edges=False, use_cores=False)
    full = rosetta.Graph(ROOT, cores=cores)
    n = len(VARIANTS)
    out = {name: np.zeros((n, n)) for name in PREDICTORS}
    for i, j in PAIRS:
        a, b = VARIANTS[i], VARIANTS[j]
        values = {"lineage_tree": tree.distance(a.msc, b.msc), "lineage_full": full.distance(a.msc, b.msc),
                  "assumption": assumption_distance(a, b), "code": code_distance(a, b)}
        for name, value in values.items():
            out[name][i, j] = out[name][j, i] = value
    return out


# -------------------------------------------------------------------- outcome

def load(path=CSV):
    """{plant: array of shape (variants, scenarios)} of 0/1 failures, plus scenario labels."""
    if not path.is_file():
        raise SystemExit(f"{path} not found. Run: python3 -m flash_demo.campaign")
    cells, labels = {}, {}
    with path.open(encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            key = (row["fault"], row["level"], row["repeat"])
            cells.setdefault(row["plant"], {}).setdefault(key, {})[row["variant"]] = int(row["fail"])
    fails = {}
    for plant, scenarios in cells.items():
        keys = sorted(scenarios)
        for key in keys:
            if set(scenarios[key]) != set(NAMES):
                raise SystemExit(f"{plant} {key}: results missing for some variants")
        fails[plant] = np.array([[scenarios[key][name] for key in keys] for name in NAMES])
        labels[plant] = keys
    if set(fails) != set(PLANTS):
        raise SystemExit(f"expected plants {sorted(PLANTS)}, found {sorted(fails)}")
    return fails, labels


def phi_matrix(fails):
    """Pairwise phi. NaN where a variant never fails or always fails."""
    n = fails.shape[0]
    out = np.full((n, n), np.nan)
    spread = fails.std(axis=1) > 0
    for i, j in PAIRS:
        if spread[i] and spread[j]:
            out[i, j] = out[j, i] = np.corrcoef(fails[i], fails[j])[0, 1]
    return out


def pair_values(matrix, order=None):
    order = range(matrix.shape[0]) if order is None else order
    return np.array([matrix[order[i], order[j]] for i, j in PAIRS])


def mantel(distance, phi, rng):
    """Spearman rho between distance and phi, with a one-sided permutation p-value (rho < 0)."""
    outcome = pair_values(phi)
    keep = np.isfinite(outcome)
    if keep.sum() < 10 or np.ptp(pair_values(distance)[keep]) == 0:
        return {"rho": None, "p": None, "pairs": int(keep.sum())}
    observed = spearmanr(pair_values(distance)[keep], outcome[keep]).statistic
    hits = 0
    for _ in range(PERMUTATIONS):
        order = rng.permutation(distance.shape[0])
        hits += spearmanr(pair_values(distance, order)[keep], outcome[keep]).statistic <= observed
    return {"rho": float(observed), "p": (hits + 1) / (PERMUTATIONS + 1), "pairs": int(keep.sum())}


def bootstrap_rho(distance, fails, rng):
    """95% interval for rho from resampling scenarios."""
    values, predictor = [], pair_values(distance)
    for _ in range(BOOTSTRAPS):
        sample = fails[:, rng.integers(0, fails.shape[1], fails.shape[1])]
        outcome = pair_values(phi_matrix(sample))
        keep = np.isfinite(outcome)
        if keep.sum() >= 10 and np.ptp(predictor[keep]) > 0:
            values.append(spearmanr(predictor[keep], outcome[keep]).statistic)
    if len(values) < BOOTSTRAPS / 2:
        return None
    return [float(np.percentile(values, 2.5)), float(np.percentile(values, 97.5))]


def coincidence(fails):
    """Observed share of scenarios where both of a pair fail, against independence."""
    rates = fails.mean(axis=1)
    observed = np.mean([np.mean(fails[i] & fails[j]) for i, j in PAIRS])
    expected = np.mean([rates[i] * rates[j] for i, j in PAIRS])
    return {"observed": float(observed), "expected_if_independent": float(expected),
            "ratio": float(observed / expected) if expected > 0 else None}


def analyse(fails, distances, rng):
    phi = phi_matrix(fails)
    return {"scenarios": int(fails.shape[1]),
            "failure_rate": {name: float(rate) for name, rate in zip(NAMES, fails.mean(axis=1))},
            "mean_phi": float(np.nanmean(pair_values(phi))),
            "coincidence": coincidence(fails),
            "tests": {name: {**mantel(distances[name], phi, rng),
                             "rho_ci95": bootstrap_rho(distances[name], fails, rng)} for name in PREDICTORS}}


# --------------------------------------------------------------------- report

def fmt(value, digits=2):
    return "n/a" if value is None else f"{value:.{digits}f}"


def report(results, distances, fails, labels):
    lines = ["# FLASH demonstrator: results", "",
             "Generated by `python3 -m flash_demo.analysis` from `results/campaign.csv`.",
             "Methods and thresholds were fixed in `PREREGISTRATION.md` before the campaign ran.", ""]
    lines += ["## Primary test (all plants pooled)", "",
              "A negative rho means more distant variants fail together less often.", "",
              "| Predictor | Spearman rho | 95% interval | One-sided p | Pairs |", "|---|---|---|---|---|"]
    for name in PREDICTORS:
        t = results["pooled"]["tests"][name]
        ci = "n/a" if t["rho_ci95"] is None else f"{t['rho_ci95'][0]:.2f} to {t['rho_ci95'][1]:.2f}"
        lines.append(f"| {name} | {fmt(t['rho'])} | {ci} | {fmt(t['p'], 4)} | {t['pairs']} |")
    lines += ["", "## Replication by plant", "", "| Plant | Predictor | rho | p | Pairs |", "|---|---|---|---|---|"]
    for plant in PLANTS:
        for name in PREDICTORS:
            t = results[plant]["tests"][name]
            lines.append(f"| {plant} | {name} | {fmt(t['rho'])} | {fmt(t['p'], 4)} | {t['pairs']} |")
    lines += ["", "## Secondary: scenarios where the variants disagree", "",
              "Scenarios in which every variant passed, or every variant failed, are removed.", "",
              "| Predictor | rho | p | Pairs | Scenarios |", "|---|---|---|---|---|"]
    for name in PREDICTORS:
        t = results["pooled_disagreement"]["tests"][name]
        lines.append(f"| {name} | {fmt(t['rho'])} | {fmt(t['p'], 4)} | {t['pairs']} | {results['pooled_disagreement']['scenarios']} |")
    c = results["pooled"]["coincidence"]
    lines += ["", "## Do the variants fail independently?", "",
              f"- Mean share of scenarios in which both variants of a pair fail: {c['observed']:.3f}.",
              f"- Expected if failures were independent: {c['expected_if_independent']:.3f}.",
              f"- Ratio: {fmt(c['ratio'])}. Mean pairwise phi: {results['pooled']['mean_phi']:.2f}.", ""]
    lines += ["## Failure rate by variant and fault class (all plants)", "",
              "| Variant | " + " | ".join(KINDS) + " | All |", "|---|" + "---|" * (len(KINDS) + 1)]
    for index, name in enumerate(NAMES):
        cells = []
        for kind in KINDS:
            total = fail = 0
            for plant in PLANTS:
                mask = np.array([key[0] == kind for key in labels[plant]])
                total += mask.sum()
                fail += fails[plant][index][mask].sum()
            cells.append(f"{fail / total:.2f}")
        lines.append(f"| {name} | " + " | ".join(cells) + f" | {results['pooled']['failure_rate'][name]:.2f} |")
    lines += ["", "## Predictor values", "", "| Pair | lineage_tree | lineage_full | assumption | code | phi (pooled) |",
              "|---|---|---|---|---|---|"]
    phi = phi_matrix(np.hstack([fails[p] for p in PLANTS]))
    for i, j in PAIRS:
        lines.append(f"| {NAMES[i]} / {NAMES[j]} | {distances['lineage_tree'][i, j]:.0f} | {distances['lineage_full'][i, j]:.0f} | "
                     f"{distances['assumption'][i, j]:.2f} | {distances['code'][i, j]:.2f} | {fmt(float(phi[i, j]) if np.isfinite(phi[i, j]) else None)} |")
    return "\n".join(lines) + "\n"


def main():
    fails, labels = load()
    distances = distance_matrices()
    rng = np.random.default_rng(RNG_SEED)
    pooled = np.hstack([fails[plant] for plant in PLANTS])
    split = pooled[:, (pooled.sum(axis=0) > 0) & (pooled.sum(axis=0) < pooled.shape[0])]
    results = {"pooled": analyse(pooled, distances, rng), "pooled_disagreement": analyse(split, distances, rng)}
    for plant in PLANTS:
        results[plant] = analyse(fails[plant], distances, rng)
    (HERE / "results" / "results.json").write_text(json.dumps(results, indent=1) + "\n", encoding="utf-8")
    (HERE / "RESULTS.md").write_text(report(results, distances, fails, labels), encoding="utf-8")
    print((HERE / "RESULTS.md").read_text(encoding="utf-8").split("## Replication")[0])


if __name__ == "__main__":
    main()
