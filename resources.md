# Resources Catalog

## Summary

This document catalogs all resources gathered for the research project on LLMs and forecasting. The collected assets cover:
- question/event forecasting with human crowd comparisons
- LLM-based time-series forecasting
- skeptical ablation baselines for time-series forecasting

## Papers

Total papers downloaded: 8

| Title | Authors | Year | File | Key Info |
|------|------|------|------|------|
| Approaching Human-Level Forecasting with Language Models | Halawi et al. | 2024 | `papers/2024_halawi_approaching_human_level_forecasting.pdf` | Best direct LM-vs-crowd event-forecasting paper |
| Large Language Model Prediction Capabilities: Evidence from a Real-World Forecasting Tournament | Schoenegger, Park | 2023 | `papers/2023_schoenegger_real_world_forecasting_tournament.pdf` | Negative GPT-4 vs human result |
| Consistency Checks for Language Model Forecasters | Paleka et al. | 2024 | `papers/2024_paleka_consistency_checks_forecasters.pdf` | Evaluation method for unresolved questions |
| Large Language Models Are Zero-Shot Time Series Forecasters | Gruver et al. | 2023 | `papers/2023_gruver_zero_shot_time_series_forecasters.pdf` | Seminal zero-shot TS paper |
| Time-LLM: Time Series Forecasting by Reprogramming Large Language Models | Jin et al. | 2023 | `papers/2023_jin_time_llm.pdf` | Major TS-LLM method |
| Are Language Models Actually Useful for Time Series Forecasting? | Tan et al. | 2024 | `papers/2024_tan_are_lms_useful_for_time_series.pdf` | Strong ablation challenge |
| Timer: Generative Pre-trained Transformers Are Large Time Series Models | Liu et al. | 2024 | `papers/2024_liu_timer_large_time_series_models.pdf` | Purpose-built TS foundation model comparator |
| T-LLM: Teaching Large Language Models to Forecast Time Series via Temporal Distillation | Guo et al. | 2026 | `papers/2026_guo_t_llm_temporal_distillation.pdf` | Recent TS-LLM improvement |

See `papers/README.md` for more detail.

## Datasets

Total datasets downloaded: 4

| Name | Source | Size | Task | Location | Notes |
|------|------|------|------|------|------|
| FOReCAst | Hugging Face | ~268 KB | binary question forecasting | `datasets/forecast_questions_forecast/` | Light, easy-to-run question benchmark |
| Forecasting Platform Dataset | Hugging Face | ~11 MB | crowd forecasting with trajectories | `datasets/forecast_questions_platforms/` | Best local question dataset for LM-vs-human experiments |
| ETTh1 | Hugging Face / Time-Series-Library | ~676 KB | multivariate TS forecasting | `datasets/timeseries_etth1/` | Standard benchmark used in Time-LLM papers |
| M4 Hourly | Hugging Face / Time-Series-Library | ~1.6 MB | short-term TS forecasting | `datasets/timeseries_m4_hourly/` | Canonical short-horizon benchmark |

See `datasets/README.md` for loading and download instructions.

## Code Repositories

Total repositories cloned: 5

| Name | URL | Purpose | Location | Notes |
|------|------|------|------|------|
| llm_forecasting | https://github.com/dannyallover/llm_forecasting | Retrieval-augmented event forecasting | `code/llm_forecasting/` | Official Halawi et al. code |
| Time-LLM | https://github.com/KimMeen/Time-LLM | Reprogrammed LLM time-series forecasting | `code/Time-LLM/` | Official ICLR 2024 repo |
| llmtime | https://github.com/ngruver/llmtime | Zero-shot TS forecasting through text serialization | `code/llmtime/` | Official NeurIPS 2023 repo |
| forecasting-tools | https://github.com/Metaculus/forecasting-tools | Operational forecasting bots and API tooling | `code/forecasting-tools/` | Best platform/tooling repo |
| LLMsForTimeSeries | https://github.com/BennyTMT/LLMsForTimeSeries | Ablations and PAttn baseline | `code/LLMsForTimeSeries/` | Best skeptical baseline repo |

See `code/README.md` for more detail.

## Resource Gathering Notes

### Search Strategy

I split the topic into two branches:
- **Question/event forecasting**: human crowd vs LLM systems on Metaculus-like questions.
- **Numeric time-series forecasting**: high-data benchmarks such as ETT and M4.

This was necessary because the hypothesis mixes two forecasting regimes that the literature usually studies separately.

### Selection Criteria

- Direct relevance to the hypothesis.
- Availability of code or datasets.
- Strong positive papers plus strong counter-evidence papers.
- Datasets small enough to keep locally in this workspace without special infrastructure.

### Challenges Encountered

- The paper-finder workflow was slower than ideal, so manual arXiv/Hugging Face/GitHub follow-up was used.
- Some older Hugging Face dataset entries use deprecated dataset scripts and cannot be loaded cleanly with the current `datasets` version.
- Several TS repos assume Conda, GPUs, or external data bundles; they were cloned and documented rather than executed end-to-end.

### Gaps and Workarounds

- No local dataset here provides a clean human baseline for numeric high-data time-series forecasting.
  Workaround: keep the high-data arm as a benchmark-comparison study unless a human baseline is added later.

- GIFT-Eval was not downloaded locally.
  Workaround: documented as a recommended next benchmark once the experiment runner chooses a larger TS evaluation pass.

## Recommendations for Experiment Design

1. **Primary dataset(s)**:
   - Use `datasets/forecast_questions_platforms/` for long-term low-data forecasting.
   - Use `datasets/timeseries_m4_hourly/` and `datasets/timeseries_etth1/` for short-term high-data forecasting.

2. **Baseline methods**:
   - Human crowd aggregate for question forecasting.
   - DLinear or PAttn for time-series baselines.
   - LLMTime and Time-LLM as LLM-based comparators.

3. **Evaluation metrics**:
   - Brier score, calibration, and accuracy for question forecasting.
   - MAE/MSE for ETT.
   - SMAPE/MASE/OWA for M4 Hourly.

4. **Code to adapt/reuse**:
   - `code/llm_forecasting/` for the event-forecasting pipeline.
   - `code/forecasting-tools/` for Metaculus-style bot infrastructure.
   - `code/LLMsForTimeSeries/` for ablations and cheap baselines.
   - `code/Time-LLM/` and `code/llmtime/` for LLM-based TS baselines.
