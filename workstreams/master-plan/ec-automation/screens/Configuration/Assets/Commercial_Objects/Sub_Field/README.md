# Sub Field — Playwright IUD

Insert / Update / Delete automation for the EC **Sub Field** screen
(Configuration → Assets → Commercial Objects → Sub Field), implemented in **Playwright** (Python).

Sub Field is a **Manage Object (OV-GM groupmodel)** screen. DELETE = **End Date = Start Date**
(zero-length window) — EC true delete (object removed from `OV_SUB_FIELD`).

> ⚠ **PARKED** — groupmodel not enabled for SUB_FIELD in this environment: inserts persist to OV_SUB_FIELD but the grid can never list them (same as Production Sub Unit) - confirmed by probe + DB on 2026-06-12

## Run
```bash
py -X utf8 playwright/ec_iud_sub_field.py
EC_HEADED=1 EC_SLOWMO=400 py -X utf8 playwright/ec_iud_sub_field.py   # watchable
```

## Folder
- `playwright/ec_iud_sub_field.py` — thin config over the shared engine (`../../Basic_Objects/_shared/iud_engine.py`)
- `investigation/` — recon scripts used to learn the screen
- `evidence/` — screenshots + results JSON from a full run
- `sub_field_sow.md` — statement of work / spec

## Equivalent RF suite
`tests/Configuration/Assets/Commercial_Objects/sub_field_iud.robot` (in `_parked/`)
