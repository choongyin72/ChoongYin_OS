*** Settings ***
Documentation       T3 (screen) — "Daily Water Injection Flowline, by Flowline" page object — the N1
...                 generalization to WATER-INJECTION flowlines (DB table IFLW_DAY_STATUS).
...                 Screen: EC Production > ... > Daily > Group Model - by Flowline > Daily Water
...                 Injection Flowline, by Flowline. Direct sibling of "Daily Production Flowline, by
...                 Flowline" (PFLW) — verified live 2026-06-15 to share the SAME grid component
...                 (daily_flowline_status:form), so it reuses daily_status_grid (T2) + DbVerify
...                 verbatim; only the screen name, scope, and DB table (IFLW_DAY_STATUS) differ.
...
...                 Edit-in-place N1 daily-status grid — DB ground truth = IFLW_DAY_STATUS, key
...                 (OBJECT_ID, DAYTIME). Non-iframed (content in dashboard.jsf?top=false).
...
...                 Navigator: DATE RANGE (From G:0 + To G:1, same day) then a 4-level cascade
...                 PU(G:2) → Area(G:3) → Facility(G:4) → Flowline(G:5, leaf). Grid is one flowline's
...                 daily row. C2 = On Strm[hr] = ON_STREAM_HRS (unitless — no UI/DB unit conversion),
...                 confirmed live 2026-06-15 (same column as PFLW). Cell is null-original, so the
...                 self-clean teardown DB-restores it to NULL (the IWEL/EQPM/PFLW model). Name source =
...                 OV_FLOWLINE. Recon: this screen's bundle investigation/ (screens/EC_Production/…).
...                 Layered: this test → this T3 → daily_status_grid (T2) + common (T1) + DbVerify.

Library             Browser
Library             ../../../../../libraries/DbVerify.py
Resource            ../../../../../resources/common.resource
Resource            ../../../../../resources/daily_status_grid.resource


*** Variables ***
${IFLW_SCREEN}             Daily Water Injection Flowline, by Flowline
${IFLW_GRID}               daily_flowline_status:form:T_data
${IFLW_CELL_PREFIX}        daily_flowline_status:form:T
${IFLW_DB_TABLE}           IFLW_DAY_STATUS
# Navigator: From/To date (G:0/G:1) + cascade PU(G:2) → Area(G:3) → Facility(G:4) → Flowline(G:5).
${IFLW_FROM_DATE_FIELD}    nav:form:G:0:R:1:C:0:da_input
${IFLW_TO_DATE_FIELD}      nav:form:G:1:R:1:C:0:da_input
${NAV_PU}                  nav:form:G:2:R:1:C:0:dd
${NAV_AREA}                nav:form:G:3:R:1:C:0:dd
${NAV_FCTY}                nav:form:G:4:R:1:C:0:dd
${NAV_FLOWLINE}            nav:form:G:5:R:1:C:0:dd
# Working scope: the P1 facility has water-injection flowlines with P rows on 2019-12-20 (9 WI
# flowlines that day). "P1 F003 WI" (OV_FLOWLINE NAME; CODE "P1 F003") is the data-bearing leaf.
# NOTE: there is also a dataless "P1 0600 F003 WI" under "P1 Facility 0600" — use Facility 1 + the
# exact name "P1 F003 WI" (the row with the IFLW_DAY_STATUS data).
${SCOPE_DATE}              2019-12-20
${SCOPE_PU}                P1 Production Unit
${SCOPE_AREA}              P1 Area
${SCOPE_FCTY}              P1 Facility 1
${SCOPE_FLOWLINE}          P1 F003 WI
# Target cell + DB column (C2 = On Strm[hr] = ON_STREAM_HRS, confirmed live; same as PFLW).
${CELL_COLUMN}             C2
${TARGET_DB_COLUMN}        ON_STREAM_HRS
${TARGET_CELL}             ${EMPTY}


*** Keywords ***
Open Water Injection Flowline Screen
    [Documentation]    Suite Setup: launch, login, open the screen, set the From/To date range, walk
    ...    the cascade (PU → Area → Facility → Flowline), GO, then resolve the flowline's row + cache cell.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${IFLW_SCREEN}    ${user}    ${pass}
    Fill EC Date    ${IFLW_FROM_DATE_FIELD}    ${SCOPE_DATE}
    Fill EC Date    ${IFLW_TO_DATE_FIELD}    ${SCOPE_DATE}
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
    ${idx}=    Daily Status Row Index For    ${IFLW_GRID}    ${SCOPE_FLOWLINE}
    Should Be True    ${idx} >= 0    msg=Flowline '${SCOPE_FLOWLINE}' not found in the loaded grid
    VAR    ${TARGET_CELL}    ${IFLW_CELL_PREFIX}:${idx}:${CELL_COLUMN}_in    scope=SUITE

Set Water Injection Flowline Cell
    [Documentation]    Edit the flowline's measured cell to ${value} (real keystrokes + Tab).
    [Arguments]    ${value}
    Edit Daily Status Cell    ${TARGET_CELL}    ${value}

Save Water Injection Flowline Status
    [Documentation]    Commit the grid edit via the toolbar Save (menubar, execute=@all).
    Save Daily Status

Insert Flowline Daily Value
    [Documentation]    INSERT — populate the (empty) measured cell with ${value}, Save, reload+re-arm.
    ...    On this daily grid the row is pre-instantiated; "insert" fills the empty value (DB null→value).
    [Arguments]    ${value}
    Set Water Injection Flowline Cell    ${value}
    Save Water Injection Flowline Status
    Reload And Find Target Flowline

Update Flowline Daily Value
    [Documentation]    UPDATE — change the measured cell to ${value}, Save, reload+re-arm (DB value→value).
    [Arguments]    ${value}
    Set Water Injection Flowline Cell    ${value}
    Save Water Injection Flowline Status
    Reload And Find Target Flowline

Delete Flowline Daily Value
    [Documentation]    DELETE — clear the measured cell, Save, reload+re-arm. Nulls the DB column
    ...    (DB value→null), i.e. the daily value is removed.
    Clear Daily Status Cell    ${TARGET_CELL}
    Save Water Injection Flowline Status
    Reload And Find Target Flowline

Water Injection Flowline Cell Should Show
    [Documentation]    Assert the on-screen cell shows ${value} (UI side; pair with the DB check).
    [Arguments]    ${value}
    Daily Status Cell Should Show    ${TARGET_CELL}    ${value}

Water Injection Flowline Value Should Be In DB
    [Documentation]    Ground truth: assert IFLW_DAY_STATUS.${TARGET_DB_COLUMN} of the (flowline × date)
    ...    row equals ${expected} (ON_STREAM_HRS is unitless — direct equality, no unit conversion).
    [Arguments]    ${expected}
    ${oid}=    Object Id By Name    OV_FLOWLINE    ${SCOPE_FLOWLINE}
    Day Status Value Should Be    ${IFLW_DB_TABLE}    ${oid}    ${SCOPE_DATE}    ${TARGET_DB_COLUMN}    ${expected}

Restore Water Injection Flowline Cell To Null
    [Documentation]    Self-clean teardown: restore the (flowline × date) cell to NULL at the DB so the
    ...    test leaves the sandbox exactly as found (cell was NULL-original; UI-clear is unreliable).
    ${oid}=    Object Id By Name    OV_FLOWLINE    ${SCOPE_FLOWLINE}
    Reset Day Status Value    ${IFLW_DB_TABLE}    ${oid}    ${SCOPE_DATE}    ${TARGET_DB_COLUMN}
    Water Injection Flowline Value Should Be In DB    ${None}
