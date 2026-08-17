# JOURNAL — feature/engine-stability-batch7-round6

Branch scope: round 6 of the engine stability program - the last 16 screens (of the 92 total with
existing hand-written drivers) never yet run through the Universal Screen Engine. Production Day
Table stays excluded (self-clean permanently impossible by design, already proven, "run
sparingly"). This closes out the full population of screens that had an existing driver to build a
stability test from.

## Screens this round (16)

Create Calculation, Dummy Tag Event Object, Financial Item Definition, Financial Item Template,
Project Data Mapping Setup, Reservoir Block Formation, Split Item Other, Stream Item, Test
Separator, Transactional Inventory Layout Set, Transactional Inventory Properties, UOP Key, Well
Bore, Well Bore Interval, Well Hole, Well Hookup.

## Result: 16/16, no engine.py changes needed

Unlike rounds 1-5, this round found **zero genuine defects in `engine.py`**. Both failures were
bugs in the test harness itself (`tmp/stability_test_round6.py`), not the engine:

1. **Financial Item Template**: the harness's pre-existing-row check assumed `find_grid_row()`
   returns `None` when nothing matches. It actually raises `FieldNotFound`. Fixed by catching the
   exception instead of checking for `None` - a one-line fix, confirmed working immediately.

2. **Reservoir Block Formation** (the real story of this round): repeatedly failed with "dropdown
   option not found" when linking a freshly-created Reservoir Block and Reservoir Formation. Three
   live-tested theories were tried and disproven in sequence before the real cause was found:
   - Time-based commit-visibility delay (like Production Day Table's ~10s) - disproven: 2+ minutes
     of retrying still failed.
   - Page-session dropdown caching, fixed by re-opening the screen fresh each retry - disproven:
     5 fresh screen re-opens in a row still failed identically.
   - Close-then-recreate-at-the-same-Start-Date creating a date-effectiveness conflict (the
     harness's own pre-clean step does exactly this) - disproven: a direct, isolated test of that
     exact sequence worked fine.

   The real cause, found only after directly reading the dropdown panel's raw HTML instead of
   trusting an automated timeout as proof of absence: **"Reservoir Formation"'s dropdown keys its
   option-matching attribute (`data-item-label`) by the object's CODE, not its Name** - unlike the
   very next field over, "Reservoir Block", which keys by Name. The harness was searching Formation
   by Name (`"AUTOTEST R6 RBF Formation"`), which never matches, even though the option was
   genuinely present and visible in the panel the entire time. Fixed by searching by Code instead.
   Confirmed with a full, live, headed re-run: Insert/Update/Delete/self-clean all PASS.

   The pre-existing hand-written driver (`reservoir_block_formation_iud.py`) has this identical
   latent mistake - it also searches Reservoir Formation by Name - but it never surfaced there
   because `ec_object_iud.select_dropdown()` silently falls back to "pick whatever's first
   available" instead of raising an error when a requested value isn't found. That means the
   original driver's own "PASS" claim never actually verified it linked to the SPECIFIC Formation
   it intended to - only that Save succeeded on whatever it fell back to.

## Real process mistakes this round (see LEARNING-SCORECARD.md for the full calibration-log entry)

- Repeatedly concluded a dropdown was "empty"/"not found" from a script's timeout, without
  actually opening the dropdown and reading its real content - the exact class of mistake already
  documented in this project's standing rules, repeated multiple times before the owner pointed
  directly at a screenshot proving the option was visible.
- Spent most of the investigation re-verifying the WRONG field ("Reservoir Block", which was never
  broken) instead of isolating which of the two `select()` calls was actually throwing
  ("Reservoir Formation").
- Ran several one-off `py -c` inline diagnostic commands instead of proper script files under
  `tmp/`, against a standing project convention.

## Results, 16 screens

| Screen | Result |
|---|---|
| Dummy Tag Event Object, Split Item Other, Test Separator, Transactional Inventory Layout Set, Transactional Inventory Properties, UOP Key, Well Hole, Well Hookup, Financial Item Definition, Project Data Mapping Setup, Well Bore, Well Bore Interval, Create Calculation | 13/13 clean, first attempt |
| Stream Item | Clean - Update deliberately out of scope (EC scheduler job `UpdateStreamItem` not configured in this sandbox, owner instruction 2026-08-02, matching the real driver's own documented limitation). Insert + Delete PASS. |
| Financial Item Template | Clean after fixing the harness's `find_grid_row()` misunderstanding. |
| Reservoir Block Formation | Clean after fixing the harness's Formation dropdown search key (Code, not Name). |

Final: **16/16 screens, full I-U-D (or documented Insert+Delete-only) PASS + self-clean, confirmed
via a fresh DB connection.**

## Self-clean status

All round-6 codes confirmed absent via a fresh DB connection, including the 2-object junction
(Reservoir Block + Reservoir Formation, torn down in reverse dependency order after the linking
Reservoir Block Formation record was removed first).

## Program status

This closes out all 92 screens that had an existing hand-written driver as ground truth - 6 rounds,
92/92 tested, engine defects found and fixed across the program: GO-after-Save (round 2), numeric
fill tolerance (round 3), draggable popup dialogs (round 3), `apply_navigator()` levels-default
over-filtering (round 5). Round 6 found zero new engine defects - both failures were test-harness
bugs, a useful signal that the engine itself has stabilized faster than the test scaffolding
around it.
