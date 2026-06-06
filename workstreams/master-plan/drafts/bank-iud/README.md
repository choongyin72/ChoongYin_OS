# EC Bank IUD Test

Automated **Insert / Update / Delete** test for the EC **Bank** screen
(Configuration → Finance Objects → Bank), implemented in **two** frameworks and
verified down to the database.

Bank is an EC **Manage Object** screen (EC14+). Both implementations cover the full
lifecycle and leave existing data untouched (test codes use the `AUTOTEST_BNK_*` prefix).

---

## Folder contents

```
bank-iud/
├── README.md                      ← this file
├── requirements.txt               ← Python dependencies
├── ec-iud-test-sow.md             ← SOW: requirements, design, dev, test, lessons (v2.1)
├── ec_iud_bank_final.py           ← Implementation A — Playwright (Python)
├── ec_iud_bank.robot              ← Implementation B — Robot Framework
└── investigation/                 ← supportive scripts (how the screen was learned + DB proof)
    ├── ec_bank_inspect.py             DOM scan of the Bank screen
    ├── ec_bank_row_select_inspect.py  DOM after row selection (found updateAttributes)
    ├── ec_bank_delete_test.py         confirmed toolbar Delete is disabled
    ├── db_query_ov_bank.py            SELECT * FROM ov_bank
    ├── db_query_ov_bank_detail.py     full detail of one bank
    ├── db_compare_delete.py           End=Start vs End=Start+1 comparison
    └── db_verify_bnk010.py            verify a true delete in the DB
```

Evidence (not in this folder): screenshots in `docs/EC/screenshots/iud_bank/`,
Robot Framework reports in `tmp/rf_output*/`.

---

## Setup

```bash
py -m pip install -r requirements.txt

# Playwright browser binary
playwright install chromium

# Robot Framework Browser library — downloads Node + Chromium
py -m Browser.entry init
```

---

## Environment (local EC sandbox)

| Item | Value |
|---|---|
| EC Web App | `https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/` (user `sysadmin`) |
| EC Database | `localhost:1521/ORCL` (user `ECKERNEL_EC` / `energy`) — for DB verification |

EC must be running and reachable. Self-signed cert is handled in both scripts
(`ignore_https_errors` / `ignoreHTTPSErrors`).

---

## How to run

### A) Playwright (Python)
```bash
# headless, default code AUTOTEST_BNK_004
py -X utf8 ec_iud_bank_final.py

# live (visible browser), slow-motion, custom fresh code
EC_HEADED=1 EC_SLOWMO=700 EC_CODE=AUTOTEST_BNK_020 py -X utf8 ec_iud_bank_final.py
```
| Env var | Default | Purpose |
|---|---|---|
| `EC_HEADED` | `0` | `1` = show the browser |
| `EC_SLOWMO` | `700` | ms slow-motion per action (only when headed) |
| `EC_CODE`   | `AUTOTEST_BNK_004` | test bank code (use a fresh one each run) |
| `EC_URL`    | sandbox URL | override the EC web app URL |
| `REPO_ROOT` | auto-detected | override the repo root (see below) |

**Paths are portable** — output locations are resolved relative to the repo root
(found by walking up to the `.git` folder), not hardcoded. Screenshots go to
`<repo>/docs/EC/screenshots/iud_bank/` and the result JSON to
`<repo>/tmp/logs/ec_iud_bank_final.json`. Set `REPO_ROOT` only if running the
script from outside the repo tree.

### B) Robot Framework
```bash
# headless
robot --outputdir out ec_iud_bank.robot

# live (visible browser), slow-motion, hold open, fresh code
robot --outputdir out \
  --variable HEADLESS:False --variable SLOWMO:0.8s --variable HOLD:6s \
  --variable TEST_CODE:AUTOTEST_BNK_021 \
  --variable "TEST_NAME:AUTOTEST Bank 021" \
  --variable "TEST_NAME_UPD:AUTOTEST Bank 021 UPDATED" \
  ec_iud_bank.robot
```
Produces `report.html` + `log.html` (the log has an expandable keyword tree with
embedded step screenshots).

> **Each run needs a fresh `AUTOTEST_BNK_*` code** — a deleted bank's code may still
> exist in the DB and EC silently rejects a duplicate code on insert.

---

## The IUD patterns (Manage Object screen)

| Op | How | Key field IDs |
|---|---|---|
| **Insert** | Insert toolbar → *New Object* → fill 3 mandatory fields → Save | `objectForm:form:G:0:R:0:C:1:in` (Code), `R:1` (Name), `R:2:da_input` (Start Date) |
| **Update** | Click row → edit in `updateAttributes` form → Save | `updateAttributes:form:G:0:R:1:C:1:in` (Name) |
| **Delete** | Click row → set **End Date = Start Date** → Save | `objectdates:form:G:0:R:0:C:3:da_input` (End Date) |

### ⚠️ Delete = End Date **equal to** Start Date
The toolbar Delete button is disabled for Bank. The EC-correct delete of a
date-effective object is to set **End Date = Start Date** (zero-length window) — EC
then removes the object entirely from `ov_bank` (a true delete, DB-verified).
Setting End Date = Start + 1 day only *soft-expires* it (the row persists in the DB,
just hidden at the current date). See `ec-iud-test-sow.md` §8 for the DB proof.

---

## Verify in the database
```bash
py -X utf8 investigation/db_query_ov_bank.py        # list all banks
py -X utf8 investigation/db_verify_bnk010.py        # confirm a code is truly gone
```
