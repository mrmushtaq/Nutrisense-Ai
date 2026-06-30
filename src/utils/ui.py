from __future__ import annotations

import streamlit as st


APP_NAME = "NutriSense AI"
APP_SUBTITLE = "AI Nutrition Intelligence Platform"


def inject_custom_css() -> None:
    st.markdown(
        """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
[data-testid="stToolbar"] {visibility: hidden; height: 0px;}

.stApp {
    background: #f3f6fa;
}

.main .block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

section[data-testid="stSidebar"] {
    width: 280px !important;
    min-width: 280px !important;
    max-width: 280px !important;
    background: #ffffff !important;
    border-right: 1px solid #e5e7eb !important;
}

section[data-testid="stSidebar"] > div {
    width: 280px !important;
    min-width: 280px !important;
    background: #ffffff !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
    padding: 1rem 1rem 1.25rem 1rem !important;
}

[data-testid="collapsedControl"],
[data-testid="stSidebarCollapsedControl"],
button[kind="header"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
}

section[data-testid="stSidebar"] ::-webkit-scrollbar {
    width: 6px;
}

section[data-testid="stSidebar"] ::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 10px;
}

.ns-brand {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1rem 0.5rem 1rem 0.5rem;
    margin-top: 0;
    border-bottom: 1px solid #e5e7eb;
}

.ns-logo {
    font-size: 1.7rem;
}
/* Remove Streamlit top whitespace/header */
[data-testid="stHeader"] {
    display: none !important;
}

.block-container {
    padding-top: 1rem !important;
    padding-bottom: 1rem !important;
}

/* Sidebar align from top */
section[data-testid="stSidebar"] {
    top: 0 !important;
}

section[data-testid="stSidebar"] > div {
    padding-top: 0.5rem !important;
}


/* remove deploy toolbar */
[data-testid="stToolbar"] {
    display: none !important;
}

[data-testid="stDecoration"] {
    display: none !important;
}

#MainMenu {
    visibility: hidden !important;
}

footer {
    visibility: hidden !important;
}

.ns-brand-title {
    font-size: 1.05rem;
    font-weight: 800;
    color: #0f172a;
    line-height: 1.2;
}

.ns-brand-subtitle {
    font-size: 0.78rem;
    color: #64748b;
    margin-top: 0.15rem;
}

.ns-section-title {
    font-size: 0.72rem;
    letter-spacing: 0.07em;
    color: #94a3b8;
    font-weight: 800;
    margin: 1.15rem 0 0.45rem 0.35rem;
    text-transform: uppercase;
}

.ns-side-card {
    background: #f8fafc;
    border: 1px solid #e5e7eb;
    border-radius: 0.8rem;
    padding: 0.75rem;
    margin-top: 0.6rem;
}

.ns-side-row {
    display: flex;
    justify-content: space-between;
    gap: 0.5rem;
    font-size: 0.82rem;
    color: #64748b;
    margin: 0.3rem 0;
}

.ns-side-row strong {
    color: #0f172a;
}

.ns-dot {
    display: inline-block;
    width: 0.55rem;
    height: 0.55rem;
    border-radius: 999px;
    margin-right: 0.35rem;
}

.green {background: #22c55e;}
.yellow {background: #facc15;}

.ns-top-header {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 1rem;
    padding: 1rem 1.25rem;
    margin-bottom: 1.75rem;
    box-shadow: 0 8px 25px rgba(15, 23, 42, 0.06);
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.ns-top-left {
    display: flex;
    align-items: center;
    gap: 0.8rem;
}

.ns-top-logo {
    font-size: 1.55rem;
}

.ns-top-title {
    font-weight: 800;
    font-size: 1.05rem;
    color: #0f172a;
}

.ns-top-subtitle {
    color: #64748b;
    font-size: 0.82rem;
}

.ns-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.55rem 0.85rem;
    border: 1px solid #dbeafe;
    border-radius: 999px;
    background: #f8fafc;
    font-size: 0.82rem;
    font-weight: 700;
    color: #334155;
}

.ns-page-title {
    font-size: 1.8rem;
    font-weight: 850;
    color: #0f172a;
    margin-bottom: 0.45rem;
}

.ns-page-subtitle {
    font-size: 1rem;
    color: #64748b;
    margin-bottom: 1.3rem;
}

.ns-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 1rem;
    padding: 1.15rem;
    box-shadow: 0 8px 25px rgba(15, 23, 42, 0.04);
}

.ns-card-soft {
    background: linear-gradient(135deg, #f0fdfa, #eff6ff);
    border: 1px solid #99f6e4;
    border-radius: 1rem;
    padding: 1.1rem 1.25rem;
}

.ns-metric {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-left: 4px solid #14b8a6;
    border-radius: 0.9rem;
    padding: 1rem 1.1rem;
    box-shadow: 0 8px 20px rgba(15, 23, 42, 0.04);
}

.ns-metric-label {
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.06em;
    color: #94a3b8;
    text-transform: uppercase;
}

.ns-metric-value {
    font-size: 1.75rem;
    font-weight: 850;
    color: #0f172a;
    margin-top: 0.45rem;
}

/* ── Hide Streamlit Default Navigation ── */
[data-testid="stSidebarNav"] {
    display: none !important;
}

[data-testid="stSidebarNavItems"] {
    display: none !important;
}

/* remove extra space left by default nav */
section[data-testid="stSidebar"] > div:first-child {
    padding-top: 0 !important;
}

.ns-metric-help {
    font-size: 0.82rem;
    color: #64748b;
    margin-top: 0.25rem;
}

.ns-info {
    padding: 0.9rem 1rem;
    border-radius: 0.8rem;
    margin: 0.65rem 0;
    font-size: 0.92rem;
}

.ns-info.info {
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    color: #1d4ed8;
}

.ns-info.success {
    background: #ecfdf5;
    border: 1px solid #86efac;
    color: #047857;
}

.ns-info.warn {
    background: #fffbeb;
    border: 1px solid #fde68a;
    color: #92400e;
}

.ns-empty-state {
    background: #ffffff;
    border: 1px dashed #cbd5e1;
    border-radius: 1rem;
    padding: 2.5rem 1rem;
    text-align: center;
    color: #64748b;
    margin: 1rem 0;
}

.ns-empty-icon {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}

.ns-empty-title {
    color: #0f172a;
    font-size: 1.1rem;
    font-weight: 800;
    margin-bottom: 0.3rem;
}

.ns-section-wrap {
    margin: 1.4rem 0 0.9rem;
}

.ns-section-heading {
    margin: 0;
    color: #0f172a;
    font-size: 1.15rem;
    font-weight: 800;
}

.ns-section-subtitle {
    margin-top: 0.25rem;
    color: #64748b;
    font-size: 0.9rem;
}

.ns-footer {
    text-align: center;
    color: #94a3b8;
    font-size: 0.8rem;
    padding: 1.4rem 0 0.4rem;
    border-top: 1px solid #e5e7eb;
    margin-top: 2rem;
}

.stButton > button {
    border-radius: 0.75rem !important;
    font-weight: 700 !important;
}

@media (max-width: 900px) {
    .main .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .ns-top-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 0.8rem;
    }
}

/* Sidebar hamesha visible */
section[data-testid="stSidebar"] {
    transform: none !important;
    display: block !important;
    visibility: visible !important;
}

[data-testid="collapsedControl"] {
    display: none !important;
}

/* Hide collapse button */
[data-testid="collapsedControl"] {
    display: none !important;
}
button[kind="header"] {
    display: none !important;
}

/* Hide sidebar collapse arrow completely */
[data-testid="collapsedControl"] {
    display: none !important;
    visibility: hidden !important;
    width: 0 !important;
    height: 0 !important;
    opacity: 0 !important;
    pointer-events: none !important;
}

section[data-testid="stSidebar"] + div [data-testid="collapsedControl"] {
    display: none !important;
}

.st-emotion-cache-1egp75f {
    display: none !important;
}

/* Collapse button - multiple selectors */
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapsedControl"],
.st-emotion-cache-1egp75f,
.st-emotion-cache-czk5ss,
.st-emotion-cache-1rtdyuf,
button[aria-label="Close sidebar"],
button[aria-label="Collapse sidebar"] {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
    width: 0 !important;
    height: 0 !important;
    position: absolute !important;
}
/* Hide collapse button completely */
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapsedControl"] {
    display: none !important;
    width: 0 !important;
    height: 0 !important;
    overflow: hidden !important;
    position: absolute !important;
    pointer-events: none !important;
}

/* Hide resize handle/pointer */
[data-testid="stSidebarResizeHandle"],
.stSidebarResizeHandle {
    display: none !important;
    width: 0 !important;
    pointer-events: none !important;
}

/* Remove resize cursor from sidebar edge */
section[data-testid="stSidebar"] {
    resize: none !important;
    cursor: default !important;
}

section[data-testid="stSidebar"] > div {
    resize: none !important;
}
</style>
""",
        unsafe_allow_html=True,
    )


def render_sidebar(active_page: str = "home") -> None:
    nav_items = [
        ("home", "🏠 Dashboard", "Home.py"),
        ("profile", "👤 My Profile", "pages/6_User_Profile.py"),
        ("upload", "📸 Food Scan", "pages/1_Upload_Food.py"),
        ("nutrition", "📊 Nutrition", "pages/2_Nutrition_Result.py"),
        ("calories", "🔥 Calories", "pages/3_Daily_Calories.py"),
        ("meal_planner", "📅 Meal Planner", "pages/7_Meal_Planner.py"),
        ("recipes", "🍳 Recipes", "pages/8_Recipe_Generator.py"),
        ("history", "📜 History", "pages/4_Meal_History.py"),
        ("coach", "🤖 AI Coach", "pages/5_AI_Recommendation.py"),
    ]

    with st.sidebar:
        st.markdown(
            """
            <div class="ns-brand">
                <div class="ns-logo">🥗</div>
                <div>
                    <div class="ns-brand-title">NutriSense AI</div>
                    <div class="ns-brand-subtitle">AI Nutrition Assistant</div>
                </div>
            </div>
            <div class="ns-section-title">Navigation</div>
            """,
            unsafe_allow_html=True,
        )

        for key, label, page in nav_items:
            try:
                st.page_link(page, label=label, width="stretch")
            except TypeError:
                try:
                    st.page_link(page, label=label, width="stretch")
                except TypeError:
                    st.page_link(page, label=label)

        st.markdown(
            """
            <div class="ns-section-title">System Status</div>
            <div class="ns-side-card">
                <div class="ns-side-row">
                    <span><span class="ns-dot green"></span>Database</span>
                    <strong>Connected</strong>
                </div>
                <div class="ns-side-row">
                    <span><span class="ns-dot yellow"></span>Model</span>
                    <strong>Training</strong>
                </div>
                <div class="ns-side-row">
                    <span>Version</span>
                    <strong>1.0</strong>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
        if st.button("🚪 Sign Out", width="stretch"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.switch_page("Home.py")

def render_top_header(
    calories_today: float | int = 0,
    daily_goal: float | int = 2200,
    user_name: str = "Mushtaque Ali",
) -> None:
    st.markdown(
        f"""
        <div class="ns-top-header">
            <div class="ns-top-left">
                <div class="ns-top-logo">🥗</div>
                <div>
                    <div class="ns-top-title">{APP_NAME}</div>
                    <div class="ns-top-subtitle">{APP_SUBTITLE}</div>
                </div>
            </div>
            <div>
                <span class="ns-pill">🔥 {calories_today:,.0f} / {daily_goal:,.0f} kcal</span>
                <span class="ns-pill">👤 {user_name}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_app_layout(
    active_page: str = "dashboard",
    calories_today: float | int = 0,
    daily_goal: float | int = 2200,
    user_name: str = "Mushtaque Ali",
) -> None:
    inject_custom_css()
    render_sidebar(active_page)
    render_top_header(calories_today, daily_goal, user_name)


def render_page_header(title: str, subtitle: str | None = None) -> None:
    st.markdown(f'<div class="ns-page-title">{title}</div>', unsafe_allow_html=True)

    if subtitle:
        st.markdown(
            f'<div class="ns-page-subtitle">{subtitle}</div>',
            unsafe_allow_html=True,
        )


def render_metric_card(
    title: str,
    value: str | int | float,
    helper_text: str = "",
    icon: str = "",
    accent: str = "#14b8a6",
) -> None:
    st.markdown(
        f"""
        <div class="ns-metric" style="border-left-color:{accent};">
            <div class="ns-metric-label">{icon} {title}</div>
            <div class="ns-metric-value">{value}</div>
            <div class="ns-metric-help">{helper_text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_info_box(message: str, box_type: str = "info") -> None:
    st.markdown(
        f'<div class="ns-info {box_type}">{message}</div>',
        unsafe_allow_html=True,
    )


def render_status_badge(text: str, status_type: str = "success") -> str:
    color = "#047857" if status_type == "success" else "#1d4ed8"
    bg = "#ecfdf5" if status_type == "success" else "#eff6ff"
    border = "#86efac" if status_type == "success" else "#bfdbfe"

    return (
        f'<span style="display:inline-flex;align-items:center;gap:.35rem;'
        f'padding:.35rem .65rem;border-radius:999px;font-size:.8rem;'
        f'font-weight:700;background:{bg};color:{color};border:1px solid {border};">'
        f'● {text}</span>'
    )


def render_empty_state(
    icon: str = "📭",
    title: str = "No data available",
    message: str = "Nothing to show yet.",
) -> None:
    st.markdown(
        f"""
        <div class="ns-empty-state">
            <div class="ns-empty-icon">{icon}</div>
            <div class="ns-empty-title">{title}</div>
            <div>{message}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_title(title: str, subtitle: str | None = None) -> None:
    st.markdown(
        f"""
        <div class="ns-section-wrap">
            <h3 class="ns-section-heading">{title}</h3>
            <div class="ns-section-subtitle">{subtitle or ""}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_card(content: str) -> None:
    st.markdown(
        f"""
        <div class="ns-card">
            {content}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_divider() -> None:
    st.markdown(
        """
        <hr style="
            border:none;
            height:1px;
            background:#e5e7eb;
            margin:1.5rem 0;
        ">
        """,
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    st.markdown(
        """
        <div class="ns-footer">
            <strong>NutriSense AI v1.0</strong><br>
            Powered by TensorFlow EfficientNetB0 · Food-101 + Pakistani Food Dataset
        </div>
        """,
        unsafe_allow_html=True,
    )

def plotly_layout(
    title: str = "",
    height: int | None = None,
    showlegend: bool | None = None,
):
    """
    Default Plotly chart styling.
    Does NOT return height/showlegend to avoid duplicate keyword errors.
    """
    layout = {
        "title": {
            "text": title,
            "font": {
                "size": 16,
                "color": "#0f172a",
            },
        },
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {
            "family": "Inter",
            "color": "#334155",
            "size": 13,
        },
        "margin": {
            "l": 20,
            "r": 20,
            "t": 45,
            "b": 20,
        },
        "xaxis": {
            "gridcolor": "#e5e7eb",
        },
        "yaxis": {
            "gridcolor": "#e5e7eb",
        },
    }

    if showlegend is not None:
        layout["showlegend"] = showlegend

    if height is not None:
        layout["height"] = height

    return layout

def render_meal_card(
    food_name,
    meta,
    calories,
    health_score=None,
    protein=0,
    carbs=0,
    fat=0
):
    score = health_score or 0
    protein = protein or 0
    carbs = carbs or 0
    fat = fat or 0
    calories = calories or 0

    st.markdown(
        f"""
        <div style="background:white;border:1px solid #e5e7eb;border-radius:16px;
                    padding:1rem;margin-bottom:.8rem;">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                <div>
                    <div style="font-size:1.05rem;font-weight:800;color:#0f172a;">
                        🍽️ {food_name}
                    </div>
                    <div style="color:#64748b;font-size:0.82rem;margin-top:0.2rem;">
                        {meta}
                    </div>
                </div>
                <div style="text-align:right;flex-shrink:0;margin-left:1rem;">
                    <div style="font-weight:800;color:#0d9488;">{float(calories):.0f} kcal</div>
                    <div style="font-size:0.82rem;color:#64748b;">⭐ {score}/100</div>
                </div>
            </div>
            <div style="border-top:1px solid #e5e7eb;margin:.75rem 0;"></div>
            <div style="font-size:0.82rem;color:#64748b;">
                P {float(protein):.1f}g · C {float(carbs):.1f}g · F {float(fat):.1f}g
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def card_header(
    title: str,
    subtitle: str | None = None,
    icon: str = "",
) -> None:
    """
    Compatibility function.
    Card section heading.
    """

    subtitle_html = ""

    if subtitle:
        subtitle_html = f"""
        <div style="
            color:#64748b;
            font-size:0.85rem;
            margin-top:0.25rem;
        ">
            {subtitle}
        </div>
        """

    st.markdown(
        f"""
        <div style="
            margin-bottom:1rem;
        ">
            <div style="
                display:flex;
                align-items:center;
                gap:0.5rem;
                font-size:1.05rem;
                font-weight:850;
                color:#0f172a;
            ">
                <span>{icon}</span>
                <span>{title}</span>
            </div>

            {subtitle_html}

        </div>
        """,
        unsafe_allow_html=True,
    )

def render_dashboard_greeting(user_name="User", calories_today=0, daily_goal=2200):
    remaining = max(daily_goal - calories_today, 0)
    st.markdown(
        f"""
        <div style="background:#ecfdf5;border:1px solid #99f6e4;border-radius:18px;
                    padding:1.5rem;margin-bottom:1rem;">
            <div style="display:flex;justify-content:space-between;align-items:center;
                        flex-wrap:wrap;gap:1rem;">
                <div>
                    <h1 style="margin:0;font-size:2rem;color:#0f172a;">
                        Welcome back, {user_name} 
                    </h1>
                    <p style="color:#64748b;margin-top:.4rem;margin-bottom:0;">
                        Here is your AI-powered nutrition overview for today.
                    </p>
                </div>
                <div style="background:white;border-radius:50px;padding:.8rem 1.2rem;
                            font-weight:800;white-space:nowrap;box-shadow:0 2px 8px rgba(0,0,0,.06);">
                    🔥 {calories_today:,.0f} kcal used · {remaining:,.0f} kcal left
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_stat_card(
    title,
    value,
    subtitle,
    icon="",
    color="#0d9488"
):

    st.markdown(
        f"""
        <div style="
            background:white;
            border-left:4px solid {color};
            border-radius:16px;
            padding:1.2rem;
            box-shadow:0 8px 20px rgba(0,0,0,.04);
        ">

        <div style="
            color:#94a3b8;
            font-size:.75rem;
            font-weight:800;
            letter-spacing:.08em;
        ">
        {title.upper()}
        </div>


        <div style="
            margin-top:.7rem;
            font-size:1.8rem;
            font-weight:900;
            color:#0f172a;
        ">
        {icon} {value}
        </div>


        <div style="
            color:#64748b;
            font-size:.85rem;
        ">
        {subtitle}
        </div>


        </div>
        """,
        unsafe_allow_html=True
    )


def render_ai_insight_card(
    title="AI Insight",
    insight="",
    icon="🥗"
):

    st.markdown(
        f"""
        <div style="
            background:#ecfdf5;
            border:1px solid #99f6e4;
            border-radius:16px;
            padding:1.2rem;
            margin:1rem 0;
        ">

        <b>{icon} {title}</b>

        <p style="
            margin-top:.7rem;
            color:#334155;
        ">
        {insight}
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )