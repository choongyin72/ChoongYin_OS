*** Settings ***
Documentation       EC IUD Test - Functional Area (Configuration > Assets > Basic Objects > Functional Area).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_FUNCTIONAL_AREA).
...                 Layered: this test -> functional_area_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. A unique AUTOTEST_FA_<timestamp> code is generated
...                 per run (EC keeps deleted codes in the base table, so codes are never reused).

Resource            ../../../../pageobjects/Configuration/Assets/Basic_Objects/functional_area_page.resource

Suite Setup         Set Up Functional Area Suite
Suite Teardown      Close EC

Test Tags           iud    functional-area


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       2000-01-01
${END_DATE}         2000-01-01


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test functional area does not exist before inserting.
    [Tags]    clean-state
    Functional Area Row Should Not Exist    ${TEST_CODE}
    Capture Step    functional_area_tc01_clean

TC02 Insert New Functional Area
    [Documentation]    Insert a new functional area and confirm it appears in the list.
    [Tags]    insert
    Insert Functional Area Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Functional Area Row Should Exist    ${TEST_CODE}
    Functional Area Should Exist In DB    ${TEST_CODE}
    Capture Step    functional_area_tc02_inserted

TC03 Update Functional Area Name
    [Documentation]    Edit the functional area name and confirm the list reflects the change.
    [Tags]    update
    Update Functional Area Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Functional Area Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    functional_area_tc03_updated

TC04 Delete Functional Area
    [Documentation]    Delete via End Date = Start Date and confirm the functional area is gone.
    [Tags]    delete    cleanup
    Delete Functional Area    ${TEST_CODE}    ${END_DATE}
    Functional Area Row Should Not Exist    ${TEST_CODE}
    Functional Area Should Not Exist In DB    ${TEST_CODE}
    Capture Step    functional_area_tc04_deleted


*** Keywords ***
Set Up Functional Area Suite
    [Documentation]    Generate a unique test code/name, then open the Functional Area screen.
    ${code}    Generate Unique Code    AUTOTEST_FA_
    VAR    ${TEST_CODE}    ${code}    scope=SUITE
    VAR    ${OBJ_NAME}    Functional Area ${code}    scope=SUITE
    VAR    ${OBJ_NAME_UPD}    Functional Area ${code} UPD    scope=SUITE
    Open Functional Area Screen
