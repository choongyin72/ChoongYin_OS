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
- Diagnosed the row-resolution failure via a direct live DOM dump
  (`investigation/recon_blank_row_diagnosis.py`) instead of trying random row-index guesses.
- Confirmed navigator fields are genuinely optional (not gating) via `field_inventory()` before
  assuming they needed to be filled - matches this project's "only fill needed fields" rule.

## Evidence
`evidence/01_loaded.png` through `07_final_state.png` - fresh 2026-08-16 run. DB re-check: 0 rows
for `AUTOTEST_FIT_001` in `FINANCIAL_ITEM_TEMPLATE` after delete (physical removal confirmed).

## Reviewer follow-up (2026-08-16)
Reviewer MUST-FIX caught two additional incomplete bundle-artifact items missed in the first pass:
`playwright/ec_iud_financial_item_template.py` (bundle-local delegator, was missing) and
`investigation/` (the real recon scripts were sitting in `tmp/`, never moved into the bundle).
Both fixed: `playwright/ec_iud_financial_item_template.py` added (thin delegator, `parents[5]`,
path verified live); `investigation/` now holds `recon_menu_path_and_fields.py` +
`recon_treeview_tooltip.py` (shared recon with Financial Item Definition - both screens' paths
were found in the same script run) and `recon_blank_row_diagnosis.py` +
`verify_db_residual.py` (screen-specific, renamed from their original `tmp/` filenames).
`CHECKLIST.md`/`VERIFY-REPORT.md` remain open pending the owner's RF-layer scope decision (see
PR #379 discussion) - not fixed in this follow-up.
