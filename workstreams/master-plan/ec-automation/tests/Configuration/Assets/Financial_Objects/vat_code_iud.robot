*** Settings ***
Documentation       EC IUD Test - VAT Code (Configuration > Assets > Financial Objects > VAT Code).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_VAT_CODE).
...                 NEVER touch existing data. A unique AUTOTEST_VAT_<timestamp> code is generated
...                 per run (EC keeps deleted codes in the base table, so codes are never reused).

Resource            ../../../../pageobjects/Configuration/Assets/Financial_Objects/vat_code_page.resource

Suite Setup         Set Up VAT Code Suite
Suite Teardown      Close EC

Test Tags           iud    vat-code


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test vat code does not exist before inserting.
    [Tags]    clean-state
    VAT Code Row Should Not Exist    ${TEST_CODE}
    Capture Step    vat_code_tc01_clean

TC02 Insert New VAT Code
    [Documentation]    Insert a new vat code and confirm it appears in the list.
    [Tags]    insert
    Insert VAT Code Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    VAT Code Row Should Exist    ${TEST_CODE}
    VAT Code Should Exist In DB    ${TEST_CODE}
    Capture Step    vat_code_tc02_inserted

TC03 Update VAT Code Name
    [Documentation]    Edit the vat code name and confirm the list reflects the change.
    [Tags]    update
    Update VAT Code Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    VAT Code Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    vat_code_tc03_updated

TC04 Delete VAT Code
    [Documentation]    Delete via End Date = Start Date and confirm the vat code is gone.
    [Tags]    delete    cleanup
    Delete VAT Code    ${TEST_CODE}    ${END_DATE}
    VAT Code Row Should Not Exist    ${TEST_CODE}
    VAT Code Should Not Exist In DB    ${TEST_CODE}
    Capture Step    vat_code_tc04_deleted


*** Keywords ***
Set Up VAT Code Suite
    [Documentation]    Generate a unique test code/name, then open the VAT Code screen.
    Prepare IUD Object Data    AUTOTEST_VAT_    VAT Code
    Open VAT Code Screen
