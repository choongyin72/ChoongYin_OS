*** Settings ***
Documentation       EC IUD Test - Calendar (Configuration > Assets > Date Objects > Calendar, CD.0024).
...                 Manage-Object (OV, date-effective) screen. Plain Bank-family OV (no mandatory extras).
...                 DELETE = End Date = Start Date (true delete in ov_calendar).
...                 Layered: this test -> calendar_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Unique AUTOTEST_CAL_<timestamp> code per run.

Resource            ../../../../pageobjects/Configuration/Assets/Date_Objects/calendar_page.resource

Suite Setup         Set Up Calendar Suite
Suite Teardown      Close EC

Test Tags           iud    calendar    date-objects


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test object does not exist before inserting.
    [Tags]    clean-state
    Calendar Row Should Not Exist    ${TEST_CODE}
    Calendar Should Not Exist In DB    ${TEST_CODE}
    Capture Step    cal_tc01_clean

TC02 Insert New Calendar
    [Documentation]    Insert a new Calendar (Code/Name/Start Date) and confirm it appears in the list and DB.
    [Tags]    insert
    Insert Calendar Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Calendar Row Should Exist    ${TEST_CODE}
    Calendar Should Exist In DB    ${TEST_CODE}
    Capture Step    cal_tc02_inserted

TC03 Update Calendar Name
    [Documentation]    Edit the name and confirm the list reflects the change.
    [Tags]    update
    Update Calendar Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Calendar Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    cal_tc03_updated

TC04 Delete Calendar
    [Documentation]    Delete via End Date = Start Date and confirm the object is gone from list and DB.
    [Tags]    delete    cleanup
    Delete Calendar    ${TEST_CODE}    ${END_DATE}
    Calendar Row Should Not Exist    ${TEST_CODE}
    Calendar Should Not Exist In DB    ${TEST_CODE}
    Capture Step    cal_tc04_deleted


*** Keywords ***
Set Up Calendar Suite
    [Documentation]    Generate a unique test code/name, then open the Calendar screen.
    Prepare IUD Object Data    AUTOTEST_CAL_    Calendar
    Open Calendar Screen
