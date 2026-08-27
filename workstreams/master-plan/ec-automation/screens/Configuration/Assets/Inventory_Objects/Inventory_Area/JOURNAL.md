# JOURNAL - Inventory Area (CD.0115) OV IUD

_Screen: Configuration > Assets > Inventory_Objects > Inventory Area (OV, date-effective). View
`OV_INVENTORY_AREA`. This JOURNAL covers two build passes (original 2026-07-26, Bank-pattern
conversion 2026-08-23/PR #460) plus the 2026-08-28 documentation backfill (Batch 9 of
`docs/lean-deliverable-backfill-workorder.md`) that restored the SOW/README/JOURNAL/evidence/
CHECKLIST/KB artifacts Section G's since-retired lean waiver had skipped for the PR #460 rebuild._

## Built

### 2026-07-26 (original build)
- **Branch:** `feature/inventory_area-iud` (own branch, stacked so the shared-engine helpers are present).
  Check-existing gate: only this build; reused shared engine + T2 + DbVerify.
- **Recon** (`investigation/recon.py`, read-only): DB `CLASS_TYPE=OBJECT` => OV; treeview
  Configuration > Assets > Inventory_Objects > Inventory Area. Mandatory Code/Name/Start Date; optional dropdowns skipped.
  Plain Bank-layout OV (single Date+GO nav, no mandatory dropdowns).
- **Label-driven** T3 (no hardcoded ids). Playwright driver -> 7/7; RF T3+suite -> live 4/4.
- `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4, Playwright 7/7.

### 2026-08-23 (Batch 8, PR #460 - Bank-pattern conversion)
- Brought Inventory Area from the partial 2026-07-26 label-driven build to the FULL Bank/Berth-pattern
  shape: properties-file-driven insert/update/verify, explicit grid-filter wiring, dedicated
  per-screen credentials, fixed test code, and a 5-TC per-TC-login business narrative.
- **Files touched:** `pageobjects/.../inventory_area_page.resource` (rebuilt to mirror
  `berth_page.resource`), `tests/.../inventory_area_iud.robot` (rebuilt to mirror `berth_iud.robot`),
  `resources/credentials.py` (additive: `INVENTORY_AREA_EC_USER`/`INVENTORY_AREA_EC_PASS`),
  4 new `testdata/inventory_area_*.properties` files, `docs/ec_screen_registry.md` +
  `docs/automation-scorecard.md` (MODIFIED existing rows, not duplicated), plus new Batch 8
  sections in `docs/grid-filter-standardization-checklist.md` and
  `docs/bank-pattern-conversion-checklist.md`. Zero changes to `resources/manage_object.resource`
  or `resources/common.resource`.
- Isolated sparse-checkout clone under `Workplaces/inventory_area/`; own-files-only commit (no
  `git add -A`); synced with master before push.

## Done well
- Live run 5/5 PASS (TC01 Verify Clean State / TC02 Insert / TC03 Update / TC04 Find / TC05 Delete);
  `robot --dryrun` on the full `tests/` tree -> 758/758 pass, 0 fail.
- Filter keyword confirmed fired: `grep -o "Find Inventory Area Row By Filter" output.xml | wc -l` -> 11 hits.
- DB self-clean via a fresh `oracledb` connection, run both BEFORE and AFTER the live suite:
  `SELECT COUNT(*) FROM OV_INVENTORY_AREA WHERE CODE = 'AUTOTEST_INVA'` = 0 and
  `CODE LIKE 'AUTOTEST%'` = 0, both times.
- Exact DbVerify assertions exercised: `Code Should Be Present In View`/`Code Should Be Absent In
  View` (`OV_INVENTORY_AREA`) via T2's `Verify Object Insert Exists`/`Verify Object Removed`/
  `Verify Object Does Not Exist`.
- No shared T1/T2 keyword changes (Batch 8 ground rule) - confirmed via `git status --short`, zero
  diff outside Inventory Area's own files.

## Done wrong / lessons
- The 2026-07-26 build's bundle (SOW/README/JOURNAL/CHECKLIST/KB map) was never refreshed when PR
  #460 rebuilt the underlying RF files on 2026-08-23 - it kept describing the OLD 4-TC label-driven
  shape (no grid-filter wiring, generated-per-run test code, no dedicated credentials) for 5 days
  while the real suite was already 5-TC/properties-driven/filter-wired. Root cause: the 2026-08-23
  lean waiver (Section G of `IUD-DELIVERABLE-CHECKLIST.md`) explicitly skipped SOW/README/JOURNAL/
  evidence/CHECKLIST/KB for Bank-pattern conversions, so PR #460 correctly did not touch them under
  the rule active at the time - but that left the bundle stale until this 2026-08-28 backfill
  (Section H retiring the waiver) caught up the docs to match the code.
- Carried the same lesson Batch 7 already flagged in PR #460's own body: registry/scorecard rows
  must be a clean replacement of the old row, not left duplicated - confirmed already correct in
  PR #460, re-verified here rather than re-done.

## Blockers -> resolution
- None for this backfill pass - documentation-only, no automation files touched, no live-run
  failures on the single re-run captured as evidence.

## Decisions
- Playwright driver (`py/inventory_area_iud.py`) is left exactly as it was in 2026-07-26 - not
  rebuilt for the Batch 8 RF conversion, and not rebuilt for this backfill either, per the
  owner's 2026-08-27 decision that the Universal Screen Engine (`py/engine.py`) supersedes
  hand-written Playwright drivers going forward (items 4/5 of the checklist stay waived
  permanently, unlike SOW/README/JOURNAL/evidence/CHECKLIST/KB which Section H restored).
- Code lives in `ec-automation`; `ec-ui-knowledge/` (repo root) is MD-only.

## Evidence
- **2026-07-26:** Playwright 7/7; RF live 4/4 (`VERIFY-REPORT.md`, OVERALL PASS).
- **2026-08-23 (PR #460):** live RF 5/5, full-tree dryrun 758/758, filter-fired grep = 11, DB
  self-clean 0 residual (both before/after, fresh connection) - all cited in the PR body.
- **2026-08-28 (this backfill):** `EC_HEADLESS=true robot tests/Configuration/Assets/
  Inventory_Objects/inventory_area_iud.robot` -> **5/5 PASS** re-confirmed; artifacts at
  `evidence/TC0[1-5]*.png` + `evidence/rf_report.html` + `evidence/rf_log.html`.
