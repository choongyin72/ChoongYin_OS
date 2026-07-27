*** Settings ***
Documentation       EC IUD Test - Calculation Library (Configuration > Assets > Calculation_Objects > Calculation Library, CO.1060).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_CALC_LIBRARY).
...                 Layered: this test -> calculation_library_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Unique AUTOTEST_CL_<timestamp> code per run.

Resource            ../../../../pageobjects/Configuration/Assets/Calculation_Objects/calculation_library_page.resource

Suite Setup         Set Up Calculation Library Suite
Suite Teardown      Close EC

Test Tags           iud    calculation_library


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test calculation_library does not exist before inserting.
    [Tags]    clean-state
    Calculation Library Row Should Not Exist    ${TEST_CODE}
    Capture Step    calculation_library_tc01_clean

TC02 Insert New Calculation Library
    [Documentation]    Insert a new calculation_library; confirm in list + DB (OV_CALC_LIBRARY).
    [Tags]    insert
    Insert Calculation Library Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Calculation Library Row Should Exist    ${TEST_CODE}
    Calculation Library Should Exist In DB    ${TEST_CODE}
    Capture Step    calculation_library_tc02_inserted

TC03 Update Calculation Library
    [Documentation]    Edit Name; confirm in list + DB ground truth.
    [Tags]    update
    Update Calculation Library Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Calculation Library Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Field Should Equal In View    OV_CALC_LIBRARY    ${TEST_CODE}    NAME    ${OBJ_NAME_UPD}
    Capture Step    calculation_library_tc03_updated

TC04 Delete Calculation Library
    [Documentation]    Delete via End Date = Start Date; confirm gone from list + DB.
    [Tags]    delete    cleanup
    Delete Calculation Library    ${TEST_CODE}    ${END_DATE}
    Calculation Library Row Should Not Exist    ${TEST_CODE}
    Calculation Library Should Not Exist In DB    ${TEST_CODE}
    Capture Step    calculation_library_tc04_deleted


*** Keywords ***
Set Up Calculation Library Suite
    [Documentation]    Generate a unique test code/name, then open the Calculation Library screen.
    Prepare IUD Object Data    AUTOTEST_CL_    Calculation Library
    Open Calculation Library Screen
