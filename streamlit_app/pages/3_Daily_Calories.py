"""NutriSense AI — Daily Calories"""

from __future__ import annotations

import os
import sys

sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
)

import streamlit as st
import plotly.graph_objects as go

from src.utils.ui import (
    render_app_layout,
    render_page_header,
    render_stat_card,
    render_info_box,
    plotly_layout,
    render_footer,
)
from src.utils.cards import render_progress_ring, card_header
from src.utils.helpers import get_active_user_id
from src.database.meals import get_today_summary
from src.ai.calorie_calculator import calculate_calorie_goal


st.set_page_config(
    page_title="NutriSense AI — Calories",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded",
)


render_app_layout(active_page="calories")
render_page_header(
    "Daily Calories",
    "Track your intake against your personalised daily goal"
)


user_id = get_active_user_id()
summary = get_today_summary(user_id)

calories_today = float(summary.get("calories", 0) or 0)
calorie_goal = float(summary.get("calorie_goal", 2200) or 2200)
remaining = max(calorie_goal - calories_today, 0)
pct = summary.get("goal_progress", 0) or 0


# ── Stat row ──────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)

with c1:
    render_stat_card(
        title="Consumed",
        value=f"{calories_today:,.0f} kcal",
        subtitle="Logged today",
        icon="🍽️",
        color="#0d9488",
    )

with c2:
    render_stat_card(
        title="Remaining",
        value=f"{remaining:,.0f} kcal",
        subtitle="Left today",
        icon="⏳",
        color="#f59e0b",
    )

with c3:
    render_stat_card(
        title="Daily Goal",
        value=f"{calorie_goal:,.0f} kcal",
        subtitle="Target",
        icon="🎯",
        color="#0284c7",
    )

with c4:
    render_stat_card(
        title="Progress",
        value=f"{pct}%",
        subtitle="Goal achieved",
        icon="📈",
        color="#7c3aed",
    )


# ── Ring + status ─────────────────────────────────────────────────────────────
ring_col, info_col = st.columns([1, 2], gap="medium")

with ring_col:
    with st.container(border=True):
        card_header("Goal Progress")
        render_progress_ring(pct, "Daily Progress")

with info_col:
    with st.container(border=True):
        card_header("Today's Status")

        if pct >= 100:
            render_info_box(
                "🎉 <strong>Daily calorie goal reached!</strong> Great work — maintain balanced portions for the rest of the day.",
                "success",
            )
        elif pct >= 80:
            render_info_box(
                f"⚠️ At <strong>{pct}%</strong> of goal — plan a lighter next meal to avoid going over.",
                "warn",
            )
        elif pct >= 50:
            render_info_box(
                f"ℹ️ Halfway there — <strong>{remaining:,.0f} kcal</strong> remaining. Stay consistent with your meal timing.",
                "info",
            )
        else:
            render_info_box(
                f"ℹ️ <strong>{remaining:,.0f} kcal</strong> remaining today. Log your meals regularly for better AI insights.",
                "info",
            )

        st.markdown(
            "<div style='margin:0.5rem 0'></div>",
            unsafe_allow_html=True,
        )

        st.markdown("**Macro Progress (today)**", help="Based on logged meals")

        protein = float(summary.get("protein", 0) or 0)
        carbs = float(summary.get("carbs", 0) or 0)
        fat = float(summary.get("fat", 0) or 0)

        from src.utils.cards import render_progress_bar

        render_progress_bar(
            min(protein / 120 * 100, 100),
            f"Protein {protein:.0f}g",
            "120g goal",
        )
        render_progress_bar(
            min(carbs / 250 * 100, 100),
            f"Carbs {carbs:.0f}g",
            "250g goal",
        )
        render_progress_bar(
            min(fat / 65 * 100, 100),
            f"Fat {fat:.0f}g",
            "65g goal",
        )


# ── Weekly trend ──────────────────────────────────────────────────────────────
with st.container(border=True):
    card_header("7-Day Calorie Trend", "daily intake vs goal")

    weekly_labels = summary.get("weekly_labels", [])
    weekly_calories = summary.get("weekly_calories", [])

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=weekly_labels,
            y=weekly_calories,
            mode="lines+markers",
            line=dict(color="#0d9488", width=2.5),
            marker=dict(size=6, color="#0d9488", line=dict(width=2, color="#fff")),
            fill="tozeroy",
            fillcolor="rgba(13,148,136,0.07)",
            name="Calories",
        )
    )

    fig.add_hline(
        y=calorie_goal,
        line_dash="dash",
        line_color="#0284c7",
        line_width=1.5,
        annotation_text="Daily Goal",
        annotation_font_size=10,
    )

    fig.update_layout(**plotly_layout())
    fig.update_layout(height=220, showlegend=False)

    try:
        st.plotly_chart(fig, width="stretch")
    except TypeError:
        st.plotly_chart(fig, use_container_width=True)


# ── Calorie calculator ────────────────────────────────────────────────────────
with st.expander("🔢  Recalculate Your Daily Goal", expanded=False):
    st.markdown(
        "<div style='margin-bottom:0.5rem;font-size:0.8rem;color:#64748b'>Uses Mifflin-St Jeor equation + activity multiplier</div>",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        weight = st.number_input("Weight (kg)", 30.0, 200.0, 70.0, 0.5)
        height = st.number_input("Height (cm)", 120.0, 220.0, 170.0, 0.5)

    with col2:
        age = st.number_input("Age", 10, 100, 25, 1)
        sex = st.selectbox("Sex", ["Male", "Female"])

    with col3:
        activity = st.selectbox(
            "Activity Level",
            ["Sedentary", "Light", "Moderate", "Active", "Very Active"],
        )
        goal_type = st.selectbox(
            "Goal",
            ["Maintain", "Lose Weight", "Gain Weight"],
        )

    if st.button("Calculate →", type="primary"):
        new_goal = calculate_calorie_goal(
            weight=weight,
            height=height,
            age=age,
            sex=sex,
            activity=activity,
            goal_type=goal_type,
        )

        st.success(f"✅ Estimated daily goal: **{new_goal:,} kcal**")
        st.caption("Update your profile in Account settings to apply this goal.")


render_footer()