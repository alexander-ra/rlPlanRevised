"""Put this chapter's implementation/ folder on sys.path (the exploration scripts reuse it)."""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
IMPL = os.path.abspath(os.path.join(_HERE, "..", "implementation"))
if IMPL not in sys.path:
    sys.path.insert(0, IMPL)
FIG = os.path.join(_HERE, "figures")
os.makedirs(FIG, exist_ok=True)
