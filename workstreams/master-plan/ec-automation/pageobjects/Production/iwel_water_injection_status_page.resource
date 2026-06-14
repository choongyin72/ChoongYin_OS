*** Settings ***
Documentation       T3 (screen) — "Daily Water Injection Well Status" page object (N1 generalization
...                 to INJECTION wells). Screen: EC Production (search) > Daily Water Injection Well
...                 Status. Same N1 daily-status grid template as WR.0001 (Daily Production Well
...                 Status 1) but for injection wells — DB ground truth = IWEL_DAY_STATUS, key
...                 (OBJECT_ID, DAYTIME). Proves the N1 pattern generalizes from production wells
...                 (PWEL_DAY_STATUS) to injection wells (IWEL_DAY_STATUS) with the SAME grid id,
...                 SAME cell ids, SAME C4=ON_STREAM_HRS mapping (DB-proven 2026-06-14).
...                 Non-iframed (top-level). Cells are NULL-original, so the self-clean teardown
...                 restores the cell to NULL at the DB (a faithful UI "clear" pops a save-confirm
...                 modal; the assertion is still the UI->DB write, verified read-only).
...                 Layered: this test -> this T3 -> daily_status_grid (T2) + common (T1) + DbVerify.
...                 Recon: docs/ec_screen_registry.md row + tmp/scripts/n1_iwel_*.

Library             Browser
Library             ../../libraries/DbVerify.py
Resource            ../../resources/daily_status_grid.resource


*** Variables ***
${IWEL_SCREEN}              Daily Water Injection Well Status
${IWEL_GRID}               daily_well_status:form:T_data
${IWEL_DB_TABLE}           IWEL_DAY_STATUS
# Navigator cascade groups (nav:form:G:{n})
${NAV_PU}                  G:1
${NAV_AREA}                G:2
${NAV_FCTY_CLASS_1}        G:3
${NAV_WELL_HOOKUP}         G:4
# Working scope (sandbox data; renders the injection-well rows). Date has 143 P rows.
${SCOPE_DATE}              2026-02-13
${SCOPE_PU}                AS2 EC Exploration Norway
${SCOPE_AREA}              AS2_Onshore Area
${SCOPE_FCTY_CLASS_1}      AS2_Production Facility no 1
${SCOPE_WELL_HOOKUP}      AS2_Water Injection Manifold 1
# Target well (resolve by NAME -> row index) + cell column + DB column (DB-proven C4=ON_STREAM_HRS).
${TARGET_WELL}             AS2_Onshore Well no 5
${CELL_COLUMN}             C4
${TARGET_DB_COLUMN}        ON_STREAM_HRS
${TARGET_CELL}             ${EMPTY}


*** Keywords ***
Open Water Injection Well Status Screen
    [Documentation]    Suite Setup: launch, login, open the screen, set the data-bearing Date, walk
    ...    the nav cascade (PU → Area → Facility Class 1 → Water Injection Manifold), GO, then resolve
    ...    the target well's row by name and cache its measured-cell id.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${IWEL_SCREEN}    ${user}    ${pass}
    Set Daily Status Date    ${SCOPE_DATE}
    Set Navigator Filter    ${NAV_PU}    ${SCOPE_PU}
    Set Navigator Filter    ${NAV_AREA}    ${SCOPE_AREA}
    Set Navigator Filter    ${NAV_FCTY_CLASS_1}    ${SCOPE_FCTY_CLASS_1}
    Set Navigator Filter    ${NAV_WELL_HOOKUP}    ${SCOPE_WELL_HOOKUP}
    Reload Daily Status Grid
    Reload And Find Target Well

Reload And Find Target Well
    [Documentation]    Re-apply the navigator GO and re-resolve the target well's row/cell (use after
    ...    a Save so the next edit arms on a freshly-rendered grid).
    Reload Daily Status Grid
    ${idx}=    Daily Status Row Index For    ${IWEL_GRID}    ${TARGET_WELL}
    Should Be True    ${idx} >= 0    msg=Well '${TARGET_WELL}' not found in the loaded grid
    VAR    ${TARGET_CELL}    daily_well_status:form:T:${idx}:${CELL_COLUMN}_in    scope=SUITE

Set Injection Well Cell
    [Documentation]    Edit the target well's measured cell to ${value} (real keystrokes + Tab).
    [Arguments]    ${value}
    Edit Daily Status Cell    ${TARGET_CELL}    ${value}

Save Injection Well Status
    [Documentation]    Commit the grid edit via the toolbar Save (menubar, execute=@all).
    Save Daily Status

Injection Well Cell Should Show
    [Documentation]    Assert the on-screen cell shows ${value} (UI side; pair with the DB check).
    [Arguments]    ${value}
    Daily Status Cell Should Show    ${TARGET_CELL}    ${value}

Injection Well Value Should Be In DB
    [Documentation]    Ground truth: assert IWEL_DAY_STATUS.${TARGET_DB_COLUMN} of the (well × date)
    ...    row equals ${expected}.
    [Arguments]    ${expected}
    ${oid}=    Object Id By Name    WELL_VERSION    ${TARGET_WELL}
    Day Status Value Should Be    ${IWEL_DB_TABLE}    ${oid}    ${SCOPE_DATE}    ${TARGET_DB_COLUMN}    ${expected}

Restore Injection Well Cell To Null
    [Documentation]    Self-clean teardown: restore the (well × date) cell to NULL at the DB so the
    ...    test leaves the sandbox exactly as found (cell was NULL-original; UI-clear is unreliable).
    ${oid}=    Object Id By Name    WELL_VERSION    ${TARGET_WELL}
    Reset Day Status Value    ${IWEL_DB_TABLE}    ${oid}    ${SCOPE_DATE}    ${TARGET_DB_COLUMN}
    Injection Well Value Should Be In DB    ${None}
