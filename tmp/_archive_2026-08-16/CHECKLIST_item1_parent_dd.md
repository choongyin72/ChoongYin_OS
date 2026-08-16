# CHECKLIST - Item 1: prove `parent_dd` (OV-GM parent-dropdown binding)

Every tick below is a line of output from a command that ran. Nothing here is filled in from reasoning.
Evidence script: `tmp/validate_parent_dd_area.py` (live, self-cleaning). Result: **OVERALL: PASS 7/7, exit 0**.

## Test-bed selection (read from shipped code, not assumed)
- [x] Node REJECTED as the test bed - its own driver documents that the Op PU panel offers only 5 PUs and
      "the nav first-available PU (AS1...) is NOT one of them". `parent_dd` binds the form dd TO the
      captured nav value, so on Node the run would fail for a reason unrelated to the capability.
- [x] Area CHOSEN - its T3 states "the inserted area must carry the same Op Production Unit to appear in
      the filtered grid", and its live-passing suite passes `${NAV_PU}` to BOTH navigator and form. So the
      PATTERN was already proven there; only MY WIRING (binding the CAPTURED value) was unproven.

## The 7 executed checks
- [x] navigator holds the PU - `captured='Production Unit'`
- [x] save raised no EC error - `(none)`
- [x] **row LISTS in the grid** - this was the untested half of the capability
- [x] row present in `ov_area`
- [x] DB parent == captured nav value, label resolved to code - `stored='EEAL' expected='EEAL' for name 'Production Unit'`
- [x] row absent from `ov_area` after End Date = Start Date
- [x] self-clean - `0 open AUTOTEST rows left`

## Three flaws found in MY TEST, none in the code under test
- [x] filling all 4 nav levels raised `dropdown has no options` - the navigator's C:3 exists but is empty;
      fixed with `levels=1` (only C:1 is mandatory).
- [x] start date `2000-01-01` meant the target PU was not offered at all (Op PU only lists PUs effective at
      the form's start date; 'Production Unit' starts 2002-01-01). Corrected to `2003-01-01`, the value the
      merged suite uses (`environment.py TEST_START_DATE_REFDD`). **I nearly reported an EC engine defect
      off this bad input.**
- [x] compared a UI LABEL to a DB CODE (`'Production Unit'` vs `'EEAL'`). `OV_PRODUCTIONUNIT` confirms
      `EEAL` IS the code for the PU named 'Production Unit'. Assertion now resolves label -> code.

## Outcome, per the commitment made before running
- [x] PASSED, so the `UNVALIDATED` warning is REMOVED from `tmp/gen_ovgm.py` and replaced with the evidence.
      (Had it failed, the commitment was to delete `parent_dd` from the generator entirely.)

## Message Group re-checked against this result (it could have been mis-parked)
- [x] `OV_FUNCTIONAL_AREA`: `Administration` -> code **ADM**; `Allocation` -> code **ALLOCATION**. Message
      Group stored `ALLOCATION` while `Administration` was requested, so that row really did save the
      NEIGHBOURING option - it was NOT the label/code confusion I had just made here.
- [x] Therefore the divergence is SCREEN-SPECIFIC (the identical wiring is correct on Area), the park entry
      and the capability doc's retraction both remain accurate, and no doc needed changing.

## Sandbox
- [x] 0 open AUTOTEST rows in `ov_area` after the run (script's own final check).
- [x] Rows created during the 3 runs were closed via End Date = Start Date (EC's delete), full row logged
      before any write.
