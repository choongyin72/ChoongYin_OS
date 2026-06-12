*** Settings ***
Documentation       EC IUD Test - Object List (Configuration > Assets > Basic Objects > Object List).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_OBJECT_LIST).
...                 Layered: this test -> object_list_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. A unique AUTOTEST_OL_<timestamp> code is generated
...                 per run (EC keeps deleted codes in the base table, so codes are never reused).

Resource            ../../../../pageobjects/Configuration/Assets/Basic_Objects/object_list_page.resource

Suite Setup         Set Up Object List Suite
Suite Teardown      Close EC

Test Tags           iud    object-list


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}
# class of objects the (empty, throwaway) test list holds - user-approved 2026-06-11
${LIST_CLASS}       BANK


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test object list does not exist before inserting.
    [Tags]    clean-state
    Object List Row Should Not Exist    ${TEST_CODE}
    Capture Step    object_list_tc01_clean

TC02 Insert New Object List
    [Documentation]    Insert a new object list and confirm it appears in the list.
    [Tags]    insert
    Insert Object List Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}    ${LIST_CLASS}
    Object List Row Should Exist    ${TEST_CODE}
    Object List Should Exist In DB    ${TEST_CODE}
    Capture Step    object_list_tc02_inserted

TC03 Update Object List Name
    [Documentation]    Edit the object list name and confirm the list reflects the change.
    [Tags]    update
    Update Object List Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Object List Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    object_list_tc03_updated

TC04 Delete Object List
    [Documentation]    Delete via End Date = Start Date and confirm the object list is gone.
    [Tags]    delete    cleanup
    Delete Object List    ${TEST_CODE}    ${END_DATE}
    Object List Row Should Not Exist    ${TEST_CODE}
    Object List Should Not Exist In DB    ${TEST_CODE}
    Capture Step    object_list_tc04_deleted


*** Keywords ***
Set Up Object List Suite
    [Documentation]    Generate a unique test code/name, then open the Object List screen.
    Prepare IUD Object Data    AUTOTEST_OL_    Object List
    Open Object List Screen
