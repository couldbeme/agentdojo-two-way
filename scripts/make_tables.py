"""Render results/*.csv into markdown tables (results/tables.md) used by RESULTS.md."""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
R = ROOT / "results"
t = pd.read_csv(R / "se_table.csv")
c = pd.read_csv(R / "coverage.csv")
out = []


def md(df):
    cols = list(df.columns)
    lines = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for _, r in df.iterrows():
        lines.append("| " + " | ".join(str(r[k]) for k in cols) + " |")
    return "\n".join(lines)


for strat, title in ((True, "Suites as fixed strata (headline)"), (False, "Pooled (grand-mean centring, as in #2605)")):
    q = t[t.stratified == strat].copy()
    q["mean"] = q["mean"].map(lambda x: f"{x:.3f}")
    q["naive SE"] = q.se_naive.map(lambda x: f"{x:.4f}")
    for k, lab in (("user", "user"), ("inj", "inj"), ("twoway", "two-way"), ("pigeon", "pigeonhole")):
        q[lab] = q[f"ratio_{k}"].map(lambda x: f"{x:.2f}x")
    q["two-way SE"] = q.se_twoway.map(lambda x: f"{x:.4f}")
    out.append(f"## SE table: {title}\n\nRatios are SE / naive SE. n = cells.\n")
    out.append(md(q[["pipeline", "metric", "n", "mean", "naive SE", "user", "inj", "two-way",
                     "two-way SE", "pigeonhole"]]))
    out.append("")
    g = t[t.stratified == strat].groupby("metric")
    s = pd.DataFrame({
        "two-way ratio min": g.ratio_twoway.min(), "median": g.ratio_twoway.median(),
        "max": g.ratio_twoway.max(),
        "pigeonhole/two-way min": (t[t.stratified == strat].se_pigeon / t[t.stratified == strat].se_twoway).groupby(t.metric).min(),
        "pigeonhole/two-way max": (t[t.stratified == strat].se_pigeon / t[t.stratified == strat].se_twoway).groupby(t.metric).max(),
        "rule picks smaller one-way": g.rule_picks_smaller.sum(),
        "two-way < larger one-way": (t[t.stratified == strat].twoway_over_max_oneway < 1).groupby(t.metric).sum(),
        "CGM fallback used": g.twoway_fallback.sum(),
    }).round(2).reset_index()
    out.append(md(s))
    out.append("\nOne-key rule understates (picks the smaller one-way SE):\n")
    for m in ("utility", "attack_success"):
        names = t[(t.stratified == strat) & (t.metric == m) & t.rule_picks_smaller].pipeline.tolist()
        out.append(f"- {m}: {', '.join(names) if names else 'none'}")
    out.append("")

piv = c.pivot_table(index="method", columns="metric", values="coverage", aggfunc=["mean", "min", "max"])
piv.columns = [f"{a} {b}" for a, b in piv.columns]
c["se_ratio"] = c.mean_se / c.true_sd
sr = c.pivot_table(index="method", columns="metric", values="se_ratio", aggfunc="median")
sr.columns = [f"median SE/true SD {b}" for b in sr.columns]
cov = piv.join(sr).round(3).reset_index()
order = ["naive", "user", "inj", "twoway", "pigeon", "twoway_pooled"]
cov = cov.set_index("method").loc[order].reset_index()
out.append(f"## Coverage (R={c.R.iloc[0]}, B={c.B.iloc[0]}, 28 pipelines per metric)\n")
out.append(md(cov))
(R / "tables.md").write_text("\n".join(out) + "\n")
print("\n".join(out))
