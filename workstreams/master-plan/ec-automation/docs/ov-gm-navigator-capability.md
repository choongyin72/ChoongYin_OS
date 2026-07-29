# OV-GM gated-navigator capability (item 1)

_Built 2026-07-29. The reusable primitive that unlocks the ~41 OV-GM object screens (grid
`manageObject:form:T_data`), which are navigator-GATED: the grid is empty until a navigator cascade is set + GO._

## The pattern (proven live on Node CD.0006)
1. **Navigator cascade** = autocomplete dropdowns in ONE row across columns: `nav:form:G:0:R:1:C:1..N:dd`
   (e.g. Group B = C1 Production Unit -> C2 Area -> C3 Facility Class 1). Fill **first-available parent->child**
   (child options render only after the parent is chosen), then **GO** (`button:form:B`). The `manageObject`
   grid loads only after this.
2. **Capture the top-parent** (C1 value, e.g. `AS1 EC Exploration Norway`).
3. **Insert:** New-Object form Code/Name/Start + mandatory extras, and set the **parent-dd**
   (e.g. `Op Production Unit` / `Business Unit Name`). Set it to the captured C1 value **if that value is
   an option** in the parent-dd panel; otherwise **first-available** (`__FIRST__`). PER-SCREEN, VERIFY:
   the parent-dd panel is date-filtered and its list can DIFFER from the navigator's (real case: on **Node**
   the Op PU panel offers 5 PUs and the nav first-available `AS1...` is NOT one of them - yet the row still
   lists after GO with first-available Op PU; contrast **Area**, where nav PU == Op PU was required). Never
   assume the nav value is a valid parent-dd option - probe the panel (`tmp/node/probe_op_pu.py`).
4. **Groupmodel check (per screen):** after Save + GO, does the row LIST in the grid? YES -> groupmodel enabled,
   buildable. NO -> groupmodel OFF (insert persists but grid never lists, e.g. Production Sub Unit) -> EXCLUDE.
5. **Lazy redraw:** the GM grid redraws async after Save+GO -> poll (`wait_for_row`) / extra Apply Navigator
   before asserting.
6. **Popups** (many OV-GM screens have `pin/pinB` popup refs) now render/populate under the applied scope ->
   handled by the merged popup capability (`pick_popup` / `Pick OV Popup By Label`).

## Capability (both stacks)
- **Playwright:** `apply_ovgm_navigator(page, levels=4, row=1)` (py/ec_object_iud.py) - fills the cascade
  first-available, GO, returns the C1 top-parent value.
- **Robot Framework:** `Apply OV-GM Navigator First Available` (manage_object.resource) - twin; returns the top-parent.

## Live proof (Node CD.0006, Group B, local sandbox)
Cascade filled PU `AS1 EC Exploration Norway` -> Area `AS1_Area` -> Facility `AS1_Facility_01` -> GO -> grid
20 rows. Insert (Code/Name/Start + Calculation Sequence Number + `Op Production Unit` = nav PU) -> Save (no
error) -> GO -> **row LISTED** (groupmodel enabled). Self-cleaned (End=Start, DB-verified 0). R12: backups in
.keyword_backups/; engine compiles + ASCII-clean; Bank sibling dryrun 4/4 (no regression).

## Batch plan (next - per-screen, attended/careful, skip-and-park)
Per screen: recon the parent-dd label + mandatory set (scan_mandatory) -> generate/build with OV-GM config
(nav cascade in Open, parent-dd = nav top, grid manageObject) -> per-screen groupmodel check -> verify_screen
OVERALL PASS -> PR off master. Groups: B(20) C1/C2(10) D(3) F(1) A-OVGM(7) + Stream Item + well-hierarchy(4).
Nav shape per screen in `tmp/ov_gm_55_nav_config.json`. Exclude groupmodel-off screens (verified) like Production Sub Unit.
