# Unit - Well Setup — EC IUD bundle

**Screen:** Configuration > Assets > Royalty Objects > **Unit - Well Setup**
**Pattern:** PC (parent-child setup) — gated navigator (form date + Unit Agreement + GO) →
inline membership grid; Insert/Delete toolbar acts on "Well Setup". Each row links a
**Perf Interval** (member) to a **Unit Agreement** (parent).
**DB oracle:** count-delta on `DV_UNIT_WELL_SETUP.PERF_INTERVAL_CODE`.

## Contents
| Path | What |
|---|---|
| `unit_well_setup_sow.md` | Statement of Work — classification, DOM, test data, dev story, lessons |
| `playwright/ec_iud_unit_well_setup.py` | Standalone Playwright reference flow (insert → delete, DB-verified, self-cleaning) |
| `investigation/` | Read-only recon + pre-flight scripts |
| `evidence/` | Screenshots + `unit_well_setup_results.json` from a full run |

## Maintained RF suite (the canonical test)
- Suite: `tests/Configuration/Assets/Royalty_Objects/unit_well_setup_iud.robot`
- Page object (T3): `pageobjects/Configuration/Assets/Royalty_Objects/unit_well_setup_page.resource`
- TC01 clean state · TC02 insert (+1) · TC03 update (COMMENTS, present-in-view) · TC04 delete (back to baseline) — all DB-verified.

## Run
```bash
# RF (headed = the proof)
EC_HEADLESS=false py -m robot --outputdir results \
  tests/Configuration/Assets/Royalty_Objects/unit_well_setup_iud.robot

# Playwright reference (headed)
EC_HEADED=1 py screens/Configuration/Assets/Royalty_Objects/Unit_Well_Setup/playwright/ec_iud_unit_well_setup.py
```

## Test data (pre-flight verified 2026-06-27)
- Parent: **Unit Agreement 3** (UNIT_3) — effective 2010-01-01, EMPTY (clean target).
- Member: Perf Interval **108_WB1-1_PF1** — effective 2003-01-01, baseline 0 rows anywhere.
- Form date / membership start: **2011-01-01** (inside both windows).

## Gotchas
- A NEW (unsaved) grid row's start-date cell is a calendar (`C0_da_input`); once SAVED the
  same row renders it as a text cell (`C0_in`). Select the persisted row for delete via `C0_in`.
- The COMMENTS/SORT_ORDER cells (`C3_in` / `C4_in`) appear **only after the row is saved** — a NEW
  blank row exposes just C0/C1/C2. So UPDATE edits a *saved* row. `C3_in`=COMMENTS, `C4_in`=SORT_ORDER.
