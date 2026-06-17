"""
src/vision/image_processor.py
================================
Image loading and preprocessing for inference.

Accepts: PIL.Image, bytes, file path, or Streamlit UploadedFile.
"""

from __future__ import annotations

import io
import logging
import numpy as np
from PIL import Image

logger = logging.getLogger(__name__)

IMAGE_SIZE = (224, 224)


def load_image(source) -> Image.Image:
    """
    Load an image from various source types.

    Accepts
    -------
    - PIL.Image.Image      → returned as-is
    - bytes / bytearray    → decoded with PIL
    - str / os.PathLike    → opened from disk
    - Streamlit UploadedFile (has .read() method)
    """
    if isinstance(source, Image.Image):
        return source

    if isinstance(source, (bytes, bytearray)):
        return Image.open(io.BytesIO(source))

    if hasattr(source, "read"):
        # Streamlit UploadedFile or any file-like object
        return Image.open(io.BytesIO(source.read()))

    if isinstance(source, (str,)):
        return Image.open(source)

    raise TypeError(f"Unsupported image source type: {type(source)}")


def prepare_for_model(
    source,
    image_size: tuple = IMAGE_SIZE,
) -> np.ndarray:
    """
    Load → convert to RGB → resize → normalise → add batch dim.

    Returns
    -------
    np.ndarray  shape (1, H, W, 3)  dtype float32  values [0, 1]
    """
    img = load_image(source)
    img = img.convert("RGB")
    img = img.resize(image_size, Image.LANCZOS)
    arr = np.array(img, dtype=np.float32) / 255.0
    return np.expand_dims(arr, axis=0)


def get_image_thumbnail(source, size: tuple = (300, 300)) -> Image.Image:
    """
    Return a resized PIL image for display (not model input).
    """
    img = load_image(source)
    img = img.convert("RGB")
    img.thumbnail(size, Image.LANCZOS)
    return img