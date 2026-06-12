*** Settings ***
Documentation       EC IUD Test - Payment Scheme (Configuration > Assets > Financial Objects > Payment Scheme).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_PAYMENT_SCHEME).
...                 NEVER touch existing data. A unique AUTOTEST_PSCH_<timestamp> code is generated
...                 per run (EC keeps deleted codes in the base table, so codes are never reused).

Resource            ../../../../pageobjects/Configuration/Assets/Financial_Objects/payment_scheme_page.resource

Suite Setup         Set Up Payment Scheme Suite
Suite Teardown      Close EC

Test Tags           iud    payment-scheme


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test payment scheme does not exist before inserting.
    [Tags]    clean-state
    Payment Scheme Row Should Not Exist    ${TEST_CODE}
    Capture Step    payment_scheme_tc01_clean

TC02 Insert New Payment Scheme
    [Documentation]    Insert a new payment scheme and confirm it appears in the list.
    [Tags]    insert
    Insert Payment Scheme Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Payment Scheme Row Should Exist    ${TEST_CODE}
    Payment Scheme Should Exist In DB    ${TEST_CODE}
    Capture Step    payment_scheme_tc02_inserted

TC03 Update Payment Scheme Name
    [Documentation]    Edit the payment scheme name and confirm the list reflects the change.
    [Tags]    update
    Update Payment Scheme Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Payment Scheme Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    payment_scheme_tc03_updated

TC04 Delete Payment Scheme
    [Documentation]    Delete via End Date = Start Date and confirm the payment scheme is gone.
    [Tags]    delete    cleanup
    Delete Payment Scheme    ${TEST_CODE}    ${END_DATE}
    Payment Scheme Row Should Not Exist    ${TEST_CODE}
    Payment Scheme Should Not Exist In DB    ${TEST_CODE}
    Capture Step    payment_scheme_tc04_deleted


*** Keywords ***
Set Up Payment Scheme Suite
    [Documentation]    Generate a unique test code/name, then open the Payment Scheme screen.
    Prepare IUD Object Data    AUTOTEST_PSCH_    Payment Scheme
    Open Payment Scheme Screen
