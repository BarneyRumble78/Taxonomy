"""Fault campaign: every variant on every plant under every fault scenario.

A trial FAILS when the estimate breaks the specification (flash_demo/SPEC.md):
  S1  |estimate - truth| > 2 sigma_v in more than 5% of scored steps, or
  S2  any estimate is not finite.

Run:  python3 -m flash_demo.campaign            (writes flash_demo/results/campaign.csv)
      python3 -m flash_demo.campaign --nominal  (development check, separate seeds)
"""
import argparse
import csv
import sys
from multiprocessing import Pool
from pathlib import Path

import numpy as np

from .faults import NOMINAL, Fault, campaign_faults
from .plants import PLANTS, SETTLE, simulate
from .variants import VARIANTS, run

HERE = Path(__file__).resolve().parent
OUT = HERE / "results" / "campaign.csv"
TOLERANCE_SIGMAS = 2.0
MAX_VIOLATION_SHARE = 0.05
REPEATS = 10
CAMPAIGN_SEED = 20261110
DEVELOPMENT_SEED = 900000
FIELDS = ("plant", "fault", "level", "repeat", "seed", "variant", "violation_share", "max_error_sigmas", "finite", "fail")


def score(plant, truth, estimate):
    """(violation share, largest error in sigma_v, all finite, fail) for one trial."""
    finite = bool(np.all(np.isfinite(estimate)))
    if not finite:
        return 1.0, float("inf"), False, True
    error = np.abs(estimate[SETTLE:] - truth[SETTLE:]) / plant.sigma_v
    share = float(np.mean(error > TOLERANCE_SIGMAS))
    return share, float(error.max()), True, share > MAX_VIOLATION_SHARE


def trial(task):
    """All variants on one (plant, fault, repeat). Every variant sees the same data."""
    plant_name, kind, level, repeat, seed = task
    plant = PLANTS[plant_name]()
    truth, z, u = simulate(plant, Fault(kind, level), seed)
    rows = []
    for variant in VARIANTS:
        share, worst, finite, fail = score(plant, truth, run(variant, plant, z, u))
        rows.append({"plant": plant_name, "fault": kind, "level": level, "repeat": repeat, "seed": seed,
                     "variant": variant.name, "violation_share": round(share, 6),
                     "max_error_sigmas": round(worst, 4), "finite": int(finite), "fail": int(fail)})
    return rows


def tasks(nominal=False, repeats=REPEATS):
    out, seed = [], DEVELOPMENT_SEED if nominal else CAMPAIGN_SEED
    faults = [NOMINAL] if nominal else campaign_faults()
    for plant_name in PLANTS:
        for fault in faults:
            for repeat in range(repeats):
                out.append((plant_name, fault.kind, fault.level, repeat, seed))
                seed += 1
    return out


def run_all(nominal=False, repeats=REPEATS, workers=8):
    with Pool(workers) as pool:
        return [row for rows in pool.map(trial, tasks(nominal, repeats), chunksize=4) for row in rows]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--nominal", action="store_true", help="fault-free development check; writes nothing")
    parser.add_argument("--repeats", type=int, default=None)
    args = parser.parse_args(argv)
    rows = run_all(args.nominal, args.repeats or (20 if args.nominal else REPEATS))
    if args.nominal:
        for plant_name in PLANTS:
            for variant in VARIANTS:
                mine = [r for r in rows if r["plant"] == plant_name and r["variant"] == variant.name]
                fails = sum(r["fail"] for r in mine)
                mean = np.mean([r["violation_share"] for r in mine])
                print(f"{plant_name:11s} {variant.name:16s} fails {fails:2d}/{len(mine)}  mean violation share {mean:.4f}")
        return 1 if any(r["fail"] for r in rows) else 0
    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"{OUT.relative_to(HERE.parent)}: {len(rows)} rows, {sum(r['fail'] for r in rows)} failures")
    return 0


if __name__ == "__main__":
    sys.exit(main())
