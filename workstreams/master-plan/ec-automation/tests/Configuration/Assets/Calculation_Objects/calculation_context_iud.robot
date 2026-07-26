*** Settings ***
Documentation       EC IUD Test - Calculation Context (Configuration > Assets > Calculation_Objects > Calculation Context, CO.1059).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_CALC_CONTEXT).
...                 Layered: this test -> calculation_context_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Unique AUTOTEST_CALCTX_<timestamp> code per run.

Resource            ../../../../pageobjects/Configuration/Assets/Calculation_Objects/calculation_context_page.resource

Suite Setup         Set Up Calculation Context Suite
Suite Teardown      Close EC

Test Tags           iud    calculation_context


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test calculation_context does not exist before inserting.
    [Tags]    clean-state
    Calculation Context Row Should Not Exist    ${TEST_CODE}
    Capture Step    calculation_context_tc01_clean

TC02 Insert New Calculation Context
    [Documentation]    Insert a new calculation_context; confirm in list + DB (OV_CALC_CONTEXT).
    [Tags]    insert
    Insert Calculation Context Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Calculation Context Row Should Exist    ${TEST_CODE}
    Calculation Context Should Exist In DB    ${TEST_CODE}
    Capture Step    calculation_context_tc02_inserted

TC03 Update Calculation Context
    [Documentation]    Edit Name; confirm in list + DB ground truth.
    [Tags]    update
    Update Calculation Context Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Calculation Context Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Field Should Equal In View    OV_CALC_CONTEXT    ${TEST_CODE}    NAME    ${OBJ_NAME_UPD}
    Capture Step    calculation_context_tc03_updated

TC04 Delete Calculation Context
    [Documentation]    Delete via End Date = Start Date; confirm gone from list + DB.
    [Tags]    delete    cleanup
    Delete Calculation Context    ${TEST_CODE}    ${END_DATE}
    Calculation Context Row Should Not Exist    ${TEST_CODE}
    Calculation Context Should Not Exist In DB    ${TEST_CODE}
    Capture Step    calculation_context_tc04_deleted


*** Keywords ***
Set Up Calculation Context Suite
    [Documentation]    Generate a unique test code/name, then open the Calculation Context screen.
    Prepare IUD Object Data    AUTOTEST_CALCTX_    Calculation Context
    Open Calculation Context Screen
