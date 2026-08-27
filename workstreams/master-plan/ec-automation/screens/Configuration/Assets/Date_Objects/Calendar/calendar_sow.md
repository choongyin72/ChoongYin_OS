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

## 7. PR #451 (2026-08-23, Batch 6, FINAL screen of the 23-screen Bank-pattern conversion pool)
- **What changed:** rebuilt `calendar_page.resource` (T3) and `calendar_iud.robot` (suite) from
  the older hardcoded-field-id pattern above to the label-driven, properties-file-driven,
  T2-consolidated Bank pattern (mirrors `bank_page.resource`/`royalty_owner_page.resource`),
  including explicit grid-filter wiring (`Find/Clear Calendar Row By Filter`) from day one. Added
  the missing TC04 Find (the pattern above only had 4 TCs: clean/insert/update/delete).
- **Ground truth confirmed live, not carried over from the note above:** custom-URL OV (grid
  `nav:form:T_data`, no navigator/GO -- T2's `Save And Refresh List` already auto-falls-back to
  toolbar Refresh) and screen-prefixed field labels "Calendar Code"/"Calendar Name" (NOT the
  generic "Code"/"Name" Bank/Object List use) -- matching Royalty Owner/State's precedent.
  `{mandatory:true}` scan reconfirmed only Calendar Code/Calendar Name/Start Date are mandatory;
  the 7 weekday-indicator checkboxes + Description/Comments stay optional and out of IUD scope,
  unchanged from the prior driver (no scope expansion).
- **New testdata files:** `testdata/calendar_insert.properties`, `calendar_update.properties`,
  `calendar_form_verify.properties`, `calendar_grid_verify.properties`.
- **Credentials:** dedicated `CALENDAR_EC_USER`/`CALENDAR_EC_PASS` pair added additively to
  `resources/credentials.py` (owner standing decision 2026-08-22 -- every EC screen gets its own
  credential pair).
- **DELETE field id:** `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` -- confirmed present
  in the DOM even though the screen has no visible "Object Dates" sub-tab link, same hardcoded
  R:0:C:3 convention as Bank/Royalty Owner.
- **Out of scope (unchanged):** the related "Calendar Usage"/Member Calendars child grid.
- **Verification cited in the PR:** live `EC_HEADLESS=true` run 5/5 PASS (TC01 Verify Clean
  State, TC02 Insert, TC03 Update, TC04 Find, TC05 Delete); fresh-connection DB assertion
  (`SELECT COUNT(*) FROM ov_calendar WHERE code = 'AUTOTEST_CALENDAR'`) = 0 before and after;
  `output.xml` grep on `Find Calendar Row By Filter` = 5 hits; robocop on the 2 changed files = 9
  issues (4 VAR02 + 5 DOC02), matching the established baseline; full-tree `robot --dryrun` =
  750/750 (baseline going in was 749/749).

## 8. This backfill (Batch 8, `docs/lean-deliverable-backfill-workorder.md`, 2026-08-28)
- No RF automation files were changed. Refreshed this SOW, `README.md`, `JOURNAL.md`,
  `CHECKLIST.md`, added a new `evidence/rf_backfill_2026-08-28/` subfolder from a fresh live run,
  and added the missing KB selector map `ec-ui-knowledge/screens/calendar.md`.
- Re-ran the existing suite once: dryrun 5/5 PASS, live headless 5/5 PASS (first attempt, no
  retry). Independent fresh-connection self-clean re-check: 0 residual `AUTOTEST_CALENDAR` rows;
  6 pre-existing `OV_CALENDAR` rows unchanged (matches this SOW's original recon count).
