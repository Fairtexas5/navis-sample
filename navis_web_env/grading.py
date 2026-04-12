"""Deterministic graders for the Navis web tasks."""

from __future__ import annotations

import math
from typing import Any, Dict

MIN_SCORE = 0.01
MAX_SCORE = 0.99


def normalize_score(score: float) -> float:
    """Clamp arbitrary scores into the strict OpenEnv-required interval (0, 1)."""

    try:
        numeric_score = float(score)
    except (TypeError, ValueError):
        return MIN_SCORE

    if not math.isfinite(numeric_score):
        return MIN_SCORE

    return round(min(max(numeric_score, MIN_SCORE), MAX_SCORE), 3)


def grade_episode(summary: Dict[str, Any]) -> float:
    """Grade an episode summary with partial credit across outcome, workflow, and robustness."""

    if not summary:
        return MIN_SCORE

    try:
        actual_steps = max(int(summary.get("actual_steps", 0)), 1)
        optimal_steps = max(int(summary.get("optimal_steps", actual_steps)), 1)
        invalid_actions = max(int(summary.get("invalid_actions", 0)), 0)
        repeat_visits = max(int(summary.get("repeat_visits", 0)), 0)
    except (TypeError, ValueError):
        return MIN_SCORE

    reached_target = bool(summary.get("reached_target"))
    if "task_id" not in summary:
        if not reached_target:
            return MIN_SCORE
        return normalize_score(0.7 + (0.3 * min(optimal_steps / actual_steps, 0.99)))

    checkpoint_coverage = float(summary.get("checkpoint_coverage", 1.0 if reached_target else 0.0) or 0.0)
    ordered_checkpoint_completion = float(
        summary.get("ordered_checkpoint_completion", 1.0 if reached_target else 0.0) or 0.0
    )
    start_distance = max(int(summary.get("start_distance_to_target", optimal_steps)), 1)
    end_distance = max(int(summary.get("end_distance_to_target", start_distance)), 0)
    progress_ratio = 1.0 - min(end_distance / start_distance, 1.0)
    efficiency_ratio = min(optimal_steps / actual_steps, 1.0)
    robustness_penalty = min((invalid_actions * 0.08) + (repeat_visits * 0.04), 0.45)
    termination_reason = summary.get("termination_reason")
    loop_penalty = 0.08 if termination_reason == "loop_cap_exceeded" else 0.0

    outcome_score = 0.55 if reached_target else 0.15 * progress_ratio
    workflow_score = 0.18 * checkpoint_coverage + 0.12 * ordered_checkpoint_completion
    efficiency_score = (0.15 if reached_target else 0.08) * efficiency_ratio
    robustness_score = max(0.0, 0.12 - robustness_penalty - loop_penalty)

    raw_score = outcome_score + workflow_score + efficiency_score + robustness_score
    if not reached_target:
        raw_score = min(raw_score, 0.69)

    return normalize_score(raw_score)
