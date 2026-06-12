*** Settings ***
Documentation       EC IUD Test - DOA Credit Limit (Configuration > Assets > Financial Objects > DOA Credit Limit).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_DOA_CREDIT_LIMIT).
...                 NEVER touch existing data. A unique AUTOTEST_DOA_<timestamp> code is generated
...                 per run (EC keeps deleted codes in the base table, so codes are never reused).

Resource            ../../../../pageobjects/Configuration/Assets/Financial_Objects/doa_credit_limit_page.resource

Suite Setup         Set Up DOA Credit Limit Suite
Suite Teardown      Close EC

Test Tags           iud    doa-credit-limit


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test doa credit limit does not exist before inserting.
    [Tags]    clean-state
    DOA Credit Limit Row Should Not Exist    ${TEST_CODE}
    Capture Step    doa_credit_limit_tc01_clean

TC02 Insert New DOA Credit Limit
    [Documentation]    Insert a new doa credit limit and confirm it appears in the list.
    [Tags]    insert
    Insert DOA Credit Limit Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    DOA Credit Limit Row Should Exist    ${TEST_CODE}
    DOA Credit Limit Should Exist In DB    ${TEST_CODE}
    Capture Step    doa_credit_limit_tc02_inserted

TC03 Update DOA Credit Limit Name
    [Documentation]    Edit the doa credit limit name and confirm the list reflects the change.
    [Tags]    update
    Update DOA Credit Limit Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    DOA Credit Limit Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    doa_credit_limit_tc03_updated

TC04 Delete DOA Credit Limit
    [Documentation]    Delete via End Date = Start Date and confirm the doa credit limit is gone.
    [Tags]    delete    cleanup
    Delete DOA Credit Limit    ${TEST_CODE}    ${END_DATE}
    DOA Credit Limit Row Should Not Exist    ${TEST_CODE}
    DOA Credit Limit Should Not Exist In DB    ${TEST_CODE}
    Capture Step    doa_credit_limit_tc04_deleted


*** Keywords ***
Set Up DOA Credit Limit Suite
    [Documentation]    Generate a unique test code/name, then open the DOA Credit Limit screen.
    Prepare IUD Object Data    AUTOTEST_DOA_    DOA Credit Limit
    Open DOA Credit Limit Screen
