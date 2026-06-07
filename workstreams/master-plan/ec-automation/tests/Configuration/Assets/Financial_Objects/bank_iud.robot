*** Settings ***
Documentation       EC IUD Test - Bank (Configuration > Assets > Financial Objects > Bank).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in ov_bank).
...                 Layered: this test -> bank_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. A unique AUTOTEST_BNK_<timestamp> code is generated
...                 per run (EC keeps deleted codes in the base table, so codes are never reused).

Resource            ../../../../pageobjects/Configuration/Assets/Financial_Objects/bank_page.resource

Suite Setup         Set Up Bank Suite
Suite Teardown      Close EC

Test Tags           iud    bank


*** Variables ***
${TEST_CODE}        ${EMPTY}
${BANK_NAME}        ${EMPTY}
${BANK_NAME_UPD}    ${EMPTY}
${START_DATE}       2000-01-01
${END_DATE}         2000-01-01


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test bank does not exist before inserting.
    [Tags]    clean-state
    Bank Row Should Not Exist    ${TEST_CODE}
    Capture Step    bank_tc01_clean

TC02 Insert New Bank
    [Documentation]    Insert a new bank and confirm it appears in the list.
    [Tags]    insert
    Insert Bank Record    ${TEST_CODE}    ${BANK_NAME}    ${START_DATE}
    Bank Row Should Exist    ${TEST_CODE}
    Bank Should Exist In DB    ${TEST_CODE}
    Capture Step    bank_tc02_inserted

TC03 Update Bank Name
    [Documentation]    Edit the bank name and confirm the list reflects the change.
    [Tags]    update
    Update Bank Name    ${TEST_CODE}    ${BANK_NAME_UPD}
    Bank Row Should Show Name    ${TEST_CODE}    ${BANK_NAME_UPD}
    Capture Step    bank_tc03_updated

TC04 Delete Bank
    [Documentation]    Delete via End Date = Start Date and confirm the bank is gone.
    [Tags]    delete    cleanup
    Delete Bank    ${TEST_CODE}    ${END_DATE}
    Bank Row Should Not Exist    ${TEST_CODE}
    Bank Should Not Exist In DB    ${TEST_CODE}
    Capture Step    bank_tc04_deleted


*** Keywords ***
Set Up Bank Suite
    [Documentation]    Generate a unique test code/name, then open the Bank screen.
    ${code}    Generate Unique Code    AUTOTEST_BNK_
    VAR    ${TEST_CODE}    ${code}    scope=SUITE
    VAR    ${BANK_NAME}    Bank ${code}    scope=SUITE
    VAR    ${BANK_NAME_UPD}    Bank ${code} UPD    scope=SUITE
    Open Bank Screen
