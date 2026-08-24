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
- **Playwright:** driver `ec-automation/py/disposition_type_iud.py` (thin, on `py/ec_object_iud.py` + `DbVerify.py`). Run: `EC_HEADED=1 py -X utf8 workstreams/master-plan/ec-automation/py/disposition_type_iud.py` → 7/7 PASS. Left UNTOUCHED by the 2026-08-24 RF Bank-pattern conversion below.
- **RF (converted to the full Bank-pattern shape, 2026-08-24):** T3 `pageobjects/Configuration/Assets/Hydrocarbon_Objects/disposition_type_page.resource` + suite
  `tests/Configuration/Assets/Hydrocarbon_Objects/disposition_type_iud.robot` — mirrors `bank_page.resource`/`berth_page.resource` exactly: properties-file-driven insert/update/verify (`testdata/disposition_type_{insert,update,form_verify,grid_verify}.properties`), explicit `Find/Clear Disposition Type Row By Filter` grid-filter wiring, fixed test code `AUTOTEST_DISPOSITION_TYPE` (confirmed free live), per-TC Login/Logout, 5 TCs (added TC04 Find - the prior build only had 4). PURE SCREEN verification (no inline DB-verify calls in the test file/T3 anymore - the prior build's `Field Should Equal In View`/`Disposition Type Should Exist/Not Exist In DB` calls were removed to match Bank's documented convention). Live **5/5 PASS**, full-tree dryrun 793/793, DB self-clean confirmed 0 residual via a fresh oracledb connection, filter keyword confirmed fired 15x (output.xml grep). No shared T1/T2 (`manage_object.resource`/`common.resource`) changes.

## Quirks / difference vs Bank
- Mandatory fields at **R2/R3** (R0/R1 are optional Master System Code/Name) — do NOT assume Bank's R0/R1.
- **Grid needs GO to load** (Bank auto-loads) — the driver clicks GO after open. **Correction (2026-08-24): the navigator has NO mandatory date field** - it's a bare GO button only (`css=[id="button:form:B"]`), confirmed live via the Bank-pattern conversion. A prior classification in `docs/bank-pattern-conversion-checklist.md`'s "Excluded" table wrongly grouped this screen with Document Date Term/Payment Term/Choke/Choke Model as "mandatory single date + GO" - corrected in that doc too.
- Labels are "Disposition Code/Name" (engine resolves by label, so this is handled).
