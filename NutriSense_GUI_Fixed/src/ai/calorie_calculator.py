"""Calorie goal calculator based on user profile inputs."""

from __future__ import annotations


_ACTIVITY_FACTORS = {
    "Sedentary": 1.2,
    "Light": 1.375,
    "Moderate": 1.55,
    "Active": 1.725,
    "Very Active": 1.9,
}


def calculate_calorie_goal(
    weight: float,
    height: float,
    age: int,
    sex: str,
    activity: str,
    goal_type: str,
) -> int:
    """Estimate daily calorie target using Mifflin-St Jeor BMR + activity multiplier."""
    if sex.lower() == "male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    tdee = bmr * _ACTIVITY_FACTORS.get(activity, 1.55)

    if goal_type == "Lose Weight":
        return max(int(tdee - 500), 1200)
    if goal_type == "Gain Weight":
        return int(tdee + 500)
    return int(tdee)
