# MMS Lease — Playwright IUD

Insert / Update / Delete automation for the EC **MMS Lease** screen
(Configuration → Assets → Commercial Objects → MMS Lease), implemented in **Playwright** (Python).

MMS Lease is a **Manage Object (OV)** screen. DELETE = **End Date = Start Date**
(zero-length window) — EC true delete (object removed from `OV_MMS_LEASE`).

## Run
```bash
py -X utf8 playwright/ec_iud_mms_lease.py
EC_HEADED=1 EC_SLOWMO=400 py -X utf8 playwright/ec_iud_mms_lease.py   # watchable
```

## Folder
- `playwright/ec_iud_mms_lease.py` — thin config over the shared engine (`../../Basic_Objects/_shared/iud_engine.py`)
- `investigation/` — recon scripts used to learn the screen
- `evidence/` — screenshots + results JSON from a full run
- `mms_lease_sow.md` — statement of work / spec

## Equivalent RF suite
`tests/Configuration/Assets/Commercial_Objects/mms_lease_iud.robot`
