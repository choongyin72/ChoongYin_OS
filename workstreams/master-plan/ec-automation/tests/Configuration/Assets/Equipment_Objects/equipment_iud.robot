*** Settings ***
Documentation       EC IUD Test - Equipment (Configuration > Assets > Equipment Objects > Equipment).
...                 Manage-Object (OV) screen with a 5-field cascading navigator.
...                 DELETE = End Date = Start Date (true delete in OV_EQPM).
...                 Layered: this test -> equipment_page (T3) -> manage_object (T2) + navigator/common (T1).
...                 NEVER touch existing data. A unique AUTOTEST_EQP_<timestamp> code is generated per run.

Resource            ../../../../pageobjects/Configuration/Assets/Equipment_Objects/equipment_page.resource

Suite Setup         Set Up Equipment Suite
Suite Teardown      Close EC

Test Tags           iud    equipment


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Navigator loads rows and the (freshly generated) equipment does not exist yet.
    [Tags]    clean-state
    Equipment Rows Should Be Loaded
    Equipment Row Should Not Exist    ${TEST_CODE}
    Capture Step    eqp_tc01_clean

TC02 Insert New Equipment
    [Documentation]    Insert a new equipment and confirm it appears (UI + DB).
    [Tags]    insert
    Insert Equipment Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Equipment Row Should Exist    ${TEST_CODE}
    Equipment Should Exist In DB    ${TEST_CODE}
    Capture Step    eqp_tc02_inserted

TC03 Update Equipment Name
    [Documentation]    Edit the equipment name and confirm the list reflects the change.
    [Tags]    update
    Update Equipment Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Equipment Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    eqp_tc03_updated

TC04 Delete Equipment
    [Documentation]    Delete via End Date = Start Date and confirm it is gone (UI + DB).
    [Tags]    delete    cleanup
    Delete Equipment    ${TEST_CODE}    ${END_DATE}
    Equipment Row Should Not Exist    ${TEST_CODE}
    Equipment Should Not Exist In DB    ${TEST_CODE}
    Capture Step    eqp_tc04_deleted


*** Keywords ***
Set Up Equipment Suite
    [Documentation]    Generate a unique test code/name, then open the Equipment screen.
    Prepare IUD Object Data    AUTOTEST_EQP_    Equipment
    Open Equipment Screen
