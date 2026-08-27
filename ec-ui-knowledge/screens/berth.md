# Screen: Berth

- **Type:** OV (EC Object Configuration, date-effective) — Bank-family (`manage_object_nav`); plain (optional
  dropdowns only, none mandatory). **One of the two original exemplar screens (with Bank) the whole
  Bank-pattern conversion initiative is named after/modeled on** — referenced as `bank_page.resource`/
  `berth_page.resource` throughout other screens' docs/registry rows.
- **BF_CODE:** CO.2012 · **Treeview:** Configuration > Assets > Transport Objects > Berth _(DB treeview JSON)_
- **DB view:** `OV_BERTH` (key `CODE`; `NAME`, `PORT_CODE`, `BUSINESSUNIT_CODE`, `CAPACITY_UOM`, `OP_*`, `OBJECT_START/END_DATE`); 11 real rows, re-confirmed live 2026-08-28
- **Last verified:** 2026-08-28 · EC 14.2.4 · local sandbox — dryrun 5/5, live headless 5/5, DB self-clean 0
  residual, hygiene PASS (this backfill's re-run; automation itself last CHANGED 2026-08-23, PR #454)

## Selectors `[from screens/Berth/berth_sow.md + berth_page.resource Variables, refreshed 2026-08-28]`
| Purpose | Selector |
|---|---|
| Open | search `Berth` → `label.tv-link` "Berth" |
| Grid | `${OV_MANAGE_OBJECT_TABLE}` = `manage_object_nav_nav:form:T_data` (needs GO to load; **single page**, 11 rows) |
| Insert (+) | hover `span.ui-icon-insert` → "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |
| Delete End Date field | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (`${BERTH_DEL_ENDDATE}`) |
| Grid-filter (added PR #454) | `Find Object Row By Filter`/`Clear Object Row Filter` (shared T2) on the Code column, wrapped as `Find Berth Row By Filter`/`Clear Berth Row Filter` |

### New Object form (`objectForm`) — labels (T3 resolves BY LABEL, not by R:C)
**Berth Code*** · **Berth Name*** · **Start Date*** (date) · End Date · Comments · Port Name (dd) · Business Unit (dd) · Reserved Capacity · Design Capacity · Capacity Uom (dd) · Op Production Unit (dd) · Op Area (dd) · Op Facility Class 1 (dd). (`*` mandatory-and-empty in a pristine Insert row; **all dropdowns optional**, incl Port Name)
- Form-label set actually round-trip-verified by RF (`@{BERTH_FORM_LABELS}`): `Berth Code`, `Berth Name`.

### Update tab (`updateAttributes`)
`Berth Code` (ro) · **`Berth Name`** (labels stable across tabs; Start Date NOT present here, insert-only).

### Delete (date-close) — `objectdates`
**`End Date`** = Start Date → leaves `OV_BERTH`.

## Automation (code in ec-automation)
- **Playwright:** `py/berth_iud.py` → 7/7 (update Name). Predates PR #454, unchanged since 2026-07-26 (owner
  decision 2026-08-27: Playwright driver stays permanently as-is for Bank-/Area-pattern screens; the
  Universal Screen Engine is the forward path, not a new hand-written driver).
- **RF:** T3 `pageobjects/Configuration/Assets/Transport_Objects/berth_page.resource` — rebuilt PR #454
  (2026-08-23) to the full properties-file-driven, T2-consolidated, grid-filter-wired Bank pattern
  (label-driven, NO hardcoded ids). Suite `tests/Configuration/Assets/Transport_Objects/berth_iud.robot` —
  rebuilt to 5 TCs (clean-state/insert/update/find/delete), per-TC Login/Logout, fixed test code
  `AUTOTEST_BERTH`, dedicated `BERTH_EC_USER`/`BERTH_EC_PASS` credentials (`resources/credentials.py`).
  Testdata: `testdata/berth_{insert,update,form_verify,grid_verify}.properties`.
- **Gate (2026-08-28 re-run, this backfill):** dryrun 5/5, live headless 5/5, robocop 9 issues (DOC02/COM04/
  DOC03/MISC06 baseline — same class as Bank's own 13, not new), hygiene PASS, DB self-clean 0 residual.

## Quirks
- **Folder-sibling of Port (CO.2003) but different:** Berth is **single-page** (Port = 2 pages) and its **Port
  Name dropdown is optional** (Port had no reference dds). Both Port-based predictions were wrong — recon each sibling.
- **Delete needs absence-polling** — grid redraws async after delete+GO. Playwright driver uses engine
  `wait_for_row_absent` (polls until gone from every page); RF's Browser auto-wait already tolerates it.
- No mandatory dropdowns — engine fills plain fields as-is.
- **Exemplar-screen blast radius:** because other screens' SOWs/registry rows cite `berth_page.resource`
  directly as a reference pattern (same as `bank_page.resource`), any future change here should be treated
  with Bank-level care — a regression risks looking like "the pattern itself changed," not a one-screen bug.
- **DB access from this sandbox:** the direct hostname `db.plutodev.woodside-pluto.tieto-og.cloud:1521/plutodev`
  timed out for an ad-hoc verification query on 2026-08-28; the repo's own default DSN alias
  `localhost:1521/ORCL` (used by `resources/environment.py`/`libraries/DbVerify.py`) is the one that actually
  reaches the DB from this box and is what the RF suite's in-suite DB checks use.
