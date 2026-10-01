import numpy as np
import pytest
import statsmodels.api as sm
from statsmodels.stats.sandwich_covariance import cov_cluster, cov_cluster_2groups

from agentdojo_two_way.estimators import (
    naive_var,
    cluster_var,
    two_way_var,
    pigeonhole_se,
    summarize,
)


def crossed(n_users=12, n_inj=8, n_suites=1, seed=0, su=1.0, si=1.0):
    rng = np.random.default_rng(seed)
    user, inj, suite, y = [], [], [], []
    for s in range(n_suites):
        a = rng.normal(0, su, n_users)
        b = rng.normal(0, si, n_inj)
        for u in range(n_users):
            for i in range(n_inj):
                p = 1 / (1 + np.exp(-(a[u] + b[i])))
                user.append(f"s{s}:u{u}")
                inj.append(f"s{s}:i{i}")
                suite.append(f"s{s}")
                y.append(float(rng.random() < p))
    return np.array(y), np.array(user), np.array(inj), np.array(suite)


def test_naive_is_sample_variance_over_n():
    y = np.array([1.0, 0, 1, 1, 0, 1])
    assert naive_var(y) == pytest.approx(y.var(ddof=1) / len(y))


def test_singleton_clusters_reduce_to_naive():
    y, *_ = crossed()
    ids = np.arange(len(y))
    assert cluster_var(y, ids) == pytest.approx(naive_var(y))


def test_one_way_matches_statsmodels_intercept_only():
    y, user, _, _ = crossed()
    res = sm.OLS(y, np.ones((len(y), 1))).fit()
    codes = np.unique(user, return_inverse=True)[1]
    ref = cov_cluster(res, codes)[0, 0]  # G/(G-1) * (n-1)/(n-1)
    assert cluster_var(y, user) == pytest.approx(ref, rel=1e-10)


def test_two_way_matches_statsmodels_cgm():
    y, user, inj, _ = crossed()
    res = sm.OLS(y, np.ones((len(y), 1))).fit()
    cu = np.unique(user, return_inverse=True)[1]
    ci = np.unique(inj, return_inverse=True)[1]
    ref = cov_cluster_2groups(res, cu, ci)[0][0, 0]
    v, fallback = two_way_var(y, user, inj)
    assert not fallback
    assert v == pytest.approx(ref, rel=1e-10)


def test_two_way_with_unique_second_key_equals_one_way():
    y, user, _, _ = crossed()
    v, _ = two_way_var(y, user, np.arange(len(y)))
    assert v == pytest.approx(cluster_var(y, user))


def test_negative_two_way_falls_back_to_larger_one_way():
    # checkerboard: row and column sums of residuals are zero, intersection is not
    y = np.array([1.0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0])
    user = np.array(["a", "a", "b", "b", "c", "c", "d", "d", "e", "e", "f", "f"])
    inj = np.array(["x", "y", "x", "y", "x", "y", "x", "y", "x", "y", "x", "y"])
    raw = cluster_var(y, user) + cluster_var(y, inj) - cluster_var(y, np.arange(len(y)))
    assert raw < 0
    v, fallback = two_way_var(y, user, inj)
    assert fallback
    assert v == pytest.approx(max(cluster_var(y, user), cluster_var(y, inj)))


def test_stratified_one_way_matches_ols_on_stratum_dummies():
    # fixed strata = OLS on suite dummies; target is the n_s/n weighted sum of suite means
    y, user, _, suite = crossed(n_users=6, n_inj=5, n_suites=3, seed=3)
    levels, sidx = np.unique(suite, return_inverse=True)
    X = np.eye(len(levels))[sidx]
    res = sm.OLS(y, X).fit()
    codes = np.unique(user, return_inverse=True)[1]
    n, k = len(y), len(levels)
    cov = cov_cluster(res, codes) * (n - k) / (n - 1)  # strip the (n-1)/(n-k) factor
    w = np.bincount(sidx) / n
    assert cluster_var(y, user, strata=suite) == pytest.approx(w @ cov @ w, rel=1e-10)


def test_stratified_differs_from_pooled_when_strata_means_differ():
    y, user, _, suite = crossed(n_users=6, n_inj=5, n_suites=3, seed=3)
    y = y.copy()
    y[suite == "s0"] = 1.0
    assert cluster_var(y, user, strata=suite) < cluster_var(y, user)


def test_pigeonhole_tracks_dominant_factor_and_is_reproducible():
    # strong user effect, no injection effect: pigeonhole near one-way-by-user
    y, user, inj, _ = crossed(n_users=40, n_inj=30, su=2.0, si=0.0, seed=1)
    a = pigeonhole_se(y, user, inj, B=2000, seed=7)
    b = pigeonhole_se(y, user, inj, B=2000, seed=7)
    assert a == b
    assert a == pytest.approx(np.sqrt(cluster_var(y, user)), rel=0.15)


def test_pigeonhole_stratified_runs_and_is_positive():
    y, user, inj, suite = crossed(n_users=8, n_inj=5, n_suites=3, seed=2)
    se = pigeonhole_se(y, user, inj, strata=suite, B=500, seed=0)
    assert se > 0


def test_summarize_keys_and_ratios():
    y, user, inj, suite = crossed(n_users=8, n_inj=5, n_suites=2, seed=4)
    out = summarize(y, user, inj, strata=suite, B=200, seed=0)
    for k in ["mean", "n", "G_user", "G_inj", "se_naive", "se_user", "se_inj",
              "se_twoway", "se_pigeon", "twoway_fallback"]:
        assert k in out
    assert out["G_user"] == 16 and out["G_inj"] == 10
    assert out["mean"] == pytest.approx(y.mean())
