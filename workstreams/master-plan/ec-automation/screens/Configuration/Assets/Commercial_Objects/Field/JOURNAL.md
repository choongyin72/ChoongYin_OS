# JOURNAL — Field IUD

_Screen: Configuration > Assets > Commercial Objects > Field (OV-GM, groupmodel manage-object).
View `OV_FIELD`. Navigator: single Area dropdown + GO. This JOURNAL was backfilled 2026-08-27
(owner decision retired the 2026-08-23/26 lean waiver — see
`docs/lean-deliverable-backfill-workorder.md`); content is pulled from the real PR #525 and
PR #529 bodies, not invented after the fact._

## Built
- **2026-06-12 (original build):** Field's first RF automation, part of the Commercial
  Objects 11-screen batch — `field_page.resource` (T3) + `field_iud.robot`, hardcoded
  field-ids, generated `AUTOTEST_FLD_<timestamp>` test code, 4 TCs with inline DB-verify
  calls. A standalone Playwright reference (`playwright/ec_iud_field.py`) was built alongside.
- **PR #525 (merged 2026-08-26):** navigator-fill delegation only. Replaced the inline
  `Select EC Dropdown Option` + `Apply Navigator` sequence with the shared T2 keyword
  `Apply Navigator From Properties` (`resources/manage_object.resource`, added for Area),
  driven by new `testdata/field_navigator.properties` (`Area=Offshore area`, reused verbatim
  from the pre-existing working value). Deliberately scoped as a reusability test of the
  shared keyword on a screen it wasn't originally built for.
- **PR #529 (content merged to master via commit `a5104dea`; PR itself shows CLOSED in GitHub,
  not MERGED — the change landed regardless, confirmed live in `field_page.resource`/
  `field_iud.robot` on master):** full structural conversion to Area's pattern — 5 TCs
  (Verify Clean State/Insert/Update/Find/Delete), per-TC `Login To EC Application`/
  `Logout From EC Application` on one browser opened once in Suite Setup, dedicated
  `FIELD_EC_USER`/`FIELD_EC_PASS` credentials, fixed test code `AUTOTEST_FIELD` (replacing the
  generated timestamp code), 4 new properties files (`field_insert/update/form_verify/
  grid_verify.properties`), explicit `Find/Clear Field Row By Filter` grid-filter wiring, and
  pure-screen verification (zero inline DB-verify calls — the DB check now lives only inside
  the shared T2 `Verify Object Removed`).

## Done well
- Full I-U-D-Find, DB-verified against `OV_FIELD` (insert Field Name, update Field Name,
  delete End=Start absent). Live 5/5 PASS on both the original conversion run (2026-08-26,
  per PR #529's cited evidence) and this backfill's independent re-run (2026-08-27).
- Fixed test code discipline: `AUTOTEST_FIELD` confirmed free via a fresh `oracledb`
  connection BEFORE each run, and confirmed 0 residual AFTER — both in PR #529's own evidence
  and reproduced independently in this backfill.
- The navigator-fill reuse (PR #525) worked cleanly on a screen the shared keyword wasn't
  originally built for — the keyword's documented single-dropdown-cascade limitation matched
  Field's real DOM shape exactly, confirmed live before conversion rather than assumed.
- No shared T1/T2 file changes were needed for either PR — `resources/manage_object.resource`/
  `common.resource` were untouched; Field's navigator shape already fit the existing keyword.

## Done wrong / lessons
- **Missing import shipped in PR #525's first pass.** `field_page.resource` had never
  imported `libraries/PropertiesReader.py` before (it had no properties-file mechanism at
  all), so the shared keyword's `Read Properties` call failed at suite-setup time once the
  navigator delegation was wired in. This was caught by the MANDATORY full-tree dryrun, not
  by review or assumption: the dryrun count regressed from 846/846 to 842/846 immediately
  after the page-object edit, before the import fix restored it. This is the honest record —
  a real defect shipped in a first-pass edit, and the process (mandatory dryrun before any PR)
  is what caught it, exactly as the process is designed to. Not smoothed over: without the
  dryrun gate this would have been a live-run failure discovered later, not a static check
  caught immediately.
- **Partial conversion left an inconsistency window.** PR #525 deliberately scoped itself to
  navigator-fill only, leaving Field's TC count/structure on the old 4-TC/generated-code shape
  for a period until the owner's 2026-08-26 standing rule (any Area-layout navigator screen
  gets Area's FULL pattern) was applied via PR #529. Scoping a change narrowly is not wrong on
  its own, but it does mean a screen can sit in a half-converted state between two PRs — worth
  noting for anyone reading history mid-stream.
- **PR #529 shows CLOSED, not MERGED, in GitHub** despite its content being live on master
  (commit `a5104dea`, confirmed via `git log`). This backfill task flagged the discrepancy
  rather than assuming either the PR metadata or the file content was correct — verified via
  `git log --oneline -- field_iud.robot`, which shows the conversion commit is real and present
  on master, so the automation itself is genuine and live-tested; only the PR's own merge
  bookkeeping is unclear (likely merged by another route, e.g. a manual merge outside the
  standard `gh pr merge` flow, or a squash onto a different branch that GitHub could not
  associate back to PR #529). This does not affect the correctness of the shipped automation.

## Blockers → resolution
- PropertiesReader import gap (above) — resolved same session via the dryrun gate, no data
  damage, no live run affected.
- No other blockers; both PRs' own evidence sections show clean baseline/after comparisons.

## Decisions
- Field keeps its genuine OV-GM Area-navigator gesture — the Area-pattern conversion is a
  STRUCTURAL conversion (TC count, login/logout shape, properties-driven data, DB-verify
  location), not a reclassification of Field as plain Bank-shaped. The navigator step is real
  and required, not removed by this conversion.
- Geo Area is filled to the navigator's Area value on Insert (business-rule requirement for
  the new row to be visible under this OV-GM scope) but deliberately excluded from the
  round-trip form-label comparison (`@{FIELD_FORM_LABELS}` = Field Code/Field Name only) —
  same re-render caveat as Area's own Op Production Unit field.
- Legacy Playwright bundle (`playwright/ec_iud_field.py`, `investigation/*.py`) kept unchanged
  as historical reference, not updated to match the RF conversion — items 4/5 of the
  deliverable checklist are permanently waived for Bank-/Area-pattern work; the Universal
  Screen Engine replaces that role going forward.

## Evidence
- PR #525: baseline `field_iud.robot` 4/4 PASS, post-change 4/4 PASS (identical), full-tree
  dryrun 846/846 PASS (after fixing the 842/846 regression), fresh-connection DB re-check
  `SELECT COUNT(*) FROM OV_FIELD WHERE CODE = 'AUTOTEST_FLD_20260826100338'` → 0.
- PR #529: live `field_iud.robot` 5/5 PASS (TC01–TC05), full-tree dryrun 847/847 PASS,
  robocop on changed files 7 issues (parity with Area's own 7-issue baseline, not a
  regression), 29 filter-keyword hits in live `output.xml`, zero inline DB-verify calls
  confirmed via grep, fresh-connection DB self-clean `SELECT COUNT(*) FROM OV_FIELD WHERE
  CODE LIKE 'AUTOTEST%'` → 0 both before and after the live run.
- This backfill (2026-08-27, independent re-run, evidence in `evidence/backfill-2026-08-27/`):
  full-tree `robot --dryrun tests/` → 883/883 PASS; live `field_iud.robot`
  (`EC_HEADLESS=true`) → 5/5 PASS (TC01–TC05); fresh-connection DB check
  `SELECT COUNT(*) FROM OV_FIELD WHERE CODE LIKE 'AUTOTEST%'` → 0; `grep` on live
  `output.xml` → 14 `Find Field Row By Filter` + 15 `Find Object Row By Filter` + 5
  `Clear Field Row Filter` + 15 `Clear Object Row Filter` hits; `py
  scripts/check_bundle_hygiene.py` → RESULT: PASS (167 bundles scanned, no hardcoded creds,
  ASCII-clean, no CHECKLIST/VERIFY-REPORT contradictions).
