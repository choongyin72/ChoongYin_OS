# Pattern N1 — Daily/Monthly Status Data-Entry Grid (T2 design, 2026-06-13)
The biggest, highest-value coverage gap (see coverage_pluto_prioritized.md §N1). All current T2
patterns (manage_object, table_class) handle **master-data IUD**. The Pluto operational core is
**transactional status entry**: for a chosen DATE + object scope, type measured values into an
editable grid, save, and the data lands in a `*_DAY_STATUS` table. This doc specs the T2 pattern
**from knowledge already held** (id grammar, As-Built 02 catalog, capstone data-flow) so the
eventual build is "fill in the recon blanks," not a cold start. It is explicit about what MUST be
confirmed live before coding.

## Representative screen (build first)
**WR.0001 Daily Production Well Status (PLU)** — rich, central, PHD-fed, ties to Issue_1052
validations. Once proven, generalize to PO.0002 Daily Gas Stream Status (different object, same
shape) to confirm the pattern holds.

## How N1 differs from the IUD patterns (the conceptual shift)
| Aspect | OV / TV (have) | N1 daily-status (new) |
|---|---|---|
| Unit of work | an object (Code/Name) | an (object × date) measurement row |
| Navigator | BU/parent dd + GO | **date** (+ object scope) + GO |
| "Insert" | New Object Form → save | row usually **pre-exists per object/day**; you EDIT measured-value cells |
| "Delete" | End Date = Start Date / physical | usually N/A (you blank/zero a value, or a status process locks it) |
| DB oracle | OV_*/base table by code | `*_DAY_STATUS` by (object_id, production_day) |
| Validation | CSDV on save | + downstream check rules (Validation Overview / Issue_1052) |

→ N1 is closer to **table_class inline-edit** than manage_object, but keyed by a DATE navigator and
with no row create/delete. Reuse table_class cell-edit gestures; add a date-navigator front end.

## Expected JSF id grammar (from ec_webapp_internals.md — CONFIRM LIVE)
- **Date navigator**: `nav:form:...:da_input` (a `_da_input` date field) + **GO** `navButton:form:B`
  or `button:form:B`. Some screens have object-scope dds alongside the date (well/stream/facility).
- **Grid**: `<grid>:form:T_data` tbody; rows `...:T:{r}:...`; measured-value cells are
  `...:C{col}_in` (numeric) or `...:C{col}:dd` (status dd) or `...:C{col}_da_input` (time).
- **Row label**: `...:R:{r}:C:0:la` (or the object name in C0) → recon labels first; the measured
  quantities (rate, pressure, temp, on-hours) each occupy a column.
- **Save**: toolbar `a[title="Save [Ctrl+s]"]` (same as everywhere) → async → **poll DB**.

## Proposed T2 keywords (new file: resources/daily_status_grid.resource)
Thin, built on existing T1 (common/table/toolbar) + the cell gestures:
```
Open Status Screen For Date
    [Arguments]    ${screen}    ${production_date}    ${scope}=${EMPTY}    ${user}=...    ${pass}=...
    Launch EC And Open Screen    ${screen}    ${user}    ${pass}
    Fill EC Date    ${NAV_DATE}    ${production_date}
    Run Keyword If    '${scope}'!='${EMPTY}'    Select EC Dropdown Option    ${NAV_SCOPE}    ${scope}
    Apply Navigator      # GO — mandatory; reloads the grid for that date

Set Day Status Value
    [Arguments]    ${grid}    ${row_key}    ${col_id_suffix}    ${value}
    # locate row by object name/key in C0, then fill the measured-value cell + change/blur (stage for Save)
    ${row}=    Resolve Row Index    ${grid}    ${row_key}
    Fill EC Field    ${grid}:${row}:${col_id_suffix}    ${value}

Save Day Status
    Save Object        # toolbar Save when enabled; async

Day Status Value Should Be In DB
    [Arguments]    ${table}    ${object_id}    ${production_day}    ${column}    ${expected}
    # DB ground-truth — the ONLY trustworthy oracle (UI optimistic-state lesson)
    Value In Day Status Should Equal    ${table}    ${object_id}    ${production_day}    ${column}    ${expected}
```
(DbVerify.py gains one helper: `value_in_day_status(table, object_id, day, column)` returning the
stored measured value for assertion — mirrors the existing `code_is_present_in_view`.)

## DB oracle (CONFIRM table + key columns live)
Wells daily status → likely **`PWEL_DAY_STATUS`** (or `WELL_DAY_STATUS`); gas stream → `STRM_DAY_STATUS`.
Key = (object FK, `PRODUCTION_DAY`/`PROD_DAY` date). Measured columns map to grid columns
(rate, pressure, temp, on-stream hours). Verify exact names with a SELECT against the sandbox before
asserting — do NOT assume (no-assumptions rule).

## Recon checklist — LIVE results (2026-06-13, tmp/scripts/wr0001_go_probe.py)
Screen opened = **"Daily Production Well Status 1"** (3rd search hit; siblings: Flowline+Well,
Well Hookup+Well, Status 1/2/3, Sub-Daily variants). Content renders in an **iframe**
(url `/com.ec.prod.wr.screens/daily_well_status/GROUPMODEL/WELL/TARGET/WELL/...`) — a
**GROUPMODEL screen, object = WELL**. The recon must traverse `page.frames` (top doc is empty).

1. ✅ **Date navigator + GO confirmed.** Date = `nav:form:G:0:R:1:C:0:da_input` (defaults to ~today,
   2026-06-12). **GO = `button:form:B`** (title "Go [Ctrl+g]") — *inside the content iframe*.
2. ✅ **Mandatory scope cascade** (nav groups, all `nav:form:G:{n}:R:1:C:0:dd_input`):
   G1 **Production Unit** · G2 **Area** · G3 **Facility Class 1** · G4 **Well Hookup**.
   GO with only Date+PU → error growl: *"Required fields are empty. Please enter data for at least
   one of these fields: Well Hookup [WELL_HOOKUP] or Facility Class 1 [FCTY_CLASS_1]."*
   → **Required nav = Date + Production Unit + (Well Hookup OR Facility Class 1)**; Area optional.
3. ⛔ **BLOCKED (sandbox data).** Could not capture grid row behaviour: for `P1 Production Unit` @
   2026-06-12 the Facility Class 1 + Well Hookup dds return **0 options** — this generic corp
   sandbox (ap-f0a7g341jn6d) has no WELL/well-hookup master data under that PU/date, so the grid
   never populates. Need a PU+date that actually has wells (DB query below to find one).
4. ⛔ **BLOCKED (same cause).** Grid id + editable columns un-captured until #3 resolved. Expected
   per id grammar: `<grid>:form:T_data` with measured-value cells `...:T:{r}:C{c}_in`.
5. ☐ **DB table** — query next (authoritative); look for `*_DAY_STATUS` / well-day-status table.
6. ✅ **Record-status governance present on-screen.** Bottom tabset = **RECORD STATUS / REVISION
   INFO / APPROVAL STATUS / HINTS & TIPS / VALIDATION / TRENDING / ATTACHMENTS**; status dd
   `statusarea_tab:tabPanel:_sa_recordstatus:form:G:0:R:1:C:6:dd_input` + Created/Last-updated/
   Record-status/Revision fields. → P→V→A is enforced here (matches HA.0001 status process).
7. ✅ **Inline VALIDATION tab present** (the tabset above) → the screen surfaces check-rule results
   (Issue_1052 family) in-context. Save-blocking vs warn-only still to confirm with data.

## DB ground truth (2026-06-13, tmp/scripts/wr0001_db_probe*.py — localhost:1521/ORCL)
Answered #3 and #5 below the UI (authoritative):
- **Table = `PWEL_DAY_STATUS`** (well grain) + **`WELL_HOOKUP_DAY_STATUS`** (well-hookup grain;
  the nav requires Well Hookup OR Facility Class 1, so this screen writes one/both). `*_JN` = journal.
  Views: `DV_PWEL_DAY_STATUS`, `DV_FRMW_PWEL_DAY_STATUS`. Sibling screens → `PFLW_DAY_STATUS`
  (flowline), `IWEL_DAY_STATUS` (injection well).
- **Key = (`OBJECT_ID` VARCHAR2 = the well, `DAYTIME` DATE = the production day).** ✅ #5.
- **`RECORD_STATUS` + `APPROVAL_STATE` live ON the status row** (not just a header) — confirms the
  P→V→A governance is per-(well,day). Sample rows all `RECORD_STATUS='P'`. ✅ #6 at DB level.
- **Rows are PRE-INSTANTIATED** ✅ #3: every sampled row has `REV_TEXT='Created by instantiation'`
  and NULL measured values → the daily-status row exists per (well × day) before any entry; **the
  screen EDITS an existing row, it never inserts/deletes one.** This is the core N1 semantic:
  *no New-Object / no Delete — only cell-edit + Save on a pre-existing row.*
- **Measured columns** (the editable grid cells): ON_STREAM_HRS, AVG_BH_PRESS/TEMP, AVG_GL_* (gas
  lift), AVG_CHOKE_SIZE, AVG_FLOW_LINE_PRESS, AVG_WH_PRESS/TEMP (wellhead), AVG_OIL/GAS/COND/
  WATER_RATE + densities + masses, THEOR_* (theoretical/back-allocated), MPM_*/VFM_* (multiphase/
  virtual-flow meters), plus generic VALUE_1..50 / TEXT_1..25 / DATE_1..5 extension slots and a
  COMMENTS field. WELL_HOOKUP_DAY_STATUS is leaner (VALUE_1..10 / TEXT_1..10 / DATE_1..5).
- Volume: PWEL_DAY_STATUS = 84,914 rows; WELL_HOOKUP_DAY_STATUS = 6,137. So data EXISTS — just not
  under `P1 Production Unit` for 2026-06-12. The data-bearing wells sit under other PUs (OBJECT_IDs
  are opaque hashes; one join well→facility-class→PU finds a usable scope).

### Revised N1 T2 semantics (corrected by DB findings)
The pattern is **edit-in-place on a pre-instantiated (object × day) row**, NOT IUD:
- `Open Status Screen For Date` → set Date + PU + (Well Hookup | Facility Class 1) → GO.
- `Set Day Status Value` → locate the well's row → fill a measured-value cell (`_in`) + change/blur.
- `Save Day Status` → toolbar Save → async.
- `Day Status Value Should Be In DB` → `SELECT <col> FROM PWEL_DAY_STATUS WHERE OBJECT_ID=:w AND
  TRUNC(DAYTIME)=:d`. (No row-count delta oracle — the row pre-exists; assert the VALUE changed.)
- Pick a day with `RECORD_STATUS='P'` (editable); a V/A day is locked (negative test candidate).

### Remaining blockers → next actions (alternative angles)
- Find a **data-bearing PU/date** (DB: which PU has WELL_HOOKUP/FCTY_CLASS_1 objects + day-status
  rows) → re-run probe with that scope to capture grid id + editable cell ids (#3, #4).
- Confirm exact **day-status table + key columns** via DB (#5).
- This is the EC generic sandbox, not Pluto — well data is sparse; a Pluto-data env or seeding a
  test well would unblock the grid capture. Documented; not a structural blocker (nav fully mapped).

## Build sequence (when sandbox reachable)
1. Read-only recon pass → answer the 7 questions → fill the id variables.
2. Write `daily_status_grid.resource` (T2) + `DbVerify.value_in_day_status` (T1 helper).
3. Build `wr0001_daily_well_status_page.resource` (T3, thin: ids + one-line delegations).
4. Dryrun → live edit one well's rate for an OPEN day → **DB-verify** the stored value → revert.
5. Add PO.0002 Daily Gas Stream Status reusing the T2 → proves the pattern generalizes (registry +
   coverage backlog updated).

## Why this is the right next bet
N1 unlocks the **most Pluto business tests** — it's where PHD data lands, where Issue_1052
validations fire, and the input to the whole allocation chain (capstone). Master-data IUD is largely
done; transactional status entry is the untouched core. This design turns the build into recon +
mechanical assembly.
