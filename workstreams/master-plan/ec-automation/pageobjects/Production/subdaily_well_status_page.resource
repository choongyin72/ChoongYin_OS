*** Settings ***
Documentation       T3 (screen) — "Sub Daily Production Well Status 1 - by Well" page object — the
...                 N1 SUB-DAILY generalization (intraday intervals). Screen: EC Production (search)
...                 > Sub Daily Production Well Status 1 - by Well. Same edit-in-place N1 mechanics
...                 as the daily well screens (reuses daily_status_grid T2: same `:T:{r}:C{c}_in`
...                 cell pattern + same Save gesture) BUT the DB row is keyed by the full DATETIME:
...                 PWEL_SUB_DAY_STATUS PK = (OBJECT_ID, DAYTIME[+time-of-day], SUMMER_TIME), so each
...                 grid row is one intraday interval, not one object. The grid shows ONE well with
...                 the time down the rows ("Daytime" column), so the target row is resolved by its
...                 Daytime value (an input — scanned by value, not page text), and the DB oracle is
...                 the datetime-keyed `Sub Day Status Value Should Be` (date + HH:MI).
...
...                 Non-iframed. 4-level nav cascade PU → Area → Facility Class 1 → Well (leaf), GO.
...                 Cell C3 = On Strm[hr] = ON_STREAM_HRS (DIFFERENT C-col than the daily screens'
...                 C4 — per-screen edit→diff; here null-original, proven by the edit→Save→DB test).
...                 Null-original cell → self-clean = DB-restore to NULL (like IWEL/EQPM).
...                 Layered: this test → this T3 → daily_status_grid (T2) + common (T1) + DbVerify.
...                 Recon: docs/pattern_n1_daily_status_grid_design.md §Sub-daily; tmp/scripts/n1_subdaily_*.

Library             Browser
Library             ../../libraries/DbVerify.py
Resource            ../../resources/daily_status_grid.resource


*** Variables ***
${SUBDAILY_SCREEN}          Sub Daily Production Well Status 1 - by Well
${SUBDAILY_GRID}            subDailyWellStatusTable:form:T_data
${SUBDAILY_CELL_PREFIX}     subDailyWellStatusTable:form:T
${SUBDAILY_DB_TABLE}        PWEL_SUB_DAY_STATUS
# Navigator cascade groups (nav:form:G:{n}) — PU → Area → Facility Class 1 → Well (leaf).
${NAV_PU}                   G:1
${NAV_AREA}                 G:2
${NAV_FCTY_CLASS_1}         G:3
${NAV_WELL}                 G:4
# Working scope (FRMW framework data; clean hourly set 00:00–23:00, all P, SUMMER_TIME='Y').
${SCOPE_DATE}               2024-10-01
${SCOPE_PU}                 FRMW PU
${SCOPE_AREA}               FRMW Area
${SCOPE_FCTY_CLASS_1}       FRMW Facility 1
${SCOPE_WELL}               FRMW Well 1
# Target interval + the PROVEN-editable cell. C9 = WHP[psig] = DB AVG_WH_PRESS (DB-proven persist
# 2026-06-14: a live edit of C9 committed via the toolbar Save). NB: C3 "On Strm[hr]" did NOT persist
# (derived/non-editable on this grid) — always use a proven cell + edit→diff per screen.
${TARGET_HOUR}              00:00
${CELL_COLUMN}              C9
${TARGET_DB_COLUMN}         AVG_WH_PRESS
${TARGET_CELL}              ${EMPTY}
# Write-test: a distinct WHP DISPLAY value (psi) + the known baseline DB value (bar) for self-clean.
# The grid shows psi, the DB stores bar (factor derived live = UI_before/DB_before ~= 14.5038),
# so the oracle is unit-robust (see reference_ec_ui_db_unit_conversion).
${NEW_WHP_DISP}             3000.00
${WHP_BASELINE_DB}          ${210}


*** Keywords ***
Open Sub Daily Well Status Screen
    [Documentation]    Suite Setup: launch, login, open the screen, set the data-bearing Date, walk
    ...    the nav cascade (PU → Area → Facility Class 1 → Well), GO, then resolve the target
    ...    interval's row by its Daytime and cache its measured-cell id.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${SUBDAILY_SCREEN}    ${user}    ${pass}
    Set Daily Status Date    ${SCOPE_DATE}
    Set Navigator Filter    ${NAV_PU}    ${SCOPE_PU}
    Set Navigator Filter    ${NAV_AREA}    ${SCOPE_AREA}
    Set Navigator Filter    ${NAV_FCTY_CLASS_1}    ${SCOPE_FCTY_CLASS_1}
    Set Navigator Filter    ${NAV_WELL}    ${SCOPE_WELL}
    Reload Daily Status Grid
    Reload And Find Target Interval

Reload And Find Target Interval
    [Documentation]    Re-apply the navigator GO and re-resolve the target interval's row/cell by its
    ...    Daytime value (use after a Save so the next edit arms on a freshly-rendered grid).
    Reload Daily Status Grid
    ${idx}=    Sub Daily Row Index For Daytime    ${SCOPE_DATE} ${TARGET_HOUR}
    Should Be True    ${idx} >= 0
    ...    msg=Interval '${SCOPE_DATE} ${TARGET_HOUR}' not found for well '${SCOPE_WELL}' in the loaded grid
    VAR    ${TARGET_CELL}    ${SUBDAILY_CELL_PREFIX}:${idx}:${CELL_COLUMN}_in    scope=SUITE

Sub Daily Row Index For Daytime
    [Documentation]    Return the 0-based grid row whose "Daytime" cell (the C1 input) holds
    ...    ${daytime_text} (e.g. '2024-10-01 00:00'). The Daytime is an INPUT, so its value is not in
    ...    the row text — scan input values, not textContent. Robust to row re-ordering after a Save.
    ...    Returns -1 if not found.
    [Arguments]    ${daytime_text}
    ${idx}=    Evaluate JavaScript    ${None}
    ...    () => { const tb=document.getElementById('${SUBDAILY_GRID}'); let i=-1; if(tb){ tb.querySelectorAll('tr').forEach((tr,n)=>{ const inp=tr.querySelector('[id$=":C1_in"]'); if(inp && (inp.value||'').trim()==='${daytime_text}') i=n; }); } return i; }
    RETURN    ${idx}

Set Sub Daily Cell
    [Documentation]    Edit the target interval's measured cell to ${value} (real keystrokes + Tab).
    [Arguments]    ${value}
    Edit Daily Status Cell    ${TARGET_CELL}    ${value}

Save Sub Daily Status
    [Documentation]    Commit the grid edit via the toolbar Save (menubar, execute=@all).
    Save Daily Status

Sub Daily Cell Should Show
    [Documentation]    Assert the on-screen cell shows ${value} (UI side; pair with the DB check).
    [Arguments]    ${value}
    Daily Status Cell Should Show    ${TARGET_CELL}    ${value}

WHP Edit Should Persist
    [Documentation]    The sub-daily WRITE oracle (datetime-keyed + unit-robust). Edit the 00:00
    ...    interval's WHP cell (C9) to ${NEW_WHP_DISP} psi, Save, then assert the DB AVG_WH_PRESS
    ...    (bar) persisted. The grid shows psi, the DB stores bar, so derive the factor LIVE from the
    ...    pre-edit UI display ÷ DB value and assert DB_after ≈ typed_display / factor (see
    ...    reference_ec_ui_db_unit_conversion). Proves the edit-in-place WRITE commits for a specific
    ...    intraday interval — the genuinely-new sub-daily capability, end to end.
    ${oid}=    Object Id By Name    WELL_VERSION    ${SCOPE_WELL}
    ${disp0}=    Read Daily Status Cell    ${TARGET_CELL}
    ${db0}=    Sub Day Status Value    ${SUBDAILY_DB_TABLE}    ${oid}    ${SCOPE_DATE}    ${TARGET_HOUR}    ${TARGET_DB_COLUMN}
    Should Be True    ${db0} is not None    msg=No baseline DB value for WHP @ ${SCOPE_DATE} ${TARGET_HOUR}
    Set Sub Daily Cell    ${NEW_WHP_DISP}
    Save Sub Daily Status
    Reload And Find Target Interval
    ${expected}=    Evaluate    float(${NEW_WHP_DISP}) * float(${db0}) / float(${disp0})
    Sub Day Status Value Should Be Approx
    ...    ${SUBDAILY_DB_TABLE}    ${oid}    ${SCOPE_DATE}    ${TARGET_HOUR}    ${TARGET_DB_COLUMN}    ${expected}    ${0.05}

Restore WHP To Baseline
    [Documentation]    Self-clean teardown: DB-restore AVG_WH_PRESS @ the 00:00 interval to its known
    ...    baseline (${WHP_BASELINE_DB} bar) so the test leaves the sandbox exactly as found, then
    ...    verify. Idempotent (no-op if already at baseline). Restores to a KNOWN documented value —
    ...    not an assumption (see feedback_no_destructive_write_on_assumption).
    ${oid}=    Object Id By Name    WELL_VERSION    ${SCOPE_WELL}
    Reset Sub Day Status Value
    ...    ${SUBDAILY_DB_TABLE}    ${oid}    ${SCOPE_DATE}    ${TARGET_HOUR}    ${TARGET_DB_COLUMN}    ${WHP_BASELINE_DB}
    Sub Day Status Value Should Be Approx
    ...    ${SUBDAILY_DB_TABLE}    ${oid}    ${SCOPE_DATE}    ${TARGET_HOUR}    ${TARGET_DB_COLUMN}    ${WHP_BASELINE_DB}    ${0.05}
