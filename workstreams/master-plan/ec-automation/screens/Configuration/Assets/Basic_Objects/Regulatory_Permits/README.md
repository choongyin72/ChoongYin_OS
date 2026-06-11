# Regulatory Permits — Playwright IUD

Insert / Update / Delete automation for the EC **Regulatory Permits** screen
(Configuration → Assets → Basic Objects → Regulatory Permits), implemented in **Playwright** (Python).

Regulatory Permits is a **Manage Object (OV)** screen. DELETE = **End Date = Start Date** (zero-length window),
which EC treats as a true delete (object removed from `OV_REGULATORY_PERMITS`).

## Run
```bash
# from this folder — headless (default); a fresh AUTOTEST code is generated per run
py -X utf8 playwright/ec_iud_regulatory_permits.py

# live (visible browser) + slow-motion
EC_HEADED=1 EC_SLOWMO=400 py -X utf8 playwright/ec_iud_regulatory_permits.py
```

| Env var | Default | Purpose |
|---|---|---|
| `EC_HEADED` | `0` | `1` = show the browser |
| `EC_SLOWMO` | `400` | ms slow-motion per action (headed only) |
| `EC_CODE` | auto timestamp | override the test code |
| `EC_URL` / `EC_DB_DSN` | sandbox | override targets |

## Folder
- `playwright/ec_iud_regulatory_permits.py` — thin config over the shared engine (`../_shared/iud_engine.py`)
- `investigation/` — recon scripts (DOM scans + DB probes) used to learn the screen
- `evidence/` — screenshots + results JSON from a full insert → update → delete run
- `regulatory_permits_sow.md` — statement of work / spec

## Equivalent RF suite
`tests/Configuration/Assets/Basic_Objects/regulatory_permits_iud.robot` (the maintained test;
this bundle is the preserved Playwright reference + discovery trail).
