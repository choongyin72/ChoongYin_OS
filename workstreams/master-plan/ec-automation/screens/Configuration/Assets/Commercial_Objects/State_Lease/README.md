# State Lease — Playwright IUD

Insert / Update / Delete automation for the EC **State Lease** screen
(Configuration → Assets → Commercial Objects → State Lease), implemented in **Playwright** (Python).

State Lease is a **Manage Object (OV)** screen. DELETE = **End Date = Start Date**
(zero-length window) — EC true delete (object removed from `OV_STATE_LEASE`).

## Run
```bash
py -X utf8 playwright/ec_iud_state_lease.py
EC_HEADED=1 EC_SLOWMO=400 py -X utf8 playwright/ec_iud_state_lease.py   # watchable
```

## Folder
- `playwright/ec_iud_state_lease.py` — thin config over the shared engine (`../../Basic_Objects/_shared/iud_engine.py`)
- `investigation/` — recon scripts used to learn the screen
- `evidence/` — screenshots + results JSON from a full run
- `state_lease_sow.md` — statement of work / spec

## Equivalent RF suite
`tests/Configuration/Assets/Commercial_Objects/state_lease_iud.robot`
