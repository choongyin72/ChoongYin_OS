# Language — Playwright IUD

Insert / Update / Delete automation for the EC **Language** screen
(Configuration → System → Language), implemented in **Playwright** (Python).

Language is a **Table class (TV view)** screen — an inline-editable grid with **no
navigator** and **physical** row delete (the row is removed from `T_BASIS_LANGUAGE`).

> ⚠️ The **Id (`LANGUAGE_ID`) cell is mandatory** (shown **yellow** in EC) — it must be
> filled before Save, alongside the Language code and Name.

## Setup
```bash
# from ec-automation/
py -m pip install -r requirements-dev.txt
playwright install chromium
```

## Run
```bash
# from this folder — headless full IUD lifecycle (default Id 999 / code ZZ)
py -X utf8 playwright/ec_iud_language.py

# live (visible browser) + a custom test row
EC_HEADED=1 EC_ID=999 EC_CODE=ZZ EC_NAME="Autotest Lang" py -X utf8 playwright/ec_iud_language.py

# isolate a single operation (also used for cleanup)
EC_INSERT_ONLY=1 py -X utf8 playwright/ec_iud_language.py
EC_DELETE_ONLY=1 EC_CODE=ZZ py -X utf8 playwright/ec_iud_language.py
```

| Env var | Default | Purpose |
|---|---|---|
| `EC_HEADED` | `0` | `1` = show the browser |
| `EC_SLOWMO` | `0` | ms slow-motion per action (headed only) |
| `EC_ID` | `999` | Id / `LANGUAGE_ID` (required) — high value, won't collide with the real 1–8 |
| `EC_CODE` | `ZZ` | Language code (the natural key) |
| `EC_NAME` | `Autotest Lang` | Name |
| `EC_INSERT_ONLY` / `EC_DELETE_ONLY` | `0` | run a single operation |

> Inline cells commit via `onchange → PrimeFaces.ab` — the script uses **real keystrokes + Tab**,
> reloads (Refresh) before verifying, and pages the grid to find rows. A fixed test row is fine
> because **physical delete self-cleans** (so the script is repeatable).

## Folder
- `playwright/ec_iud_language.py` — the implementation
- `investigation/` — recon: `language_inspect.py` (DOM scan), `db_find_language.py` (schema),
  `recon_language_confirm.py` (capture of the required-field validation that exposed the mandatory Id)
- `evidence/` — screenshots from the IUD lifecycle + the required-field validation
- `language_sow.md` — statement of work / spec

## Verify in the database
```bash
py -X utf8 investigation/db_find_language.py     # table + columns
```
