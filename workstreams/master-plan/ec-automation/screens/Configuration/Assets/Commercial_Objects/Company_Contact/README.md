# Company Contact — Playwright IUD

Insert / Update / Delete automation for the EC **Company Contact** screen
(Configuration → Assets → Commercial Objects → Company Contact), implemented in **Playwright** (Python).

Company Contact is a **Manage Object (OV)** screen. DELETE = **End Date = Start Date**
(zero-length window) — EC true delete (object removed from `OV_COMPANY_CONTACT`).

## Run
```bash
py -X utf8 playwright/ec_iud_company_contact.py
EC_HEADED=1 EC_SLOWMO=400 py -X utf8 playwright/ec_iud_company_contact.py   # watchable
```

## Folder
- `playwright/ec_iud_company_contact.py` — thin config over the shared engine (`../../Basic_Objects/_shared/iud_engine.py`)
- `investigation/` — recon scripts used to learn the screen
- `evidence/` — screenshots + results JSON from a full run
- `company_contact_sow.md` — statement of work / spec

## Equivalent RF suite
`tests/Configuration/Assets/Commercial_Objects/company_contact_iud.robot`
