# CHECKLIST - Item 3: the 2 tool fixes (keep-or-discard decision -> KEEP)

Owner asked me to complete item 3, i.e. decide. Decision: **KEEP both** - each fixed a defect that was
demonstrated, not suspected. Ticks below are executed-command output.

## Fix A - scanner grid detection was FLAKY
- [x] Defect reproduced: two consecutive `scan_ec_screen.py` runs on Service returned **`grid id: None`**
      and **`grid id: manageObject:form:T_data`**. A flaky scan silently records the wrong screen shape.
- [x] Root cause identified: step-0 readiness can be satisfied by navigator/GO alone while the grid has not
      rendered, and on a gated screen the grid appears only after a SECOND render (nav fill + GO). Grid
      detection had no wait of its own.
- [x] Fix: poll up to ~20s after GO for a `:T_data` grid; if none, print an explicit "do NOT record 'no
      grid' as this screen's shape" note.
- [x] Verified by REPETITION (the right test for flakiness): `tmp/scan_service_thrice.py` ->
      3/3 runs returned `manageObject:form:T_data`, `stable: True`, exit 0.
- [x] Regression check on a different shape: re-scan of Report Group reports
      `screen ready: {'nav': 4, 'grid': 1, 'form': 0, 'go': 1}`, the `da_input` nav field, `button:form:B`
      and grid `report_group_table:form:T_data` - matching the ground truth established by hand.

## Fix B - `parent_dd` marking -> now REPLACED BY EVIDENCE
- [x] The UNVALIDATED warning was added because the capability shipped in #288 with no passing screen.
- [x] Item 1 then PROVED it (Area, 7/7, exit 0), so the warning is removed and the evidence recorded in the
      code comment instead. See `tmp/CHECKLIST_item1_parent_dd.md`.
- [x] Verified the warning only ever fired for `parent_dd` and never for a plain-OV generation:
      `gen_ov.py` run -> 0 occurrences; `gen_ovgm.py` with `parent_dd` -> 1 occurrence.

## Repo-wide gates after both fixes
- [x] `scripts/check_bundle_hygiene.py` -> `RESULT: PASS` (28 manifest screens; includes the doc-row family
      check over registry + scorecard + bundle CHECKLIST/JOURNAL/KB).
- [x] Full `robot --dryrun tests/` -> **635 tests, 635 passed, 0 failed** (proves no import/keyword broke).
- [x] No-loss diff on the 3 screens the #287 reviewer kept as-submitted (Driver, Trailer, Cargo Planning
      Forecast): **0 unexplained deletions** across all 6 files.

## Staging discipline
- [x] Committed via `scripts/safe_commit.py`, which stages ONLY explicitly-named paths, prints the staged
      set before committing, aborts on any extra file, and appends the R8 sync line from the sync it ran.
