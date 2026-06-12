*** Settings ***
Documentation       EC IUD Test - Currency (Configuration > Assets > Financial Objects > Currency).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_CURRENCY).
...                 NEVER touch existing data. A unique AUTOTEST_CUR_<timestamp> code is generated
...                 per run (EC keeps deleted codes in the base table, so codes are never reused).

Resource            ../../../../pageobjects/Configuration/Assets/Financial_Objects/currency_page.resource

Suite Setup         Set Up Currency Suite
Suite Teardown      Close EC

Test Tags           iud    currency


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test currency does not exist before inserting.
    [Tags]    clean-state
    Currency Row Should Not Exist    ${TEST_CODE}
    Capture Step    currency_tc01_clean

TC02 Insert New Currency
    [Documentation]    Insert a new currency and confirm it appears in the list.
    [Tags]    insert
    Insert Currency Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Currency Row Should Exist    ${TEST_CODE}
    Currency Should Exist In DB    ${TEST_CODE}
    Capture Step    currency_tc02_inserted

TC03 Update Currency Name
    [Documentation]    Edit the currency name and confirm the list reflects the change.
    [Tags]    update
    Update Currency Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Currency Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    currency_tc03_updated

TC04 Delete Currency
    [Documentation]    Delete via End Date = Start Date and confirm the currency is gone.
    [Tags]    delete    cleanup
    Delete Currency    ${TEST_CODE}    ${END_DATE}
    Currency Row Should Not Exist    ${TEST_CODE}
    Currency Should Not Exist In DB    ${TEST_CODE}
    Capture Step    currency_tc04_deleted


*** Keywords ***
Set Up Currency Suite
    [Documentation]    Generate a unique test code/name, then open the Currency screen.
    Prepare IUD Object Data    AUTOTEST_CUR_    Currency
    Open Currency Screen
