*** Settings ***
Documentation       T3 (screen) — Object List Setup page object.
...                 Screen: Configuration > Assets > Basic Objects > Object List Setup.
...                 PARENT-CHILD setup screen (new pattern): navigator picks List Class +
...                 Object List + GO, then the chosen list's ITEMS show in an inline grid
...                 (TV-style cells). Insert/Delete toolbar acts on "Object List Item".
...                 DB oracle: count-delta on OBJECT_LIST_SETUP.GENERIC_OBJECT_CODE.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/table_class.resource


*** Variables ***
${OLS_SCREEN}                   Object List Setup
${OLS_TABLE}                    tab:tabPanel:object_list_table:form:T_data
# navigator dropdowns — BOTH mandatory before the item grid loads
${OLS_NAV_CLASS}                nav:form:G:1:R:1:C:0:dd
${OLS_NAV_LIST}                 nav:form:G:2:R:1:C:0:dd
# item-row cell id parts: tab:tabPanel:object_list_table:form:T:{row}:C{col}...
${OLS_CELL_PREFIX}              tab:tabPanel:object_list_table:form:T
${OLS_OBJECT_CELL_SUFFIX}       C2_dd_input
${OLS_DB_TABLE}                 OBJECT_LIST_SETUP
${OLS_DB_COLUMN}                GENERIC_OBJECT_CODE


*** Keywords ***
Open Object List Setup Screen
    [Documentation]    Suite Setup: launch, login, navigate, select List Class +
    ...    Object List in the navigator and apply (item grid is empty until then).
    [Arguments]    ${list_class}    ${object_list}    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${OLS_SCREEN}    ${user}    ${pass}
    Select EC Dropdown Option    ${OLS_NAV_CLASS}    ${list_class}
    Select EC Dropdown Option    ${OLS_NAV_LIST}    ${object_list}
    Apply Navigator

Item Count In DB
    [Documentation]    Count OBJECT_LIST_SETUP rows whose member object code is ${object_code}
    ...    (across all lists — callers assert DELTAS, so pre-existing rows never matter).
    [Arguments]    ${object_code}
    ${n}=    View Count Where    ${OLS_DB_TABLE}    ${OLS_DB_COLUMN}    ${object_code}
    RETURN    ${n}

Item Count In DB Should Be
    [Documentation]    Assert the member-code count equals ${expected}.
    [Arguments]    ${object_code}    ${expected}
    View Count Where Should Be    ${OLS_DB_TABLE}    ${OLS_DB_COLUMN}    ${object_code}    ${expected}

Insert Object List Item
    [Documentation]    Insert toolbar -> "Object List Item" -> find the blank row ->
    ...    pick the member object in its dropdown cell, RE-FIND the row (selection can
    ...    re-index the grid), fill the start date (calendar or text cell) -> Save.
    [Arguments]    ${object_label}    ${start_date}    ${sort_order}=999
    Insert New Grid Row By Label    Object List Item
    ${row}=    Find Grid Row By Cell Input Value    ${OLS_TABLE}    ${OLS_OBJECT_CELL_SUFFIX}    ${EMPTY}
    Should Be True    ${row} >= 0    msg=No blank item row appeared after Insert
    Select EC Dropdown Option    ${OLS_CELL_PREFIX}:${row}:C2_dd    ${object_label}
    ${row}=    Find Grid Row By Cell Input Value    ${OLS_TABLE}    ${OLS_OBJECT_CELL_SUFFIX}    ${object_label}
    Should Be True    ${row} >= 0    msg=Item row vanished after object selection
    Fill Item Row Date And Sort    ${row}    ${start_date}    ${sort_order}
    Save
    Refresh Screen

Fill Item Row Date And Sort
    [Documentation]    Fill the new item row's start date (calendar or text cell) and
    ...    Sort Order (C5 renders MANDATORY/yellow on a new row - must be filled).
    [Arguments]    ${row}    ${start_date}    ${sort_order}
    ${has_cal}=    Get Element Count    css=[id="${OLS_CELL_PREFIX}:${row}:C0_da_input"]
    IF    ${has_cal} > 0
        Fill EC Date    ${OLS_CELL_PREFIX}:${row}:C0_da_input    ${start_date}
    ELSE
        Type Cell By Id    ${OLS_CELL_PREFIX}:${row}:C0_in    ${start_date}
    END
    Type Cell By Id    ${OLS_CELL_PREFIX}:${row}:C5_in    ${sort_order}

Select Object List Item Row
    [Documentation]    Click the row whose object cell shows ${object_value} so the
    ...    toolbar Delete acts on it. Fails if the row is not found.
    [Arguments]    ${object_value}
    ${row}=    Find Grid Row By Cell Input Value    ${OLS_TABLE}    ${OLS_OBJECT_CELL_SUFFIX}    ${object_value}
    Should Be True    ${row} >= 0    msg=Item row with object ${object_value} not found in grid
    Click    css=[id="${OLS_CELL_PREFIX}:${row}:C0_in"]
    Sleep    0.8s

Delete Object List Item
    [Documentation]    Select the item row, Delete toolbar -> "Object List Item" -> Save.
    [Arguments]    ${object_value}
    Select Object List Item Row    ${object_value}
    Delete Selected Grid Row    Object List Item
    Save
    Refresh Screen

Item Row Should Exist
    [Documentation]    Assert an item row whose object cell shows ${object_value} is present.
    [Arguments]    ${object_value}
    ${row}=    Find Grid Row By Cell Input Value    ${OLS_TABLE}    ${OLS_OBJECT_CELL_SUFFIX}    ${object_value}
    Should Be True    ${row} >= 0    msg=Expected item row ${object_value} in ${OLS_TABLE}

Item Row Should Not Exist
    [Documentation]    Assert no item row shows ${object_value} in its object cell.
    [Arguments]    ${object_value}
    ${row}=    Find Grid Row By Cell Input Value    ${OLS_TABLE}    ${OLS_OBJECT_CELL_SUFFIX}    ${object_value}
    Should Be Equal As Integers    ${row}    -1    msg=Item row ${object_value} should NOT exist
