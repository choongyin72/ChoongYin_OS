*** Settings ***
Documentation       T3 (screen) — "Daily Equipment Status" page object (N1 generalization to a new
...                 OBJECT CLASS: equipment). Screen: EC Production (search) > Daily Equipment Status.
...                 Same N1 daily-status edit-in-place grid, but the object is EQUIPMENT (not a well
...                 or stream) — DB ground truth = EQPM_DAY_STATUS, key (OBJECT_ID, DAYTIME), object
...                 name source = OV_EQPM. Proves the N1 pattern spans well / stream / injection-well
...                 / EQUIPMENT (4 object types). Non-iframed; 3-level nav (no well-hookup level).
...                 Grid id `equipment_status:form:T_data`; cells `equipment_status:form:T:{r}:C{c}_in`;
...                 **C4 = AVG_PRESS** (DB-proven 2026-06-14). Cells NULL-original → DB-restore-null
...                 self-clean teardown (same as the injection-well screen).
...                 Layered: this test -> this T3 -> daily_status_grid (T2) + common (T1) + DbVerify.

Library             Browser
Library             ../../libraries/DbVerify.py
Resource            ../../resources/daily_status_grid.resource


*** Variables ***
${EQPM_SCREEN}             Daily Equipment Status
${EQPM_GRID}              equipment_status:form:T_data
${EQPM_DB_TABLE}          EQPM_DAY_STATUS
# Navigator cascade groups (3-level: PU → Area → Facility Class 1; equipment has no well-hookup level)
${NAV_PU}                 G:1
${NAV_AREA}               G:2
${NAV_FCTY_CLASS_1}       G:3
# Working scope (P1 Facility 1 holds 88 equipment with data on the date)
${SCOPE_DATE}             2024-02-06
${SCOPE_PU}               P1 Production Unit
${SCOPE_AREA}             P1 Area
${SCOPE_FCTY_CLASS_1}     P1 Facility 1
# Target equipment (resolve by NAME -> row index) + cell column + DB column (DB-proven C4=AVG_PRESS).
# NAME in OV_EQPM includes the code suffix.
${TARGET_EQPM}            P1 Chiller 002 PO.0011
${CELL_COLUMN}            C4
${TARGET_DB_COLUMN}       AVG_PRESS
${TARGET_CELL}            ${EMPTY}


*** Keywords ***
Open Equipment Status Screen
    [Documentation]    Suite Setup: launch, login, open the screen, set the data-bearing Date, walk
    ...    the 3-level nav cascade (PU → Area → Facility Class 1), GO, then resolve the target
    ...    equipment's row by name and cache its measured-cell id.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${EQPM_SCREEN}    ${user}    ${pass}
    Set Daily Status Date    ${SCOPE_DATE}
    Set Navigator Filter    ${NAV_PU}    ${SCOPE_PU}
    Set Navigator Filter    ${NAV_AREA}    ${SCOPE_AREA}
    Set Navigator Filter    ${NAV_FCTY_CLASS_1}    ${SCOPE_FCTY_CLASS_1}
    Reload Daily Status Grid
    Reload And Find Target Equipment

Reload And Find Target Equipment
    [Documentation]    Re-apply the navigator GO and re-resolve the target equipment's row/cell.
    Reload Daily Status Grid
    ${idx}=    Daily Status Row Index For    ${EQPM_GRID}    ${TARGET_EQPM}
    Should Be True    ${idx} >= 0    msg=Equipment '${TARGET_EQPM}' not found in the loaded grid
    VAR    ${TARGET_CELL}    equipment_status:form:T:${idx}:${CELL_COLUMN}_in    scope=SUITE

Set Equipment Cell
    [Documentation]    Edit the target equipment's measured cell to ${value} (real keystrokes + Tab).
    [Arguments]    ${value}
    Edit Daily Status Cell    ${TARGET_CELL}    ${value}

Save Equipment Status
    [Documentation]    Commit the grid edit via the toolbar Save (menubar, execute=@all).
    Save Daily Status

Equipment Cell Should Show
    [Documentation]    Assert the on-screen cell shows ${value} (UI side; pair with the DB check).
    [Arguments]    ${value}
    Daily Status Cell Should Show    ${TARGET_CELL}    ${value}

Equipment Value Should Be In DB
    [Documentation]    Ground truth: assert EQPM_DAY_STATUS.${TARGET_DB_COLUMN} of the (equipment ×
    ...    date) row equals ${expected}.
    [Arguments]    ${expected}
    ${oid}=    Object Id By Name    OV_EQPM    ${TARGET_EQPM}
    Day Status Value Should Be    ${EQPM_DB_TABLE}    ${oid}    ${SCOPE_DATE}    ${TARGET_DB_COLUMN}    ${expected}

Restore Equipment Cell To Null
    [Documentation]    Self-clean teardown: restore the (equipment × date) cell to NULL at the DB so
    ...    the test leaves the sandbox exactly as found (cell was NULL-original).
    ${oid}=    Object Id By Name    OV_EQPM    ${TARGET_EQPM}
    Reset Day Status Value    ${EQPM_DB_TABLE}    ${oid}    ${SCOPE_DATE}    ${TARGET_DB_COLUMN}
    Equipment Value Should Be In DB    ${None}
