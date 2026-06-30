"""
Analytics and history queries for NutriSense AI dashboards.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from src.database.connection import fetch_all, fetch_one
from src.database.user import get_default_user


def _resolve_user_id(user_id: int | None) -> int:
    if user_id is not None:
        return user_id
    return get_default_user()["id"]


def get_weekly_calories(user_id: int | None = None) -> dict[str, int]:
    """
    Return calorie totals for the last 7 days keyed by weekday abbreviation.
    Falls back to dummy weekly data when no meals exist in the database.
    """
    uid = _resolve_user_id(user_id)
    rows = fetch_all(
        """
        SELECT DATE(analysis_date) AS day, COALESCE(SUM(calories), 0) AS total
        FROM meals
        WHERE user_id = ?
          AND DATE(analysis_date) >= DATE('now', '-6 days')
        GROUP BY DATE(analysis_date)
        ORDER BY day ASC
        """,
        (uid,),
    )

    # Build last 7 calendar days with weekday labels (Mon, Tue, ...)
    today = datetime.now().date()
    day_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    db_map = {row["day"]: int(row["total"]) for row in rows} if rows else {}

    weekly: dict[str, int] = {}
    for offset in range(6, -1, -1):
        day = today - timedelta(days=offset)
        label = day_labels[day.weekday()]
        weekly[label] = db_map.get(day.strftime("%Y-%m-%d"), 0)

    return weekly


def get_macro_summary(user_id: int | None = None) -> dict[str, float]:
    """Return today's total protein, carbs, and fat from stored meals."""
    uid = _resolve_user_id(user_id)
    today = datetime.now().strftime("%Y-%m-%d")
    row = fetch_one(
        """
        SELECT
            COALESCE(SUM(protein), 0) AS protein,
            COALESCE(SUM(carbs), 0) AS carbs,
            COALESCE(SUM(fat), 0) AS fat,
            COALESCE(SUM(calories), 0) AS calories
        FROM meals
        WHERE user_id = ?
          AND DATE(analysis_date) = DATE(?)
        """,
        (uid, today),
    )
    if not row:
        return {"protein": 0.0, "carbs": 0.0, "fat": 0.0, "calories": 0.0}
    return {
        "protein": float(row["protein"]),
        "carbs": float(row["carbs"]),
        "fat": float(row["fat"]),
        "calories": float(row["calories"]),
    }


def get_meal_type_distribution(user_id: int | None = None) -> list[dict[str, Any]]:
    """Return calorie totals grouped by meal type."""
    uid = _resolve_user_id(user_id)
    return fetch_all(
        """
        SELECT meal_type, COALESCE(SUM(calories), 0) AS total_calories, COUNT(*) AS meal_count
        FROM meals
        WHERE user_id = ?
        GROUP BY meal_type
        ORDER BY total_calories DESC
        """,
        (uid,),
    )


def get_average_health_score(user_id: int | None = None) -> float:
    """Return average health score across all stored meals."""
    uid = _resolve_user_id(user_id)
    row = fetch_one(
        """
        SELECT COALESCE(AVG(health_score), 0) AS avg_score
        FROM meals
        WHERE user_id = ?
        """,
        (uid,),
    )
    return float(row["avg_score"]) if row else 0.0
