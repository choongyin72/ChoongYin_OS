*** Settings ***
Documentation       EC IUD Test - Channel (Configuration > Assets > Transport_Objects).
...                 OV-GM (manage-object, groupmodel): grid filtered by the navigator cascade.
...                 DELETE = End Date = Start Date (true delete in OV_CHANNEL). NEVER touch existing data;
...                 a unique AUTOTEST_CHN_<timestamp> code is generated per run.

Resource            ../../../../pageobjects/Configuration/Assets/Transport_Objects/channel_page.resource

Suite Setup         Set Up Channel Suite
Suite Teardown      Close EC

Test Tags           iud    channel


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
    Channel Row Should Not Exist    ${TEST_CODE}
    Capture Step    channel_tc01_clean

TC02 Insert New Channel
    [Documentation]    Insert under the navigator scope and confirm it lists.
    [Tags]    insert
    Insert Channel Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Channel Row Should Exist    ${TEST_CODE}
    Channel Should Exist In DB    ${TEST_CODE}
    Capture Step    channel_tc02_inserted

TC03 Update Channel Name
    [Documentation]    Edit the name and confirm the list reflects the change.
    [Tags]    update
    Update Channel Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Channel Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    channel_tc03_updated

TC04 Delete Channel
    [Documentation]    Delete via End Date = Start Date and confirm it is gone.
    [Tags]    delete    cleanup
    Delete Channel    ${TEST_CODE}    ${END_DATE}
    Channel Row Should Not Exist    ${TEST_CODE}
    Channel Should Not Exist In DB    ${TEST_CODE}
    Capture Step    channel_tc04_deleted


*** Keywords ***
Set Up Channel Suite
    [Documentation]    Generate a unique test code/name, open the screen, fill the navigator cascade.
    Prepare IUD Object Data    AUTOTEST_CHN_    Channel
    ${pu}=    Open Channel Screen
    VAR    ${GM_PU}    ${pu}    scope=SUITE
