*** Settings ***
Documentation       EC IUD Test - Field Group (Configuration > Assets > Commercial Objects > Field Group).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_FIELD_GROUP).
...                 NEVER touch existing data. A unique AUTOTEST_FG_<timestamp> code is generated
...                 per run. Section Start Date 2003-01-01: reference dropdowns are
...                 effective-date-filtered (object start date acts as a version).

Resource            ../../../../pageobjects/Configuration/Assets/Commercial_Objects/field_group_page.resource

Suite Setup         Set Up Field Group Suite
Suite Teardown      Close EC

Test Tags           iud    field-group


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       2003-01-01
${END_DATE}         2003-01-01


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test field group does not exist before inserting.
    [Tags]    clean-state
    Field Group Row Should Not Exist    ${TEST_CODE}
    Capture Step    field_group_tc01_clean

TC02 Insert New Field Group
    [Documentation]    Insert a new field group and confirm it appears in the list.
    [Tags]    insert
    Insert Field Group Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Field Group Row Should Exist    ${TEST_CODE}
    Field Group Should Exist In DB    ${TEST_CODE}
    Capture Step    field_group_tc02_inserted

TC03 Update Field Group Name
    [Documentation]    Edit the field group name and confirm the list reflects the change.
    [Tags]    update
    Update Field Group Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Field Group Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    field_group_tc03_updated

TC04 Delete Field Group
    [Documentation]    Delete via End Date = Start Date and confirm the field group is gone.
    [Tags]    delete    cleanup
    Delete Field Group    ${TEST_CODE}    ${END_DATE}
    Field Group Row Should Not Exist    ${TEST_CODE}
    Field Group Should Not Exist In DB    ${TEST_CODE}
    Capture Step    field_group_tc04_deleted


*** Keywords ***
Set Up Field Group Suite
    [Documentation]    Generate a unique test code/name, then open the Field Group screen.
    ${code}    Generate Unique Code    AUTOTEST_FG_
    VAR    ${TEST_CODE}    ${code}    scope=SUITE
    VAR    ${OBJ_NAME}    Field Group ${code}    scope=SUITE
    VAR    ${OBJ_NAME_UPD}    Field Group ${code} UPD    scope=SUITE
    Open Field Group Screen
