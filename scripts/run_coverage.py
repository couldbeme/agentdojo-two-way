"""Coverage of 95% intervals on AgentDojo's exact crossed design, per pipeline x metric.

Usage: uv run python scripts/run_coverage.py [R] [B]   (defaults 2000 replicates, 500 bootstrap)
"""

import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd

from agentdojo_two_way.data import load_runs
from agentdojo_two_way.simulate import Design, coverage, fit_crossed_logit

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "data" / "upstream" / "runs"
OUT = ROOT / "results"
R = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
B = int(sys.argv[2]) if len(sys.argv) > 2 else 500
METRICS = {"utility": "utility", "security": "attack_success"}


def job(args):
    k, pipeline, metric, y, user, inj, suite = args
    d = Design.from_keys(user, inj, suite)
    params = fit_crossed_logit(y, d)
    cov = coverage(params, d, R=R, B=B, seed=1000 + k)
    rows = []
    for method, c in cov.items():
        rows.append({"pipeline": pipeline, "metric": METRICS[metric], "method": method,
                     "obs_mean": float(np.mean(y)), "sd_user": params["sd_user"],
                     "sd_inj": params["sd_inj"], **c})
    return rows


def main():
    df = load_runs(RUNS)
    jobs = []
    for p, g in df.groupby("pipeline", sort=True):
        for m in METRICS:
            jobs.append((len(jobs), p, m, g[m].to_numpy(), g["user"].to_numpy(),
                         g["inj"].to_numpy(), g["suite"].to_numpy()))
    with ProcessPoolExecutor() as ex:
        rows = [r for rs in ex.map(job, jobs) for r in rs]
    out = pd.DataFrame(rows)
    out["R"], out["B"] = R, B
    out.to_csv(OUT / "coverage.csv", index=False)
    print(out.pivot_table(index="method", columns="metric", values="coverage",
                          aggfunc=["mean", "min", "max"]).round(3))


if __name__ == "__main__":
    main()
