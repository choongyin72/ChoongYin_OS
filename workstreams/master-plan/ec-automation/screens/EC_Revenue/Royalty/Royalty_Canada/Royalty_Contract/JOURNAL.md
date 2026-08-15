# JOURNAL - Royalty Contract (INSERT+UPDATE-ONLY)

## Built
- Insert (Code/Name/Start Date/mandatory End Date/Contract Template/Contract Area) + Update (Name)
  driven via the shared `ec_object_iud.py` engine, thin driver `py/royalty_contract_iud.py`.
- T3 page object + RF suite (TC01 clean-state, TC02 insert, TC03 update - no TC04 delete).
- Full 21-item bundle: SOW, README, this JOURNAL, `playwright/` delegator, `investigation/` root
  cause, `evidence/` screenshots, `CHECKLIST.md`, `VERIFY-REPORT.md`, KB map, registry + scorecard
  rows.

## Done wrong (earlier attempt, PR #331, 2026-08-02)
- Original park reason ("2nd dropdown mis-persisting") turned out to be the same test-data
  date-mismatch class bug found across Property/Price Index/Message Group that session - Start
  Date `2000-01-01` predates Contract Area "Alberta"'s own effective date (`2003-01-01`). Not a
  defect in this screen or the shared engine.

## Done well
- Root-caused the Delete blocker via DB (checked all FK-linked tables for the test object's
  `OBJECT_ID`), not guessed - found exactly `CNTR_PG_SETUP` (10 rows) as the EC-genuine side effect
  of the "Royalty Fixed Percentage Canada" template.
- Did NOT attempt Delete again in this pass once the prior investigation's conclusion was found and
  read in full (PR #331) - would have just reproduced the same already-known, already-disclosed
  blocker and added residual data for no new information.
- Reused the existing SOW/T3/suite/driver files verbatim where still correct, only changing what
  the new scope required (default test code bump, pre-clean guard, Delete step removed).

## Blockers -> resolution
- **Delete permanently blocked** (EC product limitation, `CNTR_PG_SETUP` auto-provisioning, no UI
  path to remove) -> resolved by scoping this bundle to Insert+Update only, per owner decision
  (closes Issue #336), matching the Production Day Table precedent.
- **`AUTOTEST_RC_002` already existed** (from an earlier ad hoc verification run this session) ->
  driver's default code bumped to `AUTOTEST_RC_003` rather than attempting a doomed pre-clean.
- **robocop VAR02/SPC03** after removing the TC04 Delete test case (unused `${END_DATE}` variable,
  missing blank line before `*** Keywords ***`) -> fixed, robocop clean.

## Decisions
- Self-clean is impossible by design on this screen (same as Production Day Table) - each proof run
  permanently adds one more `AUTOTEST_RC_*` row; disclosed plainly, not hidden, in SOW/README/
  investigation notes/PR body.
- Kept the T3's "Delete Royalty Contract" keyword in place (not deleted) for reference/future use,
  documented as not currently exercised by the suite - preserves the working gesture code in case
  EC's own limitation is ever lifted.

## Evidence
- `evidence/rc_01_loaded.png` through `rc_04_final_no_delete.png` - fresh 2026-08-15 live run
  (`AUTOTEST_RC_003`).
- `evidence/rc_05_delete_blocked_EC_defect_proof.png` - the original 2026-08-02 screenshot proving
  the EC "Child record found" error, kept as historical proof of the defect.
- `VERIFY-REPORT.md` - `OVERALL: PASS` (robocop, hygiene, dryrun 3/3, live RF 3/3, Playwright 7/7).
