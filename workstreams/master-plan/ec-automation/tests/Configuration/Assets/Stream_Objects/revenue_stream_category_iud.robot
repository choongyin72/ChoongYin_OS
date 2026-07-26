*** Settings ***
Documentation       EC IUD Test - Revenue Stream Category (Configuration > Assets > Stream_Objects > Revenue Stream Category, CD.0015).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_STREAM_CATEGORY).
...                 Layered: this test -> revenue_stream_category_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Unique AUTOTEST_RSC_<timestamp> code per run.

Resource            ../../../../pageobjects/Configuration/Assets/Stream_Objects/revenue_stream_category_page.resource

Suite Setup         Set Up Revenue Stream Category Suite
Suite Teardown      Close EC

Test Tags           iud    revenue_stream_category


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test revenue_stream_category does not exist before inserting.
    [Tags]    clean-state
    Revenue Stream Category Row Should Not Exist    ${TEST_CODE}
    Capture Step    revenue_stream_category_tc01_clean

TC02 Insert New Revenue Stream Category
    [Documentation]    Insert a new revenue_stream_category; confirm in list + DB (OV_STREAM_CATEGORY).
    [Tags]    insert
    Insert Revenue Stream Category Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Revenue Stream Category Row Should Exist    ${TEST_CODE}
    Revenue Stream Category Should Exist In DB    ${TEST_CODE}
    Capture Step    revenue_stream_category_tc02_inserted

TC03 Update Revenue Stream Category
    [Documentation]    Edit Name; confirm in list + DB ground truth.
    [Tags]    update
    Update Revenue Stream Category Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Revenue Stream Category Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Field Should Equal In View    OV_STREAM_CATEGORY    ${TEST_CODE}    NAME    ${OBJ_NAME_UPD}
    Capture Step    revenue_stream_category_tc03_updated

TC04 Delete Revenue Stream Category
    [Documentation]    Delete via End Date = Start Date; confirm gone from list + DB.
    [Tags]    delete    cleanup
    Delete Revenue Stream Category    ${TEST_CODE}    ${END_DATE}
    Revenue Stream Category Row Should Not Exist    ${TEST_CODE}
    Revenue Stream Category Should Not Exist In DB    ${TEST_CODE}
    Capture Step    revenue_stream_category_tc04_deleted


*** Keywords ***
Set Up Revenue Stream Category Suite
    [Documentation]    Generate a unique test code/name, then open the Revenue Stream Category screen.
    Prepare IUD Object Data    AUTOTEST_RSC_    Revenue Stream Category
    Open Revenue Stream Category Screen
