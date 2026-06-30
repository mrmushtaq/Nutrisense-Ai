"""Smart Meal Planner for NutriSense AI — generates daily/weekly meal plans."""

from __future__ import annotations

import random
from typing import Any

from config import GOAL_RECOMMENDATIONS

# Nutrition database for plan generation
MEAL_DATABASE: dict[str, list[dict[str, Any]]] = {
    "Breakfast": [
        {"name": "Oatmeal with Berries", "calories": 210, "protein": 8, "carbs": 38, "fat": 4, "fiber": 6, "ingredients": ["oats", "berries", "honey"], "tags": ["vegetarian", "vegan", "low_carb", "halal"]},
        {"name": "Scrambled Eggs with Toast", "calories": 320, "protein": 22, "carbs": 28, "fat": 14, "fiber": 2, "ingredients": ["eggs", "bread", "butter", "salt", "pepper"], "tags": ["vegetarian", "high_protein", "halal"]},
        {"name": "Greek Yoghurt with Granola", "calories": 260, "protein": 18, "carbs": 32, "fat": 8, "fiber": 3, "ingredients": ["yogurt", "granola", "berries"], "tags": ["vegetarian", "high_protein", "halal"]},
        {"name": "Smoothie Bowl", "calories": 280, "protein": 12, "carbs": 42, "fat": 7, "fiber": 5, "ingredients": ["banana", "berries", "yogurt", "granola", "chia seeds"], "tags": ["vegetarian", "vegan", "halal"]},
        {"name": "Paratha with Yogurt", "calories": 350, "protein": 10, "carbs": 40, "fat": 16, "fiber": 2, "ingredients": ["flour", "ghee", "yogurt", "salt"], "tags": ["vegetarian", "halal"]},
        {"name": "Boiled Eggs with Banana", "calories": 230, "protein": 16, "carbs": 24, "fat": 10, "fiber": 3, "ingredients": ["eggs", "banana", "salt", "pepper"], "tags": ["vegetarian", "high_protein", "low_carb", "halal"]},
    ],
    "Lunch": [
        {"name": "Grilled Chicken with Rice", "calories": 450, "protein": 32, "carbs": 48, "fat": 12, "fiber": 2, "ingredients": ["chicken", "rice", "olive oil", "salt", "pepper", "herbs"], "tags": ["high_protein", "halal"]},
        {"name": "Daal Chawal", "calories": 380, "protein": 14, "carbs": 58, "fat": 10, "fiber": 8, "ingredients": ["lentils", "rice", "onion", "garlic", "tomato", "cumin", "turmeric"], "tags": ["vegetarian", "vegan", "halal"]},
        {"name": "Chicken Salad Wrap", "calories": 350, "protein": 28, "carbs": 30, "fat": 12, "fiber": 4, "ingredients": ["chicken", "lettuce", "tomato", "wrap", "olive oil", "lemon"], "tags": ["high_protein", "low_carb", "halal"]},
        {"name": "Vegetable Stir-fry with Tofu", "calories": 310, "protein": 18, "carbs": 35, "fat": 11, "fiber": 6, "ingredients": ["tofu", "broccoli", "carrot", "bell pepper", "soy sauce", "garlic", "ginger", "oil"], "tags": ["vegetarian", "vegan", "low_carb", "halal"]},
        {"name": "Chicken Karahi with Roti", "calories": 420, "protein": 30, "carbs": 38, "fat": 16, "fiber": 3, "ingredients": ["chicken", "tomato", "ginger", "garlic", "green chili", "coriander", "oil", "cumin", "roti"], "tags": ["halal"]},
        {"name": "Quinoa Bowl with Chickpeas", "calories": 360, "protein": 16, "carbs": 50, "fat": 10, "fiber": 8, "ingredients": ["quinoa", "chickpeas", "cucumber", "tomato", "lemon", "olive oil"], "tags": ["vegetarian", "vegan", "halal"]},
    ],
    "Dinner": [
        {"name": "Grilled Fish with Vegetables", "calories": 380, "protein": 34, "carbs": 20, "fat": 14, "fiber": 5, "ingredients": ["fish", "broccoli", "lemon", "olive oil", "garlic", "herbs"], "tags": ["high_protein", "low_carb", "halal"]},
        {"name": "Lentil Soup with Bread", "calories": 320, "protein": 18, "carbs": 42, "fat": 8, "fiber": 8, "ingredients": ["lentils", "onion", "garlic", "tomato", "cumin", "bread"], "tags": ["vegetarian", "vegan", "halal"]},
        {"name": "Chicken Breast with Salad", "calories": 340, "protein": 36, "carbs": 12, "fat": 10, "fiber": 4, "ingredients": ["chicken", "lettuce", "tomato", "cucumber", "olive oil", "lemon"], "tags": ["high_protein", "low_carb", "halal"]},
        {"name": "Egg Fried Rice", "calories": 400, "protein": 20, "carbs": 50, "fat": 14, "fiber": 2, "ingredients": ["rice", "eggs", "carrot", "soy sauce", "oil", "spring onion"], "tags": ["vegetarian", "halal"]},
        {"name": "Seekh Kabab with Naan", "calories": 430, "protein": 28, "carbs": 38, "fat": 18, "fiber": 2, "ingredients": ["chicken", "onion", "garlic", "ginger", "green chili", "coriander", "cumin", "naan"], "tags": ["halal"]},
        {"name": "Vegetable Curry with Rice", "calories": 350, "protein": 12, "carbs": 48, "fat": 12, "fiber": 5, "ingredients": ["mixed vegetables", "onion", "tomato", "garlic", "ginger", "oil", "cumin", "rice"], "tags": ["vegetarian", "vegan", "halal"]},
    ],
    "Snacks": [
        {"name": "Mixed Nuts", "calories": 180, "protein": 6, "carbs": 8, "fat": 16, "fiber": 3, "ingredients": ["almonds", "walnuts", "cashews"], "tags": ["vegetarian", "vegan", "low_carb", "halal"]},
        {"name": "Fruit Bowl", "calories": 120, "protein": 2, "carbs": 30, "fat": 1, "fiber": 5, "ingredients": ["apple", "banana", "berries"], "tags": ["vegetarian", "vegan", "halal"]},
        {"name": "Protein Shake", "calories": 150, "protein": 25, "carbs": 8, "fat": 3, "fiber": 1, "ingredients": ["protein powder", "milk", "banana"], "tags": ["vegetarian", "high_protein", "low_carb", "halal"]},
        {"name": "Hummus with Veggies", "calories": 160, "protein": 8, "carbs": 16, "fat": 10, "fiber": 4, "ingredients": ["chickpeas", "olive oil", "lemon", "garlic", "carrot", "cucumber"], "tags": ["vegetarian", "vegan", "low_carb", "halal"]},
        {"name": "Yogurt with Dates", "calories": 200, "protein": 10, "carbs": 28, "fat": 5, "fiber": 2, "ingredients": ["yogurt", "dates"], "tags": ["vegetarian", "halal"]},
        {"name": "Chana Chaat", "calories": 220, "protein": 8, "carbs": 32, "fat": 8, "fiber": 7, "ingredients": ["chickpeas", "onion", "tomato", "cucumber", "lemon", "chaat masala", "coriander"], "tags": ["vegetarian", "vegan", "halal"]},
    ],
}

MEAL_TIMES = ["Breakfast", "Lunch", "Dinner", "Snacks"]


def _filter_meals_by_preference(
    options: list[dict[str, Any]],
    dietary_preference: str,
    allergies: list[str],
) -> list[dict[str, Any]]:
    """Filter meal options based on dietary preference and allergen keywords."""
    pref_map: dict[str, list[str]] = {
        "Vegetarian": ["vegetarian", "vegan"],
        "Vegan": ["vegan"],
        "Halal": ["halal"],
        "Keto": ["low_carb"],
        "Low-Carb": ["low_carb"],
        "High-Protein": ["high_protein"],
    }
    required_tags = pref_map.get(dietary_preference, [])

    filtered = []
    for meal in options:
        tags = meal.get("tags", [])
        if required_tags and not any(t in tags for t in required_tags):
            continue
        if allergies:
            name_lower = meal["name"].lower()
            if any(a.strip().lower() in name_lower for a in allergies if a.strip()):
                continue
        filtered.append(meal)
    return filtered


def _generate_daily_plan_raw(
    goal_type: str = "Maintenance",
    calorie_target: int | None = None,
    dietary_preference: str = "None",
    allergies: list[str] | None = None,
    medical_conditions: list[str] | None = None,
    weight_kg: float | None = None,
) -> dict[str, Any]:
    """Internal: generate a single-day plan WITHOUT validation (no recursion)."""
    if allergies is None:
        allergies = []
    if medical_conditions is None:
        medical_conditions = []

    from src.ai_agent.meal_validator import compute_macro_targets

    rec = GOAL_RECOMMENDATIONS.get(goal_type, GOAL_RECOMMENDATIONS["Maintenance"])
    target = calorie_target or rec["daily_calories"]
    macro_targets = compute_macro_targets(goal_type, target, weight_kg)

    meals: dict[str, Any] = {}
    total_cal = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0

    for meal_time in MEAL_TIMES:
        options = MEAL_DATABASE.get(meal_time, [])
        if not options:
            continue

        filtered = _filter_meals_by_preference(options, dietary_preference, allergies)
        if not filtered:
            filtered = options

        selected = random.choice(filtered)
        meals[meal_time] = selected
        total_cal += selected["calories"]
        total_protein += selected["protein"]
        total_carbs += selected["carbs"]
        total_fat += selected["fat"]

    return {
        "meals": meals,
        "totals": {
            "calories": total_cal,
            "protein": total_protein,
            "carbs": total_carbs,
            "fat": total_fat,
        },
        "target_calories": target,
        "goal_type": goal_type,
        "macro_targets": macro_targets,
    }


def generate_daily_plan(
    goal_type: str = "Maintenance",
    calorie_target: int | None = None,
    dietary_preference: str = "None",
    allergies: list[str] | None = None,
    medical_conditions: list[str] | None = None,
    weight_kg: float | None = None,
) -> dict[str, Any]:
    """Generate a validated single-day meal plan based on goal and preferences."""
    if allergies is None:
        allergies = []
    if medical_conditions is None:
        medical_conditions = []

    from src.ai_agent.meal_validator import (
        detect_conflicts, repair_plan, generate_meal_reason,
    )

    rec = GOAL_RECOMMENDATIONS.get(goal_type, GOAL_RECOMMENDATIONS["Maintenance"])
    target = calorie_target or rec["daily_calories"]

    conflict_warning = detect_conflicts(goal_type, target)

    plan = _generate_daily_plan_raw(goal_type, target, dietary_preference, allergies, medical_conditions, weight_kg)

    constraints = {
        "calorie_target": target,
        "protein_target": plan["macro_targets"]["protein"],
        "fiber_target": plan["macro_targets"]["fiber"],
        "dietary_preference": dietary_preference,
        "allergies": allergies,
        "medical_conditions": medical_conditions,
        "goal_type": goal_type,
    }

    plan = repair_plan(plan, constraints)

    for mt in MEAL_TIMES:
        if mt in plan.get("meals", {}):
            plan["meals"][mt]["reason"] = generate_meal_reason(plan["meals"][mt], goal_type)

    if conflict_warning:
        plan["conflict_warning"] = conflict_warning

    return plan


def generate_weekly_plan(
    goal_type: str = "Maintenance",
    calorie_target: int | None = None,
    dietary_preference: str = "None",
    allergies: list[str] | None = None,
    medical_conditions: list[str] | None = None,
    weight_kg: float | None = None,
) -> list[dict[str, Any]]:
    """Generate a validated 7-day meal plan with varied meals each day."""
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    plans = []
    used_meals: dict[str, set[str]] = {mt: set() for mt in MEAL_TIMES}

    from src.ai_agent.meal_validator import generate_meal_reason

    for day in day_names:
        plan = generate_daily_plan(goal_type, calorie_target, dietary_preference, allergies, medical_conditions, weight_kg)

        for mt in MEAL_TIMES:
            if mt in plan["meals"] and plan["meals"][mt]["name"] in used_meals.get(mt, set()):
                options = [m for m in MEAL_DATABASE.get(mt, []) if m["name"] not in used_meals.get(mt, set())]
                if options:
                    new_selected = random.choice(options)
                    plan["meals"][mt] = new_selected
                    plan["meals"][mt]["reason"] = generate_meal_reason(new_selected, goal_type)

                    totals = plan["totals"]
                    totals["calories"] = sum(plan["meals"][mt2]["calories"] for mt2 in MEAL_TIMES if mt2 in plan["meals"])
                    totals["protein"] = sum(plan["meals"][mt2]["protein"] for mt2 in MEAL_TIMES if mt2 in plan["meals"])
                    totals["carbs"] = sum(plan["meals"][mt2]["carbs"] for mt2 in MEAL_TIMES if mt2 in plan["meals"])
                    totals["fat"] = sum(plan["meals"][mt2]["fat"] for mt2 in MEAL_TIMES if mt2 in plan["meals"])

            used_meals[mt].add(plan["meals"][mt]["name"])

        plan["day"] = day
        plans.append(plan)

    return plans


def estimate_meal_macros(meal_name: str) -> dict[str, float]:
    """Look up approximate macros for a known meal."""
    for meal_time, options in MEAL_DATABASE.items():
        for meal in options:
            if meal["name"].lower() == meal_name.lower():
                return {
                    "calories": meal["calories"],
                    "protein": meal["protein"],
                    "carbs": meal["carbs"],
                    "fat": meal["fat"],
                }
    return {"calories": 300, "protein": 15, "carbs": 30, "fat": 12}
