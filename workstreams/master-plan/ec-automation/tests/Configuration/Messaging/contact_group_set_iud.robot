*** Settings ***
Documentation       EC IUD Test - Maintain Contact Group Set (Configuration > Messaging).
...                 OV-GM (manage-object, groupmodel): grid filtered by the navigator cascade.
...                 DELETE = End Date = Start Date (true delete in OV_CONTACT_GROUP_SET). NEVER touch existing data;
...                 a unique AUTOTEST_CGS_<timestamp> code is generated per run.

Resource            ../../../pageobjects/Configuration/Messaging/contact_group_set_page.resource

Suite Setup         Set Up Maintain Contact Group Set Suite
Suite Teardown      Close EC

Test Tags           iud    contact_group_set


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       2020-01-01
${END_DATE}         2000-01-01


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test object does not exist before inserting.
    [Tags]    clean-state
    Maintain Contact Group Set Row Should Not Exist    ${TEST_CODE}
    Capture Step    contact_group_set_tc01_clean

TC02 Insert New Maintain Contact Group Set
    [Documentation]    Insert under the navigator scope and confirm it lists.
    [Tags]    insert
    Insert Maintain Contact Group Set Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Maintain Contact Group Set Row Should Exist    ${TEST_CODE}
    Maintain Contact Group Set Should Exist In DB    ${TEST_CODE}
    Capture Step    contact_group_set_tc02_inserted

TC03 Update Maintain Contact Group Set Name
    [Documentation]    Edit the name and confirm the list reflects the change.
    [Tags]    update
    Update Maintain Contact Group Set Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Maintain Contact Group Set Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    contact_group_set_tc03_updated

TC04 Delete Maintain Contact Group Set
    [Documentation]    Delete via End Date = Start Date and confirm it is gone.
    [Tags]    delete    cleanup
    Delete Maintain Contact Group Set    ${TEST_CODE}    ${END_DATE}
    Maintain Contact Group Set Row Should Not Exist    ${TEST_CODE}
    Maintain Contact Group Set Should Not Exist In DB    ${TEST_CODE}
    Capture Step    contact_group_set_tc04_deleted


*** Keywords ***
Set Up Maintain Contact Group Set Suite
    [Documentation]    Generate a unique test code/name, open the screen, fill the navigator cascade.
    Prepare IUD Object Data    AUTOTEST_CGS_    Name
    ${pu}=    Open Maintain Contact Group Set Screen
    VAR    ${GM_PU}    ${pu}    scope=SUITE
