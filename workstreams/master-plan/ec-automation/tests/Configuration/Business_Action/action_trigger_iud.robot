*** Settings ***
Documentation       EC IUD Test - Action Trigger (Configuration > Business Action).
...                 CUSTOM-URL OV: grid nav:form:T_data, no navigator/GO (toolbar Refresh reload).
...                 DELETE = End Date = Start Date (true delete in OV_CONTROL_POINT, VERSIONED).
...                 NEVER touch existing data; a unique AUTOTEST_AT_<timestamp> code per run.
...                 5 mandatory fields: Code, Name, Start date, Action Trigger Type, Trigger Type -
...                 neither dropdown is scope-dependent (no navigator), both probed live non-empty.
...                 Insert/Update route through the opt-in mandatory-field gate
...                 (mandatory_field_gate.resource) before Save - see the page object's docstring.

Resource            ../../../pageobjects/Configuration/Business_Action/action_trigger_page.resource

Suite Setup         Set Up Action Trigger Suite
Suite Teardown      Close EC

Test Tags           iud    action-trigger


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       2000-01-01
${END_DATE}         2000-01-01


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test object does not exist before inserting.
    [Tags]    clean-state
    Action Trigger Row Should Not Exist    ${TEST_CODE}
    Capture Step    action_trigger_tc01_clean

TC02 Insert New Action Trigger
    [Documentation]    Insert (opt-in mandatory-field gate runs before Save) and confirm it lists.
    [Tags]    insert
    Insert Action Trigger Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Action Trigger Row Should Exist    ${TEST_CODE}
    Action Trigger Should Exist In DB    ${TEST_CODE}
    Capture Step    action_trigger_tc02_inserted

TC03 Update Action Trigger Name
    [Documentation]    Edit the name and confirm the list reflects the change.
    [Tags]    update
    Update Action Trigger Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Action Trigger Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    action_trigger_tc03_updated

TC04 Delete Action Trigger
    [Documentation]    Delete via End Date = Start Date and confirm it is gone.
    [Tags]    delete    cleanup
    Delete Action Trigger    ${TEST_CODE}    ${END_DATE}
    Action Trigger Row Should Not Exist    ${TEST_CODE}
    Action Trigger Should Not Exist In DB    ${TEST_CODE}
    Capture Step    action_trigger_tc04_deleted


*** Keywords ***
Set Up Action Trigger Suite
    [Documentation]    Generate a unique test code/name, open the screen (no navigator to fill).
    Prepare IUD Object Data    AUTOTEST_AT_    Action Trigger
    Open Action Trigger Screen
