# Screen: Country

- **Type:** OV (EC Object Configuration, date-effective), **plain manage-object — no navigator
  dropdown/date**, Bank pattern (not Area's OV-GM shape)
- **Treeview path:** Configuration > Assets > Basic Objects > Country
- **Open via:** `Open EC Screen  Country` (shared T1) / menu search on "Country"
- **DB view (ground truth):** `OV_COUNTRY` (key `CODE`; also `NAME`)
- **Last verified:** 2026-08-28 · EC **14.2.4** · local sandbox · live RF I-U-D 5/5 (re-confirmed
  from PR #428's original 2026-08-23 conversion; no automation changed since)
- **Pattern:** Bank pattern (label-driven, properties-file-driven, T2-consolidated) — mirrors
  `bank_page.resource`/`berth_page.resource`; converted from an older hardcoded-field-id pattern
  in PR #428 (Batch 2 of 5: Country/County/Regulatory Permits/Currency/VAT Code)

## Selectors `[from country_page.resource Variables section, 2026-08-23/2026-08-28]`

| Purpose | Selector / value |
|---|---|
| Grid (rows) | `${COUNTRY_TABLE}` = `${OV_MANAGE_OBJECT_TABLE}` = `manage_object_nav_nav:form:T_data` (shared T2 constant, not re-hardcoded) |
| Find grid row | `Find Country Row By Filter    ${code}` -> shared T2 `Find Object Row By Filter` (explicit filter wiring, not the implicit 3s-timeout fallback) |
| Clear grid filter | `Clear Country Row Filter` -> shared T2 `Clear Object Row Filter` |
| Insert | `Insert Country Record And Save` -> T2 `Insert Object From Properties And Verify Code` (properties: `testdata/country_insert.properties`) |
| Update | `Update Country Record And Save` -> T2 `Update Object From Properties` (properties: `testdata/country_update.properties`) |
| Delete (End Date field) | `${COUNTRY_DEL_ENDDATE}` = `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (reused unmodified from Bank/State/Account's row layout: Start Date C:1, End Date label C:2, End Date input C:3) |
| Login | `Login To EC Application` -> T1 `Login To EC Screen` with `${COUNTRY_EC_USER}`/`${COUNTRY_EC_PASS}` (dedicated per-screen credential pair, `resources/credentials.py`) |

## Mandatory-yellow fields (confirmed live 2026-08-23 via field-label recon, MandatoryCellStyle scan)
- **Insert (`objectForm`, 14 ECCell labels total):** Country Code*, Country Name*, Start Date*
  (only these 3 are mandatory).
- **Update (`updateAttributes`, 10 ECCell labels total):** Country Code (read-only guard), Country
  Name* (only Code/Name present at all; Start/End Date live only in Insert's inline view /
  `objectdates`, not in `updateAttributes`).
- Optional and deliberately omitted: Master System Code, Master System Name, Local Name, End Date
  (Insert-only), Dialing Code, Comments, Description, Nationality name.
- `@{COUNTRY_FORM_LABELS}` in the T3 = `Country Code    Country Name` (mandatory pair only, per
  the IUD-fill-only-needed-fields convention).

## Field-label quirk
Country uses **screen-prefixed** labels ("Country Code"/"Country Name"), NOT the generic
"Code"/"Name" that Bank/Object List/Currency use — confirmed live, do not assume the generic
labels apply here just because the screen looks Bank-shaped.

## Grid columns (confirmed live)
Country Code, Country Name, Start Date, End Date.

## Quirks
- No mandatory navigator dropdown/date before GO — plain manage-object OV (unlike Area-shaped
  screens with a mandatory Area cascade).
- Fixed test code `AUTOTEST_COUNTRY` (not a per-run timestamp) — every run must complete TC05
  (delete) so the code stays free for the next run; EC never lets a deleted code be reused if
  cleanup is skipped.
- DELETE = End Date = Start Date (zero-length window) -> true delete, row leaves `OV_COUNTRY`.

## Automation (code lives in ec-automation — this file is the MD selector reference)
- **RF (maintained):** T3 `workstreams/master-plan/ec-automation/pageobjects/Configuration/Assets/Basic_Objects/country_page.resource`
  + suite `workstreams/master-plan/ec-automation/tests/Configuration/Assets/Basic_Objects/country_iud.robot`
  (T2 `resources/manage_object.resource` + T1 `resources/common.resource` + `libraries/DbVerify.py`).
  Live 5/5 PASS (2026-08-23 PR #428; re-confirmed 2026-08-28). Grid-filter wiring confirmed firing
  live: 5 `Find Country Row By Filter` hits in `output.xml`.
- **Playwright (superseded reference, not maintained):**
  `workstreams/master-plan/ec-automation/screens/Configuration/Assets/Basic_Objects/Country/playwright/ec_iud_country.py`
  — pre-conversion (2026-06-11), kept for history only per Section H of the deliverable
  checklist (Universal Screen Engine is the owner-decided replacement going forward).
