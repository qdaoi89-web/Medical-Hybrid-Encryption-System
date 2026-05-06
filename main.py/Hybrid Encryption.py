"""Deprecated entry point. Prefer running from the repository root:

    python -m medical_vault
"""

import runpy
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

if __name__ == "__main__":
    runpy.run_module("medical_vault", run_name="__main__")
