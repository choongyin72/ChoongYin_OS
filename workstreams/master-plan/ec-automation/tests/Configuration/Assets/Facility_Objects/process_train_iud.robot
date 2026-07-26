*** Settings ***
Documentation       EC IUD Test - Process Train (Configuration > Assets > Facility_Objects > Process Train, CO.0120).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_PROCESS_TRAIN).
...                 Layered: this test -> process_train_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Unique AUTOTEST_PT_<timestamp> code per run.

Resource            ../../../../pageobjects/Configuration/Assets/Facility_Objects/process_train_page.resource

Suite Setup         Set Up Process Train Suite
Suite Teardown      Close EC

Test Tags           iud    process_train


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test process_train does not exist before inserting.
    [Tags]    clean-state
    Process Train Row Should Not Exist    ${TEST_CODE}
    Capture Step    process_train_tc01_clean

TC02 Insert New Process Train
    [Documentation]    Insert a new process_train; confirm in list + DB (OV_PROCESS_TRAIN).
    [Tags]    insert
    Insert Process Train Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Process Train Row Should Exist    ${TEST_CODE}
    Process Train Should Exist In DB    ${TEST_CODE}
    Capture Step    process_train_tc02_inserted

TC03 Update Process Train
    [Documentation]    Edit Name; confirm in list + DB ground truth.
    [Tags]    update
    Update Process Train Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Process Train Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Field Should Equal In View    OV_PROCESS_TRAIN    ${TEST_CODE}    NAME    ${OBJ_NAME_UPD}
    Capture Step    process_train_tc03_updated

TC04 Delete Process Train
    [Documentation]    Delete via End Date = Start Date; confirm gone from list + DB.
    [Tags]    delete    cleanup
    Delete Process Train    ${TEST_CODE}    ${END_DATE}
    Process Train Row Should Not Exist    ${TEST_CODE}
    Process Train Should Not Exist In DB    ${TEST_CODE}
    Capture Step    process_train_tc04_deleted


*** Keywords ***
Set Up Process Train Suite
    [Documentation]    Generate a unique test code/name, then open the Process Train screen.
    Prepare IUD Object Data    AUTOTEST_PT_    Process Train
    Open Process Train Screen
