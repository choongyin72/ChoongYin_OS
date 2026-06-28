# Tract - Well Setup — EC IUD bundle

**Screen:** Configuration > Assets > Royalty Objects > **Tract - Well Setup**
**Pattern:** PC (parent-child setup), sibling of Unit - Well Setup over the same `WELL_SETUP` base.
**Nav:** CASCADE — form date + **Unit Agreement** (G:1) + **Tract** (G:2) + GO. Each grid row links
a **Perf Interval** (member) to a **Tract** (parent, `OBJECT_CODE`).
**DB oracle:** count-delta on `DV_TRACT_WELL_SETUP.PERF_INTERVAL_CODE` (+ COMMENTS present-in-view for UPDATE).

## Contents
| Path | What |
|---|---|
| `tract_well_setup_sow.md` | Statement of Work — classification, cascade nav, test data, dev story, lessons |
| `playwright/ec_iud_tract_well_setup.py` | Standalone Playwright reference (insert -> update -> delete, DB-verified, self-cleaning) |
| `investigation/` | Read-only recon + pre-flight scripts |
| `evidence/` | Screenshots + `tract_well_setup_results.json` from a full run |

## Maintained RF suite (the canonical test)
- Suite: `tests/Configuration/Assets/Royalty_Objects/tract_well_setup_iud.robot`
- Page object (T3): `pageobjects/Configuration/Assets/Royalty_Objects/tract_well_setup_page.resource`
- TC01 clean · TC02 insert (+1) · TC03 update (COMMENTS, present-in-view) · TC04 delete (back to baseline) — all DB-verified.

## Run
```bash
EC_HEADLESS=false py -m robot --outputdir results \
  tests/Configuration/Assets/Royalty_Objects/tract_well_setup_iud.robot

EC_HEADED=1 py screens/Configuration/Assets/Royalty_Objects/Tract_Well_Setup/playwright/ec_iud_tract_well_setup.py
```

## Test data (pre-flight verified 2026-06-27)
- Unit Agreement (G:1): **Unit Agreement 3** (gates the Tract dd).
- Tract (parent, G:2): **Unit 3 Tract 01** (TRACT_U3_T01) — existing object, effective 2010-01-01;
  already holds P1 PI-5 / P1 PI-6 (never touched).
- Member: Perf Interval **108_WB1-1_PF1** — effective 2003-01-01, baseline 0 in any tract.
- Form date / membership start: **2011-01-01**.

## Gotchas (carried from Unit - Well Setup)
- **CASCADE nav:** the Tract dd (G:2) is empty until a Unit Agreement (G:1) is picked.
- NEW row start-date = calendar `C0_da_input`; SAVED row = text `C0_in` (select saved row for delete via `C0_in`).
- `C3_in`=COMMENTS, `C4_in`=SORT_ORDER — these cells appear only after the row is saved.
- No empty Tract exists; the test adds a baseline-0 member under an existing Tract and touches only its own row.
