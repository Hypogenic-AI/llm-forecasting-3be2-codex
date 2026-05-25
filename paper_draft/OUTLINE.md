# Outline: LLMs and Crowd Forecasting

## Title
- Emphasize the matched within-dataset comparison.
- Signal the mixed result: long-horizon gains, short-horizon dependence on history.

## Abstract
- State the practical question: when can an LLM beat a human crowd?
- Describe matched binary-question timepoints from one dataset.
- Summarize the two regimes and two prompt conditions.
- Report the main Brier results and the non-significant paired tests.
- State the scoped conclusion.

## Introduction
- Hook: deployment decisions depend on where LLMs help.
- Gap: prior work mixes event forecasting with time-series forecasting and often lacks matched human comparisons.
- Approach: one dataset, matched cutoff-based regimes, same model, paired crowd baseline.
- Quantitative preview: `-0.050` Brier in long-term question-only; `+0.066` short-term question-only; `-0.010` with history.
- Contributions:
  - controlled within-dataset regime comparison
  - prompt ablation separating independent reasoning from history-conditioned synthesis
  - transparent statistical analysis and failure-case interpretation

## Related Work
- Human-comparison event forecasting: Halawi et al.; Schoenegger and Park; Paleka et al.
- Time-series LLM forecasting: Gruver et al.; Jin et al.; Liu et al.; Guo et al.
- Skeptical ablations and positioning: Tan et al.; explain why this paper stays in binary question forecasting.

## Methodology
- Dataset and regime construction from local forecasting-platform test split.
- Definitions for long-term/short-term regimes.
- Sampling procedure and overlap control.
- Prompt conditions and deterministic API setup.
- Baselines, metrics, and statistics.

## Results
- Table 1: main metrics by regime and prompt.
- Table 2: paired tests and confidence intervals.
- Figure 1: Brier by regime.
- Figure 2: LLM minus crowd Brier.
- Figure 3: calibration for history condition.
- Text interpretation and ablation findings.

## Discussion
- Interpret mechanism difference across regimes.
- Discuss representative failure modes from the report.
- State limitations precisely.
- Broader implication: LLMs are complementary and information-regime dependent.

## Conclusion
- Restate main answer to the hypothesis.
- Summarize contribution and strongest result.
- Note next steps: retrieval, more samples, more models, stricter ablations.

