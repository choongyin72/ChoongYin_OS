# Screen: Tank

- **Type:** OV-GM (EC Object Configuration, date-effective) - manage-object groupmodel;
  Production Unit -> Area -> Facility Class 1 navigator cascade (same shape as Well/Area).
- **Treeview:** Configuration > Assets > Tank and Storage Objects > Tank (confirmed live
  2026-08-26 via treeview expand - direct sibling of Storage/Manage Tank/Maintain Tanks there).
- **DB view:** `OV_TANK` (versioned) - generic `CODE` column, per `libraries/DbVerify.py`.
- **Distinct from Chemical Tank** - a DIFFERENT sibling screen with its own `OV_CHEM_TANK` view,
  `chemical_tank_page.resource`, and `chemical_tank_iud.robot`. Do not confuse the two when
  searching by "tank" (`grep -ril "tank_page.resource"` must exclude any `chemical` match to find
  THIS screen's files).
- **Last verified:** 2026-08-27 - EC 14.2.4 - local sandbox - RF dryrun 5/5 PASS + live headless
  5/5 PASS (TC01-TC05), fresh-connection DB self-clean 0 residual, `check_bundle_hygiene.py` PASS
  (backfill re-run of PR #553's brand-new Area-pattern build, merged 2026-08-26).

## Selectors
| Purpose | Selector |
|---|---|
| Grid | `manageObject:form:T_data` (empty until the 3-level nav cascade + GO) |
| Nav Date (C:0, optional) | `nav:form:G:0:R:1:C:0:da_input` - working default, left untouched |
| Nav Op Production Unit (C:1, dd) | `nav:form:G:0:R:1:C:1:dd` |
| Nav Op Area (C:2, dd) | `nav:form:G:0:R:1:C:2:dd` |
| Nav Op Facility Class 1 (C:3, dd) | `nav:form:G:0:R:1:C:3:dd` |
| GO | `button:form:B` |
| Delete (End Date field) | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (hardcoded, not
  label-driven - same framework-invariant layout as Area/Bank) |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Tank Code*** - **Tank Name*** - Start Date* (date) - **Tank Meter Freq.*** (dropdown, filled
`__FIRST__`) - **Use in BF*** (dropdown, filled `__FIRST__`) - Op Production Unit / Op Area / Op
Facility Class 1 (dropdowns, NOT mandatory but must equal the nav scope or the new row is
invisible under this OV-GM navigator scope - confirmed live via a self-cleaning probe
insert/delete, `AUTOTEST_TANK_RECON`). Labels are SCREEN-PREFIXED ("Tank Code"/"Tank Name"), like
Area's "Area Code"/"Area Name" - NOT the generic "Code"/"Name" Bank/Object List use. (`*`
mandatory, confirmed via the pristine New-Object row's yellow-background cue)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Tank Code` (ro, guard) - **`Tank Name`** (only field edited; Start Date lives only in
`objectdates`, not `updateAttributes`, same pattern as Bank/Area/Storage Flow). Delete:
**`End Date`** = Start Date (zero-length window) -> true delete, row leaves `OV_TANK`.

### Grid columns (confirmed live, `manageObject:form:T` scan)
Tank Code / Tank Name / Start Date / End Date.

## Navigator values (this environment)
Op Production Unit = `P1 Production Unit`, Op Area = `P1 Area`, Op Facility Class 1 =
`P1 Facility 1` - same P1 taxonomy Well already uses - driven by
`testdata/tank_navigator.properties` via the shared T2 `Apply Navigator From Properties` keyword.

## Automation (code in ec-automation)
- **RF (the ONLY test for this screen — no historical Playwright reference exists, unlike
  converted siblings):** T3 `pageobjects/Configuration/Assets/Tank_and_Storage_Objects/
  tank_page.resource` (built directly to Area-pattern shape, PR #553, 2026-08-26) + suite
  `tests/Configuration/Assets/Tank_and_Storage_Objects/tank_iud.robot` (5 TC: Clean State /
  Insert / Update / Find / Delete, per-TC login/logout, fixed test code `AUTOTEST_TANK`).
- **Playwright:** N/A, permanently waived (owner decision 2026-08-27, Universal Screen Engine
  replaces this role) - Tank never had a Playwright driver.
- **Test data:** `testdata/tank_{navigator,insert,update,form_verify,grid_verify}.properties`.
- **Credentials:** dedicated pair `TANK_EC_USER`/`TANK_EC_PASS` in `resources/credentials.py`.
- **Recon:** `screens/Configuration/Assets/Tank_and_Storage_Objects/Tank/investigation/
  {recon.py,dbcheck_selfclean.py}` (PR #553, consolidated live-recon evidence).

## Quirks
- OV-GM navigator-gated: grid empty until the 3-level Production Unit -> Area -> Facility Class 1
  cascade + GO completes. The leading Date column (C:0) has a working default and is NOT part of
  the fill - `Apply Navigator From Properties` only ever fills C:1..C:N.
- Op Production Unit/Op Area/Op Facility Class 1 (insert form fields) MUST equal the nav scope or
  the inserted row is invisible under the filtered navigator scope - same convention as every
  other OV-GM screen converted/built in this batch (Area, Storage, Contract Area).
- OV-GM grids redraw lazily after Save+GO - the T3 keywords wait for the row to render before the
  first assertion (same lesson as every other OV-GM screen).
- **Distinct from Chemical Tank** (`OV_CHEM_TANK`, `chemical_tank_page.resource`) and from Storage
  / Storage Flow / `daily_tank_status_vcf` - all unrelated siblings under the same "Tank and
  Storage Objects" treeview branch. Confirm the right file via `grep -ril "tank_page.resource"`
  excluding any `chemical` match.
- DB self-clean checks against `OV_TANK` must use the generic `CODE` column, not a screen-specific
  `TANK_CODE` column.
- **Environment note (2026-08-27 backfill):** a real live-run flake was hit and resolved during
  this backfill's evidence capture - an accumulating pile of stray `chrome-headless-shell.exe`/
  `node.exe`/`robot.exe` processes (left behind by earlier failed attempts) caused 4 consecutive
  live-run failures with page/connection errors before a full `taskkill` sweep let the suite pass
  5/5 cleanly. Not a Tank suite defect - see
  `screens/Configuration/Assets/Tank_and_Storage_Objects/Tank/JOURNAL.md` for the full account.
