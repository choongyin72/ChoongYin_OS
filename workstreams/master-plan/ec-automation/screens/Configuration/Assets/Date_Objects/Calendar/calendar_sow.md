# SOW - Calendar IUD (CD.0024)

## 1. Screen identity
- **Screen:** Calendar
- **BF code:** CD.0024
- **Treeview path:** Configuration > Assets > Date Objects > Calendar
- **Bundle folder:** `screens/Configuration/Assets/Date_Objects/Calendar/`

## 2. Classification (DB-derived ground truth)
- **Class:** `CALENDAR` -- **OV (Manage-Object)**, `TIME_SCOPE_CODE=VERSIONED` -> date-effective -> DELETE = End Date = Start Date.
- **Base table:** `CALENDAR`; **OV view:** `OV_CALENDAR` (6 rows at recon).
- **Toolbar:** Insert + Delete enabled. **Custom-URL OV:** grid is **`nav:form:T_data`** (NOT `manage_object_nav_...`) and there is **NO navigator GO** -- reload via toolbar Refresh (cf. Account / Regulatory Permits). Confirmed live after an initial wrong-grid-id failure (see JOURNAL).
- **No child member grid** -- the extra grids on the screen (`daytimes`, `versions`) are the standard OV objectdates/versions sub-tabs, not a holiday/exception child grid. Plain OV.

## 3. New-Object form layout (DOM recon -- `investigation/recon_new_object_form.py`)
| Row | Field | Mandatory | Maps to |
|---|---|---|---|
| R:0:C:1:in | Code | YES | OBJECT_CODE / CODE |
| R:1:C:1:in | Name | YES | NAME |
| R:2:C:1:da_input | Start Date | effective | OBJECT_START_DATE |
| R:3:C:1:da_input | End Date | no | - |
| R:4 / R:5 :C:1:in | Description / Comments | no | DESCRIPTION / COMMENTS |
| R:6 .. R:12 :C:1:cb | Mon..Sun indicators (checkboxes) | no | MONDAY_IND .. SUNDAY_IND |

- **Mandatory set = Code + Name** (Start Date is the effective date). The 7 weekday indicator **checkboxes** are optional -> left at default -> a minimal Code/Name/Start-Date insert succeeds.
- **Update (updateAttributes):** Name R:1. **Delete (objectdates):** End Date R:0:C:3.

## 4. Test data + known risks
- **Code:** `AUTOTEST_CAL_<unique>` (RF) / `AUTOTEST_CAL_001` (Playwright). Unique-per-run; never touch existing rows.
- **No dropdown / no mandatory number** -> simplest of the 5 Date Objects screens (plain Bank-family OV).
- **Risk:** none beyond the standard OV flow; checkboxes deliberately not toggled (optional, default acceptable).

## 5. Deliverables
- T3: `pageobjects/Configuration/Assets/Date_Objects/calendar_page.resource`
- Suite: `tests/Configuration/Assets/Date_Objects/calendar_iud.robot`
- Playwright: `playwright/ec_iud_calendar.py`; Recon: `investigation/recon_new_object_form.py`; Evidence: `evidence/`.

## 6. Dev story + lessons
- 4th of 5 Date Objects screens. DB-first + DOM recon confirmed plain OV (no method/offset, no child grid) -> wrote a clean plain-OV T3/suite (Bank family) rather than carrying the term-screen dropdown machinery.
- T3 thin -- delegates to T2 `manage_object` generics. No shared-file edits. Full I-U-D. Stacked on CD.0023 (PR #143).
