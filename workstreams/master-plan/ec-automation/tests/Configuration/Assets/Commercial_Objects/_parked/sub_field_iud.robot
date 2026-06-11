*** Settings ***
Documentation       EC IUD Test - Sub Field (Configuration > Assets > Commercial Objects > Sub Field).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_SUB_FIELD).
...                 NEVER touch existing data. A unique AUTOTEST_SFLD_<timestamp> code is generated
...                 per run. Section Start Date 2003-01-01: reference dropdowns are
...                 effective-date-filtered (object start date acts as a version).

Resource            ../../../../../pageobjects/Configuration/Assets/Commercial_Objects/sub_field_page.resource

Suite Setup         Set Up Sub Field Suite
Suite Teardown      Close EC

Test Tags           iud    parked-groupmodel-not-enabled    sub-field


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       2003-01-01
${END_DATE}         2003-01-01


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test sub field does not exist before inserting.
    [Tags]    clean-state
    Sub Field Row Should Not Exist    ${TEST_CODE}
    Capture Step    sub_field_tc01_clean

TC02 Insert New Sub Field
    [Documentation]    Insert a new sub field and confirm it appears in the list.
    [Tags]    insert
    Insert Sub Field Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Sub Field Row Should Exist    ${TEST_CODE}
    Sub Field Should Exist In DB    ${TEST_CODE}
    Capture Step    sub_field_tc02_inserted

TC03 Update Sub Field Name
    [Documentation]    Edit the sub field name and confirm the list reflects the change.
    [Tags]    update
    Update Sub Field Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Sub Field Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    sub_field_tc03_updated

TC04 Delete Sub Field
    [Documentation]    Delete via End Date = Start Date and confirm the sub field is gone.
    [Tags]    delete    cleanup
    Delete Sub Field    ${TEST_CODE}    ${END_DATE}
    Sub Field Row Should Not Exist    ${TEST_CODE}
    Sub Field Should Not Exist In DB    ${TEST_CODE}
    Capture Step    sub_field_tc04_deleted


*** Keywords ***
Set Up Sub Field Suite
    [Documentation]    Generate a unique test code/name, then open the Sub Field screen.
    ${code}    Generate Unique Code    AUTOTEST_SFLD_
    VAR    ${TEST_CODE}    ${code}    scope=SUITE
    VAR    ${OBJ_NAME}    Sub Field ${code}    scope=SUITE
    VAR    ${OBJ_NAME_UPD}    Sub Field ${code} UPD    scope=SUITE
    Open Sub Field Screen
