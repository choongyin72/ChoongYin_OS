*** Settings ***
Documentation       EC IUD Test - Account (Configuration > Assets > Financial Objects > Account).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_FIN_ACCOUNT).
...                 NEVER touch existing data. A unique AUTOTEST_ACC_<timestamp> code is generated
...                 per run (EC keeps deleted codes in the base table, so codes are never reused).

Resource            ../../../../pageobjects/Configuration/Assets/Financial_Objects/account_page.resource

Suite Setup         Set Up Account Suite
Suite Teardown      Close EC

Test Tags           iud    account


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test account does not exist before inserting.
    [Tags]    clean-state
    Account Row Should Not Exist    ${TEST_CODE}
    Capture Step    account_tc01_clean

TC02 Insert New Account
    [Documentation]    Insert a new account and confirm it appears in the list.
    [Tags]    insert
    Insert Account Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Account Row Should Exist    ${TEST_CODE}
    Account Should Exist In DB    ${TEST_CODE}
    Capture Step    account_tc02_inserted

TC03 Update Account Name
    [Documentation]    Edit the account name and confirm the list reflects the change.
    [Tags]    update
    Update Account Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Account Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    account_tc03_updated

TC04 Delete Account
    [Documentation]    Delete via End Date = Start Date and confirm the account is gone.
    [Tags]    delete    cleanup
    Delete Account    ${TEST_CODE}    ${END_DATE}
    Account Row Should Not Exist    ${TEST_CODE}
    Account Should Not Exist In DB    ${TEST_CODE}
    Capture Step    account_tc04_deleted


*** Keywords ***
Set Up Account Suite
    [Documentation]    Generate a unique test code/name, then open the Account screen.
    Prepare IUD Object Data    AUTOTEST_ACC_    Account
    Open Account Screen
