# SOW - Facility Class 1 IUD (Configuration > Assets > Facility_Objects)

- **Screen:** Facility Class 1   **BF:** CO.0019   **View:** `OV_FCTY_CLASS_1` (versioned)   **Base:** `FCTY_CLASS_1`
- **Type:** OV-GM (manage-object, groupmodel; grid `manageObject:form:T_data`), navigator-GATED, date-effective.
  Converted to the Area-pattern 5-TC/per-TC-login/pure-screen-verify STRUCTURE (owner standing rule
  2026-08-26: any EC screen with a navigator matching Area's layout MUST follow Area's FULL pattern) -
  Facility Class 1 remains OV-GM and keeps its genuine navigator cascade; the conversion is
  STRUCTURAL, not a reclassification as plain Bank-shaped.
- **Navigator:** Production Unit -> Area, a genuine **2-level same-row cascade**
  (`nav:form:G:0:R:1:C:1:dd` for PU, `nav:form:G:0:R:1:C:2:dd` for Area, C:3 absent) + GO. Values are
  EXPLICIT (not first-available) since PR #526: `Op Production Unit=AS1 EC Exploration Norway`,
  `Op Area=AS1_Area`, sourced from `testdata/facility_class_1_navigator.properties` and applied via the
  shared T2 keyword `Apply Navigator From Properties` (`resources/manage_object.resource`, unmodified).
  This was the FIRST screen to exercise that shared keyword's multi-column same-row cascade shape -
  Area itself only has a single navigator dropdown, so it never exercised C:1/C:2-in-one-row addressing.
- **Grid columns** (confirmed live 2026-08-26, `manageObject:form:T_head` scan): Facility Class 1 Code /
  Facility Class 1 Name / Start Date / End Date - same 4-column shape as Area.
- **Form labels:** screen-prefixed **"Facility Class 1 Code"** / **"Facility Class 1 Name"** (objectForm /
  updateAttributes), like Area's "Area Code"/"Area Name" - NOT the generic "Code"/"Name" Bank/Object List use.
  Mandatory: Facility Class 1 Code, Facility Class 1 Name, Start Date.
  objectForm DOES expose "Op Production Unit"/"Op Area" fields (confirmed live 2026-08-26, broader than the
  original 2026-07-30 build's "no Op PU field" note) but the proven driver inserts successfully leaving
  them blank - left unfilled per the repo's standing rule against hunting unstated requirements.
- **IUD:** INSERT -> UPDATE (Facility Class 1 Name) -> FIND -> DELETE (End Date = Start Date, true delete
  in `OV_FCTY_CLASS_1`). Test data: **fixed code `AUTOTEST_FC1`** (confirmed free in `OV_FCTY_CLASS_1` via a
  fresh oracledb connection before use), replacing the original build's generated
  `AUTOTEST_FC1_<timestamp>` code. Self-clean = 0 residual `AUTOTEST_FC1%` rows after TC05.
- **Dev story:** built 2026-07-30 as one of the early OV-GM screens (PR #262, stacked on the
  gated-navigator capability PR #244) via the generic `ec_object_iud.py` engine + label-driven T3,
  first-available navigator values, 4-TC RF suite, `verify_screen.py` OVERALL PASS. Converted
  2026-08-26 in two stacked PRs under the owner's Area-pattern standing rule: **PR #526** moved the
  navigator-fill from "first available" to the shared, properties-file-driven `Apply Navigator From
  Properties` keyword (dedicated live recon in `tmp/recon_fc1_navigator_cascade.py` confirmed the
  C:1/C:2-present, C:3-absent shape before any config was written - no shared-file changes needed,
  the existing flat 0.7s sleep in the shared keyword was already sufficient); **PR #530** then did the
  full 5-TC/per-TC-login/fixed-code/properties-driven/pure-screen-verify structural conversion on top,
  re-confirming field labels and grid columns live rather than assuming them from Area.
- **Deliverables:** T3 `pageobjects/Configuration/Assets/Facility_Objects/facility_class_1_page.resource`,
  suite `tests/Configuration/Assets/Facility_Objects/facility_class_1_iud.robot`, 5 properties files
  (`testdata/facility_class_1_{navigator,insert,update,form_verify,grid_verify}.properties`), this SOW,
  `README.md`, `JOURNAL.md`, `CHECKLIST.md`, `evidence/`, KB map `ec-ui-knowledge/screens/facility_class_1.md`.
  The pre-existing `py/facility_class_1_iud.py` Playwright driver + `investigation/recon.py` are RETAINED
  (built 2026-07-30, still passing) but not rebuilt or extended by this backfill - per owner decision
  2026-08-27 (`docs/IUD-DELIVERABLE-CHECKLIST.md` Section H), no NEW Playwright bundle is built for
  Bank-/Area-pattern conversions; the Universal Screen Engine is the forward replacement for that role.
