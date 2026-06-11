*** Settings ***
Documentation       EC IUD Test - Commercial Entity (Configuration > Assets > Commercial Objects > Commercial Entity).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_COMMERCIAL_ENTITY).
...                 NEVER touch existing data. A unique AUTOTEST_CE_<timestamp> code is generated
...                 per run. Section Start Date 2003-01-01: reference dropdowns are
...                 effective-date-filtered (object start date acts as a version).

Resource            ../../../../pageobjects/Configuration/Assets/Commercial_Objects/commercial_entity_page.resource

Suite Setup         Set Up Commercial Entity Suite
Suite Teardown      Close EC

Test Tags           iud    commercial-entity


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       2003-01-01
${END_DATE}         2003-01-01


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test commercial entity does not exist before inserting.
    [Tags]    clean-state
    Commercial Entity Row Should Not Exist    ${TEST_CODE}
    Capture Step    commercial_entity_tc01_clean

TC02 Insert New Commercial Entity
    [Documentation]    Insert a new commercial entity and confirm it appears in the list.
    [Tags]    insert
    Insert Commercial Entity Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Commercial Entity Row Should Exist    ${TEST_CODE}
    Commercial Entity Should Exist In DB    ${TEST_CODE}
    Capture Step    commercial_entity_tc02_inserted

TC03 Update Commercial Entity Name
    [Documentation]    Edit the commercial entity name and confirm the list reflects the change.
    [Tags]    update
    Update Commercial Entity Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Commercial Entity Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    commercial_entity_tc03_updated

TC04 Delete Commercial Entity
    [Documentation]    Delete via End Date = Start Date and confirm the commercial entity is gone.
    [Tags]    delete    cleanup
    Delete Commercial Entity    ${TEST_CODE}    ${END_DATE}
    Commercial Entity Row Should Not Exist    ${TEST_CODE}
    Commercial Entity Should Not Exist In DB    ${TEST_CODE}
    Capture Step    commercial_entity_tc04_deleted


*** Keywords ***
Set Up Commercial Entity Suite
    [Documentation]    Generate a unique test code/name, then open the Commercial Entity screen.
    ${code}    Generate Unique Code    AUTOTEST_CE_
    VAR    ${TEST_CODE}    ${code}    scope=SUITE
    VAR    ${OBJ_NAME}    Commercial Entity ${code}    scope=SUITE
    VAR    ${OBJ_NAME_UPD}    Commercial Entity ${code} UPD    scope=SUITE
    Open Commercial Entity Screen
