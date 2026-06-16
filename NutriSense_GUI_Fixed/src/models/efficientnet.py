"""
src/models/efficientnet.py
===========================
EfficientNetB0 model builder for NutriSense AI.

Architecture:
    Input 224×224×3
    → EfficientNetB0 (ImageNet pretrained, frozen base)
    → GlobalAveragePooling2D
    → Dropout(0.3)
    → Dense(num_classes, softmax)

Usage:
    from src.models.efficientnet import build_model, save_model, load_model

    model = build_model(num_classes=101)
    model.summary()
"""

from __future__ import annotations

import os
import json
import logging

logger = logging.getLogger(__name__)

# ── Paths ─────────────────────────────────────────────────────────────────────
SAVED_MODELS_DIR  = os.path.join(os.path.dirname(__file__), "..", "..", "saved_models")
MODEL_PATH        = os.path.join(SAVED_MODELS_DIR, "nutrisense_food_model.h5")
CLASS_NAMES_PATH  = os.path.join(SAVED_MODELS_DIR, "class_names.json")


# ── Build ─────────────────────────────────────────────────────────────────────

def build_model(
    num_classes: int   = 101,
    image_size:  tuple = (224, 224),
    dropout_rate: float = 0.3,
    freeze_base: bool  = True,
):
    """
    Build EfficientNetB0 transfer-learning model.

    Parameters
    ----------
    num_classes  : output classes (101 for Food-101, 10 for Pakistani)
    image_size   : input image dimensions
    dropout_rate : dropout before final Dense layer
    freeze_base  : if True, freeze EfficientNetB0 weights (Phase 1 training)

    Returns
    -------
    tf.keras.Model
    """
    try:
        import tensorflow as tf
        from tensorflow.keras import layers, Model
        from tensorflow.keras.applications import EfficientNetB0
    except ImportError as e:
        raise ImportError("TensorFlow not installed. Run: pip install tensorflow") from e

    # ── Base model ────────────────────────────────────────────────────────────
    base_model = EfficientNetB0(
        include_top=False,
        weights="imagenet",
        input_shape=(*image_size, 3),
    )
    base_model.trainable = not freeze_base   # freeze during Phase 1

    # ── Classification head ───────────────────────────────────────────────────
    inputs  = tf.keras.Input(shape=(*image_size, 3))
    x       = base_model(inputs, training=False)
    x       = layers.GlobalAveragePooling2D()(x)
    x       = layers.Dropout(dropout_rate)(x)
    outputs = layers.Dense(num_classes, activation="softmax")(x)

    model = Model(inputs, outputs, name="NutriSense_EfficientNetB0")

    # ── Compile ───────────────────────────────────────────────────────────────
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    logger.info(
        f"✅ Model built — {num_classes} classes, "
        f"base frozen={freeze_base}, dropout={dropout_rate}"
    )
    return model


def unfreeze_model(model, num_layers_to_unfreeze: int = 20):
    """
    Unfreeze top N layers of base model for fine-tuning (Phase 2).

    Parameters
    ----------
    model                  : keras Model returned by build_model()
    num_layers_to_unfreeze : how many layers from top to unfreeze
    """
    import tensorflow as tf

    base_model = model.layers[1]            # EfficientNetB0 is 2nd layer
    base_model.trainable = True

    # freeze everything except last N layers
    for layer in base_model.layers[:-num_layers_to_unfreeze]:
        layer.trainable = False

    # recompile with lower LR for fine-tuning
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    logger.info(f"🔓 Unfrozen top {num_layers_to_unfreeze} layers for fine-tuning.")
    return model


# ── Save / Load ───────────────────────────────────────────────────────────────

def save_model(model, path: str = MODEL_PATH) -> None:
    """Save trained model weights to .h5 file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    model.save(path)
    logger.info(f"💾 Model saved → {path}")


def load_model(path: str = MODEL_PATH):
    """
    Load a saved model from disk.

    Returns
    -------
    tf.keras.Model or None if file doesn't exist
    """
    if not os.path.exists(path):
        logger.warning(f"⚠️  Model file not found: {path}")
        return None

    try:
        import tensorflow as tf
        model = tf.keras.models.load_model(path)
        logger.info(f"✅ Model loaded from {path}")
        return model
    except Exception as e:
        logger.error(f"❌ Failed to load model: {e}")
        return None


def model_exists(path: str = MODEL_PATH) -> bool:
    """Check if a trained model file exists."""
    return os.path.exists(path)