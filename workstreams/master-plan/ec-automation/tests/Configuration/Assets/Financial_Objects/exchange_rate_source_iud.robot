*** Settings ***
Documentation       EC IUD Test - Exchange Rate Source (Configuration > Assets > Financial Objects > Exchange Rate Source).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_FOREX_SOURCE).
...                 NEVER touch existing data. A unique AUTOTEST_ERS_<timestamp> code is generated
...                 per run (EC keeps deleted codes in the base table, so codes are never reused).

Resource            ../../../../pageobjects/Configuration/Assets/Financial_Objects/exchange_rate_source_page.resource

Suite Setup         Set Up Exchange Rate Source Suite
Suite Teardown      Close EC

Test Tags           iud    exchange-rate-source


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test exchange rate source does not exist before inserting.
    [Tags]    clean-state
    Exchange Rate Source Row Should Not Exist    ${TEST_CODE}
    Capture Step    exchange_rate_source_tc01_clean

TC02 Insert New Exchange Rate Source
    [Documentation]    Insert a new exchange rate source and confirm it appears in the list.
    [Tags]    insert
    Insert Exchange Rate Source Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Exchange Rate Source Row Should Exist    ${TEST_CODE}
    Exchange Rate Source Should Exist In DB    ${TEST_CODE}
    Capture Step    exchange_rate_source_tc02_inserted

TC03 Update Exchange Rate Source Name
    [Documentation]    Edit the exchange rate source name and confirm the list reflects the change.
    [Tags]    update
    Update Exchange Rate Source Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Exchange Rate Source Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    exchange_rate_source_tc03_updated

TC04 Delete Exchange Rate Source
    [Documentation]    Delete via End Date = Start Date and confirm the exchange rate source is gone.
    [Tags]    delete    cleanup
    Delete Exchange Rate Source    ${TEST_CODE}    ${END_DATE}
    Exchange Rate Source Row Should Not Exist    ${TEST_CODE}
    Exchange Rate Source Should Not Exist In DB    ${TEST_CODE}
    Capture Step    exchange_rate_source_tc04_deleted


*** Keywords ***
Set Up Exchange Rate Source Suite
    [Documentation]    Generate a unique test code/name, then open the Exchange Rate Source screen.
    Prepare IUD Object Data    AUTOTEST_ERS_    Exchange Rate Source
    Open Exchange Rate Source Screen
