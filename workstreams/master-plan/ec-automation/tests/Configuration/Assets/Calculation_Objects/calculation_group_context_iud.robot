*** Settings ***
Documentation       EC IUD Test - Calculation Group Context (Configuration > Assets > Calculation_Objects > Calculation Group Context, CO.0245).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_CALC_GRP_CONTEXT).
...                 Layered: this test -> calculation_group_context_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Unique AUTOTEST_CGC_<timestamp> code per run.

Resource            ../../../../pageobjects/Configuration/Assets/Calculation_Objects/calculation_group_context_page.resource

Suite Setup         Set Up Calculation Group Context Suite
Suite Teardown      Close EC

Test Tags           iud    calculation_group_context


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test calculation_group_context does not exist before inserting.
    [Tags]    clean-state
    Calculation Group Context Row Should Not Exist    ${TEST_CODE}
    Capture Step    calculation_group_context_tc01_clean

TC02 Insert New Calculation Group Context
    [Documentation]    Insert a new calculation_group_context; confirm in list + DB (OV_CALC_GRP_CONTEXT).
    [Tags]    insert
    Insert Calculation Group Context Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Calculation Group Context Row Should Exist    ${TEST_CODE}
    Calculation Group Context Should Exist In DB    ${TEST_CODE}
    Capture Step    calculation_group_context_tc02_inserted

TC03 Update Calculation Group Context
    [Documentation]    Edit Name; confirm in list + DB ground truth.
    [Tags]    update
    Update Calculation Group Context Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Calculation Group Context Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Field Should Equal In View    OV_CALC_GRP_CONTEXT    ${TEST_CODE}    NAME    ${OBJ_NAME_UPD}
    Capture Step    calculation_group_context_tc03_updated

TC04 Delete Calculation Group Context
    [Documentation]    Delete via End Date = Start Date; confirm gone from list + DB.
    [Tags]    delete    cleanup
    Delete Calculation Group Context    ${TEST_CODE}    ${END_DATE}
    Calculation Group Context Row Should Not Exist    ${TEST_CODE}
    Calculation Group Context Should Not Exist In DB    ${TEST_CODE}
    Capture Step    calculation_group_context_tc04_deleted


*** Keywords ***
Set Up Calculation Group Context Suite
    [Documentation]    Generate a unique test code/name, then open the Calculation Group Context screen.
    Prepare IUD Object Data    AUTOTEST_CGC_    Calculation Group Context
    Open Calculation Group Context Screen
