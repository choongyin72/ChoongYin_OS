# Orifice Plate — IUD Deliverable Checklist (vs `docs/IUD-DELIVERABLE-CHECKLIST.md`)

_Refreshed 2026-08-28 — lean-deliverable-backfill, Batch 10 (`docs/lean-deliverable-backfill-workorder.md`).
Per Section H of the checklist: items **4 (Playwright driver)** and **5 (investigation/)** stay
waived for Bank-pattern conversions (superseded by the Universal Screen Engine). All other items
apply in full and are ticked below with real evidence from this session + PR #463._

## Step 0 — check-existing gate
- [x] **0a** `ec-ui-knowledge/screens/orifice_plate.md` existed and was consulted/refreshed (not re-scanned from zero).
- [x] **0b** `grep -ril "orifice_plate" workstreams/master-plan/ec-automation/{py,pageobjects,tests,screens}`
      → found the existing PR #463 automation; this task REUSES/EXTENDS docs around it, builds no
      parallel copy.
- [x] **0c** Shared engine reused (T2 `resources/manage_object.resource` + `libraries/DbVerify.py`);
      zero engine changes this session.

## A. Bundle artifacts
- [x] **1.** `orifice_plate_sow.md` — refreshed to describe the current Bank-pattern automation.
- [x] **2.** `README.md` — refreshed with real run commands + this session's verified numbers.
- [x] **3.** `JOURNAL.md` — refreshed: original 2026-07-26 entry kept, PR #463's real conversion
      narrative added, plus this backfill session's own entry.
- [ ] **4.** Playwright driver — **N/A, waived** (Section H) — `py/orifice_plate_iud.py` exists
      pre-PR#463 and is untouched; the Universal Screen Engine is the owner-decided replacement
      going forward, not a per-screen rebuild.
- [ ] **5.** `investigation/` — **N/A, waived** (Section H) — pre-existing `recon.py` left as-is;
      no new investigation/ deliverable required for this backfill.
- [x] **6.** `evidence/` — refreshed: replaced the stale 2026-07-26 5-screenshot set with the
      2026-08-28 live re-run's full per-TC screenshot set + `rf_log/report/output` (see evidence/).
- [x] **7.** `CHECKLIST.md` — this file.

## B. RF files (pre-existing, untouched by this backfill)
- [x] **8.** T3 `pageobjects/Configuration/Assets/Stream_Objects/orifice_plate_page.resource` —
      rebuilt in PR #463 (2026-08-23); confirmed present and unmodified this session.
- [x] **9.** Suite `tests/Configuration/Assets/Stream_Objects/orifice_plate_iud.robot` — 5 TCs
      (Verify-Clean-State / Insert / Update / Find / Delete); confirmed present and unmodified.

## C. Verification gates (re-run this session, 2026-08-28, from `workstreams/master-plan/ec-automation/`)
- [x] **10.** robocop — `py -m robocop check pageobjects/.../orifice_plate_page.resource
      tests/.../orifice_plate_iud.robot` → **9 issues** (1x VAR02 + 5x DOC02) — matches PR #463's
      own citation and the accepted Batch 7 `berth_iud.robot` pattern (no page-object issues).
- [x] **11.** `robot --dryrun` → **5/5 PASS**, 0 fail.
- [x] **12.** LIVE run — `EC_HEADLESS=true robot tests/.../orifice_plate_iud.robot` → **5/5 PASS**,
      0 fail. (Evidence: `evidence/rf_log_2026-08-28.html` / `rf_report_2026-08-28.html`.)
- [x] **13.** DB ground-truth — suite's own `Code Should Be Present/Absent In View
      OV_ORIFICE_PLATE` + `Field Should Equal In View OV_ORIFICE_PLATE <code> NAME` (update);
      independently re-confirmed this session via a fresh `oracledb` connection query
      (`SELECT COUNT(*) FROM OV_ORIFICE_PLATE WHERE CODE LIKE 'AUTOTEST%'` → 0).
- [x] **14.** FULL I-U-D scope — Insert (TC02) + Update (TC03) + Find (TC04) + Delete (TC05), all present.
- [x] **15.** Self-clean confirmed — fresh-connection DB re-read = **0** residual `AUTOTEST%` rows
      in `OV_ORIFICE_PLATE`, both before and after the 2026-08-28 live run.
- [x] **16.** Hygiene — `py scripts/check_bundle_hygiene.py` (repo root) → **PASS** (no hardcoded
      creds/ASCII issue for this bundle; the run's one WARN is a pre-existing, unrelated
      Contract_Area recon script).

## D. Delivery
- [x] **17.** Registry row — already present in `docs/ec_screen_registry.md` (line ~278, "OV (Bank
      family) — FULL Bank-pattern", added/modified by PR #463); no change needed this session.
- [x] **18.** Scorecard row — already present in `docs/automation-scorecard.md` (line ~170, "Done
      2026-08-23 (Batch 8) — upgraded to FULL Bank-pattern"); no change needed this session.
- [x] **19.** PR — this backfill's own PR (docs-only, standard 6-field body), base branch master,
      never self-merged.

## E. Knowledge base
- [x] **20.** KB selector map `ec-ui-knowledge/screens/orifice_plate.md` — refreshed this session
      (was stale at the 2026-07-26/4-TC/no-filter build; now reflects PR #463's 5-TC/grid-filter/
      dedicated-credential shape).
- [x] **21.** Reuse clause — applies: Step 0 found the screen already implemented (PR #463); this
      session produced/refreshed the required deliverables around it (JOURNAL, evidence, KB map,
      SOW, README, this CHECKLIST) rather than declaring "done" on green tests alone.
