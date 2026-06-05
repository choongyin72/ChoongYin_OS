*** Settings ***
Documentation    Object Partition test suite — Role assignment per object
...              Tests: idempotent insert, verify in grid, remove role
...              Uses AUTOTEST_ prefix for all test data
Library          Browser
Resource         ../../resources/keywords/LoginKeywords.resource
Resource         ../../resources/keywords/ObjectPartitionKeywords.resource
Resource         ../../resources/variables/common_variables.robot
Variables        ../../vars/local.py

Suite Setup      Run Keywords
...              Open EC Browser Session
...              AND    Log In To EC    ${EC_USERNAME}    ${EC_PASSWORD}
...              AND    Navigate To Object Partition Screen
Suite Teardown   Close Browser
Test Setup       Ensure Role Does Not Exist For Operator    OPS_ENGINEER    AUTOTEST_ROLE_001
Test Teardown    Run Keywords
...              Ensure Role Does Not Exist For Operator    OPS_ENGINEER    AUTOTEST_ROLE_001
...              AND    Run Keyword If Test Failed
...                     Take Screenshot    ${OUTPUT_DIR}${/}${SUITE_NAME}_${TEST_NAME}_failure

*** Test Cases ***

TC_OP_01 Insert Role For Operator Is Idempotent
    [Documentation]    Insert AUTOTEST_ROLE_001 for OPS_ENGINEER.
    ...                Should succeed whether or not role already exists.
    [Tags]    object_partition    insert    smoke
    Insert Role For Operator    OPS_ENGINEER    AUTOTEST_ROLE_001
    Verify Role Exists For Operator    AUTOTEST_ROLE_001

TC_OP_02 Verify Role Appears In Grid After Insert
    [Documentation]    After insert, grid row must be visible.
    [Tags]    object_partition    verify
    Insert Role For Operator    OPS_ENGINEER    AUTOTEST_ROLE_001
    Verify Role Exists For Operator    AUTOTEST_ROLE_001

TC_OP_03 Remove Role From Operator
    [Documentation]    Insert then remove AUTOTEST_ROLE_001 — grid row must disappear.
    [Tags]    object_partition    delete
    Insert Role For Operator    OPS_ENGINEER    AUTOTEST_ROLE_001
    Verify Role Exists For Operator    AUTOTEST_ROLE_001
    Remove Role From Operator    AUTOTEST_ROLE_001
    Verify Row Not In Grid    AUTOTEST_ROLE_001

*** Keywords ***

Open EC Browser Session
    IF    '${HEADLESS}' == 'True'
        New Browser    chromium    headless=True
        New Context    ignoreHTTPSErrors=True    viewport={"width": 1920, "height": 1080}
    ELSE
        ${args}=    Create List    --start-maximized
        New Browser    chromium    headless=False    args=${args}
        New Context    ignoreHTTPSErrors=True    viewport=${None}
    END
