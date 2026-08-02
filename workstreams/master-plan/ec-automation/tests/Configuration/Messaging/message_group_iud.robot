*** Settings ***
Documentation       EC IUD Test - Message Group (Configuration > Messaging).
...                 OV-GM (manage-object, groupmodel): grid filtered by the navigator cascade.
...                 DELETE = End Date = Start Date (true delete in OV_MESSAGE_GROUP). NEVER touch existing data;
...                 a unique AUTOTEST_MG<timestamp> code is generated per run.

Resource            ../../../pageobjects/Configuration/Messaging/message_group_page.resource

Suite Setup         Set Up Message Group Suite
Suite Teardown      Close EC

Test Tags           iud    message_group


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       2003-01-01
${END_DATE}         2000-01-01


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test object does not exist before inserting.
    [Tags]    clean-state
    Message Group Row Should Not Exist    ${TEST_CODE}
    Capture Step    message_group_tc01_clean

TC02 Insert New Message Group
    [Documentation]    Insert under the navigator scope and confirm it lists.
    [Tags]    insert
    Insert Message Group Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Message Group Row Should Exist    ${TEST_CODE}
    Message Group Should Exist In DB    ${TEST_CODE}
    Capture Step    message_group_tc02_inserted

TC03 Update Message Group Name
    [Documentation]    Edit the name and confirm the list reflects the change.
    [Tags]    update
    Update Message Group Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Message Group Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    message_group_tc03_updated

TC04 Delete Message Group
    [Documentation]    Delete via End Date = Start Date and confirm it is gone.
    [Tags]    delete    cleanup
    Delete Message Group    ${TEST_CODE}    ${END_DATE}
    Message Group Row Should Not Exist    ${TEST_CODE}
    Message Group Should Not Exist In DB    ${TEST_CODE}
    Capture Step    message_group_tc04_deleted


*** Keywords ***
Set Up Message Group Suite
    [Documentation]    Generate a unique test code/name, open the screen, fill the navigator cascade.
    Prepare IUD Object Data    AUTOTEST_MG    Name
    ${pu}=    Open Message Group Screen
    VAR    ${GM_PU}    ${pu}    scope=SUITE
