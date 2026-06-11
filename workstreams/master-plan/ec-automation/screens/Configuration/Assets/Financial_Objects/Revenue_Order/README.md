# Revenue Order — Playwright IUD

Insert / Update / Delete automation for the EC **Revenue Order** screen
(Configuration → Assets → Financial Objects → Revenue Order), implemented in **Playwright** (Python).

Revenue Order is a **Manage Object (OV)** screen. DELETE = **End Date = Start Date**
(zero-length window) — EC true delete (object removed from `OV_FIN_REVENUE_ORDER`).

## Run
```bash
# from this folder — headless (default); a fresh AUTOTEST code is generated per run
py -X utf8 playwright/ec_iud_revenue_order.py

# live (visible browser) + slow-motion
EC_HEADED=1 EC_SLOWMO=400 py -X utf8 playwright/ec_iud_revenue_order.py
```

## Folder
- `playwright/ec_iud_revenue_order.py` — thin config over the shared engine (`../../Basic_Objects/_shared/iud_engine.py`)
- `investigation/` — recon scripts used to learn the screen
- `evidence/` — screenshots + results JSON from a full insert → update → delete run
- `revenue_order_sow.md` — statement of work / spec

## Equivalent RF suite
`tests/Configuration/Assets/Financial_Objects/revenue_order_iud.robot`
