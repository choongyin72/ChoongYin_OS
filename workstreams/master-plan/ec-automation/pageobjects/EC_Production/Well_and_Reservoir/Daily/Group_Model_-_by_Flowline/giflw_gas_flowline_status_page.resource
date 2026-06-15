*** Settings ***
Documentation       T3 (screen) — "Daily Gas Injection Flowline, by Flowline" page object — the N1
...                 daily-status grid for GAS-INJECTION flowlines (DB table IFLW_DAY_STATUS, INJ_TYPE='GI').
...                 Screen: EC Production > Well and Reservoir > Daily > Group Model - by Flowline >
...                 Daily Gas Injection Flowline, by Flowline. Sibling of the Water-Injection and
...                 Production flowline screens — verified live 2026-06-15 to share the SAME grid
...                 component (daily_flowline_status:form); reuses daily_status_grid (T2) + DbVerify
...                 verbatim. Only the screen name, scope flowline, and INJ_TYPE differ.
...
...                 ⚠️ UPDATE-ONLY: New/Delete toolbar are DISABLED — the (flowline × day) row is
...                 pre-instantiated by EC batch processes; no record insert/delete on this screen (by
...                 the business-domain nature). The suite EDITs the measured value: set / change / clear
...                 (clear+Save → DB NULL is update-to-null, not a record delete). DB ground truth =
...                 IFLW_DAY_STATUS, key (OBJECT_ID, DAYTIME). Non-iframed.
...
...                 Navigator: DATE RANGE (From G:0 + To G:1, same day) then a 4-level cascade
...                 PU(G:2) → Area(G:3) → Facility(G:4) → Flowline(G:5, leaf). C2 = On Strm[hr] =
...                 ON_STREAM_HRS (unitless, confirmed live). Cell is null-original → DB-restore-null
...                 self-clean. Name source = OV_FLOWLINE. Recon: this bundle's investigation/.
...                 Layered: this test → this T3 → daily_status_grid (T2) + common (T1) + DbVerify.

Library             Browser
Library             ../../../../../libraries/DbVerify.py
Resource            ../../../../../resources/common.resource
Resource            ../../../../../resources/daily_status_grid.resource


*** Variables ***
${GIFLW_SCREEN}            Daily Gas Injection Flowline, by Flowline
${GIFLW_GRID}             daily_flowline_status:form:T_data
${GIFLW_CELL_PREFIX}      daily_flowline_status:form:T
${GIFLW_DB_TABLE}         IFLW_DAY_STATUS
${GIFLW_FROM_DATE_FIELD}   nav:form:G:0:R:1:C:0:da_input
${GIFLW_TO_DATE_FIELD}     nav:form:G:1:R:1:C:0:da_input
${NAV_PU}                 nav:form:G:2:R:1:C:0:dd
${NAV_AREA}               nav:form:G:3:R:1:C:0:dd
${NAV_FCTY}               nav:form:G:4:R:1:C:0:dd
${NAV_FLOWLINE}           nav:form:G:5:R:1:C:0:dd
# Working scope: P1 facility has gas-injection flowlines with P rows on 2019-12-20 (P1 F004/F008/F011 GI).
${SCOPE_DATE}             2019-12-20
${SCOPE_PU}               P1 Production Unit
${SCOPE_AREA}             P1 Area
${SCOPE_FCTY}             P1 Facility 1
${SCOPE_FLOWLINE}         P1 F004 GI
# Target cell + DB column (C2 = On Strm[hr] = ON_STREAM_HRS, confirmed live; same as PFLW/IFLW-water).
${CELL_COLUMN}            C2
${TARGET_DB_COLUMN}       ON_STREAM_HRS
${TARGET_CELL}            ${EMPTY}


*** Keywords ***
Open Gas Injection Flowline Screen
    [Documentation]    Suite Setup: launch, login, open the screen, set the From/To date range, walk
    ...    the cascade (PU → Area → Facility → Flowline), GO, then resolve the flowline's row + cache cell.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${GIFLW_SCREEN}    ${user}    ${pass}
    Fill EC Date    ${GIFLW_FROM_DATE_FIELD}    ${SCOPE_DATE}
    Fill EC Date    ${GIFLW_TO_DATE_FIELD}    ${SCOPE_DATE}
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
    ${idx}=    Daily Status Row Index For    ${GIFLW_GRID}    ${SCOPE_FLOWLINE}
    Should Be True    ${idx} >= 0    msg=Flowline '${SCOPE_FLOWLINE}' not found in the loaded grid
    VAR    ${TARGET_CELL}    ${GIFLW_CELL_PREFIX}:${idx}:${CELL_COLUMN}_in    scope=SUITE

Set Gas Injection Flowline Cell
    [Documentation]    Edit the flowline's measured cell to ${value} (real keystrokes + Tab).
    [Arguments]    ${value}
    Edit Daily Status Cell    ${TARGET_CELL}    ${value}

Save Gas Injection Flowline Status
    [Documentation]    Commit the grid edit via the toolbar Save (menubar, execute=@all).
    Save Daily Status

Gas Injection Flowline Cell Should Show
    [Documentation]    Assert the on-screen cell shows ${value} (UI side; pair with the DB check).
    [Arguments]    ${value}
    Daily Status Cell Should Show    ${TARGET_CELL}    ${value}

Gas Injection Flowline Value Should Be In DB
    [Documentation]    Ground truth: assert IFLW_DAY_STATUS.${TARGET_DB_COLUMN} of the (flowline × date)
    ...    row equals ${expected} (ON_STREAM_HRS is unitless — direct equality, no unit conversion).
    [Arguments]    ${expected}
    ${oid}=    Object Id By Name    OV_FLOWLINE    ${SCOPE_FLOWLINE}
    Day Status Value Should Be    ${GIFLW_DB_TABLE}    ${oid}    ${SCOPE_DATE}    ${TARGET_DB_COLUMN}    ${expected}

Set Gas Flowline Daily Value
    [Documentation]    UPDATE the measured cell to ${value} (set or change — both edits of the
    ...    pre-instantiated row), Save, reload+re-arm. UPDATE-ONLY screen — not a record insert.
    [Arguments]    ${value}
    Set Gas Injection Flowline Cell    ${value}
    Save Gas Injection Flowline Status
    Reload And Find Target Flowline

Clear Gas Flowline Daily Value
    [Documentation]    UPDATE the measured cell to empty (clear + Save → DB column NULL), reload+re-arm.
    ...    Still an UPDATE of the existing row — the record is NOT deleted; used to restore null-original.
    Clear Daily Status Cell    ${TARGET_CELL}
    Save Gas Injection Flowline Status
    Reload And Find Target Flowline

Restore Gas Injection Flowline Cell To Null
    [Documentation]    Self-clean teardown: restore the (flowline × date) cell to NULL at the DB so the
    ...    test leaves the sandbox exactly as found (cell was NULL-original; UI-clear is unreliable here).
    ${oid}=    Object Id By Name    OV_FLOWLINE    ${SCOPE_FLOWLINE}
    Reset Day Status Value    ${GIFLW_DB_TABLE}    ${oid}    ${SCOPE_DATE}    ${TARGET_DB_COLUMN}
    Gas Injection Flowline Value Should Be In DB    ${None}
