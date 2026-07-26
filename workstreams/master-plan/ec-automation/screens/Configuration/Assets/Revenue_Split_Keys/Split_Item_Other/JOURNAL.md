# JOURNAL - Split Item Other (CD.0017) OV IUD

## 2026-07-26
- **Branch:** `feature/split_item_other-iud` (own branch, stacked so the shared-engine helpers are present).
  Check-existing gate: only this build; reused shared engine + T2 + DbVerify.
- **Recon** (`investigation/recon.py`, read-only): DB `CLASS_TYPE=OBJECT` ⇒ OV; treeview
  Configuration > Assets > Revenue_Split_Keys > Split Item Other. Mandatory Code/Name/Start Date; optional dropdowns skipped.
  Plain Bank-layout OV (single Date+GO nav, no mandatory dropdowns).
- **Label-driven** T3 (no hardcoded ids). Playwright driver -> 7/7; RF T3+suite -> live 4/4.
- `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4, Playwright 7/7.

## Lessons
- Plain OV; generic engine handled appear/absent/pagination with zero screen-specific tuning.
