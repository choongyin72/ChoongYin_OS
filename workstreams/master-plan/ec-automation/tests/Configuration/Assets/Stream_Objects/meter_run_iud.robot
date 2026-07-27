*** Settings ***
Documentation       EC IUD Test - Meter Run (Configuration > Assets > Stream_Objects > Meter Run, CO.0091).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_METER_RUN).
...                 Layered: this test -> meter_run_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Unique AUTOTEST_MR_<timestamp> code per run.

Resource            ../../../../pageobjects/Configuration/Assets/Stream_Objects/meter_run_page.resource

Suite Setup         Set Up Meter Run Suite
Suite Teardown      Close EC

Test Tags           iud    meter_run


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test meter_run does not exist before inserting.
    [Tags]    clean-state
    Meter Run Row Should Not Exist    ${TEST_CODE}
    Capture Step    meter_run_tc01_clean

TC02 Insert New Meter Run
    [Documentation]    Insert a new meter_run; confirm in list + DB (OV_METER_RUN).
    [Tags]    insert
    Insert Meter Run Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Meter Run Row Should Exist    ${TEST_CODE}
    Meter Run Should Exist In DB    ${TEST_CODE}
    Capture Step    meter_run_tc02_inserted

TC03 Update Meter Run
    [Documentation]    Edit Name; confirm in list + DB ground truth.
    [Tags]    update
    Update Meter Run Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Meter Run Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Field Should Equal In View    OV_METER_RUN    ${TEST_CODE}    NAME    ${OBJ_NAME_UPD}
    Capture Step    meter_run_tc03_updated

TC04 Delete Meter Run
    [Documentation]    Delete via End Date = Start Date; confirm gone from list + DB.
    [Tags]    delete    cleanup
    Delete Meter Run    ${TEST_CODE}    ${END_DATE}
    Meter Run Row Should Not Exist    ${TEST_CODE}
    Meter Run Should Not Exist In DB    ${TEST_CODE}
    Capture Step    meter_run_tc04_deleted


*** Keywords ***
Set Up Meter Run Suite
    [Documentation]    Generate a unique test code/name, then open the Meter Run screen.
    Prepare IUD Object Data    AUTOTEST_MR_    Meter Run
    Open Meter Run Screen
