"""FLASH demonstrator: simulator, faults, variants, scoring and bounded proofs.

These tests check the machinery. They do not run the fault campaign.
"""
import sys
import time
from pathlib import Path

import numpy as np
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from flash_demo import analysis, campaign, verify  # noqa: E402
from flash_demo.faults import KINDS, LEVELS, NOMINAL, Fault, campaign_faults  # noqa: E402
from flash_demo.plants import ONSET, PLANTS, STEPS, simulate  # noqa: E402
from flash_demo.variants import ASSUMPTIONS, NAMES, VARIANTS, run  # noqa: E402

PLANT_LIST = [make() for make in PLANTS.values()]


# ---- simulator and faults

def test_same_seed_gives_same_trial():
    for plant in PLANT_LIST:
        first, second = simulate(plant, NOMINAL, 5), simulate(plant, NOMINAL, 5)
        for a, b in zip(first, second):
            assert np.array_equal(a, b)


def test_faults_leave_the_trial_untouched_before_onset():
    plant = PLANT_LIST[0]
    truth, z, _ = simulate(plant, NOMINAL, 11)
    for fault in campaign_faults():
        t, zf, _ = simulate(plant, fault, 11)
        assert np.array_equal(zf[:ONSET], z[:ONSET]), fault
        if fault.kind != "mismatch":
            assert np.allclose(t[:ONSET + 1], truth[:ONSET + 1])


def test_bias_dropout_and_stuck_do_what_they_say():
    plant = PLANT_LIST[1]
    _, z, _ = simulate(plant, NOMINAL, 3)
    _, biased, _ = simulate(plant, Fault("bias", 2.0), 3)
    assert np.allclose(biased[ONSET:] - z[ONSET:], 2.0 * plant.sigma_v)
    _, dropped, _ = simulate(plant, Fault("dropout", 25), 3)
    assert np.isnan(dropped).sum() == 25 and np.isnan(dropped[ONSET:ONSET + 25]).all()
    _, stuck, _ = simulate(plant, Fault("stuck", 10), 3)
    assert np.all(stuck[ONSET:ONSET + 10] == stuck[ONSET - 1])


def test_campaign_has_every_kind_and_level():
    faults = campaign_faults()
    assert len(faults) == sum(len(levels) for levels in LEVELS.values()) == 36
    assert {f.kind for f in faults} == set(KINDS)
    with pytest.raises(ValueError):
        Fault("gremlins", 1.0)


def test_campaign_and_development_seeds_do_not_overlap():
    scored = {task[-1] for task in campaign.tasks()}
    development = {task[-1] for task in campaign.tasks(nominal=True, repeats=20)}
    assert len(scored) == 3 * 36 * campaign.REPEATS and not scored & development


# ---- variants

def test_ten_variants_with_distinct_lineages_and_known_assumptions():
    assert len(VARIANTS) == 10 and len(set(NAMES)) == 10
    assert len({v.msc for v in VARIANTS}) == 10
    for variant in VARIANTS:
        assert variant.assumptions and variant.assumptions <= set(ASSUMPTIONS), variant.name
        assert "unbiased" in variant.assumptions


def test_lineage_nodes_exist_in_the_mathematics_map():
    sys.path.insert(0, str(ROOT / "engine" / "v3"))
    import correspondences
    index = correspondences.NodeIndex(ROOT)
    for variant in VARIANTS:
        assert index.field_of(variant.msc) == "MA", variant.name


@pytest.mark.parametrize("plant", PLANT_LIST, ids=lambda p: p.name)
def test_every_variant_meets_the_spec_without_faults(plant):
    for seed in (campaign.DEVELOPMENT_SEED + 500, campaign.DEVELOPMENT_SEED + 501):
        truth, z, u = simulate(plant, NOMINAL, seed)
        for variant in VARIANTS:
            share, _, finite, fail = campaign.score(plant, truth, run(variant, plant, z, u))
            assert finite and not fail, (variant.name, share)


finite_or_missing = st.one_of(st.just(float("nan")), st.floats(min_value=-1000, max_value=1000))


@settings(max_examples=40, deadline=None)
@given(readings=st.lists(finite_or_missing, min_size=1, max_size=40), which=st.integers(0, 2))
def test_s2_output_is_finite_for_any_readings(readings, which):
    plant = PLANT_LIST[which]
    z = np.array(readings) * plant.sigma_v
    u = np.array([plant.input_fn(k) for k in range(len(z))])
    for variant in VARIANTS:
        assert np.all(np.isfinite(run(variant, plant, z, u))), variant.name


def test_variants_are_deterministic():
    plant = PLANT_LIST[2]
    _, z, u = simulate(plant, Fault("outliers", 0.1), 21)
    for variant in VARIANTS:
        assert np.array_equal(run(variant, plant, z, u), run(variant, plant, z, u)), variant.name


def test_s4_step_time_is_within_budget():
    plant = PLANT_LIST[0]
    _, z, u = simulate(plant, NOMINAL, 2, steps=100)
    for variant in VARIANTS:
        start = time.perf_counter()
        run(variant, plant, z, u)
        assert (time.perf_counter() - start) / 100 < 0.005, variant.name


# ---- scoring and analysis

def test_score_flags_violations_and_non_finite_output():
    plant = PLANT_LIST[1]
    truth = np.zeros(STEPS)
    assert campaign.score(plant, truth, truth.copy())[3] is False
    off = truth.copy()
    off[200:240] = 3 * plant.sigma_v                  # 40 of 350 scored steps: above 5%
    assert campaign.score(plant, truth, off)[3] is True
    off = truth.copy()
    off[200:210] = 3 * plant.sigma_v                  # 10 of 350: below 5%
    assert campaign.score(plant, truth, off)[3] is False
    broken = truth.copy()
    broken[10] = np.nan
    assert campaign.score(plant, truth, broken) == (1.0, float("inf"), False, True)


def test_distances_are_symmetric_and_assumption_distance_is_jaccard():
    distances = analysis.distance_matrices()
    for matrix in distances.values():
        assert np.allclose(matrix, matrix.T) and np.all(np.diag(matrix) == 0)
    kalman, particle = NAMES.index("kalman"), NAMES.index("particle")
    assert distances["assumption"][kalman, particle] == 0.0       # identical assumption sets
    assert distances["lineage_tree"][kalman, NAMES.index("moving_horizon")] == 2


def test_phi_and_mantel_on_constructed_data():
    rng = np.random.default_rng(0)
    base = rng.integers(0, 2, 200)
    fails = np.array([base, base, 1 - base, np.zeros(200, dtype=int)] + [rng.integers(0, 2, 200) for _ in range(6)])
    phi = analysis.phi_matrix(fails)
    assert phi[0, 1] == pytest.approx(1.0) and phi[0, 2] == pytest.approx(-1.0)
    assert np.isnan(phi[0, 3])                                   # a variant that never fails
    distance = np.where(np.isfinite(phi), 1 - phi, 0.0)           # distance built to track phi exactly
    result = analysis.mantel(distance, phi, np.random.default_rng(1))
    assert result["rho"] == pytest.approx(-1.0) and result["p"] < 0.01


def test_missing_campaign_file_is_an_error(tmp_path):
    with pytest.raises(SystemExit):
        analysis.load(tmp_path / "nope.csv")


# ---- bounded proofs

def test_z3_proves_the_invariant_and_refutes_a_tighter_one():
    rows = verify.run()
    assert [row["variant"] for row in rows] == ["luenberger", "kalman", "h_infinity"]
    for row in rows:
        assert row["invariant_proved"] and row["below_bound_refuted"], row


def test_z3_finds_a_counterexample_for_a_false_claim():
    assert verify.prove_invariant(0.95, 0.2, 0.15, 1.5, 0.1) is False
