# SOW - Document Date Term IUD (CD.0107)

## 1. Screen identity
- **Screen:** Document Date Term
- **BF code:** CD.0107
- **Treeview path:** Configuration > Assets > Date Objects > Document Date Term
- **Bundle folder:** `screens/Configuration/Assets/Date_Objects/Document_Date_Term/`

## 2. Classification (DB-derived ground truth)
- **Class:** `DOC_DATE_TERM`
- **CLASS_TYPE:** `OBJECT` -> **OV (Manage-Object)**
- **TIME_SCOPE_CODE:** `VERSIONED` -> **date-effective** -> DELETE = End Date = Start Date (true delete)
- **Base table:** `DOC_DATE_TERM` (version attr `DOC_DATE_TERM_VERSION`)
- **OV view:** `OV_DOC_DATE_TERM` (134 rows at recon)
- **Toolbar:** Insert + Delete **enabled** (master-data OV -> full IUD supported)
- **Navigator:** single date field (G:0) + GO (`button:form:B`); grid id `manage_object_nav_nav:form:T_data`

This is the **same OV pattern as Bank**, with two extra mandatory inputs on the New-Object form.

## 3. New-Object form layout (DOM recon -- `investigation/recon_new_object_form.py`)
| Row | Field | Mandatory | Maps to | Notes |
|---|---|---|---|---|
| R:0:C:1:in | Code | YES | OBJECT_CODE / CODE | |
| R:1:C:1:in | Name | YES | NAME | |
| R:2:C:1:da_input | Start Date | effective date | OBJECT_START_DATE | version date |
| R:3:C:1:da_input | End Date | no | - | optional on insert |
| R:4 / R:5 :C:1:in | Description / Comments | no | DESCRIPTION / COMMENTS | |
| R:6:C:1:dd | **Method** (autocomplete) | (defaulted) | DOC_DATE_TERM_METHOD | enum: MANUAL/SYSDATE/CAL_*/BL_* |
| R:7:C:1:in | **Offset** (number) | YES | OFFSET | mandatory numeric cell |

- **Method dropdown labels** (`investigation/recon_method_dropdown.py`): 'Set Document Date manually' (=MANUAL), 'System Date as Document Date' (=SYSDATE), 'Workdays in current Month', ... etc.
- **Update (updateAttributes):** Name at R:1 (Code read-only after creation).
- **Delete (objectdates):** End Date at R:0:C:3:da_input -> set = Start Date.

## 4. Test data + known risks
- **Code:** `AUTOTEST_DDT_<unique>` (RF) / `AUTOTEST_DDT_PW01` (Playwright). Unique-per-run; never reuse, never touch existing rows.
- **Method:** `Set Document Date manually` (MANUAL) + **Offset = 0** -- simplest valid combination (no calendar dependency).
- **Start/End Date:** `${TEST_START_DATE}` (2000-01-01) for delete End=Start.
- **Risk -- mandatory OFFSET:** unlike Bank's 3-field form, OFFSET (R:7) is a mandatory numeric cell; a silent insert reject occurs if it is left empty. Filled last so neither the date Tab-out nor the dropdown re-render clears it.
- **Risk -- METHOD dropdown re-render:** the autocomplete panel can close after the Start-Date Tab-out; the shared `Select EC Dropdown Option` has a built-in re-open retry, used here.

## 5. Deliverables
- T3 page object: `pageobjects/Configuration/Assets/Date_Objects/document_date_term_page.resource`
- Suite: `tests/Configuration/Assets/Date_Objects/document_date_term_iud.robot`
- Playwright: `playwright/ec_iud_document_date_term.py`
- Recon: `investigation/recon_new_object_form.py`, `recon_method_dropdown.py`
- Evidence: `evidence/` (11 screenshots + results.json)

## 6. Dev story + lessons
- **Pilot for the new 19-item IUD deliverable standard** (`docs/IUD-DELIVERABLE-CHECKLIST.md`). First screen built to prove the CHECKLIST.md bundle format + reviewer gate end-to-end before batching CD.0108/0023/0024/0105.
- T3 kept **thin** -- delegates Insert/Update/Delete to T2 `manage_object` generics (`Fill New Object Form`, `Update Object Name`, `Delete Object Via End Date`); only the screen-specific extras (METHOD dropdown + OFFSET) are filled in the T3 Insert wrapper, exactly as T2's docstring anticipates ("screen-specific mandatory extras filled by the caller").
- Reused the shared `Select EC Dropdown Option` (table.resource) for METHOD -- no new shared-file edits, no T1/T2 changes (R12 not triggered).
- **Scope = full I-U-D** (RC.0050 lesson: never ship I/D only). TC03 update edits Name; verified present-in-view.
