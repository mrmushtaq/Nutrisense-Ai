"""
src/dataset/custom_loader.py
==============================
Pakistani Food Custom Dataset Loader.

Safely loads images from:
    data/pakistani_food/train/
    data/pakistani_food/validation/
    data/pakistani_food/test/

If folders are empty or missing → skips gracefully, does NOT crash.

Usage:
    from src.dataset.custom_loader import get_pakistani_dataset, check_dataset_status

    status = check_dataset_status()
    print(status)  # shows how many images per split

    train_ds, val_ds, class_names = get_pakistani_dataset()
"""

from __future__ import annotations

import os
import logging

logger = logging.getLogger(__name__)

# ── Config ────────────────────────────────────────────────────────────────────
BASE_DIR    = os.path.join(os.path.dirname(__file__), "..", "..", "data", "pakistani_food")
IMAGE_SIZE  = (224, 224)
BATCH_SIZE  = 16

PAKISTANI_CLASSES = [
    "biryani", "nihari", "karahi", "haleem",
    "samosa", "pakora", "naan", "roti",
    "chapli_kabab", "seekh_kabab",
]


# ── Status check ──────────────────────────────────────────────────────────────

def check_dataset_status() -> dict:
    """
    Check how many images exist in each split.

    Returns
    -------
    dict with keys: has_data, train_count, val_count, test_count, class_summary
    """
    splits = {"train": 0, "validation": 0, "test": 0}
    class_summary = {}

    for split in splits:
        split_dir = os.path.join(BASE_DIR, split)
        if not os.path.isdir(split_dir):
            continue

        for cls in os.listdir(split_dir):
            cls_dir = os.path.join(split_dir, cls)
            if not os.path.isdir(cls_dir):
                continue

            images = [
                f for f in os.listdir(cls_dir)
                if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
            ]
            splits[split] += len(images)

            if split == "train":
                class_summary[cls] = len(images)

    total = sum(splits.values())

    return {
        "has_data":     total > 0,
        "total_images": total,
        "train_count":  splits["train"],
        "val_count":    splits["validation"],
        "test_count":   splits["test"],
        "class_summary": class_summary,
    }


# ── Dataset loader ────────────────────────────────────────────────────────────

def get_pakistani_dataset(
    image_size: tuple = IMAGE_SIZE,
    batch_size: int   = BATCH_SIZE,
) -> tuple:
    """
    Load Pakistani food dataset using Keras image_dataset_from_directory.

    Returns
    -------
    train_dataset      : tf.data.Dataset or None
    validation_dataset : tf.data.Dataset or None
    class_names        : list[str]

    If train folder is empty → returns (None, None, [])
    """
    status = check_dataset_status()

    if not status["has_data"]:
        logger.info(
            "ℹ️  Pakistani food dataset is empty. "
            "Add images to data/pakistani_food/train/<class>/ to enable training."
        )
        return None, None, []

    try:
        import tensorflow as tf
    except ImportError:
        logger.error("TensorFlow not installed.")
        return None, None, []

    AUTOTUNE = tf.data.AUTOTUNE

    def _load_split(split_name: str):
        split_dir = os.path.join(BASE_DIR, split_name)
        if not os.path.isdir(split_dir):
            return None

        # count actual images
        count = sum(
            len([f for f in os.listdir(os.path.join(split_dir, cls))
                 if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))])
            for cls in os.listdir(split_dir)
            if os.path.isdir(os.path.join(split_dir, cls))
        )

        if count == 0:
            return None

        ds = tf.keras.utils.image_dataset_from_directory(
            split_dir,
            image_size=image_size,
            batch_size=batch_size,
            label_mode="int",
            shuffle=(split_name == "train"),
        )
        return ds

    train_ds = _load_split("train")
    val_ds   = _load_split("validation")

    if train_ds is None:
        logger.info("ℹ️  No training images found in Pakistani dataset.")
        return None, None, []

    class_names = train_ds.class_names

    # normalise pixels
    def normalise(images, labels):
        return tf.cast(images, tf.float32) / 255.0, labels

    train_ds = train_ds.map(normalise, num_parallel_calls=AUTOTUNE).prefetch(AUTOTUNE)

    if val_ds is not None:
        val_ds = val_ds.map(normalise, num_parallel_calls=AUTOTUNE).prefetch(AUTOTUNE)

    logger.info(
        f"✅ Pakistani dataset loaded — "
        f"{status['train_count']} train, {status['val_count']} val images. "
        f"Classes: {class_names}"
    )

    return train_ds, val_ds, class_names