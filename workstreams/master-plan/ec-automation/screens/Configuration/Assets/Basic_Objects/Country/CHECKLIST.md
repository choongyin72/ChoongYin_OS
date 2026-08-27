# IUD Task — Deliverable Checklist (Country)

Copied from `docs/IUD-DELIVERABLE-CHECKLIST.md` (Steps 0, A minus items 4/5, B, C, D, E), per
`docs/lean-deliverable-backfill-workorder.md` Batch 6 (Bank-pattern backfill). Country's RF suite
and registry/scorecard rows were built and merged in PR #428 (2026-08-23); this checklist
documents that already-working automation retroactively, plus a fresh evidence-capture re-run
(2026-08-28) — no RF automation was modified for this backfill.

## Step 0. CHECK-EXISTING-FIRST GATE
- [x] **0a.** `ec-ui-knowledge/screens/country.md` did not exist before this backfill — created
      as part of this task (item 20 below), not pre-existing.
- [x] **0b.** `grep -ril country workstreams/master-plan/ec-automation/{py,pageobjects,tests,screens}`
      → found existing impl: `pageobjects/Configuration/Assets/Basic_Objects/country_page.resource`,
      `tests/Configuration/Assets/Basic_Objects/country_iud.robot`,
      `screens/Configuration/Assets/Basic_Objects/Country/`. REUSED/EXTENDED (this backfill adds
      docs only) — no parallel copy built.
- [x] **0c.** N/A for this backfill task — no new automation code written; the screen already
      reuses the shared T2 `resources/manage_object.resource` engine (confirmed in PR #428 body:
      "No shared T1/T2 file... touched").

## A. Bundle artifacts — `screens/Configuration/Assets/Basic_Objects/Country/`
- [x] **1. `country_sow.md`** — updated 2026-08-28 to reflect the Bank-pattern conversion
      (classification, DOM refs, test data, PR #428's real dev-story narrative); previously
      described the pre-conversion 2026-06-11 shape only.
- [x] **2. `README.md`** — updated 2026-08-28: bundle overview + exact `robot --dryrun` /
      `EC_HEADLESS=true robot` / DB self-clean commands; previously Playwright-primary framing.
- [x] **3. `JOURNAL.md`** — created 2026-08-28, modeled on
      `screens/Configuration/Assets/Financial_Objects/Bank/JOURNAL.md`, content sourced from PR
      #428's real body.
- [ ] **4. `playwright/ec_iud_country.py`** — N/A / waived (Section H: Playwright driver stays
      waived permanently for Bank-/Area-pattern work; the pre-existing 2026-06-11 Playwright
      bundle is preserved untouched as historical reference, not rebuilt).
- [ ] **5. `investigation/`** — N/A / waived (same Section H waiver; the pre-existing
      pre-conversion recon scripts are preserved untouched, not extended).
- [x] **6. `evidence/`** — pre-existing 2026-06-11 Playwright screenshots preserved; this backfill
      added `evidence/rf_backfill_2026-08-28/` with a real live RF re-run: `log.html`,
      `output.xml`, 26 per-step screenshots (`TC0*_{login,open_screen,action,verify,logout}.png`),
      and `results_summary.md`.
- [x] **7. `CHECKLIST.md`** — this file.

## B. RF files (pre-existing, merged PR #428 — NOT modified by this backfill)
- [x] **8. T3 page object** `pageobjects/Configuration/Assets/Basic_Objects/country_page.resource`
      — label-driven, locators in Variables, docstring matches (confirmed by reading the file
      2026-08-28; unchanged from PR #428).
- [x] **9. Suite** `tests/Configuration/Assets/Basic_Objects/country_iud.robot` — TC01 Verify
      Clean State -> TC02 Insert -> TC03 Update -> TC04 Find -> TC05 Delete (clean structure,
      confirmed by reading the file 2026-08-28; unchanged from PR #428).

## C. Verification gates (re-run 2026-08-28 for this backfill; `verify_screen.py` not run — see note)
> Note: `scripts/verify_screen.py` was not re-run for this backfill (this is a docs/evidence
> backfill of already-merged automation, not a new build); the individual gate commands below
> were run directly and their real output is cited.
- [x] **10. robocop clean (parity)** — `py -m robocop check pageobjects/.../country_page.resource
      tests/.../country_iud.robot` → **9 issues (4 VAR02 + 5 DOC02)**, 2026-08-28. Same
      count/kind as PR #428's own cited baseline ("9 issues... identical in kind/count to the
      State exemplar's own baseline") — no new issue classes, not a regression.
- [x] **11. `--dryrun` N/N PASS** — `robot --dryrun tests/Configuration/Assets/Basic_Objects/country_iud.robot`
      → **5/5 PASS**, 2026-08-28.
- [x] **12. LIVE headless run N/N PASS** — `EC_HEADLESS=true robot tests/Configuration/Assets/Basic_Objects/country_iud.robot`
      → **5/5 PASS** (TC01-TC05), 2026-08-28. Output/log in `evidence/rf_backfill_2026-08-28/`.
- [x] **13. DB ground-truth** — exact assertion: TC05's `Verify Country Record Removed` ->
      shared T2 `Verify Object Removed` -> `Code Should Be Absent In View OV_COUNTRY
      AUTOTEST_COUNTRY` — PASSED live 2026-08-28 (also independently confirmed at PR #428 merge
      via a fresh `oracledb` connection, per that PR's body).
- [x] **14. FULL I-U-D scope** — Insert (TC02) + Update (TC03) + Find (TC04) + Delete (TC05) all
      present and PASS, confirmed 2026-08-28.
- [x] **15. Self-clean confirmed** — 0 residual `AUTOTEST_COUNTRY` rows in `OV_COUNTRY` after the
      2026-08-28 live run (via TC05's own DB assertion above); PR #428 additionally confirmed
      code-freeness both BEFORE and AFTER its own run via a fresh connection.
- [x] **16. Hygiene PASS** — `py scripts/check_bundle_hygiene.py` (run from repo root) →
      **PASS** — "no hardcoded creds (R16), pure ASCII (R20), no CHECKLIST/VERIFY-REPORT
      contradictions, doc rows match declared families." (One unrelated WARN reported for
      Contract Area's `investigation/`, not Country.)

## D. Delivery
- [x] **17. Registry row** — `workstreams/master-plan/ec-automation/docs/ec_screen_registry.md`
      already carries Country's Bank-pattern row (line ~43, added at PR #428 merge); confirmed
      present and accurate 2026-08-28, no edit needed.
- [x] **18. Scorecard row** — `docs/automation-scorecard.md` already carries Country's row
      (added at PR #428 merge); confirmed present, no edit needed.
- [x] **19. PR** — this backfill's PR uses the standard body (What backfilled / Files added /
      Base branch = master); never self-merged.

## E. Knowledge base
- [x] **20. KB selector map** `ec-ui-knowledge/screens/country.md` — created 2026-08-28, pulled
      from `country_page.resource`'s real Variables section (nav path, DB view, grid id,
      insert/update/delete selectors, mandatory-yellow fields, quirks, last-verified date).
- [x] **21. Reuse clause** — Step 0 found the screen already implemented (PR #428, merged); this
      backfill produces the reuse-run deliverables the clause requires: JOURNAL (#3), evidence
      (#6), and KB map (#20) — not just re-confirming passing tests.

---
**OVERALL: PASS** (all applicable items ticked with real 2026-08-28 evidence; items 4/5 correctly
left unticked/N/A per the Section H Playwright-driver waiver, not silently skipped).
