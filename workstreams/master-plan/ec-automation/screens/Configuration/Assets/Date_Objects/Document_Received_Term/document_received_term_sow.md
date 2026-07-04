# SOW - Document Received Term IUD (CD.0108)

## 1. Screen identity
- **Screen:** Document Received Term
- **BF code:** CD.0108
- **Treeview path:** Configuration > Assets > Date Objects > Document Received Term
- **Bundle folder:** `screens/Configuration/Assets/Date_Objects/Document_Received_Term/`

## 2. Classification (DB-derived ground truth)
- **Class:** `DOC_RECEIVED_TERM`
- **CLASS_TYPE:** `OBJECT` -> **OV (Manage-Object)**
- **TIME_SCOPE_CODE:** `VERSIONED` -> **date-effective** -> DELETE = End Date = Start Date (true delete)
- **Base table:** `DOC_RECEIVED_TERM` (version attr `DOC_REC_TERM_VERSION`)
- **OV view:** `OV_DOC_RECEIVED_TERM` (44 rows at recon)
- **Toolbar:** Insert + Delete **enabled** (master-data OV -> full IUD supported)
- **Navigator:** single date field (G:0) + GO; grid id `manage_object_nav_nav:form:T_data`

**Sibling of Document Date Term (CD.0107)** -- identical OV form shape; only the METHOD enum differs.

## 3. New-Object form layout (DOM recon -- `investigation/recon_new_object_form.py`)
| Row | Field | Mandatory | Maps to |
|---|---|---|---|
| R:0:C:1:in | Code | YES | OBJECT_CODE / CODE |
| R:1:C:1:in | Name | YES | NAME |
| R:2:C:1:da_input | Start Date | effective date | OBJECT_START_DATE |
| R:3:C:1:da_input | End Date | no | - |
| R:4 / R:5 :C:1:in | Description / Comments | no | DESCRIPTION / COMMENTS |
| R:6:C:1:dd | **Method** (autocomplete) | (defaulted) | DOC_REC_TERM_METHOD |
| R:7:C:1:in | **Offset** (number) | YES | OFFSET |

- **Method dropdown labels** (recon): 'Manual entry', 'No Date', 'Fixed Date in Current Month', 'Fixed Date in Next Month', 'Fixed number of Working Days', 'Fixed number of Days', ... (existing rows e.g. DOCDATE='Received date is invoice date', BC20='Base Date + 20 Calendar Days').
- **Update (updateAttributes):** Name at R:1 (Code read-only). **Delete (objectdates):** End Date at R:0:C:3:da_input.

## 4. Test data + known risks
- **Code:** `AUTOTEST_DRT_<unique>` (RF) / `AUTOTEST_DRT_PW01` (Playwright). Unique-per-run; never touch existing rows.
- **Method:** `Manual entry` + **Offset = 0** -- simplest valid combination.
- **Risk -- mandatory OFFSET** (R:7) and **METHOD dropdown re-render** after the Start-Date Tab-out: same as CD.0107; OFFSET filled last; shared `Select EC Dropdown Option` has the re-open retry.

## 5. Deliverables
- T3: `pageobjects/Configuration/Assets/Date_Objects/document_received_term_page.resource`
- Suite: `tests/Configuration/Assets/Date_Objects/document_received_term_iud.robot`
- Playwright: `playwright/ec_iud_document_received_term.py`
- Recon: `investigation/recon_new_object_form.py`, `recon_method_dropdown.py`
- Evidence: `evidence/` (screenshots + results.json)

## 6. Dev story + lessons
- 2nd of 5 Date Objects screens; clean clone of the CD.0107 pilot (proven OV + METHOD-dropdown + OFFSET pattern), confirming the pilot's pattern generalises to siblings.
- T3 thin -- delegates to T2 `manage_object` generics + shared `Select EC Dropdown Option`. No shared-file edits (R12 not triggered).
- Full I-U-D scope (RC.0050 lesson). Stacked on CD.0107 (PR #141) so the registry/scorecard appends don't conflict.
