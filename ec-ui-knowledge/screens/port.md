# Screen: Port

- **Type:** OV (EC Object Configuration, date-effective) — Bank-family (`manage_object_nav`); plain (optional dropdowns only, none mandatory)
- **BF_CODE:** CO.2003 · **Treeview:** Configuration > Assets > Transport Objects > Port _(DB treeview JSON)_
- **DB view:** `OV_PORT` (key `CODE`; `NAME`, `COUNTRY_CODE`, `CANAL_CODE`, `TIME_ZONE_REGION_CODE`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-08-28 · EC 14.2.4 · local sandbox — direct robocop/dryrun/live/hygiene/DB
  self-clean re-run (see `screens/Configuration/Assets/Transport_Objects/Port/CHECKLIST.md`); RF
  shape itself last CHANGED 2026-08-23 (PR #465, Batch 9 Bank-pattern conversion)

## Selectors `[fresh scan 2026-08-28, confirms PR #465's 2026-08-23 shape still live]`
| Purpose | Selector |
|---|---|
| Open | search `Port` → `label.tv-link` "Port" |
| Grid | `${OV_MANAGE_OBJECT_TABLE}` (= `manage_object_nav_nav:form:T_data`; needs GO to load; **PAGINATED — 2 pages**, shared T2 filter/row-locate keywords walk all pages) |
| Insert (+) | hover `span.ui-icon-insert` → "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |
| Grid filter | `Find Port Row By Filter <code>` / `Clear Port Row Filter` (T3, delegates to shared T2 `Find/Clear Object Row By Filter`) |

### New Object form (`objectForm`) — labels (T3 resolves BY LABEL, not by R:C)
**Port Code*** · **Port Name*** · **Start Date*** (date) · End Date · Comments · Country Name (dd) · Receiver Rate · Max Tanker Size · Canal Restriction Indicator (chk) · Canal (dd) · Time Zone (dd) · Pilot In/Out [hr] · Carrier Alloc Priority (dd). (`*` mandatory; all dropdowns optional)

### Update tab (`updateAttributes`)
`Port Code` (ro) · **`Port Name`** (labels stable across tabs → same as objectForm).

### Delete (date-close) — `objectdates`
**`End Date`** = Start Date → leaves `OV_PORT`.

## Automation (code in ec-automation)
- **RF:** T3 `pageobjects/Configuration/Assets/Transport_Objects/port_page.resource` — **label-driven,
  properties-file-driven, grid-filter-wired** (rebuilt 2026-08-23, PR #465, to mirror
  `bank_page.resource`/`berth_page.resource` exactly) + suite
  `tests/Configuration/Assets/Transport_Objects/port_iud.robot` → **5 TCs** (Verify Clean State/
  Insert/Update/Find/Delete), per-TC login/logout on one browser opened once in Suite Setup, fixed
  test code `AUTOTEST_PORT`, dedicated `PORT_EC_USER`/`PORT_EC_PASS` credentials → live 5/5 (both at
  #465's merge and re-confirmed live 2026-08-28).
- **Testdata:** `testdata/port_{insert,update,form_verify,grid_verify}.properties`.
- **Playwright (unchanged since 2026-07-26, out of scope for Bank-pattern conversions going
  forward):** `py/port_iud.py` → 7/7 (update Name).
- **Gate (historical, 2026-07-26, predates the Batch-9 conversion):** `verify_screen.py` → OVERALL
  PASS (bundle `VERIFY-REPORT.md`). The current shape's gates (robocop/dryrun/live/hygiene/DB
  self-clean) are re-run and cited directly in the bundle's `CHECKLIST.md`/`README.md` instead.

## Quirks
- **Paginated grid (2 pages).** A freshly inserted row can render on a later page or only after an async
  redraw — never assert presence on the rendered page alone. Shared engine/T2 keywords handle this for
  ALL OV screens: the RF T2 filter/row-locate keywords and the Playwright engine's `row_exists`/
  `wait_for_row`/`select_row` all walk every paginator page.
- **Explicit grid-filter wiring** (added PR #465, 2026-08-23): `Find Port Row By Filter`/`Clear Port
  Row Filter` fire before/after every grid-dependent step (Update/Find/Verify-Found/Delete) — 15
  `Find Port Row By Filter` hits confirmed via `output.xml` grep, both at #465's merge and again on
  this KB entry's 2026-08-28 re-scan (same count, no regression).
- No mandatory dropdowns — engine/T2 fills plain fields as-is.
