*** Settings ***
Documentation    Layer 2 (Keywords) — Business-level Object Partition operations.
...              All logic delegates to page layer — no direct selectors here.
Resource         ../pages/ObjectPartitionPage.resource
Resource         ../variables/common_variables.robot
Resource         ../variables/object_partition_variables.robot

*** Keywords ***

Navigate To Object Partition Screen
    [Documentation]    Search sidebar and open Object Partition screen.
    Wait For Elements State    ${SEARCH_INPUT}    visible    timeout=${WAIT_TIMEOUT}
    Click    ${SEARCH_INPUT}
    Clear Text    ${SEARCH_INPUT}
    Type Text    ${SEARCH_INPUT}    ${OP_SCREEN_NAME}    delay=50ms
    Wait For Load State    networkidle    timeout=15s
    ${link}=    Set Variable
    ...    xpath=//label[contains(@class,'tv-link') and normalize-space(.)='${OP_SCREEN_NAME}']
    Wait For Elements State    ${link}    visible    timeout=15s
    Click    ${link}
    Wait For Load State    networkidle    timeout=30s

Insert Role For Operator
    [Documentation]    Select operator and role, then click Insert.
    ...                Pre-condition: Object Partition screen is open.
    ...                Post-condition: Role is inserted in the grid.
    [Arguments]    ${operator}    ${role}
    Select Operator    ${operator}
    Select Role        ${role}
    Click Insert Button

Verify Role Exists For Operator
    [Documentation]    Assert the role row exists in the grid.
    [Arguments]    ${role}
    Verify Row In Grid    ${role}

Remove Role From Operator
    [Documentation]    Delete the role row from the grid.
    [Arguments]    ${role}
    Delete Row From Grid    ${role}

Ensure Role Does Not Exist For Operator
    [Documentation]    Idempotent cleanup — delete role if it exists.
    ...                Safe to call in setup or teardown even if role was never inserted.
    [Arguments]    ${operator}    ${role}
    ${exists}=    Row Exists In Grid    ${role}
    IF    ${exists}
        Remove Role From Operator    ${role}
        Verify Row Not In Grid    ${role}
    END

Verify Row Not In Grid
    [Documentation]    Assert role is NOT in the grid.
    [Arguments]    ${role}
    Verify Row Not In Grid    ${role}
