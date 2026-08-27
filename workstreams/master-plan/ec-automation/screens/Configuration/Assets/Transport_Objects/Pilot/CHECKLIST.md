# IUD Task - Deliverable Checklist - Pilot (CO.2079)

_Copied from `docs/IUD-DELIVERABLE-CHECKLIST.md`. This is a **documentation/evidence backfill**
(`docs/lean-deliverable-backfill-workorder.md`, owner decision 2026-08-27, Section H, Batch 5)
around already-merged, already-live-tested RF automation (PR #560, merged 2026-08-26). No RF file
(`pilot_page.resource`, `pilot_iud.robot`, `testdata/pilot_*.properties`) was modified to produce
this checklist. Items 4/5 (Playwright driver + investigation/) stay permanently waived per
Section H - the pre-existing Playwright bundle from the screen's original 2026-07-31 build is kept
in this bundle unchanged, not rebuilt. Supersedes this bundle's earlier (2026-07-31) CHECKLIST.md,
which predated PR #560's Area-pattern conversion._

## Step 0. CHECK-EXISTING-FIRST GATE
- [x] **0a.** `ec-ui-knowledge/screens/pilot.md` existed before this backfill but described the
      PRE-#560 4-TC structure (stale) - refreshed in this backfill (see item 20). Selectors
      transcribed from `pilot_page.resource`'s own Variables/Documentation section, not re-scanned
      live.
- [x] **0b.** `grep -rn "pilot_page.resource" workstreams/master-plan/ec-automation` -> existing
      impl found: `pageobjects/Configuration/Assets/Transport_Objects/pilot_page.resource`,
      `tests/Configuration/Assets/Transport_Objects/pilot_iud.robot`,
      `testdata/pilot_{navigator,insert,update,form_verify,grid_verify}.properties`,
      `screens/Configuration/Assets/Transport_Objects/Pilot/` (SOW/README/JOURNAL/CHECKLIST/
      VERIFY-REPORT/investigation/evidence pre-existed from the 2026-07-31 build). REUSED/EXTENDED -
      no parallel copy built.
- [x] **0c.** Shared engine reused: RF suite calls the shared T2 `resources/manage_object.resource`
      (`Insert/Update/Verify Object *`, `Apply Navigator From Properties`, `Find/Clear Object Row By
      Filter`) + `libraries/DbVerify.py` for this backfill's own evidence-capture DB read. No new
      plumbing added.

## A. Bundle artifacts - `screens/Configuration/Assets/Transport_Objects/Pilot/`
- [x] **1. `pilot_sow.md`** - updated (2026-08-28 addendum) with the current classification,
      current nav/grid/cell shape, the Op Production Unit `__FIRST__` exception, and the dev story
      pulled from PR #560's real body.
- [x] **2. `README.md`** - updated with the bundle overview + exact run commands
      (dryrun/live/DB self-clean pattern) reflecting the current 5-TC shape.
- [x] **3. `JOURNAL.md`** - appended: PR #560's own Built/Done well/Decisions/Blockers section
      (pulled from `gh pr view 560`'s body) + this backfill session's own Built/Done well/Done
      wrong-or-lessons/Blockers->resolution/Decisions/Evidence.
- [ ] **4. Playwright driver** - N/A. Playwright bundle waived, owner decision 2026-08-27
      (Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md`); the pre-existing `py/pilot_iud.py` from
      the 2026-07-31 build is kept unchanged, not rebuilt.
- [ ] **5. `investigation/`** - N/A, same waiver as item 4; the pre-existing `investigation/
      recon.py` from the 2026-07-31 build is kept unchanged.
- [x] **6. `evidence/`** - captured in this session: `log.html`, `output.xml`, `report.html` from a
      live 5/5 RF run (2026-08-28), alongside the pre-existing 2026-07-31 Playwright evidence
      (`pl_0[1-5]_*.png`, `results.json` - unchanged).
- [x] **7. `CHECKLIST.md`** - this file (supersedes the 2026-07-31 pre-#560 version).

## B. RF files - treeview-mirrored (pre-existing, unmodified by this backfill)
- [x] **8. T3 page object**
      `pageobjects/Configuration/Assets/Transport_Objects/pilot_page.resource` - pre-existing,
      converted in PR #560 (2026-08-26), not touched by this backfill.
- [x] **9. Suite** `tests/Configuration/Assets/Transport_Objects/pilot_iud.robot` - pre-existing,
      converted in PR #560, not touched by this backfill.

## C. Verification gates (re-run for evidence, not re-verification of a defect)
- [x] **10. robocop clean** - `py -m robocop check
      pageobjects/Configuration/Assets/Transport_Objects/pilot_page.resource
      tests/Configuration/Assets/Transport_Objects/pilot_iud.robot` (this session, 2026-08-28) ->
      **7 issues** (DOC02 missing TC-level `[Documentation]`) - matches PR #560's own cited
      7-issue baseline exactly. No drift, no new issue category.
- [x] **11. `--dryrun` N/N PASS** - `robot --dryrun
      tests/Configuration/Assets/Transport_Objects/pilot_iud.robot` (this session) -> **5/5 PASS**.
- [x] **12. LIVE headless run N/N PASS** - `EC_HEADLESS=true robot
      tests/Configuration/Assets/Transport_Objects/pilot_iud.robot` (this session, isolated
      worktree `C:/tmp/wt-pilot-backfill`) -> **5/5 PASS on the first attempt** - no retry needed,
      no regression from PR #560.
- [x] **13. DB ground-truth** - `libraries.DbVerify.fetch_object("OV_PILOT", "AUTOTEST_PILOT")` ->
      `None` (absent) verified via a fresh oracledb connection after the live run this session
      (script: `Workplaces/pilot-backfill/db_selfclean_check.py`).
- [x] **14. FULL I-U-D scope** - TC02 Insert / TC03 Update / TC05 Delete all present and passing
      (plus TC01 Clean State, TC04 Find) - confirmed by reading `pilot_iud.robot`'s 5 test cases and
      the live 5/5 run.
- [x] **15. Self-clean confirmed** - independent DB re-read (fresh connection, this session) = 0
      residual `AUTOTEST_PILOT` rows in `OV_PILOT` after the live run.
- [x] **16. Hygiene PASS** - `py scripts/check_bundle_hygiene.py` (repo root, this session) ->
      `[hygiene] RESULT: PASS - no hardcoded creds (R16), pure ASCII (R20), no CHECKLIST/
      VERIFY-REPORT contradictions, doc rows match declared families` (167 bundles + 272 recon
      scripts scanned; the one pre-existing WARN is on an unrelated screen's recon script, not
      Pilot's).

## D. Delivery
- [ ] **17. Registry row** - N/A for this backfill. Pilot's row in
      `workstreams/master-plan/ec-automation/docs/ec_screen_registry.md` already exists and already
      documents the PR #560 conversion in full (navigator shape, `__FIRST__` exception, evidence) -
      append-only edit made at PR #560's merge time, not this backfill.
- [ ] **18. Scorecard row** - N/A for this backfill, same reasoning as item 17.
- [x] **19. PR** - this backfill's own PR, with the standard body (What was backfilled / Files
      added / Base branch = master); never self-merged.

## E. Knowledge base
- [x] **20. KB selector map** `ec-ui-knowledge/screens/pilot.md` - refreshed in this backfill (was
      stale, describing the pre-#560 4-TC/in-suite-DB-verify shape): nav path, DB view, grid id,
      insert/update/delete selectors (transcribed from `pilot_page.resource`'s own Variables
      section), the Op Production Unit `__FIRST__` exception, mandatory-yellow fields, quirks,
      last-verified date 2026-08-28.
- [x] **21. Reuse clause.** Step 0 found Pilot's RF automation ALREADY implemented, converted, and
      merged (PR #560) - this backfill produces exactly the deliverables the reuse clause requires:
      #3 JOURNAL, #6 evidence, #20 KB map (plus #1/#2/#7 restored per Section H).
