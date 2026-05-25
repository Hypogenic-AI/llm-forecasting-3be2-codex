# LLMs and Forecasting

This project tests whether a real LLM can beat contemporaneous human crowd forecasts on binary forecasting questions under two regimes drawn from the same local platform dataset. The experiment uses `gpt-4.1` on 60 matched question-timepoints from `datasets/forecast_questions_platforms/`, with both a `question_only` prompt and a `question_plus_history` prompt.

Key findings:
- In `long_term_low_data`, `gpt-4.1` beat the crowd on mean Brier with `question_only` (`0.151` vs `0.200`).
- In `short_term_high_data`, `question_only` lost badly to the crowd (`0.131` vs `0.065`), but `question_plus_history` nearly matched and slightly beat the crowd (`0.056` vs `0.065`).
- None of the LLM-vs-crowd paired comparisons were statistically significant at `alpha=0.05` with `n=30` per cell.
- The evidence supports the hypothesis only partially and only under specific prompt/information conditions.

Reproduce:
```bash
source .venv/bin/activate
python src/forecasting_experiment.py --model gpt-4.1 --sample-per-regime 30 --prompt-conditions question_only question_plus_history
python src/analyze_results.py
```

File structure:
- `planning.md`: research plan and experimental rationale
- `REPORT.md`: full report with results and limitations
- `src/forecasting_experiment.py`: dataset parsing, sampling, prompting, and API execution
- `src/analyze_results.py`: metrics, statistical tests, and figure generation
- `prompts/forecast_prompt.txt`: evaluation prompt
- `results/analysis/`: CSV summaries and statistical outputs
- `results/model_outputs/`: raw per-item API outputs
- `figures/`: generated plots

Full details: [REPORT.md](/workspaces/llm-forecasting-3be2-codex/REPORT.md)
