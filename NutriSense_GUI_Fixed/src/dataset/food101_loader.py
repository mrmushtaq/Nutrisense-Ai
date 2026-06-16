"""
src/dataset/food101_loader.py
==============================
Food-101 Dataset Loader using TensorFlow Datasets.

Usage:
    from src.dataset.food101_loader import get_food101_dataset

    train_ds, val_ds, class_names = get_food101_dataset()
"""

from __future__ import annotations

import os
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ── Constants ──────────────────────────────────────────────────────────────────
IMAGE_SIZE   = (224, 224)
BATCH_SIZE   = 32
AUTOTUNE     = None          # set after TF import
CACHE_DIR    = os.path.join(os.path.dirname(__file__), "..", "..", "data", "food101_cache")


def get_food101_dataset(
    image_size: tuple[int, int] = IMAGE_SIZE,
    batch_size: int = BATCH_SIZE,
    cache_dir: str = CACHE_DIR,
) -> tuple:
    """
    Download (if needed) and return Food-101 as TF datasets.

    Returns
    -------
    train_dataset     : tf.data.Dataset  (batched, prefetched)
    validation_dataset: tf.data.Dataset  (batched, prefetched)
    class_names       : list[str]        (101 food class labels)
    """
    try:
        import tensorflow as tf
        import tensorflow_datasets as tfds
    except ImportError as e:
        raise ImportError(
            "TensorFlow / tensorflow_datasets not installed.\n"
            "Run:  pip install tensorflow tensorflow-datasets"
        ) from e

    global AUTOTUNE
    AUTOTUNE = tf.data.AUTOTUNE

    os.makedirs(cache_dir, exist_ok=True)
    logger.info("📥 Loading Food-101 dataset (auto-download if needed)…")

    # ── Load raw splits ────────────────────────────────────────────────────────
    (raw_train, raw_val), info = tfds.load(
        "food101",
        split=["train", "validation"],
        as_supervised=True,          # returns (image, label) tuples
        with_info=True,
        data_dir=cache_dir,
        shuffle_files=True,
    )

    class_names: list[str] = info.features["label"].names
    num_classes: int        = info.features["label"].num_classes

    logger.info(f"✅ Food-101 loaded — {num_classes} classes, "
                f"{info.splits['train'].num_examples:,} train / "
                f"{info.splits['validation'].num_examples:,} val examples")

    # ── Preprocessing fn ──────────────────────────────────────────────────────
    def preprocess(image: tf.Tensor, label: tf.Tensor):
        image = tf.image.resize(image, image_size)          # 224 × 224
        image = tf.cast(image, tf.float32) / 255.0          # normalise [0, 1]
        return image, label

    # ── Augmentation fn (train only) ──────────────────────────────────────────
    def augment(image: tf.Tensor, label: tf.Tensor):
        image = tf.image.random_flip_left_right(image)
        image = tf.image.random_brightness(image, max_delta=0.15)
        image = tf.image.random_contrast(image, lower=0.85, upper=1.15)
        image = tf.clip_by_value(image, 0.0, 1.0)
        return image, label

    # ── Build optimised pipelines ──────────────────────────────────────────────
    train_dataset = (
        raw_train
        .map(preprocess, num_parallel_calls=AUTOTUNE)
        .map(augment,    num_parallel_calls=AUTOTUNE)
        .shuffle(buffer_size=2048)
        .batch(batch_size)
        .prefetch(AUTOTUNE)
    )

    validation_dataset = (
        raw_val
        .map(preprocess, num_parallel_calls=AUTOTUNE)
        .batch(batch_size)
        .prefetch(AUTOTUNE)
    )

    # ── Save class names for later use ────────────────────────────────────────
    _save_class_names(class_names)

    return train_dataset, validation_dataset, class_names


def _save_class_names(class_names: list[str]) -> None:
    """Persist class names to saved_models/class_names.json."""
    save_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "saved_models", "class_names.json"
    )
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "w") as f:
        json.dump(class_names, f, indent=2)
    logger.info(f"💾 Class names saved → {save_path}")


def load_class_names() -> list[str]:
    """
    Load class names from saved_models/class_names.json.
    Returns empty list if file doesn't exist yet.
    """
    path = os.path.join(
        os.path.dirname(__file__), "..", "..", "saved_models", "class_names.json"
    )
    if not os.path.exists(path):
        logger.warning("⚠️  class_names.json not found — run training first.")
        return []
    with open(path) as f:
        return json.load(f)