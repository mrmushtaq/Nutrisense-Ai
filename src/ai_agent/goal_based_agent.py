"""Goal-based AI agent.

Phase II: Rule-based recommendations using the config's GOAL_RECOMMENDATIONS.

The tests expect a function named `build_recommendation`.
"""

from __future__ import annotations

from typing import Any

from config import build_ai_recommendation


def build_recommendation(
    goal: str,
    today_calories: int,
    latest_meal: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build a recommendation payload for the UI.

    This is a thin wrapper around `config.build_ai_recommendation`.
    """

    return build_ai_recommendation(goal=goal, today_calories=today_calories, latest_meal=latest_meal)

