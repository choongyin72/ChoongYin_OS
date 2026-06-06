# EC Equipment IUD Test

Automated **Insert / Update / Delete** for the EC **Equipment** screen
(Configuration → Assets → Equipment Objects → Equipment), in two frameworks,
**DB-verified** in `OV_EQPM`.

Equipment is a **Manage Object** screen (EC14+) — the same family as Bank, and this is
**screen 2 of 2** for that pattern. The new element here is a **5-field cascading navigator**
that must be set before the equipment list loads. Existing data (`OFF_*` equipment) is never
touched; test codes use the `AUTOTEST_EQP_*` prefix and are self-cleaning (true delete).

---

## Folder contents
```
equipment-iud/
├── README.md                      ← this file
├── requirements.txt               ← Python dependencies
├── ec-iud-equipment-sow.md        ← SOW (requirements, design, results, lessons)
├── ec_iud_equipment.py            ← Implementation A — Playwright (Python)
├── ec_iud_equipment.robot         ← Implementation B — Robot Framework
└── investigation/                 ← Phase 0 DOM scans + DB verification
    ├── equipment_inspect.py            initial DOM scan
    ├── equipment_inspect_b.py          labeled field maps
    ├── equipment_find_table.py         locate result table
    ├── equipment_nav_crack.py          navigator attempts
    ├── equipment_nav_robust.py         navigator attempts
    ├── equipment_ac_html.py            autocomplete HTML (cracked the dd_button/dd_panel)
    ├── equipment_nav_final.py          definitive nav + full field map
    ├── db_find_view.py                 found OV_EQPM
    └── db_query_ov_equipment.py        verify a code in OV_EQPM
```

## Setup
```bash
py -m pip install -r requirements.txt
playwright install chromium          # for the Playwright script
py -m Browser.entry init             # for the Robot Framework suite
```

## Environment
| Item | Value |
|---|---|
| EC Web App | `https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/` (user `sysadmin`) |
| EC Database | `localhost:1521/ORCL` (`ECKERNEL_EC` / `energy`) — object view `OV_EQPM` |

## How to run

### A) Playwright
```bash
py -X utf8 ec_iud_equipment.py                                   # headless, AUTOTEST_EQP_001
EC_HEADED=1 EC_SLOWMO=700 EC_CODE=AUTOTEST_EQP_050 py -X utf8 ec_iud_equipment.py   # live, fresh code
```
| Env var | Default | Purpose |
|---|---|---|
| `EC_HEADED` | `0` | `1` = show the browser |
| `EC_SLOWMO` | `700` | ms slow-motion (headed only) |
| `EC_CODE` | `AUTOTEST_EQP_001` | test code (a deleted code is reusable — true delete) |
| `EC_SKIP_DELETE` | `0` | `1` = insert+update only (for DB proof) |
| `EC_DELETE_ONLY` | `0` | `1` = select existing + delete (cleanup) |
| `EC_URL` / `REPO_ROOT` | — | overrides; paths resolve relative to repo root |

### B) Robot Framework
```bash
robot --outputdir out ec_iud_equipment.robot                     # headless
robot --outputdir out --variable HEADLESS:False --variable SLOWMO:0.8s --variable HOLD:6s \
      --variable TEST_CODE:AUTOTEST_EQP_051 \
      --variable "TEST_NAME:AUTOTEST Equipment 051" \
      --variable "TEST_NAME_UPD:AUTOTEST Equipment 051 UPDATED" ec_iud_equipment.robot
```

## The navigator (the key difference vs Bank)
5 fields; set the 4 dropdowns to these **EXACT** values, then Go:

| Field | Value | Element |
|---|---|---|
| Date | (default) | `nav:form:G:0:R:1:C:0:da_input` |
| Production Unit | `Production Unit` | `nav:form:G:1:…:dd` |
| Area | `Offshore area` | `nav:form:G:2:…:dd` |
| Facility Class 1 | `Offshore facility` | `nav:form:G:3:…:dd` |
| Equipment Type | `Compressor` | `nav:form:G:4:…:dd` |
| Go | — | `button:form:B` |

Each dropdown is a `ui-autocomplete-dd`: **click the chevron `…:dd_button` → click the exact
option in `…:dd_panel`**. Do NOT type — typing fires re-render AJAX that drops characters.

## IUD field IDs
| Op | Field | Element |
|---|---|---|
| Insert | Equipment Code | `tab:tabPanel:objectForm:form:G:0:R:1:C:1:in` |
| Insert | Equipment Name | `…objectForm…:R:2:C:1:in` |
| Insert | Start Date | `…objectForm…:R:4:C:1:da_input` |
| (Insert) | Equipment Type | `…objectForm…:R:0` — read-only, auto = Compressor (from navigator) |
| Update | Equipment Name | `tab:tabPanel:updateAttributes:form:G:0:R:2:C:1:in` |
| Delete | End Date = Start Date | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` |

**Delete** = set End Date equal to Start Date (zero-length window → true delete; the toolbar
`−` button is disabled, same as Bank). Verified in `OV_EQPM`: the row is fully removed.

## Verify in the DB
```bash
py -X utf8 investigation/db_query_ov_equipment.py AUTOTEST_EQP_001
```
