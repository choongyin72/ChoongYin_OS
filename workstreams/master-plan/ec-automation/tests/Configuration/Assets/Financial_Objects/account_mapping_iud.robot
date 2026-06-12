*** Settings ***
Documentation       EC IUD Test - Account Mapping (Configuration > Assets > Financial Objects > Account Mapping).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_FIN_ACCOUNT_MAPPING).
...                 NEVER touch existing data. A unique AUTOTEST_AM_<timestamp> code is generated
...                 per run (EC keeps deleted codes in the base table, so codes are never reused).

Resource            ../../../../pageobjects/Configuration/Assets/Financial_Objects/account_mapping_page.resource

Suite Setup         Set Up Account Mapping Suite
Suite Teardown      Close EC

Test Tags           iud    account-mapping


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE_REFDD}
${END_DATE}         ${TEST_START_DATE_REFDD}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test account mapping does not exist before inserting.
    [Tags]    clean-state
    Account Mapping Row Should Not Exist    ${TEST_CODE}
    Capture Step    account_mapping_tc01_clean

TC02 Insert New Account Mapping
    [Documentation]    Insert a new account mapping and confirm it appears in the list.
    [Tags]    insert
    Insert Account Mapping Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Account Mapping Row Should Exist    ${TEST_CODE}
    Account Mapping Should Exist In DB    ${TEST_CODE}
    Capture Step    account_mapping_tc02_inserted

TC03 Update Account Mapping Name
    [Documentation]    Edit the account mapping name and confirm the list reflects the change.
    [Tags]    update
    Update Account Mapping Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Account Mapping Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    account_mapping_tc03_updated

TC04 Delete Account Mapping
    [Documentation]    Delete via End Date = Start Date and confirm the account mapping is gone.
    [Tags]    delete    cleanup
    Delete Account Mapping    ${TEST_CODE}    ${END_DATE}
    Account Mapping Row Should Not Exist    ${TEST_CODE}
    Account Mapping Should Not Exist In DB    ${TEST_CODE}
    Capture Step    account_mapping_tc04_deleted


*** Keywords ***
Set Up Account Mapping Suite
    [Documentation]    Generate a unique test code/name, then open the Account Mapping screen.
    Prepare IUD Object Data    AUTOTEST_AM_    Account Mapping
    Open Account Mapping Screen
