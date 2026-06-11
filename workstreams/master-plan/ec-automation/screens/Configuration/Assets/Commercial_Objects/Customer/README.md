# Customer — Playwright IUD

Insert / Update / Delete automation for the EC **Customer** screen
(Configuration → Assets → Commercial Objects → Customer), implemented in **Playwright** (Python).

Customer is a **Manage Object (OV)** screen. DELETE = **End Date = Start Date**
(zero-length window) — EC true delete (object removed from `OV_CUSTOMER`).

## Run
```bash
py -X utf8 playwright/ec_iud_customer.py
EC_HEADED=1 EC_SLOWMO=400 py -X utf8 playwright/ec_iud_customer.py   # watchable
```

## Folder
- `playwright/ec_iud_customer.py` — thin config over the shared engine (`../../Basic_Objects/_shared/iud_engine.py`)
- `investigation/` — recon scripts used to learn the screen
- `evidence/` — screenshots + results JSON from a full run
- `customer_sow.md` — statement of work / spec

## Equivalent RF suite
`tests/Configuration/Assets/Commercial_Objects/customer_iud.robot`
