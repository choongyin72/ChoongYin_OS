# Screen: Port

- **Type:** OV (EC Object Configuration, date-effective) — Bank-family (`manage_object_nav`); plain (optional dropdowns only, none mandatory)
- **BF_CODE:** CO.2003 · **Treeview:** Configuration > Assets > Transport Objects > Port _(DB treeview JSON)_
- **DB view:** `OV_PORT` (key `CODE`; `NAME`, `COUNTRY_CODE`, `CANAL_CODE`, `TIME_ZONE_REGION_CODE`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-07-26 · EC 14.2.4 · local sandbox — `verify_screen.py` OVERALL PASS (RF 4/4 + Playwright 7/7, DB-verified, self-clean)

## Selectors `[fresh scan 2026-07-26]`
| Purpose | Selector |
|---|---|
| Open | search `Port` → `label.tv-link` "Port" |
| Grid | `manage_object_nav_nav:form:T_data` (needs GO to load; **PAGINATED — 2 pages**) |
| Insert (+) | hover `span.ui-icon-insert` → "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) — labels (T3 resolves BY LABEL, not by R:C)
**Port Code*** · **Port Name*** · **Start Date*** (date) · End Date · Comments · Country Name (dd) · Receiver Rate · Max Tanker Size · Canal Restriction Indicator (chk) · Canal (dd) · Time Zone (dd) · Pilot In/Out [hr] · Carrier Alloc Priority (dd). (`*` mandatory; all dropdowns optional)

### Update tab (`updateAttributes`)
`Port Code` (ro) · **`Port Name`** (labels stable across tabs → same as objectForm).

### Delete (date-close) — `objectdates`
**`End Date`** = Start Date → leaves `OV_PORT`.

## Automation (code in ec-automation)
- **Playwright:** `py/port_iud.py` → 7/7 (update Name).
- **RF:** T3 `pageobjects/Configuration/Assets/Transport_Objects/port_page.resource` (**label-driven, NO hardcoded ids**) + suite `tests/.../port_iud.robot` → live 4/4.
- **Gate:** `verify_screen.py` → OVERALL PASS (bundle `VERIFY-REPORT.md`).

## Quirks
- **Paginated grid (2 pages).** A freshly inserted row can render on a later page or only after an async
  redraw — never assert presence on the rendered page alone. Shared engine now handles this for ALL OV
  screens: `row_exists` walks every paginator page (+resets to page 1), `wait_for_row` polls then sweeps all
  pages, `select_row` navigates to the code's page before clicking.
- No mandatory dropdowns — engine fills plain fields as-is.
