# Screen: Storage

- **Type:** OV-GM (EC Object Configuration, date-effective) — manage-object groupmodel;
  navigator-GATED, genuine 3-level same-row cascade (same shape as Area/Tank/Facility Class 1).
- **BF_CODE:** CO.0034 — **Treeview:** Configuration > Assets > Tank_and_Storage_Objects > Storage
- **DB view:** `OV_STORAGE` (versioned; key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-08-28 — EC 14.2.4 — local sandbox — RF dryrun 5/5 PASS + live headless
  5/5 PASS on retry (first attempt 4/5, TC05 grid-redraw timing flake — see
  `screens/Configuration/Assets/Tank_and_Storage_Objects/Storage/JOURNAL.md`), fresh-connection
  DB self-clean 0 residual `AUTOTEST%` rows, `check_bundle_hygiene.py` PASS (backfill re-run of
  PR #537's Area-pattern conversion, merged 2026-08-26).

## Selectors
| Purpose | Selector |
|---|---|
| Grid | `manageObject:form:T_data` (empty until the 3-level nav cascade + GO) |
| Nav Op Production Unit (C:1, dd) | `nav:form:G:0:R:1:C:1:dd` |
| Nav Op Area (C:2, dd) | `nav:form:G:0:R:1:C:2:dd` |
| Nav Op Facility Class 1 (C:3, dd) | `nav:form:G:0:R:1:C:3:dd` |
| GO | `button:form:B` |
| Delete (End Date field) | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (hardcoded,
  not label-driven — same documented framework-invariant layout as Area/Tank/Bank; the row packs
  Start Date at C:1 and End Date at C:3 with the End Date label at C:2, a shape the
  one-field-per-row label scan cannot safely resolve) |

### New Object form (`objectForm`) — labels (T3 resolves BY LABEL)
**Storage Code*** — **Storage Name*** — **Start Date*** (date) + dropdowns **Storage Type***,
**Product Name*** (Storage's own genuine mandatory dropdowns, filled `__FIRST__`). Op Production
Unit / Op Area / Op Facility Class 1 also exist on this objectForm but are left blank on insert —
the proven driver inserts successfully without them (trust proven behaviour, don't hunt for an
unstated requirement). Labels are SCREEN-PREFIXED ("Storage Code"/"Storage Name"), like Area's
"Area Code"/"Area Name" — NOT the generic "Code"/"Name" Bank/Object List use. (`*` mandatory,
confirmed via the pristine New-Object row's yellow-background cue)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Storage Code` (ro, guard) — **`Storage Name`** (only field edited; Start Date lives only in
`objectdates`, not `updateAttributes`, same pattern as Bank/Area/Tank). Delete: **`End Date`** =
Start Date (zero-length window) → true delete, row leaves `OV_STORAGE`.

### Grid columns (confirmed live, `manageObject:form:T_head` scan)
Storage Code / Storage Name / Start Date / End Date — same 4-column shape as Area/Tank/Facility
Class 1.

## Navigator values (this environment)
Op Production Unit = `AS1 EC Exploration Norway`, Op Area = `AS1_Area`, Op Facility Class 1 =
`AS1_Facility_01` — driven by `testdata/storage_navigator.properties` via the shared T2
`Apply Navigator From Properties` keyword (confirmed live via `tmp/recon_storage_navigator_
cascade.py`, gitignored, at PR #537; these are the same values the prior "Apply OV-GM Navigator
First Available" mechanism already picked, now captured explicitly).

## Automation (code in ec-automation)
- **RF (current, since PR #537, 2026-08-26):** T3 `pageobjects/Configuration/Assets/
  Tank_and_Storage_Objects/storage_page.resource` (Area-pattern shape: friendly-narrative
  wrappers around the shared T2, explicit `Find/Clear Storage Row By Filter` grid-filter wiring)
  + suite `tests/Configuration/Assets/Tank_and_Storage_Objects/storage_iud.robot` (5 TCs: Verify
  Clean State / Insert / Update / Find / Delete, per-TC Login/Logout on one Suite-Setup-opened
  browser, fixed test code `AUTOTEST_STG`).
- **Playwright:** `py/storage_iud.py` (2026-07-30 build, shared engine `ec_object_iud.py` +
  `apply_ovgm_navigator`) — **permanently waived going forward** (owner decision 2026-08-27, the
  Universal Screen Engine replaces this role); not rebuilt or re-verified by the PR #537
  conversion or this backfill.
- **Test data:** `testdata/storage_{navigator,insert,update,form_verify,grid_verify}.properties`.
- **Credentials:** dedicated pair `STORAGE_EC_USER`/`STORAGE_EC_PASS` in `resources/credentials.py`.
- **Bundle:** `screens/Configuration/Assets/Tank_and_Storage_Objects/Storage/` (SOW, README,
  JOURNAL, evidence, CHECKLIST — refreshed 2026-08-28 backfill per
  `docs/lean-deliverable-backfill-workorder.md` Batch 4).

## Quirks
- OV-GM navigator-gated: grid empty until the 3-level cascade + GO completes. The versioned
  groupmodel grid can redraw lazily right after a delete — a one-off live-run TC05 grid
  assertion flake (2026-08-28 backfill re-run) resolved on a single retry with 0 real DB
  residual confirmed throughout; not a code defect (see JOURNAL.md).
- Distinct from **Tank** (`OV_TANK`, `tank_page.resource`) — a sibling screen in the same
  Tank_and_Storage_Objects menu group with its own view/automation; do not confuse the two when
  grepping by a generic term.
