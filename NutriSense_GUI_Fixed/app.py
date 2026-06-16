"""
NutriSense AI — Hugging Face Spaces Entry Point
================================================
HF Spaces runs: streamlit run app.py
This file bootstraps the app from streamlit_app/Home.py
"""

import sys
import os
from pathlib import Path

# ── Path setup ────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "streamlit_app"))
sys.path.insert(0, str(ROOT / "src"))

# ── Run Home page ─────────────────────────────────────────────────────────────
exec(open(ROOT / "streamlit_app" / "Home.py").read())