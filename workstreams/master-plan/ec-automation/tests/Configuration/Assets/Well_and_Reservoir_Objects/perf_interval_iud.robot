*** Settings ***
Documentation       EC IUD Test - Perforation Interval (Configuration > Assets > Well_and_Reservoir_Objects).
...                 OV-GM, per-field nav groups with SPECIFIC values (G:4 = a REAL well, P1 W008 OP;
...                 G:5 skipped - zero options under every scope tried). Mandatory 'Well' POPUP with
...                 list grid Objects:form:T_data (screen-local picker; picks the nav-scope well, not
...                 the popup's first row which is a graph object). DELETE = End Date = Start Date
...                 (true delete in OV_PERF_INTERVAL). NEVER touch existing data; unique
...                 AUTOTEST_PI_<timestamp> code per run. Start Date 2020-01-01.

Resource            ../../../../pageobjects/Configuration/Assets/Well_and_Reservoir_Objects/perf_interval_page.resource

Suite Setup         Set Up Perforation Interval Suite
Suite Teardown      Close EC

Test Tags           iud    perf-interval


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
    Perforation Interval Row Should Not Exist    ${TEST_CODE}
    Capture Step    perf_interval_tc01_clean

TC02 Insert New Perforation Interval
    [Documentation]    Insert under the P1 well scope (incl. the mandatory Well popup) and confirm it lists.
    [Tags]    insert
    Insert Perforation Interval Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Perforation Interval Row Should Exist    ${TEST_CODE}
    Perforation Interval Should Exist In DB    ${TEST_CODE}
    Capture Step    perf_interval_tc02_inserted

TC03 Update Perforation Interval Name
    [Documentation]    Edit the name and confirm the list reflects the change.
    [Tags]    update
    Update Perforation Interval Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Perforation Interval Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    perf_interval_tc03_updated

TC04 Delete Perforation Interval
    [Documentation]    Delete via End Date = Start Date and confirm it is gone.
    [Tags]    delete    cleanup
    Delete Perforation Interval    ${TEST_CODE}    ${END_DATE}
    Perforation Interval Row Should Not Exist    ${TEST_CODE}
    Perforation Interval Should Not Exist In DB    ${TEST_CODE}
    Capture Step    perf_interval_tc04_deleted


*** Keywords ***
Set Up Perforation Interval Suite
    [Documentation]    Generate a unique test code/name, open the screen, apply the P1 nav scope.
    Prepare IUD Object Data    AUTOTEST_PI_    Perforation Interval
    Open Perforation Interval Screen
