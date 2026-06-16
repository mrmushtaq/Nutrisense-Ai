"""
streamlit_app/pages/1_Upload_Food.py
======================================
Food Scan Page — NutriSense AI.

Uses pretrained Food-101 HuggingFace prediction.
OPTIMIZED: Model cached with st.cache_resource (shared across all sessions,
loads only once for the whole app) and loaded AFTER the page layout renders,
so the UI appears instantly instead of a blank white screen.
"""

from __future__ import annotations

import os
import sys
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

import streamlit as st

from src.nutrition.nutrition_database import get_food_nutrition
from src.utils.ui import (
    render_app_layout,
    render_page_header,
    render_info_box,
    render_footer,
    card_header,
)
from src.utils.helpers import get_active_user_id
from src.database.meals import get_today_summary, add_meal

st.set_page_config(
    page_title="Food Scan — NutriSense AI",
    page_icon="📸",
    layout="wide",
    initial_sidebar_state="expanded",
)


if not st.session_state.get("authenticated"):
    from streamlit_app.Account import render_account_page
    render_account_page()
    st.stop()


@st.cache_data(ttl=60)
def _cached_summary(uid: int) -> dict:
    return get_today_summary(uid)


# ── MODEL CACHED WITH st.cache_resource ───────────────────────────────────────
# st.cache_resource caches the loaded model ONCE for the entire app
# (shared across every user/session), not just the current session.
# Combined with show_spinner=False below + our own inline placeholder,
# the user sees a clean inline message only the very first time anyone
# loads this page after the app starts — every load after that is instant.
@st.cache_resource(show_spinner=False)
def _load_model():
    try:
        from src.vision.prediction import predict_food, is_model_ready, get_model_info
        return predict_food, is_model_ready(), get_model_info()
    except Exception:
        return None, False, {}


def _default_nutrition() -> dict:
    return {
        "calories": 250,
        "protein": 8,
        "carbs": 30,
        "fat": 10,
        "health_score": 65,
        "category": "Estimated",
        "serving_size": "1 serving",
    }


def _lookup_nutrition(food_name: str) -> dict:
    clean_food_name = food_name.replace("_", " ").title()
    nutrition = get_food_nutrition(clean_food_name)
    if nutrition:
        return dict(nutrition)
    return _default_nutrition()


user_id = get_active_user_id()
summary = _cached_summary(user_id)

# ── Render the page layout FIRST (instant — no ML imports yet) ────────────────
render_app_layout(
    active_page="upload",
    calories_today=float(summary.get("calories", 0) or 0),
    daily_goal=float(summary.get("calorie_goal", 2200) or 2200),
)

render_page_header(
    "📸 Food Scan",
    "Upload a photo to identify food and get nutritional information.",
)


left_col, right_col = st.columns([1, 1])

with left_col:
    with st.container(border=True):
        card_header("Upload Food Image", "JPG, PNG, WebP supported", icon="📷")

        uploaded_file = st.file_uploader(
            "Choose an image",
            type=["jpg", "jpeg", "png", "webp"],
            label_visibility="collapsed",
        )

        meal_type = st.selectbox(
            "Meal Type",
            ["Breakfast", "Lunch", "Dinner", "Snack"],
            index=1,
        )

        scan_btn = st.button(
            "🔍 Scan Food",
            type="primary",
            disabled=(uploaded_file is None),
        )

with right_col:
    with st.container(border=True):
        card_header("Preview", icon="🖼️")

        if uploaded_file:
            st.image(uploaded_file, width="stretch", caption="Uploaded image")
        else:
            st.markdown(
                """
                <div style="
                    height:260px;display:flex;align-items:center;
                    justify-content:center;background:#f8fafc;
                    border-radius:12px;border:2px dashed #cbd5e1;
                    color:#94a3b8;font-size:1rem;
                ">
                    📷 Upload an image to preview
                </div>
                """,
                unsafe_allow_html=True,
            )


# ── Load model AFTER layout is on screen. ─────────────────────────────────────
# First-ever call across the whole app shows a clean inline message in the
# normal page flow (not a floating overlay); cached for every subsequent
# page load / user, so it disappears instantly after that.
model_status_slot = st.empty()
if "model_loaded_once" not in st.session_state:
    with model_status_slot.container():
        render_info_box(
            "⏳ Loading AI model for the first time — this may take a few seconds...",
            "info",
        )

predict_fn, model_ready, model_info = _load_model()
st.session_state["model_loaded_once"] = True
model_status_slot.empty()

if model_ready:
    render_info_box(
        f"✅ AI Model Active — "
        f"{model_info.get('classes', model_info.get('num_classes', 101))} "
        f"food classes loaded.",
        "success",
    )
else:
    render_info_box(
        "⚠️ AI model not ready. Check src/vision/prediction.py.",
        "warn",
    )


# ── STEP 1: Run prediction only on Scan click ────────────────────────────────
if scan_btn and uploaded_file:
    scan_status_slot = st.empty()
    with scan_status_slot.container():
        render_info_box("🔍 AI is analysing your food — please wait...", "info")

    try:
        suffix = os.path.splitext(uploaded_file.name)[1] or ".jpg"
        uploaded_file.seek(0)

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(uploaded_file.read())
            temp_path = tmp.name

        # Use cached predict_fn — no re-import, no re-load
        if predict_fn is not None:
            result = predict_fn(temp_path)
        else:
            from src.vision.prediction import predict_food
            result = predict_food(temp_path)

    except Exception as e:
        result = {
            "food_name": "Unknown Food",
            "confidence": 0.0,
            "model_used": "error",
            "top_predictions": [],
            "note": str(e),
        }

    scan_status_slot.empty()

    detected_food = result.get("food_name", "Unknown Food")
    nutrition = _lookup_nutrition(detected_food)

    st.session_state["last_scan_result"]    = result
    st.session_state["last_meal_type"]      = meal_type
    st.session_state["last_uploaded_image"] = uploaded_file.name
    st.session_state["last_nutrition"]      = nutrition
    st.session_state["meal_saved"]          = False


# ── STEP 2: Show result from session_state ───────────────────────────────────
if "last_scan_result" in st.session_state:
    result    = st.session_state["last_scan_result"]
    nutrition = st.session_state.get("last_nutrition", _default_nutrition())

    food_name         = result.get("food_name", "Unknown Food")
    display_food_name = food_name.replace("_", " ").title()
    confidence        = float(result.get("confidence", 0.0) or 0.0)

    saved_meal_type = st.session_state.get("last_meal_type", meal_type)
    image_name      = st.session_state.get("last_uploaded_image")

    st.success(
        f"✅ Identified: **{display_food_name}** "
        f"({confidence:.1f}% confidence)"
    )

    if result.get("model_used") == "error":
        st.error(f"Prediction error: {result.get('note', '')}")

    with st.container(border=True):
        card_header(
            "Nutrition Estimate",
            nutrition.get("source", nutrition.get("category", "Estimated")),
            icon="🥗",
        )

        n1, n2, n3, n4 = st.columns(4)
        n1.metric("Calories", f"{float(nutrition.get('calories', 0)):.0f} kcal")
        n2.metric("Protein",  f"{float(nutrition.get('protein',  0)):.1f}g")
        n3.metric("Carbs",    f"{float(nutrition.get('carbs',    0)):.1f}g")
        n4.metric("Fat",      f"{float(nutrition.get('fat',      0)):.1f}g")

    top = result.get("top_predictions", [])
    if top:
        with st.expander("📊 Top Predictions", expanded=True):
            for i, pred in enumerate(top[:5], start=1):
                label = pred.get("class") or pred.get("label") or "Unknown"
                if "confidence" in pred:
                    score = float(pred["confidence"])
                else:
                    score = float(pred.get("score", 0) or 0) * 100

                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.progress(
                        min(int(score), 100),
                        text=f"{i}. {label.replace('_', ' ').title()}",
                    )
                with col_b:
                    st.markdown(
                        f"<div style='text-align:right;font-weight:700;color:#0d9488;'>"
                        f"{score:.1f}%</div>",
                        unsafe_allow_html=True,
                    )

    st.divider()

    already_saved = st.session_state.get("meal_saved", False)
    btn_col1, btn_col2 = st.columns(2)

    with btn_col1:
        if already_saved:
            st.success("✅ Meal saved!")
        else:
            if st.button("💾 Save Meal", type="primary", width="stretch"):
                try:
                    meal_id = add_meal(
                        user_id=user_id,
                        food_name=display_food_name,
                        meal_type=saved_meal_type,
                        calories=float(nutrition.get("calories", 0) or 0),
                        protein=float(nutrition.get("protein",  0) or 0),
                        carbs=float(nutrition.get("carbs",    0) or 0),
                        fat=float(nutrition.get("fat",      0) or 0),
                        confidence=confidence,
                        health_score=int(nutrition.get("health_score", 65) or 65),
                        image_name=image_name,
                        notes="Saved from AI Food Scan",
                    )
                    st.session_state["meal_saved"] = True
                    st.cache_data.clear()
                    st.success(f"✅ Saved! Meal ID: {meal_id}")
                    st.rerun()

                except Exception as e:
                    st.error(f"❌ Save failed: {e}")

    with btn_col2:
        if st.button("📊 View Nutrition Details →", width="stretch"):
            st.switch_page("pages/2_Nutrition_Result.py")


render_footer()