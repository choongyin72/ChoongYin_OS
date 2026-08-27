# IUD Task - Deliverable Checklist - Chemical Injection Point (CO.0212)

_Copied from `docs/IUD-DELIVERABLE-CHECKLIST.md`. This is a **documentation/evidence backfill**
(`docs/lean-deliverable-backfill-workorder.md`, Batch 2, owner decision 2026-08-27, Section H)
around already-merged, already-live-tested RF automation (PR #550, merged 2026-08-26). No RF file
(`chem_injection_point_page.resource`, `chem_injection_point_iud.robot`,
`testdata/chem_injection_point_*.properties`) was modified to produce this checklist. Items 4/5
(Playwright driver + investigation/) stay permanently waived per Section H - a pre-existing
Playwright bundle from the screen's original 2026-07-30 build is kept in this bundle unchanged, not
rebuilt._

## Step 0. CHECK-EXISTING-FIRST GATE
- [x] **0a.** `ec-ui-knowledge/screens/chem_injection_point.md` already existed (from the
      2026-07-30 build) - refreshed in this PR to reflect PR #550's conversion (5-TC structure,
      `__FIRST__` gotcha, current selectors). Not re-scanned live - transcribed from
      `chem_injection_point_page.resource`'s own Variables section.
- [x] **0b.** `grep -ril "chemical_injection_point" workstreams/master-plan/ec-automation/{py,pageobjects,tests,screens}`
      -> existing impl found: `pageobjects/Configuration/Assets/Chemical_Objects/
      chem_injection_point_page.resource`, `tests/Configuration/Assets/Chemical_Objects/
      chem_injection_point_iud.robot`, `screens/Configuration/Assets/Chemical_Objects/
      Chemical_Injection_Point/` (SOW/README/CHECKLIST/VERIFY-REPORT/evidence/investigation
      pre-existed from the 2026-07-30 build). REUSED/EXTENDED - no parallel copy built.
- [x] **0c.** Shared engine reused: RF suite calls the shared T2 `resources/manage_object.resource`
      (`Insert/Update/Verify Object *`, `Apply Navigator From Properties`) +
      `libraries/DbVerify.py` for this backfill's own evidence-capture DB reads. No new plumbing
      added.

## A. Bundle artifacts - `screens/Configuration/Assets/Chemical_Objects/Chemical_Injection_Point/`
- [x] **1. `chem_injection_point_sow.md`** - updated (Section 6/7 addendum) with classification,
      current nav/grid/cell shape, test data, and the dev story pulled from PR #550's real body,
      including the Op Production Unit / `__FIRST__` gotcha.
- [x] **2. `README.md`** - updated with the bundle overview + exact run commands
      (dryrun/live/DB self-clean pattern).
- [x] **3. `JOURNAL.md`** - extended: Built/Done well/Done wrong-or-lessons/Blockers->resolution/
      Decisions/Evidence for both the 2026-08-26 PR #550 conversion and this 2026-08-27 backfill
      session, pulled from PR #550's real body + this session's own live-run evidence.
- [ ] **4. Playwright driver** - N/A. Playwright bundle waived, owner decision 2026-08-27
      (Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md`); the pre-existing
      `py/chem_injection_point_iud.py` from the 2026-07-30 build is kept unchanged, not rebuilt.
- [ ] **5. `investigation/`** - N/A, same waiver as item 4; the pre-existing
      `investigation/recon.py` from the 2026-07-30 build is kept unchanged.
- [x] **6. `evidence/`** - captured in this session: `log.html`, `output.xml`, `report.html` from a
      live 5/5 RF run (2026-08-27), alongside the pre-existing 2026-07-30 Playwright evidence
      (`cip_0[1-5]_*.png`, `results.json`, unchanged).
- [x] **7. `CHECKLIST.md`** - this file.

## B. RF files - treeview-mirrored (pre-existing, unmodified by this backfill)
- [x] **8. T3 page object**
      `pageobjects/Configuration/Assets/Chemical_Objects/chem_injection_point_page.resource` -
      pre-existing, merged in PR #550, not touched by this backfill.
- [x] **9. Suite**
      `tests/Configuration/Assets/Chemical_Objects/chem_injection_point_iud.robot` - pre-existing,
      merged in PR #550, not touched by this backfill.

## C. Verification gates (re-run for evidence, not re-verification of a defect)
- [x] **10. robocop clean** - `py -m robocop check
      pageobjects/Configuration/Assets/Chemical_Objects/chem_injection_point_page.resource
      tests/Configuration/Assets/Chemical_Objects/chem_injection_point_iud.robot`
      (this session, 2026-08-27) -> **7 issues** (DOC02 missing TC/keyword docs) - matches PR
      #550's own cited "5 DOC02, same shape as Area/Facility Class 1" baseline; no drift, no new
      issue category.
- [x] **11. `--dryrun` N/N PASS** - `robot --dryrun tests/Configuration/Assets/Chemical_Objects/
      chem_injection_point_iud.robot` (this session) -> **5/5 PASS**.
- [x] **12. LIVE headless run N/N PASS** - `EC_HEADLESS=true robot --outputdir
      screens/Configuration/Assets/Chemical_Objects/Chemical_Injection_Point/evidence
      tests/Configuration/Assets/Chemical_Objects/chem_injection_point_iud.robot`
      (this session, 2026-08-27) -> **5/5 PASS** clean, single run, no flake.
- [x] **13. DB ground-truth** - `libraries.DbVerify.fetch_object("OV_CHEM_INJ_POINT",
      "AUTOTEST_CIP")` -> `None` (absent) verified via a fresh oracledb connection after the live
      run in this session.
- [x] **14. FULL I-U-D scope** - TC02 Insert / TC03 Update / TC05 Delete all present and passing
      (plus TC01 Clean State, TC04 Find) - confirmed by reading
      `chem_injection_point_iud.robot`'s 5 test cases.
- [x] **15. Self-clean confirmed** - independent DB re-read (fresh connection, this session) = 0
      residual `AUTOTEST_CIP` rows in `OV_CHEM_INJ_POINT` after the run.
- [x] **16. Hygiene PASS** - `py scripts/check_bundle_hygiene.py` (repo root, this session) ->
      `[hygiene] RESULT: PASS - no hardcoded creds (R16), pure ASCII (R20), no CHECKLIST/
      VERIFY-REPORT contradictions, doc rows match declared families` (167 bundles + 271 recon
      scripts scanned; one pre-existing, unrelated WARN on Contract Area's own recon script).

## D. Delivery
- [ ] **17. Registry row** - N/A for this backfill. Chemical Injection Point's row in
      `workstreams/master-plan/ec-automation/docs/ec_screen_registry.md` already exists and
      already documents PR #550's conversion (append-only edit made at merge time of that PR, not
      this backfill).
- [ ] **18. Scorecard row** - N/A for this backfill, same reasoning as item 17 -
      `docs/automation-scorecard.md`'s Chemical Injection Point row already reflects the merged
      conversion.
- [x] **19. PR** - this backfill's own PR, with the standard body (What was backfilled / Files
      added / Base branch = master); never self-merged.

## E. Knowledge base
- [x] **20. KB selector map** `ec-ui-knowledge/screens/chem_injection_point.md` - refreshed in this
      backfill (pre-existed from the 2026-07-30 build, now updated): nav path, DB view, grid id,
      insert/update/delete selectors (transcribed from `chem_injection_point_page.resource`'s own
      Variables section), mandatory-yellow fields, the Op Production Unit `__FIRST__` quirk,
      last-verified date 2026-08-27.
- [x] **21. Reuse clause.** Step 0 found Chemical Injection Point's RF automation ALREADY
      implemented and merged - this backfill produces exactly the deliverables the reuse clause
      requires: #3 JOURNAL, #6 evidence, #20 KB map (plus #1/#2/#7 restored per Section H).
