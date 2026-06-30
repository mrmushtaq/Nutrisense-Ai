"""User preferences and AI memory — favorite foods, dislikes, allergies, and history."""

from __future__ import annotations

from typing import Any

from src.database.connection import execute_query, fetch_one, fetch_all


def save_favorite_food(user_id: int, food_name: str) -> None:
    """Save a food to user's favorites list."""
    existing = fetch_one(
        "SELECT id FROM user_preferences WHERE user_id = ? AND key = 'favorite_food' AND value = ?",
        (user_id, food_name),
    )
    if not existing:
        execute_query(
            "INSERT INTO user_preferences (user_id, key, value) VALUES (?, 'favorite_food', ?)",
            (user_id, food_name),
        )


def save_disliked_food(user_id: int, food_name: str) -> None:
    """Save a disliked food to avoid in recommendations."""
    existing = fetch_one(
        "SELECT id FROM user_preferences WHERE user_id = ? AND key = 'disliked_food' AND value = ?",
        (user_id, food_name),
    )
    if not existing:
        execute_query(
            "INSERT INTO user_preferences (user_id, key, value) VALUES (?, 'disliked_food', ?)",
            (user_id, food_name),
        )


def get_favorite_foods(user_id: int) -> list[str]:
    """Return list of favorite food names."""
    rows = fetch_all(
        "SELECT value FROM user_preferences WHERE user_id = ? AND key = 'favorite_food'",
        (user_id,),
    )
    return [r["value"] for r in rows]


def get_disliked_foods(user_id: int) -> list[str]:
    """Return list of disliked food names."""
    rows = fetch_all(
        "SELECT value FROM user_preferences WHERE user_id = ? AND key = 'disliked_food'",
        (user_id,),
    )
    return [r["value"] for r in rows]


def remove_favorite_food(user_id: int, food_name: str) -> None:
    execute_query(
        "DELETE FROM user_preferences WHERE user_id = ? AND key = 'favorite_food' AND value = ?",
        (user_id, food_name),
    )


def remove_disliked_food(user_id: int, food_name: str) -> None:
    execute_query(
        "DELETE FROM user_preferences WHERE user_id = ? AND key = 'disliked_food' AND value = ?",
        (user_id, food_name),
    )


def get_user_context(user_id: int) -> dict[str, Any]:
    """Build a context dict for AI prompts with user preferences."""
    from src.database.user import get_user_profile

    profile = get_user_profile(user_id)
    favorites = get_favorite_foods(user_id)
    dislikes = get_disliked_foods(user_id)
    allergies = profile.get("allergies", "")

    return {
        "favorite_foods": favorites,
        "disliked_foods": dislikes,
        "allergies": [a.strip().lower() for a in allergies.split(",") if a.strip()],
        "dietary_preference": profile.get("dietary_preference", "None"),
    }
