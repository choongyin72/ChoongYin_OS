# Bank — Playwright IUD

> **SUPERSEDED (2026-07-25):** the standalone `playwright/ec_iud_bank.py` is now a thin pointer to the
> reusable driver `py/bank_iud.py` (engine `py/ec_object_iud.py`, DB verify `libraries/DbVerify.py`).
> Selector map of record: `ec-ui-knowledge/screens/bank.md`. Notes below are retained for context.

Insert / Update / Delete automation for the EC **Bank** screen
(Configuration → Assets → Financial Objects → Bank), implemented in **Playwright** (Python).

Bank is a **Manage Object** screen. DELETE = **End Date = Start Date** (zero-length window),
which EC treats as a true delete (object removed from `ov_bank`).

## Setup
```bash
# from ec-automation/
py -m pip install -r requirements-dev.txt
playwright install chromium
```

## Run
```bash
# from this folder — headless (default)
py -X utf8 playwright/ec_iud_bank.py

# live (visible browser) + slow-motion + a fresh code
EC_HEADED=1 EC_SLOWMO=700 EC_CODE=AUTOTEST_BNK_020 py -X utf8 playwright/ec_iud_bank.py
```

| Env var | Default | Purpose |
|---|---|---|
| `EC_HEADED` | `0` | `1` = show the browser |
| `EC_SLOWMO` | `700` | ms slow-motion per action (headed only) |
| `EC_CODE` | `AUTOTEST_BNK_004` | test bank code — use a fresh one each run |
| `EC_URL` | sandbox URL | override the EC web app URL |

> Each run needs a **fresh** `AUTOTEST_BNK_*` code — a deleted bank's code lingers in the
> base table and EC silently rejects a duplicate on insert.

## Folder
- `playwright/ec_iud_bank.py` — the implementation
- `investigation/` — recon scripts (DOM scans + DB queries) used to learn the screen
- `evidence/` — screenshots from a full insert → update → delete run
- `bank_sow.md` — statement of work / spec

## Verify in the database
```bash
py -X utf8 investigation/db_query_ov_bank.py        # list ov_bank
py -X utf8 investigation/db_verify_bnk010.py        # confirm a code is truly gone
```
