*** Settings ***
Documentation       T3 (screen) — "Daily Production Flowline, by Flowline" page object — the N1
...                 generalization to FLOWLINES (6th object class: PWEL/STRM/IWEL/EQPM + flowline).
...                 Screen: EC Production (search) > Daily Production Flowline, by Flowline. Same
...                 edit-in-place N1 daily-status grid (reuses daily_status_grid T2 + DbVerify
...                 day_status helpers verbatim) — DB ground truth = PFLW_DAY_STATUS, key
...                 (OBJECT_ID, DAYTIME). Non-iframed (content in dashboard.jsf?top=false).
...
...                 Divergence from the well screens: the navigator has a DATE RANGE (From G:0 +
...                 To G:1, both set to the same day for a single-day edit) then a 4-level cascade
...                 PU(G:2) → Area(G:3) → Facility(G:4) → Flowline(G:5, leaf). Grid is one flowline's
...                 daily row. C2 = On Strm[hr] = ON_STREAM_HRS (unitless — no UI/DB unit conversion).
...                 Cell is null-original, so the self-clean teardown DB-restores it to NULL (the
...                 IWEL/EQPM model). Name source = OV_FLOWLINE. Recon: tmp/scripts/n1_pflw_*.
...                 Layered: this test → this T3 → daily_status_grid (T2) + common (T1) + DbVerify.

Library             Browser
Library             ../../libraries/DbVerify.py
Resource            ../../resources/daily_status_grid.resource


*** Variables ***
${PFLW_SCREEN}             Daily Production Flowline, by Flowline
${PFLW_GRID}               daily_flowline_status:form:T_data
${PFLW_CELL_PREFIX}        daily_flowline_status:form:T
${PFLW_DB_TABLE}           PFLW_DAY_STATUS
# Navigator: From/To date (G:0/G:1) + cascade PU(G:2) → Area(G:3) → Facility(G:4) → Flowline(G:5).
${PFLW_FROM_DATE_FIELD}    nav:form:G:0:R:1:C:0:da_input
${PFLW_TO_DATE_FIELD}      nav:form:G:1:R:1:C:0:da_input
${NAV_PU}                  nav:form:G:2:R:1:C:0:dd
${NAV_AREA}                nav:form:G:3:R:1:C:0:dd
${NAV_FCTY}                nav:form:G:4:R:1:C:0:dd
${NAV_FLOWLINE}            nav:form:G:5:R:1:C:0:dd
# Working scope (data-bearing: 7 flowlines have P rows on 2003-09-20). Area name has a leading space
# in the DB; Select EC Dropdown Option matches on normalize-space, so "Onshore area" resolves it.
${SCOPE_DATE}              2003-09-20
${SCOPE_PU}                Production Unit
${SCOPE_AREA}              Onshore area
${SCOPE_FCTY}              Onshore facility
${SCOPE_FLOWLINE}          PRD_FLUID_ADFAY_54401
# Target cell + DB column (C2 = On Strm[hr] = ON_STREAM_HRS, DB-proven by the edit→diff in TC02).
${CELL_COLUMN}             C2
${TARGET_DB_COLUMN}        ON_STREAM_HRS
${TARGET_CELL}             ${EMPTY}


*** Keywords ***
Open Flowline Status Screen
    [Documentation]    Suite Setup: launch, login, open the screen, set the From/To date range, walk
    ...    the cascade (PU → Area → Facility → Flowline), GO, then resolve the flowline's row + cache cell.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${PFLW_SCREEN}    ${user}    ${pass}
    Fill EC Date    ${PFLW_FROM_DATE_FIELD}    ${SCOPE_DATE}
    Fill EC Date    ${PFLW_TO_DATE_FIELD}    ${SCOPE_DATE}
    Select EC Dropdown Option    ${NAV_PU}    ${SCOPE_PU}
    Select EC Dropdown Option    ${NAV_AREA}    ${SCOPE_AREA}
    Select EC Dropdown Option    ${NAV_FCTY}    ${SCOPE_FCTY}
    Select EC Dropdown Option    ${NAV_FLOWLINE}    ${SCOPE_FLOWLINE}
    Reload Daily Status Grid
    Reload And Find Target Flowline

Reload And Find Target Flowline
    [Documentation]    Re-apply GO and re-resolve the flowline's row/cell (use after a Save so the next
    ...    edit arms on a freshly-rendered grid). The grid holds one row (the chosen flowline).
    Reload Daily Status Grid
    ${idx}=    Daily Status Row Index For    ${PFLW_GRID}    ${SCOPE_FLOWLINE}
    Should Be True    ${idx} >= 0    msg=Flowline '${SCOPE_FLOWLINE}' not found in the loaded grid
    VAR    ${TARGET_CELL}    ${PFLW_CELL_PREFIX}:${idx}:${CELL_COLUMN}_in    scope=SUITE

Set Flowline Cell
    [Documentation]    Edit the flowline's measured cell to ${value} (real keystrokes + Tab).
    [Arguments]    ${value}
    Edit Daily Status Cell    ${TARGET_CELL}    ${value}

Save Flowline Status
    [Documentation]    Commit the grid edit via the toolbar Save (menubar, execute=@all).
    Save Daily Status

Flowline Cell Should Show
    [Documentation]    Assert the on-screen cell shows ${value} (UI side; pair with the DB check).
    [Arguments]    ${value}
    Daily Status Cell Should Show    ${TARGET_CELL}    ${value}

Flowline Value Should Be In DB
    [Documentation]    Ground truth: assert PFLW_DAY_STATUS.${TARGET_DB_COLUMN} of the (flowline × date)
    ...    row equals ${expected} (ON_STREAM_HRS is unitless — direct equality, no unit conversion).
    [Arguments]    ${expected}
    ${oid}=    Object Id By Name    OV_FLOWLINE    ${SCOPE_FLOWLINE}
    Day Status Value Should Be    ${PFLW_DB_TABLE}    ${oid}    ${SCOPE_DATE}    ${TARGET_DB_COLUMN}    ${expected}

Restore Flowline Cell To Null
    [Documentation]    Self-clean teardown: restore the (flowline × date) cell to NULL at the DB so the
    ...    test leaves the sandbox exactly as found (cell was NULL-original; UI-clear is unreliable).
    ${oid}=    Object Id By Name    OV_FLOWLINE    ${SCOPE_FLOWLINE}
    Reset Day Status Value    ${PFLW_DB_TABLE}    ${oid}    ${SCOPE_DATE}    ${TARGET_DB_COLUMN}
    Flowline Value Should Be In DB    ${None}
