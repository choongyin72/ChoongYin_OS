*** Settings ***
Documentation       EC N1 Test — "Daily Gas Injection Flowline, by Flowline" (edit-in-place).
...                 ⚠️ UPDATE-ONLY: the New (insert) and Delete toolbar icons are DISABLED — the
...                 (flowline × day) row is PRE-INSTANTIATED by EC batch processes; the screen does NOT
...                 create or delete records (by the business-domain nature), you only EDIT the measured
...                 values. Sibling of the Water-Injection / Production flowline screens (same grid
...                 component); gas-injection rows live in IFLW_DAY_STATUS with INJ_TYPE='GI'.
...
...                 The suite exercises the full EDIT capability of On Strm[hr] (= ON_STREAM_HRS,
...                 unitless): set a value, change it, and clear it (clear+Save → DB NULL, still an
...                 UPDATE of the existing row, not a delete). Every step is DB-verified (the trustworthy
...                 oracle). Null-original, so clearing restores the original state (self-cleaning).
...                 Layered: this test → giflw_gas_flowline_status_page (T3) → daily_status_grid (T2) +
...                 common (T1) + DbVerify.

Resource            ../../../../../pageobjects/EC_Production/Well_and_Reservoir/Daily/Group_Model_-_by_Flowline/giflw_gas_flowline_status_page.resource

Suite Setup         Open Gas Injection Flowline Screen
Suite Teardown      Run Keywords    Restore Gas Injection Flowline Cell To Null    AND    Close EC

Test Tags           n1    daily_gas_injection_flowline_status    update_only


*** Variables ***
${SET_VALUE}        18
${CHANGE_VALUE}     24


*** Test Cases ***
TC01 Grid Loads For Scope
    [Documentation]    The date-range + 4-level cascade (PU → Area → Facility → Flowline) + GO renders
    ...    the pre-instantiated gas-injection flowline daily row.
    [Tags]    smoke
    ${rows}=    Get Table Rows    ${GIFLW_GRID}
    Should Not Be Empty    ${rows}    msg=No flowline row rendered for the navigator scope/date
    Capture Step    giflw_gas_tc01_grid_loaded

TC02 Set Daily Value Persists
    [Documentation]    EDIT — set On Strm[hr]=${SET_VALUE} on the (empty) cell, Save, DB-verify
    ...    IFLW_DAY_STATUS.ON_STREAM_HRS holds it. (Also proves C2 = ON_STREAM_HRS.)
    [Tags]    update
    Gas Injection Flowline Value Should Be In DB    ${None}
    Set Gas Flowline Daily Value    ${SET_VALUE}
    Gas Injection Flowline Cell Should Show    ${SET_VALUE}
    Gas Injection Flowline Value Should Be In DB    ${SET_VALUE}
    Capture Step    giflw_gas_tc02_set

TC03 Change Daily Value Persists
    [Documentation]    EDIT — change On Strm[hr] to ${CHANGE_VALUE}, Save, DB-verify the new value persisted.
    [Tags]    update
    Set Gas Flowline Daily Value    ${CHANGE_VALUE}
    Gas Injection Flowline Cell Should Show    ${CHANGE_VALUE}
    Gas Injection Flowline Value Should Be In DB    ${CHANGE_VALUE}
    Capture Step    giflw_gas_tc03_changed

TC04 Clear Daily Value Persists
    [Documentation]    EDIT — clear the cell + Save; DB-verify ON_STREAM_HRS is back to NULL. Still an
    ...    UPDATE of the existing row (no record delete); also restores the original state (self-cleaning).
    [Tags]    update
    Clear Gas Flowline Daily Value
    Gas Injection Flowline Value Should Be In DB    ${None}
    Capture Step    giflw_gas_tc04_cleared
