# IUD Task — Deliverable Checklist — Report Area (RP.0017)

_Copied from `docs/IUD-DELIVERABLE-CHECKLIST.md`. This is a **documentation/evidence backfill**
(`docs/lean-deliverable-backfill-workorder.md`, owner decision 2026-08-27, Section H, Batch 10)
around already-merged, already-live-tested RF automation — the Bank-pattern conversion in PR #468
(merged 2026-08-23, Batch 9 of the original Bank-pattern conversion project). No RF file
(`report_area_page.resource`, `report_area_iud.robot`, `testdata/report_area_*.properties`) was
modified to produce this checklist. Items 4/5 (Playwright driver + `investigation/`) stay
permanently waived per Section H — the pre-existing Playwright bundle from the screen's original
2026-07-25 build is kept in this bundle unchanged, not rebuilt. This file SUPERSEDES the
pre-existing `CHECKLIST.md`, which described the pre-conversion 4-TC/Playwright-7/7/RF-4/4 state.

## Step 0. CHECK-EXISTING-FIRST GATE
- [x] **0a.** `ec-ui-knowledge/screens/report_area.md` already existed (from the 2026-07-25
      build) — updated in this PR (see item 20) to describe the current post-PR-#468 Bank-pattern
      RF shape, not re-scanned live from scratch.
- [x] **0b.** `grep -rl "report_area_page.resource" workstreams/master-plan/ec-automation` →
      existing impl found: `pageobjects/Reporting/report_area_page.resource`,
      `tests/Reporting/report_area_iud.robot`, `py/report_area_iud.py`,
      `screens/Reporting/Report_Area/` (SOW/README/JOURNAL/CHECKLIST/VERIFY-REPORT/evidence/
      investigation pre-existed from the 2026-07-25 build). REUSED/EXTENDED — no parallel copy
      built.
- [x] **0c.** Shared engine reused: RF suite calls the shared T2 `resources/manage_object.resource`
      (`Insert/Update/Verify Object *`, `Find/Clear Object Row By Filter`) + `libraries/DbVerify.py`
      for this backfill's own evidence-capture DB reads (via new
      `investigation/check_autotest_residual.py`). No new plumbing added.

## A. Bundle artifacts — `screens/Reporting/Report_Area/`
- [x] **1. `report_area_sow.md`** — updated (Addendum 2026-08-28) with the current OV
      classification, the Bank-pattern rebuild's real changes (properties-file-driven insert,
      explicit grid-filter wiring, fixed test code, TC04 Find added), the "Start date" lowercase
      label gotcha, and the dev story pulled from PR #468's real body.
- [x] **2. `README.md`** — updated with the post-PR-#468 bundle overview + exact run commands
      (dryrun, live headless run, DB self-clean check via new
      `investigation/check_autotest_residual.py`).
- [x] **3. `JOURNAL.md`** — appended (dated 2026-08-23 entry, Built/Done well/Done wrong-or-lessons/
      Blockers→resolution/Decisions/Evidence), pulled from PR #468's real body + this session's own
      live-run evidence. Prior 2026-07-25 entry left untouched.
- [ ] **4. Playwright driver** — N/A. Playwright bundle waived, owner decision 2026-08-27 (Section H
      of `docs/IUD-DELIVERABLE-CHECKLIST.md`); the pre-existing `py/report_area_iud.py` from the
      2026-07-25 build is kept unchanged, not rebuilt.
- [ ] **5. `investigation/`** — mostly N/A per the same Section H waiver; the pre-existing recon
      scripts (`recon.py`, `recon_update.py`) are kept unchanged. One new, additive script was added
      for this backfill's own evidence capture: `check_autotest_residual.py` (self-clean re-check,
      not a re-investigation of the screen).
- [x] **6. `evidence/`** — captured in this session: `evidence/2026-08-28_backfill/` (`log.html`,
      `output.xml`, `report.html`, `playwright-log.txt`, per-TC screenshots from a live 5/5 RF run
      against the CURRENT converted suite), alongside the pre-existing 2026-07-25 evidence
      (`rpta_0[1-5]_*.png`, `rf_report.html` — kept unchanged, predates the conversion). All new
      evidence files individually well under 2MB (largest is `output.xml` at ~380KB).
- [x] **7. `CHECKLIST.md`** — this file (rewritten; the pre-existing version described the
      pre-conversion 4-TC/Playwright-7/7/RF-4/4 state and is superseded by this update).

## B. RF files — treeview-mirrored (pre-existing, unmodified by this backfill)
- [x] **8. T3 page object** `pageobjects/Reporting/report_area_page.resource` — pre-existing,
      converted to the Bank pattern in PR #468 (merged 2026-08-23), not touched by this backfill.
- [x] **9. Suite** `tests/Reporting/report_area_iud.robot` — pre-existing, converted in PR #468,
      not touched by this backfill.

## C. Verification gates (re-run for evidence, not re-verification of a defect)
- [x] **10. robocop clean** — `py -m robocop check pageobjects/Reporting/report_area_page.resource
      tests/Reporting/report_area_iud.robot` (this session, 2026-08-28) → **9 issues** (VAR02 x4 +
      DOC02 x5) — identical shape (kind/count) to PR #468's own cited baseline (parity with
      Berth's), no new finding category, no regression introduced by this backfill (no RF file
      touched).
- [x] **11. `--dryrun` N/N PASS** — `robot --dryrun tests/Reporting/report_area_iud.robot`
      (this session) → **5/5 PASS**. Full-tree `robot --dryrun tests/` (this session) →
      **883/883 PASS**, no collisions/regressions.
- [x] **12. LIVE headless run N/N PASS** — `EC_HEADLESS=true robot --outputdir
      screens/Reporting/Report_Area/evidence/2026-08-28_backfill tests/Reporting/
      report_area_iud.robot` (this session) → **5/5 PASS**, first attempt, no flake, no retry
      needed.
- [x] **13. DB ground-truth** — `investigation/check_autotest_residual.py`
      (`SELECT CODE, NAME FROM OV_REPORT_AREA WHERE CODE LIKE 'AUTOTEST%'`) → `[]` (0 residual
      rows), verified via a fresh oracledb connection after the live run in this session. TC03
      (Update) is also DB-verified inline via `Field Should Equal In View OV_REPORT_AREA`
      (pre-existing suite behavior, confirmed by reading `report_area_iud.robot`).
- [x] **14. FULL I-U-D scope** — TC02 Insert / TC03 Update / TC05 Delete all present and passing
      (plus TC01 Verify Clean State, TC04 Find) — confirmed by reading `report_area_iud.robot`'s
      5 test cases and by this session's own live 5/5 run.
- [x] **15. Self-clean confirmed** — independent DB re-read (fresh connection, this session) = 0
      residual `AUTOTEST%` rows in `OV_REPORT_AREA` after the live run.
- [x] **16. Hygiene PASS** — `py scripts/check_bundle_hygiene.py` (repo root, this session) →
      `RESULT: PASS - no hardcoded creds (R16), pure ASCII (R20), no CHECKLIST/VERIFY-REPORT
      contradictions, doc rows match declared families` (167 bundles + 273 recon scripts scanned;
      the one WARN in the output is a pre-existing, unrelated Contract Area recon script, not this
      screen).

## D. Delivery
- [ ] **17. Registry row** — N/A for this backfill. Report Area's row in
      `docs/ec_screen_registry.md` already exists and already documents the PR #468 conversion
      (append-only edit made at merge time of that PR, not this backfill).
- [ ] **18. Scorecard row** — N/A for this backfill, same reasoning as item 17 —
      `docs/automation-scorecard.md`'s Report Area row already reflects the merged conversion.
- [x] **19. PR** — this backfill's own PR, with the standard body (What was backfilled / Files
      added / Base branch = master); never self-merged.

## E. Knowledge base
- [x] **20. KB selector map** `ec-ui-knowledge/screens/report_area.md` — updated in this backfill:
      the Automation section now describes the current post-PR-#468 shape (5 TCs, per-TC login,
      properties-file-driven testdata, explicit grid-filter wiring), the "Start date" lowercase
      label gotcha, mandatory-yellow fields, quirks, last-verified date updated to 2026-08-28.
- [x] **21. Reuse clause.** Step 0 found Report Area's RF automation ALREADY implemented,
      converted, and merged — this backfill produces exactly the deliverables the reuse clause
      requires: #1/#2/#3 refreshed, #6 fresh evidence, #7 rewritten CHECKLIST, #20 KB map updated.
