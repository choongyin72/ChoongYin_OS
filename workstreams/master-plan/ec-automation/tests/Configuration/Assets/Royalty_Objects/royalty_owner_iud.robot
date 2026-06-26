*** Settings ***
Documentation       EC IUD Test - Royalty Owner (Configuration > Assets > Royalty Objects > Royalty Owner).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in ov_royalty_owner).
...                 Layered: this test -> royalty_owner_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. A unique AUTOTEST_RO_<timestamp> code is generated
...                 per run (EC keeps deleted codes in the base table, so codes are never reused).

Resource            ../../../../pageobjects/Configuration/Assets/Royalty_Objects/royalty_owner_page.resource

Suite Setup         Set Up Royalty Owner Suite
Suite Teardown      Close EC

Test Tags           iud    royalty_owner


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}        ${EMPTY}
${OBJ_NAME_UPD}    ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test royalty owner does not exist before inserting.
    [Tags]    clean-state
    Royalty Owner Row Should Not Exist    ${TEST_CODE}
    Capture Step    royalty_owner_tc01_clean

TC02 Insert New Royalty Owner
    [Documentation]    Insert a new royalty owner and confirm it appears in the list.
    [Tags]    insert
    Insert Royalty Owner Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Royalty Owner Row Should Exist    ${TEST_CODE}
    Royalty Owner Should Exist In DB    ${TEST_CODE}
    Capture Step    royalty_owner_tc02_inserted

TC03 Update Royalty Owner Name
    [Documentation]    Edit the royalty owner name and confirm the list reflects the change.
    [Tags]    update
    Update Royalty Owner Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Royalty Owner Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    royalty_owner_tc03_updated

TC04 Delete Royalty Owner
    [Documentation]    Delete via End Date = Start Date and confirm the royalty owner is gone.
    [Tags]    delete    cleanup
    Delete Royalty Owner    ${TEST_CODE}    ${END_DATE}
    Royalty Owner Row Should Not Exist    ${TEST_CODE}
    Royalty Owner Should Not Exist In DB    ${TEST_CODE}
    Capture Step    royalty_owner_tc04_deleted


*** Keywords ***
Set Up Royalty Owner Suite
    [Documentation]    Generate a unique test code/name, then open the Royalty Owner screen.
    Prepare IUD Object Data    AUTOTEST_RO_    Royalty Owner
    Open Royalty Owner Screen
