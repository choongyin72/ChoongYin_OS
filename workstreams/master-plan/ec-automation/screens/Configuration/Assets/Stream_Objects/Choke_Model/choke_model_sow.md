# SOW — Choke Model IUD

## Classification
- **Screen:** Configuration > Assets > Stream Objects > Choke Model (BF_CODE **CO.0217**)
- **Type/pattern:** OV (Manage-Object, `manage_object_nav`) — date-effective; plain (optional dropdowns only)
- **DB view:** `OV_CHOKE_MODEL` (base `CHOKE_MODEL`/versioned); key `CODE`
- **Delete:** End Date = Start Date → row leaves `OV_CHOKE_MODEL`

## Nav / grid / cells
- **Open:** menu search "Choke Model" → `label.tv-link`. Grid needs GO.
- **Grid:** `manage_object_nav_nav:form:T_data`
- **Insert (objectForm):** Choke Model Code `R0:C1:in`, Choke Model Name `R1:C1:in`, **Start Date `R4:C1:da_input`** (mandatory; Sort Order R2 + Description R3 precede Start Date); many optional dropdowns R6+
- **Update (updateAttributes):** Name `R1:C1:in`, Description `R3:C1:in` (Code `R0` read-only)
- **Delete (objectdates):** End Date `R0:C3:da_input` = Start Date

## Test data
- `AUTOTEST_CHKM_<timestamp>` unique per run; Start/End = `${TEST_START_DATE}` (2000-01-01).

## Dev story
Recon-first (DB `CLASS_TYPE=OBJECT`; live form) → plain OV; **Start Date at R4** (not R2) + folder is Stream
Objects (Choke is Well and Reservoir — verified, not assumed sibling). Playwright thin driver → 7/7. Temp-row
recon of update ids (self-cleaned). RF T3+suite reuse T2 + DbVerify → live 4/4. All gates run + auto-ticked by
`verify_screen.py` (OVERALL PASS).

## Lessons / known risks
- Don't assume sibling screens share a folder or field layout — Choke (R2 Start Date, Well and Reservoir) vs
  Choke Model (R4 Start Date, Stream Objects) differ. Recon each.
- Many optional dropdowns; all skipped (none mandatory).
