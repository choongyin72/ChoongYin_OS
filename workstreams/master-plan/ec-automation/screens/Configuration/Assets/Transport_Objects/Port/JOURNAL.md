# JOURNAL — Port (CO.2003) OV IUD

## 2026-07-26
- **Branch:** `feature/port-iud` off master. Check-existing gate: NONE covered (uncovered target from
  `docs/ov-reuse-targets.md`); reused shared engine + DbVerify + T2, no parallel copy.
- **Recon** (`investigation/recon.py`, read-only): DB `CLASS_TYPE=OBJECT` ⇒ OV; treeview
  Configuration > Assets > Transport Objects > Port. Form: Port Code / Port Name / Start Date mandatory;
  Country/Canal/Time Zone/Carrier dropdowns all **optional** ⇒ no dropdown-fill needed. Grid has real ports
  (never touched).
- **Label-driven from the start** — no hardcoded `R:n:C:n` ids in the T3; fields resolved by label via T2.
  Nice side-effect: no separate update-tab id recon needed (labels stable across the three form tabs).
- **Bug found by the driver (not hidden):** first headless run FAILED insert grid-check — row persisted to
  `OV_PORT` (DB confirmed True) but absent from the rendered grid at check-instant. Root cause = **async
  redraw on a paginated grid** (Port = 2 pages). Probe confirmed the row lands on page 1 alpha-sorted once
  redraw completes.
- **Generic fix in the shared engine** (per owner: "build generic py code to cater most cases"): `row_exists`
  walks all paginator pages + resets to page 1; `wait_for_row` polls the current page then does a full
  paginated sweep; `select_row` navigates to the page holding the code before clicking. Backed up to
  `.keyword_backups/ec_object_iud.py.pre-pagination.bak`. **Bank canary re-run 7/7** (backward-compatible).
  Port driver → **7/7 ALL PASS + self-clean**.
- **RF** T3 + suite (label-driven). `verify_screen.py` → **OVERALL PASS**: robocop 0, hygiene 0, dryrun 4/4,
  **LIVE RF 4/4**, **Playwright 7/7**.

## Lessons
- Paginated OV grids need all-page membership + page navigation on select — now handled once, generically,
  for every OV screen. New rows can render on a later page or only after async redraw; never trust the
  rendered page alone.
- Label-driven T3s are both no-hardcode AND simpler to build (skip update-tab id recon).
