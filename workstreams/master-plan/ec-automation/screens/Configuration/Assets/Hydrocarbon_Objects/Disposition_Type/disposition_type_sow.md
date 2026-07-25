# SOW — Disposition Type IUD

## Classification
- **Screen:** Configuration > Assets > Hydrocarbon Objects > Disposition Type (BF_CODE **CO.0208**)
- **Type/pattern:** OV (Manage-Object, `manage_object_nav`) — date-effective; **plain** (no mandatory ref dropdowns)
- **DB view:** `OV_DISPOSITION_TYPE` (base `DISPOSITION_TYPE` / versioned); key `CODE`
- **Delete:** End Date = Start Date (zero-length window) → row leaves `OV_DISPOSITION_TYPE`

## Nav / grid / cells
- **Open:** menu search "Disposition Type" → `label.tv-link`. **Grid needs GO** (`#button:form:B`) to load (no default rows).
- **Grid:** `manage_object_nav_nav:form:T_data` (Code / Name / Start Date / End Date)
- **Insert (objectForm):** Disposition Code `R2:C1:in`, Disposition Name `R3:C1:in`, Start Date `R4:C1:da_input` (mandatory/yellow); optional End Date/Sort Order/Description/Product(dd)
- **Update (updateAttributes):** Disposition Name `R3:C1:in`, Description `R5:C1:in` (Code `R2` read-only)
- **Delete (objectdates):** End Date `R0:C3:da_input` = Start Date

## Test data
- `AUTOTEST_DISP_<timestamp>` (unique per run; EC keeps deleted codes). Start/End = `${TEST_START_DATE}` (2000-01-01).

## Dev story
Recon-first (DB metadata + live New-Object scan) confirmed plain OV, mandatory at R2/R3/R4. Built the Playwright
driver as a thin config over the shared engine (zero engine changes) → 7/7 first run. Inserted a temp row to recon
`updateAttributes`/`objectdates` ids for the RF T3 (self-cleaned). RF T3+suite reuse T2 `manage_object` + `DbVerify.py`
→ live 4/4, update DB-verified via the new `Field Should Equal In View` keyword.

## Lessons / known risks
- Mandatory fields at R2/R3 (not R0/R1) — R0/R1 are optional Master System Code/Name. Don't clone Bank's row indices.
- Grid does not auto-load — GO after open (T3 `Open ... Screen` calls `Apply Navigator`).
- Labels are "Disposition Code/Name" — engine resolves by label; RF T3 pins the ids.
