# Reservoir Formation - IUD Deliverable Checklist (vs docs/IUD-DELIVERABLE-CHECKLIST.md)

_Backfilled 2026-08-28 per `docs/lean-deliverable-backfill-workorder.md` Batch 10 (owner decision
2026-08-27 retired Section G's lean waiver for items 1/3/6/7/20; items 4/5 stay permanently waived,
superseded by the Universal Screen Engine). The RF automation itself (items 8/9) is PR #467's
2026-08-23 Batch 9 build - NOT re-built or modified by this backfill._

## Step 0 - check-existing gate
- [x] 0a KB map existed (`ec-ui-knowledge/screens/reservoir_formation.md`, from 2026-07-26) - refreshed
      by this backfill to reflect the Batch 9 build, not re-scanned from scratch.
- [x] 0b grep `workstreams/master-plan/ec-automation/{py,pageobjects,tests,screens}` for
      `reservoir_formation` -> only this screen's own files; no parallel copy.
- [x] 0c reused shared engine + T2 (`manage_object.resource`) + `DbVerify.py` - Batch 9 added no new
      shared-file changes (grid-filter wiring is existing T2 keywords, `Find/Clear Object Row By
      Filter`, already used by Bank/Berth/Account/State).

## A. Bundle artifacts
- [x] 1 `reservoir_formation_sow.md` - rewritten this backfill to reflect Batch 9 (was the stale
      2026-07-26 4/4-era content).
- [x] 2 `README.md` - rewritten this backfill: exact dryrun/live/DB-self-clean commands.
- [x] 3 `JOURNAL.md` - rewritten this backfill per Bank's JOURNAL.md shape (Built/Done well/Done
      wrong/Blockers/Decisions/Evidence), sourced from PR #467's real body + the 2026-07-26 history.
- [ ] 4 Playwright flow - **N/A, permanently waived** (`docs/IUD-DELIVERABLE-CHECKLIST.md` Section H):
      `py/reservoir_formation_iud.py` stays as-is, superseded by the Universal Screen Engine; not
      rebuilt or re-verified by this backfill.
- [ ] 5 `investigation/` - **N/A, permanently waived** (same Section H reason). Pre-existing
      `investigation/recon.py` left untouched.
- [x] 6 `evidence/` - this backfill's own evidence-capture run (see below): screen-scoped dryrun +
      live artifacts, per-TC screenshots.
- [x] 7 `CHECKLIST.md` - this file, rewritten this backfill.

## B. RF files (unchanged by this backfill - already merged via PR #467, 2026-08-23)
- [x] 8 T3 `pageobjects/Configuration/Assets/Well_and_Reservoir_Objects/reservoir_formation_page.resource`
      - properties-file-driven, explicit grid-filter wiring, NO hardcoded ids.
- [x] 9 Suite `tests/Configuration/Assets/Well_and_Reservoir_Objects/reservoir_formation_iud.robot` -
      TC01-05 clean-state/insert/update/find/delete.

## C. Verification gates
- [x] 10 robocop - `robocop check` on the T3 + suite (this backfill, 2026-08-28): **11 issues** (all
      VAR02/DOC02 style findings - missing `[Documentation]` on TC02-05, same class the PR #467 body
      cites as "same VAR02/DOC02 findings the freshly-merged Berth exemplar itself has, zero new-pattern
      delta"). Not a regression; not fixed by this backfill (out of scope - docs-only backfill).
- [x] 11 `--dryrun` - **5/5 PASS** (screen-scoped, this backfill 2026-08-28):
      `robot --dryrun --outputdir Workplaces/reservoir-formation-backfill/dryrun tests/.../reservoir_formation_iud.robot`
      -> `evidence/dryrun/output.xml` (0 failed).
- [x] 12 LIVE headless run - **5/5 PASS** (this backfill 2026-08-28):
      `EC_HEADLESS=true robot --outputdir Workplaces/reservoir-formation-backfill/live tests/.../reservoir_formation_iud.robot`
      -> `evidence/live/output.xml`, `log.html`, `report.html` (0 failed). TC01 Verify Clean State, TC02
      Insert, TC03 Update, TC04 Find, TC05 Delete all PASS.
- [x] 13 DB ground-truth - suite's own `Verify Object Insert Exists`/`Verify Object Form Record`/
      `Verify Object Found`/`Verify Object Removed` (T2, via `DbVerify.py`) assert
      `Code Should Be Present/Absent In View OV_RESV_FORMATION` and
      `Field Should Equal In View OV_RESV_FORMATION AUTOTEST_RESVF NAME` across insert/update/delete.
      Independently re-checked this backfill via a fresh oracledb connection (separate from the suite
      process): `SELECT COUNT(*) FROM OV_RESV_FORMATION WHERE CODE = 'AUTOTEST_RESVF'` -> **0** both
      before and after the live run.
- [x] 14 FULL I-U-D - TC02 Insert + TC03 Update + TC05 Delete all present and passing (not I/D only).
- [x] 15 Self-clean confirmed - **0 residual** `AUTOTEST_RESVF` rows in `OV_RESV_FORMATION`, verified via
      a fresh oracledb connection (`localhost:1521/ORCL`, per `resources/environment.py`'s default),
      2026-08-28, after this backfill's own live run.
- [x] 16 Hygiene PASS - `py scripts/check_bundle_hygiene.py` (repo root), this backfill 2026-08-28:
      `[hygiene] RESULT: PASS - no hardcoded creds (R16), pure ASCII (R20), no CHECKLIST/VERIFY-REPORT
      contradictions, doc rows match declared families` (the one WARN reported by the scan is for an
      unrelated screen, Contract_Area, not Reservoir Formation).

## D. Delivery
- [x] 17 Registry row - already present/modified by PR #467 (`docs/ec_screen_registry.md` line ~268,
      "FULL Bank-pattern conversion (Batch 9, 2026-08-23)"). Not re-appended by this backfill (would
      violate append-only R23 to duplicate it).
- [x] 18 Scorecard row - already present/modified by PR #467 (`docs/automation-scorecard.md` line ~158).
      Not re-appended by this backfill, same reason.
- [x] 19 PR - this backfill's own PR (docs-only, standard 6-field body, base = master, never
      self-merged).

## E. Knowledge base
- [x] 20 KB selector map `ec-ui-knowledge/screens/reservoir_formation.md` - refreshed this backfill to
      reflect the Batch 9 build (properties-file-driven insert/update, grid-filter selectors, fixed test
      code, 5-TC structure); "last verified" date updated to 2026-08-28.
- [x] 21 Reuse clause - this IS a reuse-run backfill (screen already had a bundle from 2026-07-26); this
      backfill produces the refreshed JOURNAL (#3), evidence (#6), and KB map (#20) that the reuse
      clause requires, not just green tests.

_Gates 10-16 above are cited from real command output captured during this backfill session
(2026-08-28) - see `evidence/` for the raw artifacts (dryrun/live output.xml, log.html, report.html,
per-TC screenshots)._
