# SOW - Data Extract Setup IUD

## Classification
- **Screen:** Configuration > Assets > Data_Mapping_Objects > Data Extract Setup (BF_CODE **SP.0043**)
- **Type/pattern:** OV (Manage-Object, `manage_object_nav`) - date-effective; plain (no mandatory dropdowns)
- **DB view:** `OV_SUMMARY_SETUP` (versioned); key `CODE`
- **Delete:** End Date = Start Date -> row leaves `OV_SUMMARY_SETUP`

## Nav / grid / cells
- **Open:** menu search "Data Extract Setup" -> `label.tv-link`. Navigator = single **Date + GO**; grid needs GO.
- **Grid:** shared T2 `${OV_MANAGE_OBJECT_TABLE}` (= `manage_object_nav_nav:form:T_data`).
- **NO hardcoded field ids** - resolved BY LABEL via T2 `Fill OV * By Label` / `OV Field Id By Label`:
  - **Insert (objectForm):** `Data Extract Setup Code`, `Data Extract Setup Name`, `Start Date` (mandatory). Optional dropdowns skipped.
  - **Update (updateAttributes):** `Data Extract Setup Name` (Code read-only; loaded-check via `OV Field Id By Label` on `Data Extract Setup Code`).
  - **Delete (objectdates):** `End Date` = Start Date.

## Test data
- `AUTOTEST_DXS_<timestamp>` unique per run; Start/End = `${TEST_START_DATE}` (2000-01-01). Never touch real rows.

## Dev story
Recon-first (DB `CLASS_TYPE=OBJECT` ⇒ OV; live form) -> plain Bank-layout OV, no mandatory dropdowns.
Built label-driven on the shared engine + T2 (zero engine changes). Playwright driver 7/7; RF T3+suite
label-driven -> live 4/4. All gates run + auto-ticked by `verify_screen.py` (OVERALL PASS).

## Lessons / known risks
- Optional dropdowns skipped (none mandatory). Delete uses engine `wait_for_row_absent` (async redraw).
