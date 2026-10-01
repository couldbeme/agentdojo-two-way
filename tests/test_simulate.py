import numpy as np
import pytest
from scipy.special import expit

from agentdojo_two_way.simulate import Design, fit_crossed_logit, true_mean, simulate_y, coverage


def make_design(n_users=40, n_inj=30, n_suites=1):
    user, inj, suite = [], [], []
    for s in range(n_suites):
        for u in range(n_users):
            for i in range(n_inj):
                user.append(f"s{s}:u{u}")
                inj.append(f"s{s}:i{i}")
                suite.append(f"s{s}")
    return Design.from_keys(np.array(user), np.array(inj), np.array(suite))


def test_true_mean_no_random_effects_is_weighted_expit():
    mu = np.array([0.0, 1.0])
    w = np.array([0.25, 0.75])
    assert true_mean(mu, w, 0.0) == pytest.approx(0.25 * 0.5 + 0.75 * expit(1.0))


def test_true_mean_symmetric_and_matches_monte_carlo():
    assert true_mean(np.array([0.0]), np.array([1.0]), 4.0) == pytest.approx(0.5)
    z = np.random.default_rng(0).normal(0, 1.5, 2_000_000)
    mc = expit(-1.0 + z).mean()
    assert true_mean(np.array([-1.0]), np.array([1.0]), 1.5**2) == pytest.approx(mc, abs=1e-3)


def test_simulate_y_shape_and_binary():
    d = make_design(10, 5, 2)
    y = simulate_y({"mu": np.array([0.0, 0.0]), "sd_user": 1.0, "sd_inj": 1.0}, d,
                   np.random.default_rng(0))
    assert y.shape == (100,)
    assert set(np.unique(y)) <= {0.0, 1.0}


def test_fit_recovers_crossed_sds_roughly():
    d = make_design(60, 40, 1)
    truth = {"mu": np.array([0.3]), "sd_user": 1.2, "sd_inj": 0.8}
    y = simulate_y(truth, d, np.random.default_rng(1))
    est = fit_crossed_logit(y, d)
    assert est["sd_user"] == pytest.approx(1.2, rel=0.35)
    assert est["sd_inj"] == pytest.approx(0.8, rel=0.35)
    assert est["mu"][0] == pytest.approx(0.3, abs=0.5)


def test_coverage_naive_near_nominal_without_random_effects():
    d = make_design(20, 15, 1)
    params = {"mu": np.array([0.0]), "sd_user": 0.0, "sd_inj": 0.0}
    cov = coverage(params, d, R=400, B=200, seed=0)
    assert cov["naive"]["coverage"] == pytest.approx(0.95, abs=0.035)


def test_coverage_two_way_beats_naive_with_crossed_effects():
    d = make_design(20, 15, 1)
    params = {"mu": np.array([0.0]), "sd_user": 1.5, "sd_inj": 1.5}
    cov = coverage(params, d, R=300, B=200, seed=0)
    assert cov["twoway"]["coverage"] > cov["naive"]["coverage"] + 0.2
    assert set(cov) == {"naive", "user", "inj", "twoway", "twoway_pooled", "pigeon"}
    # pooled centring counts fixed suite differences as noise, so it is wider
    assert cov["twoway_pooled"]["mean_se"] >= cov["twoway"]["mean_se"] - 1e-12
