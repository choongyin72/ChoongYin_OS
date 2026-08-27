# JOURNAL - External Location (CO.0227) OV-GM IUD

_Modeled on `screens/Configuration/Assets/Financial_Objects/Bank/JOURNAL.md`. This file records TWO
distinct pieces of history: the original 2026-08-01 base build (full `ec-object-iud-builder` 21-item
bundle), then the 2026-08-26 RF conversion (PR #524 + PR #528) which changed the RF suite's structure
but - built under the since-retired 2026-08-23/26 lean waiver (`docs/IUD-DELIVERABLE-CHECKLIST.md`
Section G) - did not update this bundle's docs at the time. This entry (2026-08-27) is that backfill,
per `docs/lean-deliverable-backfill-workorder.md`._

## 2026-08-01 - base build

### Built
- **Branch:** `feature/external-location-iud`.
  Check-existing gate: 0b grep ec-automation -> only this build (checked: 0 other file(s) reference 'external_location'); reused shared engine (ec_object_iud.py) + T2 + DbVerify.
- **Recon** (`investigation/recon.py`, read-only + tmp/external_location/config.json scan): OV-GM (grid `manageObject:form:T_data`).
  Nav: GO only (navigator fields are optional filters, no mandatory scope). Mandatory External Location Code / External Location Name / Start Date.
- **Built** (generator `tmp/gen_ovgm.py`): label-driven T3 (no hardcoded ids); Playwright driver + RF T3/suite (4 TCs at the time).
- `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4 pass, Playwright 8/8. DB residual 0.

### Done well
- OV-GM: first-available nav scope + Op PU first-available lists the row after GO (parent-dd need not equal the nav PU - probe per screen). Generic engine handled the nav/appear/absent/pagination gestures with zero tuning.

## 2026-08-26 - RF conversion to Area's full pattern (PR #524, PR #528)

### Built
- **PR #524** (`feature/external-location-navigator-from-properties`): exploratory test of the new
  shared T2 keyword `Apply Navigator From Properties` (`resources/manage_object.resource`, added in
  PR #523 for Area's mandatory-PU scope) against External Location - the FIRST proof of that shared
  keyword's **zero-mandatory-nav edge case**. External Location's navigator has no mandatory scope at
  all (fields are optional filters, grid loads on GO alone), so the conversion drove the keyword with
  an intentionally EMPTY `testdata/external_location_navigator.properties` (comments only) instead of
  a bare `Apply Navigator` call. Confirmed both live and via a source-read of
  `PropertiesReader.read_properties()` that an all-comment file returns `{}`, so the keyword's
  `FOR ${label} IN @{data.keys()}` loop runs 0 iterations and falls straight through to `Apply
  Navigator` (bare GO) - i.e. byte-for-byte the same behaviour External Location always had. Zero
  changes to `resources/manage_object.resource` itself.
- **PR #528** (built on top of #524's branch, since #524 was NOT yet merged - `gh pr view 524` showed
  `state: OPEN` at the time #528 was raised, a stated premise correction, not an assumption): converted
  External Location's RF suite STRUCTURE to Area's full pattern, per the owner's 2026-08-26 standing
  rule that any EC screen with a navigator section matching Area's layout follows Area's FULL pattern,
  not just the navigator-fill piece #524 landed. 4 TCs (single suite-level login, screen-local
  `External Location Should/Should Not Exist In DB` inline DB-verify wrappers, `Fill OV Field By
  Label` hardcoded-in-.robot inserts, timestamped `AUTOTEST_EL<timestamp>` code) -> 5 TCs (added TC04
  Find) with per-TC Login/Logout, fixed test code `AUTOTEST_EXTERNAL_LOCATION` (confirmed free via a
  fresh oracledb query before the run), properties-file-driven insert/update via T2's `Insert/Update
  Object From Properties`, explicit `Find/Clear External Location Row By Filter` grid-filter wiring
  into Update/Find/Verify-Found/Delete, and PURE SCREEN verification only (zero inline DB-verify
  calls remain in `external_location_iud.robot` - the DB check now lives solely inside the shared T2
  `Verify Object Removed`). External Location's genuine GO-only/no-mandatory-nav-scope navigator
  behaviour was kept EXACTLY as-is - this was a structural conversion, not a reclassification.
- Both PRs' real DB ground-truth (from the PR bodies): #524 - live suite 4/4, `SELECT COUNT(*) FROM
  OV_EXTERNAL_LOCATION WHERE CODE = 'AUTOTEST_EL20260826100052'` -> `0`. #528 - live suite 5/5,
  full-tree dryrun 847/847 (zero collisions with the parallel Field (#525)/Facility Class 1 (#526)
  work), robocop 7 issues (VAR02 x2 + DOC02 x5) - exact parity with Area's own reference-pattern
  files, fresh-connection DB self-clean 0/0 before+after.

### Done well
- #528 disclosed and corrected a wrong task premise (that #524 was "already merged") using
  `gh pr view`/`git merge-base --is-ancestor` rather than proceeding on the stated assumption, and
  branched off #524's branch instead of master to avoid losing that work.
- Both PRs worked in isolated sparse-checkout clones and made zero changes to the shared
  `resources/manage_object.resource`/`resources/common.resource` files - confirmed via grep that
  PR #524's new keyword already covered this screen with no further shared-file gap.
- #528 checked `ec-ui-knowledge/screens/external_location.md` for real field labels/grid columns
  before writing any properties file, rather than assuming Area's labels applied verbatim (EC UI
  read-first rule).

### Done wrong / lessons (this backfill, 2026-08-27)
- Neither #524 nor #528 updated this `screens/.../External_Location/` bundle (SOW/README/JOURNAL/
  evidence/CHECKLIST/KB map) at the time - both were built and merged under the 2026-08-23/26 lean
  waiver (`docs/IUD-DELIVERABLE-CHECKLIST.md` Section G), which for Bank-/Area-pattern conversions
  explicitly waived items 1/3/4/5/6/7/20 of the 21-item checklist. That waiver was retired by the
  owner on 2026-08-27 (Section H) for everything except the Playwright driver/investigation items -
  this JOURNAL entry, the refreshed SOW/README/CHECKLIST, the new evidence run, and the refreshed KB
  map are that retroactive backfill (`docs/lean-deliverable-backfill-workorder.md`, Batch 1).
- The bundle's `evidence/` folder and `CHECKLIST.md`/`VERIFY-REPORT.md` still described the 2026-08-01
  4-TC/Playwright-only state until this backfill - anyone reading only this bundle (not the registry
  row or the RF suite itself) would have gotten a stale picture of the current 5-TC structure.

### Blockers -> resolution
- None during this backfill - the RF automation itself required no changes (per the task's explicit
  instruction not to touch it); the only "verification" needed was one dryrun + one live re-run, both
  of which passed cleanly on the first attempt.

### Decisions
- This backfill did NOT rebuild the Playwright driver (`py/external_location_iud.py`) or
  `investigation/recon.py` - both predate the 2026-08-23 lean rule (built in the original 2026-08-01
  full-checklist build) and remain untouched; they are not part of what PR #524/#528 changed.
- New evidence from this backfill's live re-run is kept alongside (not overwriting) the original
  2026-08-01 Playwright evidence screenshots, since both are real, non-contradictory records of two
  different automation layers (Playwright driver vs RF suite) at two different points in time.

### Evidence
- RF live re-run (this backfill, 2026-08-27, headless): `evidence/rf_backfill_2026-08-27/` -
  `output.xml`/`log.html`/`report.html`, **5 tests, 5 passed, 0 failed**.
- Full-tree dryrun (this backfill): **883 tests, 883 passed, 0 failed** (zero collisions).
- DB self-clean (this backfill, fresh `oracledb` connection, `localhost:1521/ORCL`,
  `ECKERNEL_EC`/`energy`): `SELECT COUNT(*) FROM OV_EXTERNAL_LOCATION WHERE CODE LIKE
  'AUTOTEST_EXTERNAL_LOCATION%'` -> `0`.
- Hygiene: `py scripts/check_bundle_hygiene.py` -> `RESULT: PASS` (repo-wide; the 2 WARN lines
  reported are pre-existing Contract Area recon-script items, unrelated to External Location).
- Original 2026-08-01 Playwright evidence: `evidence/EL_0[1-5]_*.png` + `evidence/results.json`
  (8/8 pass, kept as-is, untouched by this backfill).
