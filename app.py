"""
NutriSense AI — Application Launcher
=====================================
Phase II: Streamlit GUI + SQLite database (dummy predictions, no ML model yet).

Run the app:
    streamlit run streamlit_app/Home.py

Or from this file:
    streamlit run app.py
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HOME = ROOT / "streamlit_app" / "Home.py"


def main() -> None:
    """Launch the Streamlit dashboard."""
    if not HOME.exists():
        print(f"Error: entry point not found at {HOME}")
        sys.exit(1)

    print("=" * 60)
    print("  NutriSense AI — Phase 1 GUI Prototype")
    print("=" * 60)
    print()
    print("  Starting Streamlit server...")
    print(f"  Entry: {HOME}")
    print()
    print("  Command:")
    print("    streamlit run streamlit_app/Home.py")
    print()
    print("=" * 60)

    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", str(HOME)],
        cwd=str(ROOT),
        check=False,
    )


if __name__ == "__main__":
    main()
