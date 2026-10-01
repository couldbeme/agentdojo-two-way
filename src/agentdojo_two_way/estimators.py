"""Standard errors for a benchmark mean over a crossed (user task x injection task) design.

All functions return the variance (or SE) of the plain cell mean ybar = sum(y)/n.

Fixed strata (AgentDojo suites). With ``strata`` given, residuals are centred on the
stratum mean instead of the grand mean. This is the cluster-robust variance of the
weighted combination sum_s (n_s/n) * beta_s from an OLS of y on stratum dummies, i.e.
suites are treated as fixed and only users/injections inside a suite are random. User
and injection clusters are nested in suites, so no cluster crosses a stratum. Suite is
not itself used as a cluster (4 clusters is too few). The point estimate is unchanged:
with weights n_s/n the weighted stratum means equal the pooled mean.

Small-sample factor: G/(G-1) on every clustered term (Cameron, Gelbach and Miller 2011),
which for singleton clusters gives n/(n-1). No (n-1)/(n-K) factor is applied.

Two-way: V = V_user + V_inj - V_(user and inj) (CGM 2011, eq. 2.13 scalar case). The
scalar can be negative in finite samples; then we fall back to max(V_user, V_inj) and
report the fallback flag. (CGM 2011 discuss an eigenvalue-clipping fix for matrices; in
the scalar case clipping to 0 would be anti-conservative, so the larger one-way term is
used instead.)
"""

from __future__ import annotations

import numpy as np


def _codes(key) -> np.ndarray:
    return np.unique(np.asarray(key), return_inverse=True)[1].ravel()


def _residuals(y: np.ndarray, strata) -> np.ndarray:
    if strata is None:
        return y - y.mean()
    s = _codes(strata)
    means = np.bincount(s, weights=y) / np.bincount(s)
    return y - means[s]


def naive_var(y) -> float:
    """What inspect_ai's default stderr() reports: sample variance / n (unclustered)."""
    y = np.asarray(y, dtype=float)
    return float(y.var(ddof=1) / len(y))


def cluster_var(y, key, strata=None) -> float:
    """One-way cluster-robust variance of the mean, with G/(G-1)."""
    y = np.asarray(y, dtype=float)
    n = len(y)
    e = _residuals(y, strata)
    c = _codes(key)
    sums = np.bincount(c, weights=e)
    G = len(sums)
    return float((sums @ sums) * G / (G - 1) / n**2)


def two_way_var(y, key1, key2, strata=None) -> tuple[float, bool]:
    """CGM two-way variance. Returns (variance, fallback_used)."""
    y = np.asarray(y, dtype=float)
    k1, k2 = _codes(key1), _codes(key2)
    inter = k1 * (k2.max() + 1) + k2
    v1 = cluster_var(y, k1, strata)
    v2 = cluster_var(y, k2, strata)
    v = v1 + v2 - cluster_var(y, inter, strata)
    if v < 0:
        return max(v1, v2), True
    return v, False


def pigeonhole_draws(y, key1, key2, strata=None, B=4000, seed=0) -> np.ndarray:
    """Owen (2007) pigeonhole bootstrap replicates of the mean.

    Rows (key1) and columns (key2) are resampled independently with replacement; a cell
    gets weight (count of its row) x (count of its column). With strata, rows and columns
    are resampled within their stratum and the stratum means are recombined with the
    fixed weights n_s/n. Replicates where a stratum gets zero total weight (possible only
    for incomplete crossings) are dropped.
    """
    rng = np.random.default_rng(seed)
    y = np.asarray(y, dtype=float)
    r, c = _codes(key1), _codes(key2)
    s = np.zeros(len(y), dtype=int) if strata is None else _codes(strata)
    S = s.max() + 1
    nr, nc = r.max() + 1, c.max() + 1
    row_stratum = np.zeros(nr, dtype=int)
    row_stratum[r] = s
    col_stratum = np.zeros(nc, dtype=int)
    col_stratum[c] = s
    if np.any(row_stratum[r] != s) or np.any(col_stratum[c] != s):
        raise ValueError("row/column keys must be nested in strata")
    wr = np.zeros((B, nr))
    wc = np.zeros((B, nc))
    for k in range(S):
        rows = np.flatnonzero(row_stratum == k)
        cols = np.flatnonzero(col_stratum == k)
        wr[:, rows] = rng.multinomial(len(rows), np.full(len(rows), 1 / len(rows)), size=B)
        wc[:, cols] = rng.multinomial(len(cols), np.full(len(cols), 1 / len(cols)), size=B)
    W = wr[:, r] * wc[:, c]
    ns = np.bincount(s, minlength=S) / len(y)
    tot = np.zeros(B)
    ok = np.ones(B, dtype=bool)
    for k in range(S):
        m = s == k
        den = W[:, m].sum(axis=1)
        ok &= den > 0
        with np.errstate(invalid="ignore", divide="ignore"):
            tot += ns[k] * (W[:, m] @ y[m]) / den
    return tot[ok]


def pigeonhole_se(y, key1, key2, strata=None, B=4000, seed=0) -> float:
    return float(np.std(pigeonhole_draws(y, key1, key2, strata, B, seed), ddof=1))


def summarize(y, user, inj, strata=None, B=4000, seed=0) -> dict:
    """Mean and the five SEs for one metric of one pipeline."""
    y = np.asarray(y, dtype=float)
    v2, fb = two_way_var(y, user, inj, strata)
    return {
        "mean": float(y.mean()),
        "n": len(y),
        "G_user": len(np.unique(user)),
        "G_inj": len(np.unique(inj)),
        "se_naive": float(np.sqrt(naive_var(y))),
        "se_user": float(np.sqrt(cluster_var(y, user, strata))),
        "se_inj": float(np.sqrt(cluster_var(y, inj, strata))),
        "se_twoway": float(np.sqrt(v2)),
        "twoway_fallback": fb,
        "se_pigeon": pigeonhole_se(y, user, inj, strata, B, seed),
    }
