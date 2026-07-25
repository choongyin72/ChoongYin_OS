# Screen: Report Area

- **Type:** OV (EC Object Configuration, date-effective) — plain Bank-family (`manage_object_nav`); **simplest OV** (Code/Name/Start Date only)
- **BF_CODE:** RP.0017 · **Treeview:** Reporting > Report Area _(resolved from DB treeview JSON)_
- **DB view:** `OV_REPORT_AREA` (key `CODE`; `NAME`; `OBJECT_START/END_DATE`) — **no Description column**
- **Last verified:** 2026-07-25 · EC 14.2.4 · local sandbox — Playwright 7/7 + RF 4/4, DB-verified, self-clean
- **Pattern:** follows `../EC_OBJECT_CONFIG_IUD.md`. Reuses the shared engine (zero engine changes).

## Selectors `[fresh scan 2026-07-25]`
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
| R2 | **Start date** | date | ✅ |
| R3 | End date | date | — |

### Update tab (`updateAttributes`)
R0 Report Area Code (read-only) · **R1 Report Area Name**. (No Description — update = Name only.)

### Delete (date-close) — `objectdates`
Row R0: Start date C:1, **End date `…R:0:C:3:da_input`** = Start Date → leaves `OV_REPORT_AREA`.

## Automation (code in ec-automation)
- **Playwright:** driver `py/report_area_iud.py` (shared engine + DbVerify). 7/7 PASS.
- **RF:** T3 `pageobjects/Reporting/report_area_page.resource` + suite `tests/Reporting/report_area_iud.robot`. Live 4/4 (update DB-verified via `Field Should Equal In View`).

## Quirks
- Under top-level **Reporting** menu (not Configuration/Assets) — RF/bundle live in `Reporting/`.
- **Grid needs GO** to load (empty on open — normal for this screen, not a defect).
- No Description column — update covers Name only.
