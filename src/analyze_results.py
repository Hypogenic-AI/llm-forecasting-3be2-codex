from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import wilcoxon


ROOT = Path(__file__).resolve().parent.parent


def bootstrap_mean_diff(a: np.ndarray, b: np.ndarray, n_boot: int = 5000, seed: int = 42) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    diffs = []
    idx = np.arange(len(a))
    for _ in range(n_boot):
        sample_idx = rng.choice(idx, size=len(idx), replace=True)
        diffs.append((a[sample_idx] - b[sample_idx]).mean())
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    return float(lo), float(hi)


def summarize_metrics(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (regime, prompt_condition), g in df.groupby(["regime", "prompt_condition"]):
        rows.append(
            {
                "regime": regime,
                "prompt_condition": prompt_condition,
                "n": len(g),
                "llm_brier_mean": g["llm_brier"].mean(),
                "crowd_brier_mean": g["crowd_brier"].mean(),
                "baseline_brier_mean": g["baseline_brier"].mean(),
                "llm_log_loss_mean": g["llm_log_loss"].mean(),
                "crowd_log_loss_mean": g["crowd_log_loss"].mean(),
                "llm_accuracy": ((g["llm_prob"] >= 0.5) == (g["resolution"] == 1)).mean(),
                "crowd_accuracy": ((g["crowd_prob"] >= 0.5) == (g["resolution"] == 1)).mean(),
                "llm_minus_crowd_brier_mean": (g["llm_brier"] - g["crowd_brier"]).mean(),
            }
        )
    return pd.DataFrame(rows).sort_values(["regime", "prompt_condition"])


def paired_tests(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (regime, prompt_condition), g in df.groupby(["regime", "prompt_condition"]):
        stat, p = wilcoxon(g["llm_brier"], g["crowd_brier"], alternative="two-sided")
        ci_lo, ci_hi = bootstrap_mean_diff(g["llm_brier"].to_numpy(), g["crowd_brier"].to_numpy())
        rows.append(
            {
                "regime": regime,
                "prompt_condition": prompt_condition,
                "wilcoxon_stat": float(stat),
                "p_value": float(p),
                "mean_brier_diff_llm_minus_crowd": (g["llm_brier"] - g["crowd_brier"]).mean(),
                "ci95_lo": ci_lo,
                "ci95_hi": ci_hi,
            }
        )
    return pd.DataFrame(rows).sort_values(["regime", "prompt_condition"])


def calibration_table(df: pd.DataFrame, forecaster_col: str, prob_col: str) -> pd.DataFrame:
    work = df.copy()
    work["bucket"] = pd.cut(work[prob_col], bins=np.linspace(0, 1, 6), include_lowest=True)
    out = (
        work.groupby("bucket", observed=False)
        .agg(
            n=("resolution", "size"),
            mean_prob=(prob_col, "mean"),
            empirical_yes=("resolution", "mean"),
        )
        .reset_index()
    )
    out["forecaster"] = forecaster_col
    return out


def main() -> None:
    figures_dir = ROOT / "figures"
    analysis_dir = ROOT / "results" / "analysis"
    figures_dir.mkdir(exist_ok=True, parents=True)

    df = pd.read_csv(analysis_dir / "forecast_results.csv")

    metric_summary = summarize_metrics(df)
    test_summary = paired_tests(df)
    metric_summary.to_csv(analysis_dir / "metric_summary.csv", index=False)
    test_summary.to_csv(analysis_dir / "paired_tests.csv", index=False)

    error_rows = []
    for (regime, prompt_condition), g in df.groupby(["regime", "prompt_condition"]):
        top = g.assign(abs_gap=(g["llm_brier"] - g["crowd_brier"]).abs()).sort_values("abs_gap", ascending=False).head(5)
        for _, row in top.iterrows():
            error_rows.append(
                {
                    "regime": regime,
                    "prompt_condition": prompt_condition,
                    "question": row["question"],
                    "resolution": row["resolution"],
                    "crowd_prob": row["crowd_prob"],
                    "llm_prob": row["llm_prob"],
                    "crowd_brier": row["crowd_brier"],
                    "llm_brier": row["llm_brier"],
                }
            )
    pd.DataFrame(error_rows).to_csv(analysis_dir / "error_analysis_examples.csv", index=False)

    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(10, 6))
    plot_df = df.melt(
        id_vars=["regime", "prompt_condition", "item_id"],
        value_vars=["llm_brier", "crowd_brier", "baseline_brier"],
        var_name="forecaster",
        value_name="brier",
    )
    sns.boxplot(data=plot_df, x="regime", y="brier", hue="forecaster")
    plt.title("Brier Score by Regime")
    plt.tight_layout()
    plt.savefig(figures_dir / "brier_by_regime.png", dpi=200)
    plt.close()

    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=metric_summary,
        x="regime",
        y="llm_minus_crowd_brier_mean",
        hue="prompt_condition",
    )
    plt.axhline(0.0, color="black", linewidth=1)
    plt.ylabel("Mean Brier Difference (LLM - Crowd)")
    plt.title("Negative Values Favor the LLM")
    plt.tight_layout()
    plt.savefig(figures_dir / "llm_minus_crowd_brier.png", dpi=200)
    plt.close()

    cal_frames = []
    for (regime, prompt_condition), g in df.groupby(["regime", "prompt_condition"]):
        llm_cal = calibration_table(g, "llm", "llm_prob")
        llm_cal["regime"] = regime
        llm_cal["prompt_condition"] = prompt_condition
        crowd_cal = calibration_table(g, "crowd", "crowd_prob")
        crowd_cal["regime"] = regime
        crowd_cal["prompt_condition"] = prompt_condition
        cal_frames.extend([llm_cal, crowd_cal])
    cal_df = pd.concat(cal_frames, ignore_index=True)
    cal_df.to_csv(analysis_dir / "calibration_table.csv", index=False)

    focus = cal_df[cal_df["prompt_condition"] == "question_plus_history"]
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharex=True, sharey=True)
    regimes = list(focus["regime"].drop_duplicates())
    for ax, regime in zip(axes, regimes):
        g = focus[focus["regime"] == regime]
        for forecaster, sub in g.groupby("forecaster"):
            ax.plot(sub["mean_prob"], sub["empirical_yes"], marker="o", label=forecaster)
        ax.plot([0, 1], [0, 1], linestyle="--", color="gray")
        ax.set_title(regime)
        ax.set_xlabel("Mean predicted probability")
        ax.set_ylabel("Empirical YES rate")
        ax.legend()
    plt.tight_layout()
    plt.savefig(figures_dir / "calibration_question_plus_history.png", dpi=200)
    plt.close()

    summary = {
        "metric_summary": metric_summary.to_dict(orient="records"),
        "paired_tests": test_summary.to_dict(orient="records"),
    }
    (analysis_dir / "summary.json").write_text(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
