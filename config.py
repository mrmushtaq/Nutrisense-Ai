# config.py — NutriSense AI shared configuration, dummy data, and shared CSS

APP_NAME    = "NutriSense AI"
APP_TAGLINE = "Intelligent Food Recognition & Personalized Nutrition"
VERSION     = "2.1 (Phase II — SQLite + UI Fix)"

DAILY_CALORIE_GOAL = 2200
DAILY_PROTEIN_GOAL = 120
DAILY_CARBS_GOAL   = 250
DAILY_FAT_GOAL     = 65

HEALTH_SCORE_HIGH   = 75
HEALTH_SCORE_MEDIUM = 50

DUMMY_FOOD_DB = {
    "Biryani": {
        "calories": 450, "protein": 20, "carbs": 55, "fat": 15,
        "fiber": 3, "sugar": 4, "sodium": 620,
        "health_score": 78, "meal_type": "Lunch",
        "description": "A fragrant South Asian rice dish cooked with aromatic spices and tender meat.",
    },
    "Salad": {
        "calories": 120, "protein": 5, "carbs": 14, "fat": 4,
        "fiber": 6, "sugar": 8, "sodium": 180,
        "health_score": 92, "meal_type": "Lunch",
        "description": "A fresh mix of leafy greens, colorful vegetables, and a light dressing.",
    },
    "Pizza": {
        "calories": 570, "protein": 22, "carbs": 68, "fat": 22,
        "fiber": 3, "sugar": 6, "sodium": 950,
        "health_score": 52, "meal_type": "Dinner",
        "description": "Italian flatbread topped with tomato sauce, melted cheese, and savory toppings.",
    },
    "Oatmeal": {
        "calories": 210, "protein": 8, "carbs": 38, "fat": 4,
        "fiber": 5, "sugar": 3, "sodium": 105,
        "health_score": 88, "meal_type": "Breakfast",
        "description": "Whole-grain oats simmered with milk or water, naturally rich in fiber.",
    },
    "Burger": {
        "calories": 520, "protein": 28, "carbs": 42, "fat": 26,
        "fiber": 2, "sugar": 9, "sodium": 820,
        "health_score": 48, "meal_type": "Dinner",
        "description": "A grilled beef patty in a soft bun, loaded with vegetables and condiments.",
    },
}

DUMMY_WEEKLY_CALORIES = {
    "Mon": 1820, "Tue": 2100, "Wed": 1950,
    "Thu": 2250, "Fri": 1780, "Sat": 2400, "Sun": 1900,
}

DUMMY_USER = {
    "name": "Demo User",
    "age": 22,
    "weight_kg": 68,
    "height_cm": 172,
    "activity_level": "Moderate",
    "goal": "Maintenance",
}

# Default dummy prediction shown after Analyze Food (Phase 1)
DUMMY_NUTRITION_DATA = {
    "food": "Biryani",
    "confidence": 96,
    "calories": 450,
    "protein": 20,
    "carbs": 55,
    "fat": 15,
    "fiber": 3,
    "sugar": 4,
    "sodium": 620,
    "health_score": 78,
    "meal_type": "Lunch",
    "description": (
        "A fragrant South Asian rice dish cooked with aromatic spices and tender meat. "
        "Calorie-dense and rich in carbohydrates — suitable for lunch with portion control."
    ),
}

DUMMY_MEAL_HISTORY = [
    {"Food": "Biryani",  "Calories": 450, "Protein (g)": 20, "Carbs (g)": 55, "Fat (g)": 15, "Meal Type": "Lunch",     "Date": "2026-06-10", "Health Score": 78},
    {"Food": "Oatmeal",  "Calories": 210, "Protein (g)": 8,  "Carbs (g)": 38, "Fat (g)": 4,  "Meal Type": "Breakfast", "Date": "2026-06-10", "Health Score": 88},
    {"Food": "Salad",    "Calories": 120, "Protein (g)": 5,  "Carbs (g)": 14, "Fat (g)": 4,  "Meal Type": "Lunch",     "Date": "2026-06-09", "Health Score": 92},
    {"Food": "Pizza",    "Calories": 570, "Protein (g)": 22, "Carbs (g)": 68, "Fat (g)": 22, "Meal Type": "Dinner",    "Date": "2026-06-09", "Health Score": 52},
    {"Food": "Burger",   "Calories": 520, "Protein (g)": 28, "Carbs (g)": 42, "Fat (g)": 26, "Meal Type": "Dinner",    "Date": "2026-06-08", "Health Score": 48},
    {"Food": "Oatmeal",  "Calories": 210, "Protein (g)": 8,  "Carbs (g)": 38, "Fat (g)": 4,  "Meal Type": "Breakfast", "Date": "2026-06-08", "Health Score": 88},
    {"Food": "Salad",    "Calories": 120, "Protein (g)": 5,  "Carbs (g)": 14, "Fat (g)": 4,  "Meal Type": "Lunch",     "Date": "2026-06-07", "Health Score": 92},
    {"Food": "Biryani",  "Calories": 450, "Protein (g)": 20, "Carbs (g)": 55, "Fat (g)": 15, "Meal Type": "Dinner",    "Date": "2026-06-07", "Health Score": 78},
]

USER_GOALS = ["Weight Loss", "Weight Gain", "Maintenance", "Healthy Lifestyle"]
ACTIVITY_LEVELS = ["Low", "Moderate", "High"]

GOAL_RECOMMENDATIONS = {
    "Weight Loss": {
        "daily_calories": 1700,
        "recommended_foods": ["Salad", "Grilled Chicken", "Oatmeal", "Greek Yogurt", "Lentils", "Berries"],
        "avoid_foods": ["Fried foods", "Sugary drinks", "White bread", "Pastries", "Fast food"],
        "next_meals": {
            "high_cal": "Grilled chicken salad with lemon dressing",
            "balanced": "Vegetable soup with a side of grilled fish",
            "low_cal": "Greek yogurt with berries and a handful of almonds",
        },
        "macros": {"Protein": 35, "Carbs": 35, "Fat": 30},
        "tips": [
            "Eat protein at every meal to stay full longer.",
            "Fill half your plate with non-starchy vegetables.",
            "Drink water before meals to support portion control.",
        ],
    },
    "Weight Gain": {
        "daily_calories": 2800,
        "recommended_foods": ["Eggs", "Brown Rice", "Nuts", "Avocado", "Whole Milk", "Salmon", "Lean Beef"],
        "avoid_foods": ["Low-calorie diet foods", "Excessive caffeine", "Skipping meals"],
        "next_meals": {
            "high_cal": "Brown rice with grilled chicken and avocado",
            "balanced": "Whole-grain sandwich with eggs and milk",
            "low_cal": "Peanut butter banana smoothie with oats",
        },
        "macros": {"Protein": 30, "Carbs": 45, "Fat": 25},
        "tips": [
            "Add calorie-dense snacks between meals.",
            "Prioritize strength training with adequate protein intake.",
            "Use healthy fats like nuts, olive oil, and avocado.",
        ],
    },
    "Maintenance": {
        "daily_calories": 2200,
        "recommended_foods": ["Mixed Vegetables", "Whole Grains", "Lean Meats", "Fruits", "Legumes"],
        "avoid_foods": ["Highly processed snacks", "Trans fats", "Excess alcohol"],
        "next_meals": {
            "high_cal": "Grilled fish with quinoa and steamed vegetables",
            "balanced": "Lentil curry with brown rice and salad",
            "low_cal": "Vegetable stir-fry with tofu and whole grains",
        },
        "macros": {"Protein": 25, "Carbs": 50, "Fat": 25},
        "tips": [
            "Keep meal timings consistent every day.",
            "Balance macros across breakfast, lunch, and dinner.",
            "Track weekly trends instead of daily fluctuations.",
        ],
    },
    "Healthy Lifestyle": {
        "daily_calories": 2000,
        "recommended_foods": ["Quinoa", "Leafy Greens", "Berries", "Olive Oil", "Fish", "Legumes", "Nuts"],
        "avoid_foods": ["Artificial sweeteners", "High-sodium snacks", "Deep-fried foods"],
        "next_meals": {
            "high_cal": "Baked salmon with roasted vegetables",
            "balanced": "Chickpea salad with olive oil dressing",
            "low_cal": "Fruit bowl with yogurt and chia seeds",
        },
        "macros": {"Protein": 25, "Carbs": 45, "Fat": 30},
        "tips": [
            "Choose whole foods over ultra-processed options.",
            "Include probiotic foods for gut health.",
            "Aim for 30 minutes of moderate activity daily.",
        ],
    },
}


def build_ai_recommendation(goal: str, today_calories: int, latest_meal: dict | None) -> dict:
    """Rule-based dummy AI recommendation for Phase 1 prototype."""
    rec = GOAL_RECOMMENDATIONS[goal]
    target = rec["daily_calories"]
    diff = today_calories - target

    meal_name = (
        latest_meal.get("food_name") or latest_meal.get("food") or "your last meal"
    ) if latest_meal else "today's meals"
    meal_cal = latest_meal.get("calories", 0) if latest_meal else 0
    meal_carbs = latest_meal.get("carbs", 0) if latest_meal else 0

    if goal == "Weight Loss":
        if diff > 150 or meal_cal >= 400:
            main = (
                f"Your selected meal ({meal_name}) is high in carbohydrates and calories. "
                "Keep dinner lighter and add more protein-rich food."
            )
            why = (
                "Weight loss requires a moderate calorie deficit. High-carb, calorie-dense meals "
                "can push you over your daily target and slow progress."
            )
            next_meal = rec["next_meals"]["high_cal"]
        elif diff < -250:
            main = "Your intake is below target. Add a protein-rich snack to avoid undereating."
            why = "Very low intake can reduce energy and muscle retention during weight loss."
            next_meal = rec["next_meals"]["low_cal"]
        else:
            main = "Your calorie intake is slightly high today. Try a lighter dinner and add more protein."
            why = "A small adjustment at dinner can keep you within your weight-loss calorie budget."
            next_meal = rec["next_meals"]["balanced"]
    elif goal == "Weight Gain":
        if diff < -300:
            main = "You are under your calorie surplus target. Add an extra snack or larger portion at dinner."
            why = "Muscle and healthy weight gain need consistent surplus calories with adequate protein."
            next_meal = rec["next_meals"]["high_cal"]
        else:
            main = "Good progress toward your surplus. Keep protein intake steady across meals."
            why = "Balanced surplus with protein supports lean mass gain rather than fat-only gain."
            next_meal = rec["next_meals"]["balanced"]
    elif goal == "Healthy Lifestyle":
        if meal_carbs >= 50:
            main = "This meal is carb-heavy. Pair future meals with more vegetables and lean protein."
            why = "A healthy lifestyle benefits from balanced macros and micronutrient diversity."
            next_meal = rec["next_meals"]["balanced"]
        else:
            main = "Nice balance so far. Focus on whole foods, hydration, and regular activity."
            why = "Consistency in whole-food choices supports long-term metabolic health."
            next_meal = rec["next_meals"]["low_cal"]
    else:  # Maintenance
        if abs(diff) <= 200:
            main = "Your intake looks balanced today. Maintain consistent meal timings."
            why = "Staying near your maintenance calories helps stable weight and energy levels."
            next_meal = rec["next_meals"]["balanced"]
        elif diff > 200:
            main = "You are above maintenance today. Choose a lighter dinner to rebalance."
            why = "Small daily overshoots can accumulate over the week without portion awareness."
            next_meal = rec["next_meals"]["high_cal"]
        else:
            main = "You are below maintenance. A nutritious snack can help meet your energy needs."
            why = "Undereating may cause fatigue and make later overeating more likely."
            next_meal = rec["next_meals"]["low_cal"]

    return {
        "main_advice": main,
        "why": why,
        "next_meal": next_meal,
        "recommended_foods": rec["recommended_foods"],
        "avoid_foods": rec["avoid_foods"],
        "tips": rec["tips"],
        "target_calories": target,
        "today_calories": today_calories,
        "difference": diff,
    }

