# Chemical Injection Point - EC Object IUD bundle

**Screen:** Configuration > Assets > Chemical Objects > Chemical Injection Point (BF CO.0212)
**Type:** OV-GM (grid `manageObject:form:T_data`) - navigator-GATED (genuine 3-level Production
Unit -> Area -> Facility Class 1 cascade), date-effective.

Converted to Area's full pattern in **PR #550** (merged 2026-08-26): 5-TC structure, per-TC
login/logout, fixed test code `AUTOTEST_CIP`, properties-file-driven insert/update/verify, and the
shared T2 `Apply Navigator From Properties` keyword. See `chem_injection_point_sow.md` Section 6
for the real dev story, including the Op Production Unit / `__FIRST__` gotcha.

## RF suite - current shape (post PR #550) - this is the maintained deliverable

### Run - from `workstreams/master-plan/ec-automation/`

```bash
# structure-only dryrun (no browser/DB)
robot --dryrun tests/Configuration/Assets/Chemical_Objects/chem_injection_point_iud.robot

# live run, headless (default CI mode)
EC_HEADLESS=true robot tests/Configuration/Assets/Chemical_Objects/chem_injection_point_iud.robot

# live run, headed (visible browser, for a demo/spot-check)
EC_HEADLESS=false robot tests/Configuration/Assets/Chemical_Objects/chem_injection_point_iud.robot
```

### DB self-clean check pattern

```sql
SELECT COUNT(*) FROM OV_CHEM_INJ_POINT WHERE CODE = 'AUTOTEST_CIP';
-- expected: 0 both BEFORE and AFTER a full TC01-TC05 run (the suite's own TC05 leaves no residue)
```
Or via the shared library from a Python shell: `libraries/DbVerify.py`'s
`fetch_object("OV_CHEM_INJ_POINT", "AUTOTEST_CIP")` - `None` = confirmed absent.

## Folder
- `chem_injection_point_sow.md` - SOW: classification, nav/grid/cell shape, test data, dev story
  (original 2026-07-30 build + PR #550's 2026-08-26 Area-pattern conversion, incl. the
  `__FIRST__` gotcha).
- `README.md` - this file.
- `JOURNAL.md` - per-branch work journal (built/done-well/lessons/decisions/evidence), pulled from
  PR #550's real body.
- `evidence/` - `cip_0[1-5]_*.png` + `results.json` from the original 2026-07-30 Playwright run,
  plus `log.html`/`output.xml`/`report.html` from a live RF run captured 2026-08-27 (this backfill).
- `CHECKLIST.md` - the IUD deliverable checklist, ticked with real evidence citations.
- `investigation/recon.py` - pre-existing recon script (waived going forward per Section H of
  `docs/IUD-DELIVERABLE-CHECKLIST.md`; kept unchanged, not rebuilt).
- `VERIFY-REPORT.md` - the original 2026-07-30 `verify_screen.py` auto-generated report, describing
  the PRE-conversion 4-TC suite; retained as historical record (superseded by PR #550's own live
  5/5 evidence cited in the PR body and in this backfill's `CHECKLIST.md`/`JOURNAL.md`).

KB selector map: `ec-ui-knowledge/screens/chem_injection_point.md`.
