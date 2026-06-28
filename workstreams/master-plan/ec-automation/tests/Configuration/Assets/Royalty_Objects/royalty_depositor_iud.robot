*** Settings ***
Documentation       EC IUD Test - Royalty Depositor (Configuration > Assets > Royalty Objects > Royalty Depositor).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in ov_royalty_depositor).
...                 Layered: this test -> royalty_depositor_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. A unique AUTOTEST_RD_<timestamp> code is generated
...                 per run (EC keeps deleted codes in the base table, so codes are never reused).

Resource            ../../../../pageobjects/Configuration/Assets/Royalty_Objects/royalty_depositor_page.resource

Suite Setup         Set Up Royalty Depositor Suite
Suite Teardown      Close EC

Test Tags           iud    royalty_depositor


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}        ${EMPTY}
${OBJ_NAME_UPD}    ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test royalty depositor does not exist before inserting.
    [Tags]    clean-state
    Royalty Depositor Row Should Not Exist    ${TEST_CODE}
    Capture Step    royalty_depositor_tc01_clean

TC02 Insert New Royalty Depositor
    [Documentation]    Insert a new royalty depositor and confirm it appears in the list.
    [Tags]    insert
    Insert Royalty Depositor Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Royalty Depositor Row Should Exist    ${TEST_CODE}
    Royalty Depositor Should Exist In DB    ${TEST_CODE}
    Capture Step    royalty_depositor_tc02_inserted

TC03 Update Royalty Depositor Name
    [Documentation]    Edit the royalty depositor name and confirm the list reflects the change.
    [Tags]    update
    Update Royalty Depositor Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Royalty Depositor Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    royalty_depositor_tc03_updated

TC04 Delete Royalty Depositor
    [Documentation]    Delete via End Date = Start Date and confirm the royalty depositor is gone.
    [Tags]    delete    cleanup
    Delete Royalty Depositor    ${TEST_CODE}    ${END_DATE}
    Royalty Depositor Row Should Not Exist    ${TEST_CODE}
    Royalty Depositor Should Not Exist In DB    ${TEST_CODE}
    Capture Step    royalty_depositor_tc04_deleted


*** Keywords ***
Set Up Royalty Depositor Suite
    [Documentation]    Generate a unique test code/name, then open the Royalty Depositor screen.
    Prepare IUD Object Data    AUTOTEST_RD_    Royalty Depositor
    Open Royalty Depositor Screen
