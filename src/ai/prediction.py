"""Food recognition prediction (Phase II stub — always returns Biryani)."""

from __future__ import annotations

from typing import Any

import numpy as np

from config import DUMMY_NUTRITION_DATA


def predict_food(image_array: np.ndarray) -> dict[str, Any]:
    """Return a dummy prediction until the EfficientNet model is integrated."""
    _ = image_array
    confidence = DUMMY_NUTRITION_DATA["confidence"]
    return {
        "label": DUMMY_NUTRITION_DATA["food"],
        "confidence": confidence / 100 if confidence > 1 else confidence,
        "meal_type": DUMMY_NUTRITION_DATA.get("meal_type", "Lunch"),
        "health_score": DUMMY_NUTRITION_DATA.get("health_score", 75),
    }
