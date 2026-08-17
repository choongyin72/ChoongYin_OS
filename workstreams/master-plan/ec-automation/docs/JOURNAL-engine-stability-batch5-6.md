# JOURNAL — feature/engine-stability-batch5-6

Branch scope: continuation of the engine stability program (see
`JOURNAL-engine-stability-15screen-fixes.md` for rounds 1-4, 60 screens, PR #398 merged). This
round: 15 more real screens with existing hand-written drivers, never touched before, run against
the Universal Screen Engine with every real fact re-read directly from each screen's own
`*_iud.py` driver (per the round-1 lesson: never extrapolate config from a similar-looking screen).

## Screens this round (15)

Orifice Plate, Pilot Boat, Process Train, Production Separator, Reservoir Block, Reservoir
Formation, Revenue Stream Category, Service, Storage Flow, Stream Item Category, Task Process,
Shift, Report Group, Perforation Interval, Remote Endpoint Configuration.

**Production Day Table was deliberately excluded** - its own driver documents self-clean as
permanently impossible by design (same precedent class as Royalty Contract, owner-accepted) and
instructs running it sparingly. Re-running it would only add another permanent, unremovable
residual row for a fact already on record; a 15th screen (Task Process) was substituted instead.

## Real engine defect found + fixed

`apply_navigator(values=[...])` used to default `levels=4` regardless of how many values the
caller actually supplied, silently filling any EXTRA discovered nav column with `__FIRST__` even
when the caller never asked for it. Confirmed live on Service (nav column count = 3, caller only
ever needs to set column 1 "TS3 BU1", matching the real hand-written driver): the default call
narrowed the grid from its real 20 rows down to 1 unrelated row, making a freshly-inserted Service
object invisible with zero error - it just vanished from the grid. Root-caused by direct
comparison: `apply_navigator(values=["TS3 BU1"], levels=1)` correctly showed all 20 rows including
the hidden one; the default `levels=4` call showed only 1. This is a genuine, reproducible defect,
distinct from every screen already covered in rounds 1-4 (none of them happened to have MORE nav
columns than the caller's `values` list length while those extra columns were independently-valued
rather than true cascade children).

Fix: `levels` now defaults to `len(values)` when `values` is supplied (matching every real
driver's own touch-only-what-I-set behavior), and still defaults to 4 when `values=None`
(first-available cascade mode, unchanged). `engine_canary.py` (Bank OV + Language TV) re-verified
PASS both before and after the change.

This was only caught because of the row-identity verification guard added after the Contract
Inventory incident (rounds 1-4 journal) - without it, the Update step's `select_row()` finding the
wrong / no row would have gone unnoticed the same way Contract Inventory's did.

## Test-harness-only bug found + fixed (not an engine defect)

Remote Endpoint Configuration's Save call intermittently failed with a 30s locator timeout. Traced
to the test harness's OWN `_save()` helper, which reimplemented a simplified, fragile
title-attribute-based Save locator instead of reusing the project's proven `ec.save()` (which has a
toggle+Ctrl+S fallback for exactly this case - EC blanks the anchor's `title` attribute after the
first Save/hover interaction on a screen, a gotcha `engine.py`'s own `_save()` already documents
and works around). Fixed by calling `ec.save(page)` directly. No `engine.py` change needed here -
this was a case of hand-writing a simplified helper instead of reusing the already-correct one.

## Results, 15 screens

| Screen | Result |
|---|---|
| Orifice Plate, Pilot Boat, Process Train, Production Separator, Reservoir Block, Reservoir Formation, Revenue Stream Category, Storage Flow, Stream Item Category, Task Process, Shift, Report Group, Perforation Interval | 13/13 clean, first attempt, zero engine defects |
| Service | Update initially appeared to PASS but the DB showed it never persisted; row-identity guard caught the underlying cause (wrong grid scope from the `apply_navigator` defect above) on the next Delete attempt. Clean 15/15 after the fix. |
| Remote Endpoint Configuration | Insert initially mis-reported FAIL due to a missing retry-delay in the harness's own DB check (the row was actually inserted correctly - confirmed by direct query); then Save timed out on Update/Delete due to the harness's own `_save()` bug above. Clean 15/15 after both harness fixes. |

Final: **15/15 screens, full I-U-D PASS + self-clean, confirmed via a fresh DB connection.**

## Self-clean status

All round-5 codes confirmed absent via a fresh DB connection (`preflight_round5_codes.py` re-run
post-batch). Three timestamp-coded Remote Endpoint Configuration residuals from the
pre-fix attempts were cleaned up explicitly (code-verified before each delete) once the `ec.save()`
fix landed.

## Not covered / left open

- Production Day Table remains untested by design (see above) - already proven insert-only in an
  earlier round, no new information to gain from re-running it.
- The `apply_navigator` `levels` fix widens correctness for every screen with `values=[...]` and
  MORE nav columns than the caller lists; it was only verified against Service directly plus the
  two canary screens (neither of which has this exact column-count shape) - worth a specific
  regression screen if this class of screen becomes common in a future round.
