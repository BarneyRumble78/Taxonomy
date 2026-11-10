"""Ten estimators of one quantity, each from a different mathematical lineage.

Every variant has the same interface: step(z, u) returns an estimate of y for
the current step, where z is the measurement (NaN when missing) and u is the
known input. Every variant carries:

  msc          the mathematics map node its method belongs to
  assumptions  the shared-vocabulary assumptions it relies on (see ASSUMPTIONS)

Both were fixed in PREREGISTRATION.md before any fault run.
"""
import numpy as np
from scipy.optimize import linprog
from scipy.signal import place_poles

ASSUMPTIONS = {
    "model": "The dynamics model (A, B) is correct.",
    "process_stats": "The process-noise covariance is known.",
    "noise_variance": "The measurement-noise variance is known.",
    "gaussian": "The noises are Gaussian.",
    "unbiased": "Measurement noise has zero mean (no bias or drift).",
    "bounded": "Measurement noise never exceeds a known hard bound.",
    "every_step": "A measurement arrives at every step.",
    "no_outliers": "There are no gross outliers.",
    "smooth": "The signal is close to a straight line over a short window.",
    "in_range": "The sensor is not saturated or frozen.",
    "white": "Measurement noise is independent from step to step.",
}
WINDOW = 15


class Estimator:
    """Base class. Subclasses set name, msc and assumptions, and implement step."""
    name = ""
    msc = ""
    assumptions = frozenset()

    def __init__(self, plant):
        self.plant = plant

    def step(self, z, u):
        raise NotImplementedError


class ModelBased(Estimator):
    """Tracks the input-driven nominal state; subclasses estimate the deviation.

    The deviation d = x - nominal obeys d[k+1] = A d[k] + G w[k], with no input.
    Subclasses implement _predict() and _correct(residual) on the deviation.
    """

    def __init__(self, plant):
        super().__init__(plant)
        self.nominal = plant.x0.astype(float).copy()
        self.dev = np.zeros(plant.n)
        self.pending_input = None

    def step(self, z, u):
        p = self.plant
        if self.pending_input is not None:
            self.nominal = p.A @ self.nominal + p.B * self.pending_input
            self._predict()
        self.pending_input = u
        if np.isfinite(z):
            self._correct(z - p.C @ self.nominal)
        else:
            self._missing()
        return float(p.C @ (self.nominal + self.dev))

    def _predict(self):
        self.dev = self.plant.A @ self.dev

    def _correct(self, residual):
        raise NotImplementedError

    def _missing(self):
        """Called in place of _correct when no measurement arrived."""


class KalmanFilter(ModelBased):
    name, msc = "kalman", "MSC:93E11"
    assumptions = frozenset({"model", "process_stats", "noise_variance", "gaussian", "unbiased",
                             "no_outliers", "in_range", "white"})

    def __init__(self, plant):
        super().__init__(plant)
        self.P = np.diag(plant.x0_sd ** 2)

    def _predict(self):
        p = self.plant
        self.dev = p.A @ self.dev
        self.P = p.A @ self.P @ p.A.T + p.Q

    def _innovation(self, residual):
        p = self.plant
        variance = float(p.C @ self.P @ p.C + p.R)
        return residual - p.C @ self.dev, variance

    def _correct(self, residual):
        p = self.plant
        innovation, variance = self._innovation(residual)
        gain = self.P @ p.C / variance
        self.dev = self.dev + gain * innovation
        self.P = (np.eye(p.n) - np.outer(gain, p.C)) @ self.P


class HuberKalman(KalmanFilter):
    """Kalman filter whose innovation is clipped at 1.5 standard deviations."""
    name, msc = "huber_kalman", "MSC:62F35"
    assumptions = frozenset({"model", "process_stats", "noise_variance", "unbiased", "in_range", "white"})
    CLIP = 1.5

    def _innovation(self, residual):
        innovation, variance = super()._innovation(residual)
        limit = self.CLIP * np.sqrt(variance)
        return float(np.clip(innovation, -limit, limit)), variance


class LuenbergerObserver(ModelBased):
    """Fixed-gain observer with error poles placed inside the unit circle."""
    name, msc = "luenberger", "MSC:93B53"
    assumptions = frozenset({"model", "unbiased", "no_outliers", "in_range"})
    POLES = {1: [0.8], 2: [0.8, 0.7]}

    def __init__(self, plant):
        super().__init__(plant)
        placed = place_poles(plant.A.T, plant.C.reshape(-1, 1), self.POLES[plant.n])
        predictor_gain = placed.gain_matrix.ravel()
        self.gain = np.linalg.solve(plant.A, predictor_gain)

    def _correct(self, residual):
        self.dev = self.dev + self.gain * (residual - self.plant.C @ self.dev)


class HInfinityFilter(ModelBased):
    """Minimax filter: bounds the worst-case gain from disturbances to error."""
    name, msc = "h_infinity", "MSC:93B36"
    assumptions = frozenset({"model", "noise_variance", "unbiased", "in_range"})

    def __init__(self, plant):
        super().__init__(plant)
        self.P = np.diag(plant.x0_sd ** 2)
        self.theta = 0.5 / plant.R            # below 1/R, so the recursion stays well posed
        self.weight = np.outer(plant.C, plant.C)

    def _correct(self, residual):
        p = self.plant
        core = np.linalg.inv(np.eye(p.n) - self.theta * self.weight @ self.P + self.weight @ self.P / p.R)
        gain = self.P @ core @ p.C / p.R
        self.dev = self.dev + gain * (residual - p.C @ self.dev)
        advanced = p.A @ self.P @ core @ p.A.T + p.Q
        self.P = (advanced + advanced.T) / 2

    def _missing(self):
        p = self.plant
        self.P = p.A @ self.P @ p.A.T + p.Q


class ParticleFilter(ModelBased):
    """Bootstrap particle filter with systematic resampling."""
    name, msc = "particle", "MSC:65C35"
    assumptions = frozenset({"model", "process_stats", "noise_variance", "gaussian", "unbiased",
                             "no_outliers", "in_range", "white"})
    COUNT = 500

    def __init__(self, plant):
        super().__init__(plant)
        self.rng = np.random.default_rng(12345)
        self.particles = plant.x0_sd * self.rng.standard_normal((self.COUNT, plant.n))
        self.weights = np.full(self.COUNT, 1.0 / self.COUNT)

    def _predict(self):
        p = self.plant
        noise = p.sigma_w * self.rng.standard_normal(self.COUNT)
        self.particles = self.particles @ p.A.T + np.outer(noise, p.G)
        self.dev = self.weights @ self.particles

    def _correct(self, residual):
        p = self.plant
        errors = residual - self.particles @ p.C
        likelihood = np.exp(-0.5 * errors ** 2 / p.R)
        weights = self.weights * likelihood
        total = weights.sum()
        if total > 1e-300:                     # otherwise the reading is impossible under the model: skip it
            self.weights = weights / total
        self.dev = self.weights @ self.particles
        if 1.0 / np.sum(self.weights ** 2) < self.COUNT / 2:
            positions = (self.rng.random() + np.arange(self.COUNT)) / self.COUNT
            picks = np.minimum(np.searchsorted(np.cumsum(self.weights), positions), self.COUNT - 1)
            self.particles = self.particles[picks]
            self.weights = np.full(self.COUNT, 1.0 / self.COUNT)


class WindowModelBased(ModelBased):
    """Fits the deviation to the last WINDOW residuals, ignoring process noise inside the window."""

    def __init__(self, plant):
        super().__init__(plant)
        back = np.linalg.inv(plant.A)
        rows, power = [], np.eye(plant.n)
        for _ in range(WINDOW):
            rows.append(plant.C @ power)       # residual j steps ago = C A^-j d_now
            power = power @ back
        self.rows = np.array(rows)
        self.residuals = []

    def _correct(self, residual):
        self._push(residual)

    def _missing(self):
        self._push(np.nan)

    def _push(self, residual):
        self.residuals.insert(0, residual)
        del self.residuals[WINDOW:]
        values = np.array(self.residuals)
        keep = np.isfinite(values)
        if keep.sum() > self.plant.n:
            self.dev = self._fit(self.rows[:len(values)][keep], values[keep])

    def _fit(self, rows, values):
        raise NotImplementedError


class MovingHorizonLeastSquares(WindowModelBased):
    name, msc = "moving_horizon", "MSC:93E24"
    assumptions = frozenset({"model", "unbiased", "no_outliers", "in_range", "white"})

    def _fit(self, rows, values):
        return np.linalg.lstsq(rows, values, rcond=None)[0]


class BoundedErrorEstimator(WindowModelBased):
    """Set-membership estimate: the state that minimises the largest residual in the window."""
    name, msc = "bounded_error", "MSC:65G40"
    assumptions = frozenset({"model", "bounded", "unbiased", "no_outliers", "in_range"})

    def _fit(self, rows, values):
        n = rows.shape[1]
        cost = np.zeros(n + 1)
        cost[-1] = 1.0
        ones = np.ones((len(values), 1))
        result = linprog(cost, A_ub=np.vstack([np.hstack([rows, -ones]), np.hstack([-rows, -ones])]),
                         b_ub=np.concatenate([values, -values]),
                         bounds=[(None, None)] * n + [(0, None)], method="highs")
        if not result.success:
            raise RuntimeError(f"bounded-error fit failed: {result.message}")
        return result.x[:n]


class ModelFree(Estimator):
    """Uses the measurements only: no plant model and no input."""

    def __init__(self, plant):
        super().__init__(plant)
        self.estimate = None

    def step(self, z, u):
        if self.estimate is None:
            if not np.isfinite(z):
                return float(self.plant.C @ self.plant.x0)
            self._start(z)
            return self.estimate
        self._update(z)
        return float(self.estimate)

    def _start(self, z):
        self.estimate = float(z)

    def _update(self, z):
        raise NotImplementedError


class AlphaBetaTracker(ModelFree):
    """Fixed-gain position-and-rate tracker."""
    name, msc = "alpha_beta", "MSC:93C55"
    assumptions = frozenset({"smooth", "unbiased", "no_outliers", "in_range", "every_step"})
    ALPHA, BETA = 0.5, 0.1

    def _start(self, z):
        self.estimate, self.rate = float(z), 0.0

    def _update(self, z):
        self.estimate += self.rate
        if np.isfinite(z):
            residual = z - self.estimate
            self.estimate += self.ALPHA * residual
            self.rate += self.BETA * residual


class LowPassFilter(ModelFree):
    """First-order low-pass filter (exponential smoothing)."""
    name, msc = "low_pass", "MSC:94A12"
    assumptions = frozenset({"smooth", "unbiased", "no_outliers", "in_range"})
    ALPHA = 0.5

    def _update(self, z):
        if np.isfinite(z):
            self.estimate += self.ALPHA * (z - self.estimate)


class RepeatedMedian(ModelFree):
    """Robust straight-line fit over a window (Siegel's repeated median), read at the present."""
    name, msc = "repeated_median", "MSC:62G35"
    assumptions = frozenset({"smooth", "unbiased", "in_range"})

    def _start(self, z):
        self.estimate, self.history = float(z), [float(z)]

    def _update(self, z):
        self.history.insert(0, z)
        del self.history[WINDOW:]
        values = np.array(self.history)
        keep = np.isfinite(values)
        if keep.sum() < 3:
            return
        ages, values = -np.flatnonzero(keep).astype(float), values[keep]
        rise = values[None, :] - values[:, None]
        run = ages[None, :] - ages[:, None]
        np.fill_diagonal(run, np.nan)
        slope = np.median(np.nanmedian(rise / run, axis=1))
        self.estimate = float(np.median(values - slope * ages))


VARIANTS = (KalmanFilter, HuberKalman, LuenbergerObserver, HInfinityFilter, ParticleFilter,
            MovingHorizonLeastSquares, BoundedErrorEstimator, AlphaBetaTracker, LowPassFilter, RepeatedMedian)
NAMES = tuple(v.name for v in VARIANTS)


def run(variant, plant, z, u):
    """Estimates for a whole trial."""
    estimator = variant(plant)
    return np.array([estimator.step(z[k], u[k]) for k in range(len(z))])
