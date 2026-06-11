# DOA Credit Limit — Playwright IUD

Insert / Update / Delete automation for the EC **DOA Credit Limit** screen
(Configuration → Assets → Financial Objects → DOA Credit Limit), implemented in **Playwright** (Python).

DOA Credit Limit is a **Manage Object (OV)** screen. DELETE = **End Date = Start Date**
(zero-length window) — EC true delete (object removed from `OV_DOA_CREDIT_LIMIT`).

## Run
```bash
# from this folder — headless (default); a fresh AUTOTEST code is generated per run
py -X utf8 playwright/ec_iud_doa_credit_limit.py

# live (visible browser) + slow-motion
EC_HEADED=1 EC_SLOWMO=400 py -X utf8 playwright/ec_iud_doa_credit_limit.py
```

## Folder
- `playwright/ec_iud_doa_credit_limit.py` — thin config over the shared engine (`../../Basic_Objects/_shared/iud_engine.py`)
- `investigation/` — recon scripts used to learn the screen
- `evidence/` — screenshots + results JSON from a full insert → update → delete run
- `doa_credit_limit_sow.md` — statement of work / spec

## Equivalent RF suite
`tests/Configuration/Assets/Financial_Objects/doa_credit_limit_iud.robot`
