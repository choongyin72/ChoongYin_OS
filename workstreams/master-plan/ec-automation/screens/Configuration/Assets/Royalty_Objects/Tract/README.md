# Tract - EC Object IUD bundle

**Screen:** Configuration > Assets > Royalty Objects > Tract (RC.0056). OV-GM (groupmodel
manage-object, grid `manageObject:form:T_data`), navigator-GATED (single mandatory Unit Agreement
dropdown at `nav:form:G:1:R:1:C:0:dd` - Date at `G:0` already carries a live default and needs no
fill), date-effective (DELETE = End Date = Start Date, true delete in `OV_TRACT`). See
`tract_sow.md` and `JOURNAL.md` for the full story, including the wrong-then-corrected
classification during PR #555's own first commit.

**The maintained/live test is the Robot Framework suite**, converted to the full Area-pattern 5-TC
structure via PR #555 (merged 2026-08-26). Tract never had a Playwright bundle (RF-only since the
original 2026-06-26 build, per the OV-GM exemplar precedent - Transport System) - and per owner
decision 2026-08-27 (`docs/IUD-DELIVERABLE-CHECKLIST.md` Section H), no new Playwright bundle is
built for Area-pattern conversions regardless (the Universal Screen Engine replaces that role).

## Layout
- `tract_sow.md` - statement of work / spec (updated 2026-08-28 with PR #555's conversion story).
- `JOURNAL.md` - work journal (added 2026-08-28 backfill).
- `CHECKLIST.md` - deliverable checklist (added 2026-08-28 backfill).
- `evidence/` - original RF step screenshots from the 2026-06-26 live run
  (`tract_tc0[1-4]_*.png`), plus `backfill_2026-08-28/` (fresh dryrun + live headless output
  captured by this backfill).

## Run - Robot Framework (the proof, the only test this screen has ever had)
```bash
# from workstreams/master-plan/ec-automation/

# 1. dryrun (structure only, no browser/DB)
py -m robot --dryrun --outputdir tmp_dryrun tests/Configuration/Assets/Royalty_Objects/tract_iud.robot

# 2. live headless run (real browser, real DB writes, self-cleaning - TC05 deletes the fixed
#    AUTOTEST_TRACT code so the next run starts clean)
EC_HEADLESS=true py -m robot --outputdir tmp_live tests/Configuration/Assets/Royalty_Objects/tract_iud.robot

# 3. live headed run (visible browser, for a watched demo)
EC_HEADLESS=false py -m robot --outputdir tmp_live tests/Configuration/Assets/Royalty_Objects/tract_iud.robot
```

## DB self-clean check (ground truth - OV_TRACT)
Run BEFORE and AFTER the live suite, from a fresh connection each time (never reuse a mid-test
session), to confirm the fixed test code (`AUTOTEST_TRACT`) is absent and no `AUTOTEST%` residual
rows exist:
```sql
SELECT COUNT(*) FROM OV_TRACT WHERE CODE = 'AUTOTEST_TRACT';   -- expect 0
SELECT CODE FROM OV_TRACT WHERE CODE LIKE 'AUTOTEST%';         -- expect no rows
```
(`libraries/DbVerify.py` uses the generic `CODE` column on every `OV_*` view.)

## Key facts
- Navigator is TWO separate DOM groups (`nav:form:G:0` Date, `nav:form:G:1` Unit Agreement) - but
  ONLY `G:1`'s Unit Agreement dropdown is mandatory-and-empty; `G:0`'s Date already carries a
  non-empty default on load and needs no fill. This was originally (wrongly) read as a
  disqualifying "per-field navigator groups" shape and the conversion was declined - corrected the
  same day (2026-08-26) after fresh live DOM recon. See `JOURNAL.md`.
- Filled via the shared T2 `Apply Navigator From Properties`
  (`resources/manage_object.resource`), called as `group=1 start_col=0` - two new OPTIONAL,
  backward-compatible arguments added specifically for Tract's shape (defaults `group=0
  start_col=1` preserve every other existing caller unchanged).
- Insert Unit Agreement dd in `objectForm` MUST equal the nav value ("Unit Agreement 1") or the
  inserted row never lists in the filtered grid - the owner's field-reuse rule, applied via
  identical values in `testdata/tract_navigator.properties` and `testdata/tract_insert.properties`.
- Field labels are SCREEN-PREFIXED: "Tract Code"/"Tract Name" (like Area's own "Area
  Code"/"Area Name"), NOT the generic "Code"/"Name" Bank/Object List use.
- The RF suite uses the FIXED test code `AUTOTEST_TRACT` (since PR #555 - replaces the original
  build's per-run timestamped `AUTOTEST_TR_<run>` code).
- Delete = End Date set to Start Date
  (`tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input`, hardcoded not label-driven - same
  documented rationale as Area/Bank's own End Date field). Unit Agreement parents confirmed live
  effective `2010-01-01`; Start Date `2011-01-01` reused from the prior driver.

## Equivalent RF files (outside this bundle, treeview-mirrored)
- T3 page object: `pageobjects/Configuration/Assets/Royalty_Objects/tract_page.resource`
- Suite: `tests/Configuration/Assets/Royalty_Objects/tract_iud.robot`
- Test data: `testdata/tract_{navigator,insert,update,form_verify,grid_verify}.properties`
- KB selector map: `ec-ui-knowledge/screens/tract.md`
