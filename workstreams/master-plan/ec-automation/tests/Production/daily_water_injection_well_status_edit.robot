*** Settings ***
Documentation       EC N1 Test — "Daily Water Injection Well Status" (edit-in-place), the N1
...                 generalization to INJECTION wells. Proves the daily-status grid pattern works
...                 the same for injection wells (IWEL_DAY_STATUS) as for production wells
...                 (WR.0001 / PWEL_DAY_STATUS): open via the 4-level nav cascade, EDIT a
...                 pre-instantiated (well × day) measured cell (real keystrokes + Tab → stage),
...                 Save (menubar @all → commit), verify on-screen AND at the DB
...                 (IWEL_DAY_STATUS.ON_STREAM_HRS), then RESTORE the cell to NULL (self-cleaning —
...                 the cell was NULL-original, so cleanup is a DB reset).
...                 Layered: this test → iwel_water_injection_status_page (T3) →
...                 daily_status_grid (T2) + common (T1) + DbVerify.

Resource            ../../pageobjects/Production/iwel_water_injection_status_page.resource

Suite Setup         Open Water Injection Well Status Screen
Suite Teardown      Run Keywords    Restore Injection Well Cell To Null    AND    Close EC

Test Tags           n1    daily_water_injection_well_status


*** Variables ***
${SENTINEL_VALUE}       18


*** Test Cases ***
TC01 Grid Loads For Scope
    [Documentation]    The cascade + GO renders the pre-instantiated injection-well rows for the day.
    [Tags]    smoke
    ${rows}=    Get Table Rows    ${IWEL_GRID}
    Should Not Be Empty    ${rows}    msg=No injection-well rows rendered for the navigator scope/date
    Capture Step    iwel_tc01_grid_loaded

TC02 Edit Measured Cell And Persist
    [Documentation]    Edit the cell to a sentinel, Save, and confirm persistence on-screen AND in
    ...    IWEL_DAY_STATUS.ON_STREAM_HRS (the trustworthy oracle).
    [Tags]    edit
    Set Injection Well Cell    ${SENTINEL_VALUE}
    Save Injection Well Status
    Injection Well Cell Should Show    ${SENTINEL_VALUE}
    Injection Well Value Should Be In DB    ${SENTINEL_VALUE}
    Capture Step    iwel_tc02_edited

TC03 Restore To Null (cleanup)
    [Documentation]    Restore the cell to NULL so the test leaves the (well × day) row exactly as
    ...    found (cell was NULL-original). DB-verified back to NULL.
    [Tags]    cleanup
    Restore Injection Well Cell To Null
    Capture Step    iwel_tc03_restored
