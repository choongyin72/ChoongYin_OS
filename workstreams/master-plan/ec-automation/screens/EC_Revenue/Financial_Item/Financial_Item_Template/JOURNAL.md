# JOURNAL - Financial Item Template

## Built
Full Insert->Update->Delete (physical) via the Universal Screen Engine, live + DB-verified,
self-cleaned to 0 residual (`AUTOTEST_FIT_001`). Only the 3 confirmed-mandatory fields filled
(Code/Name/Valid From) - navigator filter fields (Business Unit/Contract Area/Date) all confirmed
optional via `field_inventory()` and left untouched.

## Context
Originally built 2026-08-14 as Phase 4 Pilot 2 - see `docs/universal_screen_engine_design.md`
section 23 for the 3 real engine/generator gaps found there. Never packaged into a `screens/`
bundle, registry row, or scorecard row - found as a gap during a 2026-08-16 cleanup pass (same
gap as Financial Item Definition).

## Done wrong (this packaging pass)
- First insert attempt: resolved the newly-inserted blank row via `find_grid_row(grid_id, "")`,
  which matches the FIRST row containing ANY blank cell (list-membership check, not "is this row
  wholly blank") - an EXISTING row's blank optional column (e.g. row 0's blank Contract Area) was
  found first, so the fill landed on the wrong row entirely and Save correctly rejected it
  ("Required fields are empty... on row 2"). Root-caused by dumping the live grid's actual row
  contents rather than guessing again - fixed by requiring BOTH Code and Name cells empty, the
  real signature of the new row (confirmed live: new row landed at index 1, not the end of the
  grid).

## Done well
- Diagnosed the row-resolution failure via a direct live DOM dump (`tmp/recon_fit_grid_insert.py`)
  instead of trying random row-index guesses.
- Confirmed navigator fields are genuinely optional (not gating) via `field_inventory()` before
  assuming they needed to be filled - matches this project's "only fill needed fields" rule.

## Evidence
`evidence/01_loaded.png` through `07_final_state.png` - fresh 2026-08-16 run. DB re-check: 0 rows
for `AUTOTEST_FIT_001` in `FINANCIAL_ITEM_TEMPLATE` after delete (physical removal confirmed).
