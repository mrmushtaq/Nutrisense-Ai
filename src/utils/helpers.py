"""
App-wide helper utilities for NutriSense AI.
Handles database initialization and shared session-state setup.
"""

from __future__ import annotations

import streamlit as st


def init_app() -> None:
    """
    Initialize database (idempotent) and seed default nutrition data.
    Safe to call on every page load.
    """
    if st.session_state.get("_app_initialized"):
        return

    from src.database.connection import initialize_database
    from src.database.user import create_default_user
    from src.nutrition.nutrition_database import seed_default_nutrition_data

    initialize_database()
    create_default_user()
    seed_default_nutrition_data()

    st.session_state["_app_initialized"] = True


def get_active_user_id() -> int:
    """
    Return the active user id for this session.
    Uses the authenticated user's id if signed in, otherwise defaults
    to user_id = 1 (default demo user).
    """
    return st.session_state.get("user_id", 1)
