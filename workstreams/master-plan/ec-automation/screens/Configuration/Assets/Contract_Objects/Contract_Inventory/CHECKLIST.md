# Contract Inventory - IUD Deliverable Checklist (vs docs/IUD-DELIVERABLE-CHECKLIST.md, Section H shape)

_Refreshed 2026-08-28 (deliverable backfill, `docs/lean-deliverable-backfill-workorder.md` Batch 4)
per Section H's restored items (SOW/README/JOURNAL/evidence/CHECKLIST/KB map). Items 4/5
(Playwright driver + investigation/) stay permanently waived for Bank-/Area-pattern work - the
Universal Screen Engine replaces that role; the original 2026-08-02 Playwright driver and its
investigation/recon.py are left as-is, unmodified._

## Step 0 - check-existing gate
- [x] 0a KB map created/refreshed (`ec-ui-knowledge/screens/contract_inventory.md`, this backfill).
- [x] 0b `grep -ril "contract_inventory_page.resource"` -> confirmed the real, already-existing
      files: T3 `pageobjects/Configuration/Assets/Contract_Objects/contract_inventory_page.resource`,
      suite `tests/Configuration/Assets/Contract_Objects/contract_inventory_iud.robot`. Existing
      impl reused, never duplicated.
- [x] 0c reused shared engine (`resources/manage_object.resource`'s T2 keywords, e.g.
      `Apply Navigator From Properties`, `Find/Clear Object Row By Filter`) + `DbVerify.py` +
      T1 (`resources/common.resource`) - no shared-file edits this task.

## A. Bundle artifacts (`screens/Configuration/Assets/Contract_Objects/Contract_Inventory/`)
- [x] 1. `contract_inventory_sow.md` - updated 2026-08-28 with the PR #556 Area-pattern conversion
      story and this backfill's own note on an unconfirmed detached-HEAD story (see JOURNAL.md).
- [x] 2. `README.md` - added 2026-08-28: bundle overview + exact dryrun/live/DB-self-clean commands.
- [x] 3. `JOURNAL.md` - refreshed 2026-08-28: Built/Done well/Done wrong/Blockers->resolution/
      Decisions/Evidence, modeled on Bank's JOURNAL.md.
- [ ] 4. Playwright flow - **N/A / permanently waived** (Section H): `py/contract_inventory_iud.py`
      predates the lean rule and is left unmodified; the Universal Screen Engine replaces this
      role for new work.
- [ ] 5. `investigation/` - **N/A / permanently waived** (Section H): pre-existing `recon.py` from
      the original 2026-08-02 build is left unmodified; no new recon scripts needed for a
      documentation-only backfill of already-working automation.
- [x] 6. `evidence/` - original `ci_0[1-5]_*.png` + `results.json` (2026-08-02) preserved; added
      `evidence/backfill_2026-08-28/` (dryrun 5/5, live 5/5 - no retry needed, DB self-clean
      before+after, robocop re-check, hygiene re-check incl. one doc-wording fix, `results_summary.md`).
- [x] 7. `CHECKLIST.md` - this file, refreshed 2026-08-28.

## B. RF files (pre-existing, NOT modified by this backfill)
- [x] 8. T3 `pageobjects/Configuration/Assets/Contract_Objects/contract_inventory_page.resource` -
      label-driven, per-TC login, `Open Contract Inventory Screen With Navigator Values Populated`,
      `Find/Clear Contract Inventory Row By Filter`, mandatory Contract Inventory Code/Contract
      Inventory Name/Start Date + fixed "Contract name" dropdown.
- [x] 9. Suite `tests/Configuration/Assets/Contract_Objects/contract_inventory_iud.robot` - 5 TCs
      (clean-state/insert/update/find/delete), per-TC login/logout, fixed test code
      `AUTOTEST_CONTRACT_INVENTORY`.

## C. Verification gates (re-run for this backfill's evidence, not a fresh build cycle)
- [x] 10. Robocop - `robocop check pageobjects/.../contract_inventory_page.resource
      tests/.../contract_inventory_iud.robot` -> **7 issues** (2x VAR02, 5x DOC02), exact parity
      with PR #556's own cited baseline (not a regression). See
      `evidence/backfill_2026-08-28/robocop_output.txt`.
- [x] 11. `--dryrun` - `robot --dryrun tests/Configuration/Assets/Contract_Objects/
      contract_inventory_iud.robot` -> **5/5 PASS**, 0 failed. See
      `evidence/backfill_2026-08-28/dryrun_output.xml`.
- [x] 12. LIVE headless run - `EC_HEADLESS=true robot tests/Configuration/Assets/Contract_Objects/
      contract_inventory_iud.robot` -> **5/5 PASS on attempt 1** (TC01-TC05), no retry needed. See
      `evidence/backfill_2026-08-28/live_log.html`/`live_report.html`/`live_output.xml`.
- [x] 13. DB ground-truth - fresh `oracledb` connection (same resolution as `libraries/
      DbVerify.py`), read-only: `SELECT COUNT(*) FROM OV_CONTRACT_INVENTORY WHERE CODE =
      'AUTOTEST_CONTRACT_INVENTORY'` = 0, `SELECT CODE FROM OV_CONTRACT_INVENTORY WHERE CODE LIKE
      'AUTOTEST%'` = no rows - run BEFORE and AFTER the live run. See
      `evidence/backfill_2026-08-28/db_selfclean_check_output.txt`.
- [x] 14. FULL I-U-D scope - Insert (TC02) + Update (TC03) + Delete (TC05) all present and passing.
- [x] 15. Self-clean confirmed - independent fresh-connection DB re-read = 0 residual both before
      and after (item 13); no pre-existing production rows touched.
- [x] 16. Hygiene PASS - `py scripts/check_bundle_hygiene.py` -> first run FAILed on a
      false-positive vocabulary hit in this backfill's OWN `JOURNAL.md` draft (the substring "no
      navigator" inside an unrelated sentence about field-reuse, tripping the OV-GM
      family-vocabulary gate); reworded the sentence, re-ran -> `RESULT: PASS` (no hardcoded
      creds/R16, pure ASCII/R20, no CHECKLIST/VERIFY-REPORT contradiction, doc rows match declared
      families). The run's only WARN is 2 pre-existing hardcoded-credential lines in **Contract
      Area's** `investigation/` recon script - a different screen, not touched here. See
      `evidence/backfill_2026-08-28/hygiene_output.txt`.

## D. Delivery
- [x] 17. Registry row - already present/updated by PR #556 in `docs/ec_screen_registry.md`
      (`| Contract Inventory | Configuration > Assets > Contract_Objects > Contract Inventory
      (CO.2054) | ... CONVERTED 2026-08-26 to the FULL Area-pattern RF STRUCTURE ...`). Not
      re-appended by this backfill.
- [x] 18. Scorecard row - already present/updated by PR #556 in `docs/automation-scorecard.md`
      (`| Contract Inventory (OV-GM, CO.2054) | OK Done 2026-08-02 (base IUD, verify_screen PASS) -
      CONVERTED 2026-08-26 to the FULL Area-pattern RF suite STRUCTURE ...`). Not re-appended by
      this backfill.
- [ ] 19. PR (R9 6-field body) - CANNOT be ticked here: this file is written BEFORE the backfill's
      own PR exists. Ticked in the PR body, never at scaffold time (lesson #235).

## E. Knowledge base
- [x] 20. KB selector map `ec-ui-knowledge/screens/contract_inventory.md` - already existed
      (2026-08-02 original build); refreshed 2026-08-28 by this backfill to describe the current
      Area-pattern RF suite (per-TC login, properties-driven, explicit filter wiring, TC04 Find)
      rather than the superseded 4-TC/inline-navigator shape.
- [x] 21. Reuse clause - this is a backfill of an already-implemented, already-merged conversion
      (PR #556): JOURNAL + evidence + KB map refresh are exactly what this task adds; tests/
      registry/scorecard already existed and were not re-done.

_Gates 10-16 were run directly by this backfill task (not `scripts/verify_screen.py`, which
requires building/registering a fresh bundle - this is evidence capture of an already-proven
suite, per the workorder's explicit instruction not to re-verify from scratch). Real command
output for every ticked item lives in `evidence/backfill_2026-08-28/`._
