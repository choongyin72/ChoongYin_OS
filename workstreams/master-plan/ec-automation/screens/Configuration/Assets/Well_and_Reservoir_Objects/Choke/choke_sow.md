# SOW — Choke IUD

## Classification
- **Screen:** Configuration > Assets > Well and Reservoir Objects > Choke (BF_CODE **CO.0185**)
- **Type/pattern:** OV (Manage-Object, `manage_object_nav`) — date-effective; plain (optional Choke Type dropdown only)
- **DB view:** `OV_CHOKE` (base `CHOKE`/versioned); key `CODE`
- **Delete:** End Date = Start Date → row leaves `OV_CHOKE`

## Nav / grid / cells
- **Open:** menu search "Choke" → `label.tv-link`. Grid needs GO; has seed data (e.g. `P1 C001` — never touch).
- **Grid:** `manage_object_nav_nav:form:T_data`
- **Insert (objectForm):** Choke Code `R0:C1:in`, Choke Name `R1:C1:in`, Start Date `R2:C1:da_input` (mandatory); End Date R3, Choke Type dd R4, Critical Opening R5, Comments R6 optional
- **Update (updateAttributes):** Choke Name `R1:C1:in`, Comments `R4:C1:in` (Code `R0` read-only)
- **Delete (objectdates):** End Date `R0:C3:da_input` = Start Date

## Test data
- `AUTOTEST_CHK_<timestamp>` unique per run; Start/End = `${TEST_START_DATE}` (2000-01-01).

## Dev story
Recon-first (DB `CLASS_TYPE=OBJECT` confirmed OV; live form) → plain OV, no mandatory dropdowns. Playwright thin
driver over the shared engine → 7/7. Temp-row recon of `updateAttributes`/`objectdates` ids (self-cleaned) →
RF T3+suite reuse T2 `manage_object` + DbVerify → live 4/4. All gates run + auto-ticked by `verify_screen.py`
(OVERALL PASS) — no hand-ticking.

## Lessons / known risks
- Grid has real seed data — strict AUTOTEST_ + never-touch-existing.
- Optional Choke Type ref dropdown left default (not mandatory).
- Every T3 keyword documented up-front (robocop DOC01 lesson from Report Area) → robocop clean first run.
