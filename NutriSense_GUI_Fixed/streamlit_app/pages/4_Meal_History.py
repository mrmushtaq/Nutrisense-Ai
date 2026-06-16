"""NutriSense AI — Meal History"""

from __future__ import annotations
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import datetime as dt
import streamlit as st

from src.utils.ui import render_app_layout, render_footer
from src.utils.helpers import get_active_user_id
from src.database.meals import get_meals_by_date_range, delete_meal

st.set_page_config(page_title="NutriSense AI — History", page_icon="📋", layout="wide", initial_sidebar_state="expanded")
render_app_layout(active_page="history")

user_id = get_active_user_id()

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.block-container { padding: 1.5rem 2rem 2rem; max-width: 1200px; }

/* ── Page header ── */
.ns-page-header { margin-bottom: 1.75rem; }
.ns-page-header h1 { font-size: 1.9rem; font-weight: 700; color: #0f172a; margin: 0 0 0.25rem; letter-spacing: -0.5px; }
.ns-page-header p  { font-size: 0.95rem; color: #64748b; margin: 0; }

/* ── Card shell ── */
.ns-card {
    background: #ffffff;
    border-radius: 16px;
    border: 1px solid #e8edf3;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06), 0 1px 3px rgba(0,0,0,0.04);
    padding: 1.4rem 1.5rem;
    margin-bottom: 1.25rem;
}
.ns-card-title { font-size: 0.95rem; font-weight: 600; color: #0f172a; margin: 0 0 0.2rem; }
.ns-card-sub   { font-size: 0.78rem; color: #94a3b8; margin: 0 0 1.1rem; }
.ns-card-header-row {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    margin-bottom: 1.1rem;
}
.ns-card-count {
    font-size: 0.78rem;
    color: #94a3b8;
    background: #f1f5f9;
    border-radius: 20px;
    padding: 0.2rem 0.65rem;
    font-weight: 500;
}

/* ── Stat tiles ── */
.ns-stat-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 1.25rem; }
.ns-stat-tile {
    background: #fff;
    border-radius: 14px;
    border: 1px solid #e8edf3;
    box-shadow: 0 1px 6px rgba(0,0,0,0.05);
    padding: 1.1rem 1.25rem;
    display: flex;
    align-items: center;
    gap: 1rem;
}
.ns-stat-icon {
    width: 44px; height: 44px;
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.3rem;
    flex-shrink: 0;
}
.ns-stat-val  { font-size: 1.3rem; font-weight: 700; color: #0f172a; line-height: 1.2; }
.ns-stat-name { font-size: 0.72rem; color: #94a3b8; font-weight: 500; text-transform: uppercase; letter-spacing: 0.04em; margin-top: 0.15rem; }
.ns-stat-hint { font-size: 0.72rem; color: #94a3b8; margin-top: 0.1rem; }

/* ── Filter card ── */
.ns-filter-card {
    background: #fff;
    border-radius: 16px;
    border: 1px solid #e8edf3;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    padding: 1.2rem 1.5rem 0.5rem;
    margin-bottom: 1.25rem;
}
.ns-filter-title { font-size: 0.95rem; font-weight: 600; color: #0f172a; margin: 0 0 1rem; }

/* ── Meal row card ── */
.ns-meal-row {
    background: #fff;
    border: 1px solid #e8edf3;
    border-radius: 14px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.7rem;
    display: flex;
    align-items: center;
    gap: 1.25rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    transition: box-shadow 0.15s;
}
.ns-meal-row:hover { box-shadow: 0 4px 14px rgba(0,0,0,0.09); }

.ns-meal-avatar {
    width: 44px; height: 44px;
    border-radius: 12px;
    background: linear-gradient(135deg, #f0fdf8, #e0f2fe);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.4rem;
    flex-shrink: 0;
}
.ns-meal-main   { flex: 1; min-width: 0; }
.ns-meal-name   { font-size: 0.95rem; font-weight: 600; color: #0f172a; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.ns-meal-meta   { font-size: 0.75rem; color: #94a3b8; margin-top: 0.15rem; }

.ns-meal-macros { display: flex; gap: 1rem; flex-shrink: 0; }
.ns-macro       { text-align: center; }
.ns-macro-val   { font-size: 0.88rem; font-weight: 700; color: #1e293b; }
.ns-macro-key   { font-size: 0.65rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.04em; }

.ns-meal-badge  {
    border-radius: 20px;
    padding: 0.2rem 0.65rem;
    font-size: 0.72rem;
    font-weight: 600;
    white-space: nowrap;
    flex-shrink: 0;
}
.ns-meal-badge.excellent { background: #d1fae5; color: #065f46; }
.ns-meal-badge.good      { background: #dcfce7; color: #166534; }
.ns-meal-badge.moderate  { background: #fef9c3; color: #854d0e; }
.ns-meal-badge.low       { background: #fee2e2; color: #991b1b; }

.ns-type-pill {
    display: inline-block;
    background: #eff6ff;
    color: #1d4ed8;
    border-radius: 12px;
    padding: 0.15rem 0.55rem;
    font-size: 0.7rem;
    font-weight: 600;
    margin-left: 0.45rem;
}

/* ── Empty state ── */
.ns-empty {
    text-align: center;
    padding: 3rem 1rem;
    color: #94a3b8;
}
.ns-empty-icon { font-size: 2.8rem; margin-bottom: 0.75rem; }
.ns-empty-title { font-size: 1rem; font-weight: 600; color: #64748b; margin-bottom: 0.4rem; }
.ns-empty-sub   { font-size: 0.85rem; color: #94a3b8; }

/* ── Divider ── */
.ns-divider { height: 1px; background: #e8edf3; margin: 0.9rem 0; border: none; }

/* ── Buttons ── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #14b8a6, #0ea5e9) !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    color: #fff !important;
    box-shadow: 0 2px 8px rgba(20,184,166,0.28) !important;
}
.stButton > button[kind="secondary"] {
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    border: 1.5px solid #e2e8f0 !important;
    color: #475569 !important;
}
/* Delete button — red tint */
.stButton > button[kind="secondary"]:has(> div > p:contains("🗑️")) {
    border-color: #fecaca !important;
    color: #dc2626 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Page header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="ns-page-header">
    <h1>📋 Meal History</h1>
    <p>Browse, search and manage your complete meal log</p>
</div>
""", unsafe_allow_html=True)

# ── Filter card ───────────────────────────────────────────────────────────────
st.markdown('<div class="ns-filter-card"><div class="ns-filter-title">🔍 Search & Filter</div>', unsafe_allow_html=True)
f1, f2, f3, f4 = st.columns(4)
with f1:
    search = st.text_input("Search food", placeholder="e.g. Biryani", label_visibility="visible")
with f2:
    meal_type_filter = st.selectbox("Meal type", ["All", "Breakfast", "Lunch", "Dinner", "Snack"])
with f3:
    start_date = st.date_input("From", value=dt.date.today() - dt.timedelta(days=7))
with f4:
    end_date = st.date_input("To", value=dt.date.today())
st.markdown("</div>", unsafe_allow_html=True)

# ── Fetch & filter ────────────────────────────────────────────────────────────
meals = get_meals_by_date_range(start_date, end_date, user_id=user_id)
if search:
    meals = [m for m in meals if search.lower() in m["food_name"].lower()]
if meal_type_filter != "All":
    meals = [m for m in meals if (m.get("meal_type") or "").lower() == meal_type_filter.lower()]

# ── Summary stats ─────────────────────────────────────────────────────────────
if meals:
    total_cal  = sum(m["calories"] for m in meals)
    avg_health = sum(m.get("health_score") or 0 for m in meals) / len(meals)

    st.markdown(f"""
    <div class="ns-stat-grid">
        <div class="ns-stat-tile">
            <div class="ns-stat-icon" style="background:linear-gradient(135deg,#f0fdf8,#ccfbf1)">📋</div>
            <div>
                <div class="ns-stat-val">{len(meals)}</div>
                <div class="ns-stat-name">Total Meals</div>
                <div class="ns-stat-hint">in date range</div>
            </div>
        </div>
        <div class="ns-stat-tile">
            <div class="ns-stat-icon" style="background:linear-gradient(135deg,#fff7ed,#fed7aa)">🔥</div>
            <div>
                <div class="ns-stat-val">{total_cal:,}</div>
                <div class="ns-stat-name">Total Calories</div>
                <div class="ns-stat-hint">kcal combined</div>
            </div>
        </div>
        <div class="ns-stat-tile">
            <div class="ns-stat-icon" style="background:linear-gradient(135deg,#f0fdf4,#bbf7d0)">💚</div>
            <div>
                <div class="ns-stat-val">{avg_health:.0f}/100</div>
                <div class="ns-stat-name">Avg Health Score</div>
                <div class="ns-stat-hint">across all meals</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Meal list ─────────────────────────────────────────────────────────────────
count_label = f"{len(meals)} result{'s' if len(meals) != 1 else ''}"
st.markdown(f"""
<div class="ns-card">
    <div class="ns-card-header-row">
        <div class="ns-card-title">Logged Meals</div>
        <span class="ns-card-count">{count_label}</span>
    </div>
""", unsafe_allow_html=True)

if not meals:
    st.markdown("""
    <div class="ns-empty">
        <div class="ns-empty-icon">📋</div>
        <div class="ns-empty-title">No meals found</div>
        <div class="ns-empty-sub">Adjust the filters above, or scan a new meal on the Food Scan page.</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    _, center, _ = st.columns([2, 1, 2])
    with center:
        if st.button("📸  Scan a Meal", type="primary", use_container_width=True):
            st.switch_page("pages/1_Upload_Food.py")
else:
    # Meal type → emoji map
    type_icons = {
        "breakfast": "🌅", "lunch": "☀️",
        "dinner": "🌙", "snack": "🍎",
    }

    for meal in meals:
        hs         = meal.get("health_score") or 0
        meal_type  = meal.get("meal_type", "Meal")
        icon       = type_icons.get(meal_type.lower(), "🍽️")
        date_str   = meal.get("analysis_date", "")
        protein    = meal.get("protein", 0)
        carbs      = meal.get("carbs", 0)
        fat        = meal.get("fat", 0)

        if hs >= 80:
            badge_cls, badge_label = "excellent", f"⭐ {hs}/100"
        elif hs >= 60:
            badge_cls, badge_label = "good",      f"✅ {hs}/100"
        elif hs >= 40:
            badge_cls, badge_label = "moderate",  f"⚠️ {hs}/100"
        else:
            badge_cls, badge_label = "low",       f"❗ {hs}/100"

        st.markdown(f"""
        <div class="ns-meal-row">
            <div class="ns-meal-avatar">{icon}</div>
            <div class="ns-meal-main">
                <div class="ns-meal-name">
                    {meal['food_name']}
                    <span class="ns-type-pill">{meal_type}</span>
                </div>
                <div class="ns-meal-meta">{date_str} · {meal['calories']} kcal</div>
            </div>
            <div class="ns-meal-macros">
                <div class="ns-macro">
                    <div class="ns-macro-val">{protein}g</div>
                    <div class="ns-macro-key">Protein</div>
                </div>
                <div class="ns-macro">
                    <div class="ns-macro-val">{carbs}g</div>
                    <div class="ns-macro-key">Carbs</div>
                </div>
                <div class="ns-macro">
                    <div class="ns-macro-val">{fat}g</div>
                    <div class="ns-macro-key">Fat</div>
                </div>
            </div>
            <div class="ns-meal-badge {badge_cls}">{badge_label}</div>
        </div>
        """, unsafe_allow_html=True)

        btn1, btn2, _ = st.columns([1, 1, 5])
        with btn1:
            if st.button("📊 Details", key=f"view_{meal['id']}", use_container_width=True):
                st.switch_page("pages/2_Nutrition_Result.py")
        with btn2:
            if st.button("🗑️ Delete", key=f"del_{meal['id']}", use_container_width=True):
                delete_meal(meal["id"])
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

render_footer()