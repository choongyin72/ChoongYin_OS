# Screen: Well Hole

- **Type:** OV-GM (EC Object Configuration, groupmodel manage-object, date-effective).
  Navigator-GATED - the grid loads ONLY after a genuine 3-level SAME-ROW navigator cascade + GO.
  Converted to Area's full RF pattern by PR #543 (2026-08-26).
- **BF_CODE:** CO.0051 - **Treeview:** Configuration > Assets > Well_and_Reservoir_Objects > Well Hole
- **DB view:** `OV_WELL_HOLE` (versioned; key `CODE`; also `NAME`, `OBJECT_START_DATE`,
  `OBJECT_END_DATE` - no Description column)
- **Last verified:** 2026-08-28 - EC 14.2.4 - local sandbox (`localhost:1521/ORCL`) - live RF 5/5,
  first attempt, no retry needed (this backfill session)

## Selectors `[from well_hole_page.resource Variables section, transcribed 2026-08-28]`

| Purpose | Selector |
|---|---|
| Grid (rows) | `manageObject:form:T_data` |
| Navigator cascade (3-level, SAME-ROW, MANDATORY) | `nav:form:G:0:R:1:C:1:dd` (Op Production Unit) -> `C:2` (Op Area) -> `C:3` (Op Facility Class 1) |
| Navigator value used | SPECIFIC "P1 Production Unit / P1 Area / P1 Facility 1" - the SAME scope already proven live by the sibling Well screen, NOT first-available (proven live 2026-08-26: lists 20 real `OV_WELL_HOLE` rows) |
| Navigator fill mechanism | Shared T2 `Apply Navigator From Properties` (`resources/manage_object.resource`), driven by `testdata/well_hole_navigator.properties` |
| Grid-filter | `Find/Clear Well Hole Row By Filter` -> shared T2 `Find/Clear Object Row By Filter` on the grid's Code column |
| Insert/Update/Verify | Delegates to shared T2 `Insert/Update/Verify Object *` keywords, all called with `code_label=Well Hole Code` |
| Delete End Date field | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (hardcoded, not label-driven - End Date label sits at `C:2`, Start Date at `C:1`, same row-packing rationale as Area's `${AREA_DEL_ENDDATE}`) |

## Mandatory / yellow fields
- **Navigator (before the grid loads any rows):** Op Production Unit -> Op Area -> Op Facility
  Class 1 cascade + GO - genuine OV-GM requirement.
- **Insert form:** Well Hole Code, Well Hole Name, Start Date (mandatory); Op Production Unit must
  equal the navigator's own PU value (`P1 Production Unit`) or the inserted row is invisible under
  the filtered grid scope.
- **Update form:** Well Hole Name only - Well Hole Code is read-only in `updateAttributes`;
  `OV_WELL_HOLE` has no Description column.
- Field labels are **screen-prefixed**: "Well Hole Code" / "Well Hole Name" (like Area's "Area
  Code"/"Area Name"), NOT the generic "Code"/"Name" that Bank/Object List use - confirmed live via
  the page object's own documented recon.

## Quirks
- **OV-GM grid stays empty until the navigator is filled + GO'd** - Well Hole's defining
  characteristic, same as Area/Well/Tank.
- **Navigator scope reused from a sibling, not re-derived:** the base build (2026-07-31) used a
  first-available cascade value, which is a documented sparse/unreliable OV-GM pattern (see
  `docs/lessons-learned.md`-style caveat: "first-available nav scope ... is NOT necessarily a valid
  Op Production Unit option"). PR #543's conversion (2026-08-26) replaced it with the SPECIFIC "P1"
  scope already proven by the sibling Well screen - but only after confirming live that this exact
  scope also lists real `OV_WELL_HOLE` rows, not by assuming it would transfer.
- **Fixed test code `AUTOTEST_WELL_HOLE`** (not a generated/unique code) - every run must complete
  TC05 so the code is free for the next run.
- **Versioned grid redraws lazily after Delete** - Save And Refresh List (inside the shared T2)
  already re-applies the navigator so the assertion reads a fresh list; same characteristic
  documented on Area/Well.

## Automation (code lives in ec-automation - this file is the MD selector reference)
- **RF (the maintained suite):** T3
  `ec-automation/pageobjects/Configuration/Assets/Well_and_Reservoir_Objects/well_hole_page.resource`
  (T2 `resources/manage_object.resource` + `libraries/PropertiesReader.py`) + suite
  `ec-automation/tests/Configuration/Assets/Well_and_Reservoir_Objects/well_hole_iud.robot` (5 TCs:
  Clean State/Insert/Update/Find/Delete, per-TC Login/Logout). Run:
  `EC_HEADLESS=true robot tests/Configuration/Assets/Well_and_Reservoir_Objects/well_hole_iud.robot`
  -> 5/5 PASS, self-clean 0 residual in `OV_WELL_HOLE`.
- **Playwright (pre-existing reference, waived from further build per Section H of
  `docs/IUD-DELIVERABLE-CHECKLIST.md` - Universal Screen Engine replaces this role going forward):**
  `ec-automation/py/well_hole_iud.py` (shared engine `ec_object_iud.py` + `apply_ovgm_navigator`),
  live 8/8 as of 2026-07-31, kept unchanged by PR #543.
- Full bundle (SOW/README/JOURNAL/evidence/CHECKLIST):
  `ec-automation/screens/Configuration/Assets/Well_and_Reservoir_Objects/Well_Hole/`.

## Disambiguation
- Distinct from sibling screens in the same treeview group: Well (`OV_WELL`, CO.0049), Well Bore,
  Well Bore Interval, Well Hookup - each has its own view/page-object/suite. Do not confuse.
