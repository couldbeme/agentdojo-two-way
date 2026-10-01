"""Parametric coverage study on AgentDojo's exact crossed design.

Generating model (per pipeline and metric), fitted to the observed cells:
    y_cell ~ Bernoulli(expit(mu_suite + a_user + b_inj)),
    a_user ~ N(0, sd_user^2), b_inj ~ N(0, sd_inj^2), independent.
Suites are fixed (mu_suite are fixed effects); users and injections are random and
nested in suites; sd_user and sd_inj are common to all suites. There is one replicate per
cell, so a user x injection interaction is not identifiable separately from Bernoulli
noise and is left out.

Fit: statsmodels BinomialBayesMixedGLM.fit_vb (variational Bayes, crossed variance
components). Estimand: the super-population mean sum_s (n_s/n) E[expit(mu_s + a + b)],
i.e. the score expected for a fresh draw of users and injections in the same suites.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import sparse
from scipy import stats
from scipy.special import expit
from statsmodels.genmod.bayes_mixed_glm import BinomialBayesMixedGLM

from .estimators import cluster_var, naive_var, two_way_var, pigeonhole_draws

METHODS = ("naive", "user", "inj", "twoway", "twoway_pooled", "pigeon")


@dataclass
class Design:
    user: np.ndarray  # integer codes
    inj: np.ndarray
    suite: np.ndarray
    n_user: int
    n_inj: int
    n_suite: int

    @classmethod
    def from_keys(cls, user, inj, suite) -> "Design":
        u = np.unique(np.asarray(user), return_inverse=True)[1].ravel()
        i = np.unique(np.asarray(inj), return_inverse=True)[1].ravel()
        s = np.unique(np.asarray(suite), return_inverse=True)[1].ravel()
        return cls(u, i, s, u.max() + 1, i.max() + 1, s.max() + 1)

    @property
    def weights(self) -> np.ndarray:
        return np.bincount(self.suite, minlength=self.n_suite) / len(self.suite)


def true_mean(mu, weights, var_total, n_nodes: int = 80) -> float:
    """sum_s w_s E[expit(mu_s + z)], z ~ N(0, var_total), by Gauss-Hermite."""
    x, wq = np.polynomial.hermite_e.hermegauss(n_nodes)
    wq = wq / wq.sum()
    sd = np.sqrt(var_total)
    per = np.array([(wq * expit(m + sd * x)).sum() for m in np.asarray(mu)])
    return float(np.asarray(weights) @ per)


def simulate_y(params: dict, d: Design, rng) -> np.ndarray:
    a = rng.normal(0, params["sd_user"], d.n_user)
    b = rng.normal(0, params["sd_inj"], d.n_inj)
    p = expit(params["mu"][d.suite] + a[d.user] + b[d.inj])
    return (rng.random(len(p)) < p).astype(float)


def fit_crossed_logit(y, d: Design) -> dict:
    y = np.asarray(y, dtype=float)
    n = len(y)
    X = np.eye(d.n_suite)[d.suite]
    Zu = sparse.csr_matrix((np.ones(n), (np.arange(n), d.user)), shape=(n, d.n_user))
    Zi = sparse.csr_matrix((np.ones(n), (np.arange(n), d.inj)), shape=(n, d.n_inj))
    Z = sparse.hstack([Zu, Zi]).tocsr()
    ident = np.r_[np.zeros(d.n_user, dtype=int), np.ones(d.n_inj, dtype=int)]
    model = BinomialBayesMixedGLM(y, X, Z, ident, vcp_p=1.0, fe_p=2.0)
    r = model.fit_vb()
    sd = np.exp(r.vcp_mean)  # vcp parameters are log standard deviations
    return {"mu": np.asarray(r.fe_mean), "sd_user": float(sd[0]), "sd_inj": float(sd[1])}


def _intervals(y, d: Design, B: int, seed: int) -> dict:
    m = y.mean()
    Gu, Gi = d.n_user, d.n_inj
    v2, _ = two_way_var(y, d.user, d.inj, d.suite)
    v2p, _ = two_way_var(y, d.user, d.inj)  # grand-mean centring, suites ignored
    draws = pigeonhole_draws(y, d.user, d.inj, d.suite, B=B, seed=seed)
    ses = {
        "naive": (np.sqrt(naive_var(y)), stats.norm.ppf(0.975)),
        "user": (np.sqrt(cluster_var(y, d.user, d.suite)), stats.t.ppf(0.975, Gu - 1)),
        "inj": (np.sqrt(cluster_var(y, d.inj, d.suite)), stats.t.ppf(0.975, Gi - 1)),
        "twoway": (np.sqrt(v2), stats.t.ppf(0.975, min(Gu, Gi) - 1)),
        "twoway_pooled": (np.sqrt(v2p), stats.t.ppf(0.975, min(Gu, Gi) - 1)),
        "pigeon": (np.std(draws, ddof=1), stats.norm.ppf(0.975)),
    }
    return {k: (m, se, q) for k, (se, q) in ses.items()}


def coverage(params: dict, d: Design, R: int = 2000, B: int = 500, seed: int = 0) -> dict:
    """Share of R replicates whose 95% interval mean +/- q*SE contains the true mean.
    All but twoway_pooled centre on suite means (fixed strata). Naive and pigeonhole use z; one-way uses t(G-1); two-way uses t(min(G_user,G_inj)-1)."""
    rng = np.random.default_rng(seed)
    theta = true_mean(params["mu"], d.weights, params["sd_user"] ** 2 + params["sd_inj"] ** 2)
    hit = {k: 0 for k in METHODS}
    se_sum = {k: 0.0 for k in METHODS}
    ests = np.empty(R)
    for r in range(R):
        y = simulate_y(params, d, rng)
        ests[r] = y.mean()
        for k, (m, se, q) in _intervals(y, d, B, seed=int(rng.integers(2**31))).items():
            hit[k] += abs(m - theta) <= q * se
            se_sum[k] += se
    sd_true = float(ests.std(ddof=1))
    return {
        k: {"coverage": hit[k] / R, "mean_se": se_sum[k] / R, "true_sd": sd_true,
            "theta": theta}
        for k in METHODS
    }
