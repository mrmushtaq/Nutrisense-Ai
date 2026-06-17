"""Image preprocessing for food recognition (Phase II stub)."""

from __future__ import annotations

from typing import Any

import numpy as np
from PIL import Image


def preprocess_image(uploaded_file: Any) -> np.ndarray:
    """Read an uploaded image into an RGB numpy array."""
    uploaded_file.seek(0)
    image = Image.open(uploaded_file).convert("RGB")
    return np.array(image)
