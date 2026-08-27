# Port — IUD Deliverable Checklist (vs docs/IUD-DELIVERABLE-CHECKLIST.md)

_Backfilled 2026-08-28 (Batch 10, `docs/lean-deliverable-backfill-workorder.md`) — the doc bundle
(SOW/README/JOURNAL/evidence/KB map) was refreshed to reflect the current Bank-pattern shape from
PR #465 (merged 2026-08-23); the RF automation itself was NOT re-built or modified by this backfill.
Items 4 (Playwright driver) and 5 (investigation/) stay as-is from the original build (Section H:
these two are permanently waived for Bank-/Area-pattern work going forward, but the pre-existing
ones were left in place, not deleted)._

## Step 0 — check-existing gate
- [x] 0a. KB map exists (`ec-ui-knowledge/screens/port.md`) — refreshed by this backfill to the
  current Batch-9 shape.
- [x] 0b. `grep -ril port_page.resource workstreams/master-plan/ec-automation` -> found existing
  impl (`pageobjects/Configuration/Assets/Transport_Objects/port_page.resource`), already the full
  Bank-pattern shape from PR #465. Backfill REUSED/DOCUMENTED it, did not build a parallel copy.
- [x] 0c. Confirmed via registry row + PR #465 body that the shared engine/T2 (`manage_object.resource`)
  is what the T3 delegates to; no new plumbing added.

## A. Bundle artifacts — `screens/Configuration/Assets/Transport_Objects/Port/`
- [x] 1. `port_sow.md` — refreshed 2026-08-28: classification (plain Bank-pattern OV, no navigator),
  grid id, mandatory fields, test data, dev story pulled from PR #465's real body.
- [x] 2. `README.md` — refreshed 2026-08-28: bundle overview + exact dryrun/live/robocop/hygiene/
  DB-self-clean commands.
- [x] 3. `JOURNAL.md` — refreshed 2026-08-28: Built/Done well/Done wrong/Blockers/Decisions/Evidence,
  covering both the 2026-07-26 original build and the 2026-08-23 Batch-9 conversion (PR #465), real
  content pulled from the merged PR body.
- [ ] 4. Playwright driver — **N/A, permanently waived** for Bank-pattern conversions (Section H,
  `docs/IUD-DELIVERABLE-CHECKLIST.md`; Universal Screen Engine is the replacement going forward).
  Pre-existing `py/port_iud.py` (from the 2026-07-26 build) left untouched, not rebuilt.
- [ ] 5. `investigation/` — **N/A, permanently waived** for Bank-pattern conversions (same Section H).
  Pre-existing `investigation/recon.py` (from the 2026-07-26 build) left untouched.
- [x] 6. `evidence/` — this backfill's fresh live RF run (2026-08-28): `TC0[1-5] *.png` +
  `log.html`/`output.xml`/`report.html`, 5/5 pass. Pre-existing 2026-07-26 evidence
  (`port_0[1-5]_*.png` + `rf_report.html`) kept alongside as historical record, not overwritten.
- [x] 7. `CHECKLIST.md` — this file, refreshed 2026-08-28.

## B. RF files — unchanged by this backfill, current shape confirmed live
- [x] 8. T3 `pageobjects/Configuration/Assets/Transport_Objects/port_page.resource` — label-driven,
  properties-file-driven, grid-filter-wired (PR #465 shape, confirmed live by this backfill).
- [x] 9. Suite `tests/Configuration/Assets/Transport_Objects/port_iud.robot` — 5 TCs (Verify Clean
  State/Insert/Update/Find/Delete), per-TC login/logout, fixed test code `AUTOTEST_PORT`.

## C. Verification gates (evidence from this backfill's own re-run, 2026-08-28)
- [x] 10. robocop clean (parity) — `py -m robocop check port_page.resource port_iud.robot` -> **9
  issues** (4 VAR02 + 5 DOC02-style), same count/kind as Berth's own established baseline (not a
  regression, matches PR #465's own citation).
- [x] 11. `--dryrun` — `py -m robot --dryrun tests/.../port_iud.robot` -> **5/5 PASS, 0 fail**.
- [x] 12. LIVE headless run — `EC_HEADLESS=true py -m robot tests/.../port_iud.robot` -> **5/5 PASS,
  0 fail** (TC01-TC05).
- [x] 13. DB ground-truth — grid-check + form-check against `OV_PORT` inside the shared T2
  (`Verify Object Insert Exists`/`Verify Object Form Record`/`Verify Object Found`/`Verify Object
  Removed`); explicit fresh-connection query used for self-clean:
  `SELECT COUNT(*) FROM OV_PORT WHERE CODE LIKE 'AUTOTEST%'`.
- [x] 14. FULL I-U-D scope — Insert (TC02) + Update (TC03) + Find (TC04) + Delete (TC05) all present
  and passing.
- [x] 15. Self-clean confirmed — fresh `oracledb` connection (independent of the RF run's own
  in-suite checks), `SELECT COUNT(*) FROM OV_PORT WHERE CODE LIKE 'AUTOTEST%'` = **0** (checked
  after the live run completed).
- [x] 16. Hygiene PASS — `py scripts/check_bundle_hygiene.py --bundle
  screens/Configuration/Assets/Transport_Objects/Port` -> **PASS** (no hardcoded creds, pure ASCII,
  no CHECKLIST/VERIFY-REPORT contradiction).

## D. Delivery
- [x] 17. Registry row — already present, updated by PR #465 (`docs/ec_screen_registry.md`, Port row
  describes the full Batch-9 conversion). Not re-touched by this backfill.
- [x] 18. Scorecard row — already present, updated by PR #465 (`docs/automation-scorecard.md`). Not
  re-touched by this backfill.
- [x] 19. PR — this backfill's own PR (branch `docs/port-backfill-artifacts`, base master, standard
  6-field body); never self-merged.

## E. Knowledge base
- [x] 20. KB map `ec-ui-knowledge/screens/port.md` — refreshed 2026-08-28 to describe the current
  properties-file-driven, grid-filter-wired, 5-TC shape (was previously dated 2026-07-26, describing
  the superseded 4-TC build).
- [x] 21. Reuse clause — this IS a reuse/backfill run (Step 0 found existing automation already
  built and merged); per the reuse clause, JOURNAL + evidence + KB map are the deliverables this
  backfill produces — all three refreshed above, alongside SOW/README/CHECKLIST.

_Gates 10-16 run directly by this backfill (robocop/robot/hygiene/DB-query commands, cited above with
real exit codes/counts) rather than via `scripts/verify_screen.py` — that tool's own auto-generated
`VERIFY-REPORT.md` in this bundle is the ORIGINAL 2026-07-26 report and predates the Batch-9
conversion; it is kept as a historical record, not re-run, since this backfill's scope per
`docs/lean-deliverable-backfill-workorder.md` is documentation/evidence, not re-verification via that
specific tool. No claim above rides on an un-run command._
