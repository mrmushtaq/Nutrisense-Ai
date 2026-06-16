"""
src/vision/model_loader.py
============================
Shared, app-wide cached model loader for the Food Scan AI.

Why this exists
----------------
`st.cache_resource` caches a value ONCE for the entire app (shared across
every user/session) — not per-session. By putting the cached loader here
and importing it from BOTH `Home.py` and `1_Upload_Food.py`, we get:

1. `Home.py` can "warm up" the model in a background thread the moment the
   app starts, while the dashboard renders normally.
2. `1_Upload_Food.py` calls the exact same cached function — if the
   background warm-up already finished, this returns INSTANTLY.
   If it's still loading, `st.cache_resource`'s internal lock makes this
   call simply wait for that same in-progress load (no duplicate work).
"""

from __future__ import annotations

import threading


@__import__("streamlit").cache_resource(show_spinner=False)
def load_model():
    """
    Load the food recognition model once for the whole app.
    Returns (predict_fn, model_ready, model_info).
    """
    try:
        from src.vision.prediction import predict_food, is_model_ready, get_model_info
        return predict_food, is_model_ready(), get_model_info()
    except Exception:
        return None, False, {}


def warm_up_model_async() -> None:
    """
    Kick off model loading in a background thread, non-blocking.

    Safe to call multiple times — `st.cache_resource` ensures the actual
    loading work only ever happens once. Call this from Home.py so loading
    starts the instant the app launches, before the user even opens
    Food Scan.
    """
    def _background_load():
        try:
            load_model()
        except Exception:
            # Any failure here is harmless — 1_Upload_Food.py will retry
            # the cached call in the foreground and surface the error there.
            pass

    threading.Thread(target=_background_load, daemon=True).start()