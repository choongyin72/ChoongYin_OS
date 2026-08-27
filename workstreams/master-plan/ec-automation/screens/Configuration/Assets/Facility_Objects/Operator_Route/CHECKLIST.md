# Operator Route - IUD Deliverable Checklist (vs docs/IUD-DELIVERABLE-CHECKLIST.md)

_Refreshed 2026-08-27 as part of `docs/lean-deliverable-backfill-workorder.md` (owner decision
2026-08-27, Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md` retired the 2026-08-23/26 lean
waiver except for items 4/5, the Playwright driver + investigation/, which stay waived permanently
- the Universal Screen Engine replaces that role). Evidence below is real: dryrun/live counts and
the DB query are from a fresh run in this session (2026-08-27); items already covered by PR #533's
merged body are cited as such._

## Step 0 - check-existing gate
- [x] **0a.** Read `ec-ui-knowledge/screens/operator_route.md` (existed; refreshed in this session
      to match the current post-PR#533 RF shape, not re-scanned from scratch).
- [x] **0b.** `grep -ril "operator_route" workstreams/master-plan/ec-automation/{py,pageobjects,tests,screens}`
      -> existing impl found: `py/operator_route_iud.py`, `pageobjects/.../operator_route_page.resource`,
      `tests/.../operator_route_iud.robot`, `screens/.../Operator_Route/`. This task is a
      documentation/evidence backfill around that existing, already-merged automation - no parallel
      copy created.
- [x] **0c.** Shared engine reused throughout (`ec_object_iud.py` for Playwright, `manage_object.resource`
      T2 + `Apply Navigator From Properties` for RF) - unchanged.

## A. Bundle artifacts - `screens/Configuration/Assets/Facility_Objects/Operator_Route/`
- [x] **1. `operator_route_sow.md`** - classification, nav/grid/cell shape, test data, dev story
      pulled from PR #533's real merged body + `docs/ec_screen_registry.md`'s Operator Route row.
      Refreshed 2026-08-27.
- [x] **2. `README.md`** - bundle overview + exact run commands (dryrun/live headless/live headed)
      + the DB self-clean query pattern. Refreshed 2026-08-27.
- [x] **3. `JOURNAL.md`** - Built/Done well/Done wrong-or-lessons/Blockers->resolution/Decisions/
      Evidence, modeled on `screens/Configuration/Assets/Financial_Objects/Bank/JOURNAL.md`.
      Refreshed 2026-08-27 with real content from PR #533's body + the 2026-08-01 base build.
- [ ] **4. Playwright driver** - N/A. Playwright bundle waived, owner decision 2026-08-27 (Section H
      of `docs/IUD-DELIVERABLE-CHECKLIST.md`) - the Universal Screen Engine is the owner-decided
      replacement for hand-written Playwright drivers going forward. `py/operator_route_iud.py`
      still exists from the 2026-08-01 base build and was left untouched.
- [ ] **5. `investigation/`** - N/A, same waiver as item 4. `investigation/recon.py` from the
      2026-08-01 base build is kept as-is (not a required deliverable going forward).
- [x] **6. `evidence/`** - `results.json` + screenshots from the 2026-08-01 base build (Playwright
      8/8), PLUS `evidence/rf_2026-08-27/` (log.html, report.html, output.xml, 23 per-TC
      screenshots, results.json) from this backfill's one-time live RF re-run (5/5) of the
      already-proven, already-merged suite - captured 2026-08-27.
- [x] **7. `CHECKLIST.md`** - this file, copied from `docs/IUD-DELIVERABLE-CHECKLIST.md` and ticked
      with real evidence.

## B. RF files - treeview-mirrored (unchanged, pre-existing, merged in PR #533)
- [x] **8.** T3 `pageobjects/Configuration/Assets/Facility_Objects/operator_route_page.resource`
      (properties-driven, label-driven, no hardcoded ids - existing, not modified this session).
- [x] **9.** Suite `tests/Configuration/Assets/Facility_Objects/operator_route_iud.robot` - 5 TCs
      (Verify Clean State -> Insert -> Update -> Find -> Delete) - existing, not modified this
      session.

## C. Verification gates (real evidence, re-run 2026-08-27 in an isolated worktree off origin/master)
- [x] **10. robocop clean (parity).** `robocop check pageobjects/.../operator_route_page.resource
      tests/.../operator_route_iud.robot` -> **7 issues found** (5x DOC02 missing-TC-documentation
      + 2x VAR02), matching PR #533's own cited parity vs Area's/Facility Class 1's reference-
      pattern files exactly - not a defect, the accepted house style for this pattern.
- [x] **11. `--dryrun` N/N PASS.** `robot --dryrun tests/Configuration/Assets/Facility_Objects/
      operator_route_iud.robot` -> **5 tests, 5 passed, 0 failed**. Full-tree
      `robot --dryrun tests/` -> **883 tests, 883 passed, 0 failed** (zero collisions with any
      other screen's suite).
- [x] **12. LIVE headless run N/N PASS.** `EC_HEADLESS=true robot --outputdir C:/tmp/or_live
      tests/Configuration/Assets/Facility_Objects/operator_route_iud.robot` -> **5 tests, 5 passed,
      0 failed** (TC01 Verify Clean State, TC02 Insert, TC03 Update, TC04 Find, TC05 Delete), local
      EC sandbox (`localhost:1521/ORCL`), 2026-08-27.
- [x] **13. DB ground-truth.** Fresh `oracledb` connection (`ECKERNEL_EC`/`localhost:1521/ORCL`),
      independent of the suite's own session:
      `SELECT COUNT(*) FROM OV_OPERATOR_ROUTE WHERE CODE LIKE 'AUTOTEST%'` -> **`(0,)` BEFORE** the
      2026-08-27 live run and **`(0,)` AFTER** it. In-suite DB assertion lives in the shared T2
      `Verify Object Removed` (TC05) against `OV_OPERATOR_ROUTE`.
- [x] **14. FULL I-U-D scope.** Insert (TC02) + Update (TC03) + Find (TC04) + Delete (TC05) all
      present and all passed live.
- [x] **15. Self-clean confirmed.** Independent fresh-connection DB re-read = 0 residual
      `AUTOTEST%` rows in `OV_OPERATOR_ROUTE` after the live run (see item 13).
- [x] **16. Hygiene PASS.** `py scripts/check_bundle_hygiene.py` run from repo root, 2026-08-27:
      `[hygiene] scanned 167 bundle(s) + 271 recon script(s)` ... `[hygiene] RESULT: PASS - no
      hardcoded creds (R16), pure ASCII (R20), no CHECKLIST/VERIFY-REPORT contradictions, doc rows
      match declared families` (one pre-existing, unrelated WARN on
      `Contract_Area/investigation/live_recon_contract_area.py` - not this screen).

## D. Delivery
- [x] **17. Registry row** - already present, appended by PR #533 (`docs/ec_screen_registry.md`,
      Operator Route row, MODIFIED not re-appended since it's the same screen's row being updated
      in place per that PR's own diff).
- [x] **18. Scorecard row** - already present, appended/modified by PR #533
      (`docs/automation-scorecard.md`).
- [ ] **19. PR** - this backfill's own PR, standard 6-field body, base branch master, never
      self-merge. Tick lives in the PR itself, not hand-typed here (lesson from PR #235).

## E. Knowledge base
- [x] **20. KB selector map** `ec-ui-knowledge/screens/operator_route.md` - refreshed 2026-08-27:
      nav path, DB view, grid id, insert/update/delete selectors, mandatory-yellow fields, quirks,
      last-verified date, now describing the 5-TC/fixed-code/filter-wired post-PR#533 shape (was
      previously stale, still describing the 2026-08-01 4-TC/generated-code shape).
- [x] **21. Reuse clause.** Step 0 found the screen ALREADY implemented and already fully bundled
      (from the 2026-08-01 base build) - but that bundle's docs were stale vs the 2026-08-26
      conversion. This backfill refreshed JOURNAL (#3), evidence (#6), and the KB map (#20) to
      match, per the reuse clause's requirement that "done" means tests + KB MD + JOURNAL +
      evidence, never just passing tests.

_Items 4/5 stay N/A per Section H's permanent waiver (Playwright bundle superseded by the Universal
Screen Engine). All other items are ticked against real, cited evidence from this session or from
PR #533's real merged body - no item is ticked from memory or assumption._
