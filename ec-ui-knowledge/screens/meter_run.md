# Screen: Meter Run

_Note: distinct from "Meter" (`ec-ui-knowledge/screens/meter.md`) - Meter is an OV-GM Area-pattern
navigator screen under Dispatching_Objects; Meter Run is a plain OV Bank-pattern screen with NO
navigator, under Stream_Objects. Do not confuse the two._

- **Type:** OV (EC Object Configuration, date-effective) - plain Bank-pattern (`manage_object_nav`),
  NO navigator cascade; mandatory extras beyond Code/Name/Start Date: Type of Taps, Pipe Material,
  Location of Taps (dropdowns), Pipe Diameter [mm], Diameter Meas Temp [deg R], All Calibration
  Factor. **Rebuilt to the full Bank-pattern shape 2026-08-23 (PR #462, Batch 8)** -
  properties-file-driven insert/update/verify + explicit grid-filter wiring, mirroring
  `bank_page.resource`/`berth_page.resource`.
- **BF_CODE:** CO.0091 - **Treeview:** Configuration > Assets > Stream_Objects > Meter Run _(DB treeview JSON)_
- **DB view:** `OV_METER_RUN` (versioned, key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-08-28 - EC 14.2.4 - local sandbox - live RF 5/5, dryrun 5/5, robocop 9
  issues (parity with `berth_iud.robot` baseline), hygiene PASS, DB self-clean 0 residual via a
  fresh oracledb connection (backfill re-run; see
  `workstreams/master-plan/ec-automation/screens/Configuration/Assets/Stream_Objects/Meter_Run/evidence/2026-08-28_backfill/`).

## Selectors `[from meter_run_page.resource Variables section, 2026-08-23/28]`
| Purpose | Selector |
|---|---|
| Open | search `Meter Run` -> `label.tv-link` "Meter Run" |
| Grid | `manage_object_nav_nav:form:T_data` (reused as T2's `${OV_MANAGE_OBJECT_TABLE}`; needs GO to load) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" (generic T1 gesture) |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |
| Grid filter | `Find/Clear Meter Run Row By Filter` (T3 wrapper around T2's `Find/Clear Object Row By Filter`, filters the Code column) - 15 hits confirmed via output.xml grep on both the PR #462 run and this backfill's re-run |
| Delete (End Date) | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (hardcoded, `${METER_RUN_DEL_ENDDATE}`; End Date = Start Date = true delete in `OV_METER_RUN`) - confirmed live via read-only recon on an existing production row (never saved) |

### New Object form (`objectForm`) - labels, screen-prefixed (T3 resolves BY LABEL via
`Insert Object From Properties And Verify Code`, driven by `testdata/meter_run_insert.properties`)
**Meter Run Code*** - **Meter Run Name*** - **Start Date*** (date, Insert-only) - **Type of
Taps*** (dropdown) - **Pipe Material*** (dropdown) - **Location of Taps*** (dropdown) -
**Pipe Diameter (temp uncorrected) [mm]*** - **Diameter Meas Temp [deg R]*** - **All Calibration
Factor***. (`*` mandatory, confirmed live - Save rejected without them; a LARGER mandatory set
than Bank/Berth's plain 3-field Code/Name/Start Date - do not extrapolate the simpler siblings'
shape onto this screen.)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Meter Run Code` (read-only in updateAttributes) - **`Meter Run Name`** (the only field exercised
by TC03, driven by `testdata/meter_run_update.properties`). Delete: **`End Date`** = Start Date ->
true delete, leaves `OV_METER_RUN`.

## Automation (code in ec-automation)
- **RF:** T3 `pageobjects/Configuration/Assets/Stream_Objects/meter_run_page.resource`
  (properties-file-driven, T2-consolidated, explicit grid-filter, per-screen credential pair
  `METER_RUN_EC_USER`/`METER_RUN_EC_PASS`) + suite `tests/Configuration/Assets/Stream_Objects/meter_run_iud.robot`
  (5 TCs: Verify Clean State / Insert / Update / Find / Delete, per-TC Login/Logout) -> live 5/5.
- **Testdata:** `testdata/meter_run_insert.properties`, `meter_run_update.properties`,
  `meter_run_form_verify.properties`, `meter_run_grid_verify.properties`.
- **Playwright:** `py/meter_run_iud.py` (built 2026-07-26, 7/7 live) - kept as historical/
  unmaintained; the Universal Screen Engine (`py/engine.py`) is the owner-decided replacement for
  hand-written Playwright drivers going forward (Section H, `docs/IUD-DELIVERABLE-CHECKLIST.md`);
  no new Playwright work was done for the 2026-08-23 conversion or this backfill.
- **Gate:** robocop 9 issues (parity with `berth_iud.robot` baseline, not a regression), hygiene
  PASS, DB self-clean 0 residual via a fresh connection.

## Quirks
- Fixed test code `AUTOTEST_METER_RUN` (not generated/timestamped) - matches Bank/Berth's
  convention; every run must complete TC05 (delete) so the code stays free for the next run.
- Mandatory field set is unusually large for a plain OV screen (6 extras beyond Code/Name/Start
  Date) - taken as-is from the already-proven driver/page object, not extrapolated from a
  simpler-looking sibling.
- Do NOT confuse with "Meter" (`meter.md`) - similar name, different screen, different pattern
  (Area/OV-GM vs Bank/OV-plain), different treeview folder (Dispatching_Objects vs
  Stream_Objects).
