# JOURNAL — Reservoir Block Formation (CO.0137) — MULTI-OBJECT

## 2026-07-27
- **Junction OV.** Reservoir Block + Reservoir Formation are dependent dropdowns (Formation populates only
  after a Block is selected). First attempt (generic single-screen build, first-of-each dropdowns) → insert
  SILENTLY rejected (invalid pair). Owner's flow: create both parents fresh, then link via RBF.
- **Playwright multi-object driver** `py/reservoir_block_formation_iud.py` → **15/15 PASS**: create Block,
  create Formation, insert RBF (Block-then-Formation so cascade populates), update RBF, delete RBF→Formation→
  Block (reverse dependency order). DB-verified each; self-clean 0 residual across all 3 views. Definitive proof.
- **RF suite** (T3 + 5-TC) → robocop clean, dryrun 5/5, **live 1/5 (WIP)**: TC02 RF `Select` on the dependent
  Formation dropdown times out (cascade render timing); TC05 `Navigate To Screen` RBF→Reservoir Formation
  superset/subset tv-link collision. Both are RF-gesture edges, not IUD-logic (the driver does the same flow OK).

## Lessons
- Junction screens = multi-object driver (create parents → link → reverse teardown); dependent dropdowns fill
  parent-first. RF `Navigate To Screen` needs an exact-match fix for superset/subset screen names.
