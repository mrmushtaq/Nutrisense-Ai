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

SHARED_CSS = """
<style>
/* ── Import Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ── Global ── */
*, *::before, *::after { box-sizing: border-box; }
html, body, [data-testid="stAppViewContainer"] {
    background: #0a0e1a !important;
    font-family: 'Inter', 'Segoe UI', sans-serif;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1220 0%, #111827 100%) !important;
    border-right: 1px solid #1e2a3a !important;
}
[data-testid="stSidebar"] * { font-family: 'Inter', sans-serif; }
[data-testid="stHeader"] { background: transparent !important; }

/* Hide Streamlit default sidebar page list — we use top horizontal navbar */
[data-testid="stSidebarNav"] { display: none !important; }
[data-testid="stSidebarNav"] + div { display: none !important; }

/* ── Top horizontal navbar ── */
.top-nav-marker { display: none; }
.top-nav-marker + div [data-testid="stHorizontalBlock"] {
    background: linear-gradient(135deg, #0d1e2e 0%, #111827 100%);
    border: 1px solid #1e2a3a;
    border-radius: 14px;
    padding: 10px 14px 6px 14px;
    margin-bottom: 18px;
}
.top-nav-brand {
    font-size: 1.05rem;
    font-weight: 800;
    color: #1de9b6;
    margin: 10px 0 0 4px;
    letter-spacing: -0.01em;
}
.top-nav-phase {
    font-size: 0.68rem;
    color: #4a7c9e;
    text-align: right;
    margin-top: 12px;
    padding-right: 4px;
}
.nav-pill-active {
    background: linear-gradient(135deg, #1de9b633, #0288d122);
    border: 1px solid #1de9b655;
    border-radius: 10px;
    color: #1de9b6 !important;
    font-weight: 700;
    text-align: center;
    padding: 9px 6px;
    font-size: 0.78rem;
    margin-top: 2px;
}
div[data-testid="column"] a[data-testid="stPageLink-Nav"],
div[data-testid="column"] .stPageLink a {
    display: block;
    text-align: center;
    background: #0a0e1a;
    border: 1px solid #1e2a3a;
    border-radius: 10px;
    color: #8ba8c4 !important;
    font-weight: 600;
    font-size: 0.78rem;
    padding: 9px 6px;
    text-decoration: none !important;
    transition: all 0.2s;
}
div[data-testid="column"] a[data-testid="stPageLink-Nav"]:hover,
div[data-testid="column"] .stPageLink a:hover {
    border-color: #1de9b644;
    color: #1de9b6 !important;
    background: #111827;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a0e1a; }
::-webkit-scrollbar-thumb { background: #1e2a3a; border-radius: 3px; }

/* ── Sidebar brand ── */
.sb-brand {
    text-align: center;
    padding: 24px 12px 18px;
}
.sb-logo-ring {
    width: 64px; height: 64px;
    background: linear-gradient(135deg, #1de9b622, #0288d122);
    border: 2px solid #1de9b644;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 12px;
    font-size: 2rem;
}
.sb-title {
    font-size: 1.15rem;
    font-weight: 800;
    background: linear-gradient(90deg, #1de9b6, #0288d1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.01em;
}
.sb-sub {
    font-size: 0.7rem;
    color: #4a7c9e;
    margin-top: 3px;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
.sb-divider {
    border: none;
    border-top: 1px solid #1e2a3a;
    margin: 14px 0;
}

/* ── Nav link buttons ── */
.sb-nav-label {
    font-size: 0.68rem;
    font-weight: 700;
    color: #4a7c9e;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 0 4px;
    margin-bottom: 6px;
}
.sb-step {
    display: flex;
    align-items: center;
    gap: 10px;
    background: #111827;
    border: 1px solid #1e2a3a;
    border-radius: 10px;
    padding: 9px 12px;
    margin-bottom: 5px;
    cursor: pointer;
    transition: all 0.2s;
}
.sb-step:hover { background: #1a2535; border-color: #1de9b644; }
.sb-step-icon { font-size: 1.1rem; flex-shrink: 0; }
.sb-step-text { flex: 1; }
.sb-step-name {
    font-size: 0.82rem;
    font-weight: 600;
    color: #d1e0f0;
}
.sb-step-hint {
    font-size: 0.68rem;
    color: #4a7c9e;
    margin-top: 1px;
}

/* ── Page header ── */
.ns-hero {
    background: linear-gradient(135deg, #0d1e2e 0%, #0a1628 60%, #0d1e38 100%);
    border: 1px solid #1e2a3a;
    border-radius: 18px;
    padding: 28px 32px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.ns-hero::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 180px; height: 180px;
    background: radial-gradient(circle, #1de9b611 0%, transparent 70%);
    border-radius: 50%;
}
.ns-hero-eyebrow {
    font-size: 0.7rem;
    font-weight: 700;
    color: #1de9b6;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.ns-hero-title {
    font-size: 2rem;
    font-weight: 800;
    color: #e8f4ff;
    letter-spacing: -0.02em;
    line-height: 1.1;
}
.ns-hero-sub {
    color: #6b8ca8;
    font-size: 0.92rem;
    margin-top: 6px;
    line-height: 1.5;
}

/* ── KPI Cards ── */
.kpi-card {
    background: linear-gradient(145deg, #111827 0%, #0d1522 100%);
    border: 1px solid #1e2a3a;
    border-radius: 16px;
    padding: 20px;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s, border-color 0.2s;
}
.kpi-card:hover { transform: translateY(-2px); border-color: #2a3f55; }
.kpi-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 16px 16px 0 0;
}
.kpi-teal::after   { background: linear-gradient(90deg, #1de9b6, #0288d1); }
.kpi-blue::after   { background: linear-gradient(90deg, #4a9eff, #7c5cfc); }
.kpi-purple::after { background: linear-gradient(90deg, #a78bfa, #ec4899); }
.kpi-orange::after { background: linear-gradient(90deg, #f5a623, #ff6b6b); }
.kpi-label {
    font-size: 0.7rem;
    font-weight: 700;
    color: #4a7c9e;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.kpi-value {
    font-size: 1.9rem;
    font-weight: 800;
    color: #e8f4ff;
    letter-spacing: -0.02em;
    line-height: 1;
}
.kpi-sub {
    font-size: 0.75rem;
    color: #4a7c9e;
    margin-top: 6px;
}
.kpi-icon {
    position: absolute;
    top: 16px; right: 16px;
    font-size: 1.6rem;
    opacity: 0.18;
}

/* ── Section headers ── */
.section-head {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 28px 0 16px;
}
.section-head-icon {
    width: 34px; height: 34px;
    background: linear-gradient(135deg, #1de9b622, #0288d122);
    border: 1px solid #1de9b633;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
    flex-shrink: 0;
}
.section-head-text {
    font-size: 1.05rem;
    font-weight: 700;
    color: #d1e0f0;
    letter-spacing: -0.01em;
}
.section-head-badge {
    font-size: 0.65rem;
    font-weight: 700;
    background: #1de9b622;
    color: #1de9b6;
    border: 1px solid #1de9b633;
    border-radius: 20px;
    padding: 2px 10px;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

/* ── Content cards ── */
.ns-card {
    background: linear-gradient(145deg, #111827 0%, #0d1522 100%);
    border: 1px solid #1e2a3a;
    border-radius: 14px;
    padding: 18px 20px;
    margin-bottom: 10px;
}
.ns-card-accent-teal   { border-left: 3px solid #1de9b6; }
.ns-card-accent-blue   { border-left: 3px solid #4a9eff; }
.ns-card-accent-purple { border-left: 3px solid #a78bfa; }
.ns-card-accent-orange { border-left: 3px solid #f5a623; }

/* ── Inline info / alert boxes ── */
.ns-info {
    background: #0a1e38;
    border: 1px solid #1de9b633;
    border-radius: 12px;
    padding: 14px 18px;
    color: #7dd3fc;
    font-size: 0.88rem;
    margin: 10px 0;
    display: flex; gap: 10px; align-items: flex-start;
}
.ns-success {
    background: #071e16;
    border: 1px solid #1de9b644;
    border-radius: 12px;
    padding: 14px 18px;
    color: #6ee7b7;
    font-size: 0.88rem;
    margin: 10px 0;
    display: flex; gap: 10px; align-items: flex-start;
}
.ns-warn {
    background: #1e1200;
    border: 1px solid #f5a62344;
    border-radius: 12px;
    padding: 14px 18px;
    color: #fcd34d;
    font-size: 0.88rem;
    margin: 10px 0;
    display: flex; gap: 10px; align-items: flex-start;
}
.ns-error {
    background: #1e0808;
    border: 1px solid #ff6b6b44;
    border-radius: 12px;
    padding: 14px 18px;
    color: #fca5a5;
    font-size: 0.88rem;
    margin: 10px 0;
    display: flex; gap: 10px; align-items: flex-start;
}
.ns-info-icon, .ns-success-icon, .ns-warn-icon, .ns-error-icon {
    font-size: 1.1rem; flex-shrink: 0; margin-top: 1px;
}

/* ── Health score badge ── */
.hs-badge {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 6px 16px;
    border-radius: 30px;
    font-weight: 700;
    font-size: 0.88rem;
    letter-spacing: 0.02em;
}
.hs-high   { background: #071e16; color: #1de9b6; border: 1px solid #1de9b644; }
.hs-medium { background: #1e1200; color: #f5a623; border: 1px solid #f5a62344; }
.hs-low    { background: #1e0808; color: #ff6b6b; border: 1px solid #ff6b6b44; }

/* ── Food result pill ── */
.food-result-card {
    background: linear-gradient(135deg, #071e16 0%, #0a1628 100%);
    border: 1px solid #1de9b633;
    border-radius: 16px;
    padding: 20px 24px;
    margin-bottom: 18px;
}
.food-result-name {
    font-size: 1.7rem;
    font-weight: 800;
    color: #e8f4ff;
    letter-spacing: -0.02em;
}
.food-result-meta {
    font-size: 0.8rem;
    color: #4a7c9e;
    margin-top: 4px;
}
.food-result-meta strong { color: #1de9b6; }

/* ── Macro mini-cards ── */
.macro-card {
    background: #111827;
    border: 1px solid #1e2a3a;
    border-radius: 12px;
    padding: 14px 16px;
    text-align: center;
}
.macro-card-val {
    font-size: 1.5rem;
    font-weight: 800;
    line-height: 1;
    letter-spacing: -0.02em;
}
.macro-card-unit {
    font-size: 0.75rem;
    opacity: 0.7;
    font-weight: 500;
    margin-left: 2px;
}
.macro-card-label {
    font-size: 0.7rem;
    font-weight: 700;
    color: #4a7c9e;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    margin-top: 4px;
}

/* ── Step guide (how-to) ── */
.step-row {
    display: flex; align-items: flex-start; gap: 16px;
    background: #111827;
    border: 1px solid #1e2a3a;
    border-radius: 12px;
    padding: 14px 16px;
    margin-bottom: 8px;
}
.step-num {
    width: 28px; height: 28px;
    background: linear-gradient(135deg, #1de9b6, #0288d1);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.78rem;
    font-weight: 800;
    color: #0a0e1a;
    flex-shrink: 0;
    margin-top: 1px;
}
.step-content {}
.step-title { font-size: 0.88rem; font-weight: 700; color: #d1e0f0; }
.step-desc  { font-size: 0.78rem; color: #4a7c9e; margin-top: 2px; line-height: 1.4; }

/* ── Meal list item ── */
.meal-item {
    display: flex; justify-content: space-between; align-items: center;
    background: #111827;
    border: 1px solid #1e2a3a;
    border-radius: 12px;
    padding: 12px 16px;
    margin-bottom: 7px;
    transition: border-color 0.2s;
}
.meal-item:hover { border-color: #2a3f55; }
.meal-item-left {}
.meal-item-name { font-size: 0.92rem; font-weight: 600; color: #d1e0f0; }
.meal-item-meta { font-size: 0.72rem; color: #4a7c9e; margin-top: 2px; }
.meal-item-right { text-align: right; }
.meal-item-cal   { font-size: 1rem; font-weight: 700; color: #1de9b6; }
.meal-item-type  { font-size: 0.68rem; color: #4a7c9e; margin-top: 2px; }

/* ── Progress bar (custom) ── */
.ns-progress-wrap {
    background: #1e2a3a;
    border-radius: 30px;
    height: 14px;
    overflow: hidden;
    margin: 6px 0 4px;
}
.ns-progress-fill {
    height: 100%;
    border-radius: 30px;
    transition: width 0.6s ease;
}

/* ── Food tag chips ── */
.tag-good {
    display: inline-block;
    background: #071e16;
    color: #1de9b6;
    border: 1px solid #1de9b633;
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.75rem;
    font-weight: 600;
    margin: 3px;
}
.tag-bad {
    display: inline-block;
    background: #1e0808;
    color: #ff6b6b;
    border: 1px solid #ff6b6b33;
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.75rem;
    font-weight: 600;
    margin: 3px;
}

/* ── Phase badge ── */
.phase-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: #1e1200;
    border: 1px solid #f5a62344;
    border-radius: 20px;
    padding: 5px 14px;
    font-size: 0.72rem;
    font-weight: 700;
    color: #fcd34d;
    letter-spacing: 0.05em;
}

/* ── Divider ── */
.ns-divider { border: none; border-top: 1px solid #1e2a3a; margin: 24px 0; }

/* ── Empty state ── */
.empty-state {
    text-align: center;
    padding: 60px 20px;
    background: #111827;
    border: 1px dashed #1e2a3a;
    border-radius: 16px;
}
.empty-state-icon { font-size: 3.5rem; margin-bottom: 14px; }
.empty-state-title { font-size: 1.1rem; font-weight: 700; color: #d1e0f0; margin-bottom: 6px; }
.empty-state-desc  { font-size: 0.85rem; color: #4a7c9e; line-height: 1.6; }

/* ── Streamlit overrides ── */
div[data-testid="stButton"] > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.2s !important;
}
div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #1de9b6, #0288d1) !important;
    border: none !important;
    color: #0a0e1a !important;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px #1de9b644 !important;
}
.stProgress > div > div > div {
    background: linear-gradient(90deg, #1de9b6, #0288d1) !important;
    border-radius: 30px !important;
}
.stProgress > div > div {
    background: #1e2a3a !important;
    border-radius: 30px !important;
}
div[data-testid="stSelectbox"] label,
div[data-testid="stRadio"] label,
div[data-testid="stSlider"] label { color: #8ba8c4 !important; font-size: 0.85rem !important; }
</style>
"""

def inject_css(st):
    st.markdown(SHARED_CSS, unsafe_allow_html=True)


def sidebar_brand(st):
    st.sidebar.markdown(
        """
        <div class="sb-brand">
            <div class="sb-logo-ring">🥗</div>
            <div class="sb-title">NutriSense AI</div>
            <div class="sb-sub">Food Intelligence System</div>
        </div>
        <hr class="sb-divider">
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.markdown('<hr class="sb-divider">', unsafe_allow_html=True)
    st.sidebar.markdown("**🤖 AI Agent** · Phase II")
    st.sidebar.caption("Use the top navigation bar to switch pages.")

    st.sidebar.markdown(
        """
        <div style="padding: 8px 4px 4px;">
            <div class="phase-badge">✅ Phase II: SQLite Database Active</div>
        </div>
        <div class="sb-nav-label" style="margin-top:14px">Navigation Guide</div>
        <div style="color:#6b8ca8;font-size:0.75rem;line-height:1.6;padding:0 4px 10px;">
            1. Upload a food image<br>
            2. Analyze and save result<br>
            3. Review nutrition breakdown<br>
            4. Track calories & history<br>
            5. Get AI recommendations
        </div>
        <div class="sb-nav-label">Future Modules</div>
        <div style="padding:0 4px;">
            <div class="sb-step" style="cursor:default;margin-bottom:4px;">
                <div class="sb-step-icon">🧠</div>
                <div class="sb-step-text">
                    <div class="sb-step-name">EfficientNetB0 Model</div>
                    <div class="sb-step-hint">Phase III — Food recognition</div>
                </div>
            </div>
            <div class="sb-step" style="cursor:default;margin-bottom:4px;">
                <div class="sb-step-icon">📦</div>
                <div class="sb-step-text">
                    <div class="sb-step-name">Food-101 Dataset</div>
                    <div class="sb-step-hint">Training data source</div>
                </div>
            </div>
            <div class="sb-step" style="cursor:default;margin-bottom:4px;">
                <div class="sb-step-icon">🇵🇰</div>
                <div class="sb-step-text">
                    <div class="sb-step-name">Pakistani Food Dataset</div>
                    <div class="sb-step-hint">Local cuisine extension</div>
                </div>
            </div>
            <div class="sb-step" style="cursor:default;margin-bottom:4px;border-color:#1de9b644;">
                <div class="sb-step-icon">🗄️</div>
                <div class="sb-step-text">
                    <div class="sb-step-name">SQLite Database</div>
                    <div class="sb-step-hint" style="color:#1de9b6">✅ Active — meal storage</div>
                </div>
            </div>
            <div class="sb-step" style="cursor:default;">
                <div class="sb-step-icon">🤖</div>
                <div class="sb-step-text">
                    <div class="sb-step-name">Goal-Based AI Agent</div>
                    <div class="sb-step-hint">Personalized coaching</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def health_score_html(score: int) -> str:
    if score >= HEALTH_SCORE_HIGH:
        cls, icon, label = "hs-high",   "🟢", "Excellent"
    elif score >= HEALTH_SCORE_MEDIUM:
        cls, icon, label = "hs-medium", "🟡", "Moderate"
    else:
        cls, icon, label = "hs-low",    "🔴", "Needs Work"
    return (
        f'<span class="hs-badge {cls}">'
        f'{icon} Health Score: <strong>{score}/100</strong> — {label}'
        f'</span>'
    )

def plotly_dark_layout() -> dict:
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#111827",
        font=dict(color="#6b8ca8", family="Inter, Segoe UI"),
        margin=dict(l=16, r=16, t=36, b=16),
        xaxis=dict(gridcolor="#1e2a3a", linecolor="#1e2a3a", tickfont=dict(color="#6b8ca8")),
        yaxis=dict(gridcolor="#1e2a3a", linecolor="#1e2a3a", tickfont=dict(color="#6b8ca8")),
    )