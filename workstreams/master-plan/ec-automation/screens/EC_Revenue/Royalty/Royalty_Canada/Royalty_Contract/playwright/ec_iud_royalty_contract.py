"""Royalty Contract - Playwright reference flow. Delegates to the actual driver at
py/royalty_contract_iud.py (kept in one place, not duplicated). INSERT+UPDATE-ONLY - see that
file's module docstring for why Delete is permanently out of scope on this screen.

Run headed: EC_HEADED=1 py -X utf8 <this file>
"""
import runpy
from pathlib import Path

_DRIVER = Path(__file__).resolve().parents[6] / "py" / "royalty_contract_iud.py"

if __name__ == "__main__":
    runpy.run_path(str(_DRIVER), run_name="__main__")
