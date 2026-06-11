# Cost Object Mapping — Playwright IUD

Insert / Update / Delete automation for the EC **Cost Object Mapping** screen
(Configuration → Assets → Financial Objects → Cost Object Mapping), implemented in **Playwright** (Python).

Cost Object Mapping is a **Manage Object (OV)** screen. DELETE = **End Date = Start Date**
(zero-length window) — EC true delete (object removed from `OV_FIN_COST_OBJECT`).

## Run
```bash
# from this folder — headless (default); a fresh AUTOTEST code is generated per run
py -X utf8 playwright/ec_iud_cost_object_mapping.py

# live (visible browser) + slow-motion
EC_HEADED=1 EC_SLOWMO=400 py -X utf8 playwright/ec_iud_cost_object_mapping.py
```

## Folder
- `playwright/ec_iud_cost_object_mapping.py` — thin config over the shared engine (`../../Basic_Objects/_shared/iud_engine.py`)
- `investigation/` — recon scripts used to learn the screen
- `evidence/` — screenshots + results JSON from a full insert → update → delete run
- `cost_object_mapping_sow.md` — statement of work / spec

## Equivalent RF suite
`tests/Configuration/Assets/Financial_Objects/cost_object_mapping_iud.robot`
