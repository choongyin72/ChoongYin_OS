# VAT Code — Playwright IUD

Insert / Update / Delete automation for the EC **VAT Code** screen
(Configuration → Assets → Financial Objects → VAT Code), implemented in **Playwright** (Python).

VAT Code is a **Manage Object (OV)** screen. DELETE = **End Date = Start Date**
(zero-length window) — EC true delete (object removed from `OV_VAT_CODE`).

## Run
```bash
# from this folder — headless (default); a fresh AUTOTEST code is generated per run
py -X utf8 playwright/ec_iud_vat_code.py

# live (visible browser) + slow-motion
EC_HEADED=1 EC_SLOWMO=400 py -X utf8 playwright/ec_iud_vat_code.py
```

## Folder
- `playwright/ec_iud_vat_code.py` — thin config over the shared engine (`../../Basic_Objects/_shared/iud_engine.py`)
- `investigation/` — recon scripts used to learn the screen
- `evidence/` — screenshots + results JSON from a full insert → update → delete run
- `vat_code_sow.md` — statement of work / spec

## Equivalent RF suite
`tests/Configuration/Assets/Financial_Objects/vat_code_iud.robot`
