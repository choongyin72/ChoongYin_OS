*** Settings ***
Documentation       EC IUD Test - Calendar Collection (Configuration > Assets > Date Objects > Calendar Collection, CD.0105).
...                 Manage-Object (OV, date-effective) screen. Plain Bank-family OV (no mandatory extras).
...                 DELETE = End Date = Start Date (true delete in ov_calendar_collection).
...                 Layered: this test -> calendar_collection_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Unique AUTOTEST_CC_<timestamp> code per run.

Resource            ../../../../pageobjects/Configuration/Assets/Date_Objects/calendar_collection_page.resource

Suite Setup         Set Up Calendar Collection Suite
Suite Teardown      Close EC

Test Tags           iud    calendar-collection    date-objects


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
    Calendar Collection Row Should Not Exist    ${TEST_CODE}
    Calendar Collection Should Not Exist In DB    ${TEST_CODE}
    Capture Step    cc_tc01_clean

TC02 Insert New Calendar Collection
    [Documentation]    Insert a new Calendar Collection (Code/Name/Start Date) and confirm it appears in the list and DB.
    [Tags]    insert
    Insert Calendar Collection Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Calendar Collection Row Should Exist    ${TEST_CODE}
    Calendar Collection Should Exist In DB    ${TEST_CODE}
    Capture Step    cc_tc02_inserted

TC03 Update Calendar Collection Name
    [Documentation]    Edit the name and confirm the list reflects the change.
    [Tags]    update
    Update Calendar Collection Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Calendar Collection Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    cc_tc03_updated

TC04 Delete Calendar Collection
    [Documentation]    Delete via End Date = Start Date and confirm the object is gone from list and DB.
    [Tags]    delete    cleanup
    Delete Calendar Collection    ${TEST_CODE}    ${END_DATE}
    Calendar Collection Row Should Not Exist    ${TEST_CODE}
    Calendar Collection Should Not Exist In DB    ${TEST_CODE}
    Capture Step    cc_tc04_deleted


*** Keywords ***
Set Up Calendar Collection Suite
    [Documentation]    Generate a unique test code/name, then open the Calendar Collection screen.
    Prepare IUD Object Data    AUTOTEST_CC_    Calendar Collection
    Open Calendar Collection Screen
