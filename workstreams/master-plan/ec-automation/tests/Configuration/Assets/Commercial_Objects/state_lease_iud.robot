*** Settings ***
Documentation       EC IUD Test - State Lease (Configuration > Assets > Commercial Objects > State Lease).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_STATE_LEASE).
...                 NEVER touch existing data. A unique AUTOTEST_STL_<timestamp> code is generated
...                 per run. Section Start Date 2003-01-01: reference dropdowns are
...                 effective-date-filtered (object start date acts as a version).

Resource            ../../../../pageobjects/Configuration/Assets/Commercial_Objects/state_lease_page.resource

Suite Setup         Set Up State Lease Suite
Suite Teardown      Close EC

Test Tags           iud    state-lease


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       2003-01-01
${END_DATE}         2003-01-01


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test state lease does not exist before inserting.
    [Tags]    clean-state
    State Lease Row Should Not Exist    ${TEST_CODE}
    Capture Step    state_lease_tc01_clean

TC02 Insert New State Lease
    [Documentation]    Insert a new state lease and confirm it appears in the list.
    [Tags]    insert
    Insert State Lease Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    State Lease Row Should Exist    ${TEST_CODE}
    State Lease Should Exist In DB    ${TEST_CODE}
    Capture Step    state_lease_tc02_inserted

TC03 Update State Lease Name
    [Documentation]    Edit the state lease name and confirm the list reflects the change.
    [Tags]    update
    Update State Lease Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    State Lease Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    state_lease_tc03_updated

TC04 Delete State Lease
    [Documentation]    Delete via End Date = Start Date and confirm the state lease is gone.
    [Tags]    delete    cleanup
    Delete State Lease    ${TEST_CODE}    ${END_DATE}
    State Lease Row Should Not Exist    ${TEST_CODE}
    State Lease Should Not Exist In DB    ${TEST_CODE}
    Capture Step    state_lease_tc04_deleted


*** Keywords ***
Set Up State Lease Suite
    [Documentation]    Generate a unique test code/name, then open the State Lease screen.
    ${code}    Generate Unique Code    AUTOTEST_STL_
    VAR    ${TEST_CODE}    ${code}    scope=SUITE
    VAR    ${OBJ_NAME}    State Lease ${code}    scope=SUITE
    VAR    ${OBJ_NAME_UPD}    State Lease ${code} UPD    scope=SUITE
    Open State Lease Screen
