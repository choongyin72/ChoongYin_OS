*** Settings ***
Documentation       EC IUD Test - Facility Class 1 (Configuration > Assets > Facility_Objects).
...                 OV-GM (manage-object, groupmodel): grid filtered by the navigator cascade.
...                 DELETE = End Date = Start Date (true delete in OV_FCTY_CLASS_1). NEVER touch existing data;
...                 a unique AUTOTEST_FC1_<timestamp> code is generated per run.

Resource            ../../../../pageobjects/Configuration/Assets/Facility_Objects/facility_class_1_page.resource

Suite Setup         Set Up Facility Class 1 Suite
Suite Teardown      Close EC

Test Tags           iud    facility_class_1


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
    Facility Class 1 Row Should Not Exist    ${TEST_CODE}
    Capture Step    facility_class_1_tc01_clean

TC02 Insert New Facility Class 1
    [Documentation]    Insert under the navigator scope and confirm it lists.
    [Tags]    insert
    Insert Facility Class 1 Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Facility Class 1 Row Should Exist    ${TEST_CODE}
    Facility Class 1 Should Exist In DB    ${TEST_CODE}
    Capture Step    facility_class_1_tc02_inserted

TC03 Update Facility Class 1 Name
    [Documentation]    Edit the name and confirm the list reflects the change.
    [Tags]    update
    Update Facility Class 1 Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Facility Class 1 Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    facility_class_1_tc03_updated

TC04 Delete Facility Class 1
    [Documentation]    Delete via End Date = Start Date and confirm it is gone.
    [Tags]    delete    cleanup
    Delete Facility Class 1    ${TEST_CODE}    ${END_DATE}
    Facility Class 1 Row Should Not Exist    ${TEST_CODE}
    Facility Class 1 Should Not Exist In DB    ${TEST_CODE}
    Capture Step    facility_class_1_tc04_deleted


*** Keywords ***
Set Up Facility Class 1 Suite
    [Documentation]    Generate a unique test code/name, open the screen, fill the navigator cascade.
    Prepare IUD Object Data    AUTOTEST_FC1_    Facility Class 1
    ${pu}=    Open Facility Class 1 Screen
    VAR    ${GM_PU}    ${pu}    scope=SUITE
