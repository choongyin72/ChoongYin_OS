# JOURNAL - Project Data Mapping Setup

## Built
Full Insert->Update->Delete via the Universal Screen Engine, live + DB-verified, self-cleaned to
0 residual (`AUTOTEST_PDMS_007`). Update explicitly demonstrates the known Reference-field fix
(re-select the same already-correct value before Save, since it fails to auto-display on
row-select). Only the confirmed-mandatory fields filled, plus Target Property (satisfies the
cross-field OR-mandatory rule) and Reference (required by the chosen Mapping Type).

## Context
This screen was originally built 2026-08-14 as Phase 4 Pilot 3 - by far the hardest pilot, proving
a genuine multi-level cross-screen master-data dependency chain plus several real engine bugs
(see `docs/universal_screen_engine_design.md`'s "Pilot 3" section). That work proved INSERT and
DELETE live and DB-verified, but never packaged a `screens/` bundle, registry row, or scorecard
row - tracked as open-items tracker item #7 (Issue #385 item 2). This pass closes that gap.

## Real mistakes made and fixed in this packaging pass (disclosed, not hidden)
- **Date-effectivity mismatch (Target Property).** First attempt used Start Date = 2000-01-01.
  Insert failed silently trying to select Target Property = "Oil Sands Projects" - the option
  never appeared. Traced via a real DB query (not repeated live guessing):
  `OV_PROPERTY.OBJECT_START_DATE` for that record is 2003-01-01 - the popup's
  `PopupDependency` scopes by the row's own Start Date, so a record can't show up before its own
  effective date. Fixed by moving Start Date to 2003-01-01.
- **Date-effectivity mismatch (Reference), same class of bug, different record.** With Start Date
  fixed to 2003-01-01, Save then failed with "Report Reference must be chosen" (Mapping Type's
  chosen value makes Reference mandatory). Selecting Reference = "Allowed Costs - Capital Test"
  then failed the same way - checked the DB again: that Report Reference's own
  `OBJECT_START_DATE` is 2009-01-01, later than Property's. Fixed by moving Start Date to
  2009-01-01 (the LATER of the two real constraints, not just re-guessing a bigger number).
- **A live-UI diagnostic click was added mid-debug, then removed.** While chasing the Target
  Property failure, a standalone "open the dropdown and print what's really there" step was added
  to the driver - flagged by the owner as exactly the trial-and-error pattern this project's
  standing rule (`feedback_no_third_option_trial_error`) exists to prevent. Removed; the actual
  fix came from the DB query above, not from re-clicking the live screen to look.
- **`open_screen()`'s toolbar click failed once with a stale-layout cause, not a data cause.** A
  separate manual "expand icon" click was added in an exploratory script AFTER `open_screen()`
  had already expanded the screen itself as its own trailing action - the second click toggled it
  back to collapsed, which is why the subsequent "New Object" toolbar link couldn't be found.
  Root-caused by reading `engine.py`'s own code (the trailing `minmaxMenu` click at the end of
  `open_screen()`), not by re-testing live. Fixed by removing the redundant click.

## Real engine improvement made during this pass
While investigating why constructing the Engine on this screen's rich New Object form (~11
dropdown fields) felt slow/wasteful, traced the actual cause in `engine.py`: `_refresh_field_map()`
eagerly classified every field's primitive via a live click-probe, including fields the task never
touches. Fixed properly (not worked around): dropdown-vs-popup classification is now lazy, resolved
only the first time a field is actually accessed via `fill()`/`select()`/`check()`/`resolve_popup()`.
Verified live before/after (touching one field resolves only that field, others stay unclicked) and
via the mandatory `engine_canary.py` regression gate (Bank + Language, ALL PASS, run twice - once
per real change, since a self-caught cache-check bug in the first attempt needed a second fix).
Shipped as its own PR (engine.py is shared code), not bundled into this screen's packaging PR.

## Done well
- Re-derived the real treeview path (`Configuration > Assets > Data_Mapping_Objects > Project Data
  Mapping Setup`) by querying the live `TV_CTRL_CONFIGURATION_STORAGE` treeview JSON directly and
  confirming this screen is a structural sibling of Property/Project Properties in the same
  `COST_CONFIG` folder - not inferred from folder-naming similarity alone.
- Confirmed the screen's actual mandatory-field set live via `Engine.field_inventory()` on the
  empty New Object form, rather than assuming it matched the original pilot's prose description.
- Every date-scoping constraint was resolved via a real DB query before being used in a live
  action, not by re-clicking the screen to "see what's there" - consistent with the project's
  no-guessing standard.
- Ran a completely fresh live proof (`AUTOTEST_PDMS_007`, 2026-08-16) rather than repackaging old
  evidence from the original Pilot 3 session (`AUTOTEST_PDMS_006`, already self-cleaned).

## Evidence
`evidence/01_loaded.png` through `07_final_state.png` - fresh 2026-08-16 run. DB re-check: 0 rows
for `AUTOTEST_PDMS_007` in `OV_COST_MAPPING` after delete. Delegator
(`playwright/ec_iud_project_data_mapping_setup.py`) independently re-run and re-verified clean.
