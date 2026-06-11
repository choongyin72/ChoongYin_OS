*** Settings ***
Documentation       EC IUD Test - Regulatory Permits (Configuration > Assets > Basic Objects > Regulatory Permits).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_REGULATORY_PERMITS).
...                 Layered: this test -> regulatory_permits_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. A unique AUTOTEST_RP_<timestamp> code is generated
...                 per run (EC keeps deleted codes in the base table, so codes are never reused).

Resource            ../../../../pageobjects/Configuration/Assets/Basic_Objects/regulatory_permits_page.resource

Suite Setup         Set Up Regulatory Permits Suite
Suite Teardown      Close EC

Test Tags           iud    regulatory-permits


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       2000-01-01
${END_DATE}         2000-01-01
# issuing agency for the throwaway test permit - user-approved 2026-06-11
${PERMIT_AGENCY}    Texas RRC


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test regulatory permits does not exist before inserting.
    [Tags]    clean-state
    Regulatory Permits Row Should Not Exist    ${TEST_CODE}
    Capture Step    regulatory_permits_tc01_clean

TC02 Insert New Regulatory Permits
    [Documentation]    Insert a new regulatory permits and confirm it appears in the list.
    [Tags]    insert
    Insert Regulatory Permits Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}    ${PERMIT_AGENCY}
    Regulatory Permits Row Should Exist    ${TEST_CODE}
    Regulatory Permits Should Exist In DB    ${TEST_CODE}
    Capture Step    regulatory_permits_tc02_inserted

TC03 Update Regulatory Permits Name
    [Documentation]    Edit the regulatory permits name and confirm the list reflects the change.
    [Tags]    update
    Update Regulatory Permits Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Regulatory Permits Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    regulatory_permits_tc03_updated

TC04 Delete Regulatory Permits
    [Documentation]    Delete via End Date = Start Date and confirm the regulatory permits is gone.
    [Tags]    delete    cleanup
    Delete Regulatory Permits    ${TEST_CODE}    ${END_DATE}
    Regulatory Permits Row Should Not Exist    ${TEST_CODE}
    Regulatory Permits Should Not Exist In DB    ${TEST_CODE}
    Capture Step    regulatory_permits_tc04_deleted


*** Keywords ***
Set Up Regulatory Permits Suite
    [Documentation]    Generate a unique test code/name, then open the Regulatory Permits screen.
    ${code}    Generate Unique Code    AUTOTEST_RP_
    VAR    ${TEST_CODE}    ${code}    scope=SUITE
    VAR    ${OBJ_NAME}    Regulatory Permits ${code}    scope=SUITE
    VAR    ${OBJ_NAME_UPD}    Regulatory Permits ${code} UPD    scope=SUITE
    Open Regulatory Permits Screen
