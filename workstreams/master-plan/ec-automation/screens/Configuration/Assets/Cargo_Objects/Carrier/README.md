# Carrier — IUD automation bundle

**Screen:** Configuration > Assets > Cargo Objects > Carrier
**Type:** OV (Manage-Object), date-effective, **plain (Bank-family grid — NOT gated)**.
**Delete:** End Date = Start Date (zero-length window ⇒ true delete from `OV_CARRIER`).
**Status:** ✅ live **4/4 PASS**, DB-verified, self-cleaning. See [carrier_sow.md](carrier_sow.md).

## Layout
- `playwright/ec_iud_carrier.py` — freestyle Playwright proof (clean→insert→update→delete, self-cleaning; env creds).
- `investigation/` — read-only recon: `resolve_carrier.py`, `scan_carrier.py`, `carrier_residue.py`.
- `evidence/` — screenshots + `ec_iud_carrier_result.json` from a full run.

## Run
```bash
cd workstreams/master-plan/ec-automation
# RF suite (the proof — headed, DB-verified):
EC_HEADLESS=false py -m robot --outputdir results/carrier_live \
  tests/Configuration/Assets/Cargo_Objects/carrier_iud.robot
# Playwright bundle (freestyle; EC_HEADED=1 to watch, EC_CODE to override):
EC_HEADED=1 py -X utf8 screens/Configuration/Assets/Cargo_Objects/Carrier/playwright/ec_iud_carrier.py
```

## Key facts
- Plain OV — navigator is an optional date; the grid (`manage_object_nav_nav:form:T_data`) loads on open. No mandatory nav dropdown, so no OV-GM lazy-redraw wait needed.
- Insert mandatory fields: **Carrier Code (R:0), Carrier Name (R:1), Start Date (R:4), Unit dd (R:9)** — Start Date is at R:4 (Carrier Group/Type rows precede it); Unit is a mandatory reference dd (first option used).
- Test data `AUTOTEST_CARR_*` only; the referenced Unit is read-only seed data — existing rows are never touched.
- Credentials come from env (`EC_USER`/`EC_PASS`, R16) — no hardcoded strings.
