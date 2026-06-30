"""NutriSense AI — User Health Profile"""

from __future__ import annotations
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import streamlit as st

from src.utils.ui import (
    render_app_layout, render_page_header, render_footer,
    render_info_box, card_header,
)
from src.utils.helpers import get_active_user_id
from src.database.user import get_user_profile, update_user_profile
from src.ai.calorie_calculator import calculate_calorie_goal

st.set_page_config(
    page_title="My Profile — NutriSense AI",
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="expanded",
)

if not st.session_state.get("authenticated"):
    from streamlit_app.Account import render_account_page
    render_account_page()
    st.stop()

user_id = get_active_user_id()
profile = get_user_profile(user_id)

render_app_layout(active_page="profile")
render_page_header("👤 My Health Profile", "Manage your personal information and health goals")

col1, col2 = st.columns([1, 1])

with col1:
    with st.container(border=True):
        card_header("Personal Information", "Basic details", icon="📋")

        name = st.text_input("Full Name", value=profile.get("name", ""))
        age = st.number_input("Age", 10, 120, int(profile.get("age", 25) or 25))
        gender = st.selectbox(
            "Gender",
            ["Not specified", "Male", "Female", "Other"],
            index=["Not specified", "Male", "Female", "Other"].index(
                profile.get("gender", "Not specified") or "Not specified"
            ),
        )

    with st.container(border=True):
        card_header("Body Measurements", "Used for BMI and calorie calculations", icon="📏")

        height_cm = st.number_input(
            "Height (cm)", 100.0, 250.0,
            float(profile.get("height_cm", 170) or 170), 0.5,
        )
        weight_kg = st.number_input(
            "Weight (kg)", 30.0, 300.0,
            float(profile.get("weight_kg", 70) or 70), 0.5,
        )

        bmi = weight_kg / ((height_cm / 100) ** 2) if height_cm > 0 else 0
        if bmi > 0:
            if bmi < 18.5:
                cat = "Underweight"
                cls = "warn"
            elif bmi < 25:
                cat = "Normal"
                cls = "success"
            elif bmi < 30:
                cat = "Overweight"
                cls = "warn"
            else:
                cat = "Obese"
                cls = "error"

            render_info_box(
                f"**BMI:** {bmi:.1f} — **{cat}**",
                cls,
            )

with col2:
    with st.container(border=True):
        card_header("Health & Diet", "Preferences and restrictions", icon="🥗")

        dietary_preference = st.selectbox(
            "Dietary Preference",
            ["None", "Vegetarian", "Vegan", "Keto", "Low-Carb", "High-Protein", "Mediterranean", "Halal"],
            index=["None", "Vegetarian", "Vegan", "Keto", "Low-Carb", "High-Protein", "Mediterranean", "Halal"].index(
                profile.get("dietary_preference", "None") or "None"
            ),
        )
        allergies = st.text_area(
            "Allergies (comma separated)",
            value=profile.get("allergies", ""),
            placeholder="e.g. peanuts, dairy, gluten",
        )
        medical_conditions = st.text_area(
            "Medical Conditions",
            value=profile.get("medical_conditions", ""),
            placeholder="e.g. diabetes, hypertension",
        )

    with st.container(border=True):
        card_header("Goals & Activity", "Your fitness targets", icon="🎯")

        goal_options = ["Lose Weight", "Gain Muscle", "Maintain Weight", "Healthy Lifestyle"]
        default_goal = profile.get("goal_type") or profile.get("goal") or "Maintain Weight"
        if default_goal not in goal_options:
            default_goal = "Maintain Weight"
        goal = st.selectbox("Health Goal", goal_options, index=goal_options.index(default_goal))

        activity_options = ["Sedentary", "Light", "Moderate", "Active", "Very Active"]
        default_activity = profile.get("activity_level", "Moderate") or "Moderate"
        if default_activity not in activity_options:
            default_activity = "Moderate"
        activity_level = st.selectbox(
            "Activity Level",
            activity_options,
            index=activity_options.index(default_activity),
        )

        if age and height_cm and weight_kg and gender != "Not specified":
            sex = "Male" if gender == "Male" else "Female"
            goal_type_map = {
                "Lose Weight": "Lose Weight",
                "Gain Muscle": "Gain Weight",
                "Maintain Weight": "Maintain",
                "Healthy Lifestyle": "Maintain",
            }
            daily_cal = calculate_calorie_goal(
                weight=weight_kg, height=height_cm, age=age,
                sex=sex, activity=activity_level,
                goal_type=goal_type_map.get(goal, "Maintain"),
            )
            st.markdown(
                f"<div style='background:#ecfdf5;border:1px solid #99f6e4;border-radius:10px;"
                f"padding:0.75rem 1rem;margin-top:0.5rem;'>"
                f"<strong>Recommended Daily Calories:</strong> {daily_cal:,} kcal</div>",
                unsafe_allow_html=True,
            )

save_btn = st.button("💾 Save Profile", type="primary", use_container_width=True)

if save_btn:
    try:
        goal_type_map = {
            "Lose Weight": "Weight Loss",
            "Gain Muscle": "Weight Gain",
            "Maintain Weight": "Maintenance",
            "Healthy Lifestyle": "Healthy Lifestyle",
        }
        sex = "Male" if gender == "Male" else "Female"
        daily_cal = (
            calculate_calorie_goal(
                weight=weight_kg, height=height_cm, age=age,
                sex=sex, activity=activity_level,
                goal_type=goal_type_map.get(goal, "Maintain"),
            )
            if age and height_cm and weight_kg and gender != "Not specified"
            else 2000
        )

        update_user_profile(
            user_id=user_id,
            name=name, age=age, gender=gender,
            height_cm=height_cm, weight_kg=weight_kg,
            dietary_preference=dietary_preference,
            allergies=allergies, medical_conditions=medical_conditions,
            activity_level=activity_level,
        )

        from src.database.user import update_user_goal as _update_goal
        _update_goal(goal_type_map.get(goal, "Maintenance"), daily_cal, activity_level, user_id=user_id)

        st.success("✅ Profile saved successfully!")
        st.rerun()
    except Exception as e:
        st.error(f"❌ Failed to save: {e}")

render_footer()
