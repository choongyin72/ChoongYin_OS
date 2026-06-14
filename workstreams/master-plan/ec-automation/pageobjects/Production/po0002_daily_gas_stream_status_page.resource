*** Settings ***
Documentation       T3 (screen) — PO.0002 Daily Gas Stream Status page object.
...                 Screen: EC Production (search) > Daily Gas Stream Status.
...                 N1 daily-status grid (GENERALIZATION of WR.0001 — proves the pattern reuses):
...                 3-level navigator cascade (Date -> Production Unit -> Area -> Facility Class 1;
...                 NO Well Hookup) loads an editable `measured:form` grid of pre-instantiated
...                 (stream x day) rows; edit a measured cell (no insert/delete). DB ground truth
...                 = STRM_DAY_STREAM (the URL CLASS_NAMEs _MEAS_GAS/_DER_GAS are view projections,
...                 NOT the physical table). Resolve the stream BY NAME via OV_STREAM. WRITE gesture
...                 = same as WR.0001 (real keystrokes + Tab stages; menubar Save commits) — DB-proven
...                 C7 -> GRS_VOL. Recon/proof: docs/pattern_n1_daily_status_grid_design.md.

Library             Browser
Library             ../../libraries/DbVerify.py
Resource            ../../resources/daily_status_grid.resource


*** Variables ***
${STREAM_STATUS_SCREEN}     Daily Gas Stream Status
${STREAM_STATUS_GRID}       measured:form:T_data
${STREAM_STATUS_DB_TABLE}   STRM_DAY_STREAM
${STREAM_NAME_SOURCE}       OV_STREAM
# Navigator cascade groups (3-level — no Well Hookup)
${NAV_PU}                   G:1
${NAV_AREA}                 G:2
${NAV_FCTY_CLASS_1}         G:3
# Working test scope (sandbox seed; renders the gas-stream rows)
${SCOPE_DATE}               2003-01-01
${SCOPE_PU}                 AS2 EC Exploration Norway
${SCOPE_AREA}               AS2_Onshore Area
${SCOPE_FCTY_CLASS_1}       AS2_Production Facility no 1
# Target stream (resolved by NAME -> row) + cell column + DB column.
# DB-PROVEN 2026-06-13: measured C7 = STRM_DAY_STREAM.GRS_VOL (edit->save persisted; revert OK).
${TARGET_STREAM}            AS2_Flare Gas 001
${CELL_COLUMN}              C7
${TARGET_DB_COLUMN}         GRS_VOL
${TARGET_CELL}              ${EMPTY}


*** Keywords ***
Open Daily Gas Stream Status Screen
    [Documentation]    Suite Setup: launch, login, open the screen, set the data-bearing Date,
    ...    walk the 3-level cascade (PU -> Area -> Facility Class 1), GO, then resolve the target
    ...    stream's row by name and cache its measured-cell id.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${STREAM_STATUS_SCREEN}    ${user}    ${pass}
    Set Daily Status Date    ${SCOPE_DATE}
    Set Navigator Filter    ${NAV_PU}    ${SCOPE_PU}
    Set Navigator Filter    ${NAV_AREA}    ${SCOPE_AREA}
    Set Navigator Filter    ${NAV_FCTY_CLASS_1}    ${SCOPE_FCTY_CLASS_1}
    Reload Daily Status Grid
    ${idx}=    Daily Status Row Index For    ${STREAM_STATUS_GRID}    ${TARGET_STREAM}
    Should Be True    ${idx} >= 0    msg=Stream '${TARGET_STREAM}' not found in the loaded grid
    VAR    ${TARGET_CELL}    measured:form:T:${idx}:${CELL_COLUMN}_in    scope=SUITE

Reload And Find Target Stream
    [Documentation]    Re-GO and re-resolve the stream's cell (use between Save and the next edit;
    ...    a fresh grid avoids the post-commit state where Save won't re-arm).
    Reload Daily Status Grid
    ${idx}=    Daily Status Row Index For    ${STREAM_STATUS_GRID}    ${TARGET_STREAM}
    Should Be True    ${idx} >= 0    msg=Stream '${TARGET_STREAM}' not found after reload
    VAR    ${TARGET_CELL}    measured:form:T:${idx}:${CELL_COLUMN}_in    scope=SUITE

Read Stream Status Value
    [Documentation]    Return the target stream's measured-cell value, commas stripped (gas rates
    ...    are formatted like 2,949.9 -> 2949.9 so the value can be re-typed on revert).
    ${v}=    Read Daily Status Cell    ${TARGET_CELL}
    RETURN    ${v}

Set Stream Status Cell
    [Documentation]    Edit the target stream's measured cell to ${value} (real keystrokes + Tab).
    [Arguments]    ${value}
    Edit Daily Status Cell    ${TARGET_CELL}    ${value}

Save Stream Status
    [Documentation]    Commit the grid edit via the toolbar Save (menubar, execute=@all).
    Save Daily Status

Stream Status Cell Should Show
    [Documentation]    Assert the on-screen cell shows ${value} (UI side; pair with the DB check).
    [Arguments]    ${value}
    Daily Status Cell Should Show    ${TARGET_CELL}    ${value}

Stream Status Value Should Be In DB
    [Documentation]    Ground truth: assert ${TARGET_DB_COLUMN} of the (stream x date) row in
    ...    STRM_DAY_STREAM equals ${expected}.
    [Arguments]    ${expected}
    ${oid}=    Object Id By Name    ${STREAM_NAME_SOURCE}    ${TARGET_STREAM}
    Day Status Value Should Be    ${STREAM_STATUS_DB_TABLE}    ${oid}    ${SCOPE_DATE}    ${TARGET_DB_COLUMN}    ${expected}
