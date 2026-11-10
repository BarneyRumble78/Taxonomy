"""Bounded proofs with the z3 SMT solver. Model-level only.

What is proved, for the scalar thermal plant and a fixed estimator gain l:

    if   |e| <= E, |w| <= W, |v| <= V
    then |e'| <= E,   where e' = (1 - l) (a e + w) - l v

e is the estimation error after a measurement update. So once the error is
inside [-E, E] it stays there for every disturbance within the bounds.

What is NOT proved: anything about the Python code, floating-point rounding,
the two-state plants, time-varying gains before they settle, or the
statistical requirement S1. This is verification-lite, not a machine-checked
proof of the implementation.

Run: python3 -m flash_demo.verify
"""
from fractions import Fraction

import numpy as np
import z3

from .plants import thermal
from .variants import HInfinityFilter, KalmanFilter, LuenbergerObserver

BOUND_SIGMAS = 3          # disturbances are assumed within 3 standard deviations
SAFETY_SIGMAS = 5         # requirement S3: worst-case error stays below 5 sigma_v
SETTLE_STEPS = 500


def settled_gain(variant, plant):
    """The gain a variant applies once its recursion has converged."""
    if variant is LuenbergerObserver:
        return float(variant(plant).gain[0])
    estimator = variant(plant)
    for _ in range(SETTLE_STEPS):
        estimator.step(0.0, 0.0)
    before = estimator.dev.copy()
    estimator._correct(1.0 + float(plant.C @ before))        # unit innovation
    return float((estimator.dev - before)[0])


def smallest_invariant(a, gain, w_bound, v_bound):
    """Smallest E for which [-E, E] is invariant (closed form for a scalar loop)."""
    return ((1 - gain) * w_bound + gain * v_bound) / (1 - abs((1 - gain) * a))


def prove_invariant(a, gain, w_bound, v_bound, limit):
    """True when z3 shows no disturbance within bounds can push the error past the limit."""
    exact = lambda value: z3.RealVal(str(Fraction(value).limit_denominator(10 ** 9)))
    e, w, v = z3.Reals("e w v")
    a_, l_, w_, v_, E = exact(a), exact(gain), exact(w_bound), exact(v_bound), exact(limit)
    after = (1 - l_) * (a_ * e + w) - l_ * v
    solver = z3.Solver()
    solver.add(e >= -E, e <= E, w >= -w_, w <= w_, v >= -v_, v <= v_)
    solver.add(z3.Or(after > E, after < -E))                 # search for a counterexample
    return solver.check() == z3.unsat


def run():
    plant = thermal()
    a = float(plant.A[0, 0])
    w_bound, v_bound = BOUND_SIGMAS * plant.sigma_w, BOUND_SIGMAS * plant.sigma_v
    safety = SAFETY_SIGMAS * plant.sigma_v
    rows = []
    for variant in (LuenbergerObserver, KalmanFilter, HInfinityFilter):
        gain = settled_gain(variant, plant)
        tight = smallest_invariant(a, gain, w_bound, v_bound)
        claimed = float(np.ceil(tight * 1000) / 1000)
        rows.append({"variant": variant.name, "gain": gain, "invariant_bound": claimed,
                     "invariant_proved": prove_invariant(a, gain, w_bound, v_bound, claimed),
                     "below_bound_refuted": not prove_invariant(a, gain, w_bound, v_bound, tight * 0.99),
                     "safety_limit": safety, "meets_s3": claimed <= safety})
    return rows


if __name__ == "__main__":
    for row in run():
        print(f"{row['variant']:12s} gain {row['gain']:.4f}  invariant |e| <= {row['invariant_bound']:.3f} "
              f"proved: {row['invariant_proved']}  tight: {row['below_bound_refuted']}  "
              f"meets S3 (<= {row['safety_limit']:.2f}): {row['meets_s3']}")
