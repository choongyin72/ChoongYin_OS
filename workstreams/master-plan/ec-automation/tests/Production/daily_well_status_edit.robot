*** Settings ***
Documentation       EC N1 Test - WR.0001 Daily Production Well Status 1 (edit-in-place).
...                 Proves the N1 daily-status-grid pattern: open via the 4-level nav cascade,
...                 EDIT a pre-instantiated (well x day) measured cell (real keystrokes + Tab ->
...                 stage), Save (menubar execute=@all -> commit), verify on-screen AND at the DB
...                 (PWEL_DAY_STATUS.ON_STREAM_HRS), then REVERT to the original value (self-cleaning
...                 -- restores the seed row, touches no other data). Gesture DB-proven 2026-06-13.
...                 Layered: this test -> wr0001_daily_well_status_page (T3) ->
...                 daily_status_grid (T2) + common (T1) + DbVerify.

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
    ${orig}=    Read Well Status Value
    VAR    ${ORIGINAL_VALUE}    ${orig}    scope=SUITE
    Set Well Status Cell    ${SENTINEL_VALUE}
    Save Well Status
    Well Status Cell Should Show    ${SENTINEL_VALUE}
    Well Status Value Should Be In DB    ${SENTINEL_VALUE}
    Capture Step    wr0001_tc02_edited

TC03 Revert To Original (cleanup)
    [Documentation]    Restore the seed value so the test leaves the row exactly as found.
    ...    Reload first: after TC02's commit the grid re-renders, so a fresh GO gives a clean
    ...    state where the revert edit arms Save (chaining edit->save->edit in one session).
    [Tags]    cleanup
    Reload And Find Target Well
    Set Well Status Cell    ${ORIGINAL_VALUE}
    Save Well Status
    Well Status Value Should Be In DB    ${ORIGINAL_VALUE}
    Capture Step    wr0001_tc03_reverted
