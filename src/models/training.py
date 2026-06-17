"""
src/models/training.py
========================
Training pipeline for NutriSense AI food recognition model.

How to train:
    python -m src.models.training

Or import:
    from src.models.training import train_food101

Saves to:
    saved_models/nutrisense_food_model.h5
    saved_models/class_names.json
"""

from __future__ import annotations

import os
import json
import logging
import argparse

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
    datefmt="%H:%M:%S",
)

# ── Paths ─────────────────────────────────────────────────────────────────────
SAVED_MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "saved_models")
MODEL_PATH       = os.path.join(SAVED_MODELS_DIR, "nutrisense_food_model.h5")
CHECKPOINT_PATH  = os.path.join(SAVED_MODELS_DIR, "checkpoint_best.h5")
CLASS_NAMES_PATH = os.path.join(SAVED_MODELS_DIR, "class_names.json")
REPORTS_DIR      = os.path.join(os.path.dirname(__file__), "..", "..", "reports")


# ── Main training function ────────────────────────────────────────────────────

def train_food101(
    epochs: int         = 15,
    batch_size: int     = 32,
    fine_tune: bool     = False,
    fine_tune_epochs: int = 5,
) -> dict:
    """
    Full training pipeline for Food-101.

    Phase 1 : Train only the classification head (base frozen).
    Phase 2 : (optional) Fine-tune top layers of EfficientNetB0.

    Parameters
    ----------
    epochs           : epochs for Phase 1
    batch_size       : images per batch
    fine_tune        : whether to run Phase 2 fine-tuning after Phase 1
    fine_tune_epochs : epochs for Phase 2

    Returns
    -------
    dict with keys: val_accuracy, val_loss, model_path
    """
    try:
        import tensorflow as tf
    except ImportError:
        raise ImportError("TensorFlow not installed. Run: pip install tensorflow")

    os.makedirs(SAVED_MODELS_DIR, exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)

    # ── 1. Load dataset ───────────────────────────────────────────────────────
    logger.info("📥 Loading Food-101 dataset…")
    from src.dataset.food101_loader import get_food101_dataset
    train_ds, val_ds, class_names = get_food101_dataset(batch_size=batch_size)

    num_classes = len(class_names)
    logger.info(f"Classes: {num_classes}")

    # ── 2. Build model ────────────────────────────────────────────────────────
    logger.info("🔨 Building EfficientNetB0 model…")
    from src.models.efficientnet import build_model, unfreeze_model, save_model

    model = build_model(num_classes=num_classes, freeze_base=True)
    model.summary(print_fn=logger.info)

    # ── 3. Callbacks ──────────────────────────────────────────────────────────
    callbacks = _build_callbacks()

    # ── 4. Phase 1 — train head ───────────────────────────────────────────────
    logger.info(f"🚀 Phase 1 training — {epochs} epochs (base frozen)…")
    history1 = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs,
        callbacks=callbacks,
        verbose=1,
    )

    # ── 5. Phase 2 — fine-tune (optional) ────────────────────────────────────
    history2 = None
    if fine_tune:
        logger.info(f"🔓 Phase 2 fine-tuning — {fine_tune_epochs} epochs…")
        model = unfreeze_model(model, num_layers_to_unfreeze=20)
        history2 = model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=fine_tune_epochs,
            callbacks=callbacks,
            verbose=1,
        )

    # ── 6. Save final model ───────────────────────────────────────────────────
    save_model(model, MODEL_PATH)
    _save_class_names(class_names)

    # ── 7. Save training plots ────────────────────────────────────────────────
    _save_training_plots(history1, history2)

    # ── 8. Final metrics ──────────────────────────────────────────────────────
    final_history = history2 or history1
    val_acc  = max(final_history.history.get("val_accuracy", [0]))
    val_loss = min(final_history.history.get("val_loss", [0]))

    result = {
        "val_accuracy": round(val_acc  * 100, 2),
        "val_loss":     round(val_loss, 4),
        "model_path":   MODEL_PATH,
        "num_classes":  num_classes,
    }

    logger.info(f"✅ Training complete — val accuracy: {result['val_accuracy']}%")
    return result


# ── Callbacks ─────────────────────────────────────────────────────────────────

def _build_callbacks() -> list:
    try:
        import tensorflow as tf
    except ImportError:
        return []

    return [
        # Stop if val_loss doesn't improve for 4 epochs
        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=4,
            restore_best_weights=True,
            verbose=1,
        ),
        # Save best checkpoint
        tf.keras.callbacks.ModelCheckpoint(
            filepath=CHECKPOINT_PATH,
            monitor="val_accuracy",
            save_best_only=True,
            verbose=1,
        ),
        # Reduce LR on plateau
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=2,
            min_lr=1e-7,
            verbose=1,
        )
    ]


# ── Helpers ───────────────────────────────────────────────────────────────────

def _save_class_names(class_names: list[str]) -> None:
    os.makedirs(SAVED_MODELS_DIR, exist_ok=True)
    with open(CLASS_NAMES_PATH, "w") as f:
        json.dump(class_names, f, indent=2)
    logger.info(f"💾 class_names.json saved → {CLASS_NAMES_PATH}")


def _save_training_plots(history1, history2=None) -> None:
    """Save accuracy and loss graphs to reports/."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        # merge histories
        acc  = history1.history.get("accuracy", [])
        loss = history1.history.get("loss", [])
        vacc = history1.history.get("val_accuracy", [])
        vloss= history1.history.get("val_loss", [])

        if history2:
            acc   += history2.history.get("accuracy", [])
            loss  += history2.history.get("loss", [])
            vacc  += history2.history.get("val_accuracy", [])
            vloss += history2.history.get("val_loss", [])

        epochs_range = range(1, len(acc) + 1)

        # Accuracy
        plt.figure(figsize=(8, 4))
        plt.plot(epochs_range, [a * 100 for a in acc],  label="Train Acc")
        plt.plot(epochs_range, [a * 100 for a in vacc], label="Val Acc")
        plt.title("Model Accuracy")
        plt.xlabel("Epoch")
        plt.ylabel("Accuracy (%)")
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(REPORTS_DIR, "accuracy_graph.png"), dpi=150)
        plt.close()

        # Loss
        plt.figure(figsize=(8, 4))
        plt.plot(epochs_range, loss,  label="Train Loss")
        plt.plot(epochs_range, vloss, label="Val Loss")
        plt.title("Model Loss")
        plt.xlabel("Epoch")
        plt.ylabel("Loss")
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(REPORTS_DIR, "loss_graph.png"), dpi=150)
        plt.close()

        logger.info("📊 Training plots saved to reports/")
    except Exception as e:
        logger.warning(f"Could not save plots: {e}")


# ── CLI entry point ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train NutriSense AI food model")
    parser.add_argument("--epochs",           type=int,  default=15)
    parser.add_argument("--batch-size",       type=int,  default=32)
    parser.add_argument("--fine-tune",        action="store_true")
    parser.add_argument("--fine-tune-epochs", type=int,  default=5)
    args = parser.parse_args()

    result = train_food101(
        epochs=args.epochs,
        batch_size=args.batch_size,
        fine_tune=args.fine_tune,
        fine_tune_epochs=args.fine_tune_epochs,
    )
    print(f"\n🎉 Done! Val Accuracy: {result['val_accuracy']}%")
    print(f"   Model saved → {result['model_path']}")