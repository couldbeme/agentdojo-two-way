"""Compare AgentDojo's published results table (docs/results-table.html at the pinned
commit) with means of the runs/ files, on all cells and on the v1.1.2 cell subset
(the 629 cells shared with the 2024 runs). Writes results/leaderboard_check.csv."""

import re
import subprocess
from pathlib import Path

import pandas as pd

from agentdojo_two_way.data import load_runs

ROOT = Path(__file__).resolve().parents[1]
UP = ROOT / "data" / "upstream"

html = subprocess.run(["git", "-C", str(UP), "show", "HEAD:docs/results-table.html"],
                      capture_output=True, text=True, check=True).stdout
lb = {}
for r in re.findall(r"<tr>(.*?)</tr>", html, re.S):
    c = [re.sub("<.*?>", "", x).strip() for x in re.findall(r"<td>(.*?)</td>", r, re.S)]
    if len(c) >= 7 and c[3] == "important_instructions":
        key = c[1].replace("/", "_") + ("" if c[2] == "None" else "-" + c[2])
        lb[key] = (float(c[5][:-1]) / 100, float(c[6][:-1]) / 100)

df = load_runs(UP / "runs")
ref = set(map(tuple, df[df.pipeline == "gpt-4o-2024-05-13"][["suite", "user", "inj"]].values))
rows = []
for p, g in df.groupby("pipeline"):
    sub = g[[tuple(x) in ref for x in g[["suite", "user", "inj"]].values]]
    lu, ls = lb.get(p, (None, None))
    rows.append({"pipeline": p, "n_all": len(g), "util_all": g.utility.mean(),
                 "asr_all": g.security.mean(), "n_v112": len(sub),
                 "util_v112": sub.utility.mean(), "asr_v112": sub.security.mean(),
                 "lb_util": lu, "lb_asr": ls})
t = pd.DataFrame(rows)
t["v112_matches_lb"] = ((t.util_v112 - t.lb_util).abs() < 5e-5) & ((t.asr_v112 - t.lb_asr).abs() < 5e-5)
t.to_csv(ROOT / "results" / "leaderboard_check.csv", index=False)
print(t.round(4).to_string(index=False))
print("on leaderboard:", t.lb_util.notna().sum(), "matched on v1.1.2 subset:", t.v112_matches_lb.sum())
