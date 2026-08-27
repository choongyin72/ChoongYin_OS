# Operator Lease — IUD Deliverable Checklist (vs docs/IUD-DELIVERABLE-CHECKLIST.md, Section H shape)

_Written 2026-08-28 (deliverable backfill, `docs/lean-deliverable-backfill-workorder.md` Batch 6)
per Section H's restored items (SOW/README/JOURNAL/evidence/CHECKLIST/KB map). Items 4/5
(Playwright driver + investigation/) stay permanently waived for Bank-/Area-pattern work — the
Universal Screen Engine replaces that role; the original 2026-06-12 Playwright driver and its
investigation/ recon scripts are left as-is, unmodified._

## Step 0 — check-existing gate
- [x] 0a KB map created (`ec-ui-knowledge/screens/operator_lease.md`, this backfill — did not
      previously exist).
- [x] 0b `grep -ril "operator_lease_page.resource"` -> confirmed the real, already-existing files:
      T3 `pageobjects/Configuration/Assets/Commercial_Objects/operator_lease_page.resource`, suite
      `tests/Configuration/Assets/Commercial_Objects/operator_lease_iud.robot`. Existing impl
      reused, never duplicated.
- [x] 0c reused shared engine (`resources/manage_object.resource`'s T2 keywords, e.g. `Find/Clear
      Object Row By Filter`) + `DbVerify.py` + T1 (`resources/common.resource`) — no shared-file
      edits this task.

## A. Bundle artifacts (`screens/Configuration/Assets/Commercial_Objects/Operator_Lease/`)
- [x] 1. `operator_lease_sow.md` — Section 6 added 2026-08-28 with the PR #436 Bank-pattern
      conversion story; original 2026-06-12 sections kept as history.
- [x] 2. `README.md` — rewritten 2026-08-28: bundle overview + exact dryrun/live/DB-self-clean
      commands, matching the RF suite that actually exists now (not the pre-conversion Playwright-
      only framing).
- [x] 3. `JOURNAL.md` — new 2026-08-28: Built/Done well/Done wrong/Blockers->resolution/Decisions/
      Evidence, modeled on Bank's JOURNAL.md.
- [ ] 4. Playwright flow — **N/A / permanently waived** (Section H): `playwright/
      ec_iud_operator_lease.py` predates the lean rule and is left unmodified; the Universal Screen
      Engine replaces this role for new work.
- [ ] 5. `investigation/` — **N/A / permanently waived** (Section H): pre-existing
      `commercial_objects_recon.py`/`probe_com_rejects.py` from the original 2026-06-12 build are
      left unmodified; no new recon scripts needed for a documentation-only backfill of
      already-working automation.
- [x] 6. `evidence/` — original `operator_lease_0[1-8]_*.png` + `operator_lease_results.json`
      (2026-06-12) preserved; added `evidence/backfill_2026-08-28/` (robocop, dryrun 5/5, full-tree
      dryrun 883/883, live 5/5 — no retry needed, DB self-clean before+after, hygiene re-check,
      `results_summary.md`).
- [x] 7. `CHECKLIST.md` — this file, new 2026-08-28.

## B. RF files (pre-existing, NOT modified by this backfill)
- [x] 8. T3 `pageobjects/Configuration/Assets/Commercial_Objects/operator_lease_page.resource` —
      label-driven, per-TC login, `Find/Clear Operator Lease Row By Filter`, mandatory Operator
      Lease Code/Operator Lease Name/Start Date on Insert; Code/Name only on Update.
- [x] 9. Suite `tests/Configuration/Assets/Commercial_Objects/operator_lease_iud.robot` — 5 TCs
      (clean-state/insert/update/find/delete), per-TC login/logout, fixed test code
      `AUTOTEST_OPERATOR_LEASE`.

## C. Verification gates (re-run for this backfill's evidence, not a fresh build cycle)
- [x] 10. Robocop — `py -m robocop check pageobjects/.../operator_lease_page.resource
      tests/.../operator_lease_iud.robot` -> **9 issues** (4x VAR02, 5x DOC02), exact parity with
      PR #436's own cited baseline (not a regression). See
      `evidence/backfill_2026-08-28/robocop_output.txt`.
- [x] 11. `--dryrun` — `py -m robot --dryrun tests/Configuration/Assets/Commercial_Objects/
      operator_lease_iud.robot` -> **5/5 PASS**, 0 failed. See
      `evidence/backfill_2026-08-28/dryrun_output.xml`. Full-tree parity check
      (`py -m robot --dryrun tests/`) -> **883/883 PASS**, see
      `evidence/backfill_2026-08-28/fulltree_dryrun_summary.txt` (raw output.xml was ~51 MB and not
      committed; summary retains the pass/fail counts).
- [x] 12. LIVE headless run — `EC_HEADLESS=true py -m robot tests/Configuration/Assets/
      Commercial_Objects/operator_lease_iud.robot` -> **5/5 PASS on attempt 1** (TC01-TC05), no
      retry needed. See `evidence/backfill_2026-08-28/live_log.html`/`live_report.html`/
      `live_output.xml`.
- [x] 13. DB ground-truth — fresh `oracledb` connection (`ECKERNEL_EC`/`localhost:1521/ORCL`),
      read-only: `SELECT COUNT(*) FROM OV_OPERATOR_LEASE WHERE CODE = 'AUTOTEST_OPERATOR_LEASE'` =
      0, `SELECT CODE FROM OV_OPERATOR_LEASE WHERE CODE LIKE 'AUTOTEST%'` = no rows — run BEFORE and
      AFTER the live run, same result both times. See "DB self-clean raw output" in
      `evidence/backfill_2026-08-28/results_summary.md`.
- [x] 14. FULL I-U-D scope — Insert (TC02) + Update (TC03) + Delete (TC05) all present and passing.
- [x] 15. Self-clean confirmed — independent fresh-connection DB re-read = 0 residual both before
      and after (item 13); no pre-existing production rows touched.
- [x] 16. Hygiene PASS — `py scripts/check_bundle_hygiene.py` (run from repo root) -> **RESULT:
      PASS** (exit 0) — no hardcoded creds (R16), pure ASCII (R20), no CHECKLIST/VERIFY-REPORT
      contradiction. Only WARN is 2 pre-existing hardcoded-credential lines in **Contract Area's**
      `investigation/` recon script — a different screen, not touched here. See
      `evidence/backfill_2026-08-28/hygiene_output.txt`.

## D. Delivery
- [x] 17. Registry row — already present/updated by PR #436 in `docs/ec_screen_registry.md`
      (`| Operator Lease | Configuration > Assets > Commercial Objects > Operator Lease | OV |
      OV_OPERATOR_LEASE | manage-object | ... |`). Not re-appended by this backfill.
- [x] 18. Scorecard row — already present/updated by PR #436 in `docs/automation-scorecard.md`
      (`| Operator Lease (OV, Commercial Objects, manage-object) | OK Done 2026-08-23 ... |`). Not
      re-appended by this backfill.
- [ ] 19. PR (R9 6-field body) — CANNOT be ticked here: this file is written BEFORE the backfill's
      own PR exists. Ticked in the PR body, never at scaffold time (lesson #235).

## E. Knowledge base
- [x] 20. KB selector map `ec-ui-knowledge/screens/operator_lease.md` — did NOT previously exist;
      created 2026-08-28 by this backfill, describing the current Bank-pattern RF suite (per-TC
      login, properties-driven, explicit filter wiring, TC04 Find).
- [x] 21. Reuse clause — this is a backfill of an already-implemented, already-merged conversion
      (PR #436): JOURNAL + evidence + KB map are exactly what this task adds; tests/registry/
      scorecard already existed and were not re-done.

_Gates 10-16 were run directly by this backfill task (not `scripts/verify_screen.py`, which
requires building/registering a fresh bundle — this is evidence capture of an already-proven suite,
per the workorder's explicit instruction not to re-verify from scratch). Real command output for
every ticked item lives in `evidence/backfill_2026-08-28/`._
