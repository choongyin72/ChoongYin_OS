*** Settings ***
Documentation       EC IUD Test - Stream Item Category (Configuration > Assets > Stream_Objects > Stream Item Category, CD.0016).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_STREAM_ITEM_CATEGORY).
...                 Layered: this test -> stream_item_category_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Unique AUTOTEST_SIC_<timestamp> code per run.

Resource            ../../../../pageobjects/Configuration/Assets/Stream_Objects/stream_item_category_page.resource

Suite Setup         Set Up Stream Item Category Suite
Suite Teardown      Close EC

Test Tags           iud    stream_item_category


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test stream_item_category does not exist before inserting.
    [Tags]    clean-state
    Stream Item Category Row Should Not Exist    ${TEST_CODE}
    Capture Step    stream_item_category_tc01_clean

TC02 Insert New Stream Item Category
    [Documentation]    Insert a new stream_item_category; confirm in list + DB (OV_STREAM_ITEM_CATEGORY).
    [Tags]    insert
    Insert Stream Item Category Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Stream Item Category Row Should Exist    ${TEST_CODE}
    Stream Item Category Should Exist In DB    ${TEST_CODE}
    Capture Step    stream_item_category_tc02_inserted

TC03 Update Stream Item Category
    [Documentation]    Edit Name; confirm in list + DB ground truth.
    [Tags]    update
    Update Stream Item Category Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Stream Item Category Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Field Should Equal In View    OV_STREAM_ITEM_CATEGORY    ${TEST_CODE}    NAME    ${OBJ_NAME_UPD}
    Capture Step    stream_item_category_tc03_updated

TC04 Delete Stream Item Category
    [Documentation]    Delete via End Date = Start Date; confirm gone from list + DB.
    [Tags]    delete    cleanup
    Delete Stream Item Category    ${TEST_CODE}    ${END_DATE}
    Stream Item Category Row Should Not Exist    ${TEST_CODE}
    Stream Item Category Should Not Exist In DB    ${TEST_CODE}
    Capture Step    stream_item_category_tc04_deleted


*** Keywords ***
Set Up Stream Item Category Suite
    [Documentation]    Generate a unique test code/name, then open the Stream Item Category screen.
    Prepare IUD Object Data    AUTOTEST_SIC_    Stream Item Category
    Open Stream Item Category Screen
