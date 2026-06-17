*** Settings ***
Documentation       T3 (screen) — PO.0005.02 Daily Tank Status - VCF Calc page object.
...                 Screen: EC Production (search) > Daily Tank Status - VCF Calc.
...                 N1 daily-status grid — TANK variant of the stream-status pattern. Same 3-level
...                 navigator cascade (Date -> Production Unit -> Area -> Facility Class 1) loads an
...                 editable grid of pre-instantiated (tank x day) rows; edit a measured cell (no
...                 insert/delete — UPDATE-only). Differs from the stream siblings:
...                  - grid is `dip_table:form:T_data` (cells `dip_table:form:T:{r}:C{c}_in`), NOT
...                    `measured:form`;
...                  - the editable input is the **Liquid Dip** (C4); Grs Vol etc. are CALCULATED
...                    from it (VCF calc runs on Save);
...                  - DB ground truth is the data-view `DV_TANK_DAY_DIP_STATUS` (col LIQUID_DIP_LEVEL)
...                    — there is no `TANK_DAY_DIP_STATUS` base table; the verify is a SELECT, so the
...                    view works fine;
...                  - the stream name source is `OV_TANK` (NAME includes the position code).
...                 Cell mapping verified live 2026-06-17 (sandbox): C4 = 'Liquid Dip' = LIQUID_DIP_LEVEL.

Library             Browser
Library             ../../libraries/DbVerify.py
Resource            ../../resources/daily_status_grid.resource


*** Variables ***
${STREAM_STATUS_SCREEN}     Daily Tank Status - VCF Calc
${STREAM_STATUS_GRID}       dip_table:form:T_data
${STREAM_STATUS_DB_TABLE}   DV_TANK_DAY_DIP_STATUS
${STREAM_NAME_SOURCE}       OV_TANK
# Navigator cascade groups (3-level — no Well Hookup)
${NAV_PU}                   G:1
${NAV_AREA}                 G:2
${NAV_FCTY_CLASS_1}         G:3
# Working test scope (sandbox P1 demo; renders the tank rows on this date)
${SCOPE_DATE}               2014-01-01
${SCOPE_PU}                 P1 Production Unit
${SCOPE_AREA}               P1 Area
${SCOPE_FCTY_CLASS_1}       P1 Facility 1
# Target tank (resolved by NAME -> row) + cell column + DB column.
# VERIFIED LIVE 2026-06-17: C4 = Liquid Dip = DV_TANK_DAY_DIP_STATUS.LIQUID_DIP_LEVEL (P1 VCF-CTSh T14 = 476.707).
${TARGET_STREAM}            P1 VCF-CTSh T14 12.1.1
${CELL_COLUMN}              C4
${TARGET_DB_COLUMN}         LIQUID_DIP_LEVEL
${TARGET_CELL}              ${EMPTY}


*** Keywords ***
Open Daily Tank Status VCF Screen
    [Documentation]    Suite Setup: launch, login, open the screen, set the data-bearing Date,
    ...    walk the 3-level cascade (PU -> Area -> Facility Class 1), GO, then resolve the target
    ...    tank's row by name and cache its Liquid-Dip cell id.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${STREAM_STATUS_SCREEN}    ${user}    ${pass}
    Set Daily Status Date    ${SCOPE_DATE}
    Set Navigator Filter    ${NAV_PU}    ${SCOPE_PU}
    Set Navigator Filter    ${NAV_AREA}    ${SCOPE_AREA}
    Set Navigator Filter    ${NAV_FCTY_CLASS_1}    ${SCOPE_FCTY_CLASS_1}
    Reload Daily Status Grid
    ${idx}=    Daily Status Row Index For    ${STREAM_STATUS_GRID}    ${TARGET_STREAM}
    Should Be True    ${idx} >= 0    msg=Tank '${TARGET_STREAM}' not found in the loaded grid
    VAR    ${TARGET_CELL}    dip_table:form:T:${idx}:${CELL_COLUMN}_in    scope=SUITE

Reload And Find Target Stream
    [Documentation]    Re-GO and re-resolve the tank's cell (use between Save and the next edit;
    ...    a fresh grid avoids the post-commit state where Save won't re-arm).
    Reload Daily Status Grid
    ${idx}=    Daily Status Row Index For    ${STREAM_STATUS_GRID}    ${TARGET_STREAM}
    Should Be True    ${idx} >= 0    msg=Tank '${TARGET_STREAM}' not found after reload
    VAR    ${TARGET_CELL}    dip_table:form:T:${idx}:${CELL_COLUMN}_in    scope=SUITE

Read Stream Status Value
    [Documentation]    Return the target tank's Liquid-Dip cell value, commas stripped.
    ${v}=    Read Daily Status Cell    ${TARGET_CELL}
    RETURN    ${v}

Set Stream Status Cell
    [Documentation]    Edit the target tank's Liquid-Dip cell to ${value} (real keystrokes + Tab).
    ...    NOTE: saving recalculates the VCF figures (Grs Vol etc.) — we assert only the dip input
    ...    + its DB column, so the downstream recalc is an unasserted side effect.
    [Arguments]    ${value}
    Edit Daily Status Cell    ${TARGET_CELL}    ${value}

Save Stream Status
    [Documentation]    Commit the grid edit via the toolbar Save (menubar, execute=@all). Save also
    ...    triggers the VCF recalculation; the ajax wait in the T2 keyword covers it.
    Save Daily Status

Stream Status Cell Should Show
    [Documentation]    Assert the on-screen Liquid-Dip cell shows ${value} (UI side; pair with DB).
    [Arguments]    ${value}
    Daily Status Cell Should Show    ${TARGET_CELL}    ${value}

Stream Status Value Should Be In DB
    [Documentation]    Ground truth: assert ${TARGET_DB_COLUMN} of the (tank x date) row in
    ...    DV_TANK_DAY_DIP_STATUS equals ${expected}.
    [Arguments]    ${expected}
    ${oid}=    Object Id By Name    ${STREAM_NAME_SOURCE}    ${TARGET_STREAM}
    Day Status Value Should Be    ${STREAM_STATUS_DB_TABLE}    ${oid}    ${SCOPE_DATE}    ${TARGET_DB_COLUMN}    ${expected}
