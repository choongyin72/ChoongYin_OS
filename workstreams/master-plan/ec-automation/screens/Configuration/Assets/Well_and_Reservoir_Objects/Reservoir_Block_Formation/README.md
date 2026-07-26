# Reservoir Block Formation (CO.0137) — OV junction IUD bundle

Multi-object screen: RBF links a Reservoir Block + Reservoir Formation (dependent dropdowns). Full I‑U‑D
proven by the Playwright driver (create both parents → link → reverse teardown), DB-verified, self-clean.

## Artifacts
- **Playwright driver:** `../../../../py/reservoir_block_formation_iud.py` — **15/15 PASS** (definitive proof)
- **RF T3/suite:** `../../../../pageobjects/.../reservoir_block_formation_page.resource` + `tests/.../reservoir_block_formation_iud.robot` — **WIP** (2 RF-gesture issues, see SOW)
- SOW · JOURNAL · investigation/ · evidence/ (rbf_*.png) · VERIFY-REPORT.md (driver PASS; RF WIP)

## Run
`EC_HEADED=0 py -X utf8 workstreams/master-plan/ec-automation/py/reservoir_block_formation_iud.py` → ALL PASS
