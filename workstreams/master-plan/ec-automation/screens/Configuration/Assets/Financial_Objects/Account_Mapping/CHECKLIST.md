# Account Mapping — IUD Deliverable Checklist (vs docs/IUD-DELIVERABLE-CHECKLIST.md, Section H shape)

_Refreshed 2026-08-28 (deliverable backfill, `docs/lean-deliverable-backfill-workorder.md` Batch 8)
per Section H's restored items (SOW/README/JOURNAL/evidence/CHECKLIST/KB map). Items 4/5
(Playwright driver + investigation/) stay permanently waived for Bank-/Area-pattern work — the
Universal Screen Engine replaces that role; the original 2026-06-11/12 Playwright driver and its
investigation/recon.py are left as-is, unmodified._

## Step 0 - check-existing gate
- [x] 0a KB map created (`ec-ui-knowledge/screens/account_mapping.md`, this backfill — did not
      exist before).
- [x] 0b `grep -ril "account_mapping_page.resource"` -> confirmed the real, already-existing files:
      T3 `pageobjects/Configuration/Assets/Financial_Objects/account_mapping_page.resource`, suite
      `tests/Configuration/Assets/Financial_Objects/account_mapping_iud.robot`. Existing impl
      reused, never duplicated.
- [x] 0c reused shared engine (`resources/manage_object.resource`'s T2 keywords, e.g.
      `Find/Clear Object Row By Filter`, `Insert/Update Object From Properties`) + `DbVerify.py` +
      T1 (`resources/common.resource`) - no shared-file edits this task.

## A. Bundle artifacts (`screens/Configuration/Assets/Financial_Objects/Account_Mapping/`)
- [x] 1. `account_mapping_sow.md` - updated 2026-08-28 with the PR #450 Bank-pattern conversion
      story (real content pulled from the PR body); old v1.0 PARKED-state content kept as history.
- [x] 2. `README.md` - updated 2026-08-28: bundle overview + exact dryrun/live/DB-self-clean
      commands (previously described only the standalone Playwright driver).
- [x] 3. `JOURNAL.md` - created 2026-08-28: Built/Done well/Done wrong/Blockers->resolution/
      Decisions/Evidence, modeled on Bank's JOURNAL.md.
- [ ] 4. Playwright flow - **N/A / permanently waived** (Section H): `playwright/
      ec_iud_account_mapping.py` predates the lean rule and is left unmodified; the Universal
      Screen Engine replaces this role for new work.
- [ ] 5. `investigation/` - **N/A / permanently waived** (Section H): pre-existing
      `financial_objects_recon.py` from the original 2026-06-11/12 build is left unmodified; no new
      recon scripts needed for a documentation-only backfill of already-working automation.
- [x] 6. `evidence/` - original `account_mapping_0[1-8]_*.png` + `account_mapping_results.json`
      (2026-06-12) preserved; added `evidence/backfill_2026-08-28/` (dryrun 5/5, live 5/5 - no
      retry needed, DB self-clean before+after, robocop re-check, hygiene re-check,
      `results_summary.md`).
- [x] 7. `CHECKLIST.md` - this file, created 2026-08-28.

## B. RF files (pre-existing, NOT modified by this backfill)
- [x] 8. T3 `pageobjects/Configuration/Assets/Financial_Objects/account_mapping_page.resource` -
      label-driven, per-TC login, `Find/Clear Account Mapping Row By Filter`, 8 mandatory reference
      dropdowns + Account Category cascade dependency for Financial Account, Line Item Type
      re-render exclusion from the round-trip form-label list.
- [x] 9. Suite `tests/Configuration/Assets/Financial_Objects/account_mapping_iud.robot` - 5 TCs
      (clean-state/insert/update/find/delete), per-TC login/logout, fixed test code `AUTOTEST_AM`.

## C. Verification gates (re-run for this backfill's evidence, not a fresh build cycle)
- [x] 10. Robocop - `robocop check pageobjects/.../account_mapping_page.resource
      tests/.../account_mapping_iud.robot` -> **7 issues** (2x VAR02, 5x DOC02), same baseline
      pattern as sibling Bank-pattern conversions (not a regression). See
      `evidence/backfill_2026-08-28/robocop_output.txt`.
- [x] 11. `--dryrun` - `robot --dryrun tests/Configuration/Assets/Financial_Objects/
      account_mapping_iud.robot` -> **5/5 PASS**, 0 failed. See
      `evidence/backfill_2026-08-28/dryrun_output.xml`.
- [x] 12. LIVE headless run - `EC_HEADLESS=true robot tests/Configuration/Assets/
      Financial_Objects/account_mapping_iud.robot` -> **5/5 PASS on attempt 1** (TC01-TC05), no
      retry needed. See `evidence/backfill_2026-08-28/live_log.html`/`live_report.html`/
      `live_output.xml`.
- [x] 13. DB ground-truth - fresh `oracledb` connection (same resolution as `libraries/
      DbVerify.py`), read-only: `SELECT COUNT(*) FROM OV_FIN_ACCOUNT_MAPPING WHERE CODE =
      'AUTOTEST_AM'` = 0, `SELECT CODE FROM OV_FIN_ACCOUNT_MAPPING WHERE CODE LIKE 'AUTOTEST%'` =
      no rows - run AFTER the live run (matches PR #450's own cited assertion:
      `Code Should Be Present In View OV_FIN_ACCOUNT_MAPPING AUTOTEST_AM` (TC02) /
      `Code Should Be Absent In View OV_FIN_ACCOUNT_MAPPING AUTOTEST_AM` (TC05)). See
      `evidence/backfill_2026-08-28/db_selfclean_check_output.txt`.
- [x] 14. FULL I-U-D scope - Insert (TC02) + Update (TC03) + Delete (TC05) all present and passing.
- [x] 15. Self-clean confirmed - independent fresh-connection DB read after the live run = 0
      residual `AUTOTEST_AM`/`AUTOTEST%` rows; total row count 75, unchanged from PR #450's own
      cited baseline (item 13).
- [x] 16. Hygiene PASS - `py scripts/check_bundle_hygiene.py` (repo root) -> `RESULT: PASS` (no
      hardcoded creds/R16, pure ASCII/R20, no CHECKLIST/VERIFY-REPORT contradiction, doc rows match
      declared families). The run's only WARN is 2 pre-existing hardcoded-credential lines in
      **Contract Area's** `investigation/` recon script - a different screen, not touched here. See
      `evidence/backfill_2026-08-28/hygiene_output.txt`.

## D. Delivery
- [x] 17. Registry row - already present/updated by PR #450 in `docs/ec_screen_registry.md`
      (`| Account Mapping | Configuration > Assets > Financial Objects > Account Mapping | OV
      rebuilt live 5/5 (2026-08-23, Batch 6, FINAL batch of the 23-screen candidate pool) ... |`).
      Not re-appended by this backfill.
- [x] 18. Scorecard row - already present/updated by PR #450 in `docs/automation-scorecard.md`.
      Not re-appended by this backfill.
- [ ] 19. PR (R9 6-field body) - CANNOT be ticked here: this file is written BEFORE the backfill's
      own PR exists. Ticked in the PR body, never at scaffold time (lesson #235).

## E. Knowledge base
- [x] 20. KB selector map `ec-ui-knowledge/screens/account_mapping.md` - CREATED 2026-08-28 by this
      backfill (did not exist before) - nav path, DB view, grid id, insert/update/delete selectors,
      8 mandatory-yellow dropdowns + Account Category cascade, Line Item Type re-render quirk,
      last-verified date.
- [x] 21. Reuse clause - this is a backfill of an already-implemented, already-merged conversion
      (PR #450): SOW/README updates + new JOURNAL + evidence + new KB map are exactly what this
      task adds; tests/registry/scorecard already existed and were not re-done.

_Gates 10-16 were run directly by this backfill task (not `scripts/verify_screen.py`, which
requires building/registering a fresh bundle - this is evidence capture of an already-proven
suite, per the workorder's explicit instruction not to re-verify from scratch). Real command
output for every ticked item lives in `evidence/backfill_2026-08-28/`._
