*** Settings ***
Documentation       EC IUD Test - Storage Flow (Configuration > Assets > Tank_and_Storage_Objects > Storage Flow, CO.2091).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_STORAGE_FLOW).
...                 Layered: this test -> storage_flow_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Unique AUTOTEST_SF_<timestamp> code per run.

Resource            ../../../../pageobjects/Configuration/Assets/Tank_and_Storage_Objects/storage_flow_page.resource

Suite Setup         Set Up Storage Flow Suite
Suite Teardown      Close EC

Test Tags           iud    storage_flow


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test storage_flow does not exist before inserting.
    [Tags]    clean-state
    Storage Flow Row Should Not Exist    ${TEST_CODE}
    Capture Step    storage_flow_tc01_clean

TC02 Insert New Storage Flow
    [Documentation]    Insert a new storage_flow; confirm in list + DB (OV_STORAGE_FLOW).
    [Tags]    insert
    Insert Storage Flow Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Storage Flow Row Should Exist    ${TEST_CODE}
    Storage Flow Should Exist In DB    ${TEST_CODE}
    Capture Step    storage_flow_tc02_inserted

TC03 Update Storage Flow
    [Documentation]    Edit Name; confirm in list + DB ground truth.
    [Tags]    update
    Update Storage Flow Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Storage Flow Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Field Should Equal In View    OV_STORAGE_FLOW    ${TEST_CODE}    NAME    ${OBJ_NAME_UPD}
    Capture Step    storage_flow_tc03_updated

TC04 Delete Storage Flow
    [Documentation]    Delete via End Date = Start Date; confirm gone from list + DB.
    [Tags]    delete    cleanup
    Delete Storage Flow    ${TEST_CODE}    ${END_DATE}
    Storage Flow Row Should Not Exist    ${TEST_CODE}
    Storage Flow Should Not Exist In DB    ${TEST_CODE}
    Capture Step    storage_flow_tc04_deleted


*** Keywords ***
Set Up Storage Flow Suite
    [Documentation]    Generate a unique test code/name, then open the Storage Flow screen.
    Prepare IUD Object Data    AUTOTEST_SF_    Storage Flow
    Open Storage Flow Screen
