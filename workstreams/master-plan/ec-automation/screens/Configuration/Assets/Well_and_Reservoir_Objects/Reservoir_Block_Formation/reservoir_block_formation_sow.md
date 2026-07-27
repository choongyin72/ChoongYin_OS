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
- **RF suite `tests/.../reservoir_block_formation_iud.robot` — PASS, 5/5 live, DB-verified, 0 residual**
  (issue #237 item 4, closed). Three distinct root causes found + fixed:
  1. **Framework-wide stuck-modal bug**: EC's own "Unsaved Changes" dialog, left open by any earlier
     mid-fill failure, has no handler in `Navigate To Screen` — its overlay mask then blocks every click
     for the rest of the run. Fixed via `Dismiss Unsaved Changes Dialog If Present` (button id verified by
     DOM probe: `confirmationForm:nobtn`), wired into `resources/screen.resource`. Protects every RF suite,
     not just RBF.
  2. **TC02** was NOT a cascade-timing race: the dependent Reservoir Formation dropdown's rendered
     `data-item-label` holds the **CODE**, not the Name (verified via DOM probe) — unlike the Block
     dropdown, which matches by Name. Fixed by passing the Formation code instead of name.
  3. **TC05** was an async render race in EC's own search-results list (the superset match "Reservoir
     Block Formation" can render before the exact "Reservoir Formation" match does). Fixed by waiting for
     the exact target tv-link to be visible before clicking, instead of a fixed sleep.
  robocop clean, `--dryrun` 5/5, LIVE 5/5.

## Verify
`verify_screen.py`: robocop 0 · hygiene 0 · dryrun 5/5 · **Playwright driver ALL PASS (15/15)** · **RF live 5/5 PASS**.
OVERALL: PASS.

## Lessons / known risks
- Junction OV screens need a **multi-object** driver (create parents → link → reverse teardown), not the
  single-screen generic pattern. Dependent dropdowns: fill parent first, child populates.
- Not every dependent-dropdown cascade keys its options the same way — verify the real `data-item-label`
  attribute via DOM probe rather than assuming Name; this screen's Formation cascade uses Code.
- EC's own client-side "Unsaved Changes" dialog can silently stall an ENTIRE suite (not just one test) if
  left unhandled after any mid-fill failure — the fix lives at the shared T1 nav layer, not per-screen.
