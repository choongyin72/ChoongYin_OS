*** Settings ***
Documentation       T3 (screen) - Unit - Well Setup page object.
...                 Screen: Configuration > Assets > Royalty Objects > Unit - Well Setup.
...                 PARENT-CHILD setup screen (PC pattern, same family as Object List
...                 Setup): the navigator picks a form date + a Unit Agreement and GO,
...                 then that agreement's WELL SETUP rows show in an inline grid (TV-style
...                 cells). Insert/Delete toolbar acts on "Well Setup"; each row links a
...                 Perf Interval (the member) to the Unit Agreement (the parent).
...                 DB oracle: count-delta on DV_UNIT_WELL_SETUP.PERF_INTERVAL_CODE.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/table_class.resource


*** Variables ***
${UWS_SCREEN}               Unit - Well Setup
${UWS_TABLE}                well_setup:form:T_data
# navigator: form date (G:0) + Unit Agreement dropdown (G:1) - BOTH precede the grid
${UWS_NAV_DATE}             nav:form:G:0:R:1:C:0:da_input
${UWS_NAV_UA}               nav:form:G:1:R:1:C:0:dd
# well-setup row cell id parts: well_setup:form:T:{row}:C{col}...
${UWS_CELL_PREFIX}          well_setup:form:T
${UWS_PI_CELL_SUFFIX}       C2_dd_input
${UWS_DB_VIEW}              DV_UNIT_WELL_SETUP
${UWS_DB_COLUMN}            PERF_INTERVAL_CODE


*** Keywords ***
Open Unit Well Setup Screen
    [Documentation]    Suite Setup: launch, login, navigate, set the form date + select
    ...    the Unit Agreement in the navigator and apply (the grid is empty until then).
    ...    The date must sit inside the agreement's effective window (UNIT_3 starts 2010).
    [Arguments]    ${unit_agreement}    ${form_date}    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${UWS_SCREEN}    ${user}    ${pass}
    Fill EC Date    ${UWS_NAV_DATE}    ${form_date}
    Select EC Dropdown Option    ${UWS_NAV_UA}    ${unit_agreement}
    Apply Navigator

Perf Interval Count In DB
    [Documentation]    Count DV_UNIT_WELL_SETUP rows whose member is ${perf_code}
    ...    (across all agreements - callers assert DELTAS, so pre-existing rows never matter).
    [Arguments]    ${perf_code}
    ${n}=    View Count Where    ${UWS_DB_VIEW}    ${UWS_DB_COLUMN}    ${perf_code}
    RETURN    ${n}

Perf Interval Count In DB Should Be
    [Documentation]    Assert the member-code count equals ${expected}.
    [Arguments]    ${perf_code}    ${expected}
    View Count Where Should Be    ${UWS_DB_VIEW}    ${UWS_DB_COLUMN}    ${perf_code}    ${expected}

Insert Well Setup
    [Documentation]    Insert toolbar -> "Well Setup" -> find the blank row -> pick the
    ...    Perf Interval in its dropdown cell, RE-FIND the row (selection can re-index the
    ...    grid), fill the start date -> Save -> Refresh.
    [Arguments]    ${perf_label}    ${start_date}
    Insert New Grid Row By Label    Well Setup
    ${row}=    Find Grid Row By Cell Input Value    ${UWS_TABLE}    ${UWS_PI_CELL_SUFFIX}    ${EMPTY}
    Should Be True    ${row} >= 0    msg=No blank well-setup row appeared after Insert
    Select EC Dropdown Option    ${UWS_CELL_PREFIX}:${row}:C2_dd    ${perf_label}
    ${row}=    Find Grid Row By Cell Input Value    ${UWS_TABLE}    ${UWS_PI_CELL_SUFFIX}    ${perf_label}
    Should Be True    ${row} >= 0    msg=Well-setup row vanished after Perf Interval selection
    Fill EC Date    ${UWS_CELL_PREFIX}:${row}:C0_da_input    ${start_date}
    Save
    Refresh Screen

Select Well Setup Row
    [Documentation]    Click the row whose Perf Interval cell shows ${perf_value} so the
    ...    toolbar Delete acts on it. Fails if the row is not found.
    [Arguments]    ${perf_value}
    ${row}=    Find Grid Row By Cell Input Value    ${UWS_TABLE}    ${UWS_PI_CELL_SUFFIX}    ${perf_value}
    Should Be True    ${row} >= 0    msg=Well-setup row with Perf Interval ${perf_value} not found in grid
    # a SAVED row renders its start-date as a TEXT cell C0_in (a NEW row shows the
    # calendar C0_da_input) - click C0_in to select the persisted row for delete
    Click    css=[id="${UWS_CELL_PREFIX}:${row}:C0_in"]
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
    ${row}=    Find Grid Row By Cell Input Value    ${UWS_TABLE}    ${UWS_PI_CELL_SUFFIX}    ${perf_value}
    Should Be True    ${row} >= 0    msg=Expected well-setup row ${perf_value} in ${UWS_TABLE}

Well Setup Row Should Not Exist
    [Documentation]    Assert no row shows ${perf_value} in its Perf Interval cell.
    [Arguments]    ${perf_value}
    ${row}=    Find Grid Row By Cell Input Value    ${UWS_TABLE}    ${UWS_PI_CELL_SUFFIX}    ${perf_value}
    Should Be Equal As Integers    ${row}    -1    msg=Well-setup row ${perf_value} should NOT exist
