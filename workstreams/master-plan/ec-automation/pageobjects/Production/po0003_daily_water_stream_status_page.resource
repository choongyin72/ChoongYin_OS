*** Settings ***
Documentation       T3 (screen) — PO.0003 Daily Water Stream Status page object.
...                 Screen: EC Production (search) > Daily Water Stream Status.
...                 N1 daily-status grid — SIBLING of PO.0002 Gas / PO.0001 Oil Stream Status
...                 (proves the pattern reuses across stream types): same 3-level navigator cascade
...                 (Date -> Production Unit -> Area -> Facility Class 1) loads an editable
...                 `measured:form` grid of pre-instantiated (stream x day) rows; edit a measured
...                 cell (no insert/delete — UPDATE-only). DB ground truth = STRM_DAY_STREAM (the
...                 _MEAS_WAT/_DER_WAT CLASS_NAMEs are view projections). Resolve the stream BY NAME
...                 via OV_STREAM. WRITE gesture = same as the gas/oil siblings.
...                 Cell mapping verified live 2026-06-17 (sandbox): measured C3 = the editable Grs
...                 Vol cell = STRM_DAY_STREAM.GRS_VOL (P1 S087 showed 100.0 == DB GRS_VOL_WAT).

Library             Browser
Library             ../../libraries/DbVerify.py
Resource            ../../resources/daily_status_grid.resource


*** Variables ***
${STREAM_STATUS_SCREEN}     Daily Water Stream Status
${STREAM_STATUS_GRID}       measured:form:T_data
${STREAM_STATUS_DB_TABLE}   STRM_DAY_STREAM
${STREAM_NAME_SOURCE}       OV_STREAM
# Navigator cascade groups (3-level — no Well Hookup)
${NAV_PU}                   G:1
${NAV_AREA}                 G:2
${NAV_FCTY_CLASS_1}         G:3
# Working test scope (sandbox P1 demo; renders the water-stream rows on this date)
${SCOPE_DATE}               2023-01-01
${SCOPE_PU}                 P1 Production Unit
${SCOPE_AREA}               P1 Area
${SCOPE_FCTY_CLASS_1}       P1 Facility 1
# Target stream (resolved by NAME -> row) + cell column + DB column.
# VERIFIED LIVE 2026-06-17: measured C3 = STRM_DAY_STREAM.GRS_VOL (P1 S087 on-screen 100.0 == DB).
${TARGET_STREAM}            P1 S087 M WAT PD.0005_07
${CELL_COLUMN}              C3
${TARGET_DB_COLUMN}         GRS_VOL
${TARGET_CELL}              ${EMPTY}


*** Keywords ***
Open Daily Water Stream Status Screen
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
    [Documentation]    Return the target stream's measured-cell value, commas stripped.
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
