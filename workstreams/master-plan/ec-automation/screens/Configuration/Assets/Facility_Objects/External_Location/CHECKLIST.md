# IUD Task - Deliverable Checklist (External Location, CO.0227)

Copied from `docs/IUD-DELIVERABLE-CHECKLIST.md` (Section H restored). This is a **backfill** per
`docs/lean-deliverable-backfill-workorder.md` Batch 1 - the RF automation itself is pre-existing,
merged, and live-tested (PR #524 + PR #528, 2026-08-26); this checklist documents the deliverable
bundle now brought up to the restored standard, not a fresh build.

## Step 0. CHECK-EXISTING-FIRST GATE
- [x] **0a.** `ec-ui-knowledge/screens/external_location.md` existed (from the 2026-08-01 base build) -
      read and used; refreshed in this backfill for the 2026-08-26 RF conversion.
- [x] **0b.** `grep -ril "external_location" workstreams/master-plan/ec-automation/{py,pageobjects,tests,screens}`
      -> only this screen's own files (driver, T3, suite, testdata, this bundle). No parallel copy.
- [x] **0c.** Shared engine reused throughout: `py/ec_object_iud.py` (Playwright, 2026-08-01, untouched)
      + `resources/manage_object.resource` T2 (RF, 2026-08-26 conversion) + `libraries/DbVerify.py`.

## A. Bundle artifacts - `screens/Configuration/Assets/Facility_Objects/External_Location/`
- [x] **1. `external_location_sow.md`** - refreshed this backfill: classification (OV-GM,
      zero-mandatory-nav edge case), nav/grid/cell shape, test data, dev story pulled from PR
      #524/#528's real bodies.
- [x] **2. `README.md`** - refreshed this backfill: bundle overview + exact dryrun/live/DB-self-clean/
      hygiene commands.
- [x] **3. `JOURNAL.md`** - refreshed this backfill: kept the 2026-08-01 base-build entry, added a
      2026-08-26 entry (Built/Done well/Done wrong-lessons/Blockers->resolution/Decisions/Evidence)
      sourced from PR #524/#528 bodies, per the Bank JOURNAL.md model.
- [ ] **4. `playwright/ec_iud_external_location.py`** - N/A, standing waiver (Section H, unchanged from
      Section G): the Universal Screen Engine replaces hand-written Playwright drivers going forward.
      NOTE: this screen already HAS a pre-existing driver at `py/external_location_iud.py` from the
      2026-08-01 base build (predates the waiver) - left untouched, not rebuilt or relocated.
- [ ] **5. `investigation/`** - N/A, same standing waiver. NOTE: this screen already has a pre-existing
      `investigation/recon.py` from the 2026-08-01 base build - left untouched.
- [x] **6. `evidence/`** - refreshed this backfill: added `evidence/rf_backfill_2026-08-27/`
      (log.html/output.xml/report.html) from a real live re-run, **5/5 pass**. Original 2026-08-01
      Playwright evidence (`EL_0[1-5]_*.png` + `results.json`, 8/8 pass) kept as-is alongside it.
- [x] **7. `CHECKLIST.md`** - this file.

## B. RF files (pre-existing, merged, NOT touched by this backfill)
- [x] **8. T3 page object** `pageobjects/Configuration/Assets/Facility_Objects/external_location_page.resource`
      (label-driven, docstring matches Variables per PR #528).
- [x] **9. Suite** `tests/Configuration/Assets/Facility_Objects/external_location_iud.robot` - 5 TCs
      (Clean State -> Insert -> Update -> Find -> Delete), per-TC Login/Logout.

## C. Verification gates (re-run for this backfill; RF automation itself unchanged)
- [x] **10. robocop clean** - per PR #528's body: 7 issues (VAR02 x2 + DOC02 x5) on
      `external_location_page.resource`/`external_location_iud.robot`, run against `area_page.resource`/
      `area_iud.robot` (the reference files) and got the identical 7 issues/categories - exact parity,
      not a regression. Not re-run in this backfill session (no code changed); cited from the merged PR.
- [x] **11. `--dryrun` full-tree PASS** - re-run this backfill (2026-08-27):
      `robot --dryrun tests/` -> **883 tests, 883 passed, 0 failed** (zero collisions).
- [x] **12. LIVE headless run PASS** - re-run this backfill (2026-08-27):
      `EC_HEADLESS=true robot tests/Configuration/Assets/Facility_Objects/external_location_iud.robot`
      -> **5 tests, 5 passed, 0 failed**. Evidence: `evidence/rf_backfill_2026-08-27/`.
- [x] **13. DB ground-truth** - re-run this backfill, fresh `oracledb` connection
      (`localhost:1521/ORCL`, `ECKERNEL_EC`): `SELECT COUNT(*) FROM OV_EXTERNAL_LOCATION WHERE CODE
      LIKE 'AUTOTEST_EXTERNAL_LOCATION%'` -> **0** (both exact-match and prefix query). Each op is
      verified at DB level inside the shared T2 (`Verify Object Insert Exists` / `Verify Object Form
      Record` / `Verify Object Removed`), per PR #528's body.
- [x] **14. FULL I-U-D scope** - Insert (TC02) + Update (TC03) + Delete (TC05) all present, plus
      Find (TC04) - not I/D only.
- [x] **15. Self-clean confirmed** - re-run this backfill: fresh-connection re-read after the live run
      = 0 residual `AUTOTEST_EXTERNAL_LOCATION%` rows in `OV_EXTERNAL_LOCATION`.
- [x] **16. Hygiene PASS** - re-run this backfill (2026-08-27) from repo root:
      `py scripts/check_bundle_hygiene.py` -> `[hygiene] RESULT: PASS - no hardcoded creds (R16), pure
      ASCII (R20), no CHECKLIST/VERIFY-REPORT contradictions, doc rows match declared families` (the
      2 WARN lines printed are pre-existing Contract Area recon-script items, unrelated to this screen).

## D. Delivery
- [x] **17. Registry row** - already present, updated by PR #524 and PR #528 (append/update-in-place
      per screen convention) at `docs/ec_screen_registry.md`, External Location row.
- [x] **18. Scorecard row** - already present, updated by PR #524 and PR #528 at
      `docs/automation-scorecard.md`.
- [ ] **19. PR** - this backfill's own PR (doc-only, standard 6-field body), raised after this
      checklist is complete. Never self-merge.

## E. Knowledge base
- [x] **20. KB selector map** `ec-ui-knowledge/screens/external_location.md` - refreshed this backfill
      to reflect the 2026-08-26 RF conversion (5-TC structure, properties-driven insert/update,
      explicit grid-filter wiring, fixed `AUTOTEST_EXTERNAL_LOCATION` test code), last-verified date
      updated to 2026-08-27.
- [x] **21. Reuse clause** - Step 0 found the screen ALREADY implemented (2026-08-01 base build,
      2026-08-26 RF conversion); this backfill produces/refreshes JOURNAL + evidence + KB map + SOW +
      README + CHECKLIST accordingly - not just re-confirming passing tests.

---

**Deviation from the generic backfill-workorder template, disclosed:** the work order's generic
per-screen instructions say to mark items 4/5 N/A. For External Location specifically, items 4/5 are
NOT absent - a pre-existing Playwright driver + investigation script already exist from the
2026-08-01 base build (before the lean waiver existed). Marking them N/A would misstate reality; they
are ticked-as-pre-existing above with the honest note that they predate and are untouched by both the
waiver and this backfill.
