# SOW - Calendar Collection IUD (CD.0105)

## 1. Screen identity
- **Screen:** Calendar Collection
- **BF code:** CD.0105
- **Treeview path:** Configuration > Assets > Date Objects > Calendar Collection
- **Bundle folder:** `screens/Configuration/Assets/Date_Objects/Calendar_Collection/`

## 2. Classification (DB-derived ground truth)
- **Class:** `CALENDAR_COLLECTION` -- **OV (Manage-Object)**, `TIME_SCOPE_CODE=VERSIONED` -> date-effective -> DELETE = End Date = Start Date.
- **Base table:** `CALENDAR_COLLECTION`; **OV view:** `OV_CALENDAR_COLLECTION` (7 rows at recon).
- **Toolbar:** Insert + Delete enabled. **Custom-URL OV:** grid **`nav:form:T_data`**, **NO navigator GO** (toolbar Refresh) -- same shape as Calendar (CD.0024).
- **Member calendars** (the calendars belonging to a collection) live in a child grid/tab; the **object-level IUD** tested here is just Code/Name/Start Date -- the membership child grid is out of scope for object IUD.

## 3. New-Object form layout (DOM recon -- `investigation/recon_new_object_form.py`)
| Row | Field | Mandatory | Maps to |
|---|---|---|---|
| R:0:C:1:in | Code | YES | OBJECT_CODE / CODE |
| R:1:C:1:in | Name | YES | NAME |
| R:2:C:1:da_input | Start Date | effective | OBJECT_START_DATE |
| R:3:C:1:da_input | End Date | no | - |
| R:4 / R:5 :C:1:in | Description / Comments | no | DESCRIPTION / COMMENTS |

- **Mandatory set = Code + Name** (Start Date = effective). No dropdown, no number, no checkbox -- the simplest OV form of the batch (tied with Calendar minus the weekday checkboxes).
- **Update (updateAttributes):** Name R:1. **Delete (objectdates):** End Date R:0:C:3.

## 4. Test data + known risks
- **Code:** `AUTOTEST_CC_<unique>` (RF) / `AUTOTEST_CC_001` (Playwright). Unique-per-run; never touch existing rows.
- **Risk:** custom-URL OV (grid `nav:form:T_data`, no GO) -- carried over from the Calendar lesson; used the same plain-OV T3 with the Refresh fallback. No other risks.

## 5. Deliverables
- T3: `pageobjects/Configuration/Assets/Date_Objects/calendar_collection_page.resource`
- Suite: `tests/Configuration/Assets/Date_Objects/calendar_collection_iud.robot`
- Playwright: `playwright/ec_iud_calendar_collection.py`; Recon: `investigation/`; Evidence: `evidence/`.

## 6. Dev story + lessons
- 5th/last of 5 Date Objects screens. Recon confirmed custom-URL OV (grid `nav:form:T_data`, no GO) + simplest form -> clean clone of the Calendar bundle (the custom-URL OV exemplar). The Calendar grid-id lesson meant zero surprises here.
- T3 thin (T2 `manage_object`, Refresh fallback); no shared-file edits; full I-U-D. Stacked on CD.0024 (PR #144).
- **Completes the Date Objects folder: 5/5.**
