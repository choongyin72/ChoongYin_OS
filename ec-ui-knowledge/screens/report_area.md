# Screen: Report Area

- **Type:** OV (EC Object Configuration, date-effective) — plain Bank-family (`manage_object_nav`); **simplest OV** (Code/Name/Start Date only)
- **BF_CODE:** RP.0017 · **Treeview:** Reporting > Report Area _(resolved from DB treeview JSON)_
- **DB view:** `OV_REPORT_AREA` (key `CODE`; `NAME`; `OBJECT_START/END_DATE`) — **no Description column**
- **Last verified:** 2026-08-28 · EC 14.2.4 · local sandbox — RF live 5/5 (Bank pattern), DB-verified, self-clean.
  Playwright 7/7 (2026-07-25, legacy stack, unchanged).
- **Pattern:** RF follows the Bank/Berth pattern (`resources/manage_object.resource` T2). Playwright
  driver follows `../EC_OBJECT_CONFIG_IUD.md`, reuses the shared engine (zero engine changes).

## Selectors `[fresh scan 2026-07-25; RF automation section refreshed 2026-08-28 to match PR #468's Bank-pattern rebuild]`
| Purpose | Selector |
|---|---|
| Open | search `Report Area` → `label.tv-link` "Report Area" |
| Grid | `manage_object_nav_nav:form:T_data` — **needs GO (`#button:form:B`) to populate** |
| Insert (+) | hover `span.ui-icon-insert` → "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) — mandatory = yellow
| Row | Field | Kind | Mandatory |
|---|---|---|---|
| R0 | **Report Area Code** | text | ✅ |
| R1 | **Report Area Name** | text | ✅ |
| R2 | **Start date** | date | ✅ — label is lowercase "date" ("Start date"), NOT "Start Date" (capital D); the exact-match label lookup fails with a 30s timeout on the capital-D form (confirmed live, PR #468). |
| R3 | End date | date | — |

### Update tab (`updateAttributes`)
R0 Report Area Code (read-only) · **R1 Report Area Name**. (No Description — update = Name only.)

### Delete (date-close) — `objectdates`
Row R0: Start date C:1, **End date `…R:0:C:3:da_input`** = Start Date → leaves `OV_REPORT_AREA`.

## Automation (code in ec-automation)
- **Playwright (unchanged legacy stack):** driver `py/report_area_iud.py` (shared engine + DbVerify). 7/7 PASS (2026-07-25).
- **RF (current, post PR #468, 2026-08-23 — Batch 9 Bank-pattern conversion):** T3
  `pageobjects/Reporting/report_area_page.resource` + suite `tests/Reporting/report_area_iud.robot`.
  5 TCs (Verify Clean State / Insert / Update / Find / Delete), per-TC Login/Logout on one browser
  opened once in Suite Setup, properties-file-driven insert/update/verify
  (`testdata/report_area_{insert,update,form_verify,grid_verify}.properties`), explicit
  `Find/Clear Report Area Row By Filter` wired into Update/Find/Verify-Found/Delete, fixed test
  code `AUTOTEST_RPTA`. Live 5/5 (update DB-verified via `Field Should Equal In View`). Re-confirmed
  live 5/5 in the 2026-08-28 doc backfill session; full-tree `robot --dryrun tests/` 883/883 pass at
  that time.

## Quirks
- Under top-level **Reporting** menu (not Configuration/Assets) — RF/bundle live in `Reporting/`.
- **Grid needs GO** to load (empty on open — normal for this screen, not a defect).
- No Description column — update covers Name only.
- **Label casing gotcha:** the Start Date field's real label is "Start date" (lowercase "date"),
  not "Start Date" — an exact-match label lookup with the capital-D form times out after 30s.
  Confirmed live during PR #468's Bank-pattern rebuild.
