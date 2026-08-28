# Screen: Calendar

- **Type:** OV (EC Object Configuration, date-effective), **custom-URL variant**
- **BF code:** CD.0024
- **Treeview path:** Configuration > Assets > Date Objects > Calendar
- **DB view (ground truth):** `OV_CALENDAR` (base `CALENDAR`/`CALENDAR_VERSION`; 6 rows at recon)
- **Last verified:** 2026-08-28 (this backfill's live re-run) · EC **14.2.4** · local sandbox ·
  live I-U-D 5/5 DB-verified · automation itself built/confirmed live 2026-08-23 (PR #451, Batch
  6 Bank-pattern conversion, final of the 23-screen conversion pool)
- **Pattern:** Bank pattern (label-driven, properties-file-driven, T2-consolidated) — mirrors
  `bank_page.resource`/`royalty_owner_page.resource`. NOT the OV-GM/navigator shape.

## Selectors `[from calendar_page.resource Variables section, PR #451]`

| Purpose | Selector |
|---|---|
| Grid (rows) | `nav:form:T_data` -- **custom-URL OV**, NOT the standard `manage_object_nav_nav:form:T_data` |
| Navigator / GO | **none** -- no navigator, no GO button. Reload via toolbar Refresh; T2's `Save And Refresh List` auto-falls-back to Refresh Screen when no GO exists |
| Grid-filter keywords | `Find Calendar Row By Filter` / `Clear Calendar Row Filter` (wraps T2 `Find/Clear Object Row By Filter`, explicit from day one) |
| Delete field id (objectdates) | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` -- present in the DOM even though the screen has no visible "Object Dates" sub-tab link; same hardcoded R:0:C:3 convention as Bank/Royalty Owner |
| Form labels (screen-prefixed) | `Calendar Code`, `Calendar Name` -- NOT the generic "Code"/"Name" Bank/Object List use; matches Royalty Owner/State's precedent |

### New Object form (`objectForm`)
Mandatory = `{mandatory:true}` CSS scan confirmed live 2026-08-23: **Calendar Code, Calendar
Name, Start Date** only. Optional (left at default, out of IUD scope, unchanged from the prior
driver): Description, Comments, and the 7 weekday-indicator checkboxes (Business day -
Monday..Sunday).

### Update tab (`updateAttributes`)
Starts at Calendar Code (read-only) / Calendar Name / Description / Comments / 7 weekday
indicators. **No Start Date / End Date here** -- those live only in `objectdates`.

### Delete (date-close) -- `objectdates`
**EC Object delete = set End Date = Start Date -> Save** (row leaves `OV_CALENDAR`). No GO/toolbar
Delete used.

## Quirks
- Custom-URL OV: no navigator/GO at all -- confirmed twice independently: original build's live
  failure (assumed `manage_object_nav_nav:form:T_data`, got a silent UI-read miss even though the
  insert had persisted) and PR #451's fresh field-inventory scan.
- Screen-prefixed labels ("Calendar Code"/"Calendar Name") rather than generic "Code"/"Name" --
  do not assume Bank's exact label text carries over; confirm live per screen (Royalty Owner/
  State share this convention).
- Related "Calendar Usage"/Member Calendars child grid is a SEPARATE object, out of scope for
  this IUD flow (not a parent-child relationship at the object level).
- Test code: fixed `AUTOTEST_CALENDAR` (not a generated-unique code) -- every run must complete
  TC05 (delete) to free the code for the next run.

## Automation (code lives in ec-automation -- this file is the MD selector reference)
- **RF:** T3 `ec-automation/pageobjects/Configuration/Assets/Date_Objects/calendar_page.resource`
  + suite `ec-automation/tests/Configuration/Assets/Date_Objects/calendar_iud.robot` (T2
  `manage_object.resource` + `DbVerify.py`). 5 TCs: Verify Clean State / Insert / Update / Find /
  Delete. Validated live 5/5 (2026-08-23 at build, re-confirmed 2026-08-28 at this backfill).
  Dedicated credentials `CALENDAR_EC_USER`/`CALENDAR_EC_PASS` in `resources/credentials.py`.
  Testdata: `testdata/calendar_{insert,update,form_verify,grid_verify}.properties`.
- **Playwright:** ORIGINAL per-screen driver `ec-automation/screens/Configuration/Assets/
  Date_Objects/Calendar/playwright/ec_iud_calendar.py`, predates PR #451; left as historical
  reference. No new Playwright bundle built for the Bank-pattern conversion (Universal Screen
  Engine is the owner-decided replacement going forward).
