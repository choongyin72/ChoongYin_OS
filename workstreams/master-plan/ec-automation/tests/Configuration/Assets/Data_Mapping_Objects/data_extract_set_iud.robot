*** Settings ***
Documentation       EC IUD Test - Data Extract Set (Configuration > Assets > Data_Mapping_Objects > Data Extract Set, SP.0049).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_SUMMARY_SET).
...                 Layered: this test -> data_extract_set_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Unique AUTOTEST_DXT_<timestamp> code per run.

Resource            ../../../../pageobjects/Configuration/Assets/Data_Mapping_Objects/data_extract_set_page.resource

Suite Setup         Set Up Data Extract Set Suite
Suite Teardown      Close EC

Test Tags           iud    data_extract_set


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test data_extract_set does not exist before inserting.
    [Tags]    clean-state
    Data Extract Set Row Should Not Exist    ${TEST_CODE}
    Capture Step    data_extract_set_tc01_clean

TC02 Insert New Data Extract Set
    [Documentation]    Insert a new data_extract_set; confirm in list + DB (OV_SUMMARY_SET).
    [Tags]    insert
    Insert Data Extract Set Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Data Extract Set Row Should Exist    ${TEST_CODE}
    Data Extract Set Should Exist In DB    ${TEST_CODE}
    Capture Step    data_extract_set_tc02_inserted

TC03 Update Data Extract Set
    [Documentation]    Edit Name; confirm in list + DB ground truth.
    [Tags]    update
    Update Data Extract Set Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Data Extract Set Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Field Should Equal In View    OV_SUMMARY_SET    ${TEST_CODE}    NAME    ${OBJ_NAME_UPD}
    Capture Step    data_extract_set_tc03_updated

TC04 Delete Data Extract Set
    [Documentation]    Delete via End Date = Start Date; confirm gone from list + DB.
    [Tags]    delete    cleanup
    Delete Data Extract Set    ${TEST_CODE}    ${END_DATE}
    Data Extract Set Row Should Not Exist    ${TEST_CODE}
    Data Extract Set Should Not Exist In DB    ${TEST_CODE}
    Capture Step    data_extract_set_tc04_deleted


*** Keywords ***
Set Up Data Extract Set Suite
    [Documentation]    Generate a unique test code/name, then open the Data Extract Set screen.
    Prepare IUD Object Data    AUTOTEST_DXT_    Data Extract Set
    Open Data Extract Set Screen
