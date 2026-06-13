*** Settings ***
Documentation       T3 (screen) — WR.0001 Daily Production Well Status 1 page object.
...                 Screen: EC Production (search) > Daily Production Well Status 1.
...                 N1 daily-status grid (see resources/daily_status_grid.resource): a 4-level
...                 navigator CASCADE (Date -> Production Unit -> Area -> Facility Class 1 ->
...                 Well Hookup) loads a grid of pre-instantiated (well x day) rows; you EDIT a
...                 measured cell (no insert/delete). DB ground truth = PWEL_DAY_STATUS, key
...                 (OBJECT_ID, DAYTIME). WRITE gesture DB-PROVEN 2026-06-13: Type Cell By Id
...                 (real keystrokes + Tab fires the cell `change` -> stages) then toolbar Save
...                 (menubar execute=@all -> commits). Target well is resolved BY NAME (its row is
...                 not 0). Recon + proof: docs/pattern_n1_daily_status_grid_design.md.

Library             Browser
Library             ../../libraries/DbVerify.py
Resource            ../../resources/daily_status_grid.resource


*** Variables ***
${WELL_STATUS_SCREEN}       Daily Production Well Status 1
${WELL_STATUS_GRID}         daily_well_status:form:T_data
${WELL_STATUS_DB_TABLE}     PWEL_DAY_STATUS
# Navigator cascade groups (nav:form:G:{n}) — confirmed by recon
${NAV_PU}                   G:1
${NAV_AREA}                 G:2
${NAV_FCTY_CLASS_1}         G:3
${NAV_WELL_HOOKUP}          G:4
# Working test scope (sandbox seed data; renders the well rows)
${SCOPE_DATE}               2003-01-01
${SCOPE_PU}                 AS2 EC Exploration Norway
${SCOPE_AREA}               AS2_Onshore Area
${SCOPE_FCTY_CLASS_1}       AS2_Production Facility no 1
${SCOPE_WELL_HOOKUP}        AS2_Lift Gas Manifold 1
# Target well (resolved by NAME -> its row index; do NOT assume row 0) + the cell column + DB column.
# DB-PROVEN: C4 = ON_STREAM_HRS (grid 24.00 == DB 24, and an automated 24->22->24 round-trip persisted).
${TARGET_WELL}              AS2_Onshore Well no 2
${CELL_COLUMN}              C4
${TARGET_DB_COLUMN}         ON_STREAM_HRS
${TARGET_CELL}              ${EMPTY}


*** Keywords ***
Open Daily Well Status Screen
    [Documentation]    Suite Setup: launch, login, open the screen, set the data-bearing Date,
    ...    walk the full nav cascade (PU -> Area -> Facility Class 1 -> Well Hookup), GO, then
    ...    resolve the target well's row by name and cache its measured-cell id.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${WELL_STATUS_SCREEN}    ${user}    ${pass}
    Set Daily Status Date    ${SCOPE_DATE}
    Set Navigator Filter    ${NAV_PU}    ${SCOPE_PU}
    Set Navigator Filter    ${NAV_AREA}    ${SCOPE_AREA}
    Set Navigator Filter    ${NAV_FCTY_CLASS_1}    ${SCOPE_FCTY_CLASS_1}
    Set Navigator Filter    ${NAV_WELL_HOOKUP}    ${SCOPE_WELL_HOOKUP}
    Reload Daily Status Grid
    ${idx}=    Daily Status Row Index For    ${WELL_STATUS_GRID}    ${TARGET_WELL}
    Should Be True    ${idx} >= 0    msg=Well '${TARGET_WELL}' not found in the loaded grid
    VAR    ${TARGET_CELL}    daily_well_status:form:T:${idx}:${CELL_COLUMN}_in    scope=SUITE

Reload And Find Target Well
    [Documentation]    Re-apply the navigator GO and re-resolve the target well's row/cell. Use
    ...    between a Save and the next edit: after a commit the grid re-renders, so a fresh reload
    ...    gives a clean state to edit again (avoids a stale post-save grid where Save won't arm).
    Reload Daily Status Grid
    ${idx}=    Daily Status Row Index For    ${WELL_STATUS_GRID}    ${TARGET_WELL}
    Should Be True    ${idx} >= 0    msg=Well '${TARGET_WELL}' not found after reload
    VAR    ${TARGET_CELL}    daily_well_status:form:T:${idx}:${CELL_COLUMN}_in    scope=SUITE

Read Well Status Value
    [Documentation]    Return the current on-screen value of the target well's measured cell.
    ${v}=    Get Cell Value By Id    ${TARGET_CELL}
    RETURN    ${v}

Set Well Status Cell
    [Documentation]    Edit the target well's measured cell to ${value} (real keystrokes + Tab).
    [Arguments]    ${value}
    Edit Daily Status Cell    ${TARGET_CELL}    ${value}

Save Well Status
    [Documentation]    Commit the grid edit via the toolbar Save (menubar, execute=@all).
    Save Daily Status

Well Status Cell Should Show
    [Documentation]    Assert the on-screen cell shows ${value} (UI side; pair with the DB check).
    [Arguments]    ${value}
    Daily Status Cell Should Show    ${TARGET_CELL}    ${value}

Well Status Value Should Be In DB
    [Documentation]    Ground truth: assert ${TARGET_DB_COLUMN} of the (well x date) row in
    ...    PWEL_DAY_STATUS equals ${expected}.
    [Arguments]    ${expected}
    Daily Status Value In DB Should Be    ${WELL_STATUS_DB_TABLE}    ${TARGET_WELL}    ${SCOPE_DATE}    ${TARGET_DB_COLUMN}    ${expected}
