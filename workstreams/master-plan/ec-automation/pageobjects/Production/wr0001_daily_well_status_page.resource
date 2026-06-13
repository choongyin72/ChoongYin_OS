*** Settings ***
Documentation       T3 (screen) — WR.0001 Daily Production Well Status 1 page object.
...                 Screen: EC Production (search) > Daily Production Well Status 1.
...                 N1 daily-status grid (see resources/daily_status_grid.resource): a 4-level
...                 navigator CASCADE (Date -> Production Unit -> Area -> Facility Class 1 ->
...                 Well Hookup) loads a grid of pre-instantiated (well x day) rows; you EDIT
...                 measured cells (no insert/delete). DB ground truth = PWEL_DAY_STATUS, key
...                 (OBJECT_ID, DAYTIME). Recon: docs/pattern_n1_daily_status_grid_design.md.
...                 NOTE: the cell<->DB-column pairing + row-0 well NAME below are recon defaults
...                 that must be CONFIRMED in the first live run (edit a cell -> Save -> diff
...                 PWEL_DAY_STATUS to see which column changed), then pinned here.

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
# Working test scope (sandbox seed data; confirmed renders 2 well rows)
${SCOPE_DATE}               2003-01-01
${SCOPE_PU}                 AS2 EC Exploration Norway
${SCOPE_AREA}               AS2_Onshore Area
${SCOPE_FCTY_CLASS_1}       AS2_Production Facility no 1
${SCOPE_WELL_HOOKUP}        AS2_Lift Gas Manifold 1
# Row-0 editable cell + its DB column — CONFIRMED by read-only cross-ref 2026-06-13:
# grid C4_in shows 24.00 and PWEL_DAY_STATUS.ON_STREAM_HRS for this well/day = 24.
${ROW0_CELL}                daily_well_status:form:T:0:C4_in
${ROW0_DB_COLUMN}           ON_STREAM_HRS
${ROW0_WELL_NAME}           AS2_Onshore Well no 2


*** Keywords ***
Open Daily Well Status Screen
    [Documentation]    Suite Setup: launch, login, open the screen, set the data-bearing Date,
    ...    walk the full nav cascade (PU -> Area -> Facility Class 1 -> Well Hookup), then GO.
    ...    The grid only populates once the Well Hookup leaf is set.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${WELL_STATUS_SCREEN}    ${user}    ${pass}
    Set Daily Status Date    ${SCOPE_DATE}
    Set Navigator Filter    ${NAV_PU}    ${SCOPE_PU}
    Set Navigator Filter    ${NAV_AREA}    ${SCOPE_AREA}
    Set Navigator Filter    ${NAV_FCTY_CLASS_1}    ${SCOPE_FCTY_CLASS_1}
    Set Navigator Filter    ${NAV_WELL_HOOKUP}    ${SCOPE_WELL_HOOKUP}
    Reload Daily Status Grid

Set Well Status Cell
    [Documentation]    Edit ${cell_id} to ${value} (defaults to the row-0 measured cell).
    [Arguments]    ${value}    ${cell_id}=${ROW0_CELL}
    Edit Daily Status Cell    ${cell_id}    ${value}

Save Well Status
    [Documentation]    Persist the grid edit via the toolbar Save.
    Save Daily Status

Well Status Value Should Be In DB
    [Documentation]    Ground truth: assert ${column} of the (well x SCOPE_DATE) row in
    ...    PWEL_DAY_STATUS equals ${expected}. ${well_name} = the grid row's well display name.
    [Arguments]    ${well_name}    ${expected}    ${column}=${ROW0_DB_COLUMN}
    Daily Status Value In DB Should Be    ${WELL_STATUS_DB_TABLE}    ${well_name}    ${SCOPE_DATE}    ${column}    ${expected}
