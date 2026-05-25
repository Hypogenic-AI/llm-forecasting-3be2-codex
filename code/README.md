# Cloned Repositories

## 1. llm_forecasting
- URL: https://github.com/dannyallover/llm_forecasting
- Location: `code/llm_forecasting/`
- Purpose: Official code for `Approaching Human-Level Forecasting with Language Models`
- Key files:
  - `README.md`
  - `pyproject.toml`
  - `scripts/data_scraping/`
  - `scripts/fine_tune/fine_tune.py`
  - `scripts/training_data/training_point_generation.py`
- Notes:
  - Implements the full retrieval -> relevancy filtering -> summarization -> reasoning -> aggregation pipeline.
  - Directly compatible with the `YuehHanChen/forecasting` dataset already downloaded locally.
  - Uses historical-news retrieval and multiple prompted forecasts aggregated into a final probability.

## 2. Time-LLM
- URL: https://github.com/KimMeen/Time-LLM
- Location: `code/Time-LLM/`
- Purpose: Official implementation of `Time-LLM: Time Series Forecasting by Reprogramming Large Language Models`
- Key files:
  - `README.md`
  - `requirements.txt`
  - `run_main.py`
  - `run_m4.py`
  - `scripts/TimeLLM_ETTh1.sh`
  - `scripts/TimeLLM_M4.sh`
- Notes:
  - Requires heavier GPU-oriented dependencies and preprocessed datasets placed under `dataset/`.
  - Best candidate for reproducing long-horizon and few-shot LLM time-series claims from the literature.

## 3. llmtime
- URL: https://github.com/ngruver/llmtime
- Location: `code/llmtime/`
- Purpose: Official implementation of `Large Language Models Are Zero Shot Time Series Forecasters`
- Key files:
  - `README.md`
  - `install.sh`
  - `demo.ipynb`
  - `experiments/run_darts.py`
  - `experiments/run_monash.py`
- Notes:
  - Focuses on numeric-to-text encoding and sampling extrapolations from general LLMs.
  - Useful zero-shot baseline when comparing repurposed text LLMs against time-series-native models.
  - Repo is the largest clone in the workspace and expects either API-backed LLMs or a stronger local environment.

## 4. forecasting-tools
- URL: https://github.com/Metaculus/forecasting-tools
- Location: `code/forecasting-tools/`
- Purpose: Production-oriented toolkit for building and benchmarking forecasting bots on Metaculus-style questions
- Key files:
  - `README.md`
  - `pyproject.toml`
  - `forecasting_tools/forecast_bots/template_bot.py`
  - `forecasting_tools/forecast_bots/main_bot.py`
  - `scripts/run_benchmarker.py`
- Notes:
  - Most useful operational codebase for current forecasting-bot workflows.
  - Includes question abstractions, tournament runners, bot templates, aggregation utilities, and reporting.
  - Strong candidate for adapting the question-forecasting experiments in this project.

## 5. LLMsForTimeSeries
- URL: https://github.com/BennyTMT/LLMsForTimeSeries
- Location: `code/LLMsForTimeSeries/`
- Purpose: Official code for `Are Language Models Actually Useful for Time Series Forecasting?`
- Key files:
  - `README.md`
  - `PAttn/`
  - `CALF/`
  - `OFA/`
  - `Time-LLM-exp/`
- Notes:
  - Valuable because it bundles the paper’s ablations and the simple `PAttn` baseline.
  - Best repo here for stress-testing whether LLM components genuinely help on ETT, Weather, Traffic, Electricity, and related benchmarks.

## Recommendation
- For question/event forecasting: start from `code/llm_forecasting/` or `code/forecasting-tools/`.
- For LLM time-series reproduction: start from `code/Time-LLM/`.
- For skeptical ablations and cheaper baselines: start from `code/LLMsForTimeSeries/`.
- For zero-shot text-LM forecasting of numeric series: start from `code/llmtime/`.
