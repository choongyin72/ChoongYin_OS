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

### ⚠️ LIVE RUN (2026-06-13) — read/nav path PROVEN; WRITE path NOT yet working (honest)
Ran the suite live (headless). Result: **TC01 PASS** — the full cascade + GO renders the well rows
LIVE (the navigation + read path is fully proven end-to-end). **TC02/TC03 FAIL — the inline-grid
EDIT does not persist**, and the DB-verify correctly caught it (no false pass). Two real findings:

1. **Save stays DISABLED after an inline edit.** The Save control is `screenToolbar:form:menuB…`
   (`onclick = EC.forceChange();PrimeFaces.ab({s:"screenToolbar:form:menu…"})`), rendered as a
   `ui-state-disabled` menu item. The cell's own `onchange` (`PrimeFaces.ab`) stages a value
   (cell shows `fVal:'21.00'`) but does NOT enable Save; clicking it (or Ctrl+s) does not commit.
   → The edit→commit gesture for this grid is NOT the OV/TV toolbar Save. Unknown to resolve:
   what enables Save here (record must be in an explicit edit mode? a row-level action? the screen
   in a different state? a status-process gate even though RECORD_STATUS='P'?).
2. **cell↔DB-column map is NOT yet established** (CORRECTION of an earlier overconfident claim).
   In a CLEAN session C4=24.00 = PWEL_DAY_STATUS.ON_STREAM_HRS (holds). The other cells I saw
   (644.0/5081.2/2356.5/239.0) did NOT match the DB rate columns (AVG_GL_RATE=791.24,
   AVG_OIL_RATE=4822.64, AVG_GAS_RATE=2186.46, AVG_WATER_RATE=187.82) — BUT that read happened
   while a stale uncommitted edit polluted the view, so it's **inconclusive**, not proof the grid
   is derived. The true full map must be re-derived in a clean session via edit→commit→diff once
   the Save gesture is solved. (Lesson: a single coincidental value match is not a mapping proof.)

**DATA INTEGRITY VERIFIED INTACT + ENVIRONMENT CLEAN:** PWEL_DAY_STATUS has NO column = 21;
ON_STREAM_HRS=24 unchanged. The `21.00` was unsaved JSF conversation view-state from the failed
live run — it **self-cleared** (a later fresh session shows C4=24.00 = DB). Nothing left dangling.

**Next (genuine blocker — needs focused, ideally headed iteration):** crack the inline-grid
edit→commit gesture (what enables `screenToolbar:form:menu…` Save / whether edit-mode or a row
action is required), THEN diff PWEL_DAY_STATUS to establish the true cell↔column map. Until then the
N1 WRITE is unproven — the suite is wired + dryrun-green + nav/read proven, but **not** a passing
live edit. Same difficulty class as the Meter save no-op (took several probes).

### DEEP-DIVE LOG — write-gesture investigation (2026-06-13, ~11 probes, ESCALATED to user)
Confirmed facts:
- Screen URL = `…/daily_well_status/GROUPMODEL/WELL/TARGET/WELL/CLASS_NAME/PWEL_DAY_STATUS` — the
  grid IS bound to PWEL_DAY_STATUS. ON_STREAM_HRS is an editable raw input (grid C4_in); most other
  visible cells (644/5081/2356/239, some duplicated across C15/C76, C23/C71, C26/C75) are
  DERIVED/theoretical/allocated columns (read-only-ish), not raw measured — hence they don't match
  the 5 non-null raw DB values.
- **Save enables only on a REAL change** (editing the cell to a value ≠ its current display).
  Earlier "Save disabled" runs were no-ops: a stale **uncommitted phantom** value kept reloading
  into the grid (server-side JSF conversation state survives across fresh browser sessions until it
  times out), so "editing" to that same value didn't dirty the form. Edit to a UNIQUE sentinel (19)
  → Save enables.
- **But clicking the enabled Save does NOT persist** — DB ON_STREAM_HRS stays 24, REV_NO stays 0,
  and NO column anywhere becomes the sentinel. Ctrl+s also no-op. After the click the Save anchor
  vanishes (menubar re-renders). The toolbar Save (`a[title="Save [Ctrl+s]"]`, a `ui-menuitem-link`
  whose onclick = `EC.forceChange();PrimeFaces.ab({s:"screenToolbar:form:menuBar",…})`) fires but
  the grid edit never reaches the DB.
- Data integrity verified intact throughout; the phantom self-clears on session expiry.
### ✅✅ SOLVED 2026-06-13 — N1 write gesture cracked + DB-PROVEN (both manual & automated)
A headed capture of the USER performing a real save, then an automated replica, both persisted to
`PWEL_DAY_STATUS` (`ON_STREAM_HRS` 24→22 by hand, then automated 22→24 revert — DB-verified both ways).
**The working gesture (now the canonical N1 commit):**
1. **Edit the measured cell with REAL keystrokes + Tab** → fires the cell's `change` behavior
   (`POST … source=daily_well_status:form:T:{r}:C{c}_in  event=change`) which **stages** the value
   server-side. The typed value MUST differ from what's currently shown, or no change event fires.
2. **Click the toolbar Save** (`screenToolbar:form:menuBar`) → `POST … execute=@all` → **commits**.
**Root cause of the earlier 14 failures:** step 1 wasn't happening — `fill()`/synthetic events don't
fire the `change` behavior, and when the value equalled the leftover phantom it was a no-op (nothing
staged), so the Save committed nothing. The framework's `Type Cell By Id` (real Type Text + Tab) DOES
fire it; the suite just needs (a) a clean/true starting value and (b) a sentinel ≠ current.
**Correction:** `AS2_Onshore Well no 2` is **row index 1** (T:1), not 0 (row 0 = Well no 1). Target the
well's row by NAME, don't assume row 0. Validated by `tmp/scripts/wr0001_revert_validate.py`.

**Earlier escalation notes (kept for the record):**
**SME answer (user, 2026-06-13): the toolbar Save IS correct and SHOULD persist** → it's a gesture
bug on the automation side, not a domain/edit-mode/approval issue. Follow-up findings:
- There is exactly ONE Save anchor: `a[title="Save [Ctrl+s]"]`, `ui-menuitem-link`, onclick
  `EC.forceChange();PrimeFaces.ab({s:"screenToolbar:form:menuBar", f:"screenToolbar:form",
  pa:[{name:"…menuBar_menuid", value:"<dynamic>|0"}]})`. It submits the **screenToolbar** form;
  `EC.forceChange()` is meant to flush the dirty grid edit first.
- **Tab IS required**: typing into the cell WITHOUT blurring leaves Save DISABLED — the cell's
  `onchange` (stage + dirty) fires only on blur/Tab. With Tab, Save enables.
- Yet type+Tab→(Save enabled)→click Save still does NOT change PWEL_DAY_STATUS (REV_NO stays 0),
  across fill() AND real-keystroke edits, with/without focus. Edits DO stage server-side (they
  survive as uncommitted "phantom" values across fresh sessions) but never commit via my click.
- The recurring phantom (stale staged value reloading into the grid) confounds headless iteration:
  it makes "edit to X" a no-op whenever the phantom already = X.
**Conclusion / next step (HEADED):** stop headless probing (~14 attempts, diminishing returns).
Capture the exact working save by OBSERVING a real headed save (record the precise gesture/timing,
any focus requirement, any post-save AJAX) — or have the SME demo it once — then encode that in
`Save Daily Status`. The robot suite is otherwise complete (nav/read proven, dryrun-green); only
this commit gesture remains. Scripts: `tmp/scripts/wr0001_write_*.py`, `wr0001_save_*.py`.
DATA INTEGRITY remains verified intact throughout (PWEL_DAY_STATUS unchanged; phantoms self-clear).

### ✅ GENERALIZES — PO.0002 Daily Gas Stream Status (recon 2026-06-13, tmp/scripts/po0002_*)
Confirms the N1 pattern is not a one-off. Same shape, screen-specific ids:
- **Nav cascade is the same, one level SHORTER**: Date → Production Unit → Area → **Facility Class 1**
  (no Well Hookup leaf — streams stop at Facility Class). Same GO `button:form:B`. → T2
  `Set Navigator Filter` + `Apply Navigator` reuse verbatim; the known-good AS2 scope works
  (AS2 EC Exploration Norway / AS2_Onshore Area / AS2_Production Facility no 1).
- **Two grids**: editable **`measured:form:T_data`** (cells `measured:form:T:{r}:C{c}_in`) +
  read-only **`derived:form:T_data`**. (Row 0 = stream `AS2_Flare Gas 001`; cells C7/C8/C9 hold gas
  rates.) So the grid id PREFIX differs (`measured:form` vs `daily_well_status:form`) — the T2
  keywords take the grid_id/cell_id as args, so they drop in.
- **Save gesture: identical** (toolbar Save, menubar @all) — transfers from WR.0001, no re-cracking.
- **Screen URL**: `/com.ec.prod.po.screens/daily_stream_status/CLASS_NAME/STRM_DAY_STREAM_MEAS_GAS/
  CLASS_NAME_DETAIL/STRM_DAY_STREAM_DER_GAS`. The CLASS_NAME is a LOGICAL data class (not a physical
  table — lesson: don't assume class==table here, unlike WR.0001). **Physical table = `STRM_DAY_STREAM`**
  (wide; the `..._MEAS_GAS`/`..._DER_GAS` classes are projections surfaced via `DV_STRM_DAY_STREAM_*`
  views). DB-verify the gas measured column in `STRM_DAY_STREAM` by (OBJECT_ID, DAYTIME).
**Conclusion:** the T2 `daily_status_grid` layer generalizes. A PO.0002 T3 = new ids (measured:form
grid, 3-level cascade, STRM_DAY_STREAM table, a stream object + its gas-rate column) + reuse of every
T2/T1 keyword. Remaining mechanical steps: pin C{c}↔STRM_DAY_STREAM column + the stream OBJECT_ID,
write the thin T3 + suite, live edit→save→DB-verify→revert (same as WR.0001, now de-risked).

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

---

## Sub-daily N1 — a genuinely NEW pattern (recon build-ready, 2026-06-14)
Daily N1 (WR.0001/PO.0002/IWEL/EQPM) keys on **(OBJECT_ID, TRUNC(DAYTIME))** — one row per object
per day. **Sub-daily breaks that**: `PWEL_SUB_DAY_STATUS` has multiple intraday rows per object, so
the daily DB-verify can't uniquely identify a row. Recon (`tmp/scripts/n1_subdaily_recon2.py`,
`n1_subdaily_scope.py`, `n1_subdaily_navdump.py`):

- **PK = (OBJECT_ID, DAYTIME, SUMMER_TIME)** — three columns. `DAYTIME` carries the **time-of-day**
  (hourly grain in the clean data), and `SUMMER_TIME` ('Y'/'N') is the DST discriminator that
  disambiguates the duplicated hour at a fall-back boundary. ⇒ the DB-verify must match the **full
  timestamp** (`DAYTIME = TO_DATE(:dt,'YYYY-MM-DD HH24:MI:SS')`) **AND `SUMMER_TIME`**, not `TRUNC`.
- **Clean test scope:** date **2024-10-01**, PU = **FRMW PU** (G1), wells **FRMW Well 1**
  (`AEBC774296C611E6E053020011ACFDF3`) + **FRMW Well 2** (`...CE11E6...`), each **24 hourly rows**
  00:00→23:00, all `RECORD_STATUS='P'`, `SUMMER_TIME='Y'` (single value — no DST ambiguity that day).
  (2011-01-01 is denser — 461 rows/18 wells — but irregular times; 2024-10-01 is the deterministic
  hourly set to map cells against.)
- **Measured cols** = the well family (ON_STREAM_HRS, AVG_WH_PRESS, AVG_WH_TEMP, …) — same as PWEL.
- **Screen** = "Sub Daily Production Well Status 1 **- by Well**" (the plain name doesn't exist; a
  "- by Period" sibling also exists). Nav = **Date (G0)** + a **5-dropdown cascade G1→G5**;
  **G1 = Production Unit** (confirmed list incl. "FRMW PU"); G2–G5 are empty until G1 is picked
  (dependent cascade, like the daily well screens: PU→Area→FacilityClass1→WellHookup→Well leaf).
  GO = `button:form:B`. Non-iframed (top-level), like IWEL/EQPM.

### Remaining to BUILD (next slice — the only open cracks)
1. **Live-crack the post-GO grid:** pick FRMW PU→cascade→FRMW Well 1, GO; dump the grid id + confirm
   whether **rows = the intraday time intervals** (expected for a "- by Well" view: one well, time
   down the rows) and the cell ids; then **edit→Save→diff** to nail one cell↔(DAYTIME-hour, column)
   — the same edit-in-place save gesture as the daily screens should apply.
2. **Datetime-keyed DbVerify variant:** `sub_day_status_value(table, object_id, datetime, column,
   summer_time='Y')` + `_should_be` + a `reset_sub_day_status_value` teardown — keyed on the full
   timestamp + SUMMER_TIME (the daily helpers' `TRUNC(DAYTIME)` would match 24 rows).
3. **T3 + suite:** likely a thin sub-daily variant of the N1 T2 (rows are time intervals, not
   objects, so the row-index→DAYTIME mapping differs); reuse the save gesture verbatim. Self-clean
   per the IWEL/EQPM model (DB-restore if cells are null-original).

### ✅ BUILT (read-only, live 2/2) + ⛔ WRITE PARKED (2026-06-14)
Built the screen layer and proved the genuinely-new READ mechanic; the edit-in-place WRITE is parked
after ONE failed attempt (stopped — no churn).
- **Grid cracked:** `subDailyWellStatusTable:form:T_data`; rows = intraday intervals for ONE well;
  cells `subDailyWellStatusTable:form:T:{r}:C{c}_in` (same pattern as daily N1). **C0_la = Well Name**
  (constant), **C1 = Daytime** (an INPUT, value like `2024-10-01 00:00`), **C3 = On Strm[hr]**. Resolve
  the target row by scanning each row's C1 input value (Daytime is an input → not in page text).
- **DbVerify datetime helpers** added + self-tested: `sub_day_status_value` / `_should_be` /
  `reset_sub_day_status_value` (keyed by date + HH:MI; `reset` matched exactly 1 row = the key is
  unique). **Shipped read-only suite `sub_daily_well_status_edit.robot`, live 2/2**: TC01 grid loads;
  TC02 distinct hours → distinct rows (proves datetime-keyed navigation, the new pattern).
- ⛔ **WRITE not proven:** a first live edit (On Strm[hr] @ 00:00 → `1`, Tab, toolbar Save) showed `1`
  in the UI cell but **did NOT persist** — `PWEL_SUB_DAY_STATUS.ON_STREAM_HRS` @ 00:00 stayed NULL.
  Unknown: does the toolbar Save commit THIS grid, or is C3 ≠ ON_STREAM_HRS (value routed elsewhere)?
- ⚠️ **Data-safety incident + full recovery (lesson):** a diagnostic that "cleaned residue" wrongly
  assumed the day's cells were null-original and NULLed **real seeded data** (rates/pressures/REV_NO,
  hours 19:00–23:00 of FRMW Well 1). Recovered via **Oracle Flashback** (`AS OF TIMESTAMP
  SYSTIMESTAMP - INTERVAL '25' MINUTE`) → 192 cells restored, 0 mismatches; seeded values (OIL 2500 /
  WHP 210 / GAS 3000) independently re-verified. **Never run a destructive cleanup on an
  assumption — read the FULL pre-existing row first; the sandbox holds real data.** Recovery script:
  `tmp/scripts/n1_subdaily_flashback_restore.py`.
- **Resume (deep-dive or SME, do NOT brute-force):** first deep-dive EC docs / ECpedia on sub-daily
  status data entry + its Save (different commit? mandatory field? edit/lock gate?), THEN reset the
  approach and crack C{c}↔column on a cell that is **already non-null** (edit known-value +1 → diff),
  so a non-persist is unambiguous and no null-assumption cleanup is ever needed. Scripts:
  `tmp/scripts/n1_subdaily_{recon2,scope,navdump,grid_crack,grid_crack2,grid_dump,cellcheck}.py`.

### ✅ WRITE PROVEN (manual, 2026-06-14) — save works; real wrinkle = UI↔DB UNIT CONVERSION
Drive-then-handover live test (I auto-navigated to the 00:00 row; the user edited + saved with their
normal save) **PERSISTED to the DB** → the save gesture works; the screen is NOT write-blocked.
- **Edit:** grid **WHP[psig]** on the 00:00 row `3045.80` → `211`, Save. **DB:** `AVG_WH_PRESS`
  `210` → `14.548`. Reverted to `210` (0 mismatches, sandbox as found; only that 1 col changed).
- 🔑 **UNIT CONVERSION** — the grid shows **psi**, the DB stores **bar**: factor `3045.80/210 =
  14.5038`; `211 psi / 14.5038 = 14.548 bar`. A naive "DB == typed value" oracle FAILS on
  pressure/rate/temp cols (ON_STREAM_HRS is unitless → matched directly on WR.0001 and hid this).
  Re-explains the old "rate cols don't match grid" note: unit conversion, not just derived values.
  See [[reference_ec_ui_db_unit_conversion]].
- **Why my automated TC02 didn't persist (revised):** not a dead screen — manual save commits. Likely
  my automated edit of **On Strm[hr] (C3)** didn't fire EC's change behavior on this grid (toolbar
  Save then committed nothing — same class as the daily-N1 14-fail), or C3 isn't the live
  ON_STREAM_HRS input. Not chased further (no-loop).
- **Finish the automated WRITE (next slice, de-risked):** target a **proven-editable** cell (WHP),
  fire the change reliably (`Type Cell By Id` real keystrokes + Tab; confirm the change POST), verify
  **unit-robustly** (read `factor = UI_display_before / DB_before`; edit UI→V; assert `DB_after ≈ V /
  factor`; revert to exact original). Confirm with user: the EXACT Save control they used (toolbar
  Save vs other) to replicate 1:1. Scripts: `tmp/scripts/n1_subdaily_{baseline,handover,revert}.py`.

### ✅✅ AUTOMATED WRITE SHIPPED — sub-daily N1 COMPLETE, live 3/3 (2026-06-14)
The automated write works and the suite is now full read+write. One informed attempt persisted first
try (`tmp/scripts/n1_subdaily_autowrite.py`): edited the **WHP cell = C9** (`AVG_WH_PRESS`) via real
keystrokes + Tab + toolbar Save (`a[title="Save [Ctrl+s]"]`, the same proven N1 commit) → typed
`3000` psi → DB `206.842` bar (`= 3000 / 14.5038`), reverted to `210`. So my original TC02 fail was
the **wrong cell** (C3 "On Strm[hr]" is derived/non-persisting) — NOT the save gesture, NOT units.
- **Suite** `sub_daily_well_status_edit.robot` now ships **TC03 Edit Intraday WHP Cell And Persist
  (unit-robust)**: reads `disp0`=UI display + `db0`=DB before, edits WHP→`NEW_WHP_DISP`, Saves,
  reloads, asserts `DB_after ≈ NEW_WHP_DISP * db0 / disp0` (factor derived live, no hardcode), via new
  DbVerify `sub_day_status_value_should_be_approx`. Suite Teardown DB-restores AVG_WH_PRESS to the
  known baseline (210 bar). **robocop clean, dryrun 3/3, live 3/3, DB clean after (210), WR.0001
  canary 3/3.** N1 sub-daily = the 5th proven N1 object/grain (PWEL/STRM/IWEL/EQPM + sub-daily) and
  the FIRST with a datetime key + unit-robust write-verify.
