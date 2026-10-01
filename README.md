# agentdojo-two-way

Honest error bars for AgentDojo scores.

AgentDojo scores a model on every combination of a user task and an injected attack task. Many outcomes share the same user task or the same attack, so they are not independent, and the plain standard error that evaluation tools report by default treats them as if they were. This repository measures how much that matters on all 28 public AgentDojo pipelines and which correction gives intervals that can be trusted.

## Findings

- Correct standard errors are about twice the plain ones: two-way clustered SEs are 1.9 to 2.9 times the plain SE for utility and 1.3 to 3.5 times for attack success.
- A nominal 95% plain interval contains the true value only 61% (utility) and 66% (attack success) of the time, measured by simulation on AgentDojo's exact design.
- Clustering on one key does not fix it reliably. The rule proposed in [inspect_evals #2605](https://github.com/UKGovernmentBEIS/inspect_evals/issues/2605) (utility by user task, attack success by injection task) covers 85% on average for attack success and 71% for the worst pipeline.
- Owen's pigeonhole bootstrap, which resamples user tasks and attacks independently within each suite, is the only method that reaches about 95% coverage for every pipeline. Two-way clustered SEs (Cameron, Gelbach and Miller) come close, at 91 to 94%.
- 32 utility and 26 attack-success model comparisons that look significant with plain SEs are not significant once the dependence is accounted for (out of 241 pairs).
- The AgentDojo leaderboard averages only the 629 cells of benchmark version v1.1.2, which explains why it differs from means over all 949 v1.2 cells; the runs reproduce all 24 leaderboard rows to four decimals on that subset.

Full method, tables and limitations are in [RESULTS.md](RESULTS.md).

## Reproduce

Requires [uv](https://docs.astral.sh/uv/). No model calls; the data are AgentDojo's released runs.

```
uv sync
git clone --filter=blob:none --no-checkout https://github.com/ethz-spylab/agentdojo.git data/upstream
git -C data/upstream sparse-checkout set --no-cone '/runs/*/*/*/important_instructions/*.json'
git -C data/upstream checkout 089ed468cf3ed0322acc66b0211f26d9d90dbf60
uv run pytest -q
uv run python scripts/run_analysis.py
uv run python scripts/run_coverage.py
uv run python scripts/check_leaderboard.py
uv run python scripts/make_tables.py
```

## Layout

- `src/agentdojo_two_way/`: estimators (plain, one-way, two-way, pigeonhole bootstrap), data loading, coverage simulation
- `scripts/`: the analyses that write `results/`
- `results/`: per-pipeline tables, model-pair counts, coverage, leaderboard check
- `tests/`: unit tests, including a check that reproduces the numbers reported in #2605

## Credits and licence

The AgentDojo runs are by the AgentDojo authors (ETH Zurich SPY Lab), released under the MIT licence. The estimators follow Cameron, Gelbach and Miller (2011, JBES) and Owen (2007, AoAS). Code in this repository is MIT-licensed; see [LICENSE](LICENSE). Analysis written with Claude Code; every number comes from the scripts here.
