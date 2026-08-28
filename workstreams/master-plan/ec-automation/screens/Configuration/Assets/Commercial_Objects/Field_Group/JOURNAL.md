# JOURNAL — Field Group IUD

_Screen: Configuration > Assets > Commercial Objects > Field Group (OV, no navigator, plain
Bank-pattern). View `OV_FIELD_GROUP`._
_This JOURNAL was backfilled 2026-08-28 (`docs/lean-deliverable-backfill-workorder.md`, Batch
6) — the bundle predated the JOURNAL rule; the Bank-pattern conversion itself (PR #434) was
built 2026-08-23 under the since-retired lean waiver. Content below is pulled from PR #434's
real body + this session's own re-run evidence, not invented._

## Built (2026-08-23, PR #434)
- Converted `field_group_page.resource` (T3) and `field_group_iud.robot` from the older
  hardcoded-field-id/generated-code pattern to the label-driven, properties-file-driven,
  T2-consolidated Bank pattern (mirroring Bank/Country), with explicit grid Find/Clear Row By
  Filter wiring included from the start.
- New properties files: `testdata/field_group_{insert,update,form_verify,grid_verify}.properties`.
- Additive credential pair in `resources/credentials.py`: `FIELD_GROUP_EC_USER`/
  `FIELD_GROUP_EC_PASS`.
- Registry row (`docs/ec_screen_registry.md`) and scorecard row (`docs/automation-scorecard.md`)
  updated at merge time of PR #434 — not re-touched by this backfill.
- Part of Batch 3 of the Bank-pattern conversion project (5 screens built in isolated git
  clones per `tmp/batch3_shared_findings.md`: Customer, **Field Group**, Licence, MMS Lease,
  Operator Lease).

## Done well
- Full I-U-D DB-verified against `OV_FIELD_GROUP` (insert/update Name+Description, delete
  End=Start absent); self-clean confirmed both pre-run and post-run via a fresh `oracledb`
  connection (PR #434's own cited evidence).
- Live RF run at conversion time: 5/5 PASS (TC01-TC05), first attempt, no retry needed.
- Live field labels confirmed via a throwaway RF recon script (deleted before commit, per
  convention) rather than assumed from a sibling screen: Code/Name/Start Date mandatory;
  End Date/Description/Comments/Field Group Type (dropdown)/Reporting Field Group Indicator
  (checkbox) all confirmed optional.
- The plain manage-object navigator (no mandatory nav scope) was reconfirmed live at
  conversion time, matching what the registry already said — no surprise mismatch.
- The `objectdates` End Date field id was reconfirmed live to match the pre-conversion file's
  own value exactly (zero drift across the rewrite).
- `robocop check` on the changed files: 9 issues (4 VAR02 + 5 DOC02), identical in kind/count
  to the established baseline — this backfill's own re-run (2026-08-28) reproduced the same
  9-issue count exactly, confirming no drift since merge.

## Done wrong / lessons
- No defect or regression was disclosed in PR #434's own body for this screen specifically.
  The main procedural lesson carried from Batch 3 as a whole (per the batch's shared-findings
  doc) is the isolated-git-clone-per-screen discipline used to avoid cross-screen file
  collisions during a 5-screen parallel batch — Field Group itself hit no such collision.
- This backfill's own note: the bundle's original `field_group_sow.md` (dated 2026-06-12,
  pre-Bank-pattern) still described the OLD generated-code test data
  (`AUTOTEST_FG_<timestamp>`) and the old grid-id literal `manage_object_nav_nav:form:T_data`
  as if current. Left the original Sections 1-5 historically intact (they describe the
  2026-06-12 build accurately) and added a Section 6 addendum documenting what actually
  changed in the 2026-08-23 conversion, rather than silently overwriting the history.

## Blockers -> resolution
- None disclosed in PR #434 for this screen. No blockers encountered during this backfill's
  own re-run (dryrun and live run both passed on the first attempt).

## Decisions
- RF stays the live-maintained suite; the pre-existing Playwright reference
  (`playwright/ec_iud_field_group.py`) is kept in the bundle unchanged — permanently waived
  from further rebuilding per `docs/lean-deliverable-backfill-workorder.md` (Universal Screen
  Engine replaces that role).
- Fixed test code `AUTOTEST_FIELD_GROUP` (matching Bank/State/Country/Object List's
  convention) — every run must reach TC05 Delete so the code stays free for the next run.

## Evidence
- PR #434 (merged 2026-08-23): live RF run 5/5 PASS; fresh `oracledb` connection confirmed 0
  residual `AUTOTEST_FIELD_GROUP` rows in `OV_FIELD_GROUP` pre- and post-run; `output.xml`
  grep confirmed `Find Field Group Row By Filter` fired exactly 5 times; `robot --dryrun`
  full-tree 735/735 PASS at that time.
- This backfill (2026-08-28): `robocop check` on `field_group_page.resource` +
  `field_group_iud.robot` -> **9 issues** (4 VAR02 + 5 DOC02), exact parity with PR #434's
  baseline. Full-tree `robot --dryrun tests/` -> **883/883 PASS**. Live headless run
  (`EC_HEADLESS=true robot tests/Configuration/Assets/Commercial_Objects/field_group_iud.robot`)
  -> **5/5 PASS**, first attempt, no retry needed — artifacts in
  `evidence/backfill_2026-08-28/` (`log.html`, `output.xml`, `report.html`). DB self-clean:
  fresh `oracledb` connection (`localhost:1521/ORCL`, `ECKERNEL_EC`) ->
  `SELECT COUNT(*) FROM OV_FIELD_GROUP WHERE CODE = 'AUTOTEST_FIELD_GROUP'` = 0;
  `SELECT CODE FROM OV_FIELD_GROUP WHERE CODE LIKE 'AUTOTEST%'` = no rows. Hygiene:
  `py scripts/check_bundle_hygiene.py` -> PASS (167 bundles + 272 recon scripts scanned; one
  pre-existing unrelated WARN on a different screen's recon script, Contract Area).
