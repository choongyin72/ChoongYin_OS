*** Settings ***
Documentation       EC IUD Test - Shift (Configuration > Assets > Facility Objects).
...                 OV-GM (manage-object, groupmodel): grid filtered by the navigator cascade.
...                 DELETE = End Date = Start Date (true delete in OV_SHIFT). NEVER touch existing data;
...                 a unique AUTOTEST_SHIFT_<timestamp> code is generated per run.

Resource            ../../../../pageobjects/Configuration/Assets/Facility Objects/shift_page.resource

Suite Setup         Set Up Shift Suite
Suite Teardown      Close EC

Test Tags           iud    shift


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
    Shift Row Should Not Exist    ${TEST_CODE}
    Capture Step    shift_tc01_clean

TC02 Insert New Shift
    [Documentation]    Insert under the navigator scope and confirm it lists.
    [Tags]    insert
    Insert Shift Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Shift Row Should Exist    ${TEST_CODE}
    Shift Should Exist In DB    ${TEST_CODE}
    Capture Step    shift_tc02_inserted

TC03 Update Shift Name
    [Documentation]    Edit the name and confirm the list reflects the change.
    [Tags]    update
    Update Shift Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Shift Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    shift_tc03_updated

TC04 Delete Shift
    [Documentation]    Delete via End Date = Start Date and confirm it is gone.
    [Tags]    delete    cleanup
    Delete Shift    ${TEST_CODE}    ${END_DATE}
    Shift Row Should Not Exist    ${TEST_CODE}
    Shift Should Not Exist In DB    ${TEST_CODE}
    Capture Step    shift_tc04_deleted


*** Keywords ***
Set Up Shift Suite
    [Documentation]    Generate a unique test code/name, open the screen, fill the navigator cascade.
    Prepare IUD Object Data    AUTOTEST_SHIFT_    Shift
    ${pu}=    Open Shift Screen
    VAR    ${GM_PU}    ${pu}    scope=SUITE
