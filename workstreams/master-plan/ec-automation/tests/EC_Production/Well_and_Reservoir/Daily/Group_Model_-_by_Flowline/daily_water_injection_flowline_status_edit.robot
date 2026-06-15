*** Settings ***
Documentation       EC N1 Test — "Daily Water Injection Flowline, by Flowline" (edit-in-place).
...                 ⚠️ This screen is **UPDATE-ONLY**: the New (insert) and Delete toolbar icons are
...                 DISABLED — verified on-screen 2026-06-15. By the nature of this business domain the
...                 (flowline × day) row is PRE-INSTANTIATED by EC batch processes; the screen does NOT
...                 create or delete records, you only EDIT the measured values. So there is no
...                 record-level Insert/Delete to test here (unlike the master-data IUD screens, e.g. Bank).
...
...                 The suite exercises the full EDIT capability of the measured cell On Strm[hr]
...                 (= IFLW_DAY_STATUS.ON_STREAM_HRS, unitless): set a value, change it, and clear it
...                 (clear+Save → DB NULL — still an UPDATE of the existing row, not a delete). Every step
...                 is verified at the DB (the trustworthy oracle, not the optimistic grid). Null-original,
...                 so clearing at the end restores the original state (self-cleaning).
...                 Layered: this test → iflw_water_flowline_status_page (T3) → daily_status_grid (T2) +
...                 common (T1) + DbVerify.

Resource            ../../../../../pageobjects/EC_Production/Well_and_Reservoir/Daily/Group_Model_-_by_Flowline/iflw_water_flowline_status_page.resource

Suite Setup         Open Water Injection Flowline Screen
Suite Teardown      Run Keywords    Restore Water Injection Flowline Cell To Null    AND    Close EC

Test Tags           n1    daily_water_injection_flowline_status    update_only


*** Variables ***
${SET_VALUE}        18
${CHANGE_VALUE}     24


*** Test Cases ***
TC01 Grid Loads For Scope
    [Documentation]    The date-range + 4-level cascade (PU → Area → Facility → Flowline) + GO renders
    ...    the pre-instantiated water-injection flowline daily row.
    [Tags]    smoke
    ${rows}=    Get Table Rows    ${IFLW_GRID}
    Should Not Be Empty    ${rows}    msg=No flowline row rendered for the navigator scope/date
    Capture Step    iflw_water_tc01_grid_loaded

TC02 Set Daily Value Persists
    [Documentation]    EDIT — set On Strm[hr]=${SET_VALUE} on the (empty) cell, Save, and DB-verify
    ...    IFLW_DAY_STATUS.ON_STREAM_HRS holds it. (Also proves C2 = ON_STREAM_HRS.)
    [Tags]    update
    Water Injection Flowline Value Should Be In DB    ${None}
    Set Flowline Daily Value    ${SET_VALUE}
    Water Injection Flowline Cell Should Show    ${SET_VALUE}
    Water Injection Flowline Value Should Be In DB    ${SET_VALUE}
    Capture Step    iflw_water_tc02_set

TC03 Change Daily Value Persists
    [Documentation]    EDIT — change On Strm[hr] to ${CHANGE_VALUE}, Save, DB-verify the new value persisted.
    [Tags]    update
    Set Flowline Daily Value    ${CHANGE_VALUE}
    Water Injection Flowline Cell Should Show    ${CHANGE_VALUE}
    Water Injection Flowline Value Should Be In DB    ${CHANGE_VALUE}
    Capture Step    iflw_water_tc03_changed

TC04 Clear Daily Value Persists
    [Documentation]    EDIT — clear the cell + Save; DB-verify ON_STREAM_HRS is back to NULL. Still an
    ...    UPDATE of the existing row (the record is NOT deleted — no record delete on this screen); this
    ...    also returns the row to its original state (self-cleaning).
    [Tags]    update
    Clear Flowline Daily Value
    Water Injection Flowline Value Should Be In DB    ${None}
    Capture Step    iflw_water_tc04_cleared
