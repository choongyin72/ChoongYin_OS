# Screen: Berth

- **Type:** OV (EC Object Configuration, date-effective) — Bank-family (`manage_object_nav`); plain (optional dropdowns only, none mandatory)
- **BF_CODE:** CO.2012 · **Treeview:** Configuration > Assets > Transport Objects > Berth _(DB treeview JSON)_
- **DB view:** `OV_BERTH` (key `CODE`; `NAME`, `PORT_CODE`, `BUSINESSUNIT_CODE`, `CAPACITY_UOM`, `OP_*`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-07-26 · EC 14.2.4 · local sandbox — `verify_screen.py` OVERALL PASS (RF 4/4 + Playwright 7/7, DB-verified, self-clean)

## Selectors `[fresh scan 2026-07-26]`
| Purpose | Selector |
|---|---|
| Open | search `Berth` → `label.tv-link` "Berth" |
| Grid | `manage_object_nav_nav:form:T_data` (needs GO to load; **single page**, 11 rows) |
| Insert (+) | hover `span.ui-icon-insert` → "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) — labels (T3 resolves BY LABEL, not by R:C)
**Berth Code*** · **Berth Name*** · **Start Date*** (date) · End Date · Comments · Port Name (dd) · Business Unit (dd) · Reserved Capacity · Design Capacity · Capacity Uom (dd) · Op Production Unit (dd) · Op Area (dd) · Op Facility Class 1 (dd). (`*` mandatory; **all dropdowns optional**, incl Port Name)

### Update tab (`updateAttributes`)
`Berth Code` (ro) · **`Berth Name`** (labels stable across tabs).

### Delete (date-close) — `objectdates`
**`End Date`** = Start Date → leaves `OV_BERTH`.

## Automation (code in ec-automation)
- **Playwright:** `py/berth_iud.py` → 7/7 (update Name).
- **RF:** T3 `pageobjects/Configuration/Assets/Transport_Objects/berth_page.resource` (**label-driven, NO hardcoded ids**) + suite `tests/.../berth_iud.robot` → live 4/4.
- **Gate:** `verify_screen.py` → OVERALL PASS (bundle `VERIFY-REPORT.md`).

## Quirks
- **Folder-sibling of Port (CO.2003) but different:** Berth is **single-page** (Port = 2 pages) and its **Port
  Name dropdown is optional** (Port had no reference dds). Both Port-based predictions were wrong — recon each sibling.
- **Delete needs absence-polling** — grid redraws async after delete+GO. Playwright driver uses engine
  `wait_for_row_absent` (polls until gone from every page); RF's Browser auto-wait already tolerates it.
- No mandatory dropdowns — engine fills plain fields as-is.
