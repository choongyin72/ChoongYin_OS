# Transport Zone — IUD automation bundle

**Screen:** Configuration > Assets > Dispatching Objects > Transport Zone
**Type:** OV-GM (Business-Unit-gated manage-object), date-effective — Area-pattern sibling.
**Delete:** End Date = Start Date (zero-length window ⇒ true delete from `OV_TRANSPORT_ZONE`).
**Status:** live **5/5 PASS** (Area-pattern, TC01-TC05), DB-verified, self-cleaning.
See [transport_zone_sow.md](transport_zone_sow.md) and [JOURNAL.md](JOURNAL.md).

**The maintained/live test is the Robot Framework suite**, converted to the full Area-pattern
5-TC structure via PR #557 (2026-08-26). No Playwright bundle exists or is built for this screen —
per owner decision 2026-08-27 (`docs/IUD-DELIVERABLE-CHECKLIST.md` Section H), the Universal Screen
Engine replaces that role for Area-pattern conversions going forward.

## Layout
- `transport_zone_sow.md` — statement of work / spec, including the PR #557 conversion story.
- `JOURNAL.md` — work journal (added 2026-08-28 backfill).
- `CHECKLIST.md` — deliverable checklist (added 2026-08-28 backfill).
- `evidence/backfill_2026-08-28/` — fresh dryrun + live re-run of the already-proven suite
  (includes a disclosed first-attempt timeout + passing retry).

## Run — Robot Framework (maintained suite)
```bash
# from workstreams/master-plan/ec-automation/

# 1. dryrun (structure only, no browser/DB)
py -m robot --dryrun --outputdir tmp_dryrun tests/Configuration/Assets/Dispatching_Objects/transport_zone_iud.robot

# 2. live headless run (real browser, real DB writes, self-cleaning — TC05 deletes the fixed
#    AUTOTEST_TRANSPORT_ZONE code so the next run starts clean)
EC_HEADLESS=true py -m robot --outputdir tmp_live tests/Configuration/Assets/Dispatching_Objects/transport_zone_iud.robot

# 3. live headed run (visible browser, for a watched demo)
EC_HEADLESS=false py -m robot --outputdir tmp_live tests/Configuration/Assets/Dispatching_Objects/transport_zone_iud.robot
```

## DB self-clean check (ground truth — OV_TRANSPORT_ZONE)
Run BEFORE and AFTER the live suite, from a fresh connection each time (never reuse a mid-test
session), to confirm the fixed test code (`AUTOTEST_TRANSPORT_ZONE`) is absent and no `AUTOTEST%`
residual rows exist:
```sql
SELECT COUNT(*) FROM OV_TRANSPORT_ZONE WHERE CODE = 'AUTOTEST_TRANSPORT_ZONE';   -- expect 0
SELECT CODE FROM OV_TRANSPORT_ZONE WHERE CODE LIKE 'AUTOTEST%';                  -- expect no rows
```
(`libraries/DbVerify.py` uses the generic `CODE` column on every `OV_*` view.)

## Key facts
- Navigator group `nav:form:G:0` has THREE columns: C:0 Date (mandatory:true but ALREADY
  defaulted/filled on load — no fill needed), **C:1 Business Unit dropdown (mandatory:true,
  genuinely empty — the ONLY field needing a fill)**, C:2 a second dropdown (mandatory:false,
  optional filter — GO succeeds with C:2 left empty once C:1 is set). The fill goes through the
  shared T2 `Apply Navigator From Properties`, driven by
  `testdata/transport_zone_navigator.properties` (Business Unit = `TS5 BU`).
- Insert **Transport System Name** dd is mandatory; the test uses `TS5 Transport System`, bound to
  the `TS5 BU` navigator scope (must pair or the inserted row is invisible under this OV-GM scope).
- Insert Zone Type / End Date are confirmed `mandatory:false` — deliberately excluded from insert data.
- The RF suite uses the FIXED test code `AUTOTEST_TRANSPORT_ZONE` (not a per-run timestamp).
- The referenced Transport System/Business Unit values are read-only seed data — existing rows are
  never touched.

## Equivalent RF files (outside this bundle, treeview-mirrored)
- T3 page object: `pageobjects/Configuration/Assets/Dispatching_Objects/transport_zone_page.resource`
- Suite: `tests/Configuration/Assets/Dispatching_Objects/transport_zone_iud.robot`
- Test data: `testdata/transport_zone_{navigator,insert,update,form_verify,grid_verify}.properties`
- KB selector map: `ec-ui-knowledge/screens/transport_zone.md`
