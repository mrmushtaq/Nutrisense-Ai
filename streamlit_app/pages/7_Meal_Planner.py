"""NutriSense AI — Smart Meal Planner"""

from __future__ import annotations
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import streamlit as st

from src.utils.ui import (
    render_app_layout, render_page_header, render_footer,
    render_info_box, card_header,
)
from src.utils.helpers import get_active_user_id
from src.database.user import get_user_profile
from src.ai_agent.meal_planner import generate_daily_plan, generate_weekly_plan, MEAL_TIMES
from src.ai_agent.meal_validator import generate_ingredient_grocery_list

st.set_page_config(
    page_title="Meal Planner — NutriSense AI",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded",
)

if not st.session_state.get("authenticated"):
    from streamlit_app.Account import render_account_page
    render_account_page()
    st.stop()

user_id = get_active_user_id()
profile = get_user_profile(user_id)

render_app_layout(active_page="meal_planner")
render_page_header("📅 Smart Meal Planner", "AI-generated meal plans tailored to your goals")

goal_type = profile.get("goal_type") or profile.get("goal") or "Maintenance"

goal_options = ["Weight Loss", "Weight Gain", "Maintenance", "Healthy Lifestyle"]
if goal_type not in goal_options:
    goal_type = "Maintenance"

dietary_pref = profile.get("dietary_preference", "None") or "None"
allergies_str = profile.get("allergies", "") or ""

plan_duration = st.radio("Plan Duration", ["Daily", "Weekly"], horizontal=True)

goal_override = st.selectbox("Goal", goal_options, index=goal_options.index(goal_type))

calorie_input = st.number_input(
    "Daily Calorie Target (optional, 0 = auto)",
    min_value=0, max_value=5000, value=0, step=50,
)

from src.ai.calorie_calculator import calculate_calorie_goal

target_cal = calorie_input if calorie_input > 0 else None

if not target_cal and profile.get("age") and profile.get("height_cm") and profile.get("weight_kg"):
    sex = "Male" if profile.get("gender") == "Male" else "Female"
    activity = profile.get("activity_level", "Moderate") or "Moderate"
    goal_map = {"Weight Loss": "Lose Weight", "Weight Gain": "Gain Weight", "Maintenance": "Maintain", "Healthy Lifestyle": "Maintain"}
    target_cal = calculate_calorie_goal(
        weight=float(profile.get("weight_kg", 70)),
        height=float(profile.get("height_cm", 170)),
        age=int(profile.get("age", 25) or 25),
        sex=sex, activity=activity,
        goal_type=goal_map.get(goal_override, "Maintain"),
    )

if st.button("🚀 Generate Plan", type="primary", use_container_width=True):
    allergies_list = [a.strip().lower() for a in allergies_str.split(",") if a.strip()]
    medical_str = profile.get("medical_conditions", "") or ""
    medical_list = [m.strip().lower() for m in medical_str.split(",") if m.strip()]
    weight_kg = profile.get("weight_kg")

    with st.spinner("🧠 Generating your meal plan..."):
        if plan_duration == "Daily":
            plan = generate_daily_plan(
                goal_type=goal_override,
                calorie_target=target_cal,
                dietary_preference=dietary_pref,
                allergies=allergies_list,
                medical_conditions=medical_list,
                weight_kg=weight_kg,
            )
            st.session_state["meal_plan"] = plan
            st.session_state["meal_plan_duration"] = "daily"
        else:
            plan = generate_weekly_plan(
                goal_type=goal_override,
                calorie_target=target_cal,
                dietary_preference=dietary_pref,
                allergies=allergies_list,
                medical_conditions=medical_list,
                weight_kg=weight_kg,
            )
            st.session_state["meal_plan"] = plan
            st.session_state["meal_plan_duration"] = "weekly"

    st.rerun()

# ── Display Plan ──────────────────────────────────────────────────────────────
if "meal_plan" in st.session_state:
    st.markdown("<div style='margin:1rem 0'></div>", unsafe_allow_html=True)

    def _check_icon(passed: bool) -> str:
        return "✅" if passed else "❌"

    def _render_constraint_checklist(validation: dict) -> None:
        if not validation or "checks" not in validation:
            return
        checks = validation["checks"]
        with st.container(border=True):
            card_header("📋 Requirements Verification", "Auto-verified against your profile", icon="✅")
            for check in checks:
                icon = _check_icon(check["passed"])
                detail = check.get("actual", "")
                target = check.get("target", "")
                st.markdown(
                    f"<div style='display:flex;align-items:center;gap:0.5rem;"
                    f"padding:0.3rem 0;font-size:0.9rem;'>"
                    f"<span>{icon}</span>"
                    f"<span><strong>{check['name']}:</strong> {detail} "
                    f"<span style='color:#94a3b8;font-size:0.8rem;'>(target: {target})</span></span>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

    def _render_daily_summary(plan: dict) -> None:
        totals = plan["totals"]
        target_cal = plan.get("target_calories", 2000)
        macro_targets = plan.get("macro_targets", {})

        cal_pass = abs(totals["calories"] - target_cal) <= target_cal * 0.15
        protein_target = macro_targets.get("protein", 80)
        protein_pass = totals["protein"] >= protein_target * 0.9
        fiber_target = macro_targets.get("fiber", 25)
        fiber_pass = sum(plan["meals"][mt].get("fiber", 0) for mt in MEAL_TIMES if mt in plan["meals"]) >= fiber_target * 0.7

        cols = st.columns([1, 1, 1, 1])
        with cols[0]:
            st.markdown(
                f"<div style='background:white;border:1px solid #e5e7eb;border-radius:12px;"
                f"padding:0.75rem;text-align:center;'>"
                f"<div style='font-size:0.75rem;color:#64748b;'>Calories</div>"
                f"<div style='font-size:1.3rem;font-weight:800;'>{totals['calories']} / {target_cal} "
                f"<span style='font-size:1rem;'>{_check_icon(cal_pass)}</span></div>"
                f"</div>", unsafe_allow_html=True,
            )
        with cols[1]:
            st.markdown(
                f"<div style='background:white;border:1px solid #e5e7eb;border-radius:12px;"
                f"padding:0.75rem;text-align:center;'>"
                f"<div style='font-size:0.75rem;color:#64748b;'>Protein</div>"
                f"<div style='font-size:1.3rem;font-weight:800;'>{totals['protein']} / {protein_target}g "
                f"<span style='font-size:1rem;'>{_check_icon(protein_pass)}</span></div>"
                f"</div>", unsafe_allow_html=True,
            )
        with cols[2]:
            st.markdown(
                f"<div style='background:white;border:1px solid #e5e7eb;border-radius:12px;"
                f"padding:0.75rem;text-align:center;'>"
                f"<div style='font-size:0.75rem;color:#64748b;'>Carbs</div>"
                f"<div style='font-size:1.3rem;font-weight:800;'>{totals['carbs']}g</div>"
                f"</div>", unsafe_allow_html=True,
            )
        with cols[3]:
            st.markdown(
                f"<div style='background:white;border:1px solid #e5e7eb;border-radius:12px;"
                f"padding:0.75rem;text-align:center;'>"
                f"<div style='font-size:0.75rem;color:#64748b;'>Fat</div>"
                f"<div style='font-size:1.3rem;font-weight:800;'>{totals['fat']}g</div>"
                f"</div>", unsafe_allow_html=True,
            )

    if st.session_state["meal_plan_duration"] == "daily":
        plan = st.session_state["meal_plan"]
        meals = plan["meals"]
        totals = plan["totals"]

        # Conflict warning
        if plan.get("conflict_warning"):
            render_info_box(f"🧠 {plan['conflict_warning']}", "warn")

        # Summary banner
        st.markdown(
            f"<div style='background:#ecfdf5;border:1px solid #99f6e4;border-radius:14px;"
            f"padding:1rem;margin-bottom:1rem;'>"
            f"<strong>Today's Plan</strong> — Target: {plan['target_calories']:,} kcal | "
            f"Estimated: {totals['calories']} kcal</div>",
            unsafe_allow_html=True,
        )

        # Meal cards with name, macros, and explanation
        for meal_time in ["Breakfast", "Lunch", "Dinner", "Snacks"]:
            if meal_time in meals:
                m = meals[meal_time]
                with st.container(border=True):
                    card_header(f"{meal_time}: {m['name']}", f"{m['calories']} kcal", icon="🍽️")
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Calories", f"{m['calories']} kcal")
                    c2.metric("Protein", f"{m['protein']}g")
                    c3.metric("Carbs", f"{m['carbs']}g")
                    c4.metric("Fat", f"{m['fat']}g")
                    if m.get("reason"):
                        st.markdown(
                            f"<div style='margin-top:0.5rem;font-size:0.82rem;color:#64748b;"
                            f"font-style:italic;'>💡 {m['reason']}</div>",
                            unsafe_allow_html=True,
                        )

        # Daily Nutrition Summary
        st.markdown("<div style='margin:1rem 0 0.5rem'></div>", unsafe_allow_html=True)
        st.markdown("### 📊 Daily Nutrition Summary")
        _render_daily_summary(plan)

        # Constraint checklist
        if plan.get("validation"):
            st.markdown("<div style='margin:0.75rem 0'></div>", unsafe_allow_html=True)
            _render_constraint_checklist(plan["validation"])

        if plan.get("needs_attention"):
            render_info_box(
                "⚠ Some constraints could not be fully satisfied with the available meal options. "
                "The closest possible plan is shown above.",
                "warn",
            )

    else:
        weekly = st.session_state["meal_plan"]
        for day_plan in weekly:
            day = day_plan["day"]
            meals = day_plan["meals"]
            totals = day_plan["totals"]

            with st.expander(f"📅 {day} — {totals['calories']} kcal", expanded=True):
                cols = st.columns(4)
                for i, mt in enumerate(["Breakfast", "Lunch", "Dinner", "Snacks"]):
                    if mt in meals:
                        m = meals[mt]
                        with cols[i]:
                            st.markdown(
                                f"<div style='background:white;border:1px solid #e5e7eb;"
                                f"border-radius:10px;padding:0.75rem;text-align:center;'>"
                                f"<strong>{mt}</strong><br>"
                                f"{m['name']}<br>"
                                f"<span style='color:#0d9488;font-weight:700;'>{m['calories']} kcal</span>"
                                f"<br><small>P:{m['protein']}g C:{m['carbs']}g F:{m['fat']}g</small>"
                                f"</div>",
                                unsafe_allow_html=True,
                            )

        # Weekly constraint checklist (aggregate from first day)
        if weekly and weekly[0].get("validation"):
            st.markdown("<div style='margin:1rem 0'></div>", unsafe_allow_html=True)
            _render_constraint_checklist(weekly[0]["validation"])

    # ── Grocery List Generator (from actual ingredients) ───────────────────────
    st.markdown("<div style='margin:1.5rem 0 0.5rem'></div>", unsafe_allow_html=True)
    with st.container(border=True):
        card_header("🛒 Grocery List", "Ingredients needed for this meal plan", icon="🛒")

        plan_data = st.session_state["meal_plan"]

        if st.button("Generate Grocery List", type="primary", key="gen_grocery"):
            grocery = generate_ingredient_grocery_list(plan_data)
            st.session_state["grocery_data"] = grocery

            lines = []
            for category, items in grocery.items():
                if items:
                    lines.append(f"{category}")
                    for item in items:
                        lines.append(f"  • {item}")
                    lines.append("")
            st.session_state["grocery_list_text"] = "\n".join(lines).strip()

        if "grocery_list_text" in st.session_state and st.session_state["grocery_list_text"]:
            st.text_area(
                "🛒 Shopping List",
                value=st.session_state["grocery_list_text"],
                height=220,
                key="grocery_display",
            )

            if st.button("📋 Copy to Clipboard", key="copy_grocery"):
                st.toast("📋 Copied! Press Ctrl+C to copy the text above.")

else:
    render_info_box(
        "Set your preferences and click **Generate Plan** to create a personalised meal plan.",
        "info",
    )

render_footer()
