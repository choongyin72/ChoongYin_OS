# IUD Deliverable Checklist - Calendar (CD.0024)

Per `docs/IUD-DELIVERABLE-CHECKLIST.md` Section H (2026-08-27 owner decision: Section G's lean
waiver is RETIRED except items 4/5). This is a Batch 8 backfill
(`docs/lean-deliverable-backfill-workorder.md`) -- Steps 0, A (minus 4/5), B, C, D, E, ticked with
real evidence. No RF automation files were changed by this backfill; the RF suite/T3 were already
built and merged in PR #451 (2026-08-23, Batch 6, final of the 23-screen conversion pool).

## Step 0. Check-existing-first gate
- [x] **0a.** `ec-ui-knowledge/screens/calendar.md` did not exist before this backfill (created
      new by item 20 below, sourced from the page object's own Variables section).
- [x] **0b.** `grep -ril "calendar" workstreams/master-plan/ec-automation/{py,pageobjects,tests,screens}`
      (excluding "calendar_collection") -> found existing impl:
      `pageobjects/Configuration/Assets/Date_Objects/calendar_page.resource`,
      `tests/Configuration/Assets/Date_Objects/calendar_iud.robot`,
      `screens/Configuration/Assets/Date_Objects/Calendar/` bundle (pre-existing, predates the
      lean rule) -> REUSED/EXTENDED, no parallel copy built.
- [x] **0c.** N/A for this backfill (doc-only task, no new code path).

## A. Bundle artifacts - `screens/Configuration/Assets/Date_Objects/Calendar/`
- [x] **1. `calendar_sow.md`** -- updated to describe the CURRENT Bank-pattern state (PR #451),
      keeping the original build's history as historical record.
- [x] **2. `README.md`** -- bundle overview + exact run commands (dryrun/live/DB self-clean),
      updated for the current automation.
- [x] **3. `JOURNAL.md`** -- built / done-well / done-wrong / to-improve / blockers / decisions /
      evidence, sourced from PR #451's real body + this backfill's own re-run.
- [ ] **4. Playwright driver** -- N/A, permanently waived for Bank-pattern work (Section H); the
      Universal Screen Engine is the owner-decided replacement. ORIGINAL driver
      (`playwright/ec_iud_calendar.py`) left untouched, not rebuilt.
- [ ] **5. `investigation/`** -- N/A, permanently waived (same reason as #4). ORIGINAL recon
      scripts left untouched, not rebuilt.
- [x] **6. `evidence/`** -- ORIGINAL 11 screenshots + `results.json` left in place; NEW
      `evidence/rf_backfill_2026-08-28/` subfolder added with screenshots + `output.xml` +
      `RESULTS.md` from this backfill's own live run.
- [x] **7. `CHECKLIST.md`** -- this file.

## B. RF files (pre-existing, untouched by this backfill)
- [x] **8. T3 page object** -- `pageobjects/Configuration/Assets/Date_Objects/calendar_page.resource`
      (built PR #451; locators in Variables; docstring matches Variables).
- [x] **9. Suite** -- `tests/Configuration/Assets/Date_Objects/calendar_iud.robot` (built PR #451;
      clean -> insert -> update -> find -> delete).

## C. Verification gates
- [x] **10. robocop clean (relative to baseline)** -- `robocop check` on T3 + suite = 9 issues
      (4x VAR02 + 5x DOC02), matching the baseline PR #451 itself reported ("9 issues, matches
      established baseline"). Re-run 2026-08-28, same count. Not fixed here (doc-only backfill).
- [x] **11. `--dryrun` N/N PASS** -- `robot --dryrun tests/Configuration/Assets/Date_Objects/calendar_iud.robot`
      -> 5 tests, 5 passed, 0 failed (re-run 2026-08-28, `_dryrun/output.xml`).
- [x] **12. LIVE headless run N/N PASS** -- `EC_HEADLESS=true robot --outputdir _live
      tests/Configuration/Assets/Date_Objects/calendar_iud.robot` -> 5 tests, 5 passed, 0 failed,
      first attempt, no retry needed (2026-08-28).
- [x] **13. DB ground-truth** -- in-suite `DbVerify` calls (via T2 `manage_object.resource`):
      TC02 insert verified present in `OV_CALENDAR`; TC05 `Verify Object Removed` confirms
      absence from `OV_CALENDAR` (both PASS in the 2026-08-28 live run).
- [x] **14. FULL I-U-D scope** -- TC02 Insert + TC03 Update (Calendar Name) + TC04 Find + TC05
      Delete (End=Start), all present and PASS in the current suite.
- [x] **15. Self-clean confirmed** -- independent fresh-connection re-check (separate `oracledb`
      connection from the suite's own): `SELECT COUNT(*) FROM OV_CALENDAR WHERE CODE =
      'AUTOTEST_CALENDAR'` = 0; `SELECT COUNT(*) FROM OV_CALENDAR` = 6 (unchanged pre-existing
      rows, matches SOW's recon count).
- [x] **16. Hygiene PASS** -- `py scripts/check_bundle_hygiene.py` (repo-wide) -> RESULT: PASS
      (R16 env creds, R20 ASCII, no CHECKLIST/VERIFY-REPORT contradictions). Sole WARN in the
      repo-wide scan is unrelated (Contract Area's investigation script).

## D. Delivery
- [x] **17. Registry row** -- already present (append-only, R23) at
      `docs/ec_screen_registry.md` line ~122 for Calendar (CD.0024), describing the PR #451
      Bank-pattern rebuild; not re-appended by this backfill (no new fact to add beyond what the
      row already states).
- [x] **18. Scorecard row** -- already present in `docs/automation-scorecard.md` (Date Objects
      row) for Calendar from the PR #451 merge; not re-appended by this backfill.
- [x] **19. PR** -- this backfill's PR uses the standard body (What was backfilled / Files added /
      Base branch = master); R8 synced with origin/master before push; never self-merged.

## E. Knowledge base
- [x] **20. KB selector map** -- `ec-ui-knowledge/screens/calendar.md` created by this backfill,
      transcribed from `calendar_page.resource`'s own Variables section (grid id, delete field
      id, form labels) -- not re-discovered live.
- [x] **21. Reuse clause** -- Step 0 found the screen already implemented; this backfill produced
      the required refresh artifacts (JOURNAL, evidence, KB map) rather than declaring "done" on
      green tests alone.

**Items 4/5 explicitly N/A per Section H's permanent waiver for Bank-pattern work. All other
items (Steps 0, A-1/2/3/6/7, B, C, D, E) are green with real evidence, none fabricated.**
