*** Settings ***
Documentation       EC IUD Test - Data Extract Setup (Configuration > Assets > Data_Mapping_Objects > Data Extract Setup, SP.0043).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_SUMMARY_SETUP).
...                 Layered: this test -> data_extract_setup_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Unique AUTOTEST_DXS_<timestamp> code per run.

Resource            ../../../../pageobjects/Configuration/Assets/Data_Mapping_Objects/data_extract_setup_page.resource

Suite Setup         Set Up Data Extract Setup Suite
Suite Teardown      Close EC

Test Tags           iud    data_extract_setup


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test data_extract_setup does not exist before inserting.
    [Tags]    clean-state
    Data Extract Setup Row Should Not Exist    ${TEST_CODE}
    Capture Step    data_extract_setup_tc01_clean

TC02 Insert New Data Extract Setup
    [Documentation]    Insert a new data_extract_setup; confirm in list + DB (OV_SUMMARY_SETUP).
    [Tags]    insert
    Insert Data Extract Setup Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Data Extract Setup Row Should Exist    ${TEST_CODE}
    Data Extract Setup Should Exist In DB    ${TEST_CODE}
    Capture Step    data_extract_setup_tc02_inserted

TC03 Update Data Extract Setup
    [Documentation]    Edit Name; confirm in list + DB ground truth.
    [Tags]    update
    Update Data Extract Setup Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Data Extract Setup Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Field Should Equal In View    OV_SUMMARY_SETUP    ${TEST_CODE}    NAME    ${OBJ_NAME_UPD}
    Capture Step    data_extract_setup_tc03_updated

TC04 Delete Data Extract Setup
    [Documentation]    Delete via End Date = Start Date; confirm gone from list + DB.
    [Tags]    delete    cleanup
    Delete Data Extract Setup    ${TEST_CODE}    ${END_DATE}
    Data Extract Setup Row Should Not Exist    ${TEST_CODE}
    Data Extract Setup Should Not Exist In DB    ${TEST_CODE}
    Capture Step    data_extract_setup_tc04_deleted


*** Keywords ***
Set Up Data Extract Setup Suite
    [Documentation]    Generate a unique test code/name, then open the Data Extract Setup screen.
    Prepare IUD Object Data    AUTOTEST_DXS_    Data Extract Setup
    Open Data Extract Setup Screen
