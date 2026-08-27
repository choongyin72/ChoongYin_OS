# JOURNAL - Operator Route (CO.0244) OV-GM IUD

_Screen: Configuration > Assets > Facility_Objects > Operator Route. OV-GM (manage-object,
groupmodel), navigator-gated (Production Unit -> Area), date-effective. View `OV_OPERATOR_ROUTE`._
_This JOURNAL was reshaped 2026-08-27 to the Bank/Area JOURNAL structure and extended with the
2026-08-26 Area-pattern conversion, per `docs/lean-deliverable-backfill-workorder.md`. The
2026-08-01 base-build content below is preserved, not overwritten._

## Built

**2026-08-01 - base IUD build.**
- Branch `feature/operator-route-iud`. Check-existing gate: 0b grep ec-automation -> only this
  build (0 other files referenced `operator_route`); reused the shared engine (`ec_object_iud.py`)
  + T2 + `DbVerify`.
- Recon (`investigation/recon.py`, read-only + `tmp/operator_route/config.json` scan): confirmed
  OV-GM (grid `manageObject:form:T_data`), nav Production Unit -> Area cascade + GO, mandatory
  Operator Route Code / Operator Route Name / Start Date.
- Generated (via `tmp/gen_ovgm.py`): label-driven T3 (no hardcoded ids); Playwright driver
  (`py/operator_route_iud.py`) + RF T3/suite (4 TCs).
- `verify_screen.py` -> OVERALL PASS: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4, Playwright
  8/8. DB residual 0.

**2026-08-26 - Area-pattern structural conversion (PR #533, merged 08:06:00Z).**
- Owner standing rule (2026-08-26): any EC screen with a navigator matching Area's layout follows
  Area's FULL pattern (5-TC/per-TC-login/pure-screen-verify/properties-driven/explicit-filter-
  wiring), not just the navigator-fill piece.
- Converted the RF layer from 4 TCs (single suite-level login, bespoke inline navigator-fill via
  `Select EC Dropdown Option` + `Apply Navigator`, a generated `AUTOTEST_OR_<timestamp>` code,
  screen-local `Operator Route Should/Should Not Exist In DB` inline DB-verify wrappers) to 5 TCs
  (added TC04 Find) with per-TC Login/Logout, a fixed test code `AUTOTEST_OR` (confirmed free via
  a fresh oracledb query on `OV_OPERATOR_ROUTE`, 0/0 before+after), navigator fill delegated to the
  shared T2 `Apply Navigator From Properties` (`resources/manage_object.resource`) driven by
  `testdata/operator_route_navigator.properties` (same PROVEN explicit values
  `P3 Production Unit` / `P3 Area` the pre-conversion driver already used), properties-file-driven
  insert/update via T2's `Insert/Update Object From Properties`
  (`testdata/operator_route_{insert,update,form_verify,grid_verify}.properties`), explicit
  `Find/Clear Operator Route Row By Filter` grid-filter wiring into Update/Find/Verify-Found/Delete
  (15 `Find Object Row By Filter` hits in `output.xml`), and PURE SCREEN verification only (zero
  inline DB-verify calls remain in `operator_route_iud.robot` - confirmed via grep; the DB check
  now lives solely inside the shared T2 `Verify Object Removed`).
- The screen's genuine mandatory 2-level PU->Area cascade + GO was kept UNCHANGED - this was a
  structural conversion only, not a reclassification of the screen's navigator shape.
- No shared T1/T2 file changes this round - the existing `Apply Navigator From Properties`
  keyword's flat 0.7s sleep between levels already handled this screen's redraw timing (same shape
  already proven on Facility Class 1).
- Playwright driver `py/operator_route_iud.py` left UNTOUCHED (RF `.robot` structural conversion
  only).

**2026-08-27 - deliverable backfill (this bundle refresh, `docs/lean-deliverable-backfill-workorder.md`).**
- Owner decision 2026-08-27 retired the 2026-08-23/26 lean waiver (`docs/IUD-DELIVERABLE-
  CHECKLIST.md` Section H): SOW/README/JOURNAL/evidence/CHECKLIST/KB map must be backfilled for
  every screen converted under the old lean rule. Operator Route (Batch 1 of
  `docs/lean-deliverable-backfill-workorder.md`) already HAD a full bundle from the 2026-08-01 base
  build (it predates the 2026-08-23 lean rule) - but that bundle's content (README, SOW, JOURNAL,
  KB map) was never updated after PR #533's 2026-08-26 structural conversion, so it described the
  old 4-TC/generated-code shape. This session refreshed `operator_route_sow.md`, `README.md`, this
  `JOURNAL.md`, and `ec-ui-knowledge/screens/operator_route.md` to describe the CURRENT merged
  RF shape, and added fresh evidence (`evidence/rf_2026-08-27/`) from a one-time live re-run of the
  already-proven, already-merged suite.
- No RF automation was rebuilt or modified in this session (`operator_route_page.resource`,
  `operator_route_iud.robot`, and the `testdata/operator_route_*.properties` files were read-only
  references, never edited).

## Done well
- Full I-U-D DB-verified vs `OV_OPERATOR_ROUTE` (insert Name, update Name, delete End=Start
  absent); self-clean 0 residual, confirmed via a fresh oracledb connection both before (0 rows)
  and after (0 rows) the 2026-08-27 re-run.
- One engine (`ec_object_iud.py`) + one DB-verify (`DbVerify.py`) shared across the base build; the
  Area-pattern conversion reused the same shared T2 `Apply Navigator From Properties` already
  proven on Facility Class 1 - zero new shared-file plumbing needed for either round.
- Genuine navigator values (`P3 Production Unit` / `P3 Area`) were carried over unchanged across
  both the base build and the conversion - no re-derivation, no first-available guess.

## Done wrong / lessons
- The 2026-08-01 base bundle's documentation (SOW/README/JOURNAL/KB map) was never refreshed when
  PR #533 restructured the RF suite on 2026-08-26 - the bundle silently went stale (still
  described a 4-TC suite with a generated timestamped code, while the merged suite was already
  5-TC with a fixed code). This is exactly the gap `docs/lean-deliverable-backfill-workorder.md`
  exists to close: a documentation bundle is not "backfilled" just because one existed once: it
  must reflect the CURRENT state of the automation it documents.
- `VERIFY-REPORT.md` in this bundle is still the 2026-08-01 auto-generated report (4-TC gate
  counts) and was NOT regenerated by `scripts/verify_screen.py` in this session (that script needs
  re-running against the 5-TC suite to produce a current auto-generated report - out of this
  backfill's stated scope, which is documentation/evidence around already-working automation, not
  a fresh `verify_screen.py` pass). `CHECKLIST.md` carries the current, re-run gate evidence
  instead.

## Blockers -> resolution
- None this session. The live suite ran clean on the first attempt (dryrun 5/5, full-tree dryrun
  883/883 with 0 collisions, live headless 5/5); no selector drift or navigator timing issue was
  observed on the local sandbox.

## Decisions
- Playwright + RF stay two separate stacks; the Playwright driver is frozen at its 2026-08-01 state
  under Section H's permanent waiver (Universal Screen Engine replaces the hand-written-driver
  role going forward) - it is not being kept in sync with RF's structural changes going forward.
- `ec-ui-knowledge/` stays MD-only; the KB map was refreshed in place (not duplicated) to reflect
  the current 5-TC/fixed-code/filter-wired shape.

## Evidence
- Base build (2026-08-01, Playwright 8/8 + RF 4/4): `evidence/results.json` +
  `evidence/or_0[1-5]_*.png`.
- This backfill (2026-08-27, RF 5/5, one-time live re-run of the already-merged Area-pattern
  suite): `evidence/rf_2026-08-27/` - `log.html`, `report.html`, `output.xml`, per-TC screenshots,
  `results.json` (dryrun 5/5, full-tree dryrun 883/883 zero collisions, live 5/5, DB AUTOTEST_OR
  0/0 before+after, 15 `Find Object Row By Filter` hits, 0 inline DB-verify calls, robocop 7 issues
  = parity with Area, hygiene PASS).
