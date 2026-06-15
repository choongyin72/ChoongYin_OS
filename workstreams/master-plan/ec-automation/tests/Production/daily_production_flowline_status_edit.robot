*** Settings ***
Documentation       EC N1 Test — "Daily Production Flowline, by Flowline" (edit-in-place), the N1
...                 generalization to FLOWLINES (6th object class after PWEL/STRM/IWEL/EQPM). Proves
...                 the daily-status grid pattern works the same for flowlines (PFLW_DAY_STATUS) as
...                 for wells: open via the date-range + PU→Area→Facility→Flowline cascade, EDIT a
...                 pre-instantiated (flowline × day) measured cell (real keystrokes + Tab → stage),
...                 Save (menubar @all → commit), verify on-screen AND at the DB
...                 (PFLW_DAY_STATUS.ON_STREAM_HRS — unitless, direct equality), then RESTORE the cell
...                 to NULL (self-cleaning — cell was NULL-original). The edit→Save→DB check also
...                 PROVES the cell↔column map (C2 = On Strm[hr]).
...                 Layered: this test → pflw_flowline_status_page (T3) → daily_status_grid (T2) +
...                 common (T1) + DbVerify.

Resource            ../../pageobjects/Production/pflw_flowline_status_page.resource

Suite Setup         Open Flowline Status Screen
Suite Teardown      Run Keywords    Restore Flowline Cell To Null    AND    Close EC

Test Tags           n1    daily_production_flowline_status


*** Variables ***
${SENTINEL_VALUE}       18


*** Test Cases ***
TC01 Grid Loads For Scope
    [Documentation]    The date-range + 4-level cascade (PU → Area → Facility → Flowline) + GO renders
    ...    the pre-instantiated flowline daily row.
    [Tags]    smoke
    ${rows}=    Get Table Rows    ${PFLW_GRID}
    Should Not Be Empty    ${rows}    msg=No flowline row rendered for the navigator scope/date
    Capture Step    pflw_tc01_grid_loaded

TC02 Edit Measured Cell And Persist
    [Documentation]    Edit On Strm[hr] to a sentinel, Save, and confirm persistence on-screen AND in
    ...    PFLW_DAY_STATUS.ON_STREAM_HRS (the trustworthy oracle — which also proves C2 = ON_STREAM_HRS).
    [Tags]    edit
    Set Flowline Cell    ${SENTINEL_VALUE}
    Save Flowline Status
    Flowline Cell Should Show    ${SENTINEL_VALUE}
    Flowline Value Should Be In DB    ${SENTINEL_VALUE}
    Capture Step    pflw_tc02_edited

TC03 Restore To Null (cleanup)
    [Documentation]    Restore the cell to NULL so the test leaves the (flowline × day) row exactly as
    ...    found (cell was NULL-original). DB-verified back to NULL.
    [Tags]    cleanup
    Restore Flowline Cell To Null
    Capture Step    pflw_tc03_restored
