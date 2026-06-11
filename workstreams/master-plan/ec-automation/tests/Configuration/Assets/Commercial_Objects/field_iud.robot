*** Settings ***
Documentation       EC IUD Test - Field (Configuration > Assets > Commercial Objects > Field).
...                 Manage-Object (OV-GM groupmodel) screen. DELETE = End Date = Start Date (true delete in OV_FIELD).
...                 NEVER touch existing data. A unique AUTOTEST_FLD_<timestamp> code is generated
...                 per run. Section Start Date 2003-01-01: reference dropdowns are
...                 effective-date-filtered (object start date acts as a version).

Resource            ../../../../pageobjects/Configuration/Assets/Commercial_Objects/field_page.resource

Suite Setup         Set Up Field Suite
Suite Teardown      Close EC

Test Tags           iud    field


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       2003-01-01
${END_DATE}         2003-01-01


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test field does not exist before inserting.
    [Tags]    clean-state
    Field Row Should Not Exist    ${TEST_CODE}
    Capture Step    field_tc01_clean

TC02 Insert New Field
    [Documentation]    Insert a new field and confirm it appears in the list.
    [Tags]    insert
    Insert Field Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Field Row Should Exist    ${TEST_CODE}
    Field Should Exist In DB    ${TEST_CODE}
    Capture Step    field_tc02_inserted

TC03 Update Field Name
    [Documentation]    Edit the field name and confirm the list reflects the change.
    [Tags]    update
    Update Field Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Field Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    field_tc03_updated

TC04 Delete Field
    [Documentation]    Delete via End Date = Start Date and confirm the field is gone.
    [Tags]    delete    cleanup
    Delete Field    ${TEST_CODE}    ${END_DATE}
    Field Row Should Not Exist    ${TEST_CODE}
    Field Should Not Exist In DB    ${TEST_CODE}
    Capture Step    field_tc04_deleted


*** Keywords ***
Set Up Field Suite
    [Documentation]    Generate a unique test code/name, then open the Field screen.
    ${code}    Generate Unique Code    AUTOTEST_FLD_
    VAR    ${TEST_CODE}    ${code}    scope=SUITE
    VAR    ${OBJ_NAME}    Field ${code}    scope=SUITE
    VAR    ${OBJ_NAME_UPD}    Field ${code} UPD    scope=SUITE
    Open Field Screen
