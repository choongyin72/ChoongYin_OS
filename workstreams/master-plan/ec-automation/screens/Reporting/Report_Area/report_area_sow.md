# SOW — Report Area IUD

## Classification
- **Screen:** Reporting > Report Area (BF_CODE **RP.0017**)
- **Type/pattern:** OV (Manage-Object, `manage_object_nav`) — date-effective; **plain, simplest OV** (no dropdowns, no Description)
- **DB view:** `OV_REPORT_AREA` (base `REPORT_AREA`/versioned); key `CODE`
- **Delete:** End Date = Start Date → row leaves `OV_REPORT_AREA`

## Nav / grid / cells
- **Open:** menu search "Report Area" → `label.tv-link`. **Grid needs GO** to load (no default rows).
- **Grid:** `manage_object_nav_nav:form:T_data`
- **Insert (objectForm):** Report Area Code `R0:C1:in`, Report Area Name `R1:C1:in`, Start date `R2:C1:da_input` (mandatory); End date `R3` optional
- **Update (updateAttributes):** Report Area Name `R1:C1:in` (Code `R0` read-only)
- **Delete (objectdates):** End date `R0:C3:da_input` = Start Date

## Test data
- `AUTOTEST_RPTA_<timestamp>` unique per run; Start/End = `${TEST_START_DATE}` (2000-01-01).

## Dev story
Recon-first (DB + live form) confirmed the simplest OV shape (Code/Name/Start Date; no Description). Playwright
thin driver over the shared engine → 7/7 first run. Temp-row recon of `updateAttributes`/`objectdates` ids
(self-cleaned) → RF T3+suite reuse T2 `manage_object` + `DbVerify.py` → live 4/4, update DB-verified via
`Field Should Equal In View`.

## Lessons / known risks
- Under top-level **Reporting** menu (not Configuration/Assets); RF/bundle in `Reporting/`.
- Grid does not auto-load — GO after open (T3 `Open ... Screen` calls `Apply Navigator`).
- No Description column — update = Name only.
