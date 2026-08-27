# Document Template - IUD Deliverable Checklist (vs docs/IUD-DELIVERABLE-CHECKLIST.md, Section H shape)

_Refreshed 2026-08-28 (deliverable backfill, `docs/lean-deliverable-backfill-workorder.md`
Batch 12, the FINAL batch) per Section H's restored items (SOW/README/JOURNAL/evidence/
CHECKLIST/KB map). Items 4/5 (Playwright driver + investigation/) stay permanently waived for
Bank-/Area-pattern work - the Universal Screen Engine replaces that role; the original
2026-07-26 Playwright driver and its investigation/recon.py are left as-is, unmodified._

## Step 0 - check-existing gate
- [x] 0a KB map created/refreshed (`ec-ui-knowledge/screens/document_template.md`, already
      current from PR #484 - re-confirmed by this backfill, no change needed).
- [x] 0b `grep -ril "document_template_page.resource"` -> confirmed the real, already-existing
      files: T3 `pageobjects/Configuration/Assets/Revenue_Document_Objects/document_template_page.resource`,
      suite `tests/Configuration/Assets/Revenue_Document_Objects/document_template_iud.robot`.
      Existing impl reused, never duplicated.
- [x] 0c reused shared engine (`resources/manage_object.resource`'s T2 keywords, e.g. `Insert/
      Update Object From Properties`, `Find/Clear Object Row By Filter`) + `DbVerify.py` +
      T1 (`resources/common.resource`) - no shared-file edits this task.

## A. Bundle artifacts (`screens/Configuration/Assets/Revenue_Document_Objects/Document_Template/`)
- [x] 1. `document_template_sow.md` - updated 2026-08-28 with the PR #484 Bank-pattern conversion
      story and the 2026-08-25 alignment fix.
- [x] 2. `README.md` - updated 2026-08-28: bundle overview + exact dryrun/live/robocop/hygiene/
      DB-self-clean commands.
- [x] 3. `JOURNAL.md` - refreshed 2026-08-28: Built/Done well/Done wrong/Blockers->resolution/
      Decisions/Evidence, modeled on Bank's JOURNAL.md.
- [ ] 4. Playwright flow - **N/A / permanently waived** (Section H): `py/document_template_iud.py`
      predates the lean rule and is left unmodified (still 7/7 from 2026-07-26); the Universal
      Screen Engine replaces this role for new work.
- [ ] 5. `investigation/` - **N/A / permanently waived** (Section H): pre-existing `recon.py` from
      the original 2026-07-26 build is left unmodified; no new recon scripts needed for a
      documentation-only backfill of already-working automation.
- [x] 6. `evidence/` - original `document_template_0[1-5]_*.png` + `rf_report.html` (2026-07-26)
      preserved; added `evidence/backfill_2026-08-28/` (dryrun 5/5, live 5/5 - no retry needed,
      per-TC screenshots, DB self-clean check, robocop re-check, hygiene re-check,
      `results_summary.md`).
- [x] 7. `CHECKLIST.md` - this file, refreshed 2026-08-28.

## B. RF files (pre-existing, NOT modified by this backfill)
- [x] 8. T3 `pageobjects/Configuration/Assets/Revenue_Document_Objects/document_template_page.resource` -
      Bank-pattern (properties-file-driven insert/update/verify, explicit `Find/Clear Document
      Template Row By Filter`, dedicated `DOCUMENT_TEMPLATE_EC_USER/PASS`, `objectdates` End Date
      resolved by label).
- [x] 9. Suite `tests/Configuration/Assets/Revenue_Document_Objects/document_template_iud.robot` -
      5 TCs (clean-state/insert/update/find/delete), fixed test code
      `AUTOTEST_DOCUMENT_TEMPLATE`, per-TC login/logout.

## C. Verification gates (re-run for this backfill's evidence, not a fresh build cycle)
- [x] 10. Robocop - `robocop check pageobjects/.../document_template_page.resource
      tests/.../document_template_iud.robot` -> **9 issues** (4x VAR02 unused suite variable,
      5x DOC02 missing test-case documentation) - not a regression: Bank's own suite returns
      **13** issues of the same two classes (checked this session for comparison). See
      `evidence/backfill_2026-08-28/robocop_output.txt`.
- [x] 11. `--dryrun` - `robot --dryrun tests/Configuration/Assets/Revenue_Document_Objects/
      document_template_iud.robot` -> **5/5 PASS**, 0 failed. See
      `evidence/backfill_2026-08-28/dryrun_output.xml`.
- [x] 12. LIVE headless run - `EC_HEADLESS=true robot tests/Configuration/Assets/
      Revenue_Document_Objects/document_template_iud.robot` -> **5/5 PASS on attempt 1**
      (TC01-TC05), no retry needed. See `evidence/backfill_2026-08-28/live_log.html` /
      `live_report.html` / `live_output.xml`.
- [x] 13. DB ground-truth - fresh `oracledb` connection (same resolution as `libraries/
      DbVerify.py`), read-only: `SELECT CODE FROM OV_DOC_TEMPLATE WHERE CODE =
      'AUTOTEST_DOCUMENT_TEMPLATE'` -> **0 rows**, run AFTER the live run completed TC05. See
      `evidence/backfill_2026-08-28/db_selfclean_check_output.txt`. In-suite screen-level checks
      (`Verify Object Insert Exists` / `Verify Object Form Record` / `Verify Object Found` /
      `Verify Object Removed`) also all passed live, per item 12.
- [x] 14. FULL I-U-D scope - Insert (TC02) + Update (TC03) + Delete (TC05) all present and
      passing (plus TC04 Find, added by the Bank-pattern conversion).
- [x] 15. Self-clean confirmed - independent fresh-connection DB re-read = 0 residual after this
      task's own live run (item 13); no pre-existing production rows touched.
- [x] 16. Hygiene PASS - `py scripts/check_bundle_hygiene.py` -> `RESULT: PASS` (no hardcoded
      creds/R16, pure ASCII/R20, no CHECKLIST/VERIFY-REPORT contradiction, doc rows match
      declared families). The run's only WARN is 2 pre-existing hardcoded-credential lines in
      **Contract Area's** `investigation/` recon script - a different screen, not touched here.
      See `evidence/backfill_2026-08-28/hygiene_output.txt`.

## D. Delivery
- [x] 17. Registry row - already present/updated by PR #484 in `docs/ec_screen_registry.md`
      (`| Document Template | ... OV (Bank family) [check] Bank-pattern conversion DONE
      (2026-08-24, Phase 3) ... |`, further updated 2026-08-25 for the alignment fix). Not
      re-appended by this backfill.
- [x] 18. Scorecard row - already present/updated by PR #484 in `docs/automation-scorecard.md`.
      Not re-appended by this backfill.
- [ ] 19. PR (R9 6-field body) - CANNOT be ticked here: this file is written BEFORE the
      backfill's own PR exists. Ticked in the PR body, never at scaffold time (lesson #235).

## E. Knowledge base
- [x] 20. KB selector map `ec-ui-knowledge/screens/document_template.md` - already refreshed by
      PR #484 (2026-08-24) to describe the current Bank-pattern RF suite (properties-driven,
      explicit filter wiring, TC04 Find, de-facto-mandatory Document Title quirk); re-confirmed
      current by this backfill, no further change needed.
- [x] 21. Reuse clause - this is a backfill of an already-implemented, already-merged conversion
      (PR #484): SOW/README/JOURNAL/evidence refresh + CHECKLIST are exactly what this task adds;
      T3/suite/registry/scorecard/KB map already existed and were not re-done.

_Gates 10-16 were run directly by this backfill task (not `scripts/verify_screen.py`, which
requires building/registering a fresh bundle - this is evidence capture of an already-proven
suite, per the workorder's explicit instruction not to re-verify from scratch). Real command
output for every ticked item lives in `evidence/backfill_2026-08-28/`._
