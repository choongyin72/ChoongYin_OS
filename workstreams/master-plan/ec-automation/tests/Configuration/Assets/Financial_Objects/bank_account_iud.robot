*** Settings ***
Documentation       EC IUD Test - Bank Account (Configuration > Assets > Financial Objects > Bank Account).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_BANK_ACCOUNT).
...                 NEVER touch existing data. A unique AUTOTEST_BACC_<timestamp> code is generated
...                 per run (EC keeps deleted codes in the base table, so codes are never reused).

Resource            ../../../../pageobjects/Configuration/Assets/Financial_Objects/bank_account_page.resource

Suite Setup         Set Up Bank Account Suite
Suite Teardown      Close EC

Test Tags           iud    bank-account


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       2003-01-01
${END_DATE}         2003-01-01


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test bank account does not exist before inserting.
    [Tags]    clean-state
    Bank Account Row Should Not Exist    ${TEST_CODE}
    Capture Step    bank_account_tc01_clean

TC02 Insert New Bank Account
    [Documentation]    Insert a new bank account and confirm it appears in the list.
    [Tags]    insert
    Insert Bank Account Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Bank Account Row Should Exist    ${TEST_CODE}
    Bank Account Should Exist In DB    ${TEST_CODE}
    Capture Step    bank_account_tc02_inserted

TC03 Update Bank Account Name
    [Documentation]    Edit the bank account name and confirm the list reflects the change.
    [Tags]    update
    Update Bank Account Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Bank Account Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    bank_account_tc03_updated

TC04 Delete Bank Account
    [Documentation]    Delete via End Date = Start Date and confirm the bank account is gone.
    [Tags]    delete    cleanup
    Delete Bank Account    ${TEST_CODE}    ${END_DATE}
    Bank Account Row Should Not Exist    ${TEST_CODE}
    Bank Account Should Not Exist In DB    ${TEST_CODE}
    Capture Step    bank_account_tc04_deleted


*** Keywords ***
Set Up Bank Account Suite
    [Documentation]    Generate a unique test code/name, then open the Bank Account screen.
    ${code}    Generate Unique Code    AUTOTEST_BACC_
    VAR    ${TEST_CODE}    ${code}    scope=SUITE
    VAR    ${OBJ_NAME}    Bank Account ${code}    scope=SUITE
    VAR    ${OBJ_NAME_UPD}    Bank Account ${code} UPD    scope=SUITE
    Open Bank Account Screen
