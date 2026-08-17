*** Settings ***
Documentation       EC IUD Test - Bank (Configuration > Assets > Financial Objects > Bank).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in ov_bank).
...                 Layered: this test -> bank_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Uses a FIXED test code (BANK_CHINA, owner-requested
...                 2026-08-17) rather than a generated unique code - confirmed absent from ov_bank
...                 before this was wired in. Every run must complete TC04 (delete) so the code is
...                 free for the next run - EC never lets a DELETED code be reused, but this fixed
...                 code only stays reusable if each run actually cleans up after itself.

Resource            ../../../../pageobjects/Configuration/Assets/Financial_Objects/bank_page.resource

Suite Setup         Set Up Bank Suite
Suite Teardown      Close EC

Test Tags           iud    bank


*** Variables ***
${TEST_CODE}        BANK_CHINA
${OBJ_NAME}        Bank of China (Hong Kong) Ltd.
${OBJ_NAME_UPD}    Bank of China (Hong Kong) Ltd. UPDATED
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
# These 3 values must stay in sync with testdata/bank_entry.properties - TC02 DB-verifies
# them against what that file actually set, not an independent assumption.
${OBJ_DESC}         Bank of China
${OBJ_ADDR1}        Bank of China Tower Branch
${OBJ_SWIFT}        BKCHHKHH


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test bank does not exist before inserting.
    [Tags]    clean-state
    Bank Row Should Not Exist    ${TEST_CODE}
    Capture Step    bank_tc01_clean

TC02 Insert New Bank
    [Documentation]    Insert a new bank DATA-DRIVEN from testdata/bank_entry.properties
    ...    (owner-requested 2026-08-17) - the fields filled and their values live in that file,
    ...    not in this test. Confirms it appears in the list and every column the properties
    ...    file set actually persisted correctly in ov_bank.
    [Tags]    insert
    ${inserted_code}=    Insert Bank From Properties
    Should Be Equal    ${inserted_code}    ${TEST_CODE}
    ...    msg=testdata/bank_entry.properties Code does not match the suite's ${TEST_CODE}
    Bank Row Should Exist    ${TEST_CODE}
    Bank Should Exist In DB    ${TEST_CODE}
    Bank Fields Should Equal In DB    ${TEST_CODE}
    ...    DESCRIPTION=${OBJ_DESC}    ADDRESS_1=${OBJ_ADDR1}    BANK_SWIFT_CODE=${OBJ_SWIFT}
    Capture Step    bank_tc02_inserted

TC03 Update Bank Name
    [Documentation]    Edit the bank name and confirm the list reflects the change.
    [Tags]    update
    Update Bank Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Bank Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
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
    [Documentation]    Open the Bank screen. Uses the FIXED test code ${TEST_CODE}
    ...    (BANK_CHINA) declared above, not a generated unique code - so a re-run only
    ...    works if the prior run's TC04 delete actually completed (EC never lets a
    ...    deleted code be reused, but a fixed code IS reusable across runs as long as
    ...    each run cleans up after itself, unlike the AUTOTEST_BNK_<timestamp> scheme).
    Open Bank Screen
