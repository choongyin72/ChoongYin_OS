# Screen: Collection Point

- **Type:** OV-GM (EC Object Configuration, groupmodel manage-object, date-effective) -
  navigator-GATED with a genuine 3-level SAME-ROW cascade (Production Unit -> Area -> Operator
  Route), unlike Area's/Contract Area's own single-dropdown navigator.
- **Treeview path:** Configuration > Assets > Facility_Objects > Collection Point (**CO.0205**)
- **DB view (ground truth):** `OV_COLLECTION_POINT` (versioned; key `CODE`; also `NAME`,
  `OBJECT_START_DATE`, `OBJECT_END_DATE`)
- **Last verified:** 2026-08-27 - EC 14.2.4 - local sandbox (`localhost:1521/ORCL`) - RF dryrun
  5/5 PASS this session; live headless TC01-TC04 PASS this session, TC05 hit a session-level
  environmental browser crash (see Quirks) — PR #541 (2026-08-26, source of the Area-pattern
  conversion this entry now describes) already recorded a clean live 5/5 with its own independent
  DB ground-truth. Supersedes the prior 2026-08-01 entry, which described the pre-conversion
  4-TC/Playwright-8/8 state (kept below for reference under "Selectors, pre-conversion").

## Selectors `[from collection_point_page.resource Variables section, transcribed 2026-08-27]`

| Purpose | Selector |
|---|---|
| Grid (rows) | `manageObject:form:T_data` |
| Navigator cascade (3-level, same row) | `nav:form:G:0:R:1:C:1:dd` (Production Unit) -> `C:2:dd` (Area) -> `C:3:dd` (Operator Route); `C:4` absent (no 4th level) |
| Navigator fill mechanism | Shared T2 `Apply Navigator From Properties` (`resources/manage_object.resource`), driven by `testdata/collection_point_navigator.properties` |
| Grid-filter | `Find/Clear Collection Point Row By Filter` -> shared T2 `Find/Clear Object Row By Filter` on the grid's Code column |
| Insert/Update/Verify | Delegates to shared T2 `Insert/Update/Verify Object *` keywords, all called with `code_label=Collection Point Code` |
| Delete End Date field | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (hardcoded, not label-driven - Start Date sits at C:1, End Date label at C:2, End Date value at C:3, same row-packing rationale as Area's/Bank's own del-enddate constant) |

## Mandatory / yellow fields
- **Navigator (before the grid loads any rows):** Production Unit -> Area -> Operator Route,
  all 3 levels + GO. PROVEN explicit values (not first-available — first-available breaks a
  later level on this screen): Op Production Unit=`P3 Production Unit`, Op Area=`P3 Area`,
  Op Operator Route=`Oper Route 1`.
- **Insert form:** Collection Point Code, Collection Point Name, Start Date (mandatory).
- **Update form:** Collection Point Name only (Collection Point Code is read-only in
  `updateAttributes`).
- Field labels are **screen-prefixed**: "Collection Point Code" / "Collection Point Name" (like
  Area's "Area Code"/"Area Name"), NOT the generic "Code"/"Name" that Bank/Object List use.

## Grid columns (confirmed live, `manageObject:form:T_head` scan)
Collection Point Code / Collection Point Name / Start Date / End Date (4-column shape, same as
Area/Facility Class 1).

## Automation (code lives in ec-automation - this file is the MD selector reference)
- **RF (the maintained suite):** T3
  `pageobjects/Configuration/Assets/Facility_Objects/collection_point_page.resource` (T2
  `resources/manage_object.resource` + `libraries/PropertiesReader.py`) + suite
  `tests/Configuration/Assets/Facility_Objects/collection_point_iud.robot` (5 TCs: Clean
  State/Insert/Update/Find/Delete, per-TC Login/Logout). Fixed test code
  `AUTOTEST_COLLECTION_POINT`. Converted to this shape via PR #541 (2026-08-26); previously 4
  TCs with suite-level login and inline nav-fill.
- **Test data:** `testdata/collection_point_{navigator,insert,update,form_verify,grid_verify}.properties`.
- **Credentials:** dedicated pair `COLLECTION_POINT_EC_USER`/`COLLECTION_POINT_EC_PASS` in
  `resources/credentials.py`.
- **Playwright (historical reference only, NOT maintained):**
  `py/collection_point_iud.py` - original 2026-08-01 build, preserved unchanged (PR #541 itself
  confirmed this file "left UNTOUCHED this round"); no new Playwright bundle is built for
  Area-pattern work (owner decision 2026-08-27, Universal Screen Engine replaces this role).
- Full bundle (SOW/README/JOURNAL/evidence/CHECKLIST):
  `screens/Configuration/Assets/Facility_Objects/Collection_Point/`.

## Quirks
- OV-GM, 3-level-cascade-gated: grid stays empty until ALL THREE navigator levels (Production
  Unit, Area, Operator Route) are filled + GO'd — do not assume a single-dropdown navigator like
  Area/Contract Area; Collection Point's cascade is genuinely 3 levels deep.
- **Cascade timing confirmed twice independently:** the shared T2 keyword's flat 0.7s sleep
  between navigator levels was confirmed live SUFFICIENT for this screen's own redraw timing at
  BOTH the PU->Area and Area->Operator Route transitions (2026-08-26, PR #541) — this is a second
  independent confirmation (after Chemical Stream Hookup, Batch 2) that the shared keyword's
  default timing generalizes across screens, not a one-off fit for a single case.
- **Fixed test code `AUTOTEST_COLLECTION_POINT`** (not a generated/timestamped code) — confirmed
  free via a fresh oracledb connection (0 rows) before use; every run must complete TC05 (delete)
  so the code is free for the next run.
- **Session-level browser-process contention (2026-08-27, this backfill's own re-verification
  pass, NOT a suite defect):** repeated `chrome-headless-shell.exe` processes kept respawning
  from another concurrent process in this shared session even after being killed, crashing the
  live suite mid-run (`Could not find active page` / `Playwright process has been terminated`)
  across 6 attempts. TC01-04 achieved a full clean pass in one attempt before TC05 hit the
  crash. A fresh DB connection confirmed 0 residual `AUTOTEST_COLLECTION_POINT` rows before and
  after every single attempt — no data was ever left behind. Always check
  `tasklist | grep -i chrome` for stray processes before concluding a live-run failure is a code
  defect.

## Selectors, pre-conversion (2026-08-01, retained for history — superseded above)
| Purpose | Selector |
|---|---|
| Open | search `Collection Point` -> `label.tv-link` "Collection Point" |
| Navigator | cascade `nav:form:G:0:R:1:C:1..N:dd` (PROVEN explicit values, not first-available) -> GO `#button:form:B` |
| Grid | `manageObject:form:T_data` (empty until cascade + GO) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |

Original automation note: Playwright `py/collection_point_iud.py` (shared engine
`ec_object_iud.py` + explicit `select_dropdown` per cascade level); RF was 4 TCs at that time,
gated by `verify_screen.py` -> OVERALL PASS (RF 4/4 + Playwright 8/8).
