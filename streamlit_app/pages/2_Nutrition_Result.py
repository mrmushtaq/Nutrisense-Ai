"""NutriSense AI — Nutrition Result"""

from __future__ import annotations
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import streamlit as st
import plotly.graph_objects as go

from src.utils.ui import (
    render_app_layout, render_page_header, render_metric_card,
    render_empty_state, plotly_layout, render_footer,
)
from src.utils.cards import (
    render_footer, render_health_badge, render_ai_summary_card, card_header,
)
from src.utils.helpers import get_active_user_id
from src.database.meals import get_latest_meal

st.set_page_config(page_title="NutriSense AI — Nutrition", page_icon="📊", layout="wide", initial_sidebar_state="expanded")
render_app_layout(active_page="nutrition")
render_page_header("Nutrition Report", "Full macro and health breakdown of your latest meal")

user_id = get_active_user_id()
meal    = get_latest_meal(user_id)

if not meal:
    render_empty_state("🧪", "No meal analysed yet", "Scan food on the Food Scan page to see your nutrition report.")
    if st.button("Go to Food Scan →", type="primary"):
        st.switch_page("pages/1_Upload_Food.py")
    render_footer()
    st.stop()

score       = meal.get("health_score", 0)
calories    = meal.get("calories", 1) or 1
protein_pct = meal["protein"] * 4 / calories * 100 if calories else 0
carbs_pct   = meal["carbs"]   * 4 / calories * 100 if calories else 0
fat_pct     = meal["fat"]     * 9 / calories * 100 if calories else 0

# ── Header row ────────────────────────────────────────────────────────────────
top_l, top_r = st.columns([3, 1])
with top_l:
    st.markdown(f"### {meal['food_name']}")
    conf = meal.get("confidence", 0)
    st.caption(f"{meal.get('meal_type', 'Meal')} · {meal.get('analysis_date', '')} · {conf:.0f}% confidence")
with top_r:
    st.markdown(render_health_badge(score), unsafe_allow_html=True)

# ── Key metrics ───────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
with c1:
    render_metric_card("Calories", f"{meal['calories']}", "kcal",  "🔥", "#0d9488")
with c2:
    render_metric_card("Protein",  f"{meal['protein']}g", "macro", "🥩", "#0284c7")
with c3:
    render_metric_card("Carbs",    f"{meal['carbs']}g",   "macro", "🌾", "#f59e0b")
with c4:
    render_metric_card("Fat",      f"{meal['fat']}g",     "macro", "🧈", "#7c3aed")

# ── Charts row ────────────────────────────────────────────────────────────────
bar_col, pie_col = st.columns([3, 2])

with bar_col:
    with st.container(border=True):
        card_header("Macro Breakdown", "grams per macronutrient")
        fig = go.Figure(data=[go.Bar(
            x=["Protein", "Carbs", "Fat"],
            y=[meal["protein"], meal["carbs"], meal["fat"]],
            marker_color=["#0284c7", "#f59e0b", "#7c3aed"],
            marker_opacity=0.85,
            text=[f"{meal['protein']}g", f"{meal['carbs']}g", f"{meal['fat']}g"],
            textposition="outside",
            textfont=dict(size=11),
        )])
        fig.update_layout(**plotly_layout(), height=200, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

with pie_col:
    with st.container(border=True):
        card_header("Calorie Distribution", "% of total kcal")
        fig2 = go.Figure(data=[go.Pie(
            labels=["Protein", "Carbs", "Fat"],
            values=[round(protein_pct, 1), round(carbs_pct, 1), round(fat_pct, 1)],
            marker=dict(colors=["#0284c7", "#f59e0b", "#7c3aed"]),
            hole=0.5,
            textinfo="percent",
            textfont=dict(size=11),
        )])
        fig2.update_layout(**plotly_layout(), height=200, showlegend=True,
                           legend=dict(orientation="h", y=-0.15, font=dict(size=10)))
        st.plotly_chart(fig2, use_container_width=True)

# ── AI Summary ────────────────────────────────────────────────────────────────
if protein_pct >= 25:
    summary = "Strong protein content — great for muscle recovery and satiety. Pair with fibre-rich vegetables for a balanced plate."
elif calories >= 500:
    summary = "Calorie-dense meal. Consider lighter portions or a lower-calorie next meal to stay within your daily goal."
elif score >= 75:
    summary = "Excellent nutritional balance. This meal supports your health goals well — keep it consistent."
else:
    summary = "Well-portioned meal. Consistent logging helps your AI coach fine-tune personalised recommendations over time."

render_ai_summary_card(summary)

# ── Navigation ────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔥  Daily Calories", type="primary", use_container_width=True):
        st.switch_page("pages/3_Daily_Calories.py")
with col2:
    if st.button("📋  Meal History", use_container_width=True):
        st.switch_page("pages/4_Meal_History.py")
with col3:
    if st.button("📸  Scan Another", use_container_width=True):
        st.switch_page("pages/1_Upload_Food.py")

render_footer()
