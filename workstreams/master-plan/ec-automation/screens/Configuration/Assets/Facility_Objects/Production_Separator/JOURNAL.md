# JOURNAL — Production Separator IUD

_Screen: Configuration > Assets > Facility_Objects > Production Separator (BF CO.0042), OV-GM
groupmodel, navigator-gated. View `OV_PRODSEPARATOR`. This JOURNAL was backfilled 2026-08-27 under
the retired-lean-waiver work order (`docs/lean-deliverable-backfill-workorder.md`, Section H of
`docs/IUD-DELIVERABLE-CHECKLIST.md`) — PR #551 (the Area-pattern conversion) is the source of the
"Built" and "Done well" content below, pulled from its real PR body, not invented._

## Built

### Original build (2026-07-30)
- **Branch:** `feature/ov-gm-production-separator` (stacked on the gated-navigator capability, PR
  #244). Check-existing gate: grep ec-automation -> only this build; reused shared engine
  (`ec_object_iud.py`) + T2 + `DbVerify.py`.
- **Recon** (`investigation/recon.py`, read-only + `tmp/production_separator/config.json` scan):
  OV-GM (grid `manageObject:form:T_data`), navigator cascade Production Unit -> Area -> Facility
  Class 1. Mandatory Production Separator Code / Production Separator Name / Start Date.
- Label-driven T3 (no hardcoded ids); Playwright driver `py/production_separator_iud.py` + RF T3/
  suite (4 TCs, suite-level login, `Apply OV-GM Navigator First Available` cascade, inline DB-
  verify calls). Op Production Unit set first-available for grid visibility.
- `verify_screen.py` -> OVERALL PASS: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4 pass,
  Playwright 8/8, DB residual 0.

### Area-pattern conversion (PR #551, merged 2026-08-26)
- Converted the RF IUD suite from the old 4-TC/suite-level-login/first-available-navigator/inline-
  DB-verify shape to Area's full pattern: 5 TCs (added TC04 Find), per-TC login/logout, the shared
  T2 `Apply Navigator From Properties` keyword driven by EXPLICIT values for the genuine 3-level
  Production Unit -> Area -> Facility Class 1 navigator cascade, properties-file-driven insert/
  update/verify, explicit grid-filter wiring (`Find/Clear Production Separator Row By Filter`), and
  ZERO inline DB-verify calls (all screen verification now delegates to shared T2 keywords).
- New test-data files: `testdata/production_separator_{navigator,insert,update,form_verify,
  grid_verify}.properties`; new dedicated credentials pair
  (`PRODUCTION_SEPARATOR_EC_USER`/`PRODUCTION_SEPARATOR_EC_PASS` in `resources/credentials.py`);
  fixed test code `AUTOTEST_PSEP` replacing the old timestamped code.
- No shared T1/T2 files (`resources/manage_object.resource`, `resources/table.resource`,
  `resources/common.resource`) were touched — the existing `Apply Navigator From Properties`
  keyword already supported this screen's 3-level same-row cascade shape as-is.
- Registry row (`docs/ec_screen_registry.md`) modified in place (not a new row); scorecard entry
  updated (not a new row).

### This backfill (2026-08-27)
- Rewrote `production_separator_sow.md` (was still describing the pre-conversion 4-TC shape),
  this `JOURNAL.md`, `CHECKLIST.md`, the KB selector map
  `ec-ui-knowledge/screens/production_separator.md` (did not exist before this backfill), and
  `evidence/backfill_2026-08-27/` (fresh dryrun + live re-run of the CURRENT PR #551 suite — no
  automation code touched).

## Done well
- Full I-U-D DB-verified vs `OV_PRODSEPARATOR` (insert Production Separator Code/Name, update
  Production Separator Name, delete End=Start absent); PR #551 body: "Fixed test code
  `AUTOTEST_PSEP` confirmed free in `OV_PRODSEPARATOR` via a fresh oracledb connection before
  wiring it in (0 rows), and 0 residual `AUTOTEST%` rows after the live run."
- Live run cited in PR #551: `EC_HEADLESS=true py -m robot
  tests/Configuration/Assets/Facility_Objects/production_separator_iud.robot` -> **5 tests, 5
  passed, 0 failed** (TC01 Verify Clean State / TC02 Insert / TC03 Update / TC04 Find / TC05
  Delete).
- DbVerify assertion: shared T2 `Verify Object Removed` (`OV_PRODSEPARATOR`, code column) inside
  TC05 — the only DB check in the suite, no inline calls in the `.robot`/`.resource` files
  (confirmed via grep in PR #551, 0 matches for `Should Exist In DB`/`Code Should Be Present/
  Absent In View`/`Field Should Equal In View`).
- Grid-filter keyword `Find Object Row By Filter` fired 15x during the live run (PR #551 body,
  `output.xml` grep).
- Full `tests/` tree dryrun stayed 100% pass (850/850) before the live run (PR #551 body).
- robocop on the changed files: 7 issues, all `DOC02` (missing TC `[Documentation]`) — identical in
  kind/count to Area's own current baseline (also 7 issues, re-checked live during this backfill,
  2026-08-27) -> parity, not a regression.
- Check-real-driver-first: the pre-existing `py/production_separator_iud.py` Playwright driver was
  read first; its proven "Op Production Unit = `__FIRST__`" mechanism was reused (not re-invented)
  after live evidence showed the exact-value approach fails.

## Done wrong / lessons
- **The `__FIRST__` gotcha (PR #551):** the form's Op Production Unit dropdown is a date-effective
  reference filtered by the form's own Start Date. Requesting the EXACT alphabetically-first value
  (`AS1 EC Exploration Norway`, resolved from a pre-Start-Date recon) after Start Date=2000-01-01
  was filled reproducibly timed out live (2 attempts). Root cause: the version-filtered list AFTER
  Start Date differs from the list BEFORE it. Fix: use the shared T2's `__FIRST__` literal instead
  of a fixed string — genuinely first-available-after-filter — matching the pre-existing driver's
  own proven mechanism (`insert_fields: {"label": "Op Production Unit", "value": "__FIRST__"}`).
  This is the SAME class of "Op Production Unit dropdown filtered / doesn't include the exact nav
  value" issue hit and fixed identically on Chemical Tank and Chemical Injection Point — not a new
  discovery, a repeat of a known EC quirk (date-effective reference dropdowns filter by the form's
  own Start Date, per `reference_ec_object_start_date_version.md`).
- No other regressions or wrong turns disclosed in PR #551's body for this conversion.
- Backfill-specific: none — the fresh dryrun (5/5), live re-run (5/5), DB self-clean (0/0 via a
  fresh oracledb connection), and hygiene check all passed on the first attempt during this
  backfill.

## Blockers -> resolution
- The Op Production Unit timeout above (2 reproducible live TC02 failures) was the only blocker in
  PR #551; resolved same-session by reusing the driver's proven `__FIRST__` mechanism rather than
  writing a new theory/script per the "no 3rd option" standing rule.
- No blockers during this backfill.

## Decisions
- Playwright bundle stays waived permanently for this backfill (owner decision 2026-08-27,
  `docs/IUD-DELIVERABLE-CHECKLIST.md` Section H) — the existing `py/production_separator_iud.py`
  from the 2026-07-30 build is preserved as-is and was NOT touched, re-verified, or regenerated.
  The Universal Screen Engine is the owner-decided replacement for hand-written Playwright drivers
  going forward.
- The RF suite remains the maintained/live test; the Playwright driver is historical reference
  only (README.md updated to say so explicitly).
- Code lives in `ec-automation`; `ec-ui-knowledge/` stays MD-only.

## Evidence
- Original build (2026-07-30): `evidence/psep_0[1-5]_*.png` + `evidence/results.json` (4-TC
  Playwright 8/8 + RF 4/4 run).
- PR #551 conversion (2026-08-26): live run `5 tests, 5 passed, 0 failed` (TC01-TC05), full-tree
  dryrun 850/850, DB self-clean 0/0 (fresh connection before and after) — all cited in the PR body;
  not re-captured as screenshots at conversion time (RF run, not Playwright).
- This backfill (2026-08-27): `evidence/backfill_2026-08-27/` — `dryrun/` (5/5 PASS, `log.html`/
  `report.html`/`output.xml`) and `live/` (5/5 PASS headless, `log.html`/`report.html`/
  `output.xml`), plus `db_self_clean_result.txt` (`OV_PRODSEPARATOR`: 0 rows for `AUTOTEST_PSEP`,
  0 residual `AUTOTEST%`, fresh connection) and `py scripts/check_bundle_hygiene.py` -> `RESULT:
  PASS`. robocop re-run on the changed files: 7 `DOC02` issues, confirmed at parity with Area's own
  7 `DOC02` issues (re-checked live the same session).
