# Carrier — IUD automation bundle

**Screen:** Configuration > Assets > Cargo Objects > Carrier
**Type:** OV (Manage-Object), date-effective, **plain Bank-pattern (Bank-family grid — NOT gated)**.
**Delete:** End Date = Start Date (zero-length window ⇒ true delete from `OV_CARRIER`).
**Status:** ✅ live **5/5 PASS** (post-conversion RF suite), DB-verified, self-cleaning. See
[carrier_sow.md](carrier_sow.md) and [JOURNAL.md](JOURNAL.md).

**History:** built 2026-06-19 (ec-object-iud-builder, original 4/4 arg-based RF + Playwright),
converted to the full Bank pattern in PR #477 (Batch 11, merged 2026-08-23). The RF T3/suite
below is the CURRENT (post-conversion) shape — do not confuse with the superseded 2026-06-19
`Fill New Object Form` version described in `carrier_sow.md` section 1-5.

## Layout
- `pageobjects/Configuration/Assets/Cargo_Objects/carrier_page.resource` — T3 page object
  (label-driven, properties-file-driven, T2-consolidated; mirrors `bank_page.resource`/
  `berth_page.resource`/`port_page.resource`).
- `tests/Configuration/Assets/Cargo_Objects/carrier_iud.robot` — RF suite, 5 TCs (clean-state /
  insert / update / find / delete), per-TC login/logout, fixed test code `AUTOTEST_CARRIER`.
- `testdata/carrier_{insert,update,form_verify,grid_verify}.properties` — the 4 properties files
  driving Insert/Update/Verify.
- `playwright/ec_iud_carrier.py` — freestyle Playwright proof (clean→insert→update→delete,
  self-cleaning; env creds). **Unchanged by the Bank-pattern conversion** — kept as-is per
  Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md` (Universal Screen Engine is the owner-decided
  replacement for new Playwright work; this pre-existing one is not rebuilt).
- `investigation/` — read-only recon: `resolve_carrier.py`, `scan_carrier.py`, `carrier_residue.py`.
- `evidence/` — screenshots + `ec_iud_carrier_result.json` from the original 2026-06-19 Playwright
  run, plus `evidence/rf-live-2026-08-28/` (this backfill's live RF re-run artifacts).

## Run

```bash
cd workstreams/master-plan/ec-automation

# --dryrun (structural check, no browser/DB):
py -m robot --dryrun --outputdir results/dryrun_carrier \
  tests/Configuration/Assets/Cargo_Objects/carrier_iud.robot

# Live headless run (the proof — DB-verified):
EC_HEADLESS=true py -m robot --outputdir results/carrier_live \
  tests/Configuration/Assets/Cargo_Objects/carrier_iud.robot

# Live headed run (to watch):
EC_HEADLESS=false py -m robot --outputdir results/carrier_live \
  tests/Configuration/Assets/Cargo_Objects/carrier_iud.robot

# Playwright bundle (freestyle; EC_HEADED=1 to watch, EC_CODE to override):
EC_HEADED=1 py -X utf8 screens/Configuration/Assets/Cargo_Objects/Carrier/playwright/ec_iud_carrier.py

# DB self-clean check (read-only, independent fresh connection):
py screens/Configuration/Assets/Cargo_Objects/Carrier/investigation/carrier_residue.py
# Expected output: "AUTOTEST residue rows in OV_CARRIER: 0"

# Equivalent raw SQL (ECKERNEL_EC schema):
# SELECT code, name, object_start_date, end_date FROM ECKERNEL_EC.OV_CARRIER
#   WHERE code LIKE 'AUTOTEST%' OR name LIKE 'AUTOTEST%';
```

## Key facts
- Plain OV — navigator is an optional date; the grid (`manage_object_nav_nav:form:T_data`) loads
  on open. No mandatory nav dropdown, so no OV-GM lazy-redraw wait needed.
- Mandatory fields: **Carrier Code, Carrier Name, Start Date, Unit** (mandatory reference
  dropdown, filled `__FIRST__` at Insert — a throwaway value, deliberately EXCLUDED from
  `@{CARRIER_FORM_LABELS}` so it is never round-trip-verified, same as Batch 2's VAT Code
  precedent). Carrier Group/Carrier Type/End Date and the rest are optional and not filled.
- Fixed test code `AUTOTEST_CARRIER` (post-conversion) — every run must complete TC05 (delete) so
  the code is free for the next run.
- Credentials come from env (`CARRIER_EC_USER`/`CARRIER_EC_PASS` in `resources/credentials.py`,
  R16) — no hardcoded strings.
