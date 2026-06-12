*** Settings ***
Documentation       EC IUD Test - County (Configuration > Assets > Basic Objects > County).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_COUNTY).
...                 Layered: this test -> county_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. A unique AUTOTEST_CNTY_<timestamp> code is generated
...                 per run (EC keeps deleted codes in the base table, so codes are never reused).

Resource            ../../../../pageobjects/Configuration/Assets/Basic_Objects/county_page.resource

Suite Setup         Set Up County Suite
Suite Teardown      Close EC

Test Tags           iud    county


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test county does not exist before inserting.
    [Tags]    clean-state
    County Row Should Not Exist    ${TEST_CODE}
    Capture Step    county_tc01_clean

TC02 Insert New County
    [Documentation]    Insert a new county and confirm it appears in the list.
    [Tags]    insert
    Insert County Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    County Row Should Exist    ${TEST_CODE}
    County Should Exist In DB    ${TEST_CODE}
    Capture Step    county_tc02_inserted

TC03 Update County Name
    [Documentation]    Edit the county name and confirm the list reflects the change.
    [Tags]    update
    Update County Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    County Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    county_tc03_updated

TC04 Delete County
    [Documentation]    Delete via End Date = Start Date and confirm the county is gone.
    [Tags]    delete    cleanup
    Delete County    ${TEST_CODE}    ${END_DATE}
    County Row Should Not Exist    ${TEST_CODE}
    County Should Not Exist In DB    ${TEST_CODE}
    Capture Step    county_tc04_deleted


*** Keywords ***
Set Up County Suite
    [Documentation]    Generate a unique test code/name, then open the County screen.
    Prepare IUD Object Data    AUTOTEST_CNTY_    County
    Open County Screen
