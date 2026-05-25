# Research Plan: LLMs and Forecasting

## Motivation & Novelty Assessment

### Why This Research Matters
Forecasting quality matters in policy, markets, and operations, and the most important practical question is not whether LLMs can generate plausible forecasts, but when they are actually better than people. A clean comparison between LLMs and human crowd forecasts can clarify whether LLMs are most useful as early-stage forecasters under uncertainty, late-stage synthesizers of abundant evidence, or neither.

### Gap in Existing Work
The literature review shows two disconnected lines of work: event/question forecasting with direct human comparisons, and numeric time-series forecasting without human baselines. Existing evidence does not directly test the user hypothesis as a single within-dataset comparison across information regimes, and the strongest positive and negative papers disagree on where LLM advantages should appear.

### Our Novel Contribution
This study tests the hypothesis within one local human-comparable dataset by converting each forecasting question into matched question-timepoints. Instead of mixing unrelated datasets, it compares a real LLM against the contemporaneous human crowd at two regimes: `short-term high-data` and `long-term low-data`, both defined from the same platform trajectories.

### Experiment Justification
- Experiment 1: Evaluate `long-term low-data` question-timepoints to test whether the LLM beats the crowd when there is sparse historical signal and long horizon uncertainty.
- Experiment 2: Evaluate `short-term high-data` question-timepoints to test whether the LLM beats the crowd when many prior updates exist and the question is near resolution.
- Experiment 3: Run prompt variants with and without explicit crowd-trajectory summaries to distinguish reasoning from simple crowd imitation.
- Experiment 4: Compare both systems to a `0.5` no-information baseline to ensure improvements are meaningful.

## Research Question
Do real LLM forecasts outperform contemporaneous human crowd forecasts on binary forecasting questions in two regimes: `short-term high-data` and `long-term low-data`?

## Background and Motivation
Prior work shows retrieval-augmented LLM systems can approach human crowd performance on event forecasting, while early direct GPT-4 comparisons underperformed humans. The literature also shows that "LLM forecasting" claims depend heavily on task definition. To avoid conflating numeric time-series benchmarking with judgmental forecasting, this project focuses on the locally available forecasting-platform dataset, where both resolved outcomes and human crowd trajectories are available.

## Hypothesis Decomposition
- H1: In `long-term low-data` settings, the LLM has lower Brier score than the human crowd.
- H2: In `short-term high-data` settings, the LLM has lower Brier score than the human crowd.
- H3: Access to structured historical crowd trajectory helps more in `short-term high-data` than in `long-term low-data`.
- Alternative explanation A: Any apparent LLM gains come from copying the crowd trajectory rather than independent synthesis.
- Alternative explanation B: Regime effects are driven by platform/domain mix rather than information regime.

Independent variables:
- Forecaster: `LLM`, `human_crowd`, `0.5_baseline`
- Regime: `long_term_low_data`, `short_term_high_data`
- Prompt condition: `question_only`, `question_plus_history`

Dependent variables:
- Primary: Brier score
- Secondary: log loss, accuracy, calibration by bucket, absolute error from outcome

## Proposed Methodology

### Approach
Use the local `datasets/forecast_questions_platforms/` test split and create matched evaluation items from resolved binary questions. For each question, select a forecast timestamp meeting either regime definition. At that timestamp, compare:
1. the contemporaneous crowd probability,
2. the LLM probability elicited from a real OpenAI model,
3. a `0.5` baseline.

The LLM will be prompted with question text, resolution criteria, background, source, and optionally a compact summary of crowd-trajectory history available before the cutoff. This keeps the evaluation reproducible and avoids needing fresh web retrieval.

### Experimental Steps
1. Load and validate the local forecasting-platform dataset and parse community trajectories.
2. Construct matched timepoints:
   - `long_term_low_data`: at least 60 days to resolution and at most 5 crowd predictions observed.
   - `short_term_high_data`: at most 14 days to resolution and at least 30 crowd predictions observed.
3. Sample balanced subsets from both regimes for affordable API evaluation.
4. Call a real OpenAI model with deterministic settings and parse probabilities from JSON outputs.
5. Score LLM, crowd, and `0.5` baseline on the same outcomes.
6. Run paired statistical tests and effect-size calculations by regime.
7. Perform error analysis, calibration analysis, and prompt-ablation comparison.

### Baselines
- Human crowd aggregate at the matched cutoff.
- `0.5` uninformed baseline.
- Prompt ablation:
  - `question_only`
  - `question_plus_history`

### Evaluation Metrics
- Brier score: primary metric for binary forecasting.
- Log loss: penalizes overconfident mistakes.
- Accuracy at 0.5 threshold: easy interpretability.
- Calibration curves / expected calibration error: to inspect confidence quality.

### Statistical Analysis Plan
- Use paired bootstrap confidence intervals for mean Brier differences.
- Use Wilcoxon signed-rank tests on paired per-item losses because binary-question loss distributions are non-normal.
- Report effect sizes as mean paired difference and rank-biserial style direction summaries.
- Significance level: `alpha = 0.05`.
- Treat each sampled question-timepoint as the unit of analysis and disclose any repeated-question overlap across regimes.

## Expected Outcomes
Support for the user hypothesis would require:
- lower LLM Brier than crowd in `long_term_low_data`, and
- lower LLM Brier than crowd in `short_term_high_data`.

Refutation occurs if the LLM loses in either regime, or if gains vanish under the ablation and appear to be simple crowd-following.

## Timeline and Milestones
1. Planning and data profiling.
2. Environment verification and dependency setup.
3. Implementation of dataset parser, prompt builder, and API runner.
4. Experiment execution on both regimes and prompt conditions.
5. Statistical analysis, figures, and report writing.

## Potential Challenges
- API variability or parsing failures.
  Mitigation: deterministic temperature, JSON-only outputs, retry logic, raw-response logging.
- Regime sample imbalance.
  Mitigation: balanced sampling with explicit filters and documented exclusions.
- Validity concern that crowd history leaks human signal into the LLM.
  Mitigation: include `question_only` ablation and frame `question_plus_history` as an upper-bound synthesis condition.
- Limited external context because no live retrieval is used.
  Mitigation: keep claims scoped to dataset-conditioned forecasting rather than open-web forecasting.

## Success Criteria
- A complete runnable pipeline under the local `.venv`.
- Real-model forecasts stored in `results/model_outputs/`.
- Statistical comparison of LLM vs crowd in both regimes.
- `REPORT.md` with actual results, figures, limitations, and a clear answer to the hypothesis.
