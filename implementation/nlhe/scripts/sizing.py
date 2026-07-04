"""Run the G6 sizing report from the repo config. Usage:
    python implementation/nlhe/scripts/sizing.py
"""
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

if __name__ == "__main__":
    import runpy
    runpy.run_path(str(SRC / "actions.py"), run_name="__main__")
