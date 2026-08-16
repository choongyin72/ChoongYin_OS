# CHECKLIST - Collection Point (CO.0205): first screen built using find_populated_scope.py

Ticks are executed-command output. Gate ticks from `verify_screen.py` -> `VERIFY-REPORT.md` (**OVERALL:
PASS**, exit 0, first live run).

## Recon - USED THE NEW TOOL instead of repeating the manual pattern a 4th time
- [x] step-0 check: only the target row, no prior diagnosis skipped.
- [x] live scan: 3-level MANDATORY cascade (Date -> Production Unit -> Area -> Operator Route). First-
      available PU's Area/Route children came back empty - the SAME trap as Message Group/Service.
- [x] `py scripts/find_populated_scope.py OV_COLLECTION_POINT` (one command, from PR #296) ->
      `CP_PRODUCTIONUNIT_CODE [('P3_PU',3),('FRMW_PU',1)]`, `CP_AREA_CODE [('P3_AREA',3),...]`,
      `CP_OPERATOR_ROUTE_CODE [('P3_ROUTE_1',2),...]` - proven scope in ONE query, not a multi-step
      manual live-debugging session like the prior 2 occurrences.
- [x] verified the 3 codes are genuinely LINKED (not independently-popular-but-unrelated): direct query on
      `ov_collection_point` shows `P3_PU/P3_AREA/P3_ROUTE_1` co-occur on 2 real rows.
- [x] resolved codes to labels: `P3_PU` -> `P3 Production Unit`, `P3_AREA` -> `P3 Area`,
      `P3_ROUTE_1` -> `Oper Route 1`.
- [x] probed the insert form UNDER that proven scope before building: grid loaded with 2 rows after GO;
      only 3 mandatory fields (Code/Name/Start Date); the 3 scope dropdowns exist but are OPTIONAL -
      bound explicitly anyway so the new row stays in the same visible scope (the `parent_dd` lesson).

## New generator capability: `nav_values` (list, multi-level explicit cascade)
- [x] `nav_value` (singular, from #292) only sets C:1 then clicks GO immediately - wrong shape for a
      3-mandatory-level cascade; would have clicked GO with C:2/C:3 unfilled and failed live.
- [x] Added `nav_values`: one explicit value per cascade level, set in order (each level's options only
      render once its parent is selected - same ordering `apply_ovgm_navigator` uses internally).
- [x] REGRESSION PROVEN, not assumed: old-style cascade config (`levels=4`, first-available) still emits
      the identical `pu = ec.apply_ovgm_navigator(page)` / `assert pu` body, checked after this change.

## Live gate - FIRST RUN, all 5 PASS
- [x] robocop 0 - [x] hygiene 0 - [x] dryrun 4/4 - [x] **LIVE RF suite 4/4 pass 0 fail** -
      [x] **Playwright driver 8/8**

## Wrong-text defect found by reading every artifact back (4th distinct site this session)
The packager/generator never learned about `nav_values`, so registry/scorecard/JOURNAL got the right
cascade text by coincidence (they read the `nav` list), but 4 more templates still said "first-available"
on a screen that uses PROVEN explicit values - the opposite of true:
- [x] CHECKLIST footer (`FAM_SPEC["ovgm"]` in package_ovgm.py)
- [x] SOW (`sow_nav_line` in gen_ovgm.py)
- [x] KB Navigator line (`KB_NAV`/`kb_nav=` in package_ovgm.py)
- [x] KB Quirks + JOURNAL Lessons (`KB_QUIRKS`/`FAM_LESSON` in package_ovgm.py)
- [x] BONUS defect found in the same pass, independent of nav_values: `kb_oppu=` never checked
      `has_op_pu` at all - it was unconditional on family, so Collection Point's KB claimed "Op Production
      Unit (first-available, grid visibility)" though this screen has none. Fixed alongside.
- [x] all 5 sites made `nav_is_explicit`-aware (and `kb_oppu` made `has_op_pu`-aware); REGRESSION PROVEN on
      an old-style config: SOW still says "first-available" (1 occurrence, unchanged).

## The JOURNAL-overwrite guard (from #293) FIRED, exactly as designed
- [x] Re-packaging after the template fix triggered a real divergence (old JOURNAL had the pre-fix
      "first-available" wording; the regenerated one had the corrected wording) -> **guard ABORTED with
      exit 1**, wrote `JOURNAL.generated.md`, did NOT silently pick one.
- [x] Per the guard's own message ("re-running inside the SAME build -> the generated one is almost
      certainly right"), verified the generated version had the correct text, then used it. This is the
      guard working as intended - built after #292 shipped the wrong file silently.

## Re-verification after all fixes
- [x] `grep -rn "first-available"` across all 6 artifacts + KB, excluding the "PROVEN explicit" phrasing
      itself -> **0 residual false claims**.
- [x] idempotency: re-run -> `registry+=False scorecard+=False`.
- [x] `verify_screen.py` re-run after the template fix -> still OVERALL PASS.
- [x] `check_bundle_hygiene.py` -> RESULT PASS.
- [x] R23: registry/scorecard/manifest edits are pure appends.

## Sandbox
- [x] Suite self-cleans in-suite (gate 15 passed within `verify_screen`'s live RF run).
