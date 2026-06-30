"""
streamlit_app/pages/5_AI_Recommendation.py
============================================
NutriSense AI — AI Nutrition Coach Page.

Chat replies: Groq API (llama-3.3-70b) with local logic fallback.
Analysis cards: Real SQLite data via recommendation.py
"""

from __future__ import annotations

from dotenv import load_dotenv
load_dotenv()

import os
import sys
import requests

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

import streamlit as st

from src.utils.ui import (
    render_app_layout,
    render_page_header,
    render_footer,
    card_header,
)
from src.utils.helpers import get_active_user_id
from src.database.meals import get_today_summary
from src.database.user import get_user_profile
from src.ai_agent.recommendation import (
    generate_daily_recommendation,
    answer_user_question,
    suggest_next_meal,
)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Coach — NutriSense AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

if not st.session_state.get("authenticated"):
    from streamlit_app.Account import render_account_page
    render_account_page()
    st.stop()

# ── Data ──────────────────────────────────────────────────────────────────────
user_id   = get_active_user_id()
profile   = get_user_profile(user_id)
summary   = get_today_summary(user_id)
user_name = profile.get("name", "Friend")

goal_options = ["Weight Loss", "Weight Gain", "Maintenance", "Healthy Lifestyle"]
default_goal = profile.get("goal_type") or profile.get("goal") or "Maintenance"
if default_goal not in goal_options:
    default_goal = "Maintenance"

if "coach_goal" not in st.session_state:
    st.session_state.coach_goal = default_goal

render_app_layout(
    active_page="coach",
    calories_today=float(summary.get("calories", 0) or 0),
    daily_goal=float(summary.get("calorie_goal", 2200) or 2200),
    user_name=user_name,
)

render_page_header(
    "🤖 AI Nutrition Coach",
    "Your personal AI dietitian — powered by Groq AI & real-time meal data.",
)

# ── Load AI analysis ──────────────────────────────────────────────────────────
with st.spinner("🧠 Analysing your nutrition data…"):
    rec = generate_daily_recommendation(user_id)

selected  = st.session_state.coach_goal
calories  = rec["calories_consumed"]
goal_cals = rec["calorie_goal"]
remaining = rec["remaining_calories"]
pct_done  = min(int(rec["goal_pct"]), 100)

# ── Groq API function ─────────────────────────────────────────────────────────
def _groq_reply(prompt: str, history: list) -> str:
    """
    Send message to Groq API (llama-3.3-70b).
    Falls back to local logic if API key missing or request fails.
    """
    api_key = os.environ.get("GROQ_API_KEY", "").strip()

    # ── System prompt with real user context ──────────────────────────────────
    system_prompt = (
        f"You are NutriSense AI Coach — a warm, knowledgeable personal nutrition assistant "
        f"inside the NutriSense app.\n\n"
        f"USER CONTEXT (from real meal database):\n"
        f"- Name: {user_name}\n"
        f"- Goal: {selected}\n"
        f"- Daily calorie target: {goal_cals:,.0f} kcal\n"
        f"- Consumed today: {calories:,.0f} kcal\n"
        f"- Remaining today: {remaining:,.0f} kcal\n"
        f"- Progress: {pct_done}% of daily goal\n"
        f"- Protein today: {rec['protein']:.0f}g\n"
        f"- Carbs today: {rec['carbs']:.0f}g\n"
        f"- Fat today: {rec['fat']:.0f}g\n"
        f"- Health score: {rec['health_score']}/100\n"
        f"- Meals logged: {rec['meals_count']}\n\n"
        f"RULES:\n"
        f"- Be warm, friendly, and encouraging — like a supportive coach.\n"
        f"- Respond naturally to greetings, small talk (hi, hello, salam, kesy ho, etc.).\n"
        f"- Answer any question. Weave in nutrition context only when relevant.\n"
        f"- Keep replies concise: 1-3 sentences for simple things, short bullet list for advice.\n"
        f"- You can reply in Roman Urdu or English, matching the user's language.\n"
        f"- Never say you are Llama or made by Meta/Groq. You are NutriSense AI Coach.\n"
        f"- Use **bold** for important numbers and food names."
    )

    # Build messages list for API
    messages = [{"role": "system", "content": system_prompt}]
    for m in history[-12:]:
        role = "user" if m["role"] == "user" else "assistant"
        messages.append({"role": role, "content": m["content"]})
    if not messages or messages[-1].get("content") != prompt:
        messages.append({"role": "user", "content": prompt})

    # ── No API key → fall back to local logic ─────────────────────────────────
    if not api_key:
        return answer_user_question(prompt, user_id)

    try:
        resp = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Content-Type":  "application/json",
                "Authorization": f"Bearer {api_key}",
            },
            json={
                "model":       "llama-3.3-70b-versatile",
                "max_tokens":  350,
                "temperature": 0.7,
                "messages":    messages,
            },
            timeout=20,
        )
        data = resp.json()

        if "error" in data:
            # API returned an error → local fallback
            return answer_user_question(prompt, user_id)

        reply = data["choices"][0]["message"]["content"].strip()
        return reply if reply else answer_user_question(prompt, user_id)

    except Exception:
        # Network timeout or any other error → local fallback
        return (
            f"I'm having a quick timeout — but I've got you! "
            f"You have **{remaining:,.0f} kcal** left today. "
            f"Keep going, {user_name}! 💚"
        )


def _md_to_html(text: str) -> str:
    """Convert **bold** and newlines to HTML."""
    import re
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = text.replace('\n', '<br>')
    return text


def _render_ai_bubble(html_content: str) -> None:
    st.markdown(
        f"""
        <div style="display:flex;gap:.75rem;margin-bottom:.9rem;align-items:flex-start;">
            <div style="font-size:1.45rem;flex-shrink:0;">🤖</div>
            <div style="background:#f0fdfa;border:1px solid #99f6e4;
                        border-radius:0 14px 14px 14px;padding:.85rem 1rem;
                        color:#0f172a;font-size:.92rem;line-height:1.65;max-width:85%;">
                {html_content}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_user_bubble(content: str) -> None:
    st.markdown(
        f"""
        <div style="display:flex;gap:.75rem;margin-bottom:.9rem;
                    align-items:flex-start;flex-direction:row-reverse;">
            <div style="font-size:1.45rem;flex-shrink:0;">👤</div>
            <div style="background:linear-gradient(135deg,#14b8a6,#0ea5e9);
                        border-radius:14px 0 14px 14px;padding:.85rem 1rem;
                        color:white;font-size:.92rem;line-height:1.65;max-width:85%;">
                {content}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── Session state init ────────────────────────────────────────────────────────
if "coach_messages" not in st.session_state:
    st.session_state.coach_messages = [
        {
            "role": "ai",
            "content": (
                f"Hello {user_name}! 👋 I'm your NutriSense AI Nutrition Coach.\n\n"
                f"I've analysed your meals today — "
                f"you've consumed **{calories:,.0f} kcal** out of your **{goal_cals:,.0f} kcal** goal.\n\n"
                f"Ask me anything:\n"
                f"- *What should I eat next?*\n"
                f"- *How is my diet today?*\n"
                f"- *How can I improve my health score?*"
            ),
        }
    ]

if "show_quick" not in st.session_state:
    st.session_state.show_quick = True

if "pending_ai_reply" not in st.session_state:
    st.session_state.pending_ai_reply = False

# ══════════════════════════════════════════════════════════════════════════════
#  ROW 1 — Greeting banner
# ══════════════════════════════════════════════════════════════════════════════

status_color = {
    "empty":    ("#f1f5f9", "#64748b", "#cbd5e1"),
    "low":      ("#fffbeb", "#92400e", "#fde68a"),
    "moderate": ("#eff6ff", "#1d4ed8", "#bfdbfe"),
    "good":     ("#ecfdf5", "#065f46", "#99f6e4"),
    "over":     ("#fef2f2", "#991b1b", "#fecaca"),
}.get(rec["status"], ("#f8fafc", "#334155", "#e2e8f0"))

status_emoji = {
    "empty": "👋", "low": "⚠️", "moderate": "📈", "good": "✅", "over": "🚨"
}.get(rec["status"], "🤖")

api_status = "🟢 Groq AI Active" if os.environ.get("GROQ_API_KEY","").strip() else "🟡 Local AI Mode"

st.markdown(
    f"""
    <div style="background:{status_color[0]};border:1.5px solid {status_color[2]};
                border-radius:18px;padding:1.4rem 1.6rem;margin-bottom:1.2rem;">
        <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:1rem;">
            <div style="display:flex;gap:1rem;align-items:flex-start;">
                <div style="font-size:2rem;">🤖</div>
                <div>
                    <div style="font-weight:800;font-size:1.05rem;color:#0f172a;">
                        {status_emoji} Hello {user_name}!
                    </div>
                    <div style="color:{status_color[1]};margin-top:0.4rem;line-height:1.6;">
                        {rec["summary"]}
                    </div>
                </div>
            </div>
            <div style="font-size:.75rem;font-weight:700;color:#64748b;
                        white-space:nowrap;background:white;
                        padding:.35rem .75rem;border-radius:999px;
                        border:1px solid #e5e7eb;">
                {api_status}
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ══════════════════════════════════════════════════════════════════════════════
#  ROW 2 — Stat cards
# ══════════════════════════════════════════════════════════════════════════════

c1, c2, c3, c4 = st.columns(4)

def _stat_mini(col, label, value, sub, color, icon):
    with col:
        st.markdown(
            f"""
            <div style="background:white;border-left:4px solid {color};
                        border-radius:14px;padding:1rem 1.1rem;
                        box-shadow:0 4px 15px rgba(0,0,0,.05);">
                <div style="font-size:.72rem;font-weight:800;letter-spacing:.07em;
                            color:#94a3b8;text-transform:uppercase;">{label}</div>
                <div style="font-size:1.6rem;font-weight:900;color:#0f172a;
                            margin:.4rem 0 .2rem;">{icon} {value}</div>
                <div style="font-size:.82rem;color:#64748b;">{sub}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

_stat_mini(c1, "Calories",     f"{rec['calories_consumed']:.0f}",
           f"Goal: {rec['calorie_goal']:.0f} kcal", "#0d9488", "🔥")
_stat_mini(c2, "Protein",      f"{rec['protein']:.0f}g",
           "Target: 120g", "#0284c7", "🥩")
_stat_mini(c3, "Health Score", f"{rec['health_score']}",
           "Out of 100", "#16a34a", "💚")
_stat_mini(c4, "Meals Today",  str(rec["meals_count"]),
           "Logged today", "#7c3aed", "🍽️")

st.markdown("<div style='margin:.8rem 0'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  ROW 3 — Progress bar
# ══════════════════════════════════════════════════════════════════════════════

pct_bar   = min(rec["goal_pct"], 100)
bar_color = "#0d9488" if pct_bar <= 80 else "#f59e0b" if pct_bar <= 100 else "#ef4444"

st.markdown(
    f"""
    <div style="background:white;border:1px solid #e5e7eb;border-radius:14px;
                padding:1.1rem 1.3rem;margin-bottom:.9rem;">
        <div style="display:flex;justify-content:space-between;font-size:.85rem;
                    font-weight:700;margin-bottom:.55rem;color:#334155;">
            <span>🔥 Daily Calorie Progress</span>
            <span style="color:{bar_color}">{rec['goal_pct']}% of {rec['calorie_goal']:.0f} kcal</span>
        </div>
        <div style="background:#f1f5f9;border-radius:999px;height:14px;overflow:hidden;">
            <div style="width:{pct_bar}%;background:{bar_color};height:100%;
                        border-radius:999px;"></div>
        </div>
        <div style="display:flex;justify-content:space-between;font-size:.78rem;
                    color:#94a3b8;margin-top:.4rem;">
            <span>0 kcal</span>
            <span>Remaining: {rec['remaining_calories']:.0f} kcal</span>
            <span>{rec['calorie_goal']:.0f} kcal</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ══════════════════════════════════════════════════════════════════════════════
#  ROW 4 — Recommendations | Next Meal + Macros
# ══════════════════════════════════════════════════════════════════════════════

left, right = st.columns([3, 2])

with left:
    with st.container(border=True):
        card_header("AI Recommendations", "Based on your today's intake", icon="🧠")

        for w in rec["warnings"]:
            st.markdown(
                f"""<div style="background:#fef2f2;border:1px solid #fecaca;
                            border-radius:10px;padding:.7rem 1rem;
                            margin-bottom:.5rem;color:#991b1b;font-size:.9rem;">
                    {w}</div>""",
                unsafe_allow_html=True,
            )

        for r in rec["recommendations"]:
            st.markdown(
                f"""<div style="background:#f8fafc;border:1px solid #e5e7eb;
                            border-radius:10px;padding:.7rem 1rem;
                            margin-bottom:.5rem;color:#334155;font-size:.92rem;">
                    {r}</div>""",
                unsafe_allow_html=True,
            )

        st.markdown(
            f"""<div style="background:#ecfdf5;border:1px solid #99f6e4;
                        border-radius:12px;padding:.9rem 1rem;margin-top:.8rem;
                        color:#065f46;font-size:.9rem;">{rec["health_tip"]}</div>""",
            unsafe_allow_html=True,
        )

with right:
    with st.container(border=True):
        card_header("Next Meal Suggestion", "AI-powered food recommendation", icon="🍽️")
        meal = suggest_next_meal(user_id)
        st.markdown(
            f"""
            <div style="background:linear-gradient(135deg,#f0fdfa,#eff6ff);
                        border:1px solid #99f6e4;border-radius:14px;padding:1.1rem;">
                <div style="font-weight:800;font-size:1rem;color:#0f172a;margin-bottom:.5rem;">
                    🍽️ {meal["meal_name"]}</div>
                <div style="font-size:.82rem;color:#64748b;margin-bottom:.8rem;">
                    {meal["reason"]}</div>
            """,
            unsafe_allow_html=True,
        )
        for item in meal["items"]:
            st.markdown(
                f"""<div style="padding:.35rem 0;border-bottom:1px solid #e5e7eb;
                            font-size:.9rem;color:#334155;">✅ {item}</div>""",
                unsafe_allow_html=True,
            )
        st.markdown(
            f"""<div style="margin-top:.75rem;font-weight:800;color:#0d9488;font-size:.95rem;">
                    ~{meal["est_calories"]} kcal estimated</div></div>""",
            unsafe_allow_html=True,
        )

    st.markdown("<div style='margin:.5rem 0'></div>", unsafe_allow_html=True)

    with st.container(border=True):
        card_header("Macro Breakdown", icon="📊")
        for name, val, target, color in [
            ("Protein", rec["protein"],  120, "#0284c7"),
            ("Carbs",   rec["carbs"],    250, "#f59e0b"),
            ("Fat",     rec["fat"],       70, "#ef4444"),
        ]:
            pct_m = min(round(val / target * 100) if target else 0, 100)
            st.markdown(
                f"""
                <div style="margin-bottom:.7rem;">
                    <div style="display:flex;justify-content:space-between;
                                font-size:.82rem;color:#334155;font-weight:700;margin-bottom:.3rem;">
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

# ══════════════════════════════════════════════════════════════════════════════
#  ROW 5 — Chat (Groq API + local fallback)
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("<div style='margin:1rem 0 .3rem'></div>", unsafe_allow_html=True)

with st.container(border=True):

    # Header with goal selector
    h_left, h_right = st.columns([2, 1])
    with h_left:
        card_header("Chat with AI Coach", "Powered by Groq llama-3.3-70b", icon="💬")
    with h_right:
        goal_index = goal_options.index(selected) if selected in goal_options else 2
        new_goal   = st.selectbox(
            "My Goal",
            goal_options,
            index=goal_index,
            key="goal_selector",
            label_visibility="collapsed",
        )
        if new_goal != selected:
            st.session_state.coach_goal     = new_goal
            st.session_state.coach_messages = []
            st.session_state.pending_ai_reply = False
            st.rerun()

    # ── Quick question buttons ────────────────────────────────────────────────
    # NOTE: clicking a button only QUEUES the question (sets pending_ai_reply).
    # The actual API call + "Thinking..." indicator happen further down, AFTER
    # the chat bubbles are rendered, so the indicator appears in the right
    # place — right below the conversation, where the new reply will land.
    st.markdown(
        "<div style='font-size:.78rem;color:#94a3b8;font-weight:700;"
        "text-transform:uppercase;letter-spacing:.06em;margin-bottom:.4rem;'>"
        "Quick Questions</div>",
        unsafe_allow_html=True,
    )

    q1, q2, q3, q4 = st.columns(4)
    quick_map = {
        "q_eat":      (q1, "🍽️ What to eat next?"),
        "q_diet":     (q2, "📊 How's my diet?"),
        "q_improve":  (q3, "💡 Improve health score"),
        "q_calories": (q4, "🔥 Calorie check"),
    }
    quick_prompts = {
        "q_eat":      "What should I eat next?",
        "q_diet":     "How is my diet today?",
        "q_improve":  "How can I improve my health score?",
        "q_calories": "How many calories have I consumed?",
    }

    quick_clicked = False
    for key, (col, label) in quick_map.items():
        with col:
            if st.button(label, key=key, use_container_width=True, disabled=st.session_state.pending_ai_reply):
                prompt = quick_prompts[key]
                st.session_state.coach_messages.append({"role": "user", "content": prompt})
                st.session_state.pending_ai_reply = True
                quick_clicked = True

    if quick_clicked:
        st.rerun()

    st.markdown("<div style='margin:.5rem 0'></div>", unsafe_allow_html=True)

    # ── Chat bubbles ──────────────────────────────────────────────────────────
    for msg in st.session_state.coach_messages:
        if msg["role"] == "ai":
            _render_ai_bubble(_md_to_html(msg["content"]))
        else:
            _render_user_bubble(msg["content"])

    # ── Pending AI reply: show inline "Thinking..." then fetch reply ───────────
    # This renders BELOW the chat bubbles (right where the new AI message will
    # appear) instead of a floating st.spinner overlay.
    if st.session_state.pending_ai_reply and st.session_state.coach_messages:
        last_msg = st.session_state.coach_messages[-1]
        if last_msg["role"] == "user":
            thinking_slot = st.empty()
            with thinking_slot.container():
                _render_ai_bubble(
                    "<span style='color:#64748b;'>🤖 Thinking"
                    "<span style='animation:nsThinkingBlink 1.2s infinite;'>...</span>"
                    "</span>"
                    "<style>@keyframes nsThinkingBlink"
                    "{0%,100%{opacity:.25}50%{opacity:1}}</style>"
                )

            reply = _groq_reply(last_msg["content"], st.session_state.coach_messages[:-1])

            thinking_slot.empty()
            st.session_state.coach_messages.append({"role": "ai", "content": reply})
            st.session_state.pending_ai_reply = False
            st.rerun()

    # ── Chat input ────────────────────────────────────────────────────────────
    user_input = st.chat_input(
        "Ask your AI Nutrition Coach anything…",
        disabled=st.session_state.pending_ai_reply,
    )

    if user_input and user_input.strip():
        st.session_state.coach_messages.append({"role": "user", "content": user_input.strip()})
        st.session_state.pending_ai_reply = True
        st.rerun()

    # ── Footer row ────────────────────────────────────────────────────────────
    f1, f2 = st.columns([4, 1])
    with f1:
        st.markdown(
            """
            <div style="background:#fffbeb;border:1px solid #fde68a;border-radius:10px;
                        padding:.65rem 1rem;font-size:.78rem;color:#92400e;margin-top:.5rem;">
                ⚠️ <strong>Disclaimer:</strong> This AI Coach provides general nutrition guidance only —
                not personalised medical advice. Consult a registered dietitian for clinical recommendations.
            </div>
            """,
            unsafe_allow_html=True,
        )
    with f2:
        if st.button("🗑️ Clear Chat", use_container_width=True, disabled=st.session_state.pending_ai_reply):
            st.session_state.coach_messages = []
            st.session_state.pending_ai_reply = False
            st.rerun()

render_footer()