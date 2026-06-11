# Product Description — Playwright IUD

Insert / Update / Delete automation for the EC **Product Description** screen
(Configuration → Assets → Financial Objects → Product Description), implemented in **Playwright** (Python).

Product Description is a **Manage Object (OV)** screen. DELETE = **End Date = Start Date**
(zero-length window) — EC true delete (object removed from `OV_PRODUCT_NODE_ITEM`).

## Run
```bash
# from this folder — headless (default); a fresh AUTOTEST code is generated per run
py -X utf8 playwright/ec_iud_product_description.py

# live (visible browser) + slow-motion
EC_HEADED=1 EC_SLOWMO=400 py -X utf8 playwright/ec_iud_product_description.py
```

## Folder
- `playwright/ec_iud_product_description.py` — thin config over the shared engine (`../../Basic_Objects/_shared/iud_engine.py`)
- `investigation/` — recon scripts used to learn the screen
- `evidence/` — screenshots + results JSON from a full insert → update → delete run
- `product_description_sow.md` — statement of work / spec

## Equivalent RF suite
`tests/Configuration/Assets/Financial_Objects/product_description_iud.robot`
