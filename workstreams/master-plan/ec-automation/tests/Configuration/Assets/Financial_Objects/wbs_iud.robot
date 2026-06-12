*** Settings ***
Documentation       EC IUD Test - WBS (Configuration > Assets > Financial Objects > WBS).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_FIN_WBS).
...                 NEVER touch existing data. A unique AUTOTEST_WBS_<timestamp> code is generated
...                 per run (EC keeps deleted codes in the base table, so codes are never reused).

Resource            ../../../../pageobjects/Configuration/Assets/Financial_Objects/wbs_page.resource

Suite Setup         Set Up WBS Suite
Suite Teardown      Close EC

Test Tags           iud    wbs


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test wbs does not exist before inserting.
    [Tags]    clean-state
    WBS Row Should Not Exist    ${TEST_CODE}
    Capture Step    wbs_tc01_clean

TC02 Insert New WBS
    [Documentation]    Insert a new wbs and confirm it appears in the list.
    [Tags]    insert
    Insert WBS Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    WBS Row Should Exist    ${TEST_CODE}
    WBS Should Exist In DB    ${TEST_CODE}
    Capture Step    wbs_tc02_inserted

TC03 Update WBS Name
    [Documentation]    Edit the wbs name and confirm the list reflects the change.
    [Tags]    update
    Update WBS Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    WBS Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    wbs_tc03_updated

TC04 Delete WBS
    [Documentation]    Delete via End Date = Start Date and confirm the wbs is gone.
    [Tags]    delete    cleanup
    Delete WBS    ${TEST_CODE}    ${END_DATE}
    WBS Row Should Not Exist    ${TEST_CODE}
    WBS Should Not Exist In DB    ${TEST_CODE}
    Capture Step    wbs_tc04_deleted


*** Keywords ***
Set Up WBS Suite
    [Documentation]    Generate a unique test code/name, then open the WBS screen.
    Prepare IUD Object Data    AUTOTEST_WBS_    WBS
    Open WBS Screen
