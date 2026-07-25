"""EC IUD Bank (Playwright) - SUPERSEDED, kept as a pointer.

The standalone Bank Playwright bundle has been consolidated into the reusable engine + driver
(single implementation, DB-verified 7/7, self-cleaning):

    engine   : workstreams/master-plan/ec-automation/py/ec_object_iud.py   (generic OV IUD)
    driver   : workstreams/master-plan/ec-automation/py/bank_iud.py        (Bank config only)
    DB verify: workstreams/master-plan/ec-automation/libraries/DbVerify.py (single ground-truth lib)
    selectors: ec-ui-knowledge/screens/bank.md  |  pattern: ec-ui-knowledge/EC_OBJECT_CONFIG_IUD.md

This file remains so the per-screen bundle path stays valid; running it delegates to the driver.
The original standalone version is in git history if ever needed.
"""
import runpy
from pathlib import Path

_DRIVER = Path(__file__).resolve().parents[6] / "py" / "bank_iud.py"

if __name__ == "__main__":
    runpy.run_path(str(_DRIVER), run_name="__main__")
