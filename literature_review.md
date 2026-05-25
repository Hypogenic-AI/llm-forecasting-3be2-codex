# Literature Review: LLMs and Forecasting

## Review Scope

### Research Question
Do LLMs outperform humans at short-term high-data forecasting and long-term low-data forecasting?

### Inclusion Criteria
- Papers on LLMs or language-model-based systems for forecasting.
- Papers with direct comparison to human or crowd forecasts, or to strong forecasting baselines.
- Papers that expose datasets, code, or benchmarks usable for follow-on experiments.
- Recent core papers from 2023 onward, plus directly relevant foundational/benchmark papers.

### Exclusion Criteria
- Purely descriptive LLM papers without forecasting evaluation.
- Domain papers where forecasting is incidental and not benchmarked.
- Papers without enough methodological detail to support reproduction planning.

### Time Frame
2023 to 2026, with emphasis on 2024 to 2026.

### Sources
- Paper-finder workflow and manual fallback
- arXiv
- Hugging Face dataset cards
- GitHub repositories

## Search Log

| Date | Query | Source | Notes |
|------|-------|--------|-------|
| 2026-05-25 | `large language models forecasting humans short-term long-term low-data high-data` | paper-finder script | Service path was slow; used manual follow-up |
| 2026-05-25 | `LLM forecasting time series human baseline` | paper-finder script | Used to seed time-series branch |
| 2026-05-25 | `language models forecasting geopolitical events human forecasts` | paper-finder script | Used to seed event-forecasting branch |
| 2026-05-25 | `large language models are zero-shot time series forecasters` | arXiv/manual | Confirmed seminal time-series paper |
| 2026-05-25 | `Approaching Human-Level Forecasting with Language Models` | arXiv/manual | Confirmed direct human comparison |
| 2026-05-25 | `Are Language Models Actually Useful for Time Series Forecasting?` | arXiv/manual | Confirmed strong ablation counterpoint |

## Screening Results

| Paper | Title Screen | Abstract Screen | Full Text | Notes |
|------|------|------|------|------|
| Halawi et al. 2024 | Include | Include | Include | Central event-forecasting paper |
| Schoenegger and Park 2023 | Include | Include | Include | Direct GPT-4 vs human crowd |
| Paleka et al. 2024 | Include | Include | Abstract+methods | Evaluation methodology |
| Gruver et al. 2023 | Include | Include | Abstract+results | Seminal zero-shot TS paper |
| Jin et al. 2023 | Include | Include | Include | Major TS-LLM method |
| Tan et al. 2024 | Include | Include | Include | Critical ablation paper |
| Liu et al. 2024 | Include | Include | Abstract+results | Time-series foundation-model comparator |
| Guo et al. 2026 | Include | Include | Abstract+results | Recent TS-LLM improvement |

## Key Papers

### Paper 1: Approaching Human-Level Forecasting with Language Models
- **Authors**: Danny Halawi, Fred Zhang, Chen Yueh-Han, Jacob Steinhardt
- **Year**: 2024
- **Source**: arXiv / NeurIPS 2024
- **Key Contribution**: Retrieval-augmented LM forecasting system evaluated on real questions from five forecasting platforms.
- **Methodology**: LM-generated search queries, news retrieval, article relevance filtering, summarization, multiple reasoned forecasts, trimmed-mean aggregation, and self-supervised fine-tuning.
- **Datasets Used**: Curated binary-question dataset from Metaculus, GJOpen, INFER, Polymarket, and Manifold; 5,516 binary questions after curation, with 3,762 train, 840 validation, 914 test.
- **Baselines Compared Against**: Zero-shot and scratchpad prompting across GPT-4, Claude, Gemini, Llama, Mixtral, plus human crowd aggregate.
- **Evaluation Metrics**: Brier score, accuracy, calibration.
- **Results**: Best baseline LM around 0.208 Brier on the test set; crowd aggregate 0.149; their full system reaches 0.179. The system is closer to crowd performance on earlier retrieval dates and on questions where the crowd is uncertain.
- **Code Available**: Yes, cloned in `code/llm_forecasting/`
- **Relevance to Our Research**: Strongest available evidence for LMs in low-data judgmental forecasting. Supports "approaches human level" but does not show general crowd outperformance.

### Paper 2: Large Language Model Prediction Capabilities: Evidence from a Real-World Forecasting Tournament
- **Authors**: Philipp Schoenegger, Peter S. Park
- **Year**: 2023
- **Source**: arXiv
- **Key Contribution**: Direct live-tournament comparison between GPT-4 and human forecasters.
- **Methodology**: Entered GPT-4 into a three-month Metaculus tournament and compared same-day initial forecasts against human crowd medians.
- **Datasets Used**: 23 binary questions from a live Metaculus tournament spanning politics, technology, public health, and geopolitics.
- **Baselines Compared Against**: Human crowd median and 0.5 no-information baseline.
- **Evaluation Metrics**: Brier score, directional accuracy.
- **Results**: GPT-4 average Brier 0.20 versus human crowd 0.07; GPT-4 did not significantly beat the 0.25 no-information baseline.
- **Code Available**: No dedicated repo found.
- **Relevance to Our Research**: Important negative result. Early general-purpose GPT-4 did not match humans at real-world event forecasting.

### Paper 3: Consistency Checks for Language Model Forecasters
- **Authors**: Daniel Paleka et al.
- **Year**: 2024
- **Source**: arXiv
- **Key Contribution**: Instantaneous evaluation framework for forecasters using arbitrage-style logical consistency.
- **Methodology**: Generate logically related question sets, elicit forecasts, and compute consistency metrics that correlate with eventual Brier scores.
- **Datasets Used**: Automated consistency benchmark and future-resolving benchmark.
- **Baselines Compared Against**: Multiple LM forecasters.
- **Evaluation Metrics**: Consistency metrics, Brier correlation.
- **Results**: Consistency metrics can help rank forecasters before outcomes resolve.
- **Code Available**: Not used locally.
- **Relevance to Our Research**: Useful evaluation tool for long-horizon questions where waiting for resolution is slow.

### Paper 4: Large Language Models Are Zero-Shot Time Series Forecasters
- **Authors**: Nate Gruver, Marc Finzi, Shikai Qiu, Andrew Gordon Wilson
- **Year**: 2023
- **Source**: arXiv / NeurIPS 2023
- **Key Contribution**: Shows numeric time series can be encoded as text and extrapolated with general LLMs in zero-shot mode.
- **Methodology**: Scale/serialize numeric sequences into text, sample textual continuations, decode back to time-series forecasts.
- **Datasets Used**: Darts and Monash-style benchmark sets.
- **Baselines Compared Against**: Standard time-series baselines and multiple base LLMs.
- **Evaluation Metrics**: Forecast likelihood and benchmark forecasting metrics.
- **Results**: Competitive zero-shot performance, but aligned models can underperform less-aligned base models.
- **Code Available**: Yes, cloned in `code/llmtime/`
- **Relevance to Our Research**: Important short-term high-data TS baseline, but it contains no human comparison.

### Paper 5: Time-LLM: Time Series Forecasting by Reprogramming Large Language Models
- **Authors**: Ming Jin et al.
- **Year**: 2023
- **Source**: arXiv / ICLR 2024
- **Key Contribution**: Reprograms frozen LLMs for time-series forecasting using patch embeddings and prompt prefixes.
- **Methodology**: RevIN normalization, patching, patch reprogramming into text-prototype space, prompt-as-prefix, frozen LLM backbone, lightweight trainable heads.
- **Datasets Used**: ETT, Weather, Electricity, Traffic, ILI, and M4.
- **Baselines Compared Against**: GPT4TS, DLinear, PatchTST, TimesNet, FEDformer, Autoformer, Informer, Reformer, N-BEATS, N-HiTS, and others.
- **Evaluation Metrics**: MSE, MAE, SMAPE, MASE, OWA.
- **Results**: Reports strong performance on long-term forecasting and few-shot settings, often beating specialized baselines.
- **Code Available**: Yes, cloned in `code/Time-LLM/`
- **Relevance to Our Research**: Useful if the project treats short-term high-data forecasting as benchmark time-series prediction rather than human judgment.

### Paper 6: Are Language Models Actually Useful for Time Series Forecasting?
- **Authors**: Mingtian Tan et al.
- **Year**: 2024
- **Source**: arXiv / NeurIPS 2024
- **Key Contribution**: Strong ablation study questioning whether LLM components help time-series forecasting at all.
- **Methodology**: Reproduces Time-LLM, OneFitsAll, and CALF; removes or replaces the LLM with attention/transformer blocks; evaluates speed, few-shot behavior, and shuffled-input sensitivity.
- **Datasets Used**: ETT, Illness, Weather, Traffic, Electricity, Exchange Rate, Covid Deaths, Taxi, NN5, FRED-MD, and more.
- **Baselines Compared Against**: Original LLM-based methods and simple patch/attention baselines.
- **Evaluation Metrics**: MAE, MSE, runtime, few-shot performance.
- **Results**: Simpler ablations often match or beat the original LLM-based models while using orders of magnitude less compute; shuffled inputs do not strongly hurt performance, suggesting weak sequence modeling transfer from LLMs.
- **Code Available**: Yes, cloned in `code/LLMsForTimeSeries/`
- **Relevance to Our Research**: The strongest caution against assuming LLM superiority in high-data time-series forecasting.

### Paper 7: Timer: Generative Pre-trained Transformers Are Large Time Series Models
- **Authors**: Yong Liu et al.
- **Year**: 2024
- **Source**: arXiv
- **Key Contribution**: Builds a large time-series model directly for forecasting/imputation/anomaly detection.
- **Methodology**: Generative pretraining over time-series tasks.
- **Datasets Used**: Benchmark time-series suites.
- **Baselines Compared Against**: Multiple TS models.
- **Evaluation Metrics**: Standard forecasting metrics.
- **Results**: Strong evidence that purpose-built TS foundation models may be a cleaner comparator than repurposed text LLMs.
- **Code Available**: Referenced in paper.
- **Relevance to Our Research**: Good non-LLM baseline family for experiments.

### Paper 8: T-LLM: Teaching Large Language Models to Forecast Time Series via Temporal Distillation
- **Authors**: Suhan Guo et al.
- **Year**: 2026
- **Source**: arXiv
- **Key Contribution**: Explicitly teaches forecasting behavior to LLMs through a temporal teacher.
- **Methodology**: Distillation from a lightweight temporal teacher into an LLM, then teacher removed at inference.
- **Datasets Used**: Benchmark TS datasets and infectious-disease forecasting tasks.
- **Baselines Compared Against**: Existing LLM-based forecasting methods.
- **Evaluation Metrics**: Standard forecasting metrics under full-shot, few-shot, and zero-shot settings.
- **Results**: Claims gains over prior TS-LLM methods.
- **Code Available**: Not cloned locally.
- **Relevance to Our Research**: Suggests the TS-LLM field is moving away from naive repurposing toward explicitly forecast-trained hybrids.

## Common Methodologies

- **Retrieval-augmented judgmental forecasting**: Used by Halawi et al. for low-data event forecasting with historical news retrieval and forecast aggregation.
- **Direct live prompting on open questions**: Used by Schoenegger and Park; simple but weaker than the retrieval-augmented systems.
- **Numeric-to-text serialization**: Used by LLMTime for zero-shot time-series extrapolation.
- **Patch reprogramming of frozen LLMs**: Used by Time-LLM to map time-series patches into language-model space.
- **Ablation-based skepticism**: Used by Tan et al. to test whether the LLM component contributes anything beyond patching and attention.

## Standard Baselines

- **Human crowd aggregate**: The most important baseline for question/event forecasting.
- **0.5 no-information forecast**: Useful sanity baseline in binary forecasting.
- **Traditional TS neural baselines**: DLinear, PatchTST, TimesNet, FEDformer, Autoformer, Informer, N-BEATS, N-HiTS.
- **Alternative TS foundation models**: Timer and related purpose-built time-series models.

## Evaluation Metrics

- **Brier score**: Primary metric for binary question forecasting; lower is better.
- **Accuracy and calibration**: Important complements for judgmental forecasting.
- **MSE / MAE**: Standard for long-horizon time-series forecasting.
- **SMAPE / MASE / OWA**: Standard for M4-style short-term time-series benchmarks.

## Datasets in the Literature

- **Forecasting platform questions**: Metaculus, GJOpen, INFER, Polymarket, Manifold. Best for LM-vs-human comparison.
- **FOReCAst**: Compact binary forecasting dataset suited to lightweight experiments.
- **YuehHanChen/forecasting**: Larger curated platform dataset aligned to Halawi et al.
- **ETT / Weather / Electricity / Traffic / ILI**: Standard long-horizon TS benchmarks used by Time-LLM and follow-ups.
- **M4**: Canonical short-term benchmark used for broad TS comparisons.

## Gaps and Opportunities

- **Gap 1: Human comparisons are concentrated in event forecasting, not numeric time series.**
  There is little direct evidence for "LLMs vs humans" on short-term high-data numeric series.

- **Gap 2: Strong positive TS-LLM papers are contested by later ablations.**
  The literature is not settled that text LLMs are the right tool for benchmark time-series forecasting.

- **Gap 3: The hypothesis mixes two forecasting regimes.**
  "Short-term high-data" fits numeric time series, while "long-term low-data" fits question/event forecasting. They likely need separate experimental pipelines.

## Recommendations for Our Experiment

- **Primary dataset(s)**:
  - `datasets/forecast_questions_platforms/` for long-term low-data judgmental forecasting.
  - `datasets/timeseries_m4_hourly/` and `datasets/timeseries_etth1/` for short-term high-data time-series forecasting.

- **Recommended baselines**:
  - Human/community crowd aggregate for question forecasting.
  - 0.5 baseline for binary sanity checks.
  - DLinear or PAttn for time-series baselines.
  - Time-LLM and LLMTime as LLM-based comparators.

- **Recommended metrics**:
  - Brier score and calibration for question forecasting.
  - MAE/MSE for ETT.
  - SMAPE/MASE/OWA for M4-style series.

- **Methodological considerations**:
  - Treat event forecasting and numeric time-series forecasting as separate experiments.
  - Do not claim human outperformance on high-data numeric TS unless a real human benchmark is introduced.
  - For long-term low-data questions, compare against the crowd aggregate at matched retrieval dates.
  - For high-data TS, include skeptical ablations because current literature shows many LLM gains may come from non-LLM components.

## Bottom Line

Current evidence does **not** cleanly support the full hypothesis as stated.

- For **long-term low-data judgmental forecasting**, LMs can approach human crowd performance and sometimes beat the crowd on subsets, especially early in a question lifecycle or when the crowd is uncertain.
- For **short-term high-data time-series forecasting**, the literature is mixed: some papers report LLM gains, but strong later ablations suggest much of the benefit may come from patching, attention, or task setup rather than language modeling itself.

The best experiment is therefore a two-track design:
1. Question/event forecasting with human crowd baselines.
2. Numeric time-series forecasting with strong non-LLM baselines and, if desired, a separately collected human baseline.
