# SOW - Chemical Transport Tank IUD

## Classification
- **Screen:** Configuration > Assets > Chemical_Objects > Chemical Transport Tank (BF_CODE **CO.0257**)
- **Type/pattern:** OV (Manage-Object, `manage_object_nav`) - date-effective; plain (no mandatory dropdowns)
- **DB view:** `OV_CHEM_TRANS_TANK` (versioned); key `CODE`
- **Delete:** End Date = Start Date -> row leaves `OV_CHEM_TRANS_TANK`

## Nav / grid / cells
- **Open:** menu search "Chemical Transport Tank" -> `label.tv-link`. Navigator = single **Date + GO**; grid needs GO.
- **Grid:** shared T2 `${OV_MANAGE_OBJECT_TABLE}` (= `manage_object_nav_nav:form:T_data`).
- **NO hardcoded field ids** - resolved BY LABEL via T2 `Fill OV * By Label` / `OV Field Id By Label`:
  - **Insert (objectForm):** `Transport Tank Code`, `Transport Tank Name`, `Start Date` (mandatory). Optional dropdowns skipped.
  - **Update (updateAttributes):** `Transport Tank Name` (Code read-only; loaded-check via `OV Field Id By Label` on `Transport Tank Code`).
  - **Delete (objectdates):** `End Date` = Start Date.

## Test data
- `AUTOTEST_CTT_<timestamp>` unique per run; Start/End = `${TEST_START_DATE}` (2000-01-01). Never touch real rows.

## Dev story
Recon-first (DB `CLASS_TYPE=OBJECT` ⇒ OV; live form) -> plain Bank-layout OV, no mandatory dropdowns.
Built label-driven on the shared engine + T2 (zero engine changes). Playwright driver 7/7; RF T3+suite
label-driven -> live 4/4. All gates run + auto-ticked by `verify_screen.py` (OVERALL PASS).

## Lessons / known risks
- Optional dropdowns skipped (none mandatory). Delete uses engine `wait_for_row_absent` (async redraw).
