*** Settings ***
Documentation       EC IUD Test - Dummy Tag Event Object (Configuration > Integration_Services > Dummy Tag Event Object, CO.1063).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_DUMMY_TAG_EVENT).
...                 Layered: this test -> dummy_tag_event_object_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Unique AUTOTEST_DTE_<timestamp> code per run.

Resource            ../../../pageobjects/Configuration/Integration_Services/dummy_tag_event_object_page.resource

Suite Setup         Set Up Dummy Tag Event Object Suite
Suite Teardown      Close EC

Test Tags           iud    dummy_tag_event_object


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test dummy_tag_event_object does not exist before inserting.
    [Tags]    clean-state
    Dummy Tag Event Object Row Should Not Exist    ${TEST_CODE}
    Capture Step    dummy_tag_event_object_tc01_clean

TC02 Insert New Dummy Tag Event Object
    [Documentation]    Insert a new dummy_tag_event_object; confirm in list + DB (OV_DUMMY_TAG_EVENT).
    [Tags]    insert
    Insert Dummy Tag Event Object Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Dummy Tag Event Object Row Should Exist    ${TEST_CODE}
    Dummy Tag Event Object Should Exist In DB    ${TEST_CODE}
    Capture Step    dummy_tag_event_object_tc02_inserted

TC03 Update Dummy Tag Event Object
    [Documentation]    Edit Name; confirm in list + DB ground truth.
    [Tags]    update
    Update Dummy Tag Event Object Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Dummy Tag Event Object Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Field Should Equal In View    OV_DUMMY_TAG_EVENT    ${TEST_CODE}    NAME    ${OBJ_NAME_UPD}
    Capture Step    dummy_tag_event_object_tc03_updated

TC04 Delete Dummy Tag Event Object
    [Documentation]    Delete via End Date = Start Date; confirm gone from list + DB.
    [Tags]    delete    cleanup
    Delete Dummy Tag Event Object    ${TEST_CODE}    ${END_DATE}
    Dummy Tag Event Object Row Should Not Exist    ${TEST_CODE}
    Dummy Tag Event Object Should Not Exist In DB    ${TEST_CODE}
    Capture Step    dummy_tag_event_object_tc04_deleted


*** Keywords ***
Set Up Dummy Tag Event Object Suite
    [Documentation]    Generate a unique test code/name, then open the Dummy Tag Event Object screen.
    Prepare IUD Object Data    AUTOTEST_DTE_    Dummy Tag Event Object
    Open Dummy Tag Event Object Screen
