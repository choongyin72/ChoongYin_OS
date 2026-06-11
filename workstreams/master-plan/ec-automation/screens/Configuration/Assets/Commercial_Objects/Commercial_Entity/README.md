# Commercial Entity — Playwright IUD

Insert / Update / Delete automation for the EC **Commercial Entity** screen
(Configuration → Assets → Commercial Objects → Commercial Entity), implemented in **Playwright** (Python).

Commercial Entity is a **Manage Object (OV)** screen. DELETE = **End Date = Start Date**
(zero-length window) — EC true delete (object removed from `OV_COMMERCIAL_ENTITY`).

## Run
```bash
py -X utf8 playwright/ec_iud_commercial_entity.py
EC_HEADED=1 EC_SLOWMO=400 py -X utf8 playwright/ec_iud_commercial_entity.py   # watchable
```

## Folder
- `playwright/ec_iud_commercial_entity.py` — thin config over the shared engine (`../../Basic_Objects/_shared/iud_engine.py`)
- `investigation/` — recon scripts used to learn the screen
- `evidence/` — screenshots + results JSON from a full run
- `commercial_entity_sow.md` — statement of work / spec

## Equivalent RF suite
`tests/Configuration/Assets/Commercial_Objects/commercial_entity_iud.robot`
