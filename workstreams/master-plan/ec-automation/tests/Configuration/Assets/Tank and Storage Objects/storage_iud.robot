*** Settings ***
Documentation       EC IUD Test - Storage (Configuration > Assets > Tank and Storage Objects).
...                 OV-GM (manage-object, groupmodel): grid filtered by the navigator cascade.
...                 DELETE = End Date = Start Date (true delete in OV_STORAGE). NEVER touch existing data;
...                 a unique AUTOTEST_STOR_<timestamp> code is generated per run.

Resource            ../../../../pageobjects/Configuration/Assets/Tank and Storage Objects/storage_page.resource

Suite Setup         Set Up Storage Suite
Suite Teardown      Close EC

Test Tags           iud    storage


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
    Storage Row Should Not Exist    ${TEST_CODE}
    Capture Step    storage_tc01_clean

TC02 Insert New Storage
    [Documentation]    Insert under the navigator scope and confirm it lists.
    [Tags]    insert
    Insert Storage Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Storage Row Should Exist    ${TEST_CODE}
    Storage Should Exist In DB    ${TEST_CODE}
    Capture Step    storage_tc02_inserted

TC03 Update Storage Name
    [Documentation]    Edit the name and confirm the list reflects the change.
    [Tags]    update
    Update Storage Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Storage Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    storage_tc03_updated

TC04 Delete Storage
    [Documentation]    Delete via End Date = Start Date and confirm it is gone.
    [Tags]    delete    cleanup
    Delete Storage    ${TEST_CODE}    ${END_DATE}
    Storage Row Should Not Exist    ${TEST_CODE}
    Storage Should Not Exist In DB    ${TEST_CODE}
    Capture Step    storage_tc04_deleted


*** Keywords ***
Set Up Storage Suite
    [Documentation]    Generate a unique test code/name, open the screen, fill the navigator cascade.
    Prepare IUD Object Data    AUTOTEST_STOR_    Storage
    ${pu}=    Open Storage Screen
    VAR    ${GM_PU}    ${pu}    scope=SUITE
