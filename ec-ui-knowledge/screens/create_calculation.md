# Screen: Create Calculation

- **Type:** context-gated TV-STYLE dual grid (header `calculation:form:T_data` + VERSIONS/static params) - calc HEADER IUD only.
- **BF_CODE:** CO.1042 - **Treeview:** Configuration > Assets > Calculation_Objects > Create Calculation
- **DB view:** `OV_CALCULATION` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-07-31 - EC 14.2.4 - local sandbox - `verify_screen.py` OVERALL PASS (RF 4/4 pass + Playwright 8/8, DB-verified, self-clean)

## Selectors
| Purpose | Selector |
|---|---|
| Open | search `Create Calculation` -> `label.tv-link` "Create Calculation" |
| Navigator (gated) | Date + ONE mandatory Calculation Context dd `nav:form:G:1:R:1:C:0:dd` (first-available; 14 contexts) -> GO `#button:form:B` |
| Grid | `calculation:form:T_data` (empty until cascade + GO) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### Insert (TV blank inline row - toolbar Insert 'Public Calculations')
Cells: **C0 Code*** / **C1 Name*** / **C2 Start Date*** (keystrokes+Tab) + **C4 Calculation Period*** / **C5 Calculation Type*** dds (mandatory-YELLOW on the BLANK row only - plain text on saved rows; 'Day'/'Equations'). Silent reject without C4/C5.

### Update / Delete
UPDATE = select row -> VERSIONS grid `calculation_version:form:T:0:C0_in` (authoritative name; header C1 is a mirror). DELETE = select row -> **DELETE CALCULATION** button + YES (physical; NOT End=Start).

## Automation (code in ec-automation)
- **Playwright:** `py/create_calculation_iud.py` (shared engine `ec_object_iud.py` + `apply_ovgm_navigator`).
- **RF:** T3 `pageobjects/Configuration/Assets/Calculation_Objects/create_calculation_page.resource` (**label-driven**) + suite `tests/Configuration/Assets/Calculation_Objects/create_calculation_iud.robot`.
- **Gate:** `verify_screen.py` -> OVERALL PASS.

## Quirks
- Row indices DYNAMIC (insert lands mid-grid) - access rows by C0-value JS scan, never fixed index; TV cells are INPUTS (invisible to text row-scans).
