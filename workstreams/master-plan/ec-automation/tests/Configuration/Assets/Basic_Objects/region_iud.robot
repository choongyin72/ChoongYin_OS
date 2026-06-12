*** Settings ***
Documentation       EC IUD Test - Region (Configuration > Assets > Basic Objects > Region).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_REGION).
...                 Layered: this test -> region_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. A unique AUTOTEST_REG_<timestamp> code is generated
...                 per run (EC keeps deleted codes in the base table, so codes are never reused).

Resource            ../../../../pageobjects/Configuration/Assets/Basic_Objects/region_page.resource

Suite Setup         Set Up Region Suite
Suite Teardown      Close EC

Test Tags           iud    region


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test region does not exist before inserting.
    [Tags]    clean-state
    Region Row Should Not Exist    ${TEST_CODE}
    Capture Step    region_tc01_clean

TC02 Insert New Region
    [Documentation]    Insert a new region and confirm it appears in the list.
    [Tags]    insert
    Insert Region Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Region Row Should Exist    ${TEST_CODE}
    Region Should Exist In DB    ${TEST_CODE}
    Capture Step    region_tc02_inserted

TC03 Update Region Name
    [Documentation]    Edit the region name and confirm the list reflects the change.
    [Tags]    update
    Update Region Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Region Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    region_tc03_updated

TC04 Delete Region
    [Documentation]    Delete via End Date = Start Date and confirm the region is gone.
    [Tags]    delete    cleanup
    Delete Region    ${TEST_CODE}    ${END_DATE}
    Region Row Should Not Exist    ${TEST_CODE}
    Region Should Not Exist In DB    ${TEST_CODE}
    Capture Step    region_tc04_deleted


*** Keywords ***
Set Up Region Suite
    [Documentation]    Generate a unique test code/name, then open the Region screen.
    Prepare IUD Object Data    AUTOTEST_REG_    Region
    Open Region Screen
