"""NutriSense AI — Recipe Generator & Pantry Mode"""

from __future__ import annotations
import os, sys, json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import streamlit as st
import random

from src.utils.ui import (
    render_app_layout, render_page_header, render_footer,
    render_info_box, card_header,
)
from src.utils.helpers import get_active_user_id
from src.database.user import get_user_profile
from src.nutrition.nutrition_database import get_all_foods, get_food_nutrition

st.set_page_config(
    page_title="Recipe Generator — NutriSense AI",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded",
)

if not st.session_state.get("authenticated"):
    from streamlit_app.Account import render_account_page
    render_account_page()
    st.stop()

user_id = get_active_user_id()
profile = get_user_profile(user_id)

render_app_layout(active_page="recipes")
render_page_header("🍳 Recipe Generator", "Enter your available ingredients and let AI suggest healthy recipes")

# Recipe knowledge base
RECIPES = [
    {
        "name": "Chicken Biryani",
        "ingredients": ["chicken", "rice", "yogurt", "onion", "tomato", "garlic", "ginger", "biryani masala"],
        "calories": 450, "protein": 28, "carbs": 55, "fat": 14,
        "time": "45 min", "difficulty": "Medium",
        "instructions": "1. Marinate chicken with yogurt and spices for 30 min\n2. Fry onions until golden\n3. Layer chicken and parboiled rice\n4. Cook on low heat for 25 min",
    },
    {
        "name": "Daal Chawal",
        "ingredients": ["lentils", "rice", "onion", "garlic", "tomato", "cumin"],
        "calories": 380, "protein": 16, "carbs": 62, "fat": 8,
        "time": "30 min", "difficulty": "Easy",
        "instructions": "1. Boil lentils with turmeric and salt\n2. Prepare tarka with fried onions and garlic\n3. Cook rice separately\n4. Serve dal over rice",
    },
    {
        "name": "Grilled Chicken Salad",
        "ingredients": ["chicken", "lettuce", "tomato", "cucumber", "olive oil", "lemon"],
        "calories": 280, "protein": 32, "carbs": 12, "fat": 12,
        "time": "20 min", "difficulty": "Easy",
        "instructions": "1. Season chicken with salt, pepper, lemon\n2. Grill until cooked through\n3. Chop vegetables\n4. Toss everything with olive oil dressing",
    },
    {
        "name": "Vegetable Stir-fry",
        "ingredients": ["broccoli", "carrot", "bell pepper", "soy sauce", "garlic", "ginger", "oil"],
        "calories": 180, "protein": 6, "carbs": 22, "fat": 10,
        "time": "15 min", "difficulty": "Easy",
        "instructions": "1. Chop all vegetables into bite-size pieces\n2. Heat oil in a wok\n3. Stir-fry garlic and ginger\n4. Add vegetables and soy sauce, cook 5 min",
    },
    {
        "name": "Omelette with Toast",
        "ingredients": ["eggs", "bread", "onion", "tomato", "butter", "salt", "pepper"],
        "calories": 340, "protein": 22, "carbs": 24, "fat": 16,
        "time": "10 min", "difficulty": "Easy",
        "instructions": "1. Beat eggs with chopped onions and tomatoes\n2. Cook in buttered pan\n3. Toast bread\n4. Serve omelette with toast",
    },
    {
        "name": "Chicken Karahi",
        "ingredients": ["chicken", "tomato", "ginger", "garlic", "green chili", "coriander", "oil", "cumin"],
        "calories": 420, "protein": 32, "carbs": 10, "fat": 28,
        "time": "35 min", "difficulty": "Medium",
        "instructions": "1. Sauté ginger garlic in oil\n2. Add chicken and cook until white\n3. Add chopped tomatoes and spices\n4. Cook until oil separates, garnish with coriander",
    },
    {
        "name": "Fruit Smoothie Bowl",
        "ingredients": ["banana", "berries", "yogurt", "honey", "granola"],
        "calories": 290, "protein": 10, "carbs": 48, "fat": 6,
        "time": "5 min", "difficulty": "Easy",
        "instructions": "1. Blend banana, berries, and yogurt\n2. Pour into bowl\n3. Top with granola and a drizzle of honey",
    },
    {
        "name": "Egg Fried Rice",
        "ingredients": ["rice", "eggs", "carrot", "soy sauce", "oil", "spring onion"],
        "calories": 400, "protein": 16, "carbs": 52, "fat": 14,
        "time": "15 min", "difficulty": "Easy",
        "instructions": "1. Scramble eggs and set aside\n2. Stir-fry vegetables\n3. Add cold rice and soy sauce\n4. Mix in scrambled eggs",
    },
    {
        "name": "Chana Chaat",
        "ingredients": ["chickpeas", "onion", "tomato", "cucumber", "lemon", "chaat masala", "coriander"],
        "calories": 220, "protein": 10, "carbs": 34, "fat": 6,
        "time": "10 min", "difficulty": "Easy",
        "instructions": "1. Drain and rinse chickpeas\n2. Chop onion, tomato, cucumber\n3. Mix everything with chaat masala and lemon juice\n4. Garnish with coriander",
    },
    {
        "name": "Grilled Fish with Vegetables",
        "ingredients": ["fish", "broccoli", "lemon", "olive oil", "garlic", "herbs"],
        "calories": 350, "protein": 34, "carbs": 8, "fat": 18,
        "time": "25 min", "difficulty": "Medium",
        "instructions": "1. Marinate fish with lemon, garlic, herbs\n2. Grill fish 4 min each side\n3. Steam broccoli\n4. Serve fish with vegetables",
    },
]

tab1, tab2 = st.tabs(["🍳 Recipe Generator", "🥘 Pantry Mode"])

with tab1:
    with st.container(border=True):
        card_header("Your Ingredients", "Enter what you have available", icon="🥕")

        available_input = st.text_area(
            "Enter ingredients (comma separated)",
            placeholder="e.g. chicken, rice, onions, tomatoes",
            height=80,
        )

        dietary_pref = profile.get("dietary_preference", "None") or "None"
        if dietary_pref != "None":
            st.caption(f"Your dietary preference: {dietary_pref}")

        if st.button("🔍 Find Recipes", type="primary", use_container_width=True) and available_input.strip():
            ingredients = [i.strip().lower() for i in available_input.split(",") if i.strip()]
            matched = []

            for recipe in RECIPES:
                recipe_ingredients_lower = [i.lower() for i in recipe["ingredients"]]
                common = set(ingredients) & set(recipe_ingredients_lower)
                match_pct = len(common) / len(recipe_ingredients_lower) * 100 if recipe_ingredients_lower else 0

                missing = [i for i in recipe_ingredients_lower if i not in ingredients]
                matched.append((match_pct, recipe, missing))

            matched.sort(key=lambda x: x[0], reverse=True)
            top_recipes = [r for r in matched if r[0] > 0][:5]

            if top_recipes:
                st.session_state["recipe_results"] = top_recipes
                st.session_state["recipe_input"] = ingredients
            else:
                render_info_box(
                    "No recipes found with those ingredients. Try adding more common items like chicken, rice, eggs, or vegetables.",
                    "warn",
                )

    if "recipe_results" in st.session_state:
        st.markdown("<div style='margin:1rem 0'></div>", unsafe_allow_html=True)
        results = st.session_state["recipe_results"]
        ingredients = st.session_state["recipe_input"]

        st.markdown(
            f"<div style='background:#ecfdf5;border:1px solid #99f6e4;border-radius:14px;"
            f"padding:0.75rem 1rem;margin-bottom:1rem;'>"
            f"Found <strong>{len(results)}</strong> recipes using your ingredients</div>",
            unsafe_allow_html=True,
        )

        for match_pct, recipe, missing in results:
            with st.container(border=True):
                cols = st.columns([3, 1])
                with cols[0]:
                    st.markdown(f"### {recipe['name']}")
                    st.markdown(
                        f"<span style='color:#64748b;font-size:0.85rem;'>"
                        f"⏱ {recipe['time']} · {recipe['difficulty']}</span>",
                        unsafe_allow_html=True,
                    )
                with cols[1]:
                    st.markdown(
                        f"<div style='text-align:right;'>"
                        f"<span style='font-size:1.3rem;font-weight:800;color:#0d9488;'>{match_pct:.0f}%</span>"
                        f"<br><span style='font-size:0.75rem;color:#64748b;'>match</span></div>",
                        unsafe_allow_html=True,
                    )

                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Calories", f"{recipe['calories']} kcal")
                c2.metric("Protein", f"{recipe['protein']}g")
                c3.metric("Carbs", f"{recipe['carbs']}g")
                c4.metric("Fat", f"{recipe['fat']}g")

                st.markdown(f"**Ingredients:** {', '.join(i.title() for i in recipe['ingredients'])}")

                if missing:
                    st.markdown(
                        f"<span style='color:#f59e0b;font-size:0.85rem;'>"
                        f"⚠ Missing: {', '.join(i.title() for i in missing)}</span>",
                        unsafe_allow_html=True,
                    )

                with st.expander("📖 Instructions"):
                    st.markdown(recipe["instructions"])

                if st.button(f"💾 Save {recipe['name']}", key=f"save_recipe_{recipe['name']}"):
                    try:
                        from src.database.preferences import save_favorite_food
                        save_favorite_food(user_id, recipe['name'])
                        st.success(f"✅ Saved {recipe['name']} to favorites!")
                    except Exception:
                        pass

with tab2:
    render_info_box(
        "Select ingredients from the pantry below to generate recipes and meal plans.",
        "info",
    )

    all_foods = get_all_foods()
    food_names = [f["food_name"] for f in all_foods] if all_foods else [
        "Chicken", "Rice", "Eggs", "Lentils", "Tomato", "Onion", "Potato",
        "Spinach", "Carrot", "Broccoli", "Fish", "Yogurt", "Flour", "Oil",
    ]

    pantry_key = "pantry_ingredients"
    if pantry_key not in st.session_state:
        st.session_state[pantry_key] = []

    available_foods = st.multiselect(
        "What's in your pantry?",
        options=sorted(set(food_names)),
        default=st.session_state[pantry_key],
        key="pantry_multiselect",
    )
    st.session_state[pantry_key] = available_foods

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 Generate Recipes from Pantry", type="primary", use_container_width=True) and available_foods:
            ingredients = [f.lower() for f in available_foods]
            matched = []
            for recipe in RECIPES:
                recipe_ingredients_lower = [i.lower() for i in recipe["ingredients"]]
                common = set(ingredients) & set(recipe_ingredients_lower)
                match_pct = len(common) / len(recipe_ingredients_lower) * 100 if recipe_ingredients_lower else 0
                missing = [i for i in recipe_ingredients_lower if i not in ingredients]
                matched.append((match_pct, recipe, missing))

            matched.sort(key=lambda x: x[0], reverse=True)
            top_pantry = [r for r in matched if r[0] > 0][:5]
            if top_pantry:
                st.session_state["pantry_results"] = top_pantry
            else:
                render_info_box("No recipes match your pantry. Try adding more ingredients.", "warn")

    with col2:
        if st.button("📅 Generate Meal Plan from Pantry", use_container_width=True) and available_foods:
            from src.ai_agent.meal_planner import generate_daily_plan
            plan = generate_daily_plan(
                goal_type=profile.get("goal_type", "Maintenance"),
            )
            st.session_state["pantry_meal_plan"] = plan
            st.success("✅ Meal plan generated from pantry!")

    if "pantry_results" in st.session_state:
        st.markdown("<div style='margin:1rem 0'></div>", unsafe_allow_html=True)
        for match_pct, recipe, missing in st.session_state["pantry_results"]:
            with st.container(border=True):
                st.markdown(f"### {recipe['name']} ({match_pct:.0f}% match)")
                c1, c2, c3 = st.columns(3)
                c1.metric("Calories", f"{recipe['calories']} kcal")
                c2.metric("Protein", f"{recipe['protein']}g")
                c3.metric("Time", recipe["time"])
                if missing:
                    st.markdown(f"🛒 **Missing:** {', '.join(i.title() for i in missing)}")

    if "pantry_meal_plan" in st.session_state:
        st.markdown("<div style='margin:0.75rem 0'></div>", unsafe_allow_html=True)
        with st.container(border=True):
            card_header("📅 Pantry Meal Plan", "Based on your available ingredients", icon="📅")
            plan = st.session_state["pantry_meal_plan"]
            for mt in ["Breakfast", "Lunch", "Dinner", "Snacks"]:
                if mt in plan["meals"]:
                    m = plan["meals"][mt]
                    st.markdown(
                        f"**{mt}:** {m['name']} — {m['calories']} kcal "
                        f"(P:{m['protein']}g C:{m['carbs']}g F:{m['fat']}g)"
                    )

render_footer()
