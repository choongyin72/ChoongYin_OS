# Screen: Disposition Type

- **Type:** OV (EC Object Configuration, date-effective) — plain Bank-family (`manage_object_nav`), **no mandatory dropdowns**
- **BF_CODE:** CO.0208 · **Treeview:** Configuration > Assets > Hydrocarbon Objects > Disposition Type _(resolved from the DB treeview JSON)_
- **DB view (ground truth):** `OV_DISPOSITION_TYPE` (key `CODE`; also `NAME`, `DESCRIPTION`, `SORT_ORDER`, `PRODUCT_CODE`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-07-25 · EC 14.2.4 · local sandbox — Playwright IUD 7/7 DB-verified, self-clean
- **Pattern:** follows `../EC_OBJECT_CONFIG_IUD.md`. Reuses the shared engine (verified live).

## Selectors `[fresh scan 2026-07-25]`
| Purpose | Selector |
|---|---|
| Open | search `Disposition Type` → `label.tv-link` "Disposition Type" |
| Grid | `manage_object_nav_nav:form:T_data` — **needs GO (`#button:form:B`) to populate** (no default rows on open) |
| Insert (+) | hover `span.ui-icon-insert` → "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

### New Object form (`objectForm`) — mandatory = yellow
| Row | Field | Kind | Mandatory |
|---|---|---|---|
| R0 | Master System Code | text | — |
| R1 | Master System Name | text | — |
| R2 | **Disposition Code** | text | ✅ |
| R3 | **Disposition Name** | text | ✅ |
| R4 | **Start Date** | date | ✅ |
| R5 | End Date | date | — |
| R6 | Sort Order | text | — |
| R7 | Description | text | — |
| R8 | Product | dropdown | — (optional ref) |

### Update tab (`updateAttributes`)
R0 Master System Code · R1 Master System Name · R2 Disposition Code (read-only) · **R3 Disposition Name** · R4 Sort Order · **R5 Description** · R6 Product (dd).

### Delete (date-close) — `objectdates`
Row R0: Start Date C:1, **End Date `…R:0:C:3:da_input`** = Start Date → leaves `OV_DISPOSITION_TYPE`. Toolbar Delete unused (EC Object).

## Automation (code in ec-automation)
- **Playwright:** driver `ec-automation/py/disposition_type_iud.py` (thin, on `py/ec_object_iud.py` + `DbVerify.py`). Run: `EC_HEADED=1 py -X utf8 workstreams/master-plan/ec-automation/py/disposition_type_iud.py` → 7/7 PASS.
- **RF:** T3 `pageobjects/Configuration/Assets/Hydrocarbon_Objects/disposition_type_page.resource` + suite
  `tests/Configuration/Assets/Hydrocarbon_Objects/disposition_type_iud.robot` (reuse T2 `manage_object` + `DbVerify.py`).
  Live **4/4 PASS** — update DB-verified via `Field Should Equal In View` (NAME + DESCRIPTION).

## Quirks / difference vs Bank
- Mandatory fields at **R2/R3** (R0/R1 are optional Master System Code/Name) — do NOT assume Bank's R0/R1.
- **Grid needs GO to load** (Bank auto-loads) — the driver clicks GO after open.
- Labels are "Disposition Code/Name" (engine resolves by label, so this is handled).
