*** Settings ***
Documentation       EC IUD Test - Payment Term (Configuration > Assets > Date Objects > Payment Term, CD.0023).
...                 Manage-Object (OV, date-effective) screen. DELETE = End Date = Start Date (true delete in ov_payment_term).
...                 Layered: this test -> payment_term_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. A unique AUTOTEST_PT_<timestamp> code is generated
...                 per run (EC keeps deleted codes in the base table, so codes are never reused).

Resource            ../../../../pageobjects/Configuration/Assets/Date_Objects/payment_term_page.resource

Suite Setup         Set Up Payment Term Suite
Suite Teardown      Close EC

Test Tags           iud    document-date-term    date-objects


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}
# Screen-specific mandatory extras on the New-Object form (PT_OFFSET = the DAY_VALUE cell, R:8)
${PT_METHOD}       Fixed number of Days
${PT_OFFSET}       30


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test object does not exist before inserting.
    [Tags]    clean-state
    Payment Term Row Should Not Exist    ${TEST_CODE}
    Payment Term Should Not Exist In DB    ${TEST_CODE}
    Capture Step    pt_tc01_clean

TC02 Insert New Payment Term
    [Documentation]    Insert a new Payment Term (Code/Name/Start Date + METHOD + OFFSET) and confirm it appears in the list and DB.
    [Tags]    insert
    Insert Payment Term Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}    ${PT_METHOD}    ${PT_OFFSET}
    Payment Term Row Should Exist    ${TEST_CODE}
    Payment Term Should Exist In DB    ${TEST_CODE}
    Capture Step    pt_tc02_inserted

TC03 Update Payment Term Name
    [Documentation]    Edit the name and confirm the list reflects the change.
    [Tags]    update
    Update Payment Term Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Payment Term Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    pt_tc03_updated

TC04 Delete Payment Term
    [Documentation]    Delete via End Date = Start Date and confirm the object is gone from list and DB.
    [Tags]    delete    cleanup
    Delete Payment Term    ${TEST_CODE}    ${END_DATE}
    Payment Term Row Should Not Exist    ${TEST_CODE}
    Payment Term Should Not Exist In DB    ${TEST_CODE}
    Capture Step    pt_tc04_deleted


*** Keywords ***
Set Up Payment Term Suite
    [Documentation]    Generate a unique test code/name, then open the Payment Term screen.
    Prepare IUD Object Data    AUTOTEST_PT_    Payment Term
    Open Payment Term Screen
