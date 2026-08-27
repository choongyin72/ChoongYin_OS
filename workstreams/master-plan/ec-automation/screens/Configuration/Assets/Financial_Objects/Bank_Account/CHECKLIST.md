# IUD Task — Deliverable Checklist — Bank Account

_Copied from `docs/IUD-DELIVERABLE-CHECKLIST.md`. This is a **documentation/evidence backfill**
(`docs/lean-deliverable-backfill-workorder.md`, owner decision 2026-08-27, Section H) around
already-merged, already-live-tested RF automation (PR #478, merged 2026-08-23 — the FINAL screen
of the confirmed 23-screen Bank-pattern candidate pool, Batch 11). No RF file
(`bank_account_page.resource`, `bank_account_iud.robot`, `testdata/bank_account_*.properties`) was
modified to produce this checklist. Items 4/5 (Playwright driver + investigation/) stay
permanently waived per Section H — a pre-existing Playwright bundle from the screen's original
2026-06-11 build is kept in this bundle unchanged, not rebuilt._

## Step 0. CHECK-EXISTING-FIRST GATE
- [x] **0a.** `ec-ui-knowledge/screens/bank_account.md` already existed (from the 2026-07-25
      backfill) — updated in this session with the current (post-PR #478) selectors/mandatory
      fields transcribed from `bank_account_page.resource`'s own Variables section, not re-scanned
      live.
- [x] **0b.** `grep -ril "bank_account_page.resource" workstreams/master-plan/ec-automation` →
      existing impl found: `pageobjects/Configuration/Assets/Financial_Objects/
      bank_account_page.resource`, `tests/Configuration/Assets/Financial_Objects/
      bank_account_iud.robot`, `screens/Configuration/Assets/Financial_Objects/Bank_Account/`
      (SOW/README/JOURNAL/playwright/investigation/evidence all pre-existed from the 2026-06-11
      build and the 2026-07-25 JOURNAL backfill). REUSED/EXTENDED — no parallel copy built.
- [x] **0c.** Shared engine reused: RF suite calls the shared T2 `resources/manage_object.resource`
      (`Insert/Update/Verify Object *`, `Find/Clear Object Row By Filter`) + `libraries/
      PropertiesReader.py` + `libraries/DbVerify.py` for this backfill's own evidence-capture DB
      reads. No new plumbing added.

## A. Bundle artifacts — `screens/Configuration/Assets/Financial_Objects/Bank_Account/`
- [x] **1. `bank_account_sow.md`** — updated (Section 7 addendum) with classification, current
      nav/grid/cell shape, test data, and the dev story pulled from PR #478's real body.
- [x] **2. `README.md`** — updated with the bundle overview + exact run commands (dryrun/live/DB
      self-clean pattern).
- [x] **3. `JOURNAL.md`** — updated: added the PR #478 conversion entry (Built/Done well/Done
      wrong-or-lessons/Blockers→resolution/Decisions/Evidence, pulled from the PR body) plus this
      backfill session's own entry, on top of the pre-existing 2026-06-11/07-25 entries (retained,
      not overwritten).
- [ ] **4. Playwright driver** — N/A. Playwright bundle waived, owner decision 2026-08-27
      (Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md`); the pre-existing
      `playwright/ec_iud_bank_account.py` from the 2026-06-11 build is kept unchanged, not
      rebuilt.
- [ ] **5. `investigation/`** — N/A, same waiver as item 4; the pre-existing `investigation/`
      scripts from the 2026-06-11 build are kept unchanged.
- [x] **6. `evidence/`** — captured in this session: `log.html`, `output.xml`, `report.html`,
      `playwright-log.txt`, per-TC screenshots from a live 5/5 RF run (2026-08-28), merged
      alongside the pre-existing 2026-06-11 Playwright evidence (`bank_account_0[1-8]_*.png`,
      `bank_account_results.json`, unchanged).
- [x] **7. `CHECKLIST.md`** — this file.

## B. RF files — treeview-mirrored (pre-existing, unmodified by this backfill)
- [x] **8. T3 page object**
      `pageobjects/Configuration/Assets/Financial_Objects/bank_account_page.resource` —
      pre-existing, rebuilt in PR #478 (2026-08-23), not touched by this backfill.
- [x] **9. Suite**
      `tests/Configuration/Assets/Financial_Objects/bank_account_iud.robot` — pre-existing,
      rebuilt in PR #478, not touched by this backfill.

## C. Verification gates (re-run for evidence, not re-verification of a defect)
- [x] **10. robocop clean** — `py -m robocop check pageobjects/.../bank_account_page.resource
      tests/.../bank_account_iud.robot` (this session, 2026-08-28) → **7 issues** (2 VAR02 + 5
      DOC02) — matches PR #478's own cited 7-issue baseline exactly. No drift, no new issue
      category.
- [x] **11. `--dryrun` N/N PASS** — `robot --dryrun
      tests/Configuration/Assets/Financial_Objects/bank_account_iud.robot` (this session) →
      **5/5 PASS**.
- [x] **12. LIVE headless run N/N PASS** — `EC_HEADLESS=true robot --outputdir
      screens/Configuration/Assets/Financial_Objects/Bank_Account/evidence
      tests/.../bank_account_iud.robot` (this session) → **5/5 PASS on the first attempt** — no
      flake, no retry needed. The evidence/ folder holds these artifacts.
- [x] **13. DB ground-truth** — `libraries.DbVerify.fetch_object("OV_BANK_ACCOUNT",
      "AUTOTEST_BACC")` via a fresh oracledb connection → `None` (absent) BEFORE the live run
      (code confirmed free) and `None` (absent) AFTER the live run, this session.
- [x] **14. FULL I-U-D scope** — TC02 Insert / TC03 Update / TC05 Delete all present and passing
      (plus TC01 Clean State, TC04 Find) — confirmed by reading `bank_account_iud.robot`'s 5 test
      cases.
- [x] **15. Self-clean confirmed** — independent DB re-read (fresh connection, this session) = 0
      residual `AUTOTEST_BACC` rows in `OV_BANK_ACCOUNT` after the clean run.
- [x] **16. Hygiene PASS** — `py scripts/check_bundle_hygiene.py` (repo root, this session) →
      `RESULT: PASS — no hardcoded creds (R16), pure ASCII (R20), no CHECKLIST/VERIFY-REPORT
      contradictions, doc rows match declared families` (167 bundles + 272 recon scripts
      scanned; the one WARN reported is a pre-existing, unrelated Contract Area script).

## D. Delivery
- [ ] **17. Registry row** — N/A for this backfill. Bank Account's row in
      `workstreams/master-plan/ec-automation/docs/ec_screen_registry.md` already exists and
      already documents the PR #478 conversion (append-only edit made at merge time of that PR,
      not this backfill).
- [ ] **18. Scorecard row** — N/A for this backfill, same reasoning as item 17 —
      `docs/automation-scorecard.md`'s Bank Account row already reflects the merged conversion.
- [x] **19. PR** — this backfill's own PR, with the standard body (What was backfilled / Files
      added / Base branch = master); never self-merged.

## E. Knowledge base
- [x] **20. KB selector map** `ec-ui-knowledge/screens/bank_account.md` — updated in this
      backfill: nav path, DB view, grid id, insert/update/delete selectors (transcribed from
      `bank_account_page.resource`'s Variables section, reflecting the post-PR #478 shape),
      mandatory-yellow fields, quirks, last-verified date 2026-08-28.
- [x] **21. Reuse clause.** Step 0 found Bank Account's RF automation ALREADY implemented and
      merged (PR #478) — this backfill produces exactly the deliverables the reuse clause
      requires: #3 JOURNAL, #6 evidence, #20 KB map (plus #1/#2/#7 restored per Section H).
