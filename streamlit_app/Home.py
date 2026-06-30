"""NutriSense AI — Dashboard (Home)"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import plotly.graph_objects as go

from config import GOAL_RECOMMENDATIONS, build_ai_recommendation
from src.utils.ui import (
    render_app_layout,
    render_empty_state,
    plotly_layout,
    render_stat_card,
    render_ai_insight_card,
    render_footer,
    render_meal_card,
    card_header,
    render_dashboard_greeting,
)
from src.utils.cards import render_progress_ring, render_health_badge
from src.utils.helpers import get_active_user_id
from src.database.meals import get_recent_meals, get_today_summary
from src.database.user import get_user_profile


st.set_page_config(
    page_title="NutriSense AI — Dashboard",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)


if not st.session_state.get("authenticated"):
    from streamlit_app.Account import render_account_page

    render_account_page()
    st.stop()


user_id = get_active_user_id()
profile = get_user_profile(user_id)
summary = get_today_summary(user_id)

goal_type = profile.get("goal_type") or profile.get("goal") or "Maintenance"

if goal_type not in GOAL_RECOMMENDATIONS:
    goal_type = "Maintenance"

calories_today = float(summary.get("calories", 0) or 0)
calorie_goal = float(summary.get("calorie_goal", 2200) or 2200)
remaining = max(calorie_goal - calories_today, 0)

pct = summary.get("goal_progress", 0) or 0
health_score = summary.get("health_score", 75) or 75
meals_count = summary.get("meals_count", 0) or 0

user_name = profile.get("name", "Mushtaque Ali")

weight_kg = profile.get("weight_kg", 0) or 0
height_cm = profile.get("height_cm", 0) or 0
bmi = weight_kg / ((height_cm / 100) ** 2) if height_cm > 0 and weight_kg > 0 else None

# ── Water tracker from session state ──────────────────────────────────────────
if "water_intake" not in st.session_state:
    st.session_state.water_intake = 0
water_goal = 8


render_app_layout(
    active_page="home",
    calories_today=calories_today,
    daily_goal=calorie_goal,
    user_name=user_name,
)


# ── Greeting ──────────────────────────────────────────────────────────────────
render_dashboard_greeting(
    user_name=user_name,
    calories_today=calories_today,
    daily_goal=calorie_goal,
)


# ── Row 1: Stat row ───────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)

with c1:
    render_stat_card(
        title="Calories Today",
        value=f"{calories_today:,.0f}",
        subtitle=f"Goal: {calorie_goal:,.0f} kcal",
        icon="🔥",
        color="#0d9488",
    )

with c2:
    render_stat_card(
        title="Health Score",
        value=f"{health_score}",
        subtitle="Balance score",
        icon="💚",
        color="#16a34a",
    )

with c3:
    render_stat_card(
        title="Meals Logged",
        value=str(meals_count),
        subtitle="Today",
        icon="🍽️",
        color="#0284c7",
    )

with c4:
    render_stat_card(
        title=f"{'BMI: ' + f'{bmi:.1f}' if bmi else 'Set Profile'}",
        value=f"{pct}%" if bmi else "—",
        subtitle=f"{'Goal: ' + goal_type if bmi else 'Update in My Profile'}",
        icon="🎯",
        color="#7c3aed",
    )


# ── Row 2: AI Insight + Goal Card + Water ─────────────────────────────────────
insight_col, goal_col, water_col = st.columns([2, 1, 1])

with insight_col:
    ai_advice = build_ai_recommendation(goal_type, calories_today, None)

    if remaining > 400:
        insight = (
            f"You are {remaining:,.0f} kcal below your target. "
            "Add a protein-rich meal to stay on track."
        )
    elif pct >= 100:
        insight = (
            "Daily calorie goal reached. Keep portions balanced and stay hydrated "
            "for your next meal."
        )
    else:
        insight = ai_advice.get("main_advice", "Keep logging meals for better AI suggestions.")

    render_ai_insight_card(
        title="AI Insight",
        insight=insight,
        icon="🥗",
    )

with goal_col:
    with st.container(border=True):
        card_header("Today's Goal", goal_type)
        render_progress_ring(pct, "Daily Progress")

with water_col:
    with st.container(border=True):
        card_header("💧 Water", f"{st.session_state.water_intake}/{water_goal} glasses")
        w1, w2 = st.columns(2)
        with w1:
            if st.button("+1", key="water_add", use_container_width=True):
                st.session_state.water_intake = min(st.session_state.water_intake + 1, water_goal)
                st.rerun()
        with w2:
            if st.button("Reset", key="water_reset", use_container_width=True):
                st.session_state.water_intake = 0
                st.rerun()
        w_pct = min(st.session_state.water_intake / water_goal * 100, 100)
        st.progress(w_pct / 100)
        if st.session_state.water_intake >= water_goal:
            st.success("✅ Goal reached!")


# ── Row 3: Quick actions ──────────────────────────────────────────────────────
st.markdown("<div style='margin:0.5rem 0'></div>", unsafe_allow_html=True)
qa1, qa2, qa3, qa4, qa5 = st.columns(5)
with qa1:
    if st.button("📸 Scan Meal", type="primary", use_container_width=True):
        st.switch_page("pages/1_Upload_Food.py")
with qa2:
    if st.button("👤 My Profile", use_container_width=True):
        st.switch_page("pages/6_User_Profile.py")
with qa3:
    if st.button("🤖 AI Coach", use_container_width=True):
        st.switch_page("pages/5_AI_Recommendation.py")
with qa4:
    if st.button("🔥 Calories", use_container_width=True):
        st.switch_page("pages/3_Daily_Calories.py")
with qa5:
    if st.button("📜 History", use_container_width=True):
        st.switch_page("pages/4_Meal_History.py")


# ── Row 4: Motivational message ───────────────────────────────────────────────
motivational_messages = [
    "🌱 Small daily improvements lead to big results. Keep going!",
    "💪 Every healthy choice counts — you're doing great!",
    "🥗 A balanced plate is the foundation of good health.",
    "🚶 A short walk after meals helps digestion and blood sugar.",
    "💧 Stay hydrated — water is your body's best friend.",
    "🌟 Consistency beats perfection. Just keep showing up.",
]
import random
st.markdown(
    f"<div style='background:linear-gradient(135deg,#f0fdfa,#eff6ff);"
    f"border:1px solid #99f6e4;border-radius:12px;padding:0.6rem 1rem;"
    f"margin:0.5rem 0 1rem;text-align:center;font-size:0.92rem;color:#065f46;'>"
    f"{random.choice(motivational_messages)}</div>",
    unsafe_allow_html=True,
)


# ── Row 5: Recent meals + weekly chart + Progress Ring ────────────────────────
left_col, mid_col, right_col = st.columns([1.2, 0.8, 1])

with left_col:
    with st.container(border=True):
        card_header("Recent Meals", "Last 4 logged")

        recent = get_recent_meals(limit=4, user_id=user_id)

        if recent:
            for meal in recent:
                meta = f"{meal.get('analysis_date', '')} · {meal.get('meal_type', 'Meal')}"

                render_meal_card(
                    meal.get("food_name") or "Unknown",
                    meta,
                    meal.get("calories") or 0,
                    meal.get("health_score") or 0,
                    protein=meal.get("protein") or 0,
                    carbs=meal.get("carbs") or 0,
                    fat=meal.get("fat") or 0,
                )
        else:
            render_empty_state(
                "🍽️",
                "No meals yet",
                "Scan your first meal to get started.",
            )

        if st.button("View Full History \u2192", key="to_history"):
            st.switch_page("pages/4_Meal_History.py")

with mid_col:
    with st.container(border=True):
        card_header("Daily Macros", f"{meals_count} meal(s) logged")

        protein = float(summary.get("protein", 0) or 0)
        carbs = float(summary.get("carbs", 0) or 0)
        fat = float(summary.get("fat", 0) or 0)

        for name, val, target, color in [
            ("Protein", protein, 120, "#0284c7"),
            ("Carbs", carbs, 250, "#f59e0b"),
            ("Fat", fat, 70, "#ef4444"),
        ]:
            pct_m = min(round(val / target * 100) if target else 0, 100)
            st.markdown(
                f"""
                <div style="margin-bottom:.6rem;">
                    <div style="display:flex;justify-content:space-between;
                                font-size:.8rem;color:#334155;font-weight:600;margin-bottom:.2rem;">
                        <span>{name}</span>
                        <span style="color:{color}">{val:.0f}g / {target}g</span>
                    </div>
                    <div style="background:#f1f5f9;border-radius:999px;height:8px;overflow:hidden;">
                        <div style="width:{pct_m}%;background:{color};height:100%;
                                    border-radius:999px;"></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(f'<div style="margin-top:0.5rem;font-size:0.82rem;color:#64748b;">'
                    f'{render_health_badge(health_score)}</div>', unsafe_allow_html=True)

with right_col:
    with st.container(border=True):
        card_header("Weekly Calories", "vs daily goal")

        weekly_labels = summary.get("weekly_labels", [])
        weekly_calories = summary.get("weekly_calories", [])

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=weekly_labels,
                y=weekly_calories,
                marker_color="#0d9488",
                marker_opacity=0.85,
                name="Calories",
                text=[f"{v:,}" for v in weekly_calories],
                textposition="outside",
                textfont=dict(size=9, color="#64748b"),
            )
        )

        fig.add_hline(
            y=calorie_goal,
            line_dash="dash",
            line_color="#0284c7",
            line_width=1.5,
            annotation_text="Goal",
            annotation_font_size=10,
        )

        pl = plotly_layout()

        max_y = max(weekly_calories + [calorie_goal]) * 1.18 if weekly_calories else calorie_goal * 1.18

        if "yaxis" not in pl:
            pl["yaxis"] = {}

        pl["yaxis"] = dict(**pl["yaxis"], range=[0, max_y])

        fig.update_layout(**pl)
        fig.update_layout(height=220, showlegend=False)

        try:
            st.plotly_chart(fig, width="stretch")
        except TypeError:
            st.plotly_chart(fig, use_container_width=True)


render_footer()