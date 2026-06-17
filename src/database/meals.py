"""
Meal CRUD operations for NutriSense AI.
Stores analyzed food records permanently in SQLite.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from src.database.connection import execute_query, fetch_all, fetch_one
from src.database.user import get_default_user


def _resolve_user_id(user_id: int | None) -> int:
    """Use provided user_id or fall back to the default demo user."""
    if user_id is not None:
        return user_id
    return get_default_user()["id"]


def add_meal(
    user_id: int,
    food_name: str,
    meal_type: str,
    calories: float,
    protein: float,
    carbs: float,
    fat: float,
    confidence: float,
    health_score: int,
    image_name: str | None = None,
    notes: str | None = None,
) -> int:
    """Insert a new analyzed meal and return its database id."""
    return execute_query(
        """
        INSERT INTO meals (
            user_id, food_name, meal_type, calories, protein, carbs, fat,
            confidence, health_score, image_name, analysis_date, notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            food_name,
            meal_type,
            calories,
            protein,
            carbs,
            fat,
            confidence,
            health_score,
            image_name,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            notes,
        ),
    )


def get_all_meals(user_id: int | None = None) -> list[dict[str, Any]]:
    """Return all meals for a user, newest first."""
    uid = _resolve_user_id(user_id)
    return fetch_all(
        """
        SELECT *
        FROM meals
        WHERE user_id = ?
        ORDER BY analysis_date DESC, id DESC
        """,
        (uid,),
    )


def get_recent_meals(limit: int = 5, user_id: int | None = None) -> list[dict[str, Any]]:
    """Return the most recent meals for dashboard preview."""
    uid = _resolve_user_id(user_id)
    return fetch_all(
        """
        SELECT *
        FROM meals
        WHERE user_id = ?
        ORDER BY analysis_date DESC, id DESC
        LIMIT ?
        """,
        (uid, limit),
    )


def get_today_meals(user_id: int | None = None) -> list[dict[str, Any]]:
    """Return meals logged today for daily calorie tracking."""
    uid = _resolve_user_id(user_id)
    today = datetime.now().strftime("%Y-%m-%d")
    return fetch_all(
        """
        SELECT *
        FROM meals
        WHERE user_id = ?
          AND DATE(analysis_date) = DATE(?)
        ORDER BY analysis_date ASC, id ASC
        """,
        (uid, today),
    )


def get_total_calories_today(user_id: int | None = None) -> float:
    """Sum calories consumed today."""
    meals = get_today_meals(user_id)
    return float(sum(m.get("calories", 0) or 0 for m in meals))


def get_meal_summary(user_id: int | None = None) -> dict[str, Any]:
    """Aggregate meal statistics for summary cards."""
    uid = _resolve_user_id(user_id)
    row = fetch_one(
        """
        SELECT
            COUNT(*) AS total_meals,
            COALESCE(SUM(calories), 0) AS total_calories,
            COALESCE(AVG(calories), 0) AS avg_calories,
            COALESCE(AVG(health_score), 0) AS avg_health_score
        FROM meals
        WHERE user_id = ?
        """,
        (uid,),
    )
    if not row:
        return {
            "total_meals": 0,
            "total_calories": 0,
            "avg_calories": 0,
            "avg_health_score": 0,
        }
    return {
        "total_meals": int(row["total_meals"]),
        "total_calories": round(float(row["total_calories"]), 1),
        "avg_calories": round(float(row["avg_calories"]), 1),
        "avg_health_score": round(float(row["avg_health_score"]), 1),
    }


def get_latest_meal(user_id: int | None = None) -> dict[str, Any] | None:
    """Return the single most recent meal record."""
    recent = get_recent_meals(limit=1, user_id=user_id)
    return recent[0] if recent else None


def clear_meal_history(user_id: int | None = None) -> int:
    """Delete all meal records for the user. Returns number of rows removed."""
    uid = _resolve_user_id(user_id)
    return execute_query("DELETE FROM meals WHERE user_id = ?", (uid,))


# ---------------------------------------------------------------------------
# Additional helpers for dashboard pages
# ---------------------------------------------------------------------------

def get_meals_by_date(date: str = "today", user_id: int | None = None) -> list[dict[str, Any]]:
    """Return meals for a given date ('today' or 'YYYY-MM-DD')."""
    if date == "today":
        return get_today_meals(user_id)

    uid = _resolve_user_id(user_id)
    return fetch_all(
        """
        SELECT *
        FROM meals
        WHERE user_id = ?
          AND DATE(analysis_date) = DATE(?)
        ORDER BY analysis_date ASC, id ASC
        """,
        (uid, date),
    )


def get_meals_by_date_range(start_date, end_date, user_id: int | None = None) -> list[dict[str, Any]]:
    """Return meals between start_date and end_date (inclusive), newest first."""
    uid = _resolve_user_id(user_id)
    return fetch_all(
        """
        SELECT *
        FROM meals
        WHERE user_id = ?
          AND DATE(analysis_date) BETWEEN DATE(?) AND DATE(?)
        ORDER BY analysis_date DESC, id DESC
        """,
        (uid, str(start_date), str(end_date)),
    )


def delete_meal(meal_id: int) -> int:
    """Delete a single meal by id. Returns number of rows removed."""
    return execute_query("DELETE FROM meals WHERE id = ?", (meal_id,))


def log_meal(
    food_name: str,
    nutrition: dict[str, Any],
    user_id: int | None = None,
    confidence: float = 96.0,
    meal_type: str = "Lunch",
    health_score: int = 75,
) -> int:
    """Insert a meal using nutrition lookup data and prediction metadata."""
    uid = _resolve_user_id(user_id)
    return add_meal(
        user_id=uid,
        food_name=food_name,
        meal_type=nutrition.get("meal_type") or meal_type,
        calories=float(nutrition.get("calories", 0) or 0),
        protein=float(nutrition.get("protein", 0) or 0),
        carbs=float(nutrition.get("carbs", 0) or 0),
        fat=float(nutrition.get("fat", 0) or 0),
        confidence=float(confidence),
        health_score=int(health_score),
    )


def _resolve_calorie_goal(user_id: int | None, calorie_goal: int | None) -> int:
    if calorie_goal is not None:
        return calorie_goal
    from config import DAILY_CALORIE_GOAL
    from src.database.user import get_user_profile

    profile = get_user_profile()
    return int(
        profile.get("daily_calorie_goal")
        or profile.get("target_calories")
        or DAILY_CALORIE_GOAL
    )


def get_today_summary(user_id: int | None = None, calorie_goal: int | None = None) -> dict[str, Any]:
    """Aggregate today's nutrition data for dashboard display."""
    uid = _resolve_user_id(user_id)
    calorie_goal = _resolve_calorie_goal(uid, calorie_goal)
    today_meals = get_today_meals(uid)

    calories = sum(m.get("calories", 0) or 0 for m in today_meals)
    protein = sum(m.get("protein", 0) or 0 for m in today_meals)
    carbs = sum(m.get("carbs", 0) or 0 for m in today_meals)
    fat = sum(m.get("fat", 0) or 0 for m in today_meals)

    goal_progress = round((calories / calorie_goal) * 100) if calorie_goal else 0
    goal_progress = max(0, min(goal_progress, 999))

    health_scores = [m.get("health_score") for m in today_meals if m.get("health_score") is not None]
    health_score = round(sum(health_scores) / len(health_scores)) if health_scores else 75

    weekly_labels: list[str] = []
    weekly_calories: list[float] = []
    for i in range(6, -1, -1):
        day = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        day_meals = fetch_all(
            """
            SELECT COALESCE(SUM(calories), 0) AS total
            FROM meals
            WHERE user_id = ? AND DATE(analysis_date) = DATE(?)
            """,
            (uid, day),
        )
        total = float(day_meals[0]["total"]) if day_meals else 0.0
        weekly_labels.append((datetime.now() - timedelta(days=i)).strftime("%a"))
        weekly_calories.append(total)

    return {
        "calories": int(calories),
        "calorie_goal": int(calorie_goal),
        "meals_count": len(today_meals),
        "goal_progress": goal_progress,
        "health_score": health_score,
        "protein": round(protein, 1),
        "carbs": round(carbs, 1),
        "fat": round(fat, 1),
        "weekly_labels": weekly_labels,
        "weekly_calories": weekly_calories,
        "macro_breakdown": {
            "Protein": round(protein, 1),
            "Carbs": round(carbs, 1),
            "Fat": round(fat, 1),
        },
    }