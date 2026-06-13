*** Settings ***
Documentation       EC N1 Test - WR.0001 Daily Production Well Status 1 (edit-in-place).
...                 Proves the N1 daily-status-grid pattern: open via the 4-level nav cascade,
...                 EDIT a pre-instantiated (well x day) measured cell, Save, verify on-screen
...                 AND at the DB (PWEL_DAY_STATUS), then REVERT to the original value (the test
...                 is self-cleaning — it restores the seed row, touching no other data).
...                 Layered: this test -> wr0001_daily_well_status_page (T3) ->
...                 daily_status_grid (T2) + common (T1) + DbVerify.
...                 FIRST LIVE RUN must pin: ${ROW0_WELL_NAME} (the grid row-0 well name) and the
...                 ${ROW0_CELL}<->${ROW0_DB_COLUMN} pairing (edit -> Save -> diff PWEL_DAY_STATUS).

Resource            ../../pageobjects/Production/wr0001_daily_well_status_page.resource

Suite Setup         Open Daily Well Status Screen
Suite Teardown      Close EC

Test Tags           n1    daily_well_status


*** Variables ***
${ORIGINAL_VALUE}       ${EMPTY}
${SENTINEL_VALUE}       21


*** Test Cases ***
TC01 Grid Loads For Scope
    [Documentation]    The cascade + GO renders the pre-instantiated well rows for the day.
    [Tags]    smoke
    ${rows}=    Get Table Rows    ${WELL_STATUS_GRID}
    Should Not Be Empty    ${rows}    msg=No well rows rendered for the navigator scope/date
    Capture Step    wr0001_tc01_grid_loaded

TC02 Edit Measured Cell And Persist
    [Documentation]    Record the original value, edit the cell to a sentinel, Save, and confirm
    ...    persistence on-screen AND in PWEL_DAY_STATUS (the trustworthy oracle).
    [Tags]    edit
    ${orig}=    Get Cell Value By Id    ${ROW0_CELL}
    VAR    ${ORIGINAL_VALUE}    ${orig}    scope=SUITE
    Set Well Status Cell    ${SENTINEL_VALUE}
    Save Well Status
    Daily Status Cell Should Show    ${ROW0_CELL}    ${SENTINEL_VALUE}
    Well Status Value Should Be In DB    ${ROW0_WELL_NAME}    ${SENTINEL_VALUE}
    Capture Step    wr0001_tc02_edited

TC03 Revert To Original (cleanup)
    [Documentation]    Restore the seed value so the test leaves the row exactly as found.
    [Tags]    cleanup
    Set Well Status Cell    ${ORIGINAL_VALUE}
    Save Well Status
    Well Status Value Should Be In DB    ${ROW0_WELL_NAME}    ${ORIGINAL_VALUE}
    Capture Step    wr0001_tc03_reverted
