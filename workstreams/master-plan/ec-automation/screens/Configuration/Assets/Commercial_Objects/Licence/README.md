# Licence — Playwright IUD

Insert / Update / Delete automation for the EC **Licence** screen
(Configuration → Assets → Commercial Objects → Licence), implemented in **Playwright** (Python).

Licence is a **Manage Object (OV)** screen. DELETE = **End Date = Start Date**
(zero-length window) — EC true delete (object removed from `OV_LICENCE`).

## Run
```bash
py -X utf8 playwright/ec_iud_licence.py
EC_HEADED=1 EC_SLOWMO=400 py -X utf8 playwright/ec_iud_licence.py   # watchable
```

## Folder
- `playwright/ec_iud_licence.py` — thin config over the shared engine (`../../Basic_Objects/_shared/iud_engine.py`)
- `investigation/` — recon scripts used to learn the screen
- `evidence/` — screenshots + results JSON from a full run
- `licence_sow.md` — statement of work / spec

## Equivalent RF suite
`tests/Configuration/Assets/Commercial_Objects/licence_iud.robot`
