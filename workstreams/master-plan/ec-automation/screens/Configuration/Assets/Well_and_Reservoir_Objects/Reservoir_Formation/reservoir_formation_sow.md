# SOW - Reservoir Formation IUD

## Classification
- **Screen:** Configuration > Assets > Well_and_Reservoir_Objects > Reservoir Formation (BF_CODE **CO.0135**)
- **Type/pattern:** OV (Manage-Object, `manage_object_nav`) - date-effective; **plain Bank/Berth-pattern OV
  (no navigator, no mandatory dropdowns)** - full Bank-pattern conversion (Batch 9, PR #467, merged
  2026-08-23)
- **DB view:** `OV_RESV_FORMATION` (versioned); key `CODE`
- **Delete:** End Date = Start Date -> row leaves `OV_RESV_FORMATION`

## Nav / grid / cells
- **Open:** menu search "Reservoir Formation" -> `label.tv-link`. Navigator = single **Date + GO**; grid needs GO.
- **Grid:** shared T2 `${OV_MANAGE_OBJECT_TABLE}` (= `manage_object_nav_nav:form:T_data`), referenced in
  the T3 as `${RESERVOIR_FORMATION_TABLE}`.
- **NO hardcoded field ids** - resolved BY LABEL, and (post Batch 9) **properties-file-driven** via T2's
  `Insert Object From Properties And Verify Code` / `Update Object From Properties`:
  - **Insert (objectForm):** `Reservoir Formation Code`, `Reservoir Formation Name`, `Start Date`
    (mandatory) - from `testdata/reservoir_formation_insert.properties`. Optional dropdowns skipped.
  - **Update (updateAttributes):** `Reservoir Formation Name` only (Code read-only) - from
    `testdata/reservoir_formation_update.properties`.
  - **Delete (objectdates):** `End Date` = Start Date, via
    `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input`.
  - **Explicit grid-filter wiring** (Batch 9 addition): `Find Reservoir Formation Row By Filter` /
    `Clear Reservoir Formation Row Filter`, wrapping T2's `Find Object Row By Filter`/`Clear Object Row
    Filter` - used before/after Update/Find/Verify-Found/Delete, matching Account/Bank/Berth/State's own
    explicit filter usage (owner, 2026-08-22).

## Test data
- Fixed code `AUTOTEST_RESVF` (Batch 9 changed this from a per-run generated unique code to a fixed
  code, matching Bank/Berth's convention) - confirmed free in `OV_RESV_FORMATION` via a fresh oracledb
  connection before use. `OBJ_NAME` = `AUTOTEST Reservoir Formation` / `OBJ_NAME_UPD` = `AUTOTEST
  Reservoir Formation UPDATED`. Start/End = `2000-01-01`. Never touch real rows.
- 5 TCs, each with its own Login/Logout on one browser opened once in Suite Setup: TC01 Verify Clean
  State, TC02 Insert, TC03 Update, TC04 Find, TC05 Delete.

## Dev story (from PR #467, merged 2026-08-23)
Reservoir Formation's RF suite started as a 2026-07-26 generator-scaffolded build: label-driven T3
(`Fill OV Field By Label`) with a 4-TC suite (no explicit Find TC, no properties-file insert/update, no
grid-filter wiring) plus a Playwright driver (7/7). Batch 9 of the Bank-pattern conversion project
(PR #467) brought it up to the full Bank/Berth shape: properties-file-driven Insert/Update/Verify,
explicit `Find/Clear Reservoir Formation Row By Filter` grid-filter wiring, dedicated per-screen
credentials (`RESERVOIR_FORMATION_EC_USER`/`RESERVOIR_FORMATION_EC_PASS`), fixed test code
`AUTOTEST_RESVF`, and expansion to 5 TCs (added TC04 Find). The PR **modified** the screen's existing
`docs/ec_screen_registry.md` / `docs/automation-scorecard.md` rows (not new rows) since the screen
already had a row from the earlier build.

**Real gotcha from the PR (see body):** the shared Batch 9 findings doc (`tmp/batch9_shared_findings.md`)
said the Batch 9 section headers in `docs/bank-pattern-conversion-checklist.md` /
`docs/grid-filter-standardization-checklist.md` were pre-created on master via PR #464, but at the time
this branch was cut off `origin/master`, PR #464 was still open/unmerged - the headers did not exist yet.
The worker added the header + its own row with an explicit note, flagging that the reviewer/merge step
should dedupe to one header per file if PR #464 merged separately (same fix already applied once for
Batch 7/8 fragmentation).

## Lessons / known risks
- Optional dropdowns skipped (none mandatory, confirmed via `ec-ui-knowledge/screens/reservoir_formation.md`
  and the proven `py/reservoir_formation_iud.py`). Delete uses the engine's `wait_for_row_absent` (async
  redraw). Full-tree dryrun 762/762 pass at Batch 9 merge time - confirms no shared T1/T2 regression from
  the grid-filter wiring change.
