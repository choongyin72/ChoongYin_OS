*** Settings ***
Documentation       EC IUD Test - Business Unit (Configuration > Assets > Basic Objects > Business Unit).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_BUSINESS_UNIT).
...                 Layered: this test -> business_unit_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. A unique AUTOTEST_BU_<timestamp> code is generated
...                 per run (EC keeps deleted codes in the base table, so codes are never reused).

Resource            ../../../../pageobjects/Configuration/Assets/Basic_Objects/business_unit_page.resource

Suite Setup         Set Up Business Unit Suite
Suite Teardown      Close EC

Test Tags           iud    business-unit


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       2000-01-01
${END_DATE}         2000-01-01


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test business unit does not exist before inserting.
    [Tags]    clean-state
    Business Unit Row Should Not Exist    ${TEST_CODE}
    Capture Step    business_unit_tc01_clean

TC02 Insert New Business Unit
    [Documentation]    Insert a new business unit and confirm it appears in the list.
    [Tags]    insert
    Insert Business Unit Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Business Unit Row Should Exist    ${TEST_CODE}
    Business Unit Should Exist In DB    ${TEST_CODE}
    Capture Step    business_unit_tc02_inserted

TC03 Update Business Unit Name
    [Documentation]    Edit the business unit name and confirm the list reflects the change.
    [Tags]    update
    Update Business Unit Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Business Unit Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    business_unit_tc03_updated

TC04 Delete Business Unit
    [Documentation]    Delete via End Date = Start Date and confirm the business unit is gone.
    [Tags]    delete    cleanup
    Delete Business Unit    ${TEST_CODE}    ${END_DATE}
    Business Unit Row Should Not Exist    ${TEST_CODE}
    Business Unit Should Not Exist In DB    ${TEST_CODE}
    Capture Step    business_unit_tc04_deleted


*** Keywords ***
Set Up Business Unit Suite
    [Documentation]    Generate a unique test code/name, then open the Business Unit screen.
    ${code}    Generate Unique Code    AUTOTEST_BU_
    VAR    ${TEST_CODE}    ${code}    scope=SUITE
    VAR    ${OBJ_NAME}    Business Unit ${code}    scope=SUITE
    VAR    ${OBJ_NAME_UPD}    Business Unit ${code} UPD    scope=SUITE
    Open Business Unit Screen
