"""
Nutrition reference database for Pakistani and common foods.
Seeds nutrition_foods table from CSV and provides lookup helpers.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from src.database.connection import execute_query, fetch_all, fetch_one

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FOOD_CSV_PATH = PROJECT_ROOT / "data" / "nutrition" / "food_calories.csv"

# Default foods used when CSV is unavailable
DEFAULT_FOODS = [
    {"food_name": "Biryani",        "calories": 450, "protein": 20, "carbs": 55, "fat": 15, "category": "Rice Dish",  "serving_size": "1 plate"},
    {"food_name": "Nihari",         "calories": 380, "protein": 28, "carbs": 12, "fat": 24, "category": "Curry",      "serving_size": "1 bowl"},
    {"food_name": "Chicken Karahi", "calories": 420, "protein": 32, "carbs": 18, "fat": 22, "category": "Curry",      "serving_size": "1 serving"},
    {"food_name": "Haleem",         "calories": 350, "protein": 22, "carbs": 40, "fat": 12, "category": "Stew",       "serving_size": "1 bowl"},
    {"food_name": "Samosa",         "calories": 260, "protein": 5,  "carbs": 28, "fat": 14, "category": "Snack",      "serving_size": "2 pieces"},
    {"food_name": "Pakora",         "calories": 280, "protein": 8,  "carbs": 22, "fat": 18, "category": "Snack",      "serving_size": "6 pieces"},
    {"food_name": "Naan",           "calories": 260, "protein": 8,  "carbs": 46, "fat": 4,  "category": "Bread",      "serving_size": "1 piece"},
    {"food_name": "Roti",           "calories": 120, "protein": 4,  "carbs": 22, "fat": 2,  "category": "Bread",      "serving_size": "1 piece"},
    {"food_name": "Chapli Kabab",   "calories": 310, "protein": 24, "carbs": 8,  "fat": 20, "category": "Meat",       "serving_size": "2 pieces"},
    {"food_name": "Seekh Kabab",    "calories": 290, "protein": 26, "carbs": 6,  "fat": 18, "category": "Meat",       "serving_size": "2 skewers"},
    {"food_name": "Daal Chawal",    "calories": 380, "protein": 14, "carbs": 58, "fat": 10, "category": "Rice Dish",  "serving_size": "1 plate"},
    {"food_name": "Chana Chaat",    "calories": 220, "protein": 8,  "carbs": 32, "fat": 8,  "category": "Snack",      "serving_size": "1 bowl"},
]


def _load_food_records() -> list[dict[str, Any]]:
    """Load food records from CSV file, or use built-in defaults."""
    if FOOD_CSV_PATH.exists():
        df = pd.read_csv(FOOD_CSV_PATH)
        return df.to_dict(orient="records")
    return DEFAULT_FOODS


def seed_default_nutrition_data() -> int:
    """
    Insert default Pakistani food nutrition data if table is empty.
    Returns number of foods inserted.
    """
    existing = fetch_one("SELECT COUNT(*) AS count FROM nutrition_foods")
    if existing and existing["count"] > 0:
        return 0

    foods = _load_food_records()
    inserted = 0
    for food in foods:
        execute_query(
            """
            INSERT OR IGNORE INTO nutrition_foods
                (food_name, calories, protein, carbs, fat, category, serving_size)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                food["food_name"],
                food["calories"],
                food["protein"],
                food["carbs"],
                food["fat"],
                food.get("category", "General"),
                food.get("serving_size", "1 serving"),
            ),
        )
        inserted += 1
    return inserted


def get_food_nutrition(food_name: str) -> dict[str, Any] | None:
    """Exact match lookup for a food name in nutrition_foods."""
    return fetch_one(
        """
        SELECT *
        FROM nutrition_foods
        WHERE LOWER(food_name) = LOWER(?)
        """,
        (food_name.strip(),),
    )


def search_food(food_name: str) -> list[dict[str, Any]]:
    """Partial match search for food names."""
    pattern = f"%{food_name.strip()}%"
    return fetch_all(
        """
        SELECT *
        FROM nutrition_foods
        WHERE food_name LIKE ?
        ORDER BY food_name ASC
        """,
        (pattern,),
    )


def get_all_foods() -> list[dict[str, Any]]:
    """Return all foods from the nutrition reference table."""
    return fetch_all(
        """
        SELECT *
        FROM nutrition_foods
        ORDER BY food_name ASC
        """
    )
