# Meter Run (CO.0091) - OV IUD bundle

Manage-Object (OV) screen: **Configuration > Assets > Stream_Objects > Meter Run**. Full Insert /
Update / Delete (End Date = Start Date), DB-verified against `OV_METER_RUN`, self-cleaning.

**Rebuilt 2026-08-23 (PR #462, Batch 8 of the Bank-pattern conversion project)** from the original
label-driven-only shape to the full **Bank-pattern** shape: properties-file-driven insert/update/
verify + explicit grid-filter wiring, T2-consolidated, mirroring `bank_page.resource`/
`berth_page.resource`. This bundle's SOW/README/JOURNAL/CHECKLIST/evidence/KB map were backfilled
2026-08-27/28 per `docs/lean-deliverable-backfill-workorder.md` (Batch 9) - the RF automation
itself was NOT touched by this backfill.

## Artifacts
- **SOW:** `meter_run_sow.md`
- **RF T3:** `../../../pageobjects/Configuration/Assets/Stream_Objects/meter_run_page.resource`
- **RF suite:** `../../../tests/Configuration/Assets/Stream_Objects/meter_run_iud.robot`
- **Testdata:** `../../../testdata/meter_run_insert.properties`, `meter_run_update.properties`,
  `meter_run_form_verify.properties`, `meter_run_grid_verify.properties`
- **Playwright driver (unchanged, pre-existing, out of scope for this backfill):**
  `../../../py/meter_run_iud.py`
- **investigation/** recon.py (pre-existing, 2026-07-26 original build) - **evidence/**
  screenshots + RF report from the 2026-08-28 backfill evidence-capture run
- **VERIFY-REPORT.md** (pre-existing, from the 2026-07-26 original build; predates the Batch 8
  conversion - kept for history, superseded in practice by the commands/results below)

## Exact commands to run this suite
```bash
cd workstreams/master-plan/ec-automation

# Dryrun (syntax/keyword-resolution check, no browser/DB)
py -m robot --dryrun --outputdir tmp_dryrun_meterrun tests/Configuration/Assets/Stream_Objects/meter_run_iud.robot

# Live headless run (real browser + DB)
EC_HEADLESS=true py -m robot --outputdir tmp_live_meterrun tests/Configuration/Assets/Stream_Objects/meter_run_iud.robot
```

## DB self-clean check (fresh connection, run before AND after the live suite)
```python
import sys
sys.path.insert(0, "libraries")
from DbVerify import fetch_object
row = fetch_object("OV_METER_RUN", "AUTOTEST_METER_RUN")
print(row)   # expect None both before and after a clean run
```

## Verified (real runs, not hand-ticked)
- **2026-07-26 (original build):** robocop 0, hygiene 0, dryrun 4/4, live RF 4/4, Playwright 7/7,
  self-clean 0 residual.
- **2026-08-23 (PR #462, Batch 8 conversion):** robocop 9 issues (parity with `berth_iud.robot`
  baseline, not a regression), full `tests/` tree dryrun 758/758, live RF **5/5**, filter keyword
  fired 15/15 (`Find/Clear Object Row By Filter`), DB self-clean 0 residual (fresh connection).
- **2026-08-28 (this backfill's evidence-capture re-run):** dryrun 5/5, live RF **5/5**, filter
  keyword fired 15/15, robocop 9 issues (same as PR #462's cited baseline - not a regression),
  hygiene PASS, DB self-clean 0 residual (fresh connection, before and after) - see `evidence/`.
