"""Deterministic graders for the Navis web tasks."""

from __future__ import annotations

from typing import Any, Dict

MIN_SCORE = 0.01
MAX_SCORE = 0.99


def normalize_score(score: float) -> float:
    """Clamp arbitrary scores into the strict OpenEnv-required interval (0, 1)."""

    return round(min(max(float(score), MIN_SCORE), MAX_SCORE), 3)


def grade_episode(summary: Dict[str, Any]) -> float:
    """Grade an episode summary on a deterministic scale strictly inside (0, 1)."""

    if not summary.get("reached_target"):
        raw_score = MIN_SCORE
    else:
        actual_steps = max(int(summary.get("actual_steps", 0)), 1)
        optimal_steps = max(int(summary.get("optimal_steps", actual_steps)), 1)
        efficiency = min(optimal_steps / actual_steps, 1.0)
        raw_score = 0.7 + (0.3 * efficiency)

    # OpenEnv requirement: scores must be strictly in (0.0, 1.0)
    return normalize_score(raw_score)
