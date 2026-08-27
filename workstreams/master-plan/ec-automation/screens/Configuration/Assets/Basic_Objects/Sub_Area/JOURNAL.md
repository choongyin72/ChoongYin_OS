# JOURNAL — Sub Area IUD

_Screen: Configuration > Assets > Basic Objects > Sub Area (OV-GM groupmodel, navigator-gated).
View `OV_SUB_AREA`. This JOURNAL was backfilled 2026-08-27 under the retired-lean-waiver work
order (`docs/lean-deliverable-backfill-workorder.md`, Section H of
`docs/IUD-DELIVERABLE-CHECKLIST.md`) — the bundle's SOW/README/evidence/playwright/investigation
predated the JOURNAL rule; PR #538 (the Area-pattern conversion) is the source of the "Built" and
"Done well" content below, pulled from its real PR body, not invented._

## Built

### Original build (2026-06-11)
- Playwright reference `playwright/ec_iud_sub_area.py` (+ shared `_shared/iud_engine.py`), full
  recon trail in `investigation/` (`basic_objects_recon2.py`, `merge_form_labels.py`,
  `phase_b_deep_dive.py`, `phase_b_micro_probes.py`, `probe_subarea_cascade_now.py`).
- RF suite (4 TC, suite-level login, bespoke navigator) — `sub_area_page.resource` +
  `sub_area_iud.robot`.

### Area-pattern conversion (PR #538, merged 2026-08-26)
- Converted the RF IUD suite from the OLD bespoke-navigator/4-TC/suite-level-login pattern to the
  full Area-pattern structure: properties-file-driven navigator via the shared `Apply Navigator
  From Properties` T2 keyword (`resources/manage_object.resource`), per-TC login/logout, 5 TCs
  (added TC04 Find), a fixed test code (`AUTOTEST_SUB_AREA`, replacing the old timestamped code),
  a dedicated credentials pair (`SUB_AREA_EC_USER`/`SUB_AREA_EC_PASS` in
  `resources/credentials.py`), and zero inline DB-verify calls in the `.robot` file.
- New test-data files: `testdata/sub_area_navigator.properties`, `sub_area_insert.properties`,
  `sub_area_update.properties`, `sub_area_form_verify.properties`, `sub_area_grid_verify.properties`.
- The screen's genuine 2-level Production Unit -> Area navigator cascade was KEPT unchanged —
  this was a structural conversion, not a reclassification of the screen as plain Bank-shaped.
- Registry row (`docs/ec_screen_registry.md`) MODIFIED in place (not a new row).

### This backfill (2026-08-27)
- Added `sub_area_sow.md` §3.2 (real PR #538 dev story), this `JOURNAL.md`, `CHECKLIST.md`, the
  KB selector map `ec-ui-knowledge/screens/sub_area.md`, and `evidence/backfill_2026-08-27/`
  (fresh dryrun + live re-run captured as evidence of the already-proven suite — no automation
  code touched).

## Done well
- Full I-U-D DB-verified vs `OV_SUB_AREA` (insert Sub Area Code/Name, update Sub Area Name,
  delete End=Start absent); self-clean 0 residual, confirmed via a FRESH oracledb connection both
  before and after the live run (PR #538 body: "Fresh oracledb connection ... confirmed
  `AUTOTEST_SUB_AREA` was free (0 rows) and no residual `AUTOTEST%` rows existed ... a SECOND
  fresh connection AFTER the run confirmed the same").
- Recon-first, no guessing: PR #538 body states the navigator shape (2-level same-row cascade,
  `nav:form:G:0:R:1:C:1:dd`/`C:2:dd`), objectForm labels (`Sub Area Code`/`Sub Area Name`/
  `Op Production Unit`/`Op Area`), and grid columns were confirmed via a LIVE RF DOM scan before
  any config was written — not assumed from Area/Facility Class 1.
- Check-real-driver-first: the conversion REUSED the pre-existing driver's proven navigator values
  (`Production Unit`/`Offshore area`) and the proven "insert sets Op PU + Op Area" behavior,
  rather than extrapolating from Facility Class 1 (which proved BLANK Op PU/Op Area works — a
  different, screen-specific behavior, deliberately NOT applied here).
- Full-tree dryrun stayed 100% pass (850/850) before the live run (per PR #538 body); this
  backfill's own fresh dryrun re-confirmed the Sub Area suite alone: 5/5 PASS.
- `resources/manage_object.resource` (shared T2) was NOT modified for this conversion — no gap
  found; Sub Area's cascade fit the already-proven shape.

## Done wrong / lessons
- No regressions or wrong turns disclosed in PR #538's body for this specific conversion. The
  screen's own KNOWN quirk from the original 2026-06-11 build — sandbox area names stored with a
  LEADING SPACE (' Offshore area') requiring normalize-space matching — was already handled by the
  shared T2 keyword before this conversion and did not resurface.
- Backfill-specific: the first DB self-clean script written during this backfill assumed a
  screen-specific `SUB_AREA_CODE` column (guessing by analogy to the UI label) and failed with
  `ORA-00904: invalid identifier`; `libraries/DbVerify.py` was then read to confirm every
  `OV_*` view uses the generic `CODE` column — fixed and re-run successfully. Recorded here as a
  reminder: check the shared library's actual column convention before writing a one-off DB
  script, don't infer it from the screen's field label.

## Blockers -> resolution
- None disclosed in PR #538. No hard blockers during this backfill; the dryrun, live run, DB
  self-clean, and hygiene check all passed on the first real attempt (after the column-name
  correction above).

## Decisions
- Playwright bundle stays waived permanently for this backfill (owner decision 2026-08-27,
  `docs/IUD-DELIVERABLE-CHECKLIST.md` Section H) — the existing `playwright/ec_iud_sub_area.py`
  from the 2026-06-11 build is preserved as-is and was NOT touched, re-verified, or regenerated.
  The Universal Screen Engine is the owner-decided replacement for hand-written Playwright drivers
  going forward.
- The RF suite remains the maintained/live test; the Playwright driver is historical reference
  only (README.md updated to say so explicitly).
- Code lives in `ec-automation`; `ec-ui-knowledge/` stays MD-only.

## Evidence
- Original build: `evidence/sub_area_0[1-8]_*.png` + `evidence/sub_area_results.json`
  (2026-06-11, 4-TC Playwright/RF run).
- PR #538 conversion: live run `5 tests, 5 passed, 0 failed` (TC01-TC05), cited in the PR body;
  not re-captured as screenshots at conversion time (RF run, not Playwright).
- This backfill (2026-08-27): `evidence/backfill_2026-08-27/` — `dryrun/` (5/5 PASS,
  `log.html`/`report.html`/`output.xml`) and `live/` (5/5 PASS headless,
  `log.html`/`report.html`/`output.xml`), plus a DB self-clean result (`OV_SUB_AREA`: 0 rows for
  `AUTOTEST_SUB_AREA`, 0 residual `AUTOTEST%`, fresh connection) and
  `py scripts/check_bundle_hygiene.py` → `RESULT: PASS`.
