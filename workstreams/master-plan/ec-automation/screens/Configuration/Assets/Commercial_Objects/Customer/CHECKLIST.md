# IUD Task — Deliverable Checklist — Customer

Copy of `docs/IUD-DELIVERABLE-CHECKLIST.md`, ticked with real evidence for the Customer screen
(Bank-pattern RF conversion, PR #435, merged 2026-08-23; documentation backfill, this PR,
2026-08-28, per `docs/lean-deliverable-backfill-workorder.md` Batch 6 / CHECKLIST Section H).

## Step 0. CHECK-EXISTING-FIRST GATE
- [x] **0a.** No `ec-ui-knowledge/screens/customer.md` existed before this backfill (confirmed:
      `ls ec-ui-knowledge/screens/ | grep -i custom` → no hit) — created fresh as item #20 below.
- [x] **0b.** `grep -ril customer_page.resource workstreams/master-plan/ec-automation` →
      existing impl found: `pageobjects/Configuration/Assets/Commercial_Objects/customer_page.resource`
      + `tests/Configuration/Assets/Commercial_Objects/customer_iud.robot` (already merged,
      PR #435). This task REUSES it — no parallel copy built.
- [x] **0c.** RF suite reuses the shared T2 `manage_object.resource` + T1 `common.resource` (via
      the page object's `Resource` imports) — confirmed by reading `customer_page.resource` lines 12-13.

## A. Bundle artifacts — `screens/Configuration/Assets/Commercial_Objects/Customer/`
- [x] **1. `customer_sow.md`** — updated 2026-08-28: classification (plain Bank-pattern OV, no
      navigator), grid id, mandatory fields, test data, dev story pulled from PR #435's body.
- [x] **2. `README.md`** — updated 2026-08-28: bundle overview + exact dryrun/live/robocop
      commands + DB self-clean scratch-script pattern.
- [x] **3. `JOURNAL.md`** — new, modeled on Bank's JOURNAL.md structure, content pulled from
      PR #435's real body (Built/Done well/Done wrong/Blockers/Decisions/Evidence).
- [ ] **4. `playwright/ec_iud_<slug>.py`** — N/A, permanently waived for Bank-pattern work
      (Universal Screen Engine replaces this role, CHECKLIST Section H). This bundle already
      has a legacy `playwright/ec_iud_customer.py` from the pre-conversion 2026-06-12 build —
      left untouched, not rebuilt.
- [ ] **5. `investigation/`** — N/A, same waiver as #4. Legacy `investigation/*.py` from the
      2026-06-12 build left untouched.
- [x] **6. `evidence/`** — pre-existing legacy screenshots (`customer_0[1-8]_*.png` +
      `customer_results.json`, 2026-06-12) plus new `rf_backfill_2026-08-28/` folder: one live
      re-run of `customer_iud.robot` (`EC_HEADLESS=true`), `log.html`/`report.html`/`output.xml`
      + `results_summary.md`.
- [x] **7. `CHECKLIST.md`** — this file.

## B. RF files — treeview-mirrored (pre-existing, merged PR #435 — NOT modified by this backfill)
- [x] **8. T3 page object** `pageobjects/Configuration/Assets/Commercial_Objects/customer_page.resource`
      — pre-existing, read-only this session.
- [x] **9. Suite** `tests/Configuration/Assets/Commercial_Objects/customer_iud.robot` — TC01
      clean-state -> TC02 insert -> TC03 update -> TC04 find -> TC05 delete/cleanup. Pre-existing,
      read-only this session.

## C. Verification gates
- [x] **10. robocop clean (relative)** — `py -m robocop check customer_page.resource
      customer_iud.robot` = 7 issues (2 VAR02 + 5 DOC02), 2026-08-28 re-run — identical count to
      PR #435's cited baseline (below the established 9-issue baseline for this project).
- [x] **11. `--dryrun` N/N PASS** — full-tree `py -m robot --dryrun tests/` = 883/883 PASS,
      2026-08-28 (tree has grown since PR #435's cited 735/735 at merge time; both are 100%).
- [x] **12. LIVE headless run N/N PASS** — `EC_HEADLESS=true py -m robot
      tests/Configuration/Assets/Commercial_Objects/customer_iud.robot` = 5/5 PASS, 2026-08-28
      (TC01-TC05). Matches PR #435's original live 5/5.
- [x] **13. DB ground-truth** — `SELECT COUNT(*) FROM OV_CUSTOMER WHERE CODE = 'AUTOTEST_CUST'`
      via a fresh oracledb connection (ECKERNEL_EC/energy@localhost:1521/ORCL) = 0, run
      immediately after the 2026-08-28 live suite completed.
- [x] **14. FULL I-U-D scope** — TC02 Insert, TC03 Update, TC05 Delete all present and PASS (not
      I/D only); TC04 Find/round-trip also present.
- [x] **15. Self-clean confirmed** — independent DB re-read (fresh connection) = 0 residual
      `AUTOTEST_CUST` rows after the 2026-08-28 run.
- [x] **16. Hygiene PASS** — `py scripts/check_bundle_hygiene.py` → `RESULT: PASS` (no hardcoded
      creds, pure ASCII, no CHECKLIST/VERIFY-REPORT contradiction, doc rows match declared
      families). The scan's one WARN belongs to an unrelated bundle (Contract Area), not Customer.

## D. Delivery
- [x] **17. Registry row** — already present in `docs/ec_screen_registry.md` (Customer row,
      appended by PR #435, 2026-08-23). No change needed this backfill.
- [x] **18. Scorecard row** — already present in `docs/automation-scorecard.md` (appended by
      PR #435). No change needed this backfill.
- [x] **19. PR** — this backfill PR uses the standard body (What was backfilled / Files added /
      Base branch = master); never self-merged.

## E. Knowledge base
- [x] **20. KB selector map** `ec-ui-knowledge/screens/customer.md` — new, created 2026-08-28,
      transcribed from `customer_page.resource`'s Variables section (grid id, form-label list,
      delete End-Date field id) — nothing re-discovered live.
- [x] **21. Reuse clause** — Step 0 found the screen ALREADY implemented (PR #435); this backfill
      produces the required deliverables (#3 JOURNAL, #6 evidence, #20 KB map) rather than
      declaring done on green tests alone.

---

**Overall for this backfill PR: SOW/README/JOURNAL/evidence/CHECKLIST/KB map added; RF
automation NOT modified; live 5/5 + dryrun 883/883 + DB self-clean 0 residual + hygiene PASS
all independently re-confirmed 2026-08-28.**
