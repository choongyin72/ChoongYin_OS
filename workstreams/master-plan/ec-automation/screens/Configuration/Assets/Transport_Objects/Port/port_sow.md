# SOW — Port IUD

## Classification
- **Screen:** Configuration > Assets > Transport Objects > Port (BF_CODE **CO.2003**)
- **Type/pattern:** OV (Manage-Object, `manage_object_nav`) — date-effective; plain (no mandatory dropdowns)
- **DB view:** `OV_PORT` (base `PORT`/versioned); key `CODE`
- **Delete:** End Date = Start Date → row leaves `OV_PORT`

## Nav / grid / cells
- **Open:** menu search "Port" → `label.tv-link`. Navigator = single **Date + GO**; grid needs GO to populate.
- **Grid:** shared T2 `${OV_MANAGE_OBJECT_TABLE}` (= `manage_object_nav_nav:form:T_data`). **Paginated (2 pages)** —
  handled generically by the engine (row_exists walks all pages; select_row navigates to the code's page).
- **NO hardcoded field ids** — fields resolved BY LABEL via T2 `Fill OV * By Label` / `OV Field Id By Label`:
  - **Insert (objectForm):** `Port Code` (mandatory), `Port Name` (mandatory), `Start Date` (mandatory).
    Optional and skipped: End Date, Comments, Country Name (dd), Receiver Rate, Max Tanker Size,
    Canal Restriction Indicator, Canal (dd), Time Zone (dd), Pilot In/Out [hr], Carrier Alloc Priority (dd).
  - **Update (updateAttributes):** `Port Name` (Code read-only; loaded-check via `OV Field Id By Label` on `Port Code`).
  - **Delete (objectdates):** `End Date` = Start Date.

## Test data
- `AUTOTEST_PORT_<timestamp>` unique per run; Start/End = `${TEST_START_DATE}` (2000-01-01). Never touch the
  real ports (ANY_PORT_USA, GAS_NO, MID_*, RBS_*, RHEA_FPSO, TERMINAL_NO, TS1_*, ...).

## Dev story
Recon-first (DB `CLASS_TYPE=OBJECT` ⇒ OV; live form) → plain OV, **no mandatory dropdowns**. First new screen
built **label-driven from the start** (no hardcoded `R:n:C:n` ids anywhere) — so no update-tab id recon was
needed. First headless driver run FAILED the insert grid-check: the row had persisted to `OV_PORT` (DB
confirmed) but wasn't on the rendered grid at check-instant — root cause **async redraw** on a **paginated**
grid. Fixed **generically in the shared engine** (not per-screen): `row_exists` now walks all paginator pages,
`wait_for_row` polls for async appearance then does a full paginated sweep, `select_row` navigates to the page
holding the code. Bank canary re-run 7/7 (backward-compatible). Playwright driver → 7/7; RF T3+suite (label-
driven) → live 4/4. All gates run + auto-ticked by `verify_screen.py` (OVERALL PASS).

## Lessons / known risks
- **Paginated OV grids** (Port = 2 pages): a freshly inserted row can render on a later page or after an async
  redraw — never assert presence on the rendered page alone. The engine now handles this for all OV screens.
- Label-driven T3 removes the need to recon update-tab field ids (labels are stable across objectForm /
  updateAttributes / objectdates on this screen: Port Code / Port Name / Start Date / End Date).
