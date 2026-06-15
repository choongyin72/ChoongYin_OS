*** Settings ***
Documentation       EC N1 IUD Test — "Daily Water Injection Flowline, by Flowline". Full Insert/Update/
...                 Delete lifecycle on the daily-status grid (IFLW_DAY_STATUS), like the Bank IUD but
...                 adapted to a daily-data screen: the (flowline × day) row is PRE-INSTANTIATED and the
...                 screen has no New/Delete toolbar, so IUD is performed on the measured VALUE in the
...                 cell — INSERT = fill the empty cell + Save (DB null→value); UPDATE = change + Save
...                 (value→value); DELETE = clear the cell + Save (value→null). The cell is null-original,
...                 so the I→U→D sequence ends back at NULL = the original state (self-cleaning).
...
...                 Every step is verified at the DB (IFLW_DAY_STATUS.ON_STREAM_HRS — unitless, direct
...                 equality) — the trustworthy oracle, not the optimistic grid. (If a row were
...                 value-original instead, the lifecycle would be Update→Delete→Insert-original; here
...                 null-original makes it Insert→Update→Delete. DELETE-clear→Save→DB-null proven 2026-06-15.)
...                 Layered: this test → iflw_water_flowline_status_page (T3) → daily_status_grid (T2) +
...                 common (T1) + DbVerify.

Resource            ../../../../../pageobjects/EC_Production/Well_and_Reservoir/Daily/Group_Model_-_by_Flowline/iflw_water_flowline_status_page.resource

Suite Setup         Open Water Injection Flowline Screen
Suite Teardown      Run Keywords    Restore Water Injection Flowline Cell To Null    AND    Close EC

Test Tags           n1    daily_water_injection_flowline_status    iud


*** Variables ***
${INSERT_VALUE}     18
${UPDATE_VALUE}     24


*** Test Cases ***
TC01 Grid Loads For Scope
    [Documentation]    The date-range + 4-level cascade (PU → Area → Facility → Flowline) + GO renders
    ...    the pre-instantiated water-injection flowline daily row.
    [Tags]    smoke
    ${rows}=    Get Table Rows    ${IFLW_GRID}
    Should Not Be Empty    ${rows}    msg=No flowline row rendered for the navigator scope/date
    Capture Step    iflw_water_tc01_grid_loaded

TC02 Insert Daily Value Persists
    [Documentation]    INSERT — from the empty (null) cell, enter On Strm[hr]=${INSERT_VALUE}, Save, and
    ...    DB-verify IFLW_DAY_STATUS.ON_STREAM_HRS now holds it (data created on the pre-instantiated row).
    [Tags]    insert
    Water Injection Flowline Value Should Be In DB    ${None}
    Insert Flowline Daily Value    ${INSERT_VALUE}
    Water Injection Flowline Cell Should Show    ${INSERT_VALUE}
    Water Injection Flowline Value Should Be In DB    ${INSERT_VALUE}
    Capture Step    iflw_water_tc02_inserted

TC03 Update Daily Value Persists
    [Documentation]    UPDATE — change On Strm[hr] to ${UPDATE_VALUE}, Save, DB-verify the new value
    ...    persisted (and proves C2 = ON_STREAM_HRS).
    [Tags]    update
    Update Flowline Daily Value    ${UPDATE_VALUE}
    Water Injection Flowline Cell Should Show    ${UPDATE_VALUE}
    Water Injection Flowline Value Should Be In DB    ${UPDATE_VALUE}
    Capture Step    iflw_water_tc03_updated

TC04 Delete Daily Value Removes It
    [Documentation]    DELETE — clear the cell + Save; DB-verify ON_STREAM_HRS is back to NULL (the daily
    ...    value is gone). This also returns the row to its original state (self-cleaning).
    [Tags]    delete
    Delete Flowline Daily Value
    Water Injection Flowline Value Should Be In DB    ${None}
    Capture Step    iflw_water_tc04_deleted
