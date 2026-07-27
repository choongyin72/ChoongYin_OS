# Screen: Reservoir Block Formation

- **Type:** OV **junction** (date-effective). Links a Reservoir Block + Reservoir Formation.
- **BF_CODE:** CO.0137 · **Treeview:** Configuration > Assets > Well and Reservoir Objects > Reservoir Block Formation
- **DB view:** `OV_RESV_BLOCK_FORMATION` (key CODE); parents OV_RESV_BLOCK / OV_RESV_FORMATION
- **Last verified:** 2026-07-27 — Playwright multi-object driver 15/15 (DB-verified, self-clean)

## Key mechanic
- `Reservoir Block` + `Reservoir Formation` are **DEPENDENT dropdowns**: Formation options render only AFTER
  a Block is selected. Select Block FIRST, then Formation. Dropdown labels = object **NAME** (e.g. 'Reservoir Block A').
- No valid pair exists in unrelated seed data → **create a fresh Block + Formation, link them, then delete in
  reverse order** (RBF → Formation → Block). See `py/reservoir_block_formation_iud.py`.

## Automation
- **Playwright:** `py/reservoir_block_formation_iud.py` — full multi-object I‑U‑D, 15/15.
- **RF:** `pageobjects/.../reservoir_block_formation_page.resource` + suite — WIP (RF cascade-dropdown timing +
  Navigate-To-Screen superset/subset collision). Driver is the ground truth until RF is fixed.
