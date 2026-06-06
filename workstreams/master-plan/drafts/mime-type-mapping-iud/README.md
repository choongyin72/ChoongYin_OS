# EC MIME Type Mapping IUD Test

Automated **Insert / Update / Delete** test for the EC **MIME Type Mapping** screen
(Configuration → System), implemented in **two** frameworks and verified down to the
database.

MIME Type Mapping is an EC **Table class (TV view)** screen — an inline-editable grid
with **no navigator** and **physical** row delete. This is the deliberate contrast to the
**Manage Object (OV)** pattern of the Bank/Equipment tasks, where delete is a
date-effective *End Date = Start Date*. Both implementations cover the full lifecycle and
leave existing data untouched (test rows use the `application/x-ec-autotest*` MIME values).

---

## Folder contents

```
mime-type-mapping-iud/
├── README.md                          ← this file
├── requirements.txt                   ← Python dependencies
├── ec-iud-mime-type-mapping-sow.md    ← SOW: requirements, design, dev, test, lessons (v2.0 COMPLETE)
├── ec_iud_mime.py                     ← Implementation A — Playwright (Python)
├── ec_iud_mime.robot                  ← Implementation B — Robot Framework
└── investigation/                     ← supportive scripts (how the screen was learned + DB proof)
    ├── mime_inspect.py                   DOM scan — grid, toolbar, Insert submenu, new-row cell IDs
    ├── mime_cell_scan.py                 cell-commit mechanism (onchange→PrimeFaces.ab), paginator
    └── db_query_tv_mime.py               TV view + base-table counts, row presence (DB verify)
```

Evidence (not in this folder): Playwright screenshots in `docs/EC/screenshots/iud_mime/`,
Robot Framework reports/screenshots in `tmp/rf_mime/`.

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
# headless full IUD lifecycle, default test row application/x-ec-autotest
py -X utf8 ec_iud_mime.py

# live (visible browser), slow-motion, custom test MIME
EC_HEADED=1 EC_SLOWMO=700 EC_CODE=application/x-ec-autotest-demo py -X utf8 ec_iud_mime.py

# isolate a single operation (also used for cleanup)
EC_INSERT_ONLY=1 py -X utf8 ec_iud_mime.py
EC_DELETE_ONLY=1 EC_CODE=application/x-ec-autotest-rf py -X utf8 ec_iud_mime.py
```
| Env var | Default | Purpose |
|---|---|---|
| `EC_HEADED` | `0` | `1` = show the browser |
| `EC_SLOWMO` | `700` | ms slow-motion per action (only applied when headed) |
| `EC_CODE` | `application/x-ec-autotest` | test MIME type (the natural key) |
| `EC_INSERT_ONLY` | `0` | `1` = run insert only |
| `EC_DELETE_ONLY` | `0` | `1` = run delete only (handy for cleanup) |
| `EC_URL` | sandbox URL | override the EC web app URL |

**Paths are portable** — screenshots resolve relative to the repo root and the result
JSON goes to `<repo>/tmp/logs/ec_iud_mime.json`.

### B) Robot Framework
```bash
# headless (self-cleaning: insert → update → physical delete)
robot --outputdir out ec_iud_mime.robot

# live (visible browser), slow-motion, hold open
robot --outputdir out \
  --variable HEADLESS:False --variable SLOWMO:200 --variable HOLD:6s \
  ec_iud_mime.robot
```
The suite uses its own self-cleaning test row `application/x-ec-autotest-rf`:
TC01 asserts clean state → TC02 insert → TC03 update → TC04 **physical** delete, leaving
the DB exactly as found. Produces `report.html` + `log.html` (expandable keyword tree
with embedded step screenshots).

---

## The IUD patterns (Table class / TV view)

| Op | How | Key field IDs |
|---|---|---|
| **Insert** | Insert toolbar → *MIME Type Mapping* → new editable grid row → fill 2 cells → Save | `mime_type_table:form:T:{row}:C0_in` (MIME Type), `…:C1_in` (File Extensions) |
| **Update** | Edit the File Extensions cell inline → Save | `mime_type_table:form:T:{row}:C1_in` |
| **Delete** | Select row → Delete toolbar → *MIME Type Mapping* → Save | (toolbar submenu) |

### ⚠️ Two things that bite (see SOW §3.2 / §8)
1. **Cells commit via `onchange → PrimeFaces.ab` (partial submit).** `fill()` + synthetic
   `change` events do **not** stage the value — drive **real keystrokes + `Tab`**, then
   wait for the AJAX, or Save commits nothing.
2. **The grid is paginated (~20 rows/page).** Look up rows by paging (first → next…), and
   **Refresh before verifying** so the grid reflects the DB. Never "diff the visible rows"
   as an integrity check — verify at the DB.

### TV vs OV — delete semantics
A Table class row is **physically deleted** from the base table (`CTRL_MIME_TYPE_MAPPING`)
— no versioning, no dates. Contrast the OV/Manage-Object delete (Bank/Equipment), which is
*End Date = Start Date* on a date-effective object.

---

## Verify in the database
```bash
py -X utf8 investigation/db_query_tv_mime.py                              # counts + list all MIME types
py -X utf8 investigation/db_query_tv_mime.py application/x-ec-autotest    # check a specific test row
```
