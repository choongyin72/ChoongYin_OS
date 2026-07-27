# SOW — Reservoir Block Formation IUD (CO.0137) — MULTI-OBJECT

## Classification
- **Screen:** Configuration > Assets > Well and Reservoir Objects > Reservoir Block Formation (CO.0137)
- **Type:** OV **junction** object. `Reservoir Block` + `Reservoir Formation` are **dependent dropdowns** —
  the Formation options only render **after** a Block is selected. A valid pair cannot be picked from
  unrelated seed data (picking first-of-each = invalid combo → silent Save reject).
- **DB view:** `OV_RESV_BLOCK_FORMATION` (key `CODE`); parents `OV_RESV_BLOCK`, `OV_RESV_FORMATION`.
- **Delete:** End Date = Start Date (each of the 3 objects).

## The flow (owner-specified, verified)
Create a fresh **Reservoir Block** → create a fresh **Reservoir Formation** → on RBF, select the new Block
(which populates the Formation dropdown) → select the new Formation → I‑U‑D the RBF → tear down in **reverse
dependency order**: RBF → Formation → Block. All DB-verified; sandbox left clean.

## Status
- **Playwright driver `py/reservoir_block_formation_iud.py` — PASS, 15/15 steps, DB-verified, 0 residual.**
  This is the definitive proof the full multi-object I‑U‑D works (create both parents, link, update, delete
  all three in reverse order). Dropdowns referenced BY NAME; Block selected before Formation so the cascade
  populates (engine `select_dropdown`).
- **RF suite `tests/.../reservoir_block_formation_iud.robot` — WIP** (2 RF-framework edges, not IUD-logic):
  1. **TC02** — RF's `Select EC Dropdown Option` on the dependent **Reservoir Formation** dropdown times out
     (cascade options don't render fast enough via the RF gesture, though they do in the Playwright driver).
  2. **TC05** — `Navigate To Screen "Reservoir Formation"` fails when navigating **from "Reservoir Block
     Formation"** (tv-link superset→subset collision).
  robocop clean, `--dryrun` 5/5. Live = 1/5 pending the two fixes above.

## Verify
`verify_screen.py`: robocop 0 · hygiene 0 · dryrun 5/5 · **Playwright driver ALL PASS** · RF live WIP (1/5).
The multi-object driver is the ground-truth proof; the RF suite is a follow-up.

## Lessons / known risks
- Junction OV screens need a **multi-object** driver (create parents → link → reverse teardown), not the
  single-screen generic pattern. Dependent dropdowns: fill parent first, child populates.
- RF `Navigate To Screen` has a **superset/subset tv-link collision** (RBF → Reservoir Formation/Block);
  needs an exact-match nav fix before the multi-object RF suite is green.
