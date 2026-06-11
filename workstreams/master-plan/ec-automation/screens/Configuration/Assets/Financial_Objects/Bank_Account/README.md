# Bank Account — Playwright IUD

Insert / Update / Delete automation for the EC **Bank Account** screen
(Configuration → Assets → Financial Objects → Bank Account), implemented in **Playwright** (Python).

Bank Account is a **Manage Object (OV)** screen. DELETE = **End Date = Start Date**
(zero-length window) — EC true delete (object removed from `OV_BANK_ACCOUNT`).

## Run
```bash
# from this folder — headless (default); a fresh AUTOTEST code is generated per run
py -X utf8 playwright/ec_iud_bank_account.py

# live (visible browser) + slow-motion
EC_HEADED=1 EC_SLOWMO=400 py -X utf8 playwright/ec_iud_bank_account.py
```

## Folder
- `playwright/ec_iud_bank_account.py` — thin config over the shared engine (`../../Basic_Objects/_shared/iud_engine.py`)
- `investigation/` — recon scripts used to learn the screen
- `evidence/` — screenshots + results JSON from a full insert → update → delete run
- `bank_account_sow.md` — statement of work / spec

## Equivalent RF suite
`tests/Configuration/Assets/Financial_Objects/bank_account_iud.robot`
