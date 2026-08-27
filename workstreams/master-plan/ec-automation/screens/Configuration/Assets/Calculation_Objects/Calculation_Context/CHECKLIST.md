# IUD Task — Deliverable Checklist — Calculation Context (CO.1059)

_Copied from `docs/IUD-DELIVERABLE-CHECKLIST.md`. This is a **documentation/evidence backfill**
(`docs/lean-deliverable-backfill-workorder.md`, owner decision 2026-08-27, Section H) around
already-merged, already-live-tested RF automation (PRs #456, #514, merged 2026-08-23/25). No RF file
(`calculation_context_page.resource`, `calculation_context_iud.robot`, `testdata/calculation_context_*.properties`)
was modified to produce this checklist. Items 4/5 (Playwright driver + investigation/) stay
permanently waived per Section H — the pre-existing Playwright bundle from the screen's original
2026-07-26 build is kept in this bundle unchanged, not rebuilt._

## Step 0. CHECK-EXISTING-FIRST GATE
- [x] **0a.** `ec-ui-knowledge/screens/calculation_context.md` already existed (from the 2026-07-26
      build) — updated in this backfill (see item 20), not re-scanned live; selectors transcribed
      from `calculation_context_page.resource`'s own Variables section.
- [x] **0b.** `grep -ril calculation_context workstreams/master-plan/ec-automation/{py,pageobjects,tests,screens}`
      → existing impl found: `py/calculation_context_iud.py`,
      `pageobjects/Configuration/Assets/Calculation_Objects/calculation_context_page.resource`,
      `tests/Configuration/Assets/Calculation_Objects/calculation_context_iud.robot`,
      `screens/Configuration/Assets/Calculation_Objects/Calculation_Context/` (SOW/README/JOURNAL/
      CHECKLIST/playwright-referencing README/investigation/evidence/VERIFY-REPORT pre-existed from
      the 2026-07-26 build). REUSED/EXTENDED — no parallel copy built. Disambiguated from the sibling
      screen Calculation Group Context (CO.0245) — confirmed via `grep -v group`, own bundle, own
      registry row.
- [x] **0c.** Shared engine reused: RF suite calls the shared T2 `resources/manage_object.resource`
      (`Insert/Update/Verify Object *`, `Find/Clear Object Row By Filter`) + `libraries/DbVerify.py`
      for this backfill's own evidence-capture DB self-clean read. No new plumbing added.

## A. Bundle artifacts — `screens/Configuration/Assets/Calculation_Objects/Calculation_Context/`
- [x] **1. `calculation_context_sow.md`** — updated with the current classification, current
      nav/grid/cell shape, test data, and the dev story pulled from PR #214/#456/#514 bodies.
- [x] **2. `README.md`** — updated with the bundle overview + exact run commands (dryrun/live/DB
      self-clean pattern), citing evidence from all 3 merged PRs plus this session's own run.
- [x] **3. `JOURNAL.md`** — updated: Built/Done well/Done wrong-or-lessons/Blockers→resolution/
      Decisions/Evidence, pulled from PR #214/#456/#514 bodies + this session's own live-run
      evidence. The real PR #514 deviation (leftover inline DB-verify) is disclosed, not smoothed
      over.
- [ ] **4. Playwright driver** — N/A. Playwright bundle waived, owner decision 2026-08-27 (Section H
      of `docs/IUD-DELIVERABLE-CHECKLIST.md`); the pre-existing `py/calculation_context_iud.py` from
      the 2026-07-26 build is kept unchanged, not rebuilt.
- [ ] **5. `investigation/`** — N/A, same waiver as item 4; the pre-existing `investigation/recon.py`
      from the 2026-07-26 build is kept unchanged.
- [x] **6. `evidence/`** — captured in this session: `log.html`, `output.xml`, `report.html`,
      `playwright-log.txt`, per-TC screenshots from a live 5/5 RF run (2026-08-28), alongside the
      pre-existing 2026-07-26 Playwright/RF evidence (`calculation_context_0[1-5]_*.png`,
      `rf_report.html`, unchanged).
- [x] **7. `CHECKLIST.md`** — this file.

## B. RF files — treeview-mirrored (pre-existing, unmodified by this backfill)
- [x] **8. T3 page object**
      `pageobjects/Configuration/Assets/Calculation_Objects/calculation_context_page.resource` —
      pre-existing, merged in PR #456 (rebuilt) and PR #514 (DB-verify removal), not touched by this
      backfill.
- [x] **9. Suite** `tests/Configuration/Assets/Calculation_Objects/calculation_context_iud.robot` —
      pre-existing, merged in PR #456/#514, not touched by this backfill.

## C. Verification gates (re-run for evidence, not re-verification of a defect)
- [x] **10. robocop clean** — `py -m robocop check pageobjects/.../calculation_context_page.resource
      tests/.../calculation_context_iud.robot` (this session, 2026-08-28) → **13 issues**, all DOC02
      (missing `[Documentation]` on TC03/TC04/TC05 test cases and several keywords) — style-only
      baseline noise, no functional finding.
- [x] **11. `--dryrun` N/N PASS** —
      `py -m robot --dryrun tests/Configuration/Assets/Calculation_Objects/calculation_context_iud.robot`
      (this session) → **5/5 PASS**. Full-tree `py -m robot --dryrun tests/` → **883/883 PASS**.
- [x] **12. LIVE headless run N/N PASS** — `EC_HEADLESS=true py -m robot --outputdir
      screens/Configuration/Assets/Calculation_Objects/Calculation_Context/evidence
      tests/.../calculation_context_iud.robot` (this session, 2026-08-28) → **5/5 PASS**, clean
      first run, no retry needed.
- [x] **13. DB ground-truth** —
      `libraries.DbVerify.view_count_where("OV_CALC_CONTEXT", "CODE", "AUTOTEST_CALCCTX")` → **0**
      verified via a fresh oracledb connection after this session's live run.
- [x] **14. FULL I-U-D scope** — TC02 Insert / TC03 Update / TC05 Delete all present and passing
      (plus TC01 Clean State, TC04 Find) — confirmed by reading `calculation_context_iud.robot`'s 5
      test cases.
- [x] **15. Self-clean confirmed** — independent DB re-read (fresh connection, this session) = 0
      residual `AUTOTEST_CALCCTX` rows in `OV_CALC_CONTEXT` after the clean run.
- [x] **16. Hygiene PASS** — `py scripts/check_bundle_hygiene.py` (repo root, this session) →
      `[hygiene] RESULT: PASS - no hardcoded creds (R16), pure ASCII (R20), no CHECKLIST/VERIFY-REPORT
      contradictions, doc rows match declared families` (167 bundles + 272 recon scripts scanned).

## D. Delivery
- [ ] **17. Registry row** — N/A for this backfill. Calculation Context's row in
      `workstreams/master-plan/ec-automation/docs/ec_screen_registry.md` (line 272) already exists
      and already documents the PR #456/#514 conversion in full (append-only edits made at merge time
      of those PRs, not this backfill).
- [ ] **18. Scorecard row** — N/A for this backfill, same reasoning as item 17 —
      `docs/automation-scorecard.md` already carries both the original 2026-07-26 row (line 162) and
      the Batch 7 conversion row (line 64, with the 2026-08-25 alignment-fix annotation).
- [x] **19. PR** — this backfill's own PR, with the standard body (What was backfilled / Files added /
      Base branch = master); never self-merged.

## E. Knowledge base
- [x] **20. KB selector map** `ec-ui-knowledge/screens/calculation_context.md` — updated in this
      backfill to describe the CURRENT automation shape (5-TC, properties-file-driven, pure-screen
      verification, grid-filter wiring), superseding the pre-conversion description it held from
      2026-07-26.
- [x] **21. Reuse clause.** Step 0 found Calculation Context's RF automation ALREADY implemented and
      merged — this backfill produces exactly the deliverables the reuse clause requires: #3 JOURNAL,
      #6 evidence, #20 KB map (plus #1/#2/#7 restored per Section H).
