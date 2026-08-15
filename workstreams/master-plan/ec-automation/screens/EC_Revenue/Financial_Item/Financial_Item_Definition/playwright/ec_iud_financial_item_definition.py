"""Financial Item Definition - Playwright reference flow. Delegates to the actual driver at
py/financial_item_definition_iud.py (kept in one place, not duplicated).

Run headed: EC_HEADED=1 py -X utf8 <this file>
"""
import runpy
from pathlib import Path

_DRIVER = Path(__file__).resolve().parents[5] / "py" / "financial_item_definition_iud.py"

if __name__ == "__main__":
    runpy.run_path(str(_DRIVER), run_name="__main__")
