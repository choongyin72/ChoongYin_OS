*** Settings ***
Documentation       EC IUD Test - Unit Agreement (Configuration > Assets > Royalty Objects > Unit Agreement).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in ov_unit_agr).
...                 Layered: this test -> unit_agreement_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. A unique AUTOTEST_UA_<timestamp> code is generated
...                 per run (EC keeps deleted codes in the base table, so codes are never reused).

Resource            ../../../../pageobjects/Configuration/Assets/Royalty_Objects/unit_agreement_page.resource

Suite Setup         Set Up Unit Agreement Suite
Suite Teardown      Close EC

Test Tags           iud    unit_agreement


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}        ${EMPTY}
${OBJ_NAME_UPD}    ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test unit agreement does not exist before inserting.
    [Tags]    clean-state
    Unit Agreement Row Should Not Exist    ${TEST_CODE}
    Capture Step    unit_agreement_tc01_clean

TC02 Insert New Unit Agreement
    [Documentation]    Insert a new unit agreement and confirm it appears in the list.
    [Tags]    insert
    Insert Unit Agreement Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Unit Agreement Row Should Exist    ${TEST_CODE}
    Unit Agreement Should Exist In DB    ${TEST_CODE}
    Capture Step    unit_agreement_tc02_inserted

TC03 Update Unit Agreement Name
    [Documentation]    Edit the unit agreement name and confirm the list reflects the change.
    [Tags]    update
    Update Unit Agreement Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Unit Agreement Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    unit_agreement_tc03_updated

TC04 Delete Unit Agreement
    [Documentation]    Delete via End Date = Start Date and confirm the unit agreement is gone.
    [Tags]    delete    cleanup
    Delete Unit Agreement    ${TEST_CODE}    ${END_DATE}
    Unit Agreement Row Should Not Exist    ${TEST_CODE}
    Unit Agreement Should Not Exist In DB    ${TEST_CODE}
    Capture Step    unit_agreement_tc04_deleted


*** Keywords ***
Set Up Unit Agreement Suite
    [Documentation]    Generate a unique test code/name, then open the Unit Agreement screen.
    Prepare IUD Object Data    AUTOTEST_UA_    Unit Agreement
    Open Unit Agreement Screen
