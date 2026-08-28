# Unit Agreement - IUD Deliverable Checklist (vs docs/IUD-DELIVERABLE-CHECKLIST.md, Section H shape)

_Added 2026-08-28 (deliverable backfill, `docs/lean-deliverable-backfill-workorder.md` Batch 8) -
this screen never had a CHECKLIST.md before. Covers Section H's restored items (SOW/README/
JOURNAL/evidence/CHECKLIST/KB map) for the 2026-08-23 Bank-pattern conversion, PR #446. Items 4/5
(Playwright driver + investigation/) stay permanently waived for Bank-/Area-pattern work - the
Universal Screen Engine replaces that role; the original 2026-06-25 Playwright driver (no
`investigation/` folder was ever built for this screen) is left as-is, unmodified._

## Step 0 - check-existing gate
- [x] 0a KB map created (`ec-ui-knowledge/screens/unit_agreement.md`, this backfill - did not
      exist before).
- [x] 0b `grep -ril "unit_agreement_page.resource"` -> confirmed the real, already-existing files:
      T3 `pageobjects/Configuration/Assets/Royalty_Objects/unit_agreement_page.resource`, suite
      `tests/Configuration/Assets/Royalty_Objects/unit_agreement_iud.robot`. Existing impl reused,
      never duplicated.
- [x] 0c reused shared engine (`resources/manage_object.resource`'s T2 keywords, e.g.
      `Find/Clear Object Row By Filter`) + `DbVerify.py` + T1 (`resources/common.resource`) - no
      shared-file edits this task.

## A. Bundle artifacts (`screens/Configuration/Assets/Royalty_Objects/Unit_Agreement/`)
- [x] 1. `unit_agreement_sow.md` - updated 2026-08-28 (new Section 0) with the PR #446 Bank-pattern
      conversion story pulled from the PR's own body; pre-conversion Sections 1-4 kept as history.
- [x] 2. `README.md` - updated 2026-08-28: bundle overview + exact dryrun/live/DB-self-clean
      commands (the pre-existing README described only the pre-conversion Playwright/RF shape).
- [x] 3. `JOURNAL.md` - added 2026-08-28 (did not exist before): Built/Done well/Done wrong/
      Blockers->resolution/Decisions/Evidence, modeled on Bank's JOURNAL.md.
- [ ] 4. Playwright flow - **N/A / permanently waived** (Section H): `playwright/
      ec_iud_unit_agreement.py` predates the lean rule and is left unmodified; the Universal
      Screen Engine replaces this role for new work.
- [ ] 5. `investigation/` - **N/A / permanently waived** (Section H): no `investigation/` folder
      was ever built for this screen; no new recon scripts needed for a documentation-only
      backfill of already-working automation.
- [x] 6. `evidence/` - original `unit_agreement_tc0[1-4]_*.png` (2026-06-25) preserved; added
      `evidence/backfill_2026-08-28/` (dryrun 5/5, live 5/5 - no retry needed, DB self-clean
      before+after, robocop, hygiene, `results_summary.md`).
- [x] 7. `CHECKLIST.md` - this file, added 2026-08-28.

## B. RF files (pre-existing, NOT modified by this backfill)
- [x] 8. T3 `pageobjects/Configuration/Assets/Royalty_Objects/unit_agreement_page.resource` -
      label-driven, per-TC login, `Open Unit Agreement Screen`, `Find/Clear Unit Agreement Row By
      Filter`, mandatory Unit Agreement Code/Unit Agreement Name/Start Date, optional Comments.
- [x] 9. Suite `tests/Configuration/Assets/Royalty_Objects/unit_agreement_iud.robot` - 5 TCs
      (clean-state/insert/update/find/delete), per-TC login/logout, fixed test code `AUTOTEST_UA`.

## C. Verification gates (re-run for this backfill's evidence, not a fresh build cycle)
- [x] 10. Robocop - `robocop check pageobjects/.../unit_agreement_page.resource
      tests/.../unit_agreement_iud.robot` -> **11 issues** (6x VAR02, 5x DOC02). PR #446's own body
      does not cite a robocop baseline for this screen, so this is the first reading on file, not
      a regression check. See `evidence/backfill_2026-08-28/robocop_output.txt`.
- [x] 11. `--dryrun` - `robot --dryrun tests/Configuration/Assets/Royalty_Objects/
      unit_agreement_iud.robot` -> **5/5 PASS**, 0 failed. See
      `evidence/backfill_2026-08-28/dryrun_output.xml`.
- [x] 12. LIVE headless run - `EC_HEADLESS=true robot tests/Configuration/Assets/Royalty_Objects/
      unit_agreement_iud.robot` -> **5/5 PASS on attempt 1** (TC01-TC05), no retry needed. See
      `evidence/backfill_2026-08-28/live_log.html`/`live_report.html`/`live_output.xml`.
- [x] 13. DB ground-truth - fresh `oracledb` connection (same resolution as `libraries/
      DbVerify.py`), read-only: `SELECT COUNT(*) FROM OV_UNIT_AGR WHERE CODE = 'AUTOTEST_UA'` = 0,
      `SELECT CODE FROM OV_UNIT_AGR WHERE CODE LIKE 'AUTOTEST%'` = no rows - run BEFORE and AFTER
      the live run. See `evidence/backfill_2026-08-28/db_selfclean_check_output.txt`.
- [x] 14. FULL I-U-D scope - Insert (TC02) + Update (TC03) + Delete (TC05) all present and passing.
- [x] 15. Self-clean confirmed - independent fresh-connection DB re-read = 0 residual both before
      and after (item 13); no pre-existing production rows touched.
- [x] 16. Hygiene PASS - `py scripts/check_bundle_hygiene.py` -> `RESULT: PASS` (no hardcoded
      creds/R16, pure ASCII/R20, no CHECKLIST/VERIFY-REPORT contradiction, doc rows match declared
      families). One pre-existing WARN belongs to the sibling Contract Area screen's
      `investigation/` recon script, untouched by this backfill. See
      `evidence/backfill_2026-08-28/hygiene_output.txt`.

## D. Delivery
- [x] 17. Registry row - already present/updated by PR #446 in `docs/ec_screen_registry.md`
      (`| Unit Agreement | Configuration > Assets > Royalty Objects > Unit Agreement | OV (Bank
      family) ... converted from the older hardcoded-field-id generator build ... |`). Not
      re-appended by this backfill.
- [x] 18. Scorecard row - already present/updated by PR #446 in `docs/automation-scorecard.md`
      (`| Royalty Objects | Unit Agreement (OV, plain) - 4/8 | Live 5/5 (2026-08-23) | ... |`). Not
      re-appended by this backfill.
- [ ] 19. PR (R9 6-field body) - CANNOT be ticked here: this file is written BEFORE the backfill's
      own PR exists. Ticked in the PR body, never at scaffold time (lesson #235).

## E. Knowledge base
- [x] 20. KB selector map `ec-ui-knowledge/screens/unit_agreement.md` - did not exist before this
      backfill; created 2026-08-28 from the T3's own Variables section (real labels, ids, quirks).
- [x] 21. Reuse clause - this is a backfill of an already-implemented, already-merged conversion
      (PR #446): JOURNAL + evidence + KB map + CHECKLIST are exactly what this task adds; tests/
      registry/scorecard already existed and were not re-done.

_Gates 10-16 were run directly by this backfill task (not `scripts/verify_screen.py`, which
requires building/registering a fresh bundle - this is evidence capture of an already-proven
suite, per the workorder's explicit instruction not to re-verify from scratch). Real command
output for every ticked item lives in `evidence/backfill_2026-08-28/`._
