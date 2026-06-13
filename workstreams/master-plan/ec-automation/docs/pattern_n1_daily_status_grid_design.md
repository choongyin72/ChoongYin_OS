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

## Recon checklist — MUST answer LIVE before coding (the honest unknowns)
1. Does WR.0001 use a **date navigator + GO**, and what are the exact nav field + GO button ids?
2. Is there an additional **object-scope** selector (well/PU/facility) required before the grid loads?
3. Are status rows **pre-populated** for the date (edit-in-place) or must a row be added per well?
4. Exact **grid id** + which columns are editable measured values vs read-only/derived.
5. Exact **`*_DAY_STATUS` table name** + object-FK and production-day column names.
6. Does saving require a **record status** be in P (editable) — i.e. is the day locked by a status
   process (HA.0001)? If month-locked, pick an open day (ties to the P→V→A gate).
7. Does the screen run **inline validation** (Issue_1052 check rules) on save, and does a WARNING
   block the save or just flag? (affects whether the test needs clean data.)

→ These are exactly the facts the existing recon scripts (tmp/scripts/*recon*) are built to harvest;
a single read-only live pass against WR.0001 fills all 7. **Blocked only by sandbox health** (the
scheduler stall doesn't affect screen recon — recon can proceed whenever the app UI is reachable).

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
