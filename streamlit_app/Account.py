from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from src.utils.helpers import init_app
from src.database.user import get_default_user, create_user, verify_login


def render_account_page() -> None:
    """Sign In / Sign Up screen."""
    init_app()

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    [data-testid="stSidebar"], header[data-testid="stHeader"] { display: none !important; }
    [data-testid="stAppViewContainer"] > .main { padding-top: 0 !important; }
    [data-testid="stAppViewContainer"], html, body {
        background: #f0f4f8 !important;
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }
    .block-container { max-width: 440px !important; padding-top: 3rem !important; margin: 0 auto !important; }

    /* Brand */
    .auth-brand { text-align: center; margin-bottom: 1.5rem; }
    .auth-logo  { font-size: 2.5rem; line-height: 1; }
    .auth-title { font-size: 1.45rem; font-weight: 800; color: #0f172a; letter-spacing: -0.025em; margin-top: 0.4rem; }
    .auth-sub   { font-size: 0.83rem; color: #64748b; margin-top: 0.2rem; }
    .auth-tagline {
        display: inline-block;
        background: #ecfdf5; color: #047857; border: 1px solid #a7f3d0;
        border-radius: 20px; padding: 0.2rem 0.75rem; font-size: 0.72rem;
        font-weight: 600; margin-top: 0.5rem; letter-spacing: 0.02em;
    }

    /* Card */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: #ffffff !important; border-radius: 14px !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 4px 20px rgba(15,23,42,0.07) !important;
        padding: 1.5rem 1.5rem !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 0; }
    .stTabs [data-baseweb="tab"] { font-size: 0.85rem; font-weight: 600; color: #64748b; padding: 0.55rem 1.1rem; }
    .stTabs [aria-selected="true"] { color: #047857 !important; }
    .stTabs [data-baseweb="tab-highlight"] { background-color: #0d9488 !important; }

    /* Inputs */
    .stTextInput input {
        border-radius: 8px !important; border: 1px solid #e2e8f0 !important;
        font-size: 0.86rem !important; padding: 0.5rem 0.75rem !important;
        transition: border-color 0.15s, box-shadow 0.15s;
    }
    .stTextInput input:focus { border-color: #0d9488 !important; box-shadow: 0 0 0 3px rgba(13,148,136,0.1) !important; }

    /* Primary button */
    .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #0d9488, #0284c7) !important;
        border: none !important; border-radius: 8px !important;
        font-weight: 700 !important; font-size: 0.86rem !important;
        width: 100%; padding: 0.55rem !important;
        box-shadow: 0 2px 8px rgba(13,148,136,0.25) !important;
    }
    .stButton button[kind="primary"]:hover { opacity: 0.9 !important; }

    /* Demo button */
    .demo-btn-wrap { text-align: center; margin-top: 0.5rem; }

    .auth-footnote { text-align: center; font-size: 0.73rem; color: #94a3b8; margin-top: 1rem; }
        
        /* Hide Press Enter to apply */
    [data-testid="InputInstructions"] {
        display: none !important;
        visibility: hidden !important;
    }
    small[data-testid="InputInstructions"] {
        display: none !important;
    }            
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="auth-brand">
        <div class="auth-logo">🥗</div>
        <div class="auth-title">NutriSense AI</div>
        <div class="auth-sub">AI Nutrition Intelligence Platform</div>
        <div><span class="auth-tagline">✦ EfficientNetB0 · Pakistani & International Foods</span></div>
    </div>
    """, unsafe_allow_html=True)

    tab_in, tab_up = st.tabs(["Sign In", "Create Account"])

    # ── Sign In ────────────────────────────────────────────────────────────────
    with tab_in:
        with st.container(border=True):
            st.markdown("##### Welcome back")
            st.markdown("<div style='font-size:0.8rem;color:#64748b;margin-bottom:0.75rem'>Sign in to your NutriSense account</div>", unsafe_allow_html=True)

            email_in    = st.text_input("Email address", key="si_email", placeholder="you@example.com")
            password_in = st.text_input("Password",      key="si_pass",  type="password", placeholder="••••••••")

            if st.button("Sign In →", type="primary", key="signin_btn"):
                if not email_in or not password_in:
                    st.error("Please enter your email and password.")
                else:
                    user = verify_login(email_in, password_in)
                    if user:
                        st.session_state["authenticated"] = True
                        st.session_state["user_id"]       = user["id"]
                        st.session_state["user_email"]    = user["email"]
                        st.session_state["user_name"]     = user.get("name", "User")
                        st.success(f"✅ Welcome back, {user.get('name', 'User')}!")
                        st.rerun()
                    else:
                        st.error("Invalid email or password.")

            st.markdown("<div style='text-align:center;margin:0.6rem 0;font-size:0.72rem;color:#cbd5e1'>— or —</div>", unsafe_allow_html=True)
            if st.button("Continue as Demo User", use_container_width=True, key="demo_btn"):
                demo = get_default_user()
                st.session_state["authenticated"] = True
                st.session_state["user_id"]       = demo["id"]
                st.session_state["user_email"]    = demo.get("email", "demo@nutrisense.ai")
                st.session_state["user_name"]     = demo.get("name", "Demo User")
                st.rerun()

    # ── Sign Up ────────────────────────────────────────────────────────────────
    with tab_up:
        with st.container(border=True):
            st.markdown("##### Create your account")
            st.markdown("<div style='font-size:0.8rem;color:#64748b;margin-bottom:0.75rem'>Free account — no credit card required</div>", unsafe_allow_html=True)

            name_up  = st.text_input("Full name",       key="su_name",  placeholder="Aisha Khan")
            email_up = st.text_input("Email address",   key="su_email", placeholder="you@example.com")
            pass_up  = st.text_input("Password",        key="su_pass",  type="password", placeholder="••••••••")
            pass_up2 = st.text_input("Confirm password",key="su_pass2", type="password", placeholder="••••••••")

            if st.button("Create Account →", type="primary", key="signup_btn"):
                if not all([name_up, email_up, pass_up, pass_up2]):
                    st.error("All fields are required.")
                elif pass_up != pass_up2:
                    st.error("Passwords do not match.")
                elif len(pass_up) < 6:
                    st.error("Password must be at least 6 characters.")
                else:
                    try:
                        user = create_user(name_up, email_up, pass_up)
                        st.session_state["authenticated"] = True
                        st.session_state["user_id"]       = user["id"]
                        st.session_state["user_email"]    = user["email"]
                        st.session_state["user_name"]     = user.get("name", name_up)
                        st.success(f"✅ Account created! Welcome, {name_up}!")
                        st.rerun()
                    except ValueError as e:
                        st.error(str(e))

    st.markdown(
        '<div class="auth-footnote">By continuing you agree to NutriSense AI\'s Terms of Service.<br>'
        'Your data is stored locally and never shared.</div>',
        unsafe_allow_html=True,
    )
