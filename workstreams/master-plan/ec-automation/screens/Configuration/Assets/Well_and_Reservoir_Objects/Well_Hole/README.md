# Well Hole — IUD bundle

**Screen:** Configuration > Assets > Well_and_Reservoir_Objects > Well Hole (BF CO.0051). OV-GM
(grid `manageObject:form:T_data`) with a genuine 3-level SAME-ROW navigator cascade (Op Production
Unit -> Op Area -> Op Facility Class 1), filled with the SPECIFIC "P1 Production Unit/P1 Area/P1
Facility 1" scope (same scope already proven live by the sibling Well screen). View `OV_WELL_HOLE`
(versioned). Date-effective; DELETE = End Date = Start Date.

Converted to the Area-pattern 5-TC/per-TC-login/pure-screen-verify STRUCTURE by PR #543
(2026-08-26) — see `JOURNAL.md` for the full history.

- **Playwright driver:** `py/well_hole_iud.py` (shared engine `ec_object_iud.py` +
  `apply_ovgm_navigator`, live 8/8, 2026-07-31) — unchanged by PR #543, which was an RF-only
  structural conversion. Stays permanently waived from further build (Section H of
  `docs/IUD-DELIVERABLE-CHECKLIST.md` — the Universal Screen Engine replaces that role).
- **RF:** T3
  `pageobjects/Configuration/Assets/Well_and_Reservoir_Objects/well_hole_page.resource` (navigator
  fill delegates to the shared T2 `Apply Navigator From Properties` in
  `resources/manage_object.resource`, driven by `testdata/well_hole_navigator.properties`) + suite
  `tests/Configuration/Assets/Well_and_Reservoir_Objects/well_hole_iud.robot` (5 TCs, per-TC
  login/logout, fixed test code `AUTOTEST_WELL_HOLE`, zero inline DB-verify calls — DB check lives
  in the shared T2 `Verify Object Removed`).
- **Legacy verify record:** `VERIFY-REPORT.md` in this folder is the ORIGINAL 2026-07-31
  `verify_screen.py` auto-generated report (robocop 0 / hygiene 0 / dryrun 4/4 / live RF 4/4 /
  Playwright 8/8) — predates the 5-TC conversion; kept as historical record, not re-generated
  because `verify_screen.py` was written against the older 4-TC shape. Fresh evidence for the
  current 5-TC suite is in `evidence/` (this backfill, 2026-08-28).

## Commands

Dryrun (single suite):
```bash
cd workstreams/master-plan/ec-automation
py -m robot --dryrun tests/Configuration/Assets/Well_and_Reservoir_Objects/well_hole_iud.robot
```

Live headless run (real browser, real DB writes, self-cleaning — TC05 deletes the fixed
`AUTOTEST_WELL_HOLE` code so the next run starts clean):
```bash
cd workstreams/master-plan/ec-automation
EC_HEADLESS=true py -m robot --outputdir <out-dir> tests/Configuration/Assets/Well_and_Reservoir_Objects/well_hole_iud.robot
```

Live headed run (visible browser, for a watched demo):
```bash
cd workstreams/master-plan/ec-automation
EC_HEADLESS=false py -m robot --outputdir <out-dir> tests/Configuration/Assets/Well_and_Reservoir_Objects/well_hole_iud.robot
```

## DB self-clean check (ground truth — `OV_WELL_HOLE`)
Run from a fresh connection (never reuse a mid-test session), to confirm the fixed test code
(`AUTOTEST_WELL_HOLE`) is absent and no `AUTOTEST%` residual rows exist:
```sql
SELECT COUNT(*) FROM OV_WELL_HOLE WHERE CODE = 'AUTOTEST_WELL_HOLE';   -- expect 0
SELECT CODE, NAME FROM OV_WELL_HOLE WHERE UPPER(CODE) LIKE 'AUTOTEST%' OR UPPER(NAME) LIKE 'AUTOTEST%';  -- expect no rows
```
(Write this to a scratch `.py` file under `Workplaces/<task>/` per repo convention — never `py -c`
inline in a committed script.)

Full-tree regression dryrun (confirms zero collisions from Well Hole's fixed test code / shared
keyword usage):
```bash
cd workstreams/master-plan/ec-automation
py -m robot --dryrun tests/
```
