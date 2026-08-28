# Operator Lease — IUD automation bundle

**Screen:** Configuration > Assets > Commercial Objects > Operator Lease.
**Type:** OV (manage-object, plain — no navigator; grid `manage_object_nav_nav:form:T_data`),
date-effective. **Delete:** End Date = Start Date (true delete, object removed from
`OV_OPERATOR_LEASE`). **Status:** live **5/5 PASS** (Bank pattern, TC01-TC05), DB-verified,
self-cleaning. See [operator_lease_sow.md](operator_lease_sow.md) and [JOURNAL.md](JOURNAL.md).

**The maintained/live test is the Robot Framework suite**, converted to the full Bank-pattern
5-TC structure via PR #436 (2026-08-23). The Playwright driver below is the original 2026-06-12
reference implementation, preserved unchanged — per owner decision 2026-08-27
(`docs/IUD-DELIVERABLE-CHECKLIST.md` Section H), no new/updated Playwright bundle is built for
Bank-pattern conversions (the Universal Screen Engine replaces that role going forward). This
README, `JOURNAL.md`, `evidence/backfill_2026-08-28/`, and `CHECKLIST.md` were added/refreshed by
the 2026-08-28 deliverable backfill (`docs/lean-deliverable-backfill-workorder.md`, Batch 6) — the
RF automation itself was NOT modified by that backfill.

## Layout
- `playwright/ec_iud_operator_lease.py` — original 2026-06-12 Playwright driver, thin config over
  the shared engine — NOT modified by PR #436 or this backfill.
- `investigation/{commercial_objects_recon.py,probe_com_rejects.py}` — read-only recon from the
  original build, unchanged.
- `evidence/` — `operator_lease_0[1-8]_*.png` + `operator_lease_results.json` from the original
  2026-06-12 run, plus `backfill_2026-08-28/` (robocop + dryrun + full-tree dryrun + live run
  output + DB self-clean + hygiene evidence captured by this backfill).
- `operator_lease_sow.md` — statement of work / spec (Section 6 added 2026-08-28 documenting the
  PR #436 Bank-pattern conversion; original 2026-06-12 sections kept as history).
- `JOURNAL.md` — work journal (added 2026-08-28 backfill to cover the PR #436 conversion).
- `CHECKLIST.md` — deliverable checklist (added 2026-08-28 backfill).

## Run — Robot Framework (maintained suite)
```bash
# from workstreams/master-plan/ec-automation/

# 1. dryrun (structure only, no browser/DB)
py -m robot --dryrun --outputdir tmp_dryrun tests/Configuration/Assets/Commercial_Objects/operator_lease_iud.robot

# 2. live headless run (real browser, real DB writes, self-cleaning — TC05 deletes the fixed
#    AUTOTEST_OPERATOR_LEASE code so the next run starts clean)
EC_HEADLESS=true py -m robot --outputdir tmp_live tests/Configuration/Assets/Commercial_Objects/operator_lease_iud.robot

# 3. live headed run (visible browser, for a watched demo)
EC_HEADLESS=false py -m robot --outputdir tmp_live tests/Configuration/Assets/Commercial_Objects/operator_lease_iud.robot
```

## DB self-clean check (ground truth — OV_OPERATOR_LEASE)
Run BEFORE and AFTER the live suite, from a fresh connection each time (never reuse a mid-test
session), to confirm the fixed test code (`AUTOTEST_OPERATOR_LEASE`) is absent and no `AUTOTEST%`
residual rows exist:
```sql
SELECT COUNT(*) FROM OV_OPERATOR_LEASE WHERE CODE = 'AUTOTEST_OPERATOR_LEASE';  -- expect 0
SELECT CODE FROM OV_OPERATOR_LEASE WHERE CODE LIKE 'AUTOTEST%';                 -- expect no rows
```
(`libraries/DbVerify.py` uses the generic `CODE` column on every `OV_*` view.)

## Run — Playwright (original reference, unmodified since 2026-06-12)
```bash
py -X utf8 playwright/ec_iud_operator_lease.py
EC_HEADED=1 EC_SLOWMO=400 py -X utf8 playwright/ec_iud_operator_lease.py   # watchable
```

## Key facts
- Grid `manage_object_nav_nav:form:T_data` — nav-free (the top Date+GO bar is the same universal
  as-at-date filter Bank also has, not a mandatory nav requirement).
- Field labels are screen-prefixed: **Operator Lease Code**/**Operator Lease Name** (NOT the
  generic "Code"/"Name" Bank/Object List use).
- Insert (`objectForm`) mandatory: Operator Lease Code, Operator Lease Name, Start Date. Update
  (`updateAttributes`) mandatory: Operator Lease Code (read-only), Operator Lease Name — Description
  optional in both.
- Delete `objectdates` End Date field id: `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input`.
- The RF suite uses the FIXED test code `AUTOTEST_OPERATOR_LEASE` (since PR #436); the Playwright
  driver still uses the original per-run `AUTOTEST_OPL_<timestamp>`.

## Equivalent RF files (outside this bundle, treeview-mirrored)
- T3 page object: `pageobjects/Configuration/Assets/Commercial_Objects/operator_lease_page.resource`
- Suite: `tests/Configuration/Assets/Commercial_Objects/operator_lease_iud.robot`
- Test data: `testdata/operator_lease_{insert,update,form_verify,grid_verify}.properties`
- KB selector map: `ec-ui-knowledge/screens/operator_lease.md`
