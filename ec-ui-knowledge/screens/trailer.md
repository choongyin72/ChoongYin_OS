# Screen: Trailer

- **Type:** Plain OV (EC Object Configuration, date-effective) - Bank family; date-only navigator + GO.
  No mandatory navigator scope (date-only GO; the grid loads without any prerequisite dropdown).
- **BF_CODE:** CO.0265 - **Treeview:** Configuration > Assets > Transport_Objects > Trailer
- **DB view:** `OV_TRAILER` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-08-28 - EC 14.2.4 - local sandbox - live RF suite 5/5 pass (this backfill
  session), robocop 9 issues (4 VAR02 + 5 DOC02, advisory-only parity with Berth), DB self-clean
  0 residual `AUTOTEST%` rows in `OV_TRAILER` (fresh connection).

## Selectors (transcribed from `trailer_page.resource`'s Variables section, PR #475, 2026-08-23)
| Purpose | Selector |
|---|---|
| Open | search `Trailer` -> `label.tv-link` "Trailer" |
| Navigator | date field -> GO via shared `Apply Navigator` (date-only, no cascade) |
| Grid (**custom, screen-owned**) | `trailer_object:form:T_data` - Trailer's OWN grid id, NOT the shared `manage_object_nav_nav:form:T_data` constant most manage-object screens use (confirmed via the proven Playwright driver's `GRID_DATA_ID`, kept unchanged through the Bank-pattern conversion) |
| Delete End Date field | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |
| Grid filter | `Find/Clear Trailer Row By Filter` (T3 wrappers) -> shared T2 `Find/Clear Object Row By Filter`, wired into Update/Find/Verify-Found/Delete (matches Account/Bank/Berth/State convention) |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Trailer Code*** - **Trailer Name*** - **Start Date*** (date) + dropdowns **Trailer Type**, **UOM**,
**Transport Company** (first-available). (`*` mandatory; dropdowns are de-facto mandatory too -
Save fails without them even though not CSS-flagged, per the proven driver's field set.)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Trailer Code` (ro) - **`Trailer Name`**. Start Date is Insert-only, not present in
`updateAttributes`. Delete: **`End Date`** = Start Date -> leaves `OV_TRAILER` (true delete).
Round-trip form-compare (TC02/TC04) uses ONLY `Trailer Code`/`Trailer Name` - the Trailer Type/UOM/
Transport Company dropdowns are excluded (can re-render Description text instead of code after
reload, not a stable live-DOM comparison target).

## Automation (code in ec-automation)
- **RF (current, maintained):** T3 `pageobjects/Configuration/Assets/Transport_Objects/trailer_page.resource`
  (properties-file-driven, label-driven, delegates to shared T2 `resources/manage_object.resource`)
  + suite `tests/Configuration/Assets/Transport_Objects/trailer_iud.robot` (5 TCs: Clean State /
  Insert / Update / Find / Delete, per-TC Login/Logout, fixed test code `AUTOTEST_TRAILER`).
  Rebuilt 2026-08-23 (PR #475, Batch 10) from a label-driven-but-hardcoded-arguments shape to the
  full Bank-pattern shape.
- **Test data:** `testdata/trailer_{insert,update,form_verify,grid_verify}.properties`.
- **Credentials:** `resources/credentials.py` - `TRAILER_EC_USER`/`TRAILER_EC_PASS` (dedicated pair).
- **Playwright (historical reference only, permanently waived for new work):** `py/trailer_iud.py`
  (shared engine `ec_object_iud.py` + `click_go`), from the original 2026-07-31 build. Not touched
  since; Universal Screen Engine replaces this role for new Bank-/Area-pattern work per
  `docs/IUD-DELIVERABLE-CHECKLIST.md` Section H (2026-08-27).

## Quirks
- Plain OV (Bank family): the navigator is a single DATE field + GO - no cascade, and no Op
  Production Unit to satisfy.
- **Custom grid id** `trailer_object:form:T_data` - Trailer's OWN, NOT the shared
  `manage_object_nav_nav:form:T_data` constant other Bank-family screens (Bank, Berth, etc.) use.
  A real, documented quirk - do not assume it matches the shared constant on a future edit.
- Licence Plate No (text) + Trailer Type/UOM/Transport Company (dropdowns, first-available) are
  de-facto mandatory for Save even though not all are CSS-flagged - carried unchanged through the
  PR #475 conversion, trusted from the proven driver rather than a static label/CSS re-scan.
- An UNSAVED CHANGES dialog (YES/NO) can block GO right after the End=Start close - answer YES
  (that commits the intended delete).

_KB map refreshed 2026-08-28 under `docs/lean-deliverable-backfill-workorder.md` (Batch 11) to
reflect the PR #475 Bank-pattern conversion (2026-08-23) - the prior 2026-07-31 version described
the screen's pre-conversion T3 shape. No automation file was touched to produce this refresh._
