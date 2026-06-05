*** Settings ***
Documentation    Layer 3 (Pages) — Object Partition screen interactions.
...              Uses selectors from variables/object_partition_variables.robot.
Library          Browser
Resource         ../variables/common_variables.robot
Resource         ../variables/object_partition_variables.robot

*** Keywords ***

Select Operator
    [Documentation]    Select an operator from the operator dropdown.
    [Arguments]    ${operator_name}
    Wait For Elements State    ${OP_OPERATOR_DROPDOWN}    visible    timeout=${WAIT_TIMEOUT}
    Select Options By    ${OP_OPERATOR_DROPDOWN}    label    ${operator_name}
    Wait For Load State    networkidle    timeout=${AJAX_TIMEOUT}

Select Role
    [Documentation]    Select a role from the role dropdown.
    [Arguments]    ${role_name}
    Wait For Elements State    ${OP_ROLE_DROPDOWN}    visible    timeout=${WAIT_TIMEOUT}
    Select Options By    ${OP_ROLE_DROPDOWN}    label    ${role_name}

Click Insert Button
    [Documentation]    Click the insert/add button and wait for grid refresh.
    Wait For Elements State    ${OP_INSERT_BTN}    visible    timeout=${WAIT_TIMEOUT}
    Click    ${OP_INSERT_BTN}
    Wait For Load State    networkidle    timeout=${AJAX_TIMEOUT}

Verify Row In Grid
    [Documentation]    Assert a row containing text is visible in the data grid.
    [Arguments]    ${row_text}
    ${row}=    Set Variable    xpath=//tr[@data-rk and contains(.,'${row_text}')]
    Wait For Elements State    ${row}    visible    timeout=${WAIT_TIMEOUT}

Verify Row Not In Grid
    [Documentation]    Assert no row with text exists in the grid.
    [Arguments]    ${row_text}
    ${count}=    Get Element Count    xpath=//tr[@data-rk and contains(.,'${row_text}')]
    Should Be Equal As Numbers    ${count}    0
    ...    msg=Expected row '${row_text}' not to exist but found ${count} rows

Delete Row From Grid
    [Documentation]    Click delete button on the row containing text.
    [Arguments]    ${row_text}
    ${delete_btn}=    Set Variable
    ...    xpath=//tr[@data-rk and contains(.,'${row_text}')]//button[contains(@id,'delete') or @title='Delete']
    Wait For Elements State    ${delete_btn}    visible    timeout=${WAIT_TIMEOUT}
    Click    ${delete_btn}
    Wait For Load State    networkidle    timeout=${AJAX_TIMEOUT}

Row Exists In Grid
    [Documentation]    Returns True/False whether a row with text exists.
    [Arguments]    ${row_text}
    ${count}=    Get Element Count    xpath=//tr[@data-rk and contains(.,'${row_text}')]
    ${exists}=    Evaluate    ${count} > 0
    RETURN    ${exists}
