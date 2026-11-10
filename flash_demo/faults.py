"""Fault classes for the campaign. Each fault begins at the onset step.

A fault changes what the sensor reports, or (for 'mismatch') how the plant
moves. Levels are fixed in PREREGISTRATION.md before any scored run.
"""
from dataclasses import dataclass

import numpy as np

LEVELS = {
    "bias": (1.0, 2.0, 3.0, 4.0),            # constant offset, in sigma_v
    "ramp": (0.01, 0.02, 0.05, 0.10),        # drift per step, in sigma_v (slow spoof)
    "dropout": (10, 25, 50, 100),            # steps with no measurement (NaN)
    "stuck": (10, 25, 50, 100),              # steps the sensor repeats its last value
    "saturation": (4.0, 2.0, 1.0, 0.0),      # sensor clips at onset value +/- level * sigma_v
    "outliers": (0.02, 0.05, 0.10, 0.20),    # chance per step of a +/- 15 sigma_v spike
    "heavy_tail": (5.0, 3.0, 2.0, 1.5),      # Student-t degrees of freedom for the noise
    "noise_scale": (1.5, 2.0, 3.0, 5.0),     # multiplier on sigma_v
    "mismatch": (2.0, 5.0, 10.0, 20.0),      # unmodelled constant forcing, in sigma_w
}
KINDS = tuple(LEVELS)
SPIKE = 15.0


@dataclass(frozen=True)
class Fault:
    kind: str
    level: float

    def __post_init__(self):
        if self.kind != "nominal" and self.kind not in LEVELS:
            raise ValueError(f"unknown fault kind {self.kind}")

    def process_shift(self, step, onset):
        """Mean shift of the process noise, in units of sigma_w."""
        return self.level if self.kind == "mismatch" and step >= onset else 0.0

    def sensor(self, plant, rng, onset):
        """A function (step, true value) -> reported measurement."""
        kind, level, sd = self.kind, self.level, plant.sigma_v
        state = {"last": 0.0, "centre": None}

        def read(step, truth):
            active = kind != "nominal" and step >= onset
            if active and kind == "heavy_tail":
                noise = sd * rng.standard_t(level)
            elif active and kind == "noise_scale":
                noise = sd * level * rng.standard_normal()
            else:
                noise = sd * rng.standard_normal()
            value = truth + noise
            if active:
                elapsed = step - onset
                if kind == "bias":
                    value += level * sd
                elif kind == "ramp":
                    value += level * sd * elapsed
                elif kind == "dropout" and elapsed < level:
                    value = np.nan
                elif kind == "stuck" and elapsed < level:
                    value = state["last"]
                elif kind == "saturation":
                    if state["centre"] is None:
                        state["centre"] = truth
                    value = float(np.clip(value, state["centre"] - level * sd, state["centre"] + level * sd))
                elif kind == "outliers" and rng.random() < level:
                    value += SPIKE * sd * (1.0 if rng.random() < 0.5 else -1.0)
            if not np.isnan(value):
                state["last"] = value
            return value

        return read


NOMINAL = Fault("nominal", 0.0)


def campaign_faults():
    """Every (kind, level) pair, in a fixed order."""
    return [Fault(kind, level) for kind in KINDS for level in LEVELS[kind]]
