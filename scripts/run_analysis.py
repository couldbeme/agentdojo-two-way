"""Per-pipeline SE table, one-key-rule check and pairwise significance counts.

Usage: uv run python scripts/run_analysis.py [runs_dir] [out_dir]
"""

import itertools
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from agentdojo_two_way.data import load_runs, paired_cells
from agentdojo_two_way.estimators import (cluster_var, naive_var, pigeonhole_se, summarize,
                                          two_way_var)

ROOT = Path(__file__).resolve().parents[1]
RUNS = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "data" / "upstream" / "runs"
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "results"
METRICS = {"utility": "utility", "security": "attack_success"}
DEFENCES = ("repeat_user_prompt", "spotlighting_with_delimiting", "tool_filter",
            "transformers_pi_detector")
RULE_KEY = {"utility": "user", "security": "inj"}  # inspect_evals #2605 suggestion


def is_defence(p):
    return any(p.endswith(s) for s in DEFENCES)


def main():
    OUT.mkdir(exist_ok=True)
    df = load_runs(RUNS)
    rows = []
    for p, g in df.groupby("pipeline", sort=True):
        for m, label in METRICS.items():
            y = g[m].to_numpy()
            for strat in (True, False):
                s = summarize(y, g["user"], g["inj"], strata=g["suite"] if strat else None,
                              B=4000, seed=0)
                rows.append({"pipeline": p, "metric": label, "stratified": strat,
                             "n_errors": int(g["error"].notna().sum()), **s})
    t = pd.DataFrame(rows)
    for k in ("user", "inj", "twoway", "pigeon"):
        t[f"ratio_{k}"] = t[f"se_{k}"] / t["se_naive"]
    rule = t["metric"].map({"utility": "se_user", "attack_success": "se_inj"})
    other = t["metric"].map({"utility": "se_inj", "attack_success": "se_user"})
    t["rule_se"] = [r[c] for (_, r), c in zip(t.iterrows(), rule)]
    t["other_se"] = [r[c] for (_, r), c in zip(t.iterrows(), other)]
    t["rule_picks_smaller"] = t["rule_se"] < t["other_se"]
    t["twoway_over_max_oneway"] = t["se_twoway"] / t[["se_user", "se_inj"]].max(axis=1)
    t.to_csv(OUT / "se_table.csv", index=False)

    # pairwise: only pipelines with identical cell sets (same benchmark version)
    cellsets = {p: frozenset(map(tuple, g[["suite", "user", "inj"]].to_numpy()))
                for p, g in df.groupby("pipeline")}
    groups = {}
    for p, cs in cellsets.items():
        groups.setdefault(cs, []).append(p)
    prs = []
    for cs, ps in groups.items():
        if len(ps) < 2:
            continue
        for a, b in itertools.combinations(sorted(ps), 2):
            for m, label in METRICS.items():
                pc = paired_cells(df, a, b, m)
                d = pc["d"].to_numpy()
                Gu, Gi = pc["user"].nunique(), pc["inj"].nunique()
                v2, fb = two_way_var(d, pc["user"], pc["inj"], pc["suite"])
                se = {
                    "naive": (np.sqrt(naive_var(d)), stats.norm.ppf(0.975)),
                    "user": (np.sqrt(cluster_var(d, pc["user"], pc["suite"])),
                             stats.t.ppf(0.975, Gu - 1)),
                    "inj": (np.sqrt(cluster_var(d, pc["inj"], pc["suite"])),
                            stats.t.ppf(0.975, Gi - 1)),
                    "twoway": (np.sqrt(v2), stats.t.ppf(0.975, min(Gu, Gi) - 1)),
                    "pigeon": (pigeonhole_se(d, pc["user"], pc["inj"], pc["suite"], B=2000,
                                             seed=0), stats.norm.ppf(0.975)),
                }
                row = {"a": a, "b": b, "metric": label, "n_cells": len(d),
                       "both_models": not (is_defence(a) or is_defence(b)),
                       "mean_diff": d.mean(), "twoway_fallback": fb}
                for k, (s, q) in se.items():
                    row[f"se_{k}"] = s
                    row[f"sig_{k}"] = bool(s > 0 and abs(d.mean()) > q * s) or (
                        s == 0 and d.mean() != 0)
                row["sig_rule"] = row["sig_user"] if m == "utility" else row["sig_inj"]
                prs.append(row)
    pr = pd.DataFrame(prs)
    pr.to_csv(OUT / "pairwise.csv", index=False)

    summary = {
        "upstream_commit": (ROOT / "data" / "UPSTREAM_COMMIT").read_text().strip()
        if (ROOT / "data" / "UPSTREAM_COMMIT").exists() else None,
        "n_pipelines": int(df.pipeline.nunique()),
        "n_cells": int(len(df)),
        "skipped_missing_outcome": df.attrs["skipped_missing_outcome"],
        "cells_with_error": {k: int(v) for k, v in df[df.error.notna()].groupby("pipeline").size().items()},
        "pairwise_groups": {str(len(cs)): sorted(ps)
                            for cs, ps in groups.items()},
    }
    for subset, mask in (("all_pairs", pr.index == pr.index), ("model_pairs", pr.both_models)):
        for label in METRICS.values():
            q = pr[mask & (pr.metric == label)]
            summary[f"{subset}:{label}"] = {
                "pairs": int(len(q)),
                **{f"sig_{k}": int(q[f"sig_{k}"].sum())
                   for k in ("naive", "user", "inj", "rule", "twoway", "pigeon")},
            }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
