*** Settings ***
Documentation       EC IUD Test - Loading Arm (Configuration > Assets > Transport_Objects).
...                 OV-GM (manage-object, groupmodel): grid filtered by the navigator cascade.
...                 DELETE = End Date = Start Date (true delete in OV_LOADING_ARM). NEVER touch existing data;
...                 a unique AUTOTEST_LA_<timestamp> code is generated per run.

Resource            ../../../../pageobjects/Configuration/Assets/Transport_Objects/loading_arm_page.resource

Suite Setup         Set Up Loading Arm Suite
Suite Teardown      Close EC

Test Tags           iud    loading_arm


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
    Loading Arm Row Should Not Exist    ${TEST_CODE}
    Capture Step    loading_arm_tc01_clean

TC02 Insert New Loading Arm
    [Documentation]    Insert under the navigator scope and confirm it lists.
    [Tags]    insert
    Insert Loading Arm Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Loading Arm Row Should Exist    ${TEST_CODE}
    Loading Arm Should Exist In DB    ${TEST_CODE}
    Capture Step    loading_arm_tc02_inserted

TC03 Update Loading Arm Name
    [Documentation]    Edit the name and confirm the list reflects the change.
    [Tags]    update
    Update Loading Arm Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Loading Arm Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    loading_arm_tc03_updated

TC04 Delete Loading Arm
    [Documentation]    Delete via End Date = Start Date and confirm it is gone.
    [Tags]    delete    cleanup
    Delete Loading Arm    ${TEST_CODE}    ${END_DATE}
    Loading Arm Row Should Not Exist    ${TEST_CODE}
    Loading Arm Should Not Exist In DB    ${TEST_CODE}
    Capture Step    loading_arm_tc04_deleted


*** Keywords ***
Set Up Loading Arm Suite
    [Documentation]    Generate a unique test code/name, open the screen, fill the navigator cascade.
    Prepare IUD Object Data    AUTOTEST_LA_    Loading Arm
    ${pu}=    Open Loading Arm Screen
    VAR    ${GM_PU}    ${pu}    scope=SUITE
