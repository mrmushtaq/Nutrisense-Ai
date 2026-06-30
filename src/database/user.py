"""
User profile and goal management for NutriSense AI.
"""

from __future__ import annotations

import hashlib
import secrets
from datetime import datetime
from typing import Any

from config import DAILY_CALORIE_GOAL, DUMMY_USER

from src.database.connection import execute_query, fetch_one


def _hash_password(password: str, salt: str) -> str:
    """Return a salted SHA-256 hash of the password."""
    return hashlib.sha256((salt + password).encode("utf-8")).hexdigest()


def create_user(name: str, email: str, password: str) -> dict[str, Any]:
    """
    Create a new user account with email/password and a default goal.
    Raises ValueError if the email is already registered.
    """
    if fetch_one("SELECT id FROM users WHERE email = ?", (email,)):
        raise ValueError("An account with this email already exists.")

    salt = secrets.token_hex(8)
    password_hash = f"{salt}${_hash_password(password, salt)}"

    user_id = execute_query(
        """
        INSERT INTO users (name, age, gender, height_cm, weight_kg, goal, daily_calorie_goal, email, password_hash, dietary_preference, allergies, medical_conditions, activity_level, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            name,
            DUMMY_USER["age"],
            "Not specified",
            DUMMY_USER["height_cm"],
            DUMMY_USER["weight_kg"],
            DUMMY_USER["goal"],
            DAILY_CALORIE_GOAL,
            email,
            password_hash,
            "None",
            "",
            "",
            DUMMY_USER["activity_level"],
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ),
    )

    execute_query(
        """
        INSERT INTO goals (user_id, goal_type, target_calories, activity_level, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            user_id,
            DUMMY_USER["goal"],
            DAILY_CALORIE_GOAL,
            DUMMY_USER["activity_level"],
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ),
    )

    return fetch_one("SELECT * FROM users WHERE id = ?", (user_id,))


def verify_login(email: str, password: str) -> dict[str, Any] | None:
    """
    Verify email/password against stored credentials.
    Returns the user record if valid, otherwise None.
    """
    user = fetch_one("SELECT * FROM users WHERE email = ?", (email,))
    if not user or not user.get("password_hash"):
        return None

    stored = user["password_hash"]
    if "$" not in stored:
        return None

    salt, hashed = stored.split("$", 1)
    if _hash_password(password, salt) == hashed:
        return user
    return None


def get_user_by_id(user_id: int) -> dict[str, Any] | None:
    """Return a user record by id."""
    return fetch_one("SELECT * FROM users WHERE id = ?", (user_id,))


def create_default_user() -> dict[str, Any]:
    """
    Create a demo user if none exists.
    Returns the default user record.
    """
    existing = fetch_one("SELECT * FROM users ORDER BY id ASC LIMIT 1")
    if existing:
        return existing

    user_id = execute_query(
        """
        INSERT INTO users (name, age, gender, height_cm, weight_kg, goal, daily_calorie_goal, dietary_preference, allergies, medical_conditions, activity_level, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            DUMMY_USER["name"],
            DUMMY_USER["age"],
            "Not specified",
            DUMMY_USER["height_cm"],
            DUMMY_USER["weight_kg"],
            DUMMY_USER["goal"],
            DAILY_CALORIE_GOAL,
            "None",
            "",
            "",
            DUMMY_USER["activity_level"],
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ),
    )

    execute_query(
        """
        INSERT INTO goals (user_id, goal_type, target_calories, activity_level, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            user_id,
            DUMMY_USER["goal"],
            DAILY_CALORIE_GOAL,
            DUMMY_USER["activity_level"],
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ),
    )

    return get_default_user()


def get_default_user() -> dict[str, Any]:
    """Return the first (default) user profile."""
    user = fetch_one("SELECT * FROM users ORDER BY id ASC LIMIT 1")
    if not user:
        return create_default_user()
    return user


def update_user_goal(goal: str, daily_calorie_goal: int, activity_level: str, user_id: int | None = None) -> None:
    """
    Update user goal settings in users table and append a goals history record.
    """
    if user_id is None:
        user = get_default_user()
        user_id = user["id"]

    execute_query(
        """
        UPDATE users
        SET goal = ?, daily_calorie_goal = ?, activity_level = ?
        WHERE id = ?
        """,
        (goal, daily_calorie_goal, activity_level, user_id),
    )

    from src.database.connection import fetch_one
    existing_goal = fetch_one(
        "SELECT id FROM goals WHERE user_id = ? ORDER BY id DESC LIMIT 1",
        (user_id,),
    )
    if existing_goal:
        execute_query(
            """
            UPDATE goals SET goal_type = ?, target_calories = ?, activity_level = ?, created_at = ?
            WHERE id = ?
            """,
            (goal, daily_calorie_goal, activity_level, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), existing_goal["id"]),
        )
    else:
        execute_query(
            """
            INSERT INTO goals (user_id, goal_type, target_calories, activity_level, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, goal, daily_calorie_goal, activity_level, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )


def update_user_profile(
    user_id: int,
    name: str | None = None,
    age: int | None = None,
    gender: str | None = None,
    height_cm: float | None = None,
    weight_kg: float | None = None,
    dietary_preference: str | None = None,
    allergies: str | None = None,
    medical_conditions: str | None = None,
    activity_level: str | None = None,
) -> None:
    """Update user profile fields. Only provided fields are updated."""
    fields = {}
    if name is not None:
        fields["name"] = name
    if age is not None:
        fields["age"] = age
    if gender is not None:
        fields["gender"] = gender
    if height_cm is not None:
        fields["height_cm"] = height_cm
    if weight_kg is not None:
        fields["weight_kg"] = weight_kg
    if dietary_preference is not None:
        fields["dietary_preference"] = dietary_preference
    if allergies is not None:
        fields["allergies"] = allergies
    if medical_conditions is not None:
        fields["medical_conditions"] = medical_conditions
    if activity_level is not None:
        fields["activity_level"] = activity_level

    if not fields:
        return

    set_clause = ", ".join(f"{k} = ?" for k in fields)
    values = list(fields.values()) + [user_id]
    execute_query(f"UPDATE users SET {set_clause} WHERE id = ?", values)


def get_user_profile(user_id: int | None = None) -> dict[str, Any]:
    """
    Return user profile enriched with latest goal and activity level.
    If user_id is given (e.g. from the active session), that user's
    profile is returned; otherwise falls back to the default user.
    """
    user = get_user_by_id(user_id) if user_id else None
    if not user:
        user = get_default_user()
    latest_goal = fetch_one(
        """
        SELECT goal_type, target_calories, activity_level, created_at
        FROM goals
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (user["id"],),
    )

    profile = dict(user)
    if latest_goal:
        profile["goal_type"] = latest_goal["goal_type"]
        profile["target_calories"] = latest_goal["target_calories"]
        profile["activity_level"] = latest_goal["activity_level"]
        profile["goal_updated_at"] = latest_goal["created_at"]
    else:
        profile["goal_type"] = user.get("goal", "Maintenance")
        profile["target_calories"] = user.get("daily_calorie_goal", DAILY_CALORIE_GOAL)
        profile["activity_level"] = DUMMY_USER["activity_level"]

    return profile
