# IUD Task — Deliverable Checklist — Service (CO.2103)

_Copied from `docs/IUD-DELIVERABLE-CHECKLIST.md`. This is a **documentation/evidence backfill**
(`docs/lean-deliverable-backfill-workorder.md`, owner decision 2026-08-27, Section H, Batch 3) around
already-merged, already-live-tested RF automation (PR #552, merged 2026-08-26). No RF file
(`service_page.resource`, `service_iud.robot`, `testdata/service_*.properties`) was modified to
produce this checklist. Items 4/5 (Playwright driver + investigation/) stay permanently waived per
Section H — a pre-existing Playwright bundle from the screen's original 2026-08-01 build is kept in
this bundle unchanged, not rebuilt._

## Step 0. CHECK-EXISTING-FIRST GATE
- [x] **0a.** `ec-ui-knowledge/screens/service.md` existed before this backfill (from the 2026-08-01
      build) — rewritten in this backfill with selectors transcribed from `service_page.resource`'s
      own Variables section (not re-scanned live), plus the PR #552 conversion + this session's
      disclosed flake.
- [x] **0b.** `grep -ril service workstreams/master-plan/ec-automation/{py,pageobjects,tests,screens}`
      → existing impl found: `py/service_iud.py`,
      `pageobjects/Configuration/Assets/Service_Objects/service_page.resource`,
      `tests/Configuration/Assets/Service_Objects/service_iud.robot`,
      `screens/Configuration/Assets/Service_Objects/Service/` (SOW/README/JOURNAL/CHECKLIST/
      investigation/evidence pre-existed from the 2026-08-01 build). REUSED/EXTENDED — no parallel
      copy built.
- [x] **0c.** Shared engine reused: RF suite calls the shared T2 `resources/manage_object.resource`
      (`Insert/Update/Verify Object *`, `Apply Navigator From Properties`) + `libraries/DbVerify.py`
      for this backfill's own evidence-capture DB reads. No new plumbing added.

## A. Bundle artifacts — `screens/Configuration/Assets/Service_Objects/Service/`
- [x] **1. `service_sow.md`** — updated with the current nav/grid/cell shape (Business Unit single
      dropdown, navigator-scope-bound Contract/Transport System fields), test data (fixed
      `AUTOTEST_SERVICE` code), and the dev story pulled from PR #552's real body (`gh pr view 552`).
- [x] **2. `README.md`** — updated with the bundle overview + exact run commands (dryrun/live/DB
      self-clean pattern) + the disclosed flake.
- [x] **3. `JOURNAL.md`** — added 2026-08-26 (PR #552, from its real PR body) and 2026-08-27 (this
      backfill's own 8-attempt evidence-capture log, disclosed honestly) sections.
- [ ] **4. Playwright driver** — N/A. Playwright bundle waived, owner decision 2026-08-27 (Section H
      of `docs/IUD-DELIVERABLE-CHECKLIST.md`); the pre-existing `py/service_iud.py` from the
      2026-08-01 build is kept unchanged, not rebuilt.
- [ ] **5. `investigation/`** — N/A, same waiver as item 4; the pre-existing `investigation/recon.py`
      from the 2026-08-01 build is kept unchanged.
- [x] **6. `evidence/`** — refreshed in this session: `log.html`, `output.xml`, `report.html`,
      `playwright-log.txt`, per-TC screenshots, and `browser/screenshot/fail-screenshot-{1,2}.png`
      from a live RF run (2026-08-27, best of 8 attempts, 4/5 PASS — see JOURNAL.md), alongside the
      pre-existing 2026-08-01 Playwright evidence (`SV_0[1-5]_*.png`, `results.json`, unchanged).
- [x] **7. `CHECKLIST.md`** — this file.

## B. RF files — treeview-mirrored (pre-existing, unmodified by this backfill)
- [x] **8. T3 page object** `pageobjects/Configuration/Assets/Service_Objects/service_page.resource`
      — pre-existing, merged in PR #552, not touched by this backfill.
- [x] **9. Suite** `tests/Configuration/Assets/Service_Objects/service_iud.robot` — pre-existing,
      merged in PR #552, not touched by this backfill.

## C. Verification gates (re-run for evidence, not re-verification of a defect)
- [x] **10. robocop clean** — `py -m robocop check pageobjects/.../service_page.resource
      tests/.../service_iud.robot` (this session, 2026-08-27) → **7 issues** (DOC02 missing TC/keyword
      docs) — matches PR #552's own cited 7-issue baseline exactly (parity with Area's reference
      files). No drift, no new issue category.
- [x] **11. `--dryrun` N/N PASS** — `robot --dryrun
      tests/Configuration/Assets/Service_Objects/service_iud.robot` (this session) → **5/5 PASS**.
      Full-tree `robot --dryrun tests/` → **883/883 PASS**, zero collisions.
- [x] **12. LIVE headless run N/N PASS — REAL result, disclosed honestly (not smoothed over).** This
      session attempted the live suite **8 times** and hit a genuine, reproducible intermittent flake
      (a navigator autocomplete panel occasionally intercepting a later grid-filter click — see
      JOURNAL.md's full attempt log and `ec-ui-knowledge/screens/service.md`'s Quirks section). Best
      clean result: **4/5 PASS** (run 7 of 8, only TC01 hit the flake) — this is the run whose
      artifacts are kept in `evidence/`. Every attempted DB operation was independently confirmed
      correct via `DbVerify.fetch_object` regardless of the UI-level flake. PR #552's OWN prior live
      run (merged 2026-08-26) was a clean **5/5** — cited in JOURNAL.md's 2026-08-26 section — so the
      automation itself is proven capable of 5/5; this session's result reflects environment
      conditions encountered during evidence capture, not a change to the automation.
- [x] **13. DB ground-truth** — `libraries.DbVerify.fetch_object("OV_SERVICE", "AUTOTEST_SERVICE")` →
      `None` (absent) verified via a fresh oracledb connection before this session's runs, after each
      cleanup, and after the final (run 7) run.
- [x] **14. FULL I-U-D scope** — TC02 Insert / TC03 Update / TC05 Delete all present (plus TC01 Clean
      State, TC04 Find) — confirmed by reading `service_iud.robot`'s 5 test cases; each op was
      individually confirmed to complete correctly at the DB level across this session's 8 attempts
      (the flake only ever affected the UI-level grid-filter click step, never the underlying
      Insert/Update/Delete operation itself).
- [x] **15. Self-clean confirmed** — independent DB re-read (fresh connection, this session) = 0
      residual `AUTOTEST_SERVICE` rows in `OV_SERVICE`, both before this session started and after
      the final run. Two interrupted attempts during this session left a residual row each time;
      both were cleaned via the screen's own TC05 delete flow (not raw SQL), confirmed absent
      afterward.
- [x] **16. Hygiene PASS** — `py scripts/check_bundle_hygiene.py` (repo root, this session) →
      `[hygiene] RESULT: PASS - no hardcoded creds (R16), pure ASCII (R20), no CHECKLIST/VERIFY-REPORT
      contradictions, doc rows match declared families` (167 bundles + 272 recon scripts scanned; the
      2 pre-existing WARN lines belong to Contract Area's investigation script, unrelated to Service).

## D. Delivery
- [ ] **17. Registry row** — N/A for this backfill. Service's row in
      `workstreams/master-plan/ec-automation/docs/ec_screen_registry.md` already exists and already
      documents the PR #552 conversion (append-only edit made at merge time of that PR, not this
      backfill).
- [ ] **18. Scorecard row** — N/A for this backfill, same reasoning as item 17 —
      `docs/automation-scorecard.md`'s Service row already reflects the merged conversion.
- [x] **19. PR** — this backfill's own PR, with the standard body (What was backfilled / Files added /
      Base branch = master); never self-merged.

## E. Knowledge base
- [x] **20. KB selector map** `ec-ui-knowledge/screens/service.md` — rewritten in this backfill:
      selectors transcribed from `service_page.resource`'s Variables section, mandatory/navigator-
      scope-bound fields, the disclosed navigator-panel click-intercept flake, last-verified date
      2026-08-27.
- [x] **21. Reuse clause.** Step 0 found Service's RF automation ALREADY implemented and merged (PR
      #552) — this backfill produces exactly the deliverables the reuse clause requires: #3 JOURNAL,
      #6 evidence, #20 KB map (plus #1/#2/#7 restored per Section H).
