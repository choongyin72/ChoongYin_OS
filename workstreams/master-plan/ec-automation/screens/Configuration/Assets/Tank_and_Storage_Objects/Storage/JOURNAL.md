# JOURNAL - Storage (CO.0034) OV-GM IUD

## 2026-07-30 (original build)
- **Branch:** `feature/ov-gm-storage` (stacked on the gated-navigator capability, PR #244).
  Check-existing gate: grep ec-automation -> only this build; reused shared engine
  (ec_object_iud.py) + T2 + DbVerify.
- **Recon** (`investigation/recon.py`, read-only + tmp/storage/config.json scan): OV-GM (grid
  `manageObject:form:T_data`), navigator cascade Production Unit -> Area -> Facility Class 1.
  Mandatory Storage Code / Storage Name / Start Date + dropdowns Storage Type, Product Name.
- **Built** (generator `tmp/gen_ovgm.py` -> proven Node/Chemical-Tank template): label-driven T3
  (no hardcoded ids); Playwright driver + RF T3/suite. Op Production Unit set first-available
  for grid visibility.
- `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4 pass,
  Playwright 8/8. DB residual 0.

## 2026-08-26 — PR #537: full Area-pattern structural conversion
- **Built:** converted Storage from its old pattern (bespoke inline "Apply OV-GM Navigator
  First Available" navigator-fill, 4 TCs, single suite-level login, generated/timestamped test
  code) to Area's full pattern: 5 TCs (Verify Clean State / Insert / Update / Find / Delete),
  per-TC Login/Logout on one Suite-Setup-opened browser, fixed test code `AUTOTEST_STG`
  (confirmed free in `OV_STORAGE` before use), properties-file-driven Insert/Update/verify via
  the shared T2 keywords, explicit `Find/Clear Storage Row By Filter` grid-filter wiring into
  Update/Find/Verify-Found/Delete, and PURE SCREEN verification in the `.robot` file (zero
  inline DB-verify calls — TC05's DB check lives inside the shared T2 `Verify Object Removed`).
  The genuine 3-level Production Unit -> Area -> Facility Class 1 navigator cascade is kept, but
  the fill mechanism moved from "Apply OV-GM Navigator First Available" to the shared T2
  "Apply Navigator From Properties", driven by a new `storage_navigator.properties` with
  EXPLICIT values confirmed live via a dedicated recon script
  (`tmp/recon_storage_navigator_cascade.py`, gitignored): `Op Production Unit=AS1 EC
  Exploration Norway`, `Op Area=AS1_Area`, `Op Facility Class 1=AS1_Facility_01` — the same
  values first-available already picked, now captured explicitly. Storage's own genuine
  mandatory `Storage Type`/`Product Name` dropdowns kept as `__FIRST__`, preserving the proven
  driver's exact handling. No T1/T2 (`resources/manage_object.resource`/`resources/
  common.resource`) changes were needed.
- **Files touched:** `pageobjects/.../storage_page.resource` (rebuilt to Area's shape),
  `tests/.../storage_iud.robot` (rebuilt: 5 TCs, per-TC login), 5 new `testdata/storage_*
  .properties` files, `resources/credentials.py` (additive `STORAGE_EC_USER`/`STORAGE_EC_PASS`),
  `docs/ec_screen_registry.md` + `docs/automation-scorecard.md` (modified existing Storage
  rows). No other screen's files were touched — done in an isolated worktree
  (`C:/tmp/wt-storage`) off `origin/master`.

## Done well
- Full I-U-D DB-verified vs `OV_STORAGE` (insert Name, update Name, delete End=Start -> absent);
  fresh-connection self-clean 0 residual `AUTOTEST%` rows.
- Live RF 5/5 pass at PR time; full-tree dryrun 850/850; filter keyword confirmed fired 15x in
  `output.xml`.
- Trusted the already-proven driver's behaviour (leaving Op Production Unit/Op Area/Op Facility
  Class 1 blank on insert) instead of hunting for an unstated requirement, per the owner's
  standing rule from the External Location incident.

## Done wrong / lessons
- The bundle under `screens/Configuration/Assets/Tank_and_Storage_Objects/Storage/` (SOW,
  README, JOURNAL, evidence, CHECKLIST) was NOT refreshed at PR #537's merge — it still
  described the pre-conversion 4-TC/first-available/timestamped-code shape until this backfill
  (2026-08-28). The registry and scorecard rows WERE updated at merge time; the screen-local
  bundle was missed. This is exactly the gap `docs/lean-deliverable-backfill-workorder.md`
  exists to close.
- During this backfill's live re-run (2026-08-28), the first attempt's TC05 failed on the
  post-delete grid assertion (`Row AUTOTEST_STG should NOT exist ... 1 != 0`) while a fresh DB
  connection immediately after showed 0 `AUTOTEST%` rows in `OV_STORAGE` — a screen-side
  lazy-redraw timing issue on the versioned groupmodel grid after delete, not a real residual
  row or a code defect. A same-day retry (one retry, per the process rule) passed 5/5 clean.
  Disclosed here rather than smoothed over, per the backfill task's honesty requirement.

## Blockers -> resolution
- One live-run flake (TC05 grid-redraw timing, above) -> resolved by a single retry, no data
  damage, no code change. No other blockers.

## Decisions
- Playwright driver `py/storage_iud.py` stays untouched and un-rebuilt — permanently waived per
  the 2026-08-27 owner decision (Universal Screen Engine replaces that role going forward).
- This backfill only adds documentation/evidence artifacts; it does not re-run the original
  build or modify `storage_page.resource`, `storage_iud.robot`, or any `testdata/storage_*
  .properties` file.

## Evidence
- Dryrun (2026-08-28, this backfill): `evidence/dryrun_output.xml` — 5/5 pass.
- Live headless run #1 (2026-08-28): `evidence/live_attempt1_output.xml` — 4/5 pass, TC05 grid
  assertion flake (see "Done wrong / lessons").
- Live headless run #2 / retry (2026-08-28): `evidence/live_output.xml` +
  `evidence/live_report.html` — 5/5 pass. Cited as this backfill's live evidence.
- DB self-clean (fresh `oracledb` connection, 2026-08-28): `SELECT CODE, OBJECT_START_DATE,
  OBJECT_END_DATE FROM OV_STORAGE WHERE CODE LIKE 'AUTOTEST%'` -> empty result set (0 residual).
