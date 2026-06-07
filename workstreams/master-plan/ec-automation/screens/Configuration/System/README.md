# MIME Type Mapping — Playwright IUD

Insert / Update / Delete automation for the EC **MIME Type Mapping** screen
(Configuration → System → MIME Type Mapping), implemented in **Playwright** (Python).

MIME Type Mapping is a **Table class (TV view)** screen — an inline-editable **paginated grid**
with **no navigator** and **physical** row delete (the row is removed from
`CTRL_MIME_TYPE_MAPPING`, not date-expired).

## Setup
```bash
# from ec-automation/
py -m pip install -r requirements-dev.txt
playwright install chromium
```

## Run
```bash
# from this folder — headless full IUD lifecycle (default code application/x-ec-autotest)
py -X utf8 playwright/ec_iud_mime.py

# live (visible browser) + slow-motion + custom test MIME
EC_HEADED=1 EC_SLOWMO=700 EC_CODE=application/x-ec-autotest-demo py -X utf8 playwright/ec_iud_mime.py

# isolate a single operation (also used for cleanup)
EC_INSERT_ONLY=1 py -X utf8 playwright/ec_iud_mime.py
EC_DELETE_ONLY=1 EC_CODE=application/x-ec-autotest-rf py -X utf8 playwright/ec_iud_mime.py
```

| Env var | Default | Purpose |
|---|---|---|
| `EC_HEADED` | `0` | `1` = show the browser |
| `EC_SLOWMO` | `700` | ms slow-motion per action (headed only) |
| `EC_CODE` | `application/x-ec-autotest` | test MIME type (the natural key) |
| `EC_INSERT_ONLY` / `EC_DELETE_ONLY` | `0` | run a single operation |
| `EC_URL` | sandbox URL | override the EC web app URL |

> Inline cells commit via `onchange → PrimeFaces.ab` — the script drives **real keystrokes + Tab**
> (a synthetic `fill` stages nothing), reloads (Refresh) before verifying, and pages the grid to find rows.

## Folder
- `playwright/ec_iud_mime.py` — the implementation
- `investigation/` — recon scripts: `mime_inspect.py`, `mime_cell_scan.py` (cell-commit discovery), DB query
- `evidence/` — screenshots from the IUD lifecycle + scans
- `mime_sow.md` — statement of work / spec

## Verify in the database
```bash
py -X utf8 investigation/db_query_tv_mime.py                              # counts + list
py -X utf8 investigation/db_query_tv_mime.py application/x-ec-autotest    # check a specific row
```
