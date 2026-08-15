# Royalty Contract - Delete-blocked root cause (read-only investigation record)

Summarizes the read-only DB investigation from PR #331 (2026-08-02) that root-caused why Delete
(End Date = Start Date) genuinely cannot succeed on this screen - reproduced again 2026-08-15
before packaging this bundle.

## Method
1. Live repro: select Contract Template = "Royalty Fixed Percentage Canada" on Insert, then attempt
   End=Start close on the same record. EC's own error banner reports `"Child record found... all
   child records must be deleted first"` (captured via `ec.ec_error()`, screenshot
   `evidence/rc_05_delete_blocked_EC_defect_proof.png`).
2. DB root cause (not guessed): checked every table with a live FK to `CONTRACT` for rows tied to
   the test object's `OBJECT_ID`. Found exactly `CNTR_PG_SETUP` (10 rows, one per Product Group x
   member-Product: `BLEND`->{Diluent,Blend,Shrinkage,Bitumen}, `DILUENT`->{Diluent},
   `TIETO_BLEND`->{Diluent,Blend,Shrinkage,Bitumen}, `TIETO_DIL`->{Diluent}) plus the expected
   `CONTRACT_VERSION` (1 row, normal).
3. Confirmed these 10 rows are a genuine EC side effect of the template's own royalty-percentage
   business logic (all `CREATED_BY='sysadmin'` at the exact Save timestamp, tied to the test
   object's `OBJECT_ID`) - not pre-existing data, not a bug in `ec_object_iud.py` or the shared
   engine.
4. This screen's UI exposes no path to view or delete `CNTR_PG_SETUP` rows directly, so the
   standard End=Start close can never succeed while a "Royalty Fixed Percentage Canada" contract's
   auto-provisioned children exist.

## Conclusion
Genuine EC product limitation (parent-child relationship), not an automation defect. Delete is
permanently out of scope for this screen's IUD bundle (owner-confirmed 2026-08-15, closes Issue
#336) - same precedent as Production Day Table (CO.1033). Insert and Update are fully proven,
live + DB-verified (see `../VERIFY-REPORT.md`).

## Residual data (disclosed, not hidden)
Each Insert+Update proof run (Playwright driver or RF suite) permanently accumulates one more
`AUTOTEST_RC_*` row in `OV_ROYALTY_CONTRACT`, since there is no way to remove them. As of this
bundle's packaging: `AUTOTEST_RC_001` (original, PR #331), `AUTOTEST_RC_002` (2026-08-15 recon
run), `AUTOTEST_RC_003` (this bundle's own official driver proof), plus 2 RF-suite timestamp-coded
rows from the live suite verification runs (`verify_screen.py`) - 5 total, all accepted per the
same owner decision that closed Issue #336.
