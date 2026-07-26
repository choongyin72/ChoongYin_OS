# SOW — Berth IUD

## Classification
- **Screen:** Configuration > Assets > Transport Objects > Berth (BF_CODE **CO.2012**)
- **Type/pattern:** OV (Manage-Object, `manage_object_nav`) — date-effective; plain (no mandatory dropdowns)
- **DB view:** `OV_BERTH` (base `BERTH`/versioned); key `CODE`; 11 real rows (never touched)
- **Delete:** End Date = Start Date → row leaves `OV_BERTH`

## Nav / grid / cells
- **Open:** menu search "Berth" → `label.tv-link`. Navigator = single **Date + GO**; grid needs GO to populate.
- **Grid:** shared T2 `${OV_MANAGE_OBJECT_TABLE}` (= `manage_object_nav_nav:form:T_data`). **Single page** (11 rows,
  no paginator) — unlike its folder-sibling Port (2 pages). Verified by recon, not assumed.
- **NO hardcoded field ids** — fields resolved BY LABEL via T2 `Fill OV * By Label` / `OV Field Id By Label`:
  - **Insert (objectForm):** `Berth Code` (mandatory), `Berth Name` (mandatory), `Start Date` (mandatory).
    Optional and skipped: End Date, Comments, **Port Name (dd)**, Business Unit (dd), Reserved/Design Capacity,
    Capacity Uom (dd), Op Production Unit / Op Area / Op Facility Class 1 (dds).
  - **Update (updateAttributes):** `Berth Name` (Code read-only; loaded-check via `OV Field Id By Label` on `Berth Code`).
  - **Delete (objectdates):** `End Date` = Start Date.

## Test data
- `AUTOTEST_BERTH_<timestamp>` unique per run; Start/End = `${TEST_START_DATE}` (2000-01-01). Never touch the
  real berths (MID_*, RBS_LNG_JETTY_*, TS1_BERTH_*).

## Dev story
Recon-first (DB `CLASS_TYPE=OBJECT` ⇒ OV; live form). **Two predictions from the Port sibling were verified
WRONG by recon** (recon-first paid off): Berth is **single-page** (not paginated like Port) and its **Port Name
dropdown is optional** (not a mandatory reference). So it's a plain OV like Port — mandatory Code/Name/Start
Date only. Built label-driven from the start (no hardcoded ids). Playwright driver → INSERT/UPDATE passed;
DELETE first failed the grid-absence check — DB confirmed the row WAS deleted from `OV_BERTH` (count 0), so the
grid was just mid-async-redraw at check-instant. Fixed generically: added engine `wait_for_row_absent` (polls
until the row is gone from every page; mirror of `wait_for_row`). Re-run → 7/7. RF T3+suite (label-driven) →
live 4/4 (RF's Browser auto-wait already handled the delete redraw; only the Playwright driver needed the new
helper). All gates run + auto-ticked by `verify_screen.py` (OVERALL PASS).

## Lessons / known risks
- **Don't assume folder-siblings match** — Port (paginated, its own optional dds) vs Berth (single page,
  optional Port-ref dd). Recon each; both predictions were wrong here.
- **Delete needs absence-polling too** — after delete+GO the grid redraws async; assert with
  `wait_for_row_absent`, never an immediate `not row_exists`. Now generic in the shared engine.
