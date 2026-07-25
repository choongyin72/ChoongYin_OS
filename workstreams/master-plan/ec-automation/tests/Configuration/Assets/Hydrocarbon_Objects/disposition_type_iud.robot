*** Settings ***
Documentation       EC IUD Test - Disposition Type (Configuration > Assets > Hydrocarbon Objects > Disposition Type).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_DISPOSITION_TYPE).
...                 Layered: this test -> disposition_type_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Unique AUTOTEST_DISP_<timestamp> code per run.

Resource            ../../../../pageobjects/Configuration/Assets/Hydrocarbon_Objects/disposition_type_page.resource

Suite Setup         Set Up Disposition Type Suite
Suite Teardown      Close EC

Test Tags           iud    disposition_type


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${OBJ_DESC_UPD}     AUTOTEST desc UPDATED
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test disposition type does not exist before inserting.
    [Tags]    clean-state
    Disposition Type Row Should Not Exist    ${TEST_CODE}
    Capture Step    disposition_type_tc01_clean

TC02 Insert New Disposition Type
    [Documentation]    Insert a new disposition type; confirm in list + DB (OV_DISPOSITION_TYPE).
    [Tags]    insert
    Insert Disposition Type Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Disposition Type Row Should Exist    ${TEST_CODE}
    Disposition Type Should Exist In DB    ${TEST_CODE}
    Capture Step    disposition_type_tc02_inserted

TC03 Update Disposition Type
    [Documentation]    Edit Name + Description; confirm in list + DB ground truth.
    [Tags]    update
    Update Disposition Type    ${TEST_CODE}    ${OBJ_NAME_UPD}    ${OBJ_DESC_UPD}
    Disposition Type Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Field Should Equal In View    OV_DISPOSITION_TYPE    ${TEST_CODE}    NAME    ${OBJ_NAME_UPD}
    Field Should Equal In View    OV_DISPOSITION_TYPE    ${TEST_CODE}    DESCRIPTION    ${OBJ_DESC_UPD}
    Capture Step    disposition_type_tc03_updated

TC04 Delete Disposition Type
    [Documentation]    Delete via End Date = Start Date; confirm gone from list + DB.
    [Tags]    delete    cleanup
    Delete Disposition Type    ${TEST_CODE}    ${END_DATE}
    Disposition Type Row Should Not Exist    ${TEST_CODE}
    Disposition Type Should Not Exist In DB    ${TEST_CODE}
    Capture Step    disposition_type_tc04_deleted


*** Keywords ***
Set Up Disposition Type Suite
    [Documentation]    Generate a unique test code/name, then open the Disposition Type screen.
    Prepare IUD Object Data    AUTOTEST_DISP_    Disposition
    Open Disposition Type Screen
