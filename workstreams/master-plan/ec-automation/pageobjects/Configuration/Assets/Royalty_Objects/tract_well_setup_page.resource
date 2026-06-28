*** Settings ***
Documentation       T3 (screen) - Tract - Well Setup page object.
...                 Screen: Configuration > Assets > Royalty Objects > Tract - Well Setup.
...                 PARENT-CHILD setup screen (PC, sibling of Unit - Well Setup over the same
...                 WELL_SETUP base): the navigator CASCADES Unit Agreement -> Tract + GO,
...                 then that Tract's WELL SETUP rows show in an inline grid. Insert/Delete
...                 toolbar acts on "Well Setup"; each row links a Perf Interval (member) to
...                 the Tract (parent, OBJECT_CODE). DB oracle: count-delta on
...                 DV_TRACT_WELL_SETUP.PERF_INTERVAL_CODE.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/table_class.resource


*** Variables ***
${TWS_SCREEN}              Tract - Well Setup
${TWS_TABLE}              well_setup:form:T_data
# navigator CASCADE: form date (G:0) + Unit Agreement (G:1) + Tract (G:2) - Tract dd
# only populates after a Unit Agreement is picked
${TWS_NAV_DATE}           nav:form:G:0:R:1:C:0:da_input
${TWS_NAV_UA}             nav:form:G:1:R:1:C:0:dd
${TWS_NAV_TRACT}          nav:form:G:2:R:1:C:0:dd
${TWS_CELL_PREFIX}        well_setup:form:T
${TWS_PI_CELL_SUFFIX}     C2_dd_input
${TWS_DB_VIEW}            DV_TRACT_WELL_SETUP
${TWS_DB_COLUMN}          PERF_INTERVAL_CODE


*** Keywords ***
Open Tract Well Setup Screen
    [Documentation]    Suite Setup: launch, login, navigate, then CASCADE the navigator -
    ...    set form date, select the Unit Agreement (G:1), select the Tract (G:2, populated
    ...    only after the agreement) and apply. Date must sit inside the Tract's effective
    ...    window (the U3/U4 tracts start 2010).
    [Arguments]    ${unit_agreement}    ${tract}    ${form_date}    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${TWS_SCREEN}    ${user}    ${pass}
    Fill EC Date    ${TWS_NAV_DATE}    ${form_date}
    Select EC Dropdown Option    ${TWS_NAV_UA}    ${unit_agreement}
    Select EC Dropdown Option    ${TWS_NAV_TRACT}    ${tract}
    Apply Navigator

Perf Interval Count In DB
    [Documentation]    Count DV_TRACT_WELL_SETUP rows whose member is ${perf_code}
    ...    (across all tracts - callers assert DELTAS, so pre-existing rows never matter).
    [Arguments]    ${perf_code}
    ${n}=    View Count Where    ${TWS_DB_VIEW}    ${TWS_DB_COLUMN}    ${perf_code}
    RETURN    ${n}

Perf Interval Count In DB Should Be
    [Documentation]    Assert the member-code count equals ${expected}.
    [Arguments]    ${perf_code}    ${expected}
    View Count Where Should Be    ${TWS_DB_VIEW}    ${TWS_DB_COLUMN}    ${perf_code}    ${expected}

Insert Well Setup
    [Documentation]    Insert toolbar -> "Well Setup" -> find the blank row -> pick the
    ...    Perf Interval in its dropdown cell, RE-FIND the row (selection can re-index the
    ...    grid), fill the start date -> Save -> Refresh.
    [Arguments]    ${perf_label}    ${start_date}
    Insert New Grid Row By Label    Well Setup
    ${row}=    Find Grid Row By Cell Input Value    ${TWS_TABLE}    ${TWS_PI_CELL_SUFFIX}    ${EMPTY}
    Should Be True    ${row} >= 0    msg=No blank well-setup row appeared after Insert
    Select EC Dropdown Option    ${TWS_CELL_PREFIX}:${row}:C2_dd    ${perf_label}
    ${row}=    Find Grid Row By Cell Input Value    ${TWS_TABLE}    ${TWS_PI_CELL_SUFFIX}    ${perf_label}
    Should Be True    ${row} >= 0    msg=Well-setup row vanished after Perf Interval selection
    Fill EC Date    ${TWS_CELL_PREFIX}:${row}:C0_da_input    ${start_date}
    Save
    Refresh Screen

Update Well Setup Comments
    [Documentation]    UPDATE: on the SAVED membership row (found by Perf Interval), type a
    ...    new value into the COMMENTS cell (C3_in maps to DV_TRACT_WELL_SETUP.COMMENTS,
    ...    same WELL_SETUP base as Unit - Well Setup) -> Save -> Refresh.
    [Arguments]    ${perf_value}    ${comment}
    ${row}=    Find Grid Row By Cell Input Value    ${TWS_TABLE}    ${TWS_PI_CELL_SUFFIX}    ${perf_value}
    Should Be True    ${row} >= 0    msg=Well-setup row ${perf_value} not found to update
    Type Cell By Id    ${TWS_CELL_PREFIX}:${row}:C3_in    ${comment}
    Save
    Refresh Screen

Comment Should Be Present In DB
    [Documentation]    Assert the updated COMMENTS value persisted in DV_TRACT_WELL_SETUP
    ...    (scans the view's string columns - the sentinel is unique to COMMENTS).
    [Arguments]    ${comment}
    Code Should Be Present In View    ${TWS_DB_VIEW}    ${comment}

Comment Should Be Absent In DB
    [Documentation]    Assert the COMMENTS sentinel is NOT present in DV_TRACT_WELL_SETUP.
    [Arguments]    ${comment}
    Code Should Be Absent In View    ${TWS_DB_VIEW}    ${comment}

Select Well Setup Row
    [Documentation]    Click the row whose Perf Interval cell shows ${perf_value} so the
    ...    toolbar Delete acts on it. Fails if the row is not found.
    [Arguments]    ${perf_value}
    ${row}=    Find Grid Row By Cell Input Value    ${TWS_TABLE}    ${TWS_PI_CELL_SUFFIX}    ${perf_value}
    Should Be True    ${row} >= 0    msg=Well-setup row with Perf Interval ${perf_value} not found in grid
    # a SAVED row renders its start-date as a TEXT cell C0_in (a NEW row shows the
    # calendar C0_da_input) - click C0_in to select the persisted row for delete
    Click    css=[id="${TWS_CELL_PREFIX}:${row}:C0_in"]
    Sleep    0.8s

Delete Well Setup
    [Documentation]    Select the well-setup row, Delete toolbar -> "Well Setup" -> Save.
    [Arguments]    ${perf_value}
    Select Well Setup Row    ${perf_value}
    Delete Selected Grid Row    Well Setup
    Save
    Refresh Screen

Well Setup Row Should Exist
    [Documentation]    Assert a row whose Perf Interval cell shows ${perf_value} is present.
    [Arguments]    ${perf_value}
    ${row}=    Find Grid Row By Cell Input Value    ${TWS_TABLE}    ${TWS_PI_CELL_SUFFIX}    ${perf_value}
    Should Be True    ${row} >= 0    msg=Expected well-setup row ${perf_value} in ${TWS_TABLE}

Well Setup Row Should Not Exist
    [Documentation]    Assert no row shows ${perf_value} in its Perf Interval cell.
    [Arguments]    ${perf_value}
    ${row}=    Find Grid Row By Cell Input Value    ${TWS_TABLE}    ${TWS_PI_CELL_SUFFIX}    ${perf_value}
    Should Be Equal As Integers    ${row}    -1    msg=Well-setup row ${perf_value} should NOT exist
