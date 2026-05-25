from __future__ import annotations

import argparse
import json
import logging
import os
import random
import re
import subprocess
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from datasets import load_from_disk
from openai import OpenAI


ROOT = Path(__file__).resolve().parent.parent
PROMPT_PATH = ROOT / "prompts" / "forecast_prompt.txt"


def set_seed(seed: int = 42) -> None:
    random.seed(seed)
    np.random.seed(seed)


def setup_logging(log_path: Path) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[logging.FileHandler(log_path), logging.StreamHandler(sys.stdout)],
    )


@dataclass
class EvalItem:
    item_id: str
    regime: str
    source: str
    question: str
    background: str
    resolution_criteria: str
    date_begin: str
    date_resolve_at: str
    cutoff_date: str
    days_to_resolution: int
    n_predictions_seen: int
    crowd_prob: float
    resolution: float
    trajectory_summary: str
    trajectory_points_json: str


def safe_json_loads(text: str) -> Any:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            raise
        return json.loads(match.group(0))


def load_platform_test() -> pd.DataFrame:
    dataset = load_from_disk(str(ROOT / "datasets" / "forecast_questions_platforms"))["test"]
    rows = []
    for idx, ex in enumerate(dataset):
        if ex["question_type"] != "binary" or not ex["is_resolved"]:
            continue
        rows.append({"row_id": idx, **ex})
    return pd.DataFrame(rows)


def parse_predictions(text: str) -> list[tuple[pd.Timestamp, float]]:
    raw = safe_json_loads(text)
    parsed = []
    for date_str, prob in raw:
        parsed.append((pd.to_datetime(date_str), float(prob)))
    parsed.sort(key=lambda x: x[0])
    return parsed


def summarize_trajectory(points: list[tuple[pd.Timestamp, float]]) -> str:
    probs = [p for _, p in points]
    head = points[:2]
    tail = points[-3:]
    pieces = [
        f"{len(points)} crowd predictions observed before cutoff.",
        f"Initial probability: {head[0][1]:.2f} on {head[0][0].date()}.",
    ]
    if len(head) > 1:
        pieces.append(f"Early follow-up: {head[1][1]:.2f} on {head[1][0].date()}.")
    pieces.extend(
        [
            f"Latest available probability: {tail[-1][1]:.2f} on {tail[-1][0].date()}.",
            f"Range so far: min {min(probs):.2f}, max {max(probs):.2f}, mean {np.mean(probs):.2f}.",
            "Recent updates: "
            + "; ".join(f"{ts.date()}={prob:.2f}" for ts, prob in tail),
        ]
    )
    return " ".join(pieces)


def select_eval_items(df: pd.DataFrame, sample_per_regime: int, seed: int) -> list[EvalItem]:
    candidates_long: list[EvalItem] = []
    candidates_short: list[EvalItem] = []

    for _, row in df.iterrows():
        try:
            begin = pd.to_datetime(row["date_begin"])
            resolve = pd.to_datetime(row["date_resolve_at"])
            preds = parse_predictions(row["community_predictions"])
        except Exception:
            continue

        long_item = None
        for idx, (ts, prob) in enumerate(preds, start=1):
            days_to_resolution = int((resolve - ts).days)
            if days_to_resolution >= 60 and idx <= 5:
                subset = preds[:idx]
                long_item = EvalItem(
                    item_id=f"{row['row_id']}_long",
                    regime="long_term_low_data",
                    source=row["data_source"],
                    question=row["question"],
                    background=row["background"],
                    resolution_criteria=row["resolution_criteria"],
                    date_begin=str(begin),
                    date_resolve_at=str(resolve),
                    cutoff_date=str(ts),
                    days_to_resolution=days_to_resolution,
                    n_predictions_seen=idx,
                    crowd_prob=prob,
                    resolution=float(row["resolution"]),
                    trajectory_summary=summarize_trajectory(subset),
                    trajectory_points_json=json.dumps(
                        [[str(d.date()), round(p, 4)] for d, p in subset]
                    ),
                )
                break
        if long_item:
            candidates_long.append(long_item)

        short_item = None
        for idx in range(len(preds), 0, -1):
            ts, prob = preds[idx - 1]
            days_to_resolution = int((resolve - ts).days)
            if days_to_resolution <= 14 and idx >= 30:
                subset = preds[:idx]
                short_item = EvalItem(
                    item_id=f"{row['row_id']}_short",
                    regime="short_term_high_data",
                    source=row["data_source"],
                    question=row["question"],
                    background=row["background"],
                    resolution_criteria=row["resolution_criteria"],
                    date_begin=str(begin),
                    date_resolve_at=str(resolve),
                    cutoff_date=str(ts),
                    days_to_resolution=days_to_resolution,
                    n_predictions_seen=idx,
                    crowd_prob=prob,
                    resolution=float(row["resolution"]),
                    trajectory_summary=summarize_trajectory(subset),
                    trajectory_points_json=json.dumps(
                        [[str(d.date()), round(p, 4)] for d, p in subset[-10:]]
                    ),
                )
                break
        if short_item:
            candidates_short.append(short_item)

    rng = random.Random(seed)
    rng.shuffle(candidates_long)

    used_question_ids = {item.item_id.split("_")[0] for item in candidates_long[:sample_per_regime]}
    short_non_overlap = [
        item for item in candidates_short if item.item_id.split("_")[0] not in used_question_ids
    ]
    rng.shuffle(short_non_overlap)

    selected = candidates_long[:sample_per_regime] + short_non_overlap[:sample_per_regime]
    return selected


def build_user_prompt(item: EvalItem, prompt_condition: str) -> str:
    base = f"""
Forecasting question: {item.question}
Platform/source: {item.source}
Question opened: {item.date_begin}
Forecast cutoff date: {item.cutoff_date}
Resolution date: {item.date_resolve_at}
Days remaining until resolution at cutoff: {item.days_to_resolution}

Background:
{item.background}

Resolution criteria:
{item.resolution_criteria}
""".strip()

    if prompt_condition == "question_plus_history":
        history = f"""

Historical crowd information available before the cutoff:
{item.trajectory_summary}

Recent visible trajectory points:
{item.trajectory_points_json}
""".rstrip()
        return base + history
    return base


def get_env_info() -> dict[str, Any]:
    def run_cmd(cmd: list[str]) -> str:
        try:
            return subprocess.check_output(cmd, text=True).strip()
        except Exception:
            return "unavailable"

    return {
        "python": sys.version,
        "platform": sys.platform,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "working_directory": str(ROOT),
        "gpu_info": run_cmd(
            [
                "nvidia-smi",
                "--query-gpu=name,memory.total,memory.free",
                "--format=csv",
            ]
        ),
        "packages": {
            "numpy": np.__version__,
            "pandas": pd.__version__,
            "openai": __import__("openai").__version__,
        },
    }


def call_model(
    client: OpenAI,
    system_prompt: str,
    user_prompt: str,
    model: str,
    temperature: float,
    max_retries: int = 5,
) -> tuple[dict[str, Any], Any]:
    last_exc = None
    for attempt in range(1, max_retries + 1):
        try:
            response = client.chat.completions.create(
                model=model,
                temperature=temperature,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            )
            content = response.choices[0].message.content
            parsed = safe_json_loads(content)
            return parsed, response
        except Exception as exc:
            last_exc = exc
            sleep_s = min(2**attempt, 20)
            logging.warning("API call failed on attempt %s/%s: %s", attempt, max_retries, exc)
            time.sleep(sleep_s)
    raise RuntimeError(f"API call failed after {max_retries} attempts: {last_exc}")


def run_experiment(args: argparse.Namespace) -> None:
    set_seed(args.seed)
    output_dir = ROOT / "results" / "model_outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    df = load_platform_test()
    items = select_eval_items(df, sample_per_regime=args.sample_per_regime, seed=args.seed)
    system_prompt = PROMPT_PATH.read_text()
    client = OpenAI()

    metadata = {
        "model": args.model,
        "temperature": args.temperature,
        "seed": args.seed,
        "sample_per_regime": args.sample_per_regime,
        "prompt_conditions": args.prompt_conditions,
        "environment": get_env_info(),
    }
    (ROOT / "results" / "config.json").write_text(json.dumps(metadata, indent=2))

    pd.DataFrame([asdict(item) for item in items]).to_csv(
        ROOT / "results" / "analysis" / "selected_items.csv", index=False
    )

    records: list[dict[str, Any]] = []
    for item in items:
        for prompt_condition in args.prompt_conditions:
            user_prompt = build_user_prompt(item, prompt_condition)
            logging.info("Forecasting %s under %s", item.item_id, prompt_condition)
            parsed, response = call_model(
                client=client,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                model=args.model,
                temperature=args.temperature,
            )

            prob = float(parsed["prob_yes"])
            prob = min(max(prob, 0.01), 0.99)

            record = {
                **asdict(item),
                "prompt_condition": prompt_condition,
                "model": args.model,
                "llm_prob": prob,
                "llm_confidence": parsed.get("confidence", ""),
                "llm_rationale": parsed.get("rationale", ""),
                "crowd_brier": (item.crowd_prob - item.resolution) ** 2,
                "llm_brier": (prob - item.resolution) ** 2,
                "baseline_brier": (0.5 - item.resolution) ** 2,
                "crowd_log_loss": -(
                    item.resolution * np.log(max(item.crowd_prob, 1e-6))
                    + (1 - item.resolution) * np.log(max(1 - item.crowd_prob, 1e-6))
                ),
                "llm_log_loss": -(
                    item.resolution * np.log(max(prob, 1e-6))
                    + (1 - item.resolution) * np.log(max(1 - prob, 1e-6))
                ),
                "raw_response_text": response.choices[0].message.content,
                "prompt_text": user_prompt,
                "usage_prompt_tokens": getattr(response.usage, "prompt_tokens", None),
                "usage_completion_tokens": getattr(response.usage, "completion_tokens", None),
                "usage_total_tokens": getattr(response.usage, "total_tokens", None),
            }
            records.append(record)

            raw_path = output_dir / f"{item.item_id}__{prompt_condition}.json"
            raw_path.write_text(json.dumps(record, indent=2))
            time.sleep(args.sleep_between_calls)

    results_df = pd.DataFrame(records)
    results_path = ROOT / "results" / "analysis" / "forecast_results.csv"
    results_df.to_csv(results_path, index=False)
    logging.info("Saved %s rows to %s", len(results_df), results_path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="gpt-4.1")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--sample-per-regime", type=int, default=30)
    parser.add_argument(
        "--prompt-conditions",
        nargs="+",
        default=["question_only", "question_plus_history"],
        choices=["question_only", "question_plus_history"],
    )
    parser.add_argument("--sleep-between-calls", type=float, default=0.2)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    setup_logging(ROOT / "logs" / "forecasting_experiment.log")
    run_experiment(args)
