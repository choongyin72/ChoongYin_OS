# Well Bore Interval — IUD bundle

**Screen:** Configuration > Assets > Well_and_Reservoir_Objects > Well Bore Interval (BF CO.0057).
OV-GM with a genuine **6 PER-FIELD navigator groups** shape (`nav:form:G:1..G:6:R:1:C:0` — NOT a
same-row/increasing-column cascade): G:1 Production Unit / G:2 Area / G:3 Facility Class 1 / G:4
'Well & Well Hookup' = real well `P1 W008 OP` / G:6 'Well Bore' = `P1 W008 WB001`; G:5 present but
0 usable options under this scope, deliberately skipped. Mandatory **'Well Bore' popup** with list
grid `Objects:form:T_data` (screen-local picker, reuses the navigator's own G:6 value). View
`OV_WELL_BORE_INTERVAL` (167 rows). Date-effective; DELETE = End Date = Start Date.

Converted to the Area-pattern 5-TC/per-TC-login/pure-screen-verify STRUCTURE by PR #563
(2026-08-27), on top of the 2026-07-31 base build — see `JOURNAL.md` for the full history. The
genuine per-field navigator was kept via a BESPOKE screen-local T3 keyword (see below), not the
shared T2 keyword — `resources/manage_object.resource` was NOT touched by the conversion.

- **Playwright driver:** `py/well_bore_interval_iud.py` (shared engine `ec_object_iud.py` +
  screen-local `apply_wbi_navigator`/`pick_well_bore_popup`, live 8/8, 2026-07-31) — unchanged by
  PR #563, which was an RF-only structural conversion. Stays permanently waived from further build
  (Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md` — the Universal Screen Engine replaces that
  role).
- **RF:** T3
  `pageobjects/Configuration/Assets/Well_and_Reservoir_Objects/well_bore_interval_page.resource`
  — BESPOKE `Apply Well Bore Interval Navigator` keyword (loops `Select Nav Group Value` over
  G:1/G:2/G:3/G:4/G:6 read from `testdata/well_bore_interval_navigator.properties`, then one GO),
  screen-local `Pick Well Bore Popup` (list grid `Objects:form:T_data`, FIELD-REUSE RULE against
  the navigator's own G:6 value), explicit `Find/Clear Well Bore Interval Row By Filter` — plus
  suite `tests/Configuration/Assets/Well_and_Reservoir_Objects/well_bore_interval_iud.robot` (5
  TCs, per-TC login/logout, fixed test code `AUTOTEST_WBI`, zero inline DB-verify calls — DB check
  lives in the shared T2 `Verify Object Removed`).
- **Legacy verify record:** `VERIFY-REPORT.md` in this folder is the ORIGINAL 2026-07-31
  `verify_screen.py` auto-generated report (robocop 0 / hygiene 0 / dryrun 4/4 / live RF 4/4 /
  Playwright 8/8) — predates the 5-TC conversion; kept as historical record, not re-generated
  because `verify_screen.py` was written against the older 4-TC shape. Fresh evidence for the
  current 5-TC suite is in `evidence/` (this backfill, 2026-08-28).

## Commands

Dryrun (single suite):
```bash
cd workstreams/master-plan/ec-automation
py -m robot --dryrun tests/Configuration/Assets/Well_and_Reservoir_Objects/well_bore_interval_iud.robot
```

Live headless run (real browser, real DB writes, self-cleaning — TC05 deletes the fixed
`AUTOTEST_WBI` code so the next run starts clean):
```bash
cd workstreams/master-plan/ec-automation
EC_HEADLESS=true py -m robot --outputdir <out-dir> tests/Configuration/Assets/Well_and_Reservoir_Objects/well_bore_interval_iud.robot
```

Live headed run (visible browser, for a watched demo):
```bash
cd workstreams/master-plan/ec-automation
EC_HEADLESS=false py -m robot --outputdir <out-dir> tests/Configuration/Assets/Well_and_Reservoir_Objects/well_bore_interval_iud.robot
```

## DB self-clean check (ground truth — `OV_WELL_BORE_INTERVAL`)
Run from a fresh connection (never reuse a mid-test session), to confirm the fixed test code
(`AUTOTEST_WBI`) is absent and no `AUTOTEST%` residual rows exist:
```sql
SELECT COUNT(*) FROM OV_WELL_BORE_INTERVAL WHERE CODE = 'AUTOTEST_WBI';   -- expect 0
SELECT CODE, NAME FROM OV_WELL_BORE_INTERVAL WHERE UPPER(CODE) LIKE 'AUTOTEST%' OR UPPER(NAME) LIKE 'AUTOTEST%';  -- expect no rows
```
(Write this to a scratch `.py` file under `Workplaces/<task>/` per repo convention — never `py -c`
inline in a committed script.)

Full-tree regression dryrun (confirms zero collisions from Well Bore Interval's fixed test code /
shared keyword usage):
```bash
cd workstreams/master-plan/ec-automation
py -m robot --dryrun tests/
```
