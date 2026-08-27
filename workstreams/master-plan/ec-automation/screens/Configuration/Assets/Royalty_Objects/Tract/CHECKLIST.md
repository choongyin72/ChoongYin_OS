# IUD Task - Deliverable Checklist - Tract

Copied from `docs/IUD-DELIVERABLE-CHECKLIST.md` (Section H restored requirements). This is a
**backfill** (`docs/lean-deliverable-backfill-workorder.md`, Batch 4) - Tract's RF suite was
already converted to the Area pattern and merged via PR #555 (2026-08-26); this checklist
documents the retroactive documentation/evidence bundle added 2026-08-28, plus a fresh
dryrun+live evidence-capture re-run of the already-proven suite. **No automation code was
rebuilt, modified, or re-verified from scratch.**

---

## Step 0. CHECK-EXISTING-FIRST GATE
- [x] **0a.** `ec-ui-knowledge/screens/tract.md` did NOT already exist - created fresh this
      backfill (transcribed from `tract_page.resource`'s own Variables/Documentation section, not
      re-scanned live).
- [x] **0b.** `grep -ril "tract" workstreams/master-plan/ec-automation/{py,pageobjects,tests,
      screens,testdata}` -> found existing impl at
      `pageobjects/Configuration/Assets/Royalty_Objects/tract_page.resource`,
      `tests/Configuration/Assets/Royalty_Objects/tract_iud.robot`,
      `testdata/tract_{navigator,insert,update,form_verify,grid_verify}.properties`, and a
      pre-existing `screens/.../Tract/` bundle (sow.md/README/evidence from the original
      2026-06-26 build) - REUSED/EXTENDED, no parallel copy built.
- [x] **0c.** Shared T2 `resources/manage_object.resource` reused as-is (PR #555 needed only the
      `Apply Navigator From Properties` keyword's new optional `${group}`/`${start_col}` args,
      already added 2026-08-26) - not modified by this backfill either.

## A. Bundle artifacts - `screens/Configuration/Assets/Royalty_Objects/Tract/`
- [x] **1. `tract_sow.md`** - updated (not replaced): classification/nav/grid/cell shape corrected
      (Date at G:0 already defaulted, Unit Agreement at G:1:C:0 the only mandatory-and-empty nav
      field) and a "Dev story" section added with the real PR #555 wrong-then-corrected narrative
      and the shared-keyword extension.
- [x] **2. `README.md`** - updated with exact RF commands (dryrun/live headless/live headed) and
      the `OV_TRACT` DB self-clean query pattern; the wrong-then-corrected classification story
      called out under "Key facts".
- [x] **3. `JOURNAL.md`** - created (did not exist before). Built/Done well/Done wrong-or-lessons/
      Blockers->resolution/Decisions/Evidence, modeled on
      `screens/Configuration/Assets/Financial_Objects/Bank/JOURNAL.md`, content pulled from PR
      #555's real body. The wrong-then-corrected classification and the field-reuse rule
      application are given prominent, honest treatment in "Done wrong / lessons", per this
      backfill's explicit instruction.
- [ ] **4. `playwright/ec_iud_tract.py`** - N/A. Tract never had a Playwright bundle (RF-only since
      the original 2026-06-26 build, per the OV-GM exemplar precedent - Transport System). Also
      permanently waived regardless by owner decision 2026-08-27
      (`docs/IUD-DELIVERABLE-CHECKLIST.md` Section H).
- [ ] **5. `investigation/`** - N/A, same reason as #4 - never existed, permanently waived.
- [x] **6. `evidence/`** - pre-existing screenshots (`tract_tc0[1-4]_*.png`, 2026-06-26) kept
      unchanged; NEW `evidence/backfill_2026-08-28/` added with a fresh dryrun
      (`dryrun/log.html`+`report.html`+`output.xml`) and live headless run
      (`live/log.html`+`report.html`+`output.xml`) of the ALREADY-PROVEN Area-pattern suite.
- [x] **7. `CHECKLIST.md`** - this file.

## B. RF files - treeview-mirrored (NOT modified by this backfill)
- [x] **8. T3 page object**
      `pageobjects/Configuration/Assets/Royalty_Objects/tract_page.resource` - already exists
      (PR #555), unmodified by this backfill; reviewed only for the KB map's transcription.
- [x] **9. Suite** `tests/Configuration/Assets/Royalty_Objects/tract_iud.robot` - already exists
      (PR #555), unmodified by this backfill; TC01 clean -> TC02 insert -> TC03 update -> TC04
      find -> TC05 delete/cleanup, confirmed by re-running it (not by reading alone).

## C. Verification gates (real re-run evidence, 2026-08-28)
- [x] **10. robocop clean (parity with Area)** - `py -m robocop check
      pageobjects/.../tract_page.resource tests/.../tract_iud.robot` (2026-08-28, this session)
      -> **7 issues** (DOC02 missing test-case documentation across TC01-TC05 + VAR02). Cross-
      checked `py -m robocop check pageobjects/Configuration/Assets/Basic_Objects/area_page.
      resource tests/Configuration/Assets/Basic_Objects/area_iud.robot` (the Area-pattern role
      model) -> **also 7 issues**, same DOC02/VAR02 pattern. Tract's robocop output is at parity
      with Area's own established baseline, not a new/worse defect - no fix applied, per this
      task's explicit "do not modify the RF automation" scope.
- [x] **11. `--dryrun` N/N PASS** - `py -m robot --dryrun --outputdir
      evidence/backfill_2026-08-28/dryrun tests/Configuration/Assets/Royalty_Objects/
      tract_iud.robot` -> **5 tests, 5 passed, 0 failed** (2026-08-28, this session; log/report/
      output archived in `evidence/backfill_2026-08-28/dryrun/`).
- [x] **12. LIVE headless run N/N PASS** - `EC_HEADLESS=true py -m robot --outputdir
      evidence/backfill_2026-08-28/live tests/Configuration/Assets/Royalty_Objects/
      tract_iud.robot` -> **5 tests, 5 passed, 0 failed** (TC01-TC05 all PASS, first attempt, no
      retry needed, 2026-08-28, this session; archived in `evidence/backfill_2026-08-28/live/`).
- [x] **13. DB ground-truth** - fresh oracledb connection, 2026-08-28, this session, post-run:
      `SELECT COUNT(*) FROM OV_TRACT WHERE CODE = 'AUTOTEST_TRACT'` -> `0`;
      `SELECT CODE FROM OV_TRACT WHERE CODE LIKE 'AUTOTEST%'` -> no rows. Confirms the suite's own
      TC02/TC03/TC05 insert/update/delete cycle against `OV_TRACT` completed cleanly.
- [x] **14. FULL I-U-D scope** - TC02 Insert + TC03 Update + TC05 Delete all present and PASS (see
      item 12); TC04 Find also present (Area-pattern's 5th TC).
- [x] **15. Self-clean confirmed** - independent fresh-connection re-read (item 13) = 0 residual
      `AUTOTEST_TRACT` / `AUTOTEST%` rows in `OV_TRACT` after the live run.
- [x] **16. Hygiene PASS** - `py scripts/check_bundle_hygiene.py` (run from repo root, 2026-08-28,
      this session) -> `RESULT: PASS - no hardcoded creds (R16), pure ASCII (R20), no
      CHECKLIST/VERIFY-REPORT contradictions, doc rows match declared families` (one unrelated
      pre-existing WARN about a Contract Area `investigation/` selector-string false positive, not
      related to Tract).

## D. Delivery
- [x] **17. Registry row** - already present, MODIFIED IN PLACE by PR #555 (not this backfill);
      confirmed live: `docs/ec_screen_registry.md` line 115, records both the wrong conclusion and
      its correction. This backfill does not touch the registry row again (append-only / no-
      duplicate-edit).
- [x] **18. Scorecard row** - pre-existing from the original build / PR #555
      (`docs/automation-scorecard.md` line 62, Royalty Objects section); not duplicated by this
      backfill (documentation-only task, no new automation scope to score).
- [ ] **19. PR** - this backfill's own PR (branch `docs/tract-backfill-artifacts`), 6-field body,
      base = master, sync-before-push done, never self-merge. (Ticked once the PR is raised - see
      PR body for the R9 fields.)

## E. Knowledge base
- [x] **20. KB selector map** `ec-ui-knowledge/screens/tract.md` - CREATED 2026-08-28 (did not
      exist before) - transcribed from `tract_page.resource`'s own Variables/Documentation
      section, not re-scanned live, per the backfill work order's instruction to transcribe, not
      re-discover. Includes the wrong-then-corrected classification as a documented gotcha for
      future navigator-screen work.
- [x] **21. Reuse clause** - Step 0 found the screen ALREADY implemented (PR #555); this backfill
      produced the deliverables that document it: JOURNAL (#3), evidence (#6), KB map (#20), plus
      the SOW/README/CHECKLIST this retroactive-backfill scope additionally requires.

---

## Deviations from the standard 21-item list (stated explicitly, per R-no-silent-deviation)
- Items 4/5 (Playwright driver + investigation/) are marked N/A. Two independent reasons apply:
  Tract never had a Playwright bundle in the first place (RF-only since 2026-06-26, per the OV-GM
  exemplar precedent), AND the item is permanently waived regardless for all Bank-/Area-pattern
  work by owner decision 2026-08-27 (`docs/IUD-DELIVERABLE-CHECKLIST.md` Section H).
- Items 17/18 (registry/scorecard rows) are NOT re-appended by this backfill - they already exist
  (modified in place by PR #555) and appending a second row for the same screen would violate the
  append-only, no-duplicate convention (R23).
- Item 12's live re-run passed 5/5 on the FIRST attempt this session - no flake, no retry, nothing
  to disclose beyond the plain PASS result.
