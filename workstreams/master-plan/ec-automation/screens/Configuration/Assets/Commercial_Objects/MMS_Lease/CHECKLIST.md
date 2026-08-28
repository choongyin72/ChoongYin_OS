# IUD Task — Deliverable Checklist — MMS Lease

Copied from `docs/IUD-DELIVERABLE-CHECKLIST.md`. Backfill per
`docs/lean-deliverable-backfill-workorder.md` Batch 6 (owner decision 2026-08-27, Section H
retires the 2026-08-23/26 lean waiver except items 4/5, which stay waived). Ticks below cite
real evidence from PR #437 (merged 2026-08-23) plus this backfill's own re-run
(2026-08-28) — none are hand-typed without a command behind them.

## Step 0. CHECK-EXISTING-FIRST GATE
- [x] **0a.** `ec-ui-knowledge/screens/mms_lease.md` did not exist before this backfill — created now (item 20).
- [x] **0b.** `grep -ril "mms_lease" workstreams/master-plan/ec-automation/{py,pageobjects,tests,screens}` →
      found existing impl: `pageobjects/Configuration/Assets/Commercial_Objects/mms_lease_page.resource` +
      `tests/Configuration/Assets/Commercial_Objects/mms_lease_iud.robot` (Bank-pattern, PR #437) — REUSED, not
      rebuilt. This backfill adds documentation/evidence only.
- [x] **0c.** Screen uses the shared T2 (`resources/manage_object.resource`) + T1 (`resources/common.resource`)
      pattern, not a new engine — confirmed via the T3's `Resource` imports.

## A. Bundle artifacts — `screens/Configuration/Assets/Commercial_Objects/MMS_Lease/`
- [x] **1. `mms_lease_sow.md`** — updated 2026-08-28 with real classification/fields/dev-story pulled from PR #437's body.
- [x] **2. `README.md`** — updated 2026-08-28 with exact dryrun/live/DB self-clean commands.
- [x] **3. `JOURNAL.md`** — added 2026-08-28, modeled on Bank's JOURNAL.md, real content from PR #437.
- [ ] **4. `playwright/ec_iud_<slug>.py`** — WAIVED (Section H, unchanged from Section G). Legacy driver
      `playwright/ec_iud_mms_lease.py` predates the Bank-pattern conversion and is kept for reference only;
      no new Playwright work done.
- [ ] **5. `investigation/`** — WAIVED (Section H, unchanged from Section G). Legacy recon scripts kept as-is.
- [x] **6. `evidence/`** — added `evidence/rf_bank_pattern_2026-08-28/` (dryrun_output.xml, output.xml,
      log.html, report.html, results_summary.md) from a real re-run of the already-merged suite.
- [x] **7. `CHECKLIST.md`** — this file.

## B. RF files — treeview-mirrored (pre-existing, NOT modified by this backfill)
- [x] **8. T3 page object** `pageobjects/Configuration/Assets/Commercial_Objects/mms_lease_page.resource` —
      pre-existing (PR #437), locators in Variables, docstring matches Variables.
- [x] **9. Suite** `tests/Configuration/Assets/Commercial_Objects/mms_lease_iud.robot` — pre-existing
      (PR #437), TC01 clean-state -> TC02 insert -> TC03 update -> TC04 find -> TC05 delete.

## C. Verification gates
- [x] **10. robocop clean (baseline-matched)** — `py -m robocop check pageobjects/.../mms_lease_page.resource
      tests/.../mms_lease_iud.robot` = **9 issues (4 VAR02 + 5 DOC02)**, re-run 2026-08-28, identical
      count/kind to PR #437's cited Bank/Country baseline (not zero, but an accepted stable characteristic
      of this pattern family, same standard applied to every other Batch 2-4 sibling).
- [x] **11. `--dryrun` N/N PASS** — `robot --dryrun tests/Configuration/Assets/Commercial_Objects/mms_lease_iud.robot`
      → **5/5 PASS**, re-run 2026-08-28 (`evidence/rf_bank_pattern_2026-08-28/dryrun_output.xml`).
- [x] **12. LIVE headed/headless run N/N PASS** — `EC_HEADLESS=true robot
      tests/Configuration/Assets/Commercial_Objects/mms_lease_iud.robot` → **5/5 PASS**, re-run 2026-08-28
      (`evidence/rf_bank_pattern_2026-08-28/output.xml` + `log.html` + `report.html`).
- [x] **13. DB ground-truth** — `SELECT COUNT(*) FROM OV_MMS_LEASE WHERE CODE = 'AUTOTEST_MMS_LEASE'` via a
      fresh `oracledb` connection (ECKERNEL_EC/localhost:1521/ORCL): **0 before** the live run, **0 after**
      (row inserted by TC02, updated by TC03, deleted by TC05 — each op DB-verified in-suite via `DbVerify.py`
      plus this backfill's own before/after count).
- [x] **14. FULL I-U-D scope** — TC02 Insert, TC03 Update, TC04 Find/verify, TC05 Delete all present and
      PASS (not I/D only).
- [x] **15. Self-clean confirmed** — independent fresh-connection re-read = **0 residual**
      `AUTOTEST_MMS_LEASE` rows after the 2026-08-28 live re-run.
- [x] **16. Hygiene PASS** — `py scripts/check_bundle_hygiene.py` (repo root) → `RESULT: PASS - no
      hardcoded creds (R16), pure ASCII (R20), no CHECKLIST/VERIFY-REPORT contradictions, doc rows match
      declared families`. (One WARN line in that run belongs to a different screen, Contract_Area, not MMS Lease.)

## D. Delivery
- [x] **17. Registry row** — already present in `docs/ec_screen_registry.md` (row for MMS Lease, added at
      PR #437's merge, 2026-08-23) — no change needed, verified present.
- [x] **18. Scorecard row** — already present in `docs/automation-scorecard.md` (added at PR #437's merge)
      — no change needed, verified present.
- [x] **19. PR** — this backfill PR uses the standard body (What was backfilled / Files added / Base
      branch = master); never self-merged.

## E. Knowledge base
- [x] **20. KB selector map** `ec-ui-knowledge/screens/mms_lease.md` — added by this backfill, transcribed
      from the T3's own Variables section (nav path, DB view, grid id, insert/update/delete selectors,
      mandatory fields, quirks, last-verified 2026-08-28).
- [x] **21. Reuse clause** — Step 0 found MMS Lease already implemented (PR #437); this backfill is exactly
      the "reuse run" the clause requires: JOURNAL + evidence + KB map produced/refreshed, not just green tests.

## Overall

**Items 4 and 5 are explicitly waived** (Universal Screen Engine supersedes the Playwright bundle role,
per Section H). **All other items (0, 1, 2, 3, 6-21) are complete with real evidence cited above.** No
RF/pageobject automation file was modified to produce this bundle.
