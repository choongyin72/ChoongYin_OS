# JOURNAL — Chemical Transport Tank (CO.0257) OV IUD

_Screen: Configuration > Assets > Chemical_Objects > Chemical Transport Tank (OV, date-effective,
plain Bank-family, no navigator/mandatory dropdowns). View `OV_CHEM_TRANS_TANK`. NOT the "Chemical
Tank" screen (Area-pattern OV-GM, backfilled separately in Batch 4) - confirm paths before touching
anything._

_This JOURNAL was backfilled 2026-08-28 (lean-deliverable backfill, Batch 9) per owner decision
2026-08-27 retiring the lean waiver in `docs/IUD-DELIVERABLE-CHECKLIST.md` Section H. The prior
version of this file (and the SOW/README/CHECKLIST/KB map) still described the original
2026-07-26 partial build and had never been updated for the Batch 8 conversion below — this entry
covers BOTH the real history (from PR #461's body/commits) and this backfill's own work._

## Built
- **2026-07-26 (original build):** partial label-driven RF T3 + suite (4-TC: insert/update/find/
  delete, no clean-state TC, no grid-filter wiring, generated-unique test codes) + Playwright driver
  `py/chemical_transport_tank_iud.py` (7/7). First cut, not yet on the properties-file-driven/
  T2-consolidated Bank shape.
- **2026-08-23 (PR #461, Batch 8 of the Bank-pattern conversion project):** rebuilt
  `chemical_transport_tank_page.resource` (T3) and `chemical_transport_tank_iud.robot` (suite,
  4-TC -> 5-TC) to mirror `bank_page.resource`/`berth_page.resource` exactly:
  properties-file-driven insert/update/verify (`testdata/chemical_transport_tank_insert.properties`,
  `_update.properties`, `_form_verify.properties`, `_grid_verify.properties`, all new), explicit
  grid-filter wiring (`Find Chemical Transport Tank Row By Filter`/`Clear ... Row Filter` ->
  shared T2 `Find Object Row By Filter`/`Clear Object Row Filter`), fixed test code `AUTOTEST_CTT`
  (replacing the generated-unique code), per-TC login/logout with dedicated credentials
  (`CHEMICAL_TRANSPORT_TANK_EC_USER`/`_EC_PASS`, added to `resources/credentials.py`).
  Registry (`docs/ec_screen_registry.md`) and scorecard (`docs/automation-scorecard.md`) rows were
  **replaced in place**, not duplicated. No shared T1/T2 files touched.
- **2026-08-28 (this backfill, Batch 9):** refreshed SOW/README/JOURNAL/CHECKLIST to describe the
  real, currently-merged Batch 8 automation instead of the stale 2026-07-26 description; refreshed
  `ec-ui-knowledge/screens/chemical_transport_tank.md`; captured fresh evidence
  (`evidence/batch8-live-2026-08-28/`) from a real dryrun + live run of the *current* 5-TC suite;
  moved the original 2026-07-26 screenshots/report to `evidence/pre-batch8-2026-07-26/` for history
  rather than deleting them. No RF/page-object/test-data files touched.

## Done well
- Full I-U-D DB-verified vs `OV_CHEM_TRANS_TANK` (insert Name, update Name, delete End=Start
  absent); self-clean 0 residual (PR #461's fresh-connection check; re-confirmed in-suite by this
  backfill's TC01/TC05 passing).
- Live RF 5/5 both at original merge (PR #461) and at this backfill's re-run (2026-08-28), first
  attempt, no retry needed.
- Field labels/mandatory set for the Batch 8 rebuild were trusted from the already-proven,
  live-tested Playwright driver (`py/chemical_transport_tank_iud.py` INSERT_FIELDS/UPDATE_FIELDS)
  rather than re-scanned live - avoided redundant recon.

## Done wrong / lessons
- **Docs went stale after a conversion.** The 2026-07-26 build's SOW/README/JOURNAL/CHECKLIST/KB
  map were never updated when PR #461 rebuilt the T3/suite on 2026-08-23 - they kept describing the
  old 4-TC, non-filter-wired, generated-unique-code build for over a month. This is exactly the gap
  the lean-deliverable backfill work order (`docs/lean-deliverable-backfill-workorder.md`) exists to
  close; this screen is proof the risk is real, not hypothetical.
- Batch 7's registry/scorecard merge-conflict defect (PR #458/#459) was a known risk for this
  conversion too - PR #461 explicitly replaced the existing rows in place rather than appending a
  duplicate, and called this out in its own PR body.

## Blockers -> resolution
- This backfill: a direct standalone `oracledb` connection from the local shell to
  `db.plutodev.woodside-pluto.tieto-og.cloud:1521/plutodev` timed out (network path issue on this
  box). Not treated as a live-run failure per the process rule (retry-once-then-disclose) - the
  live RF suite's OWN DB assertions (TC01/TC05, via `libraries/DbVerify.py` inside the same run)
  are the real ground truth here and both passed, so the self-clean claim is backed by that, not
  by the failed standalone query. Disclosed here rather than silently retried or worked around.
- No other blockers on this backfill; automation itself required no changes.

## Decisions
- Kept the original 2026-07-26 evidence (`evidence/pre-batch8-2026-07-26/`) rather than deleting
  it, so the bundle's history is traceable end-to-end.
- Playwright driver + `investigation/recon.py` are untouched and NOT rebuilt for Batch 8's shape -
  Section H's retired waiver keeps items 4/5 permanently waived (Universal Screen Engine replaces
  that role going forward); this backfill only restores items 1/2/3/6/7/20.

## Evidence
- Original build (2026-07-26): `evidence/pre-batch8-2026-07-26/chemical_transport_tank_0[1-5]_*.png`
  + `rf_report.html` (4/4 RF, 7/7 Playwright).
- PR #461 (2026-08-23): cited in its own PR body - live RF 5/5, dryrun full-tree 758/758, DB
  self-clean 0 residual, grid-filter fired 7x.
- This backfill (2026-08-28): `evidence/batch8-live-2026-08-28/` - dryrun 5/5
  (`Workplaces/chemical-transport-tank-backfill/dryrun/`), live 5/5 with per-TC screenshots +
  `log.html`/`output.xml`/`report.html`.
