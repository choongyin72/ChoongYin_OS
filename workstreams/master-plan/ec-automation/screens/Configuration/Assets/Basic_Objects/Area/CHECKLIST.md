# IUD Task — Deliverable Checklist — Area (CO.0003)

_Copied from `docs/IUD-DELIVERABLE-CHECKLIST.md`. This is a **documentation/evidence backfill**
(`docs/lean-deliverable-backfill-workorder.md`, owner decision 2026-08-27, Section H) around
already-merged, already-live-tested RF automation (PRs #521, #523, merged 2026-08-25). No RF file
(`area_page.resource`, `area_iud.robot`, `testdata/area_*.properties`) was modified to produce this
checklist. Items 4/5 (Playwright driver + investigation/) stay permanently waived per Section H — a
pre-existing Playwright bundle from the screen's original 2026-06-11 build is kept in this bundle
unchanged, not rebuilt._

## Step 0. CHECK-EXISTING-FIRST GATE
- [x] **0a.** `ec-ui-knowledge/screens/area.md` did not exist before this backfill — created in this
      PR (see item 20). Selectors transcribed from `area_page.resource`'s own Variables section, not
      re-scanned live.
- [x] **0b.** `grep -ril area workstreams/master-plan/ec-automation/{py,pageobjects,tests,screens}` →
      existing impl found: `pageobjects/Configuration/Assets/Basic_Objects/area_page.resource`,
      `tests/Configuration/Assets/Basic_Objects/area_iud.robot`,
      `screens/Configuration/Assets/Basic_Objects/Area/` (SOW/README/playwright/investigation/evidence
      pre-existed from the 2026-06-11 build). REUSED/EXTENDED — no parallel copy built.
- [x] **0c.** Shared engine reused: RF suite calls the shared T2 `resources/manage_object.resource`
      (`Insert/Update/Verify Object *`, `Apply Navigator From Properties`) + `libraries/DbVerify.py`
      for this backfill's own evidence-capture DB reads. No new plumbing added.

## A. Bundle artifacts — `screens/Configuration/Assets/Basic_Objects/Area/`
- [x] **1. `area_sow.md`** — updated (Section 7 addendum) with classification, current nav/grid/cell
      shape, test data, and the dev story pulled from PR #521/#523 bodies.
- [x] **2. `README.md`** — updated with the bundle overview + exact run commands (dryrun/live/DB
      self-clean pattern).
- [x] **3. `JOURNAL.md`** — created: Built/Done well/Done wrong-or-lessons/Blockers→resolution/
      Decisions/Evidence, pulled from PR #521/#523 bodies + this session's own live-run evidence.
- [ ] **4. Playwright driver** — N/A. Playwright bundle waived, owner decision 2026-08-27 (Section H
      of `docs/IUD-DELIVERABLE-CHECKLIST.md`); the pre-existing `playwright/ec_iud_area.py` from the
      2026-06-11 build is kept unchanged, not rebuilt.
- [ ] **5. `investigation/`** — N/A, same waiver as item 4; the pre-existing `investigation/` scripts
      from the 2026-06-11 build are kept unchanged.
- [x] **6. `evidence/`** — captured in this session: `log.html`, `output.xml`, `report.html`,
      `playwright-log.txt`, per-TC screenshots from a live 5/5 RF run (2026-08-27), alongside the
      pre-existing 2026-06-11 Playwright evidence (unchanged).
- [x] **7. `CHECKLIST.md`** — this file.

## B. RF files — treeview-mirrored (pre-existing, unmodified by this backfill)
- [x] **8. T3 page object** `pageobjects/Configuration/Assets/Basic_Objects/area_page.resource` —
      pre-existing, merged in PR #521/#523, not touched by this backfill.
- [x] **9. Suite** `tests/Configuration/Assets/Basic_Objects/area_iud.robot` — pre-existing, merged in
      PR #521, not touched by this backfill.

## C. Verification gates (re-run for evidence, not re-verification of a defect)
- [x] **10. robocop clean** — `py -m robocop check pageobjects/.../area_page.resource
      tests/.../area_iud.robot` (this session, 2026-08-27) → **7 issues** (DOC02 missing TC/keyword
      docs) — matches PR #521's own cited 7-issue baseline exactly. No drift, no new issue category.
- [x] **11. `--dryrun` N/N PASS** — `robot --dryrun tests/Configuration/Assets/Basic_Objects/area_iud.robot`
      (this session) → **5/5 PASS**.
- [x] **12. LIVE headed/headless run N/N PASS** — `EC_HEADLESS=true robot --outputdir
      screens/Configuration/Assets/Basic_Objects/Area/evidence tests/.../area_iud.robot` (this
      session, 2 runs): run 1 = **4/5 PASS** (TC05 grid-redraw flake, disclosed in JOURNAL.md — DB
      confirmed the underlying delete succeeded, only the UI grid hadn't yet redrawn, matching this
      screen's own documented lazy-redraw quirk); run 2 (immediately after, same session, no code
      change) = **5/5 PASS** clean. The evidence/ folder holds run 2's artifacts.
- [x] **13. DB ground-truth** — `libraries.DbVerify.fetch_object("OV_AREA", "AUTOTEST_AREA")` → `None`
      (absent) verified via a fresh oracledb connection after both live runs in this session.
- [x] **14. FULL I-U-D scope** — TC02 Insert / TC03 Update / TC05 Delete all present and passing (plus
      TC01 Clean State, TC04 Find) — confirmed by reading `area_iud.robot`'s 5 test cases.
- [x] **15. Self-clean confirmed** — independent DB re-read (fresh connection, this session) = 0
      residual `AUTOTEST_AREA` rows in `OV_AREA` after the clean run.
- [x] **16. Hygiene PASS** — `py scripts/check_bundle_hygiene.py` (repo root, this session) →
      `[hygiene] RESULT: PASS - no hardcoded creds (R16), pure ASCII (R20), no CHECKLIST/VERIFY-REPORT
      contradictions, doc rows match declared families` (167 bundles + 271 recon scripts scanned).

## D. Delivery
- [ ] **17. Registry row** — N/A for this backfill. Area's row in
      `workstreams/master-plan/ec-automation/docs/ec_screen_registry.md` already exists and already
      documents the PR #521/#523 conversion (append-only edits made at merge time of those PRs, not
      this backfill).
- [ ] **18. Scorecard row** — N/A for this backfill, same reasoning as item 17 —
      `docs/automation-scorecard.md`'s Area row already reflects the merged conversion.
- [x] **19. PR** — this backfill's own PR, with the standard body (What was backfilled / Files added /
      Base branch = master); never self-merged.

## E. Knowledge base
- [x] **20. KB selector map** `ec-ui-knowledge/screens/area.md` — created in this backfill: nav path,
      DB view, grid id, insert/update/delete selectors (transcribed from `area_page.resource`'s
      Variables section), mandatory-yellow fields, quirks, last-verified date 2026-08-27.
- [x] **21. Reuse clause.** Step 0 found Area's RF automation ALREADY implemented and merged — this
      backfill produces exactly the deliverables the reuse clause requires: #3 JOURNAL, #6 evidence,
      #20 KB map (plus #1/#2/#7 restored per Section H).
