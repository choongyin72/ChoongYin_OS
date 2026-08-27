# Pipeline Segment — IUD automation bundle

**Screen:** Configuration > Assets > Dispatching Objects > Pipeline Segment
**Type:** OV-GM (Business-Unit-gated manage-object), date-effective — Area-pattern sibling.
**Delete:** End Date = Start Date (zero-length window ⇒ true delete from `OV_PIPELINE_SEGMENT`).
**Status:** ✅ live **5/5 PASS** (Area-pattern, TC01-TC05), DB-verified, self-cleaning.
See [pipeline_segment_sow.md](pipeline_segment_sow.md) and [JOURNAL.md](JOURNAL.md).

**The maintained/live test is the Robot Framework suite**, converted to the full Area-pattern
5-TC structure via PR #558 (2026-08-26). No Playwright bundle exists or is built for this screen —
per owner decision 2026-08-27 (`docs/IUD-DELIVERABLE-CHECKLIST.md` Section H), the Universal Screen
Engine replaces that role for Area-pattern conversions going forward.

## Layout
- `pipeline_segment_sow.md` — statement of work / spec, including the PR #558 conversion story
  and the disclosed shared-checkout git-plumbing incident (§3.2).
- `JOURNAL.md` — work journal (added 2026-08-27 backfill).
- `CHECKLIST.md` — deliverable checklist (added 2026-08-27 backfill).
- `evidence/backfill_2026-08-27/` — fresh dryrun + live re-run of the already-proven suite,
  captured by this backfill (includes a disclosed first-attempt flake + passing retry).

## Run — Robot Framework (maintained suite)
```bash
# from workstreams/master-plan/ec-automation/

# 1. dryrun (structure only, no browser/DB)
py -m robot --dryrun --outputdir tmp_dryrun tests/Configuration/Assets/Dispatching_Objects/pipeline_segment_iud.robot

# 2. live headless run (real browser, real DB writes, self-cleaning — TC05 deletes the fixed
#    AUTOTEST_PIPELINE_SEGMENT code so the next run starts clean)
EC_HEADLESS=true py -m robot --outputdir tmp_live tests/Configuration/Assets/Dispatching_Objects/pipeline_segment_iud.robot

# 3. live headed run (visible browser, for a watched demo)
EC_HEADLESS=false py -m robot --outputdir tmp_live tests/Configuration/Assets/Dispatching_Objects/pipeline_segment_iud.robot
```

## DB self-clean check (ground truth — OV_PIPELINE_SEGMENT)
Run BEFORE and AFTER the live suite, from a fresh connection each time (never reuse a mid-test
session), to confirm the fixed test code (`AUTOTEST_PIPELINE_SEGMENT`) is absent and no `AUTOTEST%`
residual rows exist:
```sql
SELECT COUNT(*) FROM OV_PIPELINE_SEGMENT WHERE CODE = 'AUTOTEST_PIPELINE_SEGMENT';   -- expect 0
SELECT CODE FROM OV_PIPELINE_SEGMENT WHERE CODE LIKE 'AUTOTEST%';                    -- expect no rows
```
(`libraries/DbVerify.py` uses the generic `CODE` column on every `OV_*` view.)

## Key facts
- Navigator **Business Unit** dd `nav:form:G:0:R:1:C:1:dd` is mandatory; pick a BU + GO
  (`button:form:B`) before the grid (`manageObject:form:T_data`) loads. The fill goes through the
  shared T2 `Apply Navigator From Properties`, driven by
  `testdata/pipeline_segment_navigator.properties`.
- A second navigator dropdown at `nav:form:G:0:R:1:C:2:dd` ("Pipeline") is an OPTIONAL grid filter,
  NOT mandatory — GO succeeds with only the Business Unit filled.
- Insert **Pipeline Name** dd is mandatory; the test uses `TS5 Gas Pipeline` under the `TS5 BU`
  navigator scope.
- The RF suite uses the FIXED test code `AUTOTEST_PIPELINE_SEGMENT` (not a per-run timestamp).
- The referenced Pipeline/Business Unit values are read-only seed data — existing rows are never
  touched.

## Equivalent RF files (outside this bundle, treeview-mirrored)
- T3 page object: `pageobjects/Configuration/Assets/Dispatching_Objects/pipeline_segment_page.resource`
- Suite: `tests/Configuration/Assets/Dispatching_Objects/pipeline_segment_iud.robot`
- Test data: `testdata/pipeline_segment_{navigator,insert,update,form_verify,grid_verify}.properties`
- KB selector map: `ec-ui-knowledge/screens/pipeline_segment.md`
