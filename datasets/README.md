# Downloaded Datasets

This directory contains locally downloaded datasets for the forecasting project. The data is present on disk for immediate use, but should remain excluded from git.

## Dataset 1: FOReCAst

### Overview
- Source: `MoyYuan/FOReCAst`
- Local path: `datasets/forecast_questions_forecast/`
- Approx. local size: 268 KB
- Task: binary question forecasting
- Splits: train 1,394, validation 206, test 529
- Format: Hugging Face DatasetDict saved with `save_to_disk`
- Why relevant: compact binary forecasting benchmark with resolved questions and normalized confidence scores

### Download Instructions

Using Hugging Face:

```python
from datasets import load_dataset

dataset = load_dataset("MoyYuan/FOReCAst")
dataset.save_to_disk("datasets/forecast_questions_forecast")
```

### Loading the Dataset

```python
from datasets import load_from_disk

dataset = load_from_disk("datasets/forecast_questions_forecast")
print(dataset["train"][0])
```

### Sample Data
- Saved at `datasets/forecast_questions_forecast/samples/samples.json`

### Notes
- Best fit for rapid experiments on question-level probability prediction.
- Lighter than the platform-scale dataset below, so useful for first-pass pipeline debugging.

## Dataset 2: Forecasting Platform Dataset

### Overview
- Source: `YuehHanChen/forecasting`
- Local path: `datasets/forecast_questions_platforms/`
- Approx. local size: 11 MB
- Task: forecasting on real platform questions with temporal community trajectories
- Splits: train 3,762, validation 840, test 914
- Format: Hugging Face DatasetDict saved with `save_to_disk`
- Why relevant: directly aligned with Halawi et al. 2024 and includes platform, background, resolution criteria, and crowd prediction history

### Download Instructions

```python
from datasets import load_dataset

dataset = load_dataset("YuehHanChen/forecasting")
dataset.save_to_disk("datasets/forecast_questions_platforms")
```

### Loading the Dataset

```python
from datasets import load_from_disk

dataset = load_from_disk("datasets/forecast_questions_platforms")
print(dataset["train"][0]["question"])
```

### Sample Data
- Saved at `datasets/forecast_questions_platforms/samples/samples.json`

### Notes
- Strongest local dataset for comparing LM forecasts to human/community aggregates.
- Contains community prediction trajectories that support dynamic or early-vs-late forecast analyses.

## Dataset 3: ETTh1

### Overview
- Source: `thuml/Time-Series-Library`, config `ETTh1`
- Local path: `datasets/timeseries_etth1/`
- Approx. local size: 676 KB
- Task: multivariate long-horizon time-series forecasting
- Splits: train 17,420 rows
- Format: Hugging Face DatasetDict saved with `save_to_disk`
- Why relevant: standard benchmark used by Time-LLM and multiple LLM-for-time-series papers

### Download Instructions

```python
from datasets import load_dataset

dataset = load_dataset("thuml/Time-Series-Library", "ETTh1")
dataset.save_to_disk("datasets/timeseries_etth1")
```

### Loading the Dataset

```python
from datasets import load_from_disk

dataset = load_from_disk("datasets/timeseries_etth1")
print(dataset["train"][0])
```

### Sample Data
- Saved at `datasets/timeseries_etth1/samples/samples.json`

### Notes
- Good fit for reproducing Time-LLM-style long-term forecasting claims.
- No human baseline is included; use it for the high-data time-series side only.

## Dataset 4: M4 Hourly

### Overview
- Source: `thuml/Time-Series-Library`, config `m4-hourly`
- Local path: `datasets/timeseries_m4_hourly/`
- Approx. local size: 1.6 MB
- Task: short-term univariate time-series forecasting
- Splits: train 414, test 414
- Format: Hugging Face DatasetDict saved with `save_to_disk`
- Why relevant: canonical forecasting competition data, heavily used for zero-shot and few-shot time-series evaluation

### Download Instructions

```python
from datasets import load_dataset

dataset = load_dataset("thuml/Time-Series-Library", "m4-hourly")
dataset.save_to_disk("datasets/timeseries_m4_hourly")
```

### Loading the Dataset

```python
from datasets import load_from_disk

dataset = load_from_disk("datasets/timeseries_m4_hourly")
print(dataset["train"][0]["V1"])
```

### Sample Data
- Saved at `datasets/timeseries_m4_hourly/samples/samples.json`

### Notes
- Useful for short-horizon forecasting experiments.
- Row format is wide, with `V1` as series id and later columns as sequential values.

## Additional Recommended Benchmark Not Downloaded

### GIFT-Eval
- Source: `Salesforce/GiftEval`
- Why not downloaded now: benchmark is broader and more evaluation-oriented; better added once the experiment runner chooses a specific foundation-model protocol
- Why still important: covers diverse zero-shot time-series settings and is a good later-stage benchmark for comparing non-LLM foundation models vs LLM-based methods
