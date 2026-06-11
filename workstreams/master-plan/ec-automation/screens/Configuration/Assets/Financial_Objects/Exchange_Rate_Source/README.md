# Exchange Rate Source — Playwright IUD

Insert / Update / Delete automation for the EC **Exchange Rate Source** screen
(Configuration → Assets → Financial Objects → Exchange Rate Source), implemented in **Playwright** (Python).

Exchange Rate Source is a **Manage Object (OV)** screen. DELETE = **End Date = Start Date**
(zero-length window) — EC true delete (object removed from `OV_FOREX_SOURCE`).

## Run
```bash
# from this folder — headless (default); a fresh AUTOTEST code is generated per run
py -X utf8 playwright/ec_iud_exchange_rate_source.py

# live (visible browser) + slow-motion
EC_HEADED=1 EC_SLOWMO=400 py -X utf8 playwright/ec_iud_exchange_rate_source.py
```

## Folder
- `playwright/ec_iud_exchange_rate_source.py` — thin config over the shared engine (`../../Basic_Objects/_shared/iud_engine.py`)
- `investigation/` — recon scripts used to learn the screen
- `evidence/` — screenshots + results JSON from a full insert → update → delete run
- `exchange_rate_source_sow.md` — statement of work / spec

## Equivalent RF suite
`tests/Configuration/Assets/Financial_Objects/exchange_rate_source_iud.robot`
