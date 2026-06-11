*** Settings ***
Documentation       EC IUD Test - Operator Lease (Configuration > Assets > Commercial Objects > Operator Lease).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_OPERATOR_LEASE).
...                 NEVER touch existing data. A unique AUTOTEST_OPL_<timestamp> code is generated
...                 per run. Section Start Date 2003-01-01: reference dropdowns are
...                 effective-date-filtered (object start date acts as a version).

Resource            ../../../../pageobjects/Configuration/Assets/Commercial_Objects/operator_lease_page.resource

Suite Setup         Set Up Operator Lease Suite
Suite Teardown      Close EC

Test Tags           iud    operator-lease


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       2003-01-01
${END_DATE}         2003-01-01


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test operator lease does not exist before inserting.
    [Tags]    clean-state
    Operator Lease Row Should Not Exist    ${TEST_CODE}
    Capture Step    operator_lease_tc01_clean

TC02 Insert New Operator Lease
    [Documentation]    Insert a new operator lease and confirm it appears in the list.
    [Tags]    insert
    Insert Operator Lease Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Operator Lease Row Should Exist    ${TEST_CODE}
    Operator Lease Should Exist In DB    ${TEST_CODE}
    Capture Step    operator_lease_tc02_inserted

TC03 Update Operator Lease Name
    [Documentation]    Edit the operator lease name and confirm the list reflects the change.
    [Tags]    update
    Update Operator Lease Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Operator Lease Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    operator_lease_tc03_updated

TC04 Delete Operator Lease
    [Documentation]    Delete via End Date = Start Date and confirm the operator lease is gone.
    [Tags]    delete    cleanup
    Delete Operator Lease    ${TEST_CODE}    ${END_DATE}
    Operator Lease Row Should Not Exist    ${TEST_CODE}
    Operator Lease Should Not Exist In DB    ${TEST_CODE}
    Capture Step    operator_lease_tc04_deleted


*** Keywords ***
Set Up Operator Lease Suite
    [Documentation]    Generate a unique test code/name, then open the Operator Lease screen.
    ${code}    Generate Unique Code    AUTOTEST_OPL_
    VAR    ${TEST_CODE}    ${code}    scope=SUITE
    VAR    ${OBJ_NAME}    Operator Lease ${code}    scope=SUITE
    VAR    ${OBJ_NAME_UPD}    Operator Lease ${code} UPD    scope=SUITE
    Open Operator Lease Screen
