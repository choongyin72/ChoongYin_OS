# JOURNAL — Berth (CO.2012) OV IUD

## 2026-07-26
- **Branch:** `feature/berth-iud` **stacked on `feature/port-iud`** (depends on PR #203 — needs the shared-engine
  pagination + wait helpers). Check-existing gate: only `py/berth_iud.py` (this build); reused shared engine + T2 + DbVerify.
- **Recon** (`investigation/recon.py`, read-only): DB `CLASS_TYPE=OBJECT` ⇒ OV; treeview
  Configuration > Assets > Transport Objects > Berth (same folder as Port). **Two Port-sibling predictions
  proven WRONG by recon:** (1) grid is **single page** (11 rows, `paginator pages: 0`) — not paginated like Port;
  (2) **Port Name dropdown is OPTIONAL**, not a mandatory reference. ⇒ plain OV, mandatory Code/Name/Start Date only.
- **Label-driven from the start** — no hardcoded `R:n:C:n` ids.
- **Bug found (delete):** Playwright INSERT/UPDATE passed; DELETE first FAILED the grid-absence check while DB
  confirmed the row was gone from `OV_BERTH` (count 0). Root cause = **async grid redraw after delete+GO** (mirror
  of the Port insert-appear timing). **Generic fix:** added engine `wait_for_row_absent` (polls until the row is
  gone from every page). Additive (new symbol; the pagination changes it sits beside were Bank-canary-validated on
  #203). Re-run → **7/7 ALL PASS + self-clean**.
- **RF** T3 + suite (label-driven). `verify_screen.py` → **OVERALL PASS**: robocop 0, hygiene 0, dryrun 4/4,
  **LIVE RF 4/4**, **Playwright 7/7**. (RF's Browser auto-wait already tolerated the delete redraw; only the
  Playwright driver needed the new helper.)

## Lessons
- Folder-siblings are NOT the same screen — recon each (both Port-based predictions were wrong here).
- Delete assertions need absence-polling (`wait_for_row_absent`), not an immediate `not row_exists` — the grid
  redraws async after delete+GO. Now generic for every OV screen.
