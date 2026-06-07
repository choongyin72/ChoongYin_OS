# Equipment — Playwright IUD

Insert / Update / Delete automation for the EC **Equipment** screen
(Configuration → Assets → Equipment Objects → Equipment), implemented in **Playwright** (Python).

Equipment is a **Manage Object** screen with a **5-field cascading navigator**
(Production Unit → Offshore area → Offshore facility → Compressor → Go) that must be set
before the list loads. DELETE = **End Date = Start Date** (true delete in `OV_EQPM`).

## Setup
```bash
# from ec-automation/
py -m pip install -r requirements-dev.txt
playwright install chromium
```

## Run
```bash
# from this folder — headless (default)
py -X utf8 playwright/ec_iud_equipment.py

# live (visible browser) + slow-motion + a fresh code
EC_HEADED=1 EC_SLOWMO=700 EC_CODE=AUTOTEST_EQP_020 py -X utf8 playwright/ec_iud_equipment.py
```

| Env var | Default | Purpose |
|---|---|---|
| `EC_HEADED` | `0` | `1` = show the browser |
| `EC_SLOWMO` | `700` | ms slow-motion per action (headed only) |
| `EC_CODE` | `AUTOTEST_EQP_*` | test equipment code — use a fresh one each run |
| `EC_URL` | sandbox URL | override the EC web app URL |

> The cascading navigator is driven via each filter's chevron (`dd_button`) → exact option in
> the panel (`dd_panel`) — typing into the autocomplete is unreliable. Use a **fresh** code each run.

## Folder
- `playwright/ec_iud_equipment.py` — the implementation
- `investigation/` — recon scripts incl. the navigator-cracking iterations + DB queries
- `evidence/` — screenshots from a full insert → update → delete run
- `equipment_sow.md` — statement of work / spec

## Verify in the database
```bash
py -X utf8 investigation/db_query_ov_equipment.py
```
