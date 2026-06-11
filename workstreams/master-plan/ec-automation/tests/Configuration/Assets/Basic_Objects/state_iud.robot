*** Settings ***
Documentation       EC IUD Test - State (Configuration > Assets > Basic Objects > State).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_STATE).
...                 Layered: this test -> state_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. A unique AUTOTEST_ST_<timestamp> code is generated
...                 per run (EC keeps deleted codes in the base table, so codes are never reused).

Resource            ../../../../pageobjects/Configuration/Assets/Basic_Objects/state_page.resource

Suite Setup         Set Up State Suite
Suite Teardown      Close EC

Test Tags           iud    state


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       2000-01-01
${END_DATE}         2000-01-01


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test state does not exist before inserting.
    [Tags]    clean-state
    State Row Should Not Exist    ${TEST_CODE}
    Capture Step    state_tc01_clean

TC02 Insert New State
    [Documentation]    Insert a new state and confirm it appears in the list.
    [Tags]    insert
    Insert State Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    State Row Should Exist    ${TEST_CODE}
    State Should Exist In DB    ${TEST_CODE}
    Capture Step    state_tc02_inserted

TC03 Update State Name
    [Documentation]    Edit the state name and confirm the list reflects the change.
    [Tags]    update
    Update State Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    State Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    state_tc03_updated

TC04 Delete State
    [Documentation]    Delete via End Date = Start Date and confirm the state is gone.
    [Tags]    delete    cleanup
    Delete State    ${TEST_CODE}    ${END_DATE}
    State Row Should Not Exist    ${TEST_CODE}
    State Should Not Exist In DB    ${TEST_CODE}
    Capture Step    state_tc04_deleted


*** Keywords ***
Set Up State Suite
    [Documentation]    Generate a unique test code/name, then open the State screen.
    ${code}    Generate Unique Code    AUTOTEST_ST_
    VAR    ${TEST_CODE}    ${code}    scope=SUITE
    VAR    ${OBJ_NAME}    State ${code}    scope=SUITE
    VAR    ${OBJ_NAME_UPD}    State ${code} UPD    scope=SUITE
    Open State Screen
