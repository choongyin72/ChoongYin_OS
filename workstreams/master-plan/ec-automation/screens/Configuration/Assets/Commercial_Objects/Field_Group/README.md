# Field Group — Playwright IUD

Insert / Update / Delete automation for the EC **Field Group** screen
(Configuration → Assets → Commercial Objects → Field Group), implemented in **Playwright** (Python).

Field Group is a **Manage Object (OV)** screen. DELETE = **End Date = Start Date**
(zero-length window) — EC true delete (object removed from `OV_FIELD_GROUP`).

## Run
```bash
py -X utf8 playwright/ec_iud_field_group.py
EC_HEADED=1 EC_SLOWMO=400 py -X utf8 playwright/ec_iud_field_group.py   # watchable
```

## Folder
- `playwright/ec_iud_field_group.py` — thin config over the shared engine (`../../Basic_Objects/_shared/iud_engine.py`)
- `investigation/` — recon scripts used to learn the screen
- `evidence/` — screenshots + results JSON from a full run
- `field_group_sow.md` — statement of work / spec

## Equivalent RF suite
`tests/Configuration/Assets/Commercial_Objects/field_group_iud.robot`
