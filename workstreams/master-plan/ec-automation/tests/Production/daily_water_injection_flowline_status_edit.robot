*** Settings ***
Documentation       EC N1 Test — "Daily Water Injection Flowline, by Flowline" (edit-in-place). The N1
...                 daily-status grid generalized to WATER-INJECTION flowlines (IFLW_DAY_STATUS) —
...                 the direct menu sibling of "Daily Production Flowline, by Flowline" (PFLW), sharing
...                 the same grid component. Open via the date-range + PU→Area→Facility→Flowline
...                 cascade, EDIT a pre-instantiated (flowline × day) measured cell (real keystrokes +
...                 Tab → stage), Save (menubar @all → commit), verify on-screen AND at the DB
...                 (IFLW_DAY_STATUS.ON_STREAM_HRS — unitless, direct equality), then RESTORE the cell
...                 to NULL (self-cleaning — cell was NULL-original). The edit→Save→DB check also
...                 PROVES the cell↔column map (C2 = On Strm[hr]).
...                 Layered: this test → iflw_water_flowline_status_page (T3) → daily_status_grid (T2) +
...                 common (T1) + DbVerify.

Resource            ../../pageobjects/Production/iflw_water_flowline_status_page.resource

Suite Setup         Open Water Injection Flowline Screen
Suite Teardown      Run Keywords    Restore Water Injection Flowline Cell To Null    AND    Close EC

Test Tags           n1    daily_water_injection_flowline_status


*** Variables ***
${SENTINEL_VALUE}       18


*** Test Cases ***
TC01 Grid Loads For Scope
    [Documentation]    The date-range + 4-level cascade (PU → Area → Facility → Flowline) + GO renders
    ...    the pre-instantiated water-injection flowline daily row.
    [Tags]    smoke
    ${rows}=    Get Table Rows    ${IFLW_GRID}
    Should Not Be Empty    ${rows}    msg=No flowline row rendered for the navigator scope/date
    Capture Step    iflw_water_tc01_grid_loaded

TC02 Edit Measured Cell And Persist
    [Documentation]    Edit On Strm[hr] to a sentinel, Save, and confirm persistence on-screen AND in
    ...    IFLW_DAY_STATUS.ON_STREAM_HRS (the trustworthy oracle — which also proves C2 = ON_STREAM_HRS).
    [Tags]    edit
    Set Water Injection Flowline Cell    ${SENTINEL_VALUE}
    Save Water Injection Flowline Status
    Water Injection Flowline Cell Should Show    ${SENTINEL_VALUE}
    Water Injection Flowline Value Should Be In DB    ${SENTINEL_VALUE}
    Capture Step    iflw_water_tc02_edited

TC03 Restore To Null (cleanup)
    [Documentation]    Restore the cell to NULL so the test leaves the (flowline × day) row exactly as
    ...    found (cell was NULL-original). DB-verified back to NULL.
    [Tags]    cleanup
    Restore Water Injection Flowline Cell To Null
    Capture Step    iflw_water_tc03_restored
