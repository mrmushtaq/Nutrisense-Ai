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


# ── Stat row ──────────────────────────────────────────────────────────────────
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
        title="Goal Progress",
        value=f"{pct}%",
        subtitle="Of daily target",
        icon="🎯",
        color="#7c3aed",
    )


# ── AI Insight ────────────────────────────────────────────────────────────────
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


# ── Quick action ──────────────────────────────────────────────────────────────
if st.button("📸  Scan a Meal", type="primary"):
    st.switch_page("pages/1_Upload_Food.py")

st.markdown("<div style='margin:0.25rem 0'></div>", unsafe_allow_html=True)


# ── Recent meals + weekly chart ───────────────────────────────────────────────
left_col, right_col = st.columns([1, 1])

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

        if st.button("View Full History →", key="to_history"):
            st.switch_page("pages/4_Meal_History.py")


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