# IUD Task — Deliverable Checklist — Payment Scheme

_Copied from `docs/IUD-DELIVERABLE-CHECKLIST.md`. This is a **documentation/evidence backfill**
(`docs/lean-deliverable-backfill-workorder.md`, owner decision 2026-08-27, Section H) around
already-merged, already-live-tested RF automation (PR #420, merged 2026-08-22). No RF file
(`payment_scheme_page.resource`, `payment_scheme_iud.robot`, `testdata/payment_scheme_*.properties`)
was modified to produce this checklist. Items 4/5 (Playwright driver + investigation/) stay
permanently waived per Section H — the pre-existing Playwright bundle from the screen's original
2026-06-11 build is kept in this bundle unchanged, not rebuilt._

## Step 0. CHECK-EXISTING-FIRST GATE
- [x] **0a.** `ec-ui-knowledge/screens/payment_scheme.md` did not exist before this backfill —
      created in this PR (see item 20). Selectors transcribed from `payment_scheme_page.resource`'s
      own Variables section, not re-scanned live.
- [x] **0b.** `grep -rl payment_scheme_page.resource workstreams/master-plan/ec-automation` ->
      existing impl found: `pageobjects/Configuration/Assets/Financial_Objects/payment_scheme_page.resource`,
      `tests/Configuration/Assets/Financial_Objects/payment_scheme_iud.robot`,
      `screens/Configuration/Assets/Financial_Objects/Payment_Scheme/` (SOW/README/playwright/
      investigation/evidence pre-existed from the 2026-06-11 build). REUSED/EXTENDED — no parallel
      copy built.
- [x] **0c.** Shared engine reused: RF suite calls the shared T2 `resources/manage_object.resource`
      (`Insert/Update/Find/Verify Object *`, `Find/Clear Object Row By Filter`) + `libraries/DbVerify.py`
      for this backfill's own evidence-capture DB reads. No new plumbing added.

## A. Bundle artifacts — `screens/Configuration/Assets/Financial_Objects/Payment_Scheme/`
- [x] **1. `payment_scheme_sow.md`** — updated (Section 7 addendum) with classification, current
      nav/grid/cell shape, test data, and the dev story pulled from PR #420's body.
- [x] **2. `README.md`** — updated with the bundle overview + exact run commands (dryrun/live/DB
      self-clean pattern).
- [x] **3. `JOURNAL.md`** — created: Built/Done well/Done wrong-or-lessons/Blockers->resolution/
      Decisions/Evidence, pulled from PR #420's body + this session's own live-run evidence.
- [ ] **4. Playwright driver** — N/A. Playwright bundle waived, owner decision 2026-08-27
      (Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md`); the pre-existing
      `playwright/ec_iud_payment_scheme.py` from the 2026-06-11 build is kept unchanged, not
      rebuilt.
- [ ] **5. `investigation/`** — N/A, same waiver as item 4; the pre-existing `investigation/`
      script from the 2026-06-11 build is kept unchanged.
- [x] **6. `evidence/`** — captured in this session: `log.html`, `output.xml`, `report.html`,
      `playwright-log.txt`, per-TC screenshots from a live 5/5 RF run (2026-08-28), alongside the
      pre-existing 2026-06-11 Playwright evidence (unchanged).
- [x] **7. `CHECKLIST.md`** — this file.

## B. RF files — treeview-mirrored (pre-existing, unmodified by this backfill)
- [x] **8. T3 page object** `pageobjects/Configuration/Assets/Financial_Objects/payment_scheme_page.resource`
      — pre-existing, merged in PR #420, not touched by this backfill.
- [x] **9. Suite** `tests/Configuration/Assets/Financial_Objects/payment_scheme_iud.robot` —
      pre-existing, merged in PR #420, not touched by this backfill.

## C. Verification gates (re-run for evidence, not re-verification of a defect)
- [x] **10. robocop clean** — `py -m robocop check pageobjects/.../payment_scheme_page.resource
      tests/.../payment_scheme_iud.robot` (this session, 2026-08-28) -> **9 issues** (5x DOC02
      missing TC docs + VAR02 unused `${OBJ_NAME_UPD}`) — matches PR #420's own cited 9-issue
      baseline exactly. No drift, no new issue category.
- [x] **11. `--dryrun` N/N PASS** — `robot --dryrun tests/Configuration/Assets/Financial_Objects/payment_scheme_iud.robot`
      (this session) -> **5/5 PASS**.
- [x] **12. LIVE headless run N/N PASS** — `EC_HEADLESS=true robot --outputdir
      screens/Configuration/Assets/Financial_Objects/Payment_Scheme/evidence tests/.../payment_scheme_iud.robot`
      (this session, 2026-08-28) -> **5/5 PASS**, first attempt, no retry needed (process rule's
      one-retry allowance was not invoked).
- [x] **13. DB ground-truth** — `libraries.DbVerify.fetch_object("OV_PAYMENT_SCHEME",
      "AUTOTEST_PAYMENT_SCHEME")` -> `None` (absent) verified via a fresh oracledb connection
      after the live run in this session.
- [x] **14. FULL I-U-D scope** — TC02 Insert / TC03 Update / TC05 Delete all present and passing
      (plus TC01 Clean State, TC04 Find) — confirmed by reading `payment_scheme_iud.robot`'s 5
      test cases.
- [x] **15. Self-clean confirmed** — independent DB re-read (fresh connection, this session) = 0
      residual `AUTOTEST_PAYMENT_SCHEME` rows in `OV_PAYMENT_SCHEME` after the run.
- [x] **16. Hygiene PASS** — `py scripts/check_bundle_hygiene.py` (repo root, this session) ->
      `[hygiene] RESULT: PASS - no hardcoded creds (R16), pure ASCII (R20), no CHECKLIST/VERIFY-REPORT
      contradictions, doc rows match declared families` (167 bundles + 272 recon scripts scanned;
      one unrelated pre-existing WARN on a Contract Area recon script, not Payment Scheme's).

## D. Delivery
- [ ] **17. Registry row** — N/A for this backfill. Payment Scheme's row in
      `workstreams/master-plan/ec-automation/docs/ec_screen_registry.md` already exists and
      already documents the PR #420 conversion (append-only edit made at merge time of that PR,
      not this backfill).
- [ ] **18. Scorecard row** — N/A for this backfill, same reasoning as item 17 —
      `docs/automation-scorecard.md`'s Payment Scheme row already reflects the merged conversion.
- [x] **19. PR** — this backfill's own PR, with the standard body (What was backfilled / Files
      added / Base branch = master); never self-merged.

## E. Knowledge base
- [x] **20. KB selector map** `ec-ui-knowledge/screens/payment_scheme.md` — created in this
      backfill: nav path, DB view, grid id, insert/update/delete selectors (transcribed from
      `payment_scheme_page.resource`'s Variables section), mandatory-yellow fields, quirks,
      last-verified date 2026-08-28.
- [x] **21. Reuse clause.** Step 0 found Payment Scheme's RF automation ALREADY implemented and
      merged — this backfill produces exactly the deliverables the reuse clause requires: #3
      JOURNAL, #6 evidence, #20 KB map (plus #1/#2/#7 restored per Section H).
