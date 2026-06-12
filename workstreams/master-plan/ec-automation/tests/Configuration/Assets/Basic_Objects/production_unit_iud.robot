*** Settings ***
Documentation       EC IUD Test - Production Unit (Configuration > Assets > Basic Objects > Production Unit).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_PRODUCTIONUNIT).
...                 Layered: this test -> production_unit_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. A unique AUTOTEST_PU_<timestamp> code is generated
...                 per run (EC keeps deleted codes in the base table, so codes are never reused).

Resource            ../../../../pageobjects/Configuration/Assets/Basic_Objects/production_unit_page.resource

Suite Setup         Set Up Production Unit Suite
Suite Teardown      Close EC

Test Tags           iud    production-unit


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test production unit does not exist before inserting.
    [Tags]    clean-state
    Production Unit Row Should Not Exist    ${TEST_CODE}
    Capture Step    production_unit_tc01_clean

TC02 Insert New Production Unit
    [Documentation]    Insert a new production unit and confirm it appears in the list.
    [Tags]    insert
    Insert Production Unit Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Production Unit Row Should Exist    ${TEST_CODE}
    Production Unit Should Exist In DB    ${TEST_CODE}
    Capture Step    production_unit_tc02_inserted

TC03 Update Production Unit Name
    [Documentation]    Edit the production unit name and confirm the list reflects the change.
    [Tags]    update
    Update Production Unit Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Production Unit Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    production_unit_tc03_updated

TC04 Delete Production Unit
    [Documentation]    Delete via End Date = Start Date and confirm the production unit is gone.
    [Tags]    delete    cleanup
    Delete Production Unit    ${TEST_CODE}    ${END_DATE}
    Production Unit Row Should Not Exist    ${TEST_CODE}
    Production Unit Should Not Exist In DB    ${TEST_CODE}
    Capture Step    production_unit_tc04_deleted


*** Keywords ***
Set Up Production Unit Suite
    [Documentation]    Generate a unique test code/name, then open the Production Unit screen.
    Prepare IUD Object Data    AUTOTEST_PU_    Production Unit
    Open Production Unit Screen
