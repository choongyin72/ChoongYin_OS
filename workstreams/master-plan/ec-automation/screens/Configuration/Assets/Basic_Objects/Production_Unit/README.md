# Production Unit — Playwright IUD

Insert / Update / Delete automation for the EC **Production Unit** screen
(Configuration → Assets → Basic Objects → Production Unit), implemented in **Playwright** (Python).

Production Unit is a **Manage Object (OV)** screen. DELETE = **End Date = Start Date** (zero-length window),
which EC treats as a true delete (object removed from `OV_PRODUCTIONUNIT`).

## Run
```bash
# from this folder — headless (default); a fresh AUTOTEST code is generated per run
py -X utf8 playwright/ec_iud_production_unit.py

# live (visible browser) + slow-motion
EC_HEADED=1 EC_SLOWMO=400 py -X utf8 playwright/ec_iud_production_unit.py
```

| Env var | Default | Purpose |
|---|---|---|
| `EC_HEADED` | `0` | `1` = show the browser |
| `EC_SLOWMO` | `400` | ms slow-motion per action (headed only) |
| `EC_CODE` | auto timestamp | override the test code |
| `EC_URL` / `EC_DB_DSN` | sandbox | override targets |

## Folder
- `playwright/ec_iud_production_unit.py` — thin config over the shared engine (`../_shared/iud_engine.py`)
- `investigation/` — recon scripts (DOM scans + DB probes) used to learn the screen
- `evidence/` — screenshots + results JSON from a full insert → update → delete run
- `production_unit_sow.md` — statement of work / spec

## Equivalent RF suite
`tests/Configuration/Assets/Basic_Objects/production_unit_iud.robot` (the maintained test;
this bundle is the preserved Playwright reference + discovery trail).
