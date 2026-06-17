from __future__ import annotations

from src.ai_agent.goal_based_agent import build_recommendation


def test_build_recommendation_returns_required_keys():
    latest_meal = {
        "food": "Biryani",
        "calories": 450,
        "carbs": 55,
    }

    rec = build_recommendation(
        goal="Weight Loss",
        today_calories=2500,
        latest_meal=latest_meal,
    )

    assert isinstance(rec, dict)
    for key in [
        "main_advice",
        "why",
        "next_meal",
        "recommended_foods",
        "avoid_foods",
        "tips",
        "target_calories",
        "today_calories",
        "difference",
    ]:
        assert key in rec

    assert isinstance(rec["main_advice"], str)
    assert isinstance(rec["difference"], int)

