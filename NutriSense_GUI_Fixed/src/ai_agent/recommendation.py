"""
src/ai_agent/recommendation.py
================================
NutriSense AI — Nutrition Coach & Recommendation Engine.

Analyses real meal data from SQLite and generates personalised advice.
No external API needed — pure logic-based intelligent recommendations.
"""

from __future__ import annotations

import datetime
import logging

logger = logging.getLogger(__name__)

# ── Nutrition targets (daily) ─────────────────────────────────────────────────
DEFAULT_PROTEIN_GOAL = 120   # grams
DEFAULT_FAT_LIMIT    = 70    # grams
DEFAULT_CARB_GOAL    = 250   # grams


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN FUNCTION — Daily Analysis
# ══════════════════════════════════════════════════════════════════════════════

def generate_daily_recommendation(user_id: int) -> dict:
    """
    Analyse today's nutrition and return structured AI advice.

    Returns
    -------
    {
        "status":              "good" | "low" | "over" | "moderate",
        "summary":             str,
        "recommendations":     list[str],
        "warnings":            list[str],
        "next_meal_suggestion": str,
        "health_tip":          str,
        "calories_consumed":   float,
        "calorie_goal":        float,
        "remaining_calories":  float,
        "goal_pct":            float,
        "protein":             float,
        "carbs":               float,
        "fat":                 float,
        "health_score":        int,
        "meals_count":         int,
    }
    """
    summary = _get_summary(user_id)

    calories    = float(summary.get("calories",      0) or 0)
    goal        = float(summary.get("calorie_goal",  2200) or 2200)
    protein     = float(summary.get("protein",       0) or 0)
    carbs       = float(summary.get("carbs",         0) or 0)
    fat         = float(summary.get("fat",           0) or 0)
    health_score= int(  summary.get("health_score",  50) or 50)
    meals_count = int(  summary.get("meals_count",   0) or 0)

    remaining   = max(goal - calories, 0)
    goal_pct    = round((calories / goal * 100) if goal > 0 else 0, 1)

    # ── Status ────────────────────────────────────────────────────────────────
    if meals_count == 0:
        status = "empty"
    elif goal_pct < 40:
        status = "low"
    elif goal_pct <= 80:
        status = "moderate"
    elif goal_pct <= 100:
        status = "good"
    else:
        status = "over"

    # ── Summary sentence ──────────────────────────────────────────────────────
    summary_text = _build_summary(status, calories, goal, goal_pct, meals_count)

    # ── Recommendations ───────────────────────────────────────────────────────
    recommendations = _build_recommendations(
        status, calories, goal, protein, carbs, fat, meals_count, health_score
    )

    # ── Warnings ──────────────────────────────────────────────────────────────
    warnings = _build_warnings(
        status, calories, goal, protein, fat, health_score
    )

    # ── Next meal suggestion ──────────────────────────────────────────────────
    next_meal = suggest_next_meal_text(remaining, protein, fat)

    # ── Health tip ────────────────────────────────────────────────────────────
    health_tip = _health_tip(health_score, protein, fat, meals_count)

    return {
        "status":               status,
        "summary":              summary_text,
        "recommendations":      recommendations,
        "warnings":             warnings,
        "next_meal_suggestion": next_meal,
        "health_tip":           health_tip,
        "calories_consumed":    calories,
        "calorie_goal":         goal,
        "remaining_calories":   remaining,
        "goal_pct":             goal_pct,
        "protein":              protein,
        "carbs":                carbs,
        "fat":                  fat,
        "health_score":         health_score,
        "meals_count":          meals_count,
    }


# ══════════════════════════════════════════════════════════════════════════════
#  MEAL SUGGESTION
# ══════════════════════════════════════════════════════════════════════════════

def suggest_next_meal(user_id: int) -> dict:
    """
    Suggest next meal based on remaining calories and macros.

    Returns
    -------
    {
        "meal_name": str,
        "reason":    str,
        "items":     list[str],
        "est_calories": int,
    }
    """
    summary   = _get_summary(user_id)
    calories  = float(summary.get("calories",     0)    or 0)
    goal      = float(summary.get("calorie_goal", 2200) or 2200)
    protein   = float(summary.get("protein",      0)    or 0)
    fat       = float(summary.get("fat",          0)    or 0)
    remaining = max(goal - calories, 0)

    return _meal_suggestion_dict(remaining, protein, fat)


def suggest_next_meal_text(remaining: float, protein: float, fat: float) -> str:
    d = _meal_suggestion_dict(remaining, protein, fat)
    items = " + ".join(d["items"])
    return f"{d['meal_name']}: {items} (~{d['est_calories']} kcal)"


# ══════════════════════════════════════════════════════════════════════════════
#  CHAT / Q&A RESPONSES
# ══════════════════════════════════════════════════════════════════════════════

def answer_user_question(question: str, user_id: int) -> str:
    """
    Answer a free-text nutrition question using local logic.
    No external API required.
    """
    q   = question.lower().strip()
    rec = generate_daily_recommendation(user_id)

    calories   = rec["calories_consumed"]
    goal       = rec["calorie_goal"]
    remaining  = rec["remaining_calories"]
    protein    = rec["protein"]
    fat        = rec["fat"]
    carbs      = rec["carbs"]
    pct        = rec["goal_pct"]
    score      = rec["health_score"]
    status     = rec["status"]
    meals      = rec["meals_count"]

    # ── Intent matching ───────────────────────────────────────────────────────
    if _match(q, ["eat next", "eat now", "should i eat", "what to eat", "meal suggest"]):
        meal = rec["next_meal_suggestion"]
        return (
            f"Based on your current intake of **{calories:.0f} kcal** "
            f"(remaining: **{remaining:.0f} kcal**), I suggest:\n\n"
            f"🍽️ **{meal}**\n\n"
            f"{rec['health_tip']}"
        )

    if _match(q, ["diet today", "how am i doing", "my diet", "today diet", "my intake"]):
        return (
            f"Here's your nutrition snapshot for today:\n\n"
            f"🔥 **Calories:** {calories:.0f} / {goal:.0f} kcal ({pct}%)\n"
            f"🥩 **Protein:** {protein:.1f}g\n"
            f"🍞 **Carbs:** {carbs:.1f}g\n"
            f"🧈 **Fat:** {fat:.1f}g\n"
            f"💚 **Health Score:** {score}/100\n\n"
            f"{rec['summary']}"
        )

    if _match(q, ["improve", "health score", "better", "healthier"]):
        tips = [
            "✅ Eat more vegetables and lean proteins (chicken, lentils, eggs).",
            "✅ Reduce fried and oily foods to lower saturated fat.",
            "✅ Stay hydrated — drink 8 glasses of water daily.",
            "✅ Log all meals to keep your health score accurate.",
            "✅ Aim for 3 balanced meals + 1 healthy snack per day.",
        ]
        if fat > DEFAULT_FAT_LIMIT:
            tips.insert(0, f"⚠️ Your fat intake ({fat:.1f}g) is high — cut oily foods first.")
        if protein < DEFAULT_PROTEIN_GOAL * 0.5:
            tips.insert(0, f"⚠️ Protein is low ({protein:.1f}g) — add eggs, chicken, or lentils.")
        return "Here's how to improve your health score:\n\n" + "\n".join(tips)

    if _match(q, ["calorie", "calories", "how many"]):
        return (
            f"🔥 You have consumed **{calories:.0f} kcal** out of your **{goal:.0f} kcal** goal.\n"
            f"Remaining: **{remaining:.0f} kcal** ({100 - pct:.1f}% left).\n\n"
            + ("You're on track! Keep going. 💪" if status in ("good", "moderate")
               else "Try to reach your calorie goal with balanced meals." if status == "low"
               else "⚠️ You've exceeded your daily limit. Choose light foods.")
        )

    if _match(q, ["protein"]):
        status_p = "good ✅" if protein >= DEFAULT_PROTEIN_GOAL * 0.7 else "low ⚠️"
        return (
            f"🥩 Your protein intake today: **{protein:.1f}g** (target: {DEFAULT_PROTEIN_GOAL}g) — {status_p}\n\n"
            + ("Great job! Protein helps muscle repair and keeps you full."
               if protein >= DEFAULT_PROTEIN_GOAL * 0.7
               else "Add chicken breast, eggs, lentils (daal), or Greek yoghurt to boost protein.")
        )

    if _match(q, ["fat", "oily", "oil"]):
        status_f = "high ⚠️" if fat > DEFAULT_FAT_LIMIT else "within range ✅"
        return (
            f"🧈 Your fat intake today: **{fat:.1f}g** (limit: {DEFAULT_FAT_LIMIT}g) — {status_f}\n\n"
            + ("Try to avoid fried foods, ghee, and heavy curries for the rest of the day."
               if fat > DEFAULT_FAT_LIMIT
               else "Good control! Keep choosing grilled or baked options.")
        )

    if _match(q, ["meal", "how many meal", "meals logged", "log"]):
        return (
            f"📋 You have logged **{meals} meal(s)** today.\n\n"
            + ("Scan your first meal to get personalised recommendations! 📸"
               if meals == 0
               else "Keep logging meals for better AI insights throughout the day.")
        )

    if _match(q, ["weight", "lose", "gain"]):
        if status == "over":
            return (
                "⚠️ You've exceeded your calorie goal today. To manage weight:\n\n"
                "- Choose high-fibre, low-calorie foods (salads, fruits, soups).\n"
                "- Avoid sugary drinks and processed snacks.\n"
                "- Consider a 30-minute walk after meals."
            )
        elif status == "low":
            return (
                "Your calorie intake is low today. If you want to gain or maintain weight:\n\n"
                "- Add calorie-dense healthy foods (nuts, whole grains, lean meats).\n"
                "- Try not to skip meals — consistency matters more than perfection."
            )
        else:
            return (
                "You're on a healthy track! For weight management:\n\n"
                "- Keep your calorie intake consistent.\n"
                "- Balance protein, carbs, and fats at every meal.\n"
                "- Stay active and hydrated."
            )

    # ── Default fallback ──────────────────────────────────────────────────────
    return (
        f"I'm your NutriSense AI Coach 🥗\n\n"
        f"Today: **{calories:.0f}/{goal:.0f} kcal** · "
        f"Protein **{protein:.0f}g** · Score **{score}/100**\n\n"
        f"{rec['summary']}\n\n"
        f"Try asking me:\n"
        f"- *What should I eat next?*\n"
        f"- *How is my diet today?*\n"
        f"- *How can I improve my health score?*"
    )


# ══════════════════════════════════════════════════════════════════════════════
#  INTERNAL HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def _get_summary(user_id: int) -> dict:
    try:
        from src.database.meals import get_today_summary
        return get_today_summary(user_id) or {}
    except Exception as e:
        logger.error(f"Could not fetch summary: {e}")
        return {}


def _build_summary(status, calories, goal, pct, meals_count) -> str:
    if status == "empty":
        return "No meals logged today. Scan your first meal to get personalised recommendations."
    if status == "low":
        return (
            f"Your intake is only {pct}% of your daily goal ({calories:.0f}/{goal:.0f} kcal). "
            "Add balanced protein-rich meals to reach your target."
        )
    if status == "moderate":
        return (
            f"You've consumed {pct}% of your daily goal ({calories:.0f}/{goal:.0f} kcal). "
            "Good progress — keep logging meals throughout the day."
        )
    if status == "good":
        return (
            f"You're close to your goal at {pct}% ({calories:.0f}/{goal:.0f} kcal). "
            "Choose lighter, nutrient-dense options for remaining meals."
        )
    if status == "over":
        over = calories - goal
        return (
            f"You've exceeded your calorie goal by {over:.0f} kcal ({calories:.0f}/{goal:.0f}). "
            "Prefer low-calorie foods like fruits, salads, or soups for the rest of the day."
        )
    return f"You've consumed {calories:.0f} kcal today across {meals_count} meal(s)."


def _build_recommendations(status, calories, goal, protein, carbs, fat, meals, score) -> list[str]:
    recs = []

    # Calorie-based
    if status == "empty":
        recs.append("📸 Scan your first meal to unlock AI-powered nutrition tracking.")
    elif status == "low":
        recs.append("🍽️ Add 2 more balanced meals to reach your calorie target.")
        recs.append("🥗 Include complex carbs like rice, roti, or whole grain bread.")
    elif status == "over":
        recs.append("🥬 Switch to salads, soups, or fruits for your next meal.")
        recs.append("🚫 Avoid fried foods, sugary drinks, and heavy curries.")

    # Protein
    if protein < DEFAULT_PROTEIN_GOAL * 0.5 and status != "empty":
        recs.append(f"🥩 Protein is low ({protein:.0f}g). Add chicken, eggs, lentils, or yoghurt.")
    elif protein >= DEFAULT_PROTEIN_GOAL:
        recs.append(f"✅ Great protein intake ({protein:.0f}g)! Muscles are well fuelled.")

    # Fat
    if fat > DEFAULT_FAT_LIMIT:
        recs.append(f"⚠️ Fat intake ({fat:.0f}g) is above limit ({DEFAULT_FAT_LIMIT}g). Avoid oily/fried foods.")

    # Health score
    if score < 60:
        recs.append("💚 Improve health score by eating more vegetables and reducing processed food.")
    elif score >= 85:
        recs.append("🌟 Excellent health score! Keep up your balanced diet.")

    # Meals frequency
    hour = datetime.datetime.now().hour
    if meals < 2 and hour >= 14:
        recs.append("⏰ It's afternoon — make sure to log your lunch if you've eaten.")

    return recs if recs else ["✅ Everything looks balanced today. Keep it up!"]


def _build_warnings(status, calories, goal, protein, fat, score) -> list[str]:
    warnings = []
    if status == "over":
        warnings.append(f"🚨 Calorie limit exceeded by {calories - goal:.0f} kcal.")
    if fat > DEFAULT_FAT_LIMIT * 1.3:
        warnings.append(f"🚨 Fat intake is very high ({fat:.0f}g). Risk of unhealthy weight gain.")
    if protein < DEFAULT_PROTEIN_GOAL * 0.3 and status not in ("empty",):
        warnings.append(f"⚠️ Very low protein ({protein:.0f}g). Risk of muscle loss and fatigue.")
    if score < 40:
        warnings.append("⚠️ Health score is critically low. Focus on whole, unprocessed foods.")
    return warnings


def _health_tip(score, protein, fat, meals) -> str:
    if meals == 0:
        return "💡 Tip: Log your first meal and I'll give you personalised health advice!"
    if fat > DEFAULT_FAT_LIMIT:
        return "💡 Tip: Replace fried foods with grilled or baked alternatives to reduce fat."
    if protein < DEFAULT_PROTEIN_GOAL * 0.5:
        return "💡 Tip: Start your day with a protein-rich breakfast (eggs, yoghurt, or daal)."
    if score >= 80:
        return "💡 Tip: You're doing great! Drink plenty of water and stay consistent."
    tips = [
        "💡 Tip: Eat slowly and mindfully — it helps digestion and prevents overeating.",
        "💡 Tip: Add a handful of vegetables to every meal to boost fibre and vitamins.",
        "💡 Tip: A short walk after meals helps regulate blood sugar.",
        "💡 Tip: Sleep 7-8 hours — poor sleep increases hunger hormones.",
    ]
    import random
    return random.choice(tips)


def _meal_suggestion_dict(remaining: float, protein: float, fat: float) -> dict:
    protein_low = protein < DEFAULT_PROTEIN_GOAL * 0.5
    fat_high    = fat > DEFAULT_FAT_LIMIT

    if remaining > 700:
        if protein_low:
            return {
                "meal_name":    "High-Protein Balanced Meal",
                "reason":       "Large calorie budget + low protein",
                "items":        ["Grilled Chicken", "Brown Rice", "Steamed Vegetables", "Daal"],
                "est_calories": 650,
            }
        return {
            "meal_name":    "Full Balanced Meal",
            "reason":       "Large remaining calorie budget",
            "items":        ["Chicken Karahi / Daal", "Roti / Rice", "Salad", "Yoghurt"],
            "est_calories": 600,
        }

    elif 300 <= remaining <= 700:
        if fat_high:
            return {
                "meal_name":    "Light Low-Fat Meal",
                "reason":       "Moderate budget + high fat already consumed",
                "items":        ["Grilled Fish", "Salad", "Whole Wheat Roti"],
                "est_calories": 380,
            }
        if protein_low:
            return {
                "meal_name":    "Protein Snack Meal",
                "reason":       "Moderate budget + low protein",
                "items":        ["Boiled Eggs (x2)", "Greek Yoghurt", "Whole Grain Toast"],
                "est_calories": 350,
            }
        return {
            "meal_name":    "Light Balanced Meal",
            "reason":       "Moderate remaining calories",
            "items":        ["Vegetable Soup", "Whole Wheat Roti", "Yoghurt"],
            "est_calories": 320,
        }

    else:  # remaining < 300
        return {
            "meal_name":    "Very Light Snack",
            "reason":       "Low remaining calories",
            "items":        ["Fresh Fruit (Apple/Banana)", "Handful of Nuts", "Green Tea"],
            "est_calories": 180,
        }


def _match(query: str, keywords: list[str]) -> bool:
    return any(kw in query for kw in keywords)