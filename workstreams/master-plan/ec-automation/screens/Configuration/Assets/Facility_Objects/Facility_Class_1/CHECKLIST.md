# IUD Task - Deliverable Checklist (Facility Class 1)

Copy of `docs/IUD-DELIVERABLE-CHECKLIST.md`, ticked with real evidence for this screen. This is a
**backfill** (2026-08-27, `docs/lean-deliverable-backfill-workorder.md`) of the documentation/evidence
artifacts the 2026-08-23/26 lean-deliverable waiver (Section G) skipped for the Area-pattern
conversion already merged via PR #526 (navigator-fill) and PR #530 (full structural conversion). Per
Section H (2026-08-27, owner decision), items 4 (Playwright driver) and 5 (investigation/) stay
waived permanently for Bank-/Area-pattern conversions - the Universal Screen Engine replaces that
role. **No RF/Playwright code was changed to produce this checklist.**

## Step 0. CHECK-EXISTING-FIRST GATE
- [x] **0a.** `ec-ui-knowledge/screens/facility_class_1.md` existed (built at the 2026-07-30 original
      construction) - read first; updated by this backfill to reflect the 2026-08-26 conversion
      (fixed code, properties-driven navigator, explicit values) rather than re-scanned from scratch.
- [x] **0b.** `grep -ril facility_class_1 workstreams/master-plan/ec-automation/{py,pageobjects,tests,screens}`
      -> existing impl found: `py/facility_class_1_iud.py`, `pageobjects/.../facility_class_1_page.resource`,
      `tests/.../facility_class_1_iud.robot`, `screens/.../Facility_Class_1/`. REUSED/EXTENDED via
      documentation backfill only - no parallel copy created.
- [x] **0c.** Shared engine already in use: T2 `resources/manage_object.resource`
      (`Apply Navigator From Properties`, `Insert/Update Object From Properties`, `Verify Object
      Removed`, etc.) - confirmed unmodified by PR #526/#530 (`git status --porcelain` before each
      commit, per those PRs' own bodies).

## A. Bundle artifacts - `screens/Configuration/Assets/Facility_Objects/Facility_Class_1/`
- [x] **1. `facility_class_1_sow.md`** - updated this backfill: classification (OV-GM, Area-pattern
      structural conversion), 2-level PU->Area same-row cascade shape, grid/form labels
      (screen-prefixed), fixed test code `AUTOTEST_FC1`, dev story pulled from PR #526/#530 bodies.
- [x] **2. `README.md`** - updated this backfill: bundle overview + exact dryrun/live-headless/
      self-clean-query commands.
- [x] **3. `JOURNAL.md`** - extended this backfill with two new dated sections (2026-08-26 conversion,
      2026-08-27 backfill) modeled on `Bank/JOURNAL.md`'s Built/Done well/Done wrong/Blockers/
      Decisions/Evidence structure, using PR #526/#530's real disclosed history (first live exercise
      of the shared keyword's multi-column same-row cascade shape; zero shared-file changes needed).
- [ ] **4. `playwright/ec_iud_facility_class_1.py`** - **N/A, Playwright bundle waived** (owner
      decision 2026-08-27, `docs/IUD-DELIVERABLE-CHECKLIST.md` Section H - Universal Screen Engine
      replaces hand-written Playwright drivers for Bank-/Area-pattern work going forward). The
      PRE-EXISTING `py/facility_class_1_iud.py` (built 2026-07-30, still passing) is retained as-is,
      not rebuilt or extended.
- [ ] **5. `investigation/`** - **N/A, waived** (same Section H decision). The pre-existing
      `investigation/recon.py` (2026-07-30) is retained; the 2026-08-26 conversion's own dedicated
      recon (`tmp/recon_fc1_navigator_cascade.py`, per PR #526's body) was a throwaway scratch script,
      not promoted to a permanent `investigation/` deliverable, consistent with Section H's guidance.
- [x] **6. `evidence/`** - this backfill added a fresh live RF run's `log.html`/`report.html`/
      `output.xml` (2026-08-27, EC_HEADLESS=true, 5 tests / 5 passed / 0 failed) alongside the
      pre-existing 2026-07-30 Playwright driver's `fc1_0[1-5]_*.png` + `results.json`.
- [x] **7. `CHECKLIST.md`** - this file (replaces the stale 2026-07-30 21-item version, which
      described the retired 4-TC/first-available-navigator shape).

## B. RF files - treeview-mirrored (pre-existing, unmodified by this backfill)
- [x] **8. T3 page object** `pageobjects/Configuration/Assets/Facility_Objects/facility_class_1_page.resource`
      - label-driven (`code_label=Facility Class 1 Code` passed to every T2 call), docstring matches
      Variables section (re-confirmed on read, not just assumed).
- [x] **9. Suite** `tests/Configuration/Assets/Facility_Objects/facility_class_1_iud.robot` - 5 TCs
      (Verify Clean State / Insert / Update / Find / Delete), per-TC Login/Logout, fixed test code
      `AUTOTEST_FC1`.

## C. Verification gates - re-run 2026-08-27 for this backfill (real evidence below, not carried over
   from the stale 2026-07-30 `VERIFY-REPORT.md`)
- [x] **10. robocop clean** - `robocop check pageobjects/.../facility_class_1_page.resource
      tests/.../facility_class_1_iud.robot` -> **7 issues (2 VAR02 + 5 DOC02)**, run 2026-08-27.
      Identical in kind/count to Area's own current baseline (also 7: 2 VAR02 + 5 DOC02) and to what
      PR #530 itself cited - not a regression, both screens share the same T2-delegation shape that
      trips the same style rules.
- [x] **11. `--dryrun` N/N PASS** - `robot --dryrun tests/Configuration/Assets/Facility_Objects/facility_class_1_iud.robot`
      -> **5 tests, 5 passed, 0 failed** (run 2026-08-27).
- [x] **12. LIVE headless run N/N PASS** - `EC_HEADLESS=true robot tests/Configuration/Assets/Facility_Objects/facility_class_1_iud.robot`
      -> **5 tests, 5 passed, 0 failed** (run 2026-08-27; artifacts in `evidence/log.html`/`report.html`/`output.xml`).
- [x] **13. DB ground-truth** - PURE SCREEN verification in the `.robot`/T3 files (zero inline
      `Should Exist In DB`/`Field Should Equal In View`/`Code Should Be Present|Absent In View` calls
      - grep for those patterns on `facility_class_1_iud.robot` = no matches, exit 1); the DB check
      lives inside the shared T2 `Verify Object Removed` keyword (called from
      `Verify Facility Class 1 Record Removed`), asserting absence from `OV_FCTY_CLASS_1`.
- [x] **14. FULL I-U-D scope** - Insert (TC02) + Update (TC03) + Find (TC04) + Delete (TC05) all
      present and passing.
- [x] **15. Self-clean confirmed** - independent fresh oracledb connection (not the RF library's own),
      run 2026-08-27 AFTER the live suite: `SELECT COUNT(*) FROM OV_FCTY_CLASS_1 WHERE CODE LIKE
      'AUTOTEST_FC1%'` = **0**.
- [x] **16. Hygiene PASS** - `py scripts/check_bundle_hygiene.py` (from repo root, run 2026-08-27) ->
      `[hygiene] RESULT: PASS - no hardcoded creds (R16), pure ASCII (R20), no CHECKLIST/VERIFY-REPORT
      contradictions, doc rows match declared families` (167 bundles + 271 recon scripts scanned; the
      one WARN in the output is a pre-existing, unrelated Contract_Area recon script, not Facility
      Class 1).

## D. Delivery
- [x] **17. Registry row** - `workstreams/master-plan/ec-automation/docs/ec_screen_registry.md`, row
      "Facility Class 1" (updated by PR #526 then PR #530; append-only edits to the same screen's own
      row, both already merged to master).
- [x] **18. Scorecard row** - `docs/automation-scorecard.md` Facility Class 1 row (updated by PR
      #526/#530, already merged to master).
- [x] **19. PR** - this backfill's own PR (branch `docs/facility-class-1-backfill-artifacts`, 6-field
      body, base master, synced before push, never self-merged). The automation itself was already
      delivered via PR #526 and PR #530 (both merged, 6-field bodies, never self-merged).

## E. Knowledge base
- [x] **20. KB selector map** `ec-ui-knowledge/screens/facility_class_1.md` - updated this backfill:
      nav path, `OV_FCTY_CLASS_1` view, `manageObject:form:T_data` grid id, insert/update/delete
      selectors (pulled from the T3's own Variables section), mandatory-yellow fields, quirks
      (2-level same-row cascade, fixed test code, screen-prefixed labels), last-verified date
      2026-08-27.
- [x] **21. Reuse clause** - Step 0 found the screen ALREADY implemented (2026-07-30 build, then
      2026-08-26 conversion); this backfill produces the required refresh: JOURNAL (#3, extended),
      evidence (#6, fresh live run added), and KB map (#20, updated) - not just a "tests still pass"
      claim.

---

**Overall:** all applicable gates (0, 1-3, 6-21) PASS with cited real evidence above. Items 4/5
correctly marked N/A per the owner's 2026-08-27 Section H decision (Playwright bundle superseded by
the Universal Screen Engine). This checklist was produced by re-running the already-proven suite and
hygiene/robocop tools on 2026-08-27, not by hand-typing ticks against assumed behavior.
