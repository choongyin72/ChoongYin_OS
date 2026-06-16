*** Settings ***
Documentation       EC N1 Test - PO.0066 Daily Electrical Stream Status (edit-in-place).
...                 SIBLING of PO.0002 Gas / PO.0001 Oil / PO.0003 Water Stream Status — proves the
...                 N1 daily-status-grid pattern reuses across ALL stream types. Open via the 3-level
...                 nav cascade, EDIT the measured cell (real keystrokes + Tab -> stage), Save
...                 (menubar execute=@all -> commit), verify on-screen AND at the DB
...                 (STRM_DAY_STREAM.POWER_CONSUMPTION — electrical has no volume), then REVERT
...                 (self-cleaning). UPDATE-only (no I/D). Layered: this test ->
...                 po0066_daily_electrical_stream_status_page (T3) -> daily_status_grid (T2) +
...                 common (T1) + DbVerify.

Resource            ../../pageobjects/Production/po0066_daily_electrical_stream_status_page.resource

Suite Setup         Open Daily Electrical Stream Status Screen
Suite Teardown      Close EC

Test Tags           n1    daily_electrical_stream_status


*** Variables ***
${ORIGINAL_VALUE}       ${EMPTY}
${SENTINEL_VALUE}       1234.5


*** Test Cases ***
TC01 Grid Loads For Scope
    [Documentation]    The cascade + GO renders the pre-instantiated electrical-stream rows.
    [Tags]    smoke
    ${rows}=    Get Table Rows    ${STREAM_STATUS_GRID}
    Should Not Be Empty    ${rows}    msg=No stream rows rendered for the navigator scope/date
    Capture Step    po0066_tc01_grid_loaded

TC02 Edit Measured Cell And Persist
    [Documentation]    Record the original value, edit Power Consumption to a sentinel, Save, and
    ...    confirm persistence on-screen AND in STRM_DAY_STREAM.POWER_CONSUMPTION (the oracle).
    [Tags]    edit
    ${orig}=    Read Stream Status Value
    VAR    ${ORIGINAL_VALUE}    ${orig}    scope=SUITE
    Set Stream Status Cell    ${SENTINEL_VALUE}
    Save Stream Status
    Stream Status Cell Should Show    ${SENTINEL_VALUE}
    Stream Status Value Should Be In DB    ${SENTINEL_VALUE}
    Capture Step    po0066_tc02_edited

TC03 Revert To Original (cleanup)
    [Documentation]    Restore the seed value so the test leaves the row exactly as found.
    ...    Reload first (post-commit re-render) so the revert edit arms Save.
    [Tags]    cleanup
    Reload And Find Target Stream
    Set Stream Status Cell    ${ORIGINAL_VALUE}
    Save Stream Status
    Stream Status Value Should Be In DB    ${ORIGINAL_VALUE}
    Capture Step    po0066_tc03_reverted
