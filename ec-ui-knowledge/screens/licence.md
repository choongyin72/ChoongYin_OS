# Screen: Licence

- **Type:** OV (Manage Object, Bank pattern — plain OV, no navigator)
- **Treeview path:** Configuration > Assets > Commercial Objects > Licence
- **Open via:** menu search / `Open EC Screen` (T1 common.resource)
- **DB view (ground truth):** `OV_LICENCE` (key `CODE`; also `NAME`, `OBJECT_START_DATE`, `OBJECT_END_DATE`)
- **Last verified:** 2026-08-28 · EC **14.2.4** · local sandbox · live RF I-U-D 5/5 DB-verified (re-confirmed during doc backfill; automation itself built/verified in PR #438, 2026-08-23)
- **Pattern:** Bank pattern (`docs/lean-deliverable-backfill-workorder.md`); follows `bank_page.resource`/`country_page.resource`'s label-driven, properties-file-driven, T2-consolidated shape

## Selectors `[from screens/Licence/licence_page.resource Variables section]`

| Purpose | Selector / value |
|---|---|
| Grid (rows) | `manage_object_nav_nav:form:T_data` (shared T2 constant `${OV_MANAGE_OBJECT_TABLE}`, not re-hardcoded) — confirmed live 2026-08-23 via GO-button count = 0/94 elements, nav-free |
| Delete (End Date input) | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (Start Date C:1, End Date label C:2, End Date input C:3 — framework-invariant row layout, same as Bank/State/Country/Account) |
| Insert form labels (mandatory) | `Licence Code`, `Licence Name` (screen-prefixed, NOT the generic "Code"/"Name" Bank/Object List use) |
| Insert-only field | `Start Date` (present in `objectForm`, NOT present in `updateAttributes`) |
| Update form fields | `Licence Code` (read-only), `Licence Name` |
| Grid columns | Licence Code / Licence Name / Start Date / End Date (4 columns, Bank convention) |
| Grid filter | `Find Licence Row By Filter` / `Clear Licence Row Filter` — wraps T2 `Find/Clear Object Row By Filter` against the Code column |

### Field label inventory (live recon, 2026-08-23 — objectForm has 8 labels, updateAttributes has 6)
`Licence Code`, `Licence Name`, `Sort Order`, `Description`, `Master System Code`,
`Master System Name`, `Start Date`/`End Date` (objectdates-only, shown inline on Insert
but NOT part of `updateAttributes`). Only `Licence Code`/`Licence Name` are
MandatoryCellStyle-confirmed mandatory besides `Start Date` (Insert-only).

## Mandatory / yellow fields
`Licence Code`, `Licence Name`, `Start Date` (Insert only). All other fields (Sort Order,
Description, Master System Code, Master System Name) are optional and left blank per the
IUD-fill-only-needed-fields convention.

## Test data (RF suite)
Fixed code `AUTOTEST_LICENCE` (not timestamped — matches Bank/State/Country convention;
confirmed free in `OV_LICENCE` before being wired in) | Name `AUTOTEST Licence` (+`
UPDATED`) | Start=End `2000-01-01`.

## Quirks
- Field labels are screen-prefixed (`Licence Code`/`Licence Name`), unlike Bank/Object
  List's generic `Code`/`Name` — do not assume the generic pair when writing
  `code_label=`/form-label arguments; this screen's keywords pass `code_label=Licence Code`
  explicitly throughout.
- `Start Date` is Insert-only — absent from `updateAttributes` — same as Bank/State/Country;
  TC03/TC04 verification properties correctly omit it.
- Grid-filter wiring (`Find/Clear Licence Row By Filter`) was included from the initial
  2026-08-23 Bank-pattern conversion, not deferred to a later pass.

## Automation (code lives in ec-automation — this file is the MD selector reference)
- **RF (current, primary):** T3 `ec-automation/pageobjects/Configuration/Assets/Commercial_Objects/licence_page.resource`
  + suite `ec-automation/tests/Configuration/Assets/Commercial_Objects/licence_iud.robot`
  (T2 `manage_object.resource` + `libraries/DbVerify.py`). Rebuilt to the Bank pattern in
  PR #438 (2026-08-23). Live 5/5 PASS (re-confirmed 2026-08-28), self-clean 0 residual,
  filter-fired grep = 5.
- **Playwright (history only, not primary):** original 2026-06-12 standalone reference
  `ec-automation/screens/Configuration/Assets/Commercial_Objects/Licence/playwright/ec_iud_licence.py`
  (thin config over `../../Basic_Objects/_shared/iud_engine.py`). Not rebuilt — the
  Universal Screen Engine (`py/engine.py`) is the owner-decided replacement for new
  hand-written Playwright drivers going forward (2026-08-27 decision).
