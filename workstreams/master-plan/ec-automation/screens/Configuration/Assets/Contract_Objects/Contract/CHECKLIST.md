# Contract — IUD Deliverable Checklist (vs docs/IUD-DELIVERABLE-CHECKLIST.md, Section H shape)

_Refreshed 2026-08-27 (deliverable backfill, `docs/lean-deliverable-backfill-workorder.md` Batch 3)
per Section H's restored items (SOW/README/JOURNAL/evidence/CHECKLIST/KB map). Items 4/5
(Playwright driver + investigation/) stay permanently waived for Bank-/Area-pattern work — the
Universal Screen Engine replaces that role; the original 2026-08-02 Playwright driver and its
investigation/recon.py are left as-is, unmodified._

## Step 0 — check-existing gate
- [x] 0a KB map created/refreshed (`ec-ui-knowledge/screens/contract.md`, this backfill).
- [x] 0b `grep -ril "contract_page.resource"` (disambiguated from Contract Area/Contract
      Capacity/Contract Inventory) -> confirmed the real, already-existing files: T3
      `pageobjects/Configuration/Assets/Contract_Objects/contract_page.resource`, suite
      `tests/Configuration/Assets/Contract_Objects/contract_iud.robot`. Existing impl reused,
      never duplicated.
- [x] 0c reused shared engine (`resources/manage_object.resource`'s T2 keywords, e.g.
      `Apply Navigator From Properties`, `Find/Clear Object Row By Filter`) + `DbVerify.py` +
      T1 (`resources/common.resource`) — no shared-file edits this task.

## A. Bundle artifacts (`screens/Configuration/Assets/Contract_Objects/Contract/`)
- [x] 1. `contract_sow.md` — updated 2026-08-27 with §2 (PR #546 Area-pattern conversion, incl.
      the branch-collision incident) and §3 (this backfill).
- [x] 2. `README.md` — added 2026-08-27: bundle overview + exact dryrun/live/DB-self-clean commands.
- [x] 3. `JOURNAL.md` — refreshed 2026-08-27: Built/Done well/Done wrong/Blockers->resolution
      (honest branch-collision + UI-timing-flake narrative)/Decisions/Evidence, modeled on Bank's
      JOURNAL.md.
- [ ] 4. Playwright flow — **N/A / permanently waived** (Section H): `py/contract_iud.py`
      predates the lean rule and is left unmodified; the Universal Screen Engine replaces this
      role for new work.
- [ ] 5. `investigation/` — **N/A / permanently waived** (Section H): pre-existing `recon.py` from
      the original 2026-08-02 build is left unmodified; no new recon scripts needed for a
      documentation-only backfill of already-working automation.
- [x] 6. `evidence/` — original `ct_0[1-5]_*.png` + `results.json` (2026-08-02) preserved; added
      `evidence/backfill_2026-08-27/` (dryrun 5/5, live-run flake + clean 5/5 rerun, DB self-clean
      re-check, robocop re-check, hygiene PASS, `results_summary.md`).
- [x] 7. `CHECKLIST.md` — this file, refreshed 2026-08-27.

## B. RF files (pre-existing, NOT modified by this backfill)
- [x] 8. T3 `pageobjects/Configuration/Assets/Contract_Objects/contract_page.resource` —
      label-driven, per-TC login, `Open Contract Screen With Navigator Values Populated`,
      `Find/Clear Contract Row By Filter`, mandatory Contract Code/Contract Name/Start
      Date/**End Date**/**Contract Year Start** + Contract Template/Contract Area dropdowns.
- [x] 9. Suite `tests/Configuration/Assets/Contract_Objects/contract_iud.robot` — 5 TCs
      (clean-state/insert/update/find/delete), per-TC login/logout, fixed test code
      `AUTOTEST_CONTRACT`.

## C. Verification gates (re-run for this backfill's evidence, not a fresh build cycle)
- [x] 10. Robocop — `robocop check pageobjects/.../contract_page.resource
      tests/.../contract_iud.robot` -> **7 issues** (2x VAR02, 5x DOC02), exact parity with PR
      #546's own cited baseline (not a regression). See
      `evidence/backfill_2026-08-27/robocop_output.txt`.
- [x] 11. `--dryrun` — `robot --dryrun tests/Configuration/Assets/Contract_Objects/contract_iud.robot`
      -> **5/5 PASS**, 0 failed.
- [x] 12. LIVE headless run — `EC_HEADLESS=true robot tests/Configuration/Assets/Contract_Objects/
      contract_iud.robot` -> attempt 1 hit a transient `Could not find active page` UI-timing flake
      (TC01 PASS, TC02-TC05 FAIL); retried ONCE per the workorder's instruction -> attempt 2:
      **5/5 PASS** (TC01-TC05). Kept: `evidence/backfill_2026-08-27/log.html`/`report.html`/
      `output.xml`.
- [x] 13. DB ground-truth — fresh `oracledb` connection (same resolution as `libraries/
      DbVerify.py`), read-only: `SELECT COUNT(*) FROM OV_CONTRACT WHERE CODE =
      'AUTOTEST_CONTRACT'` = 0, `SELECT COUNT(*) FROM OV_CONTRACT WHERE CODE LIKE 'AUTOTEST%'` = 0
      — run AFTER the clean 5/5 live run. See `evidence/backfill_2026-08-27/
      db_selfclean_check_output.txt`.
- [x] 14. FULL I-U-D scope — Insert (TC02) + Update (TC03) + Delete (TC05) all present and passing.
- [x] 15. Self-clean confirmed — independent fresh-connection DB re-read = 0 residual (item 13);
      no pre-existing production rows touched.
- [x] 16. Hygiene PASS — `py scripts/check_bundle_hygiene.py` -> `RESULT: PASS` (no hardcoded
      creds/R16, pure ASCII/R20, no CHECKLIST/VERIFY-REPORT contradiction across the tree). The
      run's only WARN is 2 pre-existing hardcoded-credential lines in **Contract_Area's**
      `investigation/` recon script — a different screen, not touched here.

## D. Delivery
- [x] 17. Registry row — already present/updated by PR #546 in `docs/ec_screen_registry.md`
      (`| Contract | Configuration > Assets > Contract_Objects > Contract (CO.2016) | ... FULL
      Area-pattern conversion (2026-08-26) ...`). Not re-appended by this backfill.
- [x] 18. Scorecard row — already present/updated by PR #546 in `docs/automation-scorecard.md`
      (`| Contract (OV-GM, CO.2016) | OK Done 2026-08-26 - FULL Area-pattern conversion ...`). Not
      re-appended by this backfill.
- [ ] 19. PR (R9 6-field body) — CANNOT be ticked here: this file is written BEFORE the backfill's
      own PR exists. Ticked in the PR body, never at scaffold time (lesson #235).

## E. Knowledge base
- [x] 20. KB selector map `ec-ui-knowledge/screens/contract.md` — created 2026-08-27 by this
      backfill (did not previously exist), transcribed from `contract_page.resource`'s own
      Variables section.
- [x] 21. Reuse clause — this is a backfill of an already-implemented, already-merged conversion
      (PR #546): JOURNAL + evidence + KB map are exactly what this task adds; tests/registry/
      scorecard already existed and were not re-done.

_Gates 10-16 were run directly by this backfill task (not `scripts/verify_screen.py`, which
requires building/registering a fresh bundle — this is evidence capture of an already-proven
suite, per the workorder's explicit instruction not to re-verify from scratch). Real command
output for every ticked item lives in `evidence/backfill_2026-08-27/`._
