# IUD Deliverable Checklist - Calendar Collection (CD.0105)

Per `docs/IUD-DELIVERABLE-CHECKLIST.md` Section H (2026-08-27 owner decision: Section G's lean
waiver is RETIRED except items 4/5). This is a Batch 8 backfill
(`docs/lean-deliverable-backfill-workorder.md`) — Steps 0, A (minus 4/5), B, C, D, E, ticked with
real evidence. No RF automation files were changed by this backfill; the RF suite/T3 were already
built and merged in PR #449 (2026-08-23, Batch 6).

## Step 0. Check-existing-first gate
- [x] **0a.** `ec-ui-knowledge/screens/calendar_collection.md` did not exist before this backfill
      (created new by item 20 below, sourced from the page object's own Variables section).
- [x] **0b.** `grep -ril "calendar_collection" workstreams/master-plan/ec-automation/{py,pageobjects,tests,screens}`
      -> found existing impl: `pageobjects/Configuration/Assets/Date_Objects/calendar_collection_page.resource`,
      `tests/Configuration/Assets/Date_Objects/calendar_collection_iud.robot`,
      `screens/Configuration/Assets/Date_Objects/Calendar_Collection/` bundle (pre-existing, predates
      the lean rule) -> REUSED/EXTENDED, no parallel copy built.
- [x] **0c.** N/A for this backfill (doc-only task, no new code path).

## A. Bundle artifacts - `screens/Configuration/Assets/Date_Objects/Calendar_Collection/`
- [x] **1. `calendar_collection_sow.md`** -- updated to describe the CURRENT Bank-pattern state
      (PR #449), keeping the original PR #144 history as historical record.
- [x] **2. `README.md`** -- bundle overview + exact run commands (dryrun/live/DB self-clean),
      updated for the current automation.
- [x] **3. `JOURNAL.md`** -- built / done-well / done-wrong / to-improve / blockers / decisions /
      evidence, sourced from PR #449's real body + this backfill's own re-run.
- [ ] **4. Playwright driver** -- N/A, permanently waived for Bank-pattern work (Section H); the
      Universal Screen Engine is the owner-decided replacement. ORIGINAL PR #144 driver
      (`playwright/ec_iud_calendar_collection.py`) left untouched, not rebuilt.
- [ ] **5. `investigation/`** -- N/A, permanently waived (same reason as #4). ORIGINAL PR #144
      recon scripts left untouched, not rebuilt.
- [x] **6. `evidence/`** -- ORIGINAL 11 screenshots + `results.json` (PR #144) left in place;
      NEW `evidence/rf_backfill_2026-08-28/` subfolder added with 20 screenshots + `output.xml` +
      `RESULTS.md` from this backfill's own live run.
- [x] **7. `CHECKLIST.md`** -- this file.

## B. RF files (pre-existing, untouched by this backfill)
- [x] **8. T3 page object** -- `pageobjects/Configuration/Assets/Date_Objects/calendar_collection_page.resource`
      (built PR #449; locators in Variables; docstring matches Variables).
- [x] **9. Suite** -- `tests/Configuration/Assets/Date_Objects/calendar_collection_iud.robot`
      (built PR #449; clean -> insert -> update -> find -> delete).

## C. Verification gates
- [x] **10. robocop clean (relative to baseline)** -- `robocop check` on T3 + suite = 9 issues
      (5x VAR02, 4x DOC02), matching the baseline PR #449 itself reported ("9 issues, matches
      established baseline"). Re-run 2026-08-28, same count. Not fixed here (doc-only backfill).
- [x] **11. `--dryrun` N/N PASS** -- `robot --dryrun tests/Configuration/Assets/Date_Objects/calendar_collection_iud.robot`
      -> 5 tests, 5 passed, 0 failed (re-run 2026-08-28).
- [x] **12. LIVE headless run N/N PASS** -- `EC_HEADLESS=true robot --outputdir /tmp/cc_live
      tests/Configuration/Assets/Date_Objects/calendar_collection_iud.robot` -> 5 tests, 5 passed,
      0 failed, first attempt, no retry needed (2026-08-28).
- [x] **13. DB ground-truth** -- in-suite `DbVerify` calls: TC02 `Code Should Be Present In View
      OV_CALENDAR_COLLECTION AUTOTEST_CALENDAR_COLLECTION`; TC05 `Code Should Be Absent In View
      OV_CALENDAR_COLLECTION AUTOTEST_CALENDAR_COLLECTION` (both PASS in the 2026-08-28 live run).
- [x] **14. FULL I-U-D scope** -- TC02 Insert + TC03 Update (Name) + TC04 Find + TC05 Delete
      (End=Start), all present and PASS in the current suite.
- [x] **15. Self-clean confirmed** -- independent fresh-connection re-check (separate `oracledb`
      connection from the suite's own): `SELECT COUNT(*) FROM OV_CALENDAR_COLLECTION WHERE CODE =
      'AUTOTEST_CALENDAR_COLLECTION'` = 0; `SELECT COUNT(*) FROM OV_CALENDAR_COLLECTION` = 7
      (unchanged pre-existing rows, matches SOW's recon count).
- [x] **16. Hygiene PASS** -- `py scripts/check_bundle_hygiene.py` (repo-wide) -> RESULT: PASS
      (R16 env creds, R20 ASCII, no CHECKLIST/VERIFY-REPORT contradictions). Sole WARN in the
      repo-wide scan is unrelated (Contract Area's investigation script).

## D. Delivery
- [x] **17. Registry row** -- already present (append-only, R23) at
      `docs/ec_screen_registry.md` line ~123 for Calendar Collection (CD.0105), describing the
      PR #449 Bank-pattern rebuild; not re-appended by this backfill (no new fact to add beyond
      what the row already states).
- [x] **18. Scorecard row** -- already present in `docs/automation-scorecard.md` for Calendar
      Collection from the PR #449 merge; not re-appended by this backfill.
- [x] **19. PR** -- this backfill's PR uses the standard body (What was backfilled / Files added /
      Base branch = master); R8 synced with origin/master before push; never self-merged.

## E. Knowledge base
- [x] **20. KB selector map** -- `ec-ui-knowledge/screens/calendar_collection.md` created by this
      backfill, transcribed from `calendar_collection_page.resource`'s own Variables section (grid
      id, delete field id, form labels) -- not re-discovered live.
- [x] **21. Reuse clause** -- Step 0 found the screen already implemented; this backfill produced
      the required refresh artifacts (JOURNAL, evidence, KB map) rather than declaring "done" on
      green tests alone.

**Items 4/5 explicitly N/A per Section H's permanent waiver for Bank-pattern work. All other
items (Steps 0, A-1/2/3/6/7, B, C, D, E) are green with real evidence, none fabricated.**
