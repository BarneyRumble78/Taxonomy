"""Three small linear plants and the simulator. Discrete time, one measured output.

    x[k+1] = A x[k] + B u[k] + G w[k],   w ~ N(0, sigma_w^2)
    z[k]   = C x[k] + v[k],              v ~ N(0, sigma_v^2)

The quantity to estimate is y[k] = C x[k]. Every estimator sees the same z.
"""
from dataclasses import dataclass
from typing import Callable

import numpy as np
from scipy.linalg import expm

STEPS = 400      # length of one trial
SETTLE = 50      # steps excluded from scoring while estimators converge
ONSET = 150      # step at which a fault begins


@dataclass(frozen=True)
class Plant:
    name: str
    A: np.ndarray
    B: np.ndarray
    C: np.ndarray
    G: np.ndarray
    sigma_w: float
    sigma_v: float
    x0: np.ndarray
    x0_sd: np.ndarray
    input_fn: Callable[[int], float]

    @property
    def n(self):
        return self.A.shape[0]

    @property
    def Q(self):
        return np.outer(self.G, self.G) * self.sigma_w ** 2

    @property
    def R(self):
        return self.sigma_v ** 2


def _no_input(step):
    return 0.0


def _square_wave(step):
    return 1.0 if (step // 100) % 2 == 0 else 0.0


def tracking():
    """Constant-velocity target; position measured. State: position, velocity."""
    dt = 0.1
    return Plant("tracking", A=np.array([[1.0, dt], [0.0, 1.0]]), B=np.zeros(2), C=np.array([1.0, 0.0]),
                 G=np.array([dt ** 2 / 2, dt]), sigma_w=0.5, sigma_v=1.0,
                 x0=np.array([0.0, 1.0]), x0_sd=np.array([1.0, 0.3]), input_fn=_no_input)


def thermal():
    """First-order thermal mass with a known heater input; temperature measured."""
    a = 0.95
    return Plant("thermal", A=np.array([[a]]), B=np.array([0.1]), C=np.array([1.0]),
                 G=np.array([1.0]), sigma_w=0.05, sigma_v=0.5,
                 x0=np.array([0.0]), x0_sd=np.array([0.5]), input_fn=_square_wave)


def oscillator():
    """Lightly damped mass-spring with random forcing; position measured."""
    dt, omega, zeta = 0.1, 1.0, 0.05
    continuous = np.array([[0.0, 1.0], [-omega ** 2, -2 * zeta * omega]])
    return Plant("oscillator", A=expm(continuous * dt), B=np.zeros(2), C=np.array([1.0, 0.0]),
                 G=np.array([dt ** 2 / 2, dt]), sigma_w=0.3, sigma_v=0.2,
                 x0=np.array([0.5, 0.0]), x0_sd=np.array([0.2, 0.2]), input_fn=_no_input)


PLANTS = {"tracking": tracking, "thermal": thermal, "oscillator": oscillator}


def simulate(plant, fault, seed, steps=STEPS, onset=ONSET):
    """One trial. Returns (y, z, u): truth, faulted measurements, inputs.

    The same seed gives the same truth and the same noise for every estimator.
    """
    rng = np.random.default_rng(seed)
    x = plant.x0 + plant.x0_sd * rng.standard_normal(plant.n)
    y, z, u = np.empty(steps), np.empty(steps), np.empty(steps)
    sensor = fault.sensor(plant, rng, onset)
    for k in range(steps):
        y[k] = plant.C @ x
        z[k] = sensor(k, y[k])
        u[k] = plant.input_fn(k)
        w = plant.sigma_w * (rng.standard_normal() + fault.process_shift(k, onset))
        x = plant.A @ x + plant.B * u[k] + plant.G * w
    return y, z, u
