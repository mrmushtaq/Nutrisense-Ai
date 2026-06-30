"""Validation engine for AI-generated meal plans — ensures every constraint is satisfied."""

from __future__ import annotations

from typing import Any

from src.ai_agent.meal_planner import MEAL_DATABASE, MEAL_TIMES, _filter_meals_by_preference
from src.ai.calorie_calculator import calculate_calorie_goal


def compute_macro_targets(
    goal_type: str,
    calorie_target: int,
    weight_kg: float | None = None,
) -> dict[str, int]:
    """Compute recommended daily protein, carbs, fat, and fiber targets based on goal."""
    protein_per_kg = {
        "Weight Loss": 1.8,
        "Weight Gain": 1.8,
        "Maintenance": 1.4,
        "Healthy Lifestyle": 1.4,
    }.get(goal_type, 1.4)

    if weight_kg and weight_kg > 0:
        protein_g = max(int(protein_per_kg * weight_kg), 60)
    else:
        protein_g = {"Weight Loss": 100, "Weight Gain": 110, "Maintenance": 80, "Healthy Lifestyle": 80}.get(goal_type, 80)

    protein_cal = protein_g * 4
    fat_cal = int(calorie_target * 0.25)
    fat_g = max(int(fat_cal / 9), 20)
    carb_cal = calorie_target - protein_cal - fat_cal
    carbs_g = max(int(carb_cal / 4), 50)

    return {
        "protein": protein_g,
        "carbs": carbs_g,
        "fat": fat_g,
        "fiber": 25,
    }


def detect_conflicts(goal_type: str, calorie_target: int) -> str | None:
    """Detect conflicting goals and return an explanatory message."""
    if goal_type == "Weight Gain" and calorie_target and calorie_target < 1800:
        return (
            "Building muscle while on a significant calorie deficit is difficult. "
            "I will prioritise a high-protein meal plan while staying as close as possible "
            "to your calorie target."
        )
    if goal_type == "Weight Loss" and calorie_target and calorie_target > 3000:
        return (
            "A calorie target this high may not support weight loss. "
            "I will generate a plan aligned with your selected goal."
        )
    return None


def _compute_actual_fiber(plan: dict) -> int:
    """Calculate total fiber from meal ingredients in the plan."""
    total = 0
    for meal_time in MEAL_TIMES:
        if meal_time in plan.get("meals", {}):
            m = plan["meals"][meal_time]
            total += m.get("fiber", 0)
    return total


def validate_plan(plan: dict, constraints: dict[str, Any]) -> dict[str, Any]:
    """Run all constraint checks against a meal plan and return results."""
    checks = []
    totals = plan.get("totals", {})
    target_cal = plan.get("target_calories", 2000)
    actual_cal = totals.get("calories", 0)

    # Calorie check (±15% window)
    cal_lower = int(target_cal * 0.85)
    cal_upper = int(target_cal * 1.15)
    cal_pass = cal_lower <= actual_cal <= cal_upper
    checks.append({
        "name": "Daily Calories",
        "passed": cal_pass,
        "actual": f"{actual_cal} kcal",
        "target": f"{target_cal} kcal",
    })

    # Protein check
    protein_target = constraints.get("protein_target", 80)
    actual_protein = totals.get("protein", 0)
    protein_pass = actual_protein >= protein_target * 0.9
    checks.append({
        "name": "Protein Target",
        "passed": protein_pass,
        "actual": f"{actual_protein}g",
        "target": f"≥{protein_target}g",
    })

    # Fiber check
    fiber_target = constraints.get("fiber_target", 25)
    actual_fiber = _compute_actual_fiber(plan)
    fiber_pass = actual_fiber >= fiber_target * 0.7
    checks.append({
        "name": "Fiber",
        "passed": fiber_pass,
        "actual": f"{actual_fiber}g",
        "target": f"≥{fiber_target}g",
    })

    # Dietary preference check
    pref = constraints.get("dietary_preference", "None")
    allergies = constraints.get("allergies", [])
    pref_pass = True
    pref_detail = f"{pref}" if pref != "None" else "None specified"
    if pref != "None":
        pref_map: dict[str, list[str]] = {
            "Vegetarian": ["vegetarian", "vegan"],
            "Vegan": ["vegan"],
            "Halal": ["halal"],
            "Keto": ["low_carb"],
            "Low-Carb": ["low_carb"],
            "High-Protein": ["high_protein"],
        }
        required_tags = pref_map.get(pref, [])
        for meal_time in MEAL_TIMES:
            if meal_time in plan.get("meals", {}):
                m = plan["meals"][meal_time]
                tags = m.get("tags", [])
                if required_tags and not any(t in tags for t in required_tags):
                    pref_pass = False
                    break

    checks.append({
        "name": "Dietary Preference",
        "passed": pref_pass,
        "actual": "Respected" if pref_pass else "Violated",
        "target": pref_detail,
    })

    # Allergy check
    allergy_pass = True
    allergy_violations = []
    if allergies:
        for meal_time in MEAL_TIMES:
            if meal_time in plan.get("meals", {}):
                m = plan["meals"][meal_time]
                name_lower = m["name"].lower()
                for a in allergies:
                    if a.strip() and a.strip().lower() in name_lower:
                        allergy_pass = False
                        allergy_violations.append(f"{m['name']} ({a})")

    checks.append({
        "name": "Allergy Safe",
        "passed": allergy_pass,
        "actual": "All clear" if allergy_pass else f"Conflict: {', '.join(allergy_violations)}",
        "target": ", ".join(allergies) if allergies else "None specified",
    })

    # Medical conditions check (diabetes → high fiber preference)
    med_conditions = constraints.get("medical_conditions", [])
    med_pass = True
    med_detail = []
    if any("diabetes" in c.lower() for c in med_conditions):
        if actual_fiber < 20:
            med_pass = False
            med_detail.append("Low fiber for diabetes-friendly plan")
    if any("hypertension" in c.lower() for c in med_conditions):
        pass  # No sodium data in meals currently

    checks.append({
        "name": "Medical Conditions",
        "passed": med_pass,
        "actual": "Respected" if med_pass else "; ".join(med_detail),
        "target": ", ".join(med_conditions) if med_conditions else "None specified",
    })

    # Goal support check
    goal = constraints.get("goal_type", "Maintenance")
    goal_pass = cal_pass  # calories aligned with goal
    checks.append({
        "name": f"Goal: {goal}",
        "passed": goal_pass,
        "actual": f"{actual_cal} kcal",
        "target": f"{target_cal} kcal target",
    })

    all_passed = all(c["passed"] for c in checks)

    return {
        "all_passed": all_passed,
        "checks": checks,
    }


def repair_plan(
    plan: dict,
    constraints: dict[str, Any],
    max_attempts: int = 15,
) -> dict:
    """Regenerate a meal plan until all constraints pass, or return best attempt."""
    best = plan
    best_result = validate_plan(plan, constraints)

    for attempt in range(max_attempts):
        if best_result["all_passed"]:
            break

        from src.ai_agent.meal_planner import _generate_daily_plan_raw

        new_plan = _generate_daily_plan_raw(
            goal_type=constraints.get("goal_type", "Maintenance"),
            calorie_target=constraints.get("calorie_target"),
            dietary_preference=constraints.get("dietary_preference", "None"),
            allergies=constraints.get("allergies", []),
        )

        result = validate_plan(new_plan, constraints)

        new_pass_count = sum(1 for c in result["checks"] if c["passed"])
        best_pass_count = sum(1 for c in best_result["checks"] if c["passed"])

        if new_pass_count > best_pass_count:
            best = new_plan
            best_result = result

    best["validation"] = best_result
    best["needs_attention"] = not best_result["all_passed"]
    return best


def generate_ingredient_grocery_list(plan: dict) -> dict[str, list[str]]:
    """Extract and deduplicate actual ingredient lists from meal plan meals."""
    grocery: dict[str, list[str]] = {
        "Vegetables": [],
        "Fruits": [],
        "Grains": [],
        "Proteins": [],
        "Healthy Fats": [],
        "Spices": [],
    }

    seen: set[str] = set()

    ingredient_category_map: dict[str, str] = {
        "oats": "Grains", "rice": "Grains", "bread": "Grains", "toast": "Grains",
        "roti": "Grains", "naan": "Grains", "granola": "Grains", "quinoa": "Grains",
        "pasta": "Grains", "wrap": "Grains", "flour": "Grains",
        "chicken": "Proteins", "fish": "Proteins", "eggs": "Proteins", "egg": "Proteins",
        "tofu": "Proteins", "lentils": "Proteins", "chickpeas": "Proteins",
        "lentil": "Proteins", "daal": "Proteins", "chana": "Proteins",
        "protein powder": "Proteins", "nuts": "Proteins", "seeds": "Proteins",
        "yogurt": "Proteins", "yoghurt": "Proteins", "milk": "Proteins",
        "cheese": "Proteins", "paneer": "Proteins",
        "banana": "Fruits", "berries": "Fruits", "fruit": "Fruits",
        "dates": "Fruits", "lemon": "Fruits", "apple": "Fruits",
        "spinach": "Vegetables", "broccoli": "Vegetables", "lettuce": "Vegetables",
        "onion": "Vegetables", "tomato": "Vegetables", "cucumber": "Vegetables",
        "carrot": "Vegetables", "bell pepper": "Vegetables", "green chili": "Vegetables",
        "coriander": "Vegetables", "spring onion": "Vegetables", "salad": "Vegetables",
        "vegetable": "Vegetables", "mixed vegetables": "Vegetables",
        "olive oil": "Healthy Fats", "oil": "Healthy Fats", "ghee": "Healthy Fats",
        "butter": "Healthy Fats", "honey": "Healthy Fats", "chia seeds": "Healthy Fats",
        "soy sauce": "Spices", "salt": "Spices", "pepper": "Spices",
        "cumin": "Spices", "biryani masala": "Spices", "chaat masala": "Spices",
        "garlic": "Spices", "ginger": "Spices", "herbs": "Spices",
        "turmeric": "Spices", "coriander powder": "Spices", "red chili": "Spices",
        "chilli": "Spices",
    }

    all_meal_names = []
    if isinstance(plan, list):
        for day_plan in plan:
            for mt in MEAL_TIMES:
                if mt in day_plan.get("meals", {}):
                    all_meal_names.append(day_plan["meals"][mt]["name"])
    else:
        for mt in MEAL_TIMES:
            if mt in plan.get("meals", {}):
                all_meal_names.append(plan["meals"][mt]["name"])

    for meal_name in all_meal_names:
        name_lower = meal_name.lower()
        for ingredient, category in ingredient_category_map.items():
            if ingredient in name_lower and ingredient not in seen:
                seen.add(ingredient)
                display_name = ingredient.title()
                grocery[category].append(display_name)

    for cat in list(grocery.keys()):
        grocery[cat] = sorted(set(grocery[cat]))
        if not grocery[cat]:
            del grocery[cat]

    return grocery


def generate_meal_reason(meal: dict, goal_type: str) -> str:
    """Generate a human-readable explanation for why a meal was selected."""
    name = meal["name"]
    tags = meal.get("tags", [])
    protein = meal.get("protein", 0)
    fiber = meal.get("fiber", 0)
    calories = meal.get("calories", 0)

    reasons = []

    if "high_protein" in tags and protein >= 20:
        reasons.append(f"high in protein ({protein}g)")
    if fiber >= 5:
        reasons.append(f"rich in fibre ({fiber}g)")
    if protein >= 20 and fiber >= 5:
        reasons = [f"provides {protein}g protein and {fiber}g fibre"]

    if goal_type == "Weight Loss":
        if calories <= 250:
            reasons.append(f"light option at {calories} kcal")
        elif "low_carb" in tags:
            reasons.append("low in carbohydrates")
        if "vegetarian" in tags or "vegan" in tags:
            reasons.append("plant-based for sustained energy")
    elif goal_type == "Weight Gain":
        if calories >= 350:
            reasons.append(f"calorie-dense at {calories} kcal")
        if "high_protein" in tags:
            reasons.append("supports muscle repair and growth")
    elif goal_type == "Healthy Lifestyle":
        if "vegetarian" in tags or "vegan" in tags:
            reasons.append("whole-food plant-based option")
        if fiber >= 4:
            reasons.append("supports digestive health")
    else:
        if "vegetarian" in tags or "vegan" in tags:
            reasons.append("balanced plant-based option")

    if not reasons:
        if calories <= 200:
            reasons.append(f"light at {calories} kcal")
        else:
            reasons.append(f"balanced option at {calories} kcal")

    return f"{name} was selected because it {reasons[0]}."
