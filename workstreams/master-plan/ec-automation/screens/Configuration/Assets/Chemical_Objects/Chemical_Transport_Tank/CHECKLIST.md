# IUD Task — Deliverable Checklist — Chemical Transport Tank (CO.0257)

_Copied from `docs/IUD-DELIVERABLE-CHECKLIST.md`. Backfilled 2026-08-28 (lean-deliverable backfill,
Batch 9) per owner decision 2026-08-27 (Section H retires the 2026-08-23/26 lean waiver for
Bank-/Area-pattern conversions, except items 4/5 which stay permanently waived — Universal Screen
Engine replaces the Playwright-driver role). Screen is a plain Bank-pattern OV (no navigator),
converted via `ec-bank-pattern-converter` in PR #461 (Batch 8, merged 2026-08-23). Distinct from
"Chemical Tank" (Area-pattern OV-GM, backfilled separately in Batch 4)._

## Step 0. CHECK-EXISTING-FIRST GATE
- [x] **0a.** `ec-ui-knowledge/screens/chemical_transport_tank.md` existed (from the 2026-07-26
      build) — refreshed by this backfill rather than re-scanned from scratch.
- [x] **0b.** `grep -ril "chemical_transport_tank" workstreams/master-plan/ec-automation/{py,pageobjects,tests,screens}`
      → found: T3, suite, Playwright driver, bundle all already existed → this is a doc/evidence
      backfill of already-working automation, not a new build.
- [x] **0c.** No engine/T1/T2 changes made or needed; PR #461 reused `resources/manage_object.resource`
      + `resources/common.resource` as-is (confirmed via PR #461 body).

## A. Bundle artifacts — `screens/Configuration/Assets/Chemical_Objects/Chemical_Transport_Tank/`
- [x] **1. `chemical_transport_tank_sow.md`** — updated 2026-08-28 to describe the real Batch 8
      conversion (was describing the superseded 2026-07-26 build).
- [x] **2. `README.md`** — updated 2026-08-28 with exact dryrun/live/DB-self-clean commands.
- [x] **3. `JOURNAL.md`** — updated 2026-08-28; Built/Done well/Done wrong/Blockers/Decisions/
      Evidence sections pulled from PR #461's real body + this backfill's own re-run.
- [ ] **4. Playwright bundle** — **N/A, permanently waived** (Section H): Universal Screen Engine
      replaces this role; existing `py/chemical_transport_tank_iud.py` from the 2026-07-26 build is
      left untouched, not rebuilt.
- [ ] **5. `investigation/`** — **N/A, permanently waived** (Section H), same reasoning; the
      existing `investigation/recon.py` from 2026-07-26 is left untouched, not rebuilt.
- [x] **6. `evidence/`** — refreshed: `evidence/pre-batch8-2026-07-26/` (original build's
      screenshots + `rf_report.html`, kept for history) + new `evidence/batch8-live-2026-08-28/`
      (this backfill's fresh dryrun + live run of the CURRENT 5-TC suite: per-TC screenshots +
      `log.html`/`output.xml`/`report.html`).
- [x] **7. `CHECKLIST.md`** — this file.

## B. RF files (pre-existing, unmodified by this backfill)
- [x] **8. T3** `pageobjects/Configuration/Assets/Chemical_Objects/chemical_transport_tank_page.resource`
      — label-driven, properties-file-driven, rebuilt in PR #461 (2026-08-23).
- [x] **9. Suite** `tests/Configuration/Assets/Chemical_Objects/chemical_transport_tank_iud.robot`
      — TC01 clean-state → TC02 insert → TC03 update → TC04 find → TC05 delete.

## C. Verification gates (re-run for this backfill; original evidence from PR #461)
- [x] **10. robocop** — not re-run standalone by this backfill (no RF files touched); PR #461's
      merge already gated on it. Not re-claimed here beyond that.
- [x] **11. `--dryrun` N/N PASS** — **5/5 PASS**, this backfill, 2026-08-28
      (`Workplaces/chemical-transport-tank-backfill/dryrun/`, `output.xml`/`log.html`/`report.html`).
- [x] **12. LIVE headless run N/N PASS** — **5/5 PASS**, this backfill, 2026-08-28, first attempt,
      `EC_HEADLESS=true` (`evidence/batch8-live-2026-08-28/`).
- [x] **13. DB ground-truth** — TC01 `Verify Object Does Not Exist` → `Code Should Be Absent In View
      OV_CHEM_TRANS_TANK`; TC05 `Verify Object Removed` → same keyword post-delete. Both ran and
      passed inside this backfill's live run (`libraries/DbVerify.py`). A standalone `oracledb`
      connection attempted from the local shell (outside the suite) timed out on the network path —
      disclosed honestly rather than silently retried; the in-suite DB assertions are the real
      ground truth and both passed.
- [x] **14. FULL I-U-D scope** — Insert + Update + Delete all present and exercised (TC02/TC03/TC05).
- [x] **15. Self-clean confirmed** — TC01 (pre) + TC05 (post) both assert absence in
      `OV_CHEM_TRANS_TANK` via DB query; PR #461's original merge additionally confirmed via a fresh
      standalone connection (0 residual `AUTOTEST%` rows).
- [x] **16. Hygiene PASS** — not re-run standalone by this backfill (no code/test-data files
      touched); PR #461's merge already gated on it.

## D. Delivery
- [x] **17. Registry row** — `docs/ec_screen_registry.md` (Chemical Transport Tank row, updated in
      place by PR #461, describes the Batch 8 conversion). Not modified by this backfill.
- [x] **18. Scorecard row** — `docs/automation-scorecard.md` (repo root), updated in place by
      PR #461. Not modified by this backfill.
- [x] **19. PR** — this backfill's own PR (R9 6-field body); base branch master; never self-merge.

## E. Knowledge base
- [x] **20. KB selector map** `ec-ui-knowledge/screens/chemical_transport_tank.md` — refreshed
      2026-08-28 to cite the Batch 8 grid-filter keywords and 5-TC structure (was describing the
      2026-07-26 4-TC build).
- [x] **21. Reuse clause** — this IS the reuse-clause case: Step 0 found the screen already fully
      implemented; this backfill produced/refreshed exactly #3 (JOURNAL), #6 (evidence), and #20
      (KB map) as required, plus #1/#2/#7 per the Section H restoration.
