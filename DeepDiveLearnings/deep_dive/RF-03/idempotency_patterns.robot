*** Settings ***
Documentation    Idempotency Patterns — EC Robot Framework
...              Demonstrates: ensure-state pattern, AUTOTEST_ prefix,
...              setup+teardown symmetry, Run Keyword And Continue On Failure
Library          Browser
Resource         ../RF-02/ec_project_scaffold/resources/keywords/ObjectPartitionKeywords.resource
Resource         ../RF-02/ec_project_scaffold/resources/variables/common_variables.robot
Variables        ../RF-02/ec_project_scaffold/vars/local.py

# Both setup AND teardown clean — test can be re-run any number of times
Test Setup       Ensure Role Does Not Exist For Operator    OPS_ENGINEER    AUTOTEST_ROLE_001
Test Teardown    Run Keywords
...              Run Keyword And Continue On Failure
...                  Ensure Role Does Not Exist For Operator    OPS_ENGINEER    AUTOTEST_ROLE_001
...              AND    Run Keyword If Test Failed
...                  Take Screenshot    ${OUTPUT_DIR}${/}${SUITE_NAME}_${TEST_NAME}_failure

*** Test Cases ***

TC_Idempotent_Insert Role Is Safe To Run Multiple Times
    [Documentation]    Insert AUTOTEST_ROLE_001 — safe even if role already exists.
    [Tags]    idempotency    demo
    # This is safe to run multiple times
    Insert Role For Operator    OPS_ENGINEER    AUTOTEST_ROLE_001
    Verify Role Exists For Operator    AUTOTEST_ROLE_001
    # If run again immediately, setup cleans up, test inserts again → always passes

TC_Idempotent_Delete Is Safe When Role Does Not Exist
    [Documentation]    Ensure role deleted — does not fail if role was never inserted.
    [Tags]    idempotency    demo
    # This should pass even if role doesn't exist
    Ensure Role Does Not Exist For Operator    OPS_ENGINEER    AUTOTEST_ROLE_NOT_REAL

*** Keywords ***

Ensure Role Does Not Exist For Operator
    [Documentation]    Idempotent cleanup — deletes role if it exists, no-op if absent.
    ...                Safe to call in setup AND teardown.
    [Arguments]    ${operator}    ${role}
    ${exists}=    Row Exists In Grid    ${role}
    IF    ${exists}
        Remove Role From Operator    ${role}
        # Verify cleanup succeeded
        Verify Row Not In Grid    ${role}
    ELSE
        Log    Role '${role}' does not exist — no cleanup needed
    END

Row Exists In Grid
    [Documentation]    Returns ${True}/${False} — does row with text exist in grid?
    [Arguments]    ${row_text}
    ${count}=    Get Element Count    xpath=//tr[@data-rk and contains(.,'${row_text}')]
    ${exists}=    Evaluate    ${count} > 0
    RETURN    ${exists}
