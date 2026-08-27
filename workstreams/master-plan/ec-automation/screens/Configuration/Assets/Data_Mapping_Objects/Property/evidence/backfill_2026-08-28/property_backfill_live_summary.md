# Property - lean-deliverable backfill evidence (2026-08-28, Batch 5)

Evidence capture of the already-proven Area-pattern suite (PR #559, merged 2026-08-26) per
`docs/lean-deliverable-backfill-workorder.md` - this run does NOT modify the suite, T3, or any
shared resource file.

## Dryrun

```
cd workstreams/master-plan/ec-automation
py -m robot --dryrun --outputdir <outdir> tests/Configuration/Assets/Data_Mapping_Objects/property_iud.robot
```
Result: **5 tests, 5 passed, 0 failed.**

## Live headless run

```
cd workstreams/master-plan/ec-automation
EC_HEADLESS=true py -m robot --outputdir <outdir> tests/Configuration/Assets/Data_Mapping_Objects/property_iud.robot
```
Result: **5 tests, 5 passed, 0 failed** - first attempt, no retry needed.

| TC | Result |
|---|---|
| TC01 Verify Clean State | PASS |
| TC02 Insert Property Data | PASS |
| TC03 Update Property Data | PASS |
| TC04 Find Property Data | PASS |
| TC05 Delete Property Data | PASS |

## Grid-filter keyword fired

`grep -c "Find Object Row By Filter" output.xml` = **15** (matches PR #559's own cited count of 15).

## DB self-clean

TC05's own in-suite assertion (`Verify Property Record Removed` -> shared T2 `Verify Object
Removed` against `OV_PROPERTY`) passed, confirming the fixed test code `AUTOTEST_PROPERTY` is
absent from `OV_PROPERTY` after this run - no separate out-of-suite DB connection was opened for
this backfill; the suite's own DB-verify step already re-proves self-clean each run since PR #559
removed inline/ad-hoc DB checks in favour of the shared T2 keyword.

## Artifacts in this folder
- `log.html`, `report.html`, `output.xml` - full Robot Framework run output.
- Per-step screenshots (`TC0N <name>_<step>.png`) - captured automatically by the suite's own
  `Capture Step` calls (login/open_screen/action/verify/logout per TC).

## Process-rule note
No live-run timeout or browser error was hit this session - both the dryrun and the live run
passed cleanly on the first attempt, so the "retry once, then disclose" rule was not invoked.
