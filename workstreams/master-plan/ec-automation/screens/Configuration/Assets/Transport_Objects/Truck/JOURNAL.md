# JOURNAL - Truck (CO.0264) plain-OV IUD + plain-OV GENERATOR audit

## 2026-07-31
- **Branch:** `feature/truck-iud`. Group A #5. Doubles as the end-to-end audit of the NEW plain-OV
  (Bank-family) generator `tmp/gen_ov.py`, built because ~30 remaining Group A screens are plain OV
  and only an OV-GM generator existed.
- **Generator built by transforming the proven `gen_ovgm.py`** (grid id, date-only navigator, no Op PU,
  Bank-family docs). **The audit exposed and fixed 6 real defects - none would have been caught by
  reading the code alone:**
  1. leftover `assert pu` from the OV-GM navigator -> NameError at runtime.
  2. plain-OV grids do NOT lazily drop a closed row -> delete verification needed an explicit GO
     re-query (`wait_for_row_absent` alone polls a stale grid).
  3. re-opening the screen to refresh is NOT viable (the tv-link is not re-findable once open) ->
     GO re-query instead.
  4. **UNSAVED CHANGES dialog** (YES/NO) appears on plain-OV screens when a GO happens with a pending
     edit (e.g. right after End=Start) and BLOCKS the GO button -> added `commit_unsaved_changes()`
     at 4 call sites (YES commits the pending End Date, which is the intended delete).
  5. grid id is not universal -> new `grid` config key (Truck uses `truck_object:form:T_data`).
  6. many screens have mandatory FREE-TEXT extras -> new `extra_texts` config key; and the generated
     insert keyword then broke robocop LEN03 -> template split into
     `Fill <Screen> Mandatory Fields` + `Insert <Screen> Record` (LEN03-proof for any field count).
- **Mandatory set discovered from EC itself, iteratively:** each save returned "Required fields are
  empty. Please enter data for these fields: ..." naming the next missing one - Licence Plate No,
  then 3 quantity fields, then Transport Company. This is MORE reliable than the yellow-cell scan
  (several of these render white). Banked as a technique.
- `verify_screen.py` -> **OVERALL PASS** (run 2; run 1 failed ONLY robocop LEN03, live 4/4 both runs):
  robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4, Playwright 8/8. Self-clean 0 residual.

## Lessons
- A generator is only proven by a full green screen: this one looked correct after transformation and
  still had 6 runtime defects. R32 (never batch off an unaudited generator) earned its keep again.
- When a save is rejected, EC's message is a FIELD SPEC - read it instead of guessing mandatory sets.
