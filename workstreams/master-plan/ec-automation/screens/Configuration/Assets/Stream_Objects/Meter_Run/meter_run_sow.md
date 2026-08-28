# SOW - Meter Run IUD

## Classification
- **Screen:** Configuration > Assets > Stream_Objects > Meter Run (BF_CODE **CO.0091**)
- **Type/pattern:** OV (Manage-Object, `manage_object_nav`) - plain Bank-pattern, date-effective, NO
  navigator cascade (single Date + GO). **Rebuilt 2026-08-23 (Batch 8, PR #462) to the full
  Bank-pattern shape** (properties-file-driven insert/update/verify + explicit grid-filter wiring),
  mirroring `bank_page.resource`/`berth_page.resource` exactly.
- **DB view:** `OV_METER_RUN` (versioned); key `CODE`
- **Grid id:** `manage_object_nav_nav:form:T_data` (reused from T2's `${OV_MANAGE_OBJECT_TABLE}`
  constant, not re-hardcoded)
- **Delete:** End Date = Start Date -> row leaves `OV_METER_RUN`

## Mandatory fields (confirmed live - Save rejected without them)
- `Meter Run Code`, `Meter Run Name`, `Start Date` (Insert-only)
- PLUS three dropdowns: `Type of Taps`, `Pipe Material`, `Location of Taps`
- PLUS three numeric fields: `Pipe Diameter (temp uncorrected) [mm]`, `Diameter Meas Temp [deg R]`,
  `All Calibration Factor`
- This is a larger mandatory set than Bank/Berth's plain 3-field (Code/Name/Start Date) baseline -
  taken as-is from the already-proven driver/page object, not extrapolated from the simpler
  siblings (per PR #462's "Rules applied").

## Test data
- Fixed code `AUTOTEST_METER_RUN` (matches Bank/Berth convention, not a generated/timestamped code) -
  confirmed absent from `OV_METER_RUN` before each run; every run must complete TC05 (delete) so the
  code stays free for the next run.
- Start/End Date = `2000-01-01`. Never touch real rows.

## Dev story
Two builds, same screen:
1. **2026-07-26 (original build):** Recon-first (DB `CLASS_TYPE=OBJECT` => OV; live form) found the
   mandatory extras beyond Code/Name/Start Date. Built label-driven on the shared `ec_object_iud.py`
   engine + T2, zero engine changes. Playwright driver 7/7 (`py/meter_run_iud.py`); RF T3+suite
   label-driven-only (no properties files, no explicit grid-filter) -> live 4/4.
2. **2026-08-23 (PR #462, Batch 8 of the Bank-pattern conversion project):** rebuilt the RF T3
   (`meter_run_page.resource`) and suite (`meter_run_iud.robot`) from the label-driven-only shape to
   the full Bank-pattern shape - 4 new `testdata/meter_run_*.properties` files, explicit
   `Find/Clear Meter Run Row By Filter` wiring (15 filter-keyword hits confirmed via output.xml
   grep), per-TC Login/Logout, 5-TC structure (Verify Clean State/Insert/Update/Find/Delete), and
   Meter Run's own dedicated credential pair (`METER_RUN_EC_USER`/`METER_RUN_EC_PASS`). No shared
   T1/T2 (`manage_object.resource`/`common.resource`) changes. Playwright driver untouched
   (out of scope for the conversion; the Universal Screen Engine is the owner-decided replacement
   for hand-written Playwright drivers going forward, per Section H of
   `docs/IUD-DELIVERABLE-CHECKLIST.md`).

## Lessons / known risks
- Mandatory field set is screen-specific (6 extra fields beyond Code/Name/Start Date) - do not copy
  Bank/Berth's simpler 3-field assumption onto this screen.
- Delete End Date field id (`tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input`) confirmed live via
  a read-only recon on an existing production row (never saved) - same convention as Bank/Berth's
  `*_DEL_ENDDATE` constant, not assumed from a sibling.
