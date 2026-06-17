"""
Card and layout helper components for NutriSense AI — SaaS dashboard.
"""

from __future__ import annotations

import html as html_lib
from datetime import datetime

import streamlit as st

APP_VERSION = "1.0"


def render_stat_card(col, label: str, value: str, hint: str = "", accent: str = "#0d9488") -> None:
    """Compact equal-height stat card for dashboard."""
    with col:
        st.markdown(
            f'<div class="stat-card" style="border-left:3px solid {accent};">'
            f'<div class="stat-label">{html_lib.escape(label)}</div>'
            f'<div class="stat-value">{html_lib.escape(str(value))}</div>'
            f'<div class="stat-hint">{html_lib.escape(str(hint))}</div>'
            f"</div>",
            unsafe_allow_html=True,
        )


def render_metric_card(
    col,
    title: str,
    value: str,
    icon: str,
    helper_text: str,
    accent: str = "#0d9488",
) -> None:
    """Small KPI card for inner pages."""
    with col:
        st.markdown(
            f'<div class="stat-card stat-card-sm" style="border-left:3px solid {accent};">'
            f'<div class="stat-label">{html_lib.escape(f"{icon} {title}")}</div>'
            f'<div class="stat-value">{html_lib.escape(str(value))}</div>'
            f'<div class="stat-hint">{html_lib.escape(str(helper_text))}</div>'
            f"</div>",
            unsafe_allow_html=True,
        )


def render_rich_metric_card(
    col,
    title: str,
    value: str,
    icon: str,
    helper_text: str,
    accent: str = "#0d9488",
    progress_pct: float | None = None,
) -> None:
    with col:
        st.markdown(
            f'<div class="stat-card" style="border-left:3px solid {accent};">'
            f'<div class="stat-label">{html_lib.escape(f"{icon} {title}")}</div>'
            f'<div class="stat-value">{html_lib.escape(str(value))}</div>'
            f'<div class="stat-hint">{html_lib.escape(str(helper_text))}</div>'
            f"</div>",
            unsafe_allow_html=True,
        )
        if progress_pct is not None:
            pct = max(0, min(float(progress_pct), 100))
            st.progress(pct / 100)


def render_dashboard_greeting(today_cal: int, daily_goal: int, name: str = "there") -> None:
    hour = datetime.now().hour
    greeting = "Good Morning" if hour < 12 else ("Good Afternoon" if hour < 17 else "Good Evening")
    st.markdown(
        f"""
        <div class="dash-greeting">
            <div class="dash-greeting-left">
                <h1>{greeting} 👋</h1>
                <p>Your AI nutrition overview</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_ai_insight_card(message: str) -> None:
    safe = html_lib.escape(message)
    st.markdown(
        f"""
        <div class="ai-insight-card">
            <div class="ai-insight-label">🥗 AI Insight</div>
            <p>{safe}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_upload_zone() -> None:
    st.markdown(
        """
        <div class="upload-zone">
            <div class="upload-zone-icon">📷</div>
            <div class="upload-zone-title">Drop your meal image here</div>
            <div class="upload-zone-sub">Supported formats: JPG · PNG · JPEG</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_processing_timeline(stage: int = 0) -> None:
    """Vertical AI pipeline with checkmarks. stage 0-4."""
    steps = [
        "Image uploaded",
        "Food detected",
        "Nutrition calculated",
        "Advice generated",
    ]
    items = []
    for i, label in enumerate(steps, start=1):
        if i < stage:
            icon, cls = "✓", "done"
        elif i == stage:
            icon, cls = "●", "active"
        else:
            icon, cls = "○", "pending"
        items.append(
            f'<div class="proc-step {cls}">'
            f'<span class="proc-icon">{icon}</span>'
            f'<span>{html_lib.escape(label)}</span></div>'
        )
    st.markdown(f'<div class="proc-timeline">{"".join(items)}</div>', unsafe_allow_html=True)


def render_progress_ring(pct: float, label: str = "Daily Progress") -> None:
    pct_clamped = max(0, min(float(pct), 100))
    st.markdown(
        f"""
        <div class="ring-wrap">
            <div class="ring-label">{html_lib.escape(label)}</div>
            <div class="ring-outer">
                <div class="ring-inner">{pct_clamped:.0f}%</div>
            </div>
        </div>
        <style>
        .ring-outer {{
            background: conic-gradient(#0d9488 {pct_clamped}%, #e2e8f0 0);
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def card_header(title: str, subtitle: str = "") -> None:
    st.markdown(f'<div class="card-title">{html_lib.escape(title)}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="card-subtitle">{html_lib.escape(subtitle)}</div>', unsafe_allow_html=True)


def render_health_badge(score: int | float | None) -> str:
    if score is None:
        score = 0
    score = int(score)
    if score >= 75:
        cls, label, dot = "health-badge-high", "Excellent", "🟢"
    elif score >= 50:
        cls, label, dot = "health-badge-mid", "Good", "🟡"
    else:
        cls, label, dot = "health-badge-low", "Needs Balance", "🔴"
    return f'<span class="health-badge {cls}">{dot} {label} · {score}/100</span>'


def render_step_pipeline(steps: list[tuple[str, str]], active: int = 1) -> None:
    items = []
    for i, (num, label) in enumerate(steps, start=1):
        cls = "active" if i == active else ("done" if i < active else "")
        items.append(f'<div class="step-item {cls}"><span class="step-num">{num}</span>{label}</div>')
    st.markdown(f'<div class="step-pipeline">{"".join(items)}</div>', unsafe_allow_html=True)


def render_progress_bar(pct: float, label_left: str = "", label_right: str = "") -> None:
    pct_clamped = max(0, min(pct, 100))
    st.markdown(
        f"""
        <div class="progress-label"><span>{label_left}</span><span>{label_right}</span></div>
        <div class="progress-wrap"><div class="progress-fill" style="width:{pct_clamped}%"></div></div>
        """,
        unsafe_allow_html=True,
    )


def render_meal_card(
    food_name: str, meta: str, calories: int | float,
    health_score: int | float | None = None, icon: str = "🍛",
    protein: float | None = None, carbs: float | None = None, fat: float | None = None,
) -> None:
    badge = f'<div style="margin-top:4px">{render_health_badge(health_score)}</div>' if health_score is not None else ""
    macros = ""
    if protein is not None:
        macros = f'<div class="meal-macros">P {protein}g · C {carbs}g · F {fat}g</div>'
    st.markdown(
        f'<div class="meal-card"><div><div class="meal-name">{icon} {html_lib.escape(food_name)}</div>'
        f'<div class="meal-meta">{html_lib.escape(meta)}</div>{macros}{badge}</div>'
        f'<div class="meal-cal">{int(calories)} kcal</div></div>',
        unsafe_allow_html=True,
    )


def render_meal_history_card(
    food_name: str, meal_type: str, calories: float, protein: float,
    carbs: float, fat: float, health_score: int | float | None, date_str: str,
) -> None:
    badge = render_health_badge(health_score) if health_score is not None else ""
    st.markdown(
        f'<div class="history-meal-card"><div class="history-meal-top"><div>'
        f'<div class="meal-name">🍛 {html_lib.escape(food_name)}</div>'
        f'<div class="meal-meta">{html_lib.escape(meal_type)} · {html_lib.escape(date_str)}</div></div>'
        f'<div class="meal-cal">{int(calories)} kcal</div></div>'
        f'<div class="history-meal-macros"><span>🥩 {protein}g</span><span>🌾 {carbs}g</span>'
        f'<span>🧈 {fat}g</span></div><div class="history-meal-bottom">{badge}</div></div>',
        unsafe_allow_html=True,
    )


def render_action_section(text: str) -> None:
    st.markdown(f'<div class="action-card"><span class="action-card-text">{html_lib.escape(text)}</span></div>', unsafe_allow_html=True)


def render_chat_bubble(role: str, message: str) -> None:
    """ChatGPT-like bubbles.

    User message: simple avatar.
    AI message: nutrition assistant icon.
    """
    if role == "user":
        role_label = "You"
        css_class = "chat-bubble-user"
        avatar = "👤"
    else:
        role_label = "Nutrition Assistant"
        css_class = "chat-bubble-ai"
        avatar = "🥗"

    st.markdown(
        f'<div class="chat-bubble {css_class}">'
        f'<div class="chat-role"><span style="margin-right:6px">{avatar}</span>{role_label}</div>'
        f"<p>{html_lib.escape(str(message))}</p></div>",
        unsafe_allow_html=True,
    )



def render_chat_panel(user_message: str, coach_message: str) -> None:
    st.markdown('<div class="chat-panel">', unsafe_allow_html=True)
    render_chat_bubble("user", user_message)
    render_chat_bubble("coach", coach_message)
    st.markdown("</div>", unsafe_allow_html=True)


def render_ai_summary_card(text: str) -> None:
    st.markdown(
        f'<div class="ai-summary-card"><div class="ai-summary-label">AI Nutrition Summary</div>'
        f'<p>{html_lib.escape(text)}</p></div>',
        unsafe_allow_html=True,
    )


def render_footer(version: str = APP_VERSION) -> None:
    st.markdown(
        f'<div class="app-footer"><strong>NutriSense AI v{version}</strong> · '
        f'Powered by EfficientNetB0</div>',
        unsafe_allow_html=True,
    )


def render_health_report(
    quality: str, best_for: str, note: str, suggestion: str, quality_dot: str = "🟡",
) -> None:
    st.markdown(
        f'<div class="health-report">'
        f'<div class="hr-row"><span>Meal Quality</span><strong>{quality_dot} {html_lib.escape(quality)}</strong></div>'
        f'<div class="hr-row"><span>Best For</span><strong>{html_lib.escape(best_for)}</strong></div>'
        f'<div class="hr-row"><span>Nutrition Note</span><strong>{html_lib.escape(note)}</strong></div>'
        f'<div class="hr-suggestion"><span>Suggestion</span><p>{html_lib.escape(suggestion)}</p></div>'
        f"</div>",
        unsafe_allow_html=True,
    )


def render_welcome_hero(goal: str, target: int, today_cal: int = 0) -> None:
    render_dashboard_greeting(today_cal, target)


def render_ai_engine_card() -> None:
    pass
