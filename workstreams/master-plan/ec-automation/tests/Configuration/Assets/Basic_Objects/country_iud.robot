*** Settings ***
Documentation       EC IUD Test - Country (Configuration > Assets > Basic Objects > Country).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_COUNTRY).
...                 Layered: this test -> country_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. A unique AUTOTEST_CTRY_<timestamp> code is generated
...                 per run (EC keeps deleted codes in the base table, so codes are never reused).

Resource            ../../../../pageobjects/Configuration/Assets/Basic_Objects/country_page.resource

Suite Setup         Set Up Country Suite
Suite Teardown      Close EC

Test Tags           iud    country


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test country does not exist before inserting.
    [Tags]    clean-state
    Country Row Should Not Exist    ${TEST_CODE}
    Capture Step    country_tc01_clean

TC02 Insert New Country
    [Documentation]    Insert a new country and confirm it appears in the list.
    [Tags]    insert
    Insert Country Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Country Row Should Exist    ${TEST_CODE}
    Country Should Exist In DB    ${TEST_CODE}
    Capture Step    country_tc02_inserted

TC03 Update Country Name
    [Documentation]    Edit the country name and confirm the list reflects the change.
    [Tags]    update
    Update Country Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Country Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    country_tc03_updated

TC04 Delete Country
    [Documentation]    Delete via End Date = Start Date and confirm the country is gone.
    [Tags]    delete    cleanup
    Delete Country    ${TEST_CODE}    ${END_DATE}
    Country Row Should Not Exist    ${TEST_CODE}
    Country Should Not Exist In DB    ${TEST_CODE}
    Capture Step    country_tc04_deleted


*** Keywords ***
Set Up Country Suite
    [Documentation]    Generate a unique test code/name, then open the Country screen.
    Prepare IUD Object Data    AUTOTEST_CTRY_    Country
    Open Country Screen
