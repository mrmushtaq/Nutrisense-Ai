"""
src/dataset/preprocessing.py
==============================
Shared image preprocessing utilities.
Used by both Food-101 loader and the prediction pipeline.
"""

from __future__ import annotations

import io
import numpy as np
from PIL import Image

IMAGE_SIZE = (224, 224)


# ── For training (TensorFlow tensors) ─────────────────────────────────────────

def preprocess_image_tensor(image, label, image_size: tuple = IMAGE_SIZE):
    """
    Resize + normalise a (image_tensor, label) pair.
    Used inside tf.data pipelines.
    """
    import tensorflow as tf
    image = tf.image.resize(image, image_size)
    image = tf.cast(image, tf.float32) / 255.0
    return image, label


def augment_image_tensor(image, label):
    """
    Random augmentation for training.
    """
    import tensorflow as tf
    image = tf.image.random_flip_left_right(image)
    image = tf.image.random_brightness(image, max_delta=0.15)
    image = tf.image.random_contrast(image, lower=0.85, upper=1.15)
    image = tf.clip_by_value(image, 0.0, 1.0)
    return image, label


# ── For inference (PIL / bytes / numpy) ───────────────────────────────────────

def preprocess_pil_image(
    pil_image: Image.Image,
    image_size: tuple = IMAGE_SIZE,
) -> np.ndarray:
    """
    Convert a PIL Image → normalised numpy array ready for model.predict().

    Parameters
    ----------
    pil_image : PIL.Image.Image
    image_size: (width, height) — default 224×224

    Returns
    -------
    np.ndarray  shape (1, H, W, 3)  dtype float32
    """
    img = pil_image.convert("RGB")
    img = img.resize(image_size, Image.LANCZOS)
    arr = np.array(img, dtype=np.float32) / 255.0
    return np.expand_dims(arr, axis=0)          # add batch dimension


def preprocess_bytes(
    image_bytes: bytes,
    image_size: tuple = IMAGE_SIZE,
) -> np.ndarray:
    """
    Convert raw image bytes → normalised numpy array.
    Accepts JPEG, PNG, WebP, etc.
    """
    pil_image = Image.open(io.BytesIO(image_bytes))
    return preprocess_pil_image(pil_image, image_size)


def preprocess_file_path(
    file_path: str,
    image_size: tuple = IMAGE_SIZE,
) -> np.ndarray:
    """
    Load an image from disk and preprocess it.
    """
    pil_image = Image.open(file_path)
    return preprocess_pil_image(pil_image, image_size)


def decode_predictions_topk(
    predictions: np.ndarray,
    class_names: list[str],
    top_k: int = 5,
) -> list[dict]:
    """
    Convert raw softmax output → top-k class predictions.

    Parameters
    ----------
    predictions : np.ndarray  shape (1, num_classes)
    class_names : list[str]
    top_k       : how many top results to return

    Returns
    -------
    list of dicts:
        [{"class": "pizza", "confidence": 94.3}, ...]
    """
    probs = predictions[0]
    top_indices = np.argsort(probs)[::-1][:top_k]

    results = []
    for idx in top_indices:
        results.append({
            "class":      class_names[idx],
            "confidence": round(float(probs[idx]) * 100, 2),
        })
    return results