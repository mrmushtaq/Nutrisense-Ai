from __future__ import annotations

import numpy as np

from src.ai.prediction import predict_food


def test_predict_food_returns_expected_shape():
    img = np.zeros((224, 224, 3), dtype=np.float32)
    out = predict_food(img)

    assert isinstance(out, dict)
    assert "label" in out
    assert "confidence" in out
    assert "meal_type" in out
    assert "health_score" in out

    assert isinstance(out["label"], str)
    assert isinstance(out["meal_type"], str)
    assert isinstance(out["health_score"], int)
    assert isinstance(out["confidence"], float)


def test_confidence_is_in_valid_range():
    img = np.zeros((10, 10, 3), dtype=np.float32)
    out = predict_food(img)

    assert 0.0 <= out["confidence"] <= 1.0

