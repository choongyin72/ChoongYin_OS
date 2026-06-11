# Field — Playwright IUD

Insert / Update / Delete automation for the EC **Field** screen
(Configuration → Assets → Commercial Objects → Field), implemented in **Playwright** (Python).

Field is a **Manage Object (OV-GM groupmodel)** screen. DELETE = **End Date = Start Date**
(zero-length window) — EC true delete (object removed from `OV_FIELD`).

## Run
```bash
py -X utf8 playwright/ec_iud_field.py
EC_HEADED=1 EC_SLOWMO=400 py -X utf8 playwright/ec_iud_field.py   # watchable
```

## Folder
- `playwright/ec_iud_field.py` — thin config over the shared engine (`../../Basic_Objects/_shared/iud_engine.py`)
- `investigation/` — recon scripts used to learn the screen
- `evidence/` — screenshots + results JSON from a full run
- `field_sow.md` — statement of work / spec

## Equivalent RF suite
`tests/Configuration/Assets/Commercial_Objects/field_iud.robot`
