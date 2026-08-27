# Property - EC Object IUD bundle

**Screen:** Configuration > Assets > Data_Mapping_Objects > Property (BF SP.0059). OV-GM (grid
`manageObject:form:T_data`), navigator-GATED, date-effective. Converted to the full Area-pattern
structure via PR #559 (2026-08-26): 5 TCs, per-TC login/logout, properties-file-driven insert/
update/verify via the shared T2 `Apply Navigator From Properties` (`group=1 start_col=0`),
explicit grid-filter wiring, zero inline DB-verify calls. See `property_sow.md`, `JOURNAL.md`,
`CHECKLIST.md`, `VERIFY-REPORT.md`. Driver `py/property_iud.py` (untouched by the RF-only
conversion); T3/suite under `Configuration/Assets/Data_Mapping_Objects`.

## Run commands

Dryrun (structural check, no live EC needed):
```
cd workstreams/master-plan/ec-automation
py -m robot --dryrun --outputdir <outdir> tests/Configuration/Assets/Data_Mapping_Objects/property_iud.robot
```

Live headless run against the local sandbox EC instance:
```
cd workstreams/master-plan/ec-automation
EC_HEADLESS=true py -m robot --outputdir <outdir> tests/Configuration/Assets/Data_Mapping_Objects/property_iud.robot
```

DB self-clean check (fixed test code `AUTOTEST_PROPERTY` must be absent from `OV_PROPERTY` once
TC05 Delete has run) - the suite's own TC05 already asserts this in-suite via the shared T2
`Verify Object Removed` (`libraries/DbVerify.py`); to re-check independently outside the suite,
query:
```sql
SELECT COUNT(*) FROM OV_PROPERTY WHERE CODE LIKE 'AUTOTEST%';
-- expect 0
```

## Bundle contents
- `property_sow.md` - classification, navigator shape, dev story
- `JOURNAL.md` - built / done-well / done-wrong / blockers / decisions / evidence
- `evidence/` - screenshots + output.xml/log.html from a real live run
- `CHECKLIST.md` - 21-item deliverable checklist, ticked with evidence
- `VERIFY-REPORT.md` - the 2026-08-02 original build's auto-generated gate report
