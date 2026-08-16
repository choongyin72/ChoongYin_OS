# CHECKLIST - Contract Capacity (CO.2044): TABLE-class screen with an OV-GM UI shape

Ticks are executed-command output. Gate ticks from `verify_screen.py` -> `VERIFY-REPORT.md` (**OVERALL:
PASS**, exit 0, first live run).

## Recon caught a real classification contradiction before building
- [x] step-0 check: only the target row, no prior diagnosis skipped.
- [x] live scan: `CLASS_TYPE=TABLE` (resolves to 3 distinct classes: CONTRACT_CAPACITY,
      CAPACITY_REL_CNTR_CAP, CAPACITY_BID_CNTR_CAP) - by the scanner's OV/TV binary this should be TV, but
      no blank insert row was found.
- [x] probed live rather than trusting the class-type assumption: toolbar Insert produces "New Object" /
      "New Version" menu items (OV-style), NOT a TV inline-add-row gesture. `objectForm` with 42 fields
      renders. **Confirmed genuinely OV-GM shaped despite the TABLE classification** - the OV/TV binary
      does not hold universally.
- [x] 5 mandatory fields: Code, Name, Start Date, Contract Name (dd), Location Name (dd).

## Scope trap - caught by find_populated_scope.py + a linkage check, same pattern as Collection Point
- [x] `py scripts/find_populated_scope.py OV_CONTRACT_CAPACITY` -> `CONTRACT_CODE` top values TS3_*,
      `OPERATIONAL_LOCATIONS_CODE` top values TS5_* - **different prefixes, a red flag**.
- [x] verified linkage directly: `TS3_FIRM2`/`TS3_FIRM1` (individually popular) pair only with TS3
      locations; `TS5_DP_GP_GSP` (also popular) pairs only with TS5 contracts. The two most-popular
      individual values are NOT linked to each other - using them together would have produced another
      "saved outside the visible scope" failure. Chose the genuinely CO-OCCURRING pair instead:
      `TS5_FTR_SHB_01` + `TS5_DP_GP_GSP` (paired twice in real data).
- [x] date-effectivity trap (same class as Area's `parent_dd` validation): default start date 2000-01-01
      returned 0 options for "TS5 Shipper B Firm" in the Contract Name panel; corrected to 2020-01-01,
      panel then showed the exact label.
- [x] Location Name resolved WITHOUT guessing: it is NOT a cascade child of Contract Name (230 unfiltered
      options either way), and a plausible-looking substring guess ("TS5 Gas Pool" for code
      `TS5_DP_GP_GSP`) was explicitly rejected. Resolved exactly instead: read `OPERATIONAL_LOCATIONS_ID`
      off an existing linked row, then found the actual backing view `OV_DELIVERY_POINT` by object_id ->
      `'TS5 Domestic Gas Storage'`.
- [x] nav Business Unit resolved via the same 2-hop chain used for Service: contract `TS5_FTR_SHB_01` ->
      contract_area `TS5_CA` -> business_unit `TS5_BU` (name `'TS5 BU'`).

## Live gate - FIRST RUN, all 5 PASS
- [x] robocop 0 - [x] hygiene 0 - [x] dryrun 4/4 - [x] **LIVE RF suite 4/4 pass 0 fail** -
      [x] **Playwright driver 8/8**

## A generator gap found and fixed: TWO explicit-nav mechanisms, only one text-checked
`nav_is_explicit` (added for Collection Point) only checked `nav_values` (plural, multi-level). Contract
Capacity uses `nav_value` (singular, the OLDER #292 mechanism, correct here since only 1 nav level exists)
- so the CHECKLIST/SOW/KB/JOURNAL still said "first-available" on a screen using an explicit value, the
SAME defect class recurring because there are two mechanisms and only one was covered:
- [x] `nav_is_explicit` now checks BOTH `nav_values` and `nav_value`.
- [x] `sow_nav_line` in `gen_ovgm.py` had the identical gap (`if nav_values` only) - fixed alongside.
- [x] REGRESSION PROVEN: old-style config's SOW still says "first-available" (1 occurrence, unchanged).

## A structural gap found: fixes from other branches don't exist on a fresh branch off master
- [x] `has_op_pu`/`nav_is_explicit` text fixes exist only on the unmerged Collection Point/External
      Location branch chain. This branch started from `feature/scope-probe-tool` (off master), which does
      NOT have them - first packaging attempt reproduced BOTH already-fixed defects (false "first-available"
      AND false "Op Production Unit first-available" though `has_op_pu=False`).
- [x] Fixed by MERGING the branch chains together (`origin/feature/collection-point-iud`) rather than
      re-fixing a third time in a new location - the accumulated fix then applied correctly, confirmed by
      re-reading every artifact.
- [ ] Not resolved here, flagged for the owner: until #295/#296/#297 merge to master, every NEW branch
      risks re-shipping these same already-fixed defects. Worth merging that stack soon.

## The #293 JOURNAL-overwrite guard fired again, correctly
- [x] Re-packaging after the nav_is_explicit fix produced a real divergence -> guard **ABORTED exit 1**,
      wrote `JOURNAL.generated.md`. Verified the generated text was correct (referenced
      `find_populated_scope.py` accurately), then used it - second real-build confirmation this guard
      works, not a synthetic test.

## Re-verification after all fixes
- [x] `grep -rn "first-available"` across all 6 artifacts + KB -> **0 false claims** (all remaining hits
      are the correct "PROVEN explicit values, not first-available" phrasing).
- [x] idempotency: re-run -> `registry+=False scorecard+=False`.
- [x] `verify_screen.py` re-run after both template fixes -> still OVERALL PASS.
- [x] `check_bundle_hygiene.py` -> RESULT PASS.
- [x] R23: registry/scorecard/manifest edits are pure appends (verified 3-way merge conflict resolved by
      keeping all three screens' independent rows, no content lost).

## Sandbox
- [x] Suite self-cleans in-suite (gate 15 passed within `verify_screen`'s live run).
