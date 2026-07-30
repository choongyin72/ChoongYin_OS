*** Settings ***
Documentation       EC IUD Test - Contract Area Setup (Configuration > Assets > Contract_Objects).
...                 CUSTOM-URL OV: grid nav:form:T_data, no navigator/GO (toolbar Refresh reload).
...                 DELETE = End Date = Start Date (true delete in OV_CONTRACT_AREA_SETUP).
...                 NEVER touch existing data; a unique AUTOTEST_CAS_<timestamp> code per run.
...                 Start Date 2020-01-01: the 2 mandatory ref dropdowns (Contract Area Name /
...                 Contract Name) only offer objects effective at the form Start Date.

Resource            ../../../../pageobjects/Configuration/Assets/Contract_Objects/contract_area_setup_page.resource

Suite Setup         Set Up Contract Area Setup Suite
Suite Teardown      Close EC

Test Tags           iud    contract-area-setup


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       2020-01-01
${END_DATE}         2020-01-01


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test object does not exist before inserting.
    [Tags]    clean-state
    Contract Area Setup Row Should Not Exist    ${TEST_CODE}
    Capture Step    contract_area_setup_tc01_clean

TC02 Insert New Contract Area Setup
    [Documentation]    Insert with ref dropdowns first-available and confirm it lists.
    [Tags]    insert
    Insert Contract Area Setup Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Contract Area Setup Row Should Exist    ${TEST_CODE}
    Contract Area Setup Should Exist In DB    ${TEST_CODE}
    Capture Step    contract_area_setup_tc02_inserted

TC03 Update Contract Area Setup Name
    [Documentation]    Edit the name and confirm the list reflects the change.
    [Tags]    update
    Update Contract Area Setup Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Contract Area Setup Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    contract_area_setup_tc03_updated

TC04 Delete Contract Area Setup
    [Documentation]    Delete via End Date = Start Date and confirm it is gone.
    [Tags]    delete    cleanup
    Delete Contract Area Setup    ${TEST_CODE}    ${END_DATE}
    Contract Area Setup Row Should Not Exist    ${TEST_CODE}
    Contract Area Setup Should Not Exist In DB    ${TEST_CODE}
    Capture Step    contract_area_setup_tc04_deleted


*** Keywords ***
Set Up Contract Area Setup Suite
    [Documentation]    Generate a unique test code/name, open the screen (no navigator to fill).
    Prepare IUD Object Data    AUTOTEST_CAS_    Contract Area Setup
    Open Contract Area Setup Screen
