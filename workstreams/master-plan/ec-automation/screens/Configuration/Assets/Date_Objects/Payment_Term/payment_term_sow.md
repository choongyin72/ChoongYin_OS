# SOW - Payment Term IUD (CD.0023)

## 1. Screen identity
- **Screen:** Payment Term
- **BF code:** CD.0023
- **Treeview path:** Configuration > Assets > Date Objects > Payment Term
- **Bundle folder:** `screens/Configuration/Assets/Date_Objects/Payment_Term/`

## 2. Classification (DB-derived ground truth)
- **Class:** `PAYMENT_TERM` -- **OV (Manage-Object)**, `TIME_SCOPE_CODE=VERSIONED` -> date-effective -> DELETE = End Date = Start Date.
- **Base table:** `PAYMENT_TERM`; **OV view:** `OV_PAYMENT_TERM` (91 rows at recon).
- **Toolbar:** Insert + Delete enabled. **Navigator:** single date + GO; grid `manage_object_nav_nav:form:T_data`.

Same OV family as the term screens, but a **richer New-Object form** (10 fields, with the method/value cells shifted down by the extra optional fields).

## 3. New-Object form layout (DOM recon -- `investigation/recon_new_object_form.py`)
| Row | Field | Mandatory | Maps to |
|---|---|---|---|
| R:0:C:1:in | Code | YES | OBJECT_CODE / CODE |
| R:1:C:1:in | Name | YES | NAME |
| R:2:C:1:da_input | Start Date | effective | OBJECT_START_DATE |
| R:3:C:1:da_input | End Date | no | - |
| R:4 / R:5 / R:6 :C:1:in | text | no | DESCRIPTION / COMMENTS / FIN_CODE |
| **R:7:C:1:dd** | **Method** (autocomplete) | (defaulted) | PAYMENT_TERM_METHOD |
| **R:8:C:1:in** | **Day Value** (number) | YES | DAY_VALUE |
| R:9:C:1:dd | Calculation (autocomplete) | no (empty options) | CALCULATION_CODE |

- **Note:** the T3/suite/playwright variable named `*_OFFSET` is the **R:8 DAY_VALUE** cell (generic clone naming kept; semantics = "day value").
- **Method labels** (recon): 'No Date', 'Fixed Date in Current Month', 'Fixed Date in Next Month', 'Fixed number of Working Days', 'Fixed number of Days'.
- **Update (updateAttributes):** Name R:1. **Delete (objectdates):** End Date R:0:C:3.

## 4. Test data + known risks
- **Code:** `AUTOTEST_PT_<unique>` (RF) / `AUTOTEST_PT_PW01` (Playwright). Unique-per-run; never touch existing rows.
- **Method:** `Fixed number of Days` + **Day Value = 30** -- a realistic "30 days" payment term (matches existing rows like D30T).
- **Risk -- shifted field rows:** unlike the term screens (Method R6 / number R7), Payment Term has Method at **R7** and the mandatory number at **R8** (extra optional FIN_CODE + Calculation fields). Confirmed by recon before building -- not assumed.
- **Risk -- mandatory DAY_VALUE (R8)** + **METHOD dropdown re-render** after the Start-Date Tab-out: number filled last; shared `Select EC Dropdown Option` has the re-open retry. R:9 Calculation dd is optional + empty -> skipped.

## 5. Deliverables
- T3: `pageobjects/Configuration/Assets/Date_Objects/payment_term_page.resource`
- Suite: `tests/Configuration/Assets/Date_Objects/payment_term_iud.robot`
- Playwright: `playwright/ec_iud_payment_term.py`; Recon: `investigation/`; Evidence: `evidence/`.

## 6. Dev story + lessons
- 3rd of 5 Date Objects screens. DB-first recon flagged the extra columns (FIN_CODE, DAY_VALUE, CALCULATION_CODE); live DOM recon confirmed the **shifted field rows** -> remapped the clone's Method/number ids (R6/R7 -> R7/R8) rather than blind-cloning. (Template-trust-boundary lesson: recon the form, don't trust the exemplar's row indices.)
- T3 thin -- reuses T2 `manage_object` + shared `Select EC Dropdown Option`; no shared-file edits. Full I-U-D. Stacked on CD.0108 (PR #142).
