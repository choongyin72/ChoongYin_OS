# SOW - Operator Route IUD (Configuration > Assets > Facility_Objects)

_Backfilled 2026-08-27 per `docs/lean-deliverable-backfill-workorder.md` (owner decision 2026-08-27,
`docs/IUD-DELIVERABLE-CHECKLIST.md` Section H) - the base build below predates the Area-pattern
conversion in PR #533; this SOW is updated to describe the CURRENT, merged shape of the automation,
not the 2026-08-01 base build alone._

## Classification
- **Screen:** Operator Route   **BF:** CO.0244   **View:** `OV_OPERATOR_ROUTE`   **Base:** `OPERATOR_ROUTE`
- **Treeview:** Configuration > Assets > Facility_Objects > Operator Route
- **Type:** OV-GM (manage-object, groupmodel; grid `manageObject:form:T_data`), navigator-GATED,
  date-effective. Pattern: **Area-pattern** (structural conversion, 2026-08-26, PR #533) - the
  owner's standing rule that any EC screen with a navigator matching Area's layout follows Area's
  FULL pattern (5-TC/per-TC-login/pure-screen-verify/properties-driven/explicit-filter-wiring).

## Navigator / grid / cell shape
- **Navigator:** genuine mandatory 2-level **Production Unit -> Area** SAME-ROW cascade
  (`nav:form:G:0:R:1:C:1:dd` then `nav:form:G:0:R:1:C:2:dd`) + GO - the grid stays empty until this
  is filled. Fill is delegated to the shared T2 `Apply Navigator From Properties`
  (`resources/manage_object.resource`), driven by `testdata/operator_route_navigator.properties`
  with the PROVEN explicit values `Op Production Unit=P3 Production Unit` / `Op Area=P3 Area`
  (carried over unchanged from this screen's own pre-conversion driver - not first-available, per
  this screen's own registry note that the first-available option is not guaranteed to have data
  underneath it).
- **Grid id:** `manageObject:form:T_data` - filtered explicitly on the Code column via the shared
  T2 `Find/Clear Object Row Filter` (screen wrapper: `Find/Clear Operator Route Row By Filter`),
  wired into Update/Find/Verify-Found/Delete (15 `Find Object Row By Filter` hits confirmed in a
  live run's `output.xml`, 2026-08-27).
- **Delete field:** `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (End Date). EC delete =
  End Date set equal to Start Date (zero-length window) -> object fully removed from
  `OV_OPERATOR_ROUTE` (true delete, DB-verified both before and after PR #533's conversion).

## Mandatory fields
- Insert (`objectForm`, screen-prefixed labels like Area's "Area Code"/"Area Name"):
  **Operator Route Code**, **Operator Route Name**, **Start Date**.
- Update (`updateAttributes`): **Operator Route Name** only - Operator Route Code is read-only
  after creation.

## Test data used
| Field | Value |
|---|---|
| Operator Route Code | `AUTOTEST_OR` (FIXED code post-conversion - confirmed absent from `OV_OPERATOR_ROUTE` via a fresh oracledb connection both before and after every run; the pre-conversion build used a generated `AUTOTEST_OR_<timestamp>` code instead) |
| Operator Route Name (Insert) | `Automation Test Operator Route` |
| Operator Route Name (Update) | `Automation Test Operator Route UPDATED` |
| Start Date | `2000-01-01` |
| End Date (Delete) | `2000-01-01` (= Start Date -> true delete) |
| Navigator | Op Production Unit=`P3 Production Unit`, Op Area=`P3 Area` |

## Dev story (real, from PR #533 - "convert Operator Route to full Area pattern", merged
2026-08-26T08:06:00Z)
Operator Route's base IUD (4 TCs, single suite-level login, bespoke inline navigator-fill via
`Select EC Dropdown Option` + `Apply Navigator`, a generated `AUTOTEST_OR_<timestamp>` code, and
screen-local `Operator Route Should/Should Not Exist In DB` inline DB-verify wrappers) had already
passed `verify_screen.py` on 2026-08-01 (RF 4/4, Playwright 8/8, DB-verified, self-clean). On
2026-08-26, under the owner's standing rule that any navigator screen matching Area's layout takes
Area's full pattern (not just the navigator-fill piece), the RF layer was rebuilt to 5 TCs (added
TC04 Find) with per-TC Login/Logout, a fixed test code `AUTOTEST_OR`, navigator fill delegated to
the shared T2 `Apply Navigator From Properties`, properties-file-driven insert/update via T2's
`Insert/Update Object From Properties`, explicit grid-filter wiring, and PURE SCREEN verification
only (zero inline DB-verify calls left in the `.robot` file - the DB check for delete now lives
solely inside the shared T2 `Verify Object Removed`). The genuine mandatory 2-level PU->Area
cascade + GO was kept exactly as proven - this was a structural RF conversion, not a
reclassification of the screen's navigator shape. No shared T1/T2 file changes were needed; the
existing `Apply Navigator From Properties` keyword's flat sleep already handled this screen's
2-level same-row cascade (same shape already proven on Facility Class 1). The Playwright driver
(`py/operator_route_iud.py`) was left untouched. Live run: 5/5 pass; full-tree dryrun 850/850 (0
collisions, per PR #533); robocop parity vs Area's own reference-pattern files (5x DOC02 + 2x
VAR02 per screen).

## Deliverables (current)
- Driver `py/operator_route_iud.py` (waived from further change by Section H of the deliverable
  checklist - the Playwright bundle stays as the pre-conversion 2026-08-01 build; the Universal
  Screen Engine is the owner-decided replacement for hand-written Playwright drivers going
  forward).
- T3 `pageobjects/Configuration/Assets/Facility_Objects/operator_route_page.resource`
  (properties-driven, post-conversion).
- Suite `tests/Configuration/Assets/Facility_Objects/operator_route_iud.robot` (5 TCs,
  post-conversion).
- `testdata/operator_route_{navigator,insert,update,form_verify,grid_verify}.properties`.
- This SOW, `README.md`, `JOURNAL.md`, `evidence/`, `CHECKLIST.md` (this backfill, 2026-08-27) +
  `ec-ui-knowledge/screens/operator_route.md` (KB map, refreshed 2026-08-27).
- `VERIFY-REPORT.md` (auto-generated 2026-08-01, base-build gates only; RF gate counts there are
  now stale vs the 5-TC suite - see `CHECKLIST.md` for the current, re-run gate evidence).
