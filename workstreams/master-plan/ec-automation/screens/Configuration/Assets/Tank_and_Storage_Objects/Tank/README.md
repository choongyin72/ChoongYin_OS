# Tank — IUD automation bundle

**Screen:** Configuration > Assets > Tank and Storage Objects > Tank
**Type:** OV-GM (manage-object, groupmodel), date-effective — Area-pattern navigator (3-level
Production Unit -> Area -> Facility Class 1 cascade + GO).
**Delete:** End Date = Start Date (zero-length window ⇒ true delete from `OV_TANK`).
**Status:** live **5/5 PASS** (Area-pattern, TC01-TC05), DB-verified, self-cleaning.
See [tank_sow.md](tank_sow.md) and [JOURNAL.md](JOURNAL.md).

**Brand-new build, not a conversion.** Tank never had any prior automation before PR #553
(2026-08-26) — no legacy Playwright driver, no old-style RF suite. It was built from scratch
straight to the current Area-pattern shape via the `ec-area-pattern-new-screen` skill. Per owner
decision 2026-08-27 (`docs/IUD-DELIVERABLE-CHECKLIST.md` Section H), no Playwright bundle is built
for Area-pattern work — the Universal Screen Engine replaces that role — so this bundle has no
`playwright/` folder; that is correctly N/A, not a gap.

**Distinct from Chemical Tank** — a different sibling screen with its own `OV_CHEM_TANK` view,
`chemical_tank_page.resource`, and `chemical_tank_iud.robot`. Do not confuse the two.

## Layout
- `tank_sow.md` — statement of work / spec, including the real PR #553 build story.
- `JOURNAL.md` — work journal (added 2026-08-27 backfill).
- `CHECKLIST.md` — deliverable checklist (added 2026-08-27 backfill).
- `investigation/` — read-only recon: `recon.py` (navigator/mandatory-field/grid-header live scan),
  `dbcheck_selfclean.py` (fresh-connection `OV_TANK` residual check). Original PR #553 build,
  unchanged by this backfill.
- `evidence/backfill_2026-08-27/` — dryrun + live output captured by this backfill (no original
  build `evidence/` folder existed — this was a lean new-screen build).

## Run — Robot Framework (the only automation for this screen)
```bash
# from workstreams/master-plan/ec-automation/

# 1. dryrun (structure only, no browser/DB)
py -m robot --dryrun --outputdir tmp_dryrun tests/Configuration/Assets/Tank_and_Storage_Objects/tank_iud.robot

# 2. live headless run (real browser, real DB writes, self-cleaning — TC05 deletes the fixed
#    AUTOTEST_TANK code so the next run starts clean)
EC_HEADLESS=true py -m robot --outputdir tmp_live tests/Configuration/Assets/Tank_and_Storage_Objects/tank_iud.robot

# 3. live headed run (visible browser, for a watched demo)
EC_HEADLESS=false py -m robot --outputdir tmp_live tests/Configuration/Assets/Tank_and_Storage_Objects/tank_iud.robot
```

## DB self-clean check (ground truth — `OV_TANK`, NOT `OV_CHEM_TANK`)
Run from a fresh connection (never reuse a mid-test session), to confirm the fixed test code
(`AUTOTEST_TANK`) is absent and no `AUTOTEST%` residual rows exist:
```sql
SELECT COUNT(*) FROM OV_TANK WHERE CODE = 'AUTOTEST_TANK';   -- expect 0
SELECT CODE, NAME FROM OV_TANK WHERE UPPER(CODE) LIKE 'AUTOTEST%' OR UPPER(NAME) LIKE 'AUTOTEST%';  -- expect no rows
```
Or run the pre-existing script: `py investigation/dbcheck_selfclean.py` (uses `EC_DB_USER`/
`EC_DB_PASS`/`EC_DB_DSN` env vars, sandbox defaults `ECKERNEL_EC`/`energy`/`localhost:1521/ORCL`).

## Key facts
- Navigator: single row, increasing-column cascade `nav:form:G:0:R:1:C:0..3`. C:0 is a Date field
  with a working default (left untouched — GO succeeds without filling it). C:1/C:2/C:3 are
  Production Unit -> Area -> Facility Class 1 (dropdowns), filled via the shared T2
  `Apply Navigator From Properties`, driven by `testdata/tank_navigator.properties`
  (`P1 Production Unit`/`P1 Area`/`P1 Facility 1`).
- Insert fields are SCREEN-PREFIXED: "Tank Code"/"Tank Name" (like Area's "Area Code"/"Area
  Name"), not the generic "Code"/"Name" Bank/Object List use.
- Op Production Unit/Op Area/Op Facility Class 1 exist on `objectForm` but are NOT mandatory and
  are NOT auto-populated from the navigator scope — must be filled explicitly to match the nav
  scope or the new row is invisible under this OV-GM navigator scope.
- The RF suite uses the FIXED test code `AUTOTEST_TANK` (not a per-run timestamp).
- OV-GM grids redraw lazily after Save+GO — the T3 keywords wait for the row before asserting.

## Equivalent RF files (outside this bundle, treeview-mirrored)
- T3 page object: `pageobjects/Configuration/Assets/Tank_and_Storage_Objects/tank_page.resource`
- Suite: `tests/Configuration/Assets/Tank_and_Storage_Objects/tank_iud.robot`
- Test data: `testdata/tank_{navigator,insert,update,form_verify,grid_verify}.properties`
- KB selector map: `ec-ui-knowledge/screens/tank.md`
