# Two-way clustered intervals for AgentDojo

Data: every pipeline in `runs/` of github.com/ethz-spylab/agentdojo at commit `089ed468cf3ed0322acc66b0211f26d9d90dbf60` (2026-06-02), attack `important_instructions` only. 28 pipelines, 19,381 files (226 MB by the git tree), 19,380 cells with an outcome. No model was run. All numbers below are produced by the scripts in `scripts/` and stored in `results/`. The AgentDojo runs are by the AgentDojo authors (ETH Zurich SPY Lab) and are MIT-licensed; the derived tables in `results/` keep that attribution. This repository's code is MIT-licensed (see `LICENSE`).

## What was estimated

Each cell is one (suite, user task, injection task) episode with two binary outcomes: utility, and `security`, which AgentDojo sets when the injected task was executed (attack success). The target is the plain cell mean that AgentDojo and inspect_evals report. Five standard errors are computed for it:

1. naive: sample variance / n, what inspect_ai's default `stderr()` reports;
2. one-way cluster-robust by user task;
3. one-way cluster-robust by injection task;
4. two-way Cameron, Gelbach and Miller (2011): V_user + V_inj - V_(user and inj), each term with G/(G-1); if the sum is negative the larger one-way term is used and flagged (it never was);
5. Owen's (2007) pigeonhole bootstrap: users and injections resampled independently, cell weight = product of the two counts.

Suites are fixed strata: residuals are centred on suite means rather than on the grand mean. The result equals the cluster-robust variance of the n_s/n-weighted combination of suite means from a regression on suite dummies, and a test checks this against statsmodels. The pigeonhole bootstrap resamples users and injections within their suite and recombines suite means with fixed n_s/n weights. Suite is never a cluster: four clusters is too few. Task ids repeat across suites, so all keys are suite-qualified. Interval critical values: z for naive and pigeonhole, t(G-1) for one-way, t(min(G_user, G_inj)-1) for two-way. The pooled variant (grand-mean centring, suites ignored) is also reported because it is what issue #2605 computed; on claude-3-7-sonnet it reproduces that issue's numbers (naive 0.0125 and 0.0070, user 0.0334, injection 0.0177), and a test pins this.

## Headline

With suites fixed, the two-way SE is 1.89x to 2.89x the naive SE for utility (median 2.16x) and 1.33x to 3.45x for attack success (median 2.12x). Pooled, the ratios are larger, 2.03x to 3.37x (median 2.48x) and 1.53x to 4.31x (median 2.83x), because grand-mean centring counts the fixed differences between suites as sampling noise.

The pigeonhole SE is 1.05x to 1.18x the two-way SE for utility and 1.03x to 1.35x for attack success.

In the coverage simulation below, nominal 95% naive intervals cover 61% (utility) and 66% (attack success) of the time on average. The two-way interval covers 93.5% and 91.3%. The pigeonhole interval covers 95.2% and 94.9%.

## The one-key rule in #2605

Issue #2605 suggests clustering utility by user task and security by injection task. Using the issue's pooled convention, that rule picks the smaller of the two one-way SEs for 4 of 28 pipelines on utility (claude-3-5-sonnet-20240620, gpt-4-0125-preview, gpt-4o-2024-05-13, gpt-4o-2024-05-13-spotlighting_with_delimiting) and 4 of 28 on attack success (Meta-SecAlign-70B, Meta-SecAlign-70B-repeat_user_prompt, command-r, command-r-plus). With suites fixed, it understates for 2 of 28 on utility (claude-3-5-sonnet-20240620, gpt-4-0125-preview) and 10 of 28 on attack success (both Meta-SecAlign-70B pipelines, command-r, command-r-plus, gemini-1.5-pro-002, gemini-2.0-flash-001, gemini-2.0-flash-exp, gpt-4o-mini-2024-07-18, and both Llama-3.3-70B pipelines). In the simulation the rule's interval covers 92.9% on average for utility (worst pipeline 86.0%) but 84.8% for attack success (worst 70.8%).

The dominant key also changes between levels and differences. For a paired difference between two pipelines on the same cells, the injection effect largely cancels: the median ratio of injection-clustered to naive SE on utility differences is 0.90, against 1.93 for user clustering.

## Model comparisons

Pairs are formed only between pipelines with identical cell sets: the 22 pipelines on the 629-cell set (v1.1.2 tasks) and the 5 on the 949-cell set (v1.2 tasks), 241 pairs. Llama-3.3-70B-Instruct-repeat_user_prompt (797 cells) is in neither. For each pair the cell-level difference d = y_a - y_b is analysed with the same estimators and strata; a pair counts as significant if |mean d| exceeds the critical value times the SE.

| metric | pairs | naive | user | injection | #2605 rule | two-way | pigeonhole |
|---|---|---|---|---|---|---|---|
| utility, all pipelines | 241 | 199 | 168 | 203 | 168 | 167 | 159 |
| attack success, all pipelines | 241 | 211 | 205 | 191 | 191 | 185 | 179 |
| utility, no defence pipelines | 159 | 126 | 103 | 128 | 103 | 101 | 96 |
| attack success, no defence pipelines | 159 | 140 | 136 | 131 | 131 | 127 | 121 |

Every pair significant under two-way is also significant under naive. Moving from naive to two-way, 32 utility pairs and 26 attack-success pairs stop being separable (16% and 12% of the naive-significant ones). "No defence" drops the pipelines run with a defence: the four gpt-4o defence variants and Meta-SecAlign-70B-repeat_user_prompt.

## Coverage on the real crossed structure

For each pipeline and metric, a logit model y ~ Bernoulli(expit(mu_suite + a_user + b_inj)) with a_user ~ N(0, sd_user^2) and b_inj ~ N(0, sd_inj^2) was fitted with statsmodels `BinomialBayesMixedGLM.fit_vb`. Fitted SDs (logit scale) range from 2.7 to 6.0 for users on utility and from 0.3 to 3.6 for injections across both metrics. Each of the 2000 replicates redraws user and injection effects and outcomes on AgentDojo's exact design (same users, injections and suites), and scores whether each 95% interval contains the super-population mean (sum over suites of n_s/n E[expit(mu_s + a + b)], by Gauss-Hermite). Pigeonhole uses B = 500 per replicate. Monte Carlo SE of a coverage near 0.95 is about 0.005.

| method | mean cov. utility | min | max | mean cov. attack success | min | max | median SE / true SD, utility | attack success |
|---|---|---|---|---|---|---|---|---|
| naive | 0.613 | 0.486 | 0.694 | 0.659 | 0.400 | 0.908 | 0.46 | 0.48 |
| one-way user | 0.929 | 0.860 | 0.948 | 0.759 | 0.356 | 0.914 | 0.96 | 0.64 |
| one-way injection | 0.519 | 0.300 | 0.788 | 0.848 | 0.708 | 0.926 | 0.32 | 0.79 |
| two-way CGM (strata) | 0.935 | 0.924 | 0.946 | 0.913 | 0.876 | 0.935 | 0.92 | 0.90 |
| pigeonhole (strata) | 0.952 | 0.938 | 0.962 | 0.949 | 0.915 | 0.978 | 1.04 | 1.05 |
| two-way CGM, pooled | 0.966 | 0.946 | 0.995 | 0.967 | 0.918 | 1.000 | 1.06 | 1.26 |

Naive intervals are about half as wide as they should be. Each one-way interval works only when its key happens to dominate, and which key dominates differs by metric and by pipeline. Stratified two-way CGM under-covers by up to 7 points (worst 87.6%) because its SE runs about 8 to 10% low. Our reading, not tested separately, is that the subtracted intersection term carries the user-level variance in this fully crossed design and pulls the estimate down; consistent with that, for the same 21 of 28 utility pipelines the stratified one-way injection SE is below naive and the two-way SE is below the user SE. The stratified pigeonhole bootstrap is the only method near nominal in every scenario. Pooled CGM is conservative, reaching 99.5% and 100% for some pipelines.

## Positioning

The estimators are not new. Two-way clustering is Cameron, Gelbach and Miller (2011, JBES 29(2) 238-249); the crossed bootstrap is Owen (2007, AoAS 1(2)). Miller (2024, arXiv 2411.00640) brought one-way clustered SEs to LLM evals. Bowyer, Aitchison and Ivanova (2025, arXiv 2503.01747) showed that clustered CLT intervals can miss nominal coverage, but only on a synthetic Beta-Bernoulli model. Akimitsu (2026, arXiv 2607.23424) already uses two-way clustering by task and by model in an LLM evaluation. inspect_evals issue #2605 surveyed one-way ratios and proposed one key per metric. What this note adds: the crossing inside a prompt-injection benchmark (user task x injection task within suite) measured on all 28 public AgentDojo pipelines; a check of the one-key rule against both one-way SEs; a count of model comparisons that change; and coverage measured on the benchmark's actual crossed design with effects fitted to its data.

## Resolved: leaderboard vs runs means

The AgentDojo results table (`docs/results-table.html`) is generated by `util_scripts/create_results_table.py`, whose default `benchmark_version` is `v1.1.2`. It therefore averages only the v1.1.2 cells (629) even for pipelines run on v1.2 (949). On those 629 cells the runs reproduce all 24 leaderboard rows to four decimals (`scripts/check_leaderboard.py`, `results/leaderboard_check.csv`). For claude-3-7-sonnet that gives 77.27% utility and 7.31% attack success on 629 cells, against 82.09% and 4.95% on all 949. The two Meta-SecAlign pipelines and both Llama-3.3 pipelines are not on the leaderboard.

## Limitations

- Upstream runner, not inspect_evals. The 949 v1.2 cells here differ from inspect_evals' 1014 samples (eval version "2-A"), and the inspect port may behave differently. These numbers describe the upstream released runs; the 949 vs 1014 gap is not reconciled.
- Within-version only. The 629-cell and 949-cell sets were not compared with each other, because task definitions may have changed between versions for the same ids.
- The coverage result depends on the generating model: additive logit effects, SDs shared across suites, no user x injection interaction (with one replicate per cell that interaction cannot be separated from Bernoulli noise). Variational Bayes underestimated SDs by about 6 to 14% on synthetic checks (3 settings x 8 seeds on a 25 x 9 x 4 design; for example 1.33 for a true 1.5), and observed two-way SEs are a median 1.04x the simulated ones. The simulated clustering is therefore slightly weaker than the real one, which would make the shortfall of naive and one-way intervals an understatement rather than an overstatement.
- Coverage was measured for single-pipeline means, not for paired differences. The pairwise counts use two-way intervals, which under-cover slightly, so they are a lower bound on the comparisons that do not survive.
- Suites are fixed, so the intervals are conditional on these four suites. A suite-random analysis would need far more than four suites.
- 91 cells in five pipelines carry a runner error. They keep the outcome the runner recorded, as the leaderboard does. One cell of Llama-3.3-70B-Instruct-repeat_user_prompt has no outcome and is dropped (797 of 798 files).
- Small-sample choices: G/(G-1) only, no (n-1)/(n-K) factor; t(G-1) degrees of freedom; pigeonhole intervals use bootstrap SE with z, not percentiles. B is 4000 for the table, 2000 for pairs and 500 in the simulation.

## Reproduce

```
uv sync
git clone --filter=blob:none --no-checkout https://github.com/ethz-spylab/agentdojo.git data/upstream
git -C data/upstream sparse-checkout set --no-cone '/runs/*/*/*/important_instructions/*.json'
git -C data/upstream checkout 089ed468cf3ed0322acc66b0211f26d9d90dbf60
uv run pytest -q
uv run python scripts/run_analysis.py      # results/se_table.csv, pairwise.csv, summary.json
uv run python scripts/run_coverage.py      # results/coverage.csv (under 2 minutes here, multi-process)
uv run python scripts/check_leaderboard.py # results/leaderboard_check.csv
uv run python scripts/make_tables.py       # results/tables.md
```

## Per-pipeline table (suites as fixed strata)

Ratios are SE / naive SE; n is the number of cells. The pooled table is in `results/tables.md`.

| pipeline | metric | n | mean | naive SE | user | inj | two-way | two-way SE | pigeonhole |
|---|---|---|---|---|---|---|---|---|---|
| Meta-SecAlign-70B | utility | 949 | 0.780 | 0.0135 | 2.72x | 0.48x | 2.58x | 0.0348 | 2.77x |
| Meta-SecAlign-70B | attack_success | 949 | 0.022 | 0.0048 | 2.35x | 0.52x | 2.21x | 0.0105 | 2.46x |
| Meta-SecAlign-70B-repeat_user_prompt | utility | 949 | 0.801 | 0.0130 | 2.72x | 0.33x | 2.56x | 0.0332 | 2.74x |
| Meta-SecAlign-70B-repeat_user_prompt | attack_success | 949 | 0.021 | 0.0047 | 2.31x | 0.62x | 2.18x | 0.0102 | 2.42x |
| claude-3-5-sonnet-20240620 | utility | 629 | 0.512 | 0.0199 | 1.95x | 2.27x | 2.82x | 0.0563 | 3.03x |
| claude-3-5-sonnet-20240620 | attack_success | 629 | 0.339 | 0.0189 | 1.03x | 3.22x | 3.25x | 0.0614 | 3.34x |
| claude-3-5-sonnet-20241022 | utility | 629 | 0.725 | 0.0178 | 2.36x | 0.33x | 2.18x | 0.0388 | 2.36x |
| claude-3-5-sonnet-20241022 | attack_success | 629 | 0.011 | 0.0042 | 1.06x | 1.27x | 1.33x | 0.0055 | 1.78x |
| claude-3-7-sonnet-20250219 | utility | 949 | 0.821 | 0.0125 | 2.59x | 0.69x | 2.49x | 0.0311 | 2.65x |
| claude-3-7-sonnet-20250219 | attack_success | 949 | 0.050 | 0.0070 | 1.23x | 2.02x | 2.17x | 0.0153 | 2.46x |
| claude-3-haiku-20240307 | utility | 629 | 0.334 | 0.0188 | 2.28x | 0.47x | 2.10x | 0.0396 | 2.36x |
| claude-3-haiku-20240307 | attack_success | 629 | 0.091 | 0.0115 | 1.25x | 1.69x | 1.88x | 0.0215 | 2.19x |
| claude-3-opus-20240229 | utility | 629 | 0.525 | 0.0199 | 2.15x | 0.65x | 2.01x | 0.0400 | 2.30x |
| claude-3-opus-20240229 | attack_success | 629 | 0.113 | 0.0126 | 1.06x | 1.87x | 1.94x | 0.0245 | 2.21x |
| claude-3-sonnet-20240229 | utility | 629 | 0.332 | 0.0188 | 1.99x | 1.15x | 2.07x | 0.0389 | 2.33x |
| claude-3-sonnet-20240229 | attack_success | 629 | 0.267 | 0.0177 | 1.44x | 1.92x | 2.20x | 0.0389 | 2.43x |
| command-r | utility | 629 | 0.308 | 0.0184 | 2.17x | 0.62x | 2.03x | 0.0373 | 2.29x |
| command-r | attack_success | 629 | 0.033 | 0.0072 | 1.47x | 0.87x | 1.41x | 0.0101 | 1.87x |
| command-r-plus | utility | 629 | 0.251 | 0.0173 | 2.13x | 0.51x | 1.97x | 0.0342 | 2.27x |
| command-r-plus | attack_success | 629 | 0.045 | 0.0082 | 1.99x | 0.61x | 1.83x | 0.0151 | 2.12x |
| gemini-1.5-flash-001 | utility | 629 | 0.342 | 0.0189 | 2.28x | 0.36x | 2.10x | 0.0398 | 2.35x |
| gemini-1.5-flash-001 | attack_success | 629 | 0.122 | 0.0131 | 1.31x | 1.57x | 1.81x | 0.0237 | 2.14x |
| gemini-1.5-flash-002 | utility | 629 | 0.324 | 0.0187 | 2.40x | 0.42x | 2.23x | 0.0416 | 2.43x |
| gemini-1.5-flash-002 | attack_success | 629 | 0.035 | 0.0073 | 1.01x | 2.11x | 2.13x | 0.0156 | 2.38x |
| gemini-1.5-pro-001 | utility | 629 | 0.289 | 0.0181 | 2.06x | 0.53x | 1.89x | 0.0342 | 2.20x |
| gemini-1.5-pro-001 | attack_success | 629 | 0.286 | 0.0180 | 1.38x | 1.39x | 1.75x | 0.0315 | 2.06x |
| gemini-1.5-pro-002 | utility | 629 | 0.471 | 0.0199 | 2.21x | 0.62x | 2.08x | 0.0415 | 2.33x |
| gemini-1.5-pro-002 | attack_success | 629 | 0.170 | 0.0150 | 1.39x | 1.14x | 1.55x | 0.0233 | 1.89x |
| gemini-2.0-flash-001 | utility | 949 | 0.393 | 0.0159 | 3.00x | 0.53x | 2.89x | 0.0459 | 3.10x |
| gemini-2.0-flash-001 | attack_success | 949 | 0.141 | 0.0113 | 1.60x | 0.92x | 1.65x | 0.0187 | 1.92x |
| gemini-2.0-flash-exp | utility | 629 | 0.399 | 0.0195 | 2.32x | 0.51x | 2.16x | 0.0422 | 2.38x |
| gemini-2.0-flash-exp | attack_success | 629 | 0.170 | 0.0150 | 1.59x | 1.07x | 1.68x | 0.0252 | 2.06x |
| gpt-3.5-turbo-0125 | utility | 629 | 0.347 | 0.0190 | 2.31x | 0.57x | 2.17x | 0.0411 | 2.44x |
| gpt-3.5-turbo-0125 | attack_success | 629 | 0.103 | 0.0121 | 1.49x | 1.78x | 2.12x | 0.0257 | 2.37x |
| gpt-4-0125-preview | utility | 629 | 0.407 | 0.0196 | 1.63x | 1.72x | 2.19x | 0.0430 | 2.41x |
| gpt-4-0125-preview | attack_success | 629 | 0.563 | 0.0198 | 0.78x | 3.48x | 3.45x | 0.0683 | 3.55x |
| gpt-4-turbo-2024-04-09 | utility | 629 | 0.541 | 0.0199 | 2.05x | 1.02x | 2.06x | 0.0411 | 2.33x |
| gpt-4-turbo-2024-04-09 | attack_success | 629 | 0.286 | 0.0180 | 1.20x | 1.79x | 1.99x | 0.0359 | 2.21x |
| gpt-4o-2024-05-13 | utility | 629 | 0.501 | 0.0200 | 1.80x | 1.43x | 2.11x | 0.0420 | 2.34x |
| gpt-4o-2024-05-13 | attack_success | 629 | 0.477 | 0.0199 | 1.28x | 2.17x | 2.37x | 0.0473 | 2.54x |
| gpt-4o-2024-05-13-repeat_user_prompt | utility | 629 | 0.672 | 0.0187 | 2.10x | 1.18x | 2.19x | 0.0411 | 2.45x |
| gpt-4o-2024-05-13-repeat_user_prompt | attack_success | 629 | 0.278 | 0.0179 | 1.16x | 2.19x | 2.31x | 0.0414 | 2.54x |
| gpt-4o-2024-05-13-spotlighting_with_delimiting | utility | 629 | 0.556 | 0.0198 | 1.74x | 1.68x | 2.24x | 0.0445 | 2.48x |
| gpt-4o-2024-05-13-spotlighting_with_delimiting | attack_success | 629 | 0.417 | 0.0197 | 1.06x | 2.60x | 2.67x | 0.0525 | 2.83x |
| gpt-4o-2024-05-13-tool_filter | utility | 629 | 0.563 | 0.0198 | 2.06x | 0.60x | 1.90x | 0.0377 | 2.24x |
| gpt-4o-2024-05-13-tool_filter | attack_success | 629 | 0.068 | 0.0101 | 1.14x | 1.77x | 1.85x | 0.0186 | 2.22x |
| gpt-4o-2024-05-13-transformers_pi_detector | utility | 629 | 0.211 | 0.0163 | 2.27x | 0.93x | 2.25x | 0.0366 | 2.49x |
| gpt-4o-2024-05-13-transformers_pi_detector | attack_success | 629 | 0.079 | 0.0108 | 1.23x | 2.86x | 2.96x | 0.0320 | 3.14x |
| gpt-4o-mini-2024-07-18 | utility | 629 | 0.499 | 0.0200 | 2.19x | 0.78x | 2.11x | 0.0421 | 2.34x |
| gpt-4o-mini-2024-07-18 | attack_success | 629 | 0.272 | 0.0178 | 1.72x | 1.60x | 2.15x | 0.0382 | 2.41x |
| meta-llama_Llama-3-70b-chat-hf | utility | 629 | 0.183 | 0.0154 | 2.16x | 0.93x | 2.14x | 0.0331 | 2.39x |
| meta-llama_Llama-3-70b-chat-hf | attack_success | 629 | 0.256 | 0.0174 | 1.43x | 2.26x | 2.50x | 0.0435 | 2.73x |
| meta-llama_Llama-3.3-70B-Instruct | utility | 949 | 0.414 | 0.0160 | 2.81x | 0.72x | 2.73x | 0.0437 | 2.92x |
| meta-llama_Llama-3.3-70B-Instruct | attack_success | 949 | 0.231 | 0.0137 | 1.55x | 1.49x | 1.97x | 0.0269 | 2.23x |
| meta-llama_Llama-3.3-70B-Instruct-repeat_user_prompt | utility | 797 | 0.395 | 0.0173 | 2.88x | 0.92x | 2.86x | 0.0495 | 3.01x |
| meta-llama_Llama-3.3-70B-Instruct-repeat_user_prompt | attack_success | 797 | 0.090 | 0.0102 | 1.75x | 1.54x | 2.13x | 0.0216 | 2.37x |

| metric | two-way ratio min | median | max | pigeonhole/two-way min | pigeonhole/two-way max | rule picks smaller one-way | two-way < larger one-way | CGM fallback used |
|---|---|---|---|---|---|---|---|---|
| attack_success | 1.33 | 2.12 | 3.45 | 1.03 | 1.35 | 10 | 5 | 0 |
| utility | 1.89 | 2.16 | 2.89 | 1.05 | 1.18 | 2 | 21 | 0 |

One-key rule understates (picks the smaller one-way SE):

- utility: claude-3-5-sonnet-20240620, gpt-4-0125-preview
- attack_success: Meta-SecAlign-70B, Meta-SecAlign-70B-repeat_user_prompt, command-r, command-r-plus, gemini-1.5-pro-002, gemini-2.0-flash-001, gemini-2.0-flash-exp, gpt-4o-mini-2024-07-18, meta-llama_Llama-3.3-70B-Instruct, meta-llama_Llama-3.3-70B-Instruct-repeat_user_prompt

