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
2. ✅ **Scope is a 4-level CASCADE** (nav groups, all `nav:form:G:{n}:R:1:C:0:dd_input`):
   G1 **Production Unit** → G2 **Area** → G3 **Facility Class 1** → G4 **Well Hookup**.
   Each level filters the next (Area options come from PU; FC1 from Area; Well Hookup from FC1).
   The "Well Hookup OR Facility Class 1" required-field growl is satisfied by FC1, BUT the grid
   stays empty until you drill all the way to **Well Hookup** (the leaf that resolves to wells).
   → **To get rows: Date + PU + Area + Facility Class 1 + Well Hookup, then GO.**
   ⚠️ **Earlier false-zero lesson:** scanning FC1/WH right after picking PU shows 0 options — they
   cascade from **Area**, not PU. Always walk the cascade in order.
3. ✅ **Rows are PRE-INSTANTIATED, edit-in-place** (confirmed UI + DB). With full scope @ 2003-01-01
   the grid showed 2 well rows (the wells under AS2_Lift Gas Manifold 1), each an existing
   (well × day) row to edit — no New-Object / no Delete.
4. ✅ **Grid id = `daily_well_status:form:T_data`** (tbody). **Editable cells =
   `daily_well_status:form:T:{row}:C{col}_in`** (numeric text) with `...:C{col}_dd_input` where a
   column is a dropdown (e.g. C3). Columns C2..C26+ are measured-value `_in` inputs. Grouped
   headers: Well · Choke · Well Head · Downhole · Gas lift · USC · Measured Rates · Scale-inhibitor ·
   Multiphase Meter (+mass rates) · Sub-Daily Theoretical · External Calc Theor 1-4 · Theoretical
   Calculated · Override Theoretical · Allocated Results · ESP · Name. (Matches predicted grammar.)
5. ✅ **DB table = `PWEL_DAY_STATUS`** (+ `WELL_HOOKUP_DAY_STATUS`) — see DB section below.
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

### ✅ RECON COMPLETE — all 7 unknowns answered (2026-06-13)
**Working test scope** (generic sandbox `ap-f0a7g341jn6d`, seed epoch): Date **2003-01-01** →
PU **AS2 EC Exploration Norway** → Area **AS2_Onshore Area** → Facility Class 1 **AS2_Production
Facility no 1** → Well Hookup **AS2_Lift Gas Manifold 1** → GO → grid shows 2 well rows
(`daily_well_status:form:T:0:*` / `:T:1:*`). Date MUST be data-bearing — 2003-01-xx has 113 filled
wells (confirms the **object-start-date = version-filter** rule; the default ~today shows nothing).
Recon scripts: `tmp/scripts/wr0001_{status_recon,go_probe,find_scope,find_date,trace_well,
trace_group,area_cascade}.py` + `wr0001_db_probe{,2}.py`.

**BUILD DONE (dryrun-green) — one live step remains.** Delivered:
- T1 `DbVerify` helpers (self-tested, commit 4b8e96f): `well_object_id_by_name`, `day_status_value`,
  `day_status_value_should_be`.
- T2 `resources/daily_status_grid.resource` — the reusable N1 layer (Set Daily Status Date /
  Reload / Edit Daily Status Cell / Daily Status Cell Should Show / Save / DB assert). Thin: built
  on existing T1 (navigator/table `Type Cell By Id`/toolbar).
- T3 `pageobjects/Production/wr0001_daily_well_status_page.resource` — ids + working scope + cascade.
- Suite `tests/Production/daily_well_status_edit.robot` — self-reverting edit-in-place test
  (read original → edit → Save → UI + DB verify → revert). **Robocop clean, `--dryrun` PASS 3/3**;
  re-dryran nomination_cycle (a DbVerify consumer) PASS — the helper append broke nothing.

**Remaining = the live run (best headed, per run-robot-headed):** on first live execution, pin two
recon-default values in the T3: `${ROW0_WELL_NAME}` (grid row-0 well display name) and the
`${ROW0_CELL}`↔`${ROW0_DB_COLUMN}` pairing (edit the cell → Save → diff PWEL_DAY_STATUS to see which
column changed). Then the suite proves the N1 pattern end-to-end and generalizes to PO.0002 etc.

### ✅ Frame handling: NONE needed — screen is the MAIN frame (settled 2026-06-13)
Initial worry of a nested iframe was a Playwright frame-detachment artifact. **Decisive test
(`tmp/scripts/wr0001_toplevel_test.py`): the screen frame IS `page.main_frame`** — opening the
screen NAVIGATES the main content frame to `/com.ec.prod.wr.screens/daily_well_status/...`, and the
app shell (search/toolbar) re-renders in that same document. A **top-level** locator
`[id="nav:form:G:0:R:1:C:0:da_input"]` returns count=1 (so does the grid `daily_well_status:form:*`).
→ **N1 is reachable exactly like every other screen — no `>>>` piercing for the screen itself**
(only popups still use `popupIFrame`). No new framework capability required; existing T1 keywords
(`Launch EC And Open Screen`, `Select EC Dropdown Option`, `Fill EC Field`, `Apply Navigator`/GO)
apply directly. The build is straightforward.

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
