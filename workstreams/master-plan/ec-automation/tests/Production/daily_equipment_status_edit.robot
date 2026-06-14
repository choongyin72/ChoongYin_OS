*** Settings ***
Documentation       EC N1 Test — "Daily Equipment Status" (edit-in-place), the N1 generalization to a
...                 new OBJECT CLASS: equipment. Proves the daily-status grid pattern works for
...                 equipment (EQPM_DAY_STATUS) exactly as for wells/streams: open via the 3-level nav
...                 cascade, EDIT a pre-instantiated (equipment × day) measured cell (real keystrokes
...                 + Tab → stage), Save (menubar @all → commit), verify on-screen AND at the DB
...                 (EQPM_DAY_STATUS.AVG_PRESS), then RESTORE the cell to NULL (self-cleaning — the
...                 cell was NULL-original, so cleanup is a DB reset).
...                 N1 now spans 4 object types: PWEL (WR.0001) / STRM (PO.0002) / IWEL / EQPM.
...                 Layered: this test → eqpm_daily_status_page (T3) → daily_status_grid (T2) +
...                 common (T1) + DbVerify.

Resource            ../../pageobjects/Production/eqpm_daily_status_page.resource

Suite Setup         Open Equipment Status Screen
Suite Teardown      Run Keywords    Restore Equipment Cell To Null    AND    Close EC

Test Tags           n1    daily_equipment_status


*** Variables ***
${SENTINEL_VALUE}       18


*** Test Cases ***
TC01 Grid Loads For Scope
    [Documentation]    The cascade + GO renders the pre-instantiated equipment rows for the day.
    [Tags]    smoke
    ${rows}=    Get Table Rows    ${EQPM_GRID}
    Should Not Be Empty    ${rows}    msg=No equipment rows rendered for the navigator scope/date
    Capture Step    eqpm_tc01_grid_loaded

TC02 Edit Measured Cell And Persist
    [Documentation]    Edit the cell to a sentinel, Save, and confirm persistence on-screen AND in
    ...    EQPM_DAY_STATUS.AVG_PRESS (the trustworthy oracle).
    [Tags]    edit
    Set Equipment Cell    ${SENTINEL_VALUE}
    Save Equipment Status
    Equipment Cell Should Show    ${SENTINEL_VALUE}
    Equipment Value Should Be In DB    ${SENTINEL_VALUE}
    Capture Step    eqpm_tc02_edited

TC03 Restore To Null (cleanup)
    [Documentation]    Restore the cell to NULL so the test leaves the (equipment × day) row exactly
    ...    as found. DB-verified back to NULL.
    [Tags]    cleanup
    Restore Equipment Cell To Null
    Capture Step    eqpm_tc03_restored
