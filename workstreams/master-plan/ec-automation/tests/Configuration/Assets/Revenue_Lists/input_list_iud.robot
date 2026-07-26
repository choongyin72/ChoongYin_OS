*** Settings ***
Documentation       EC IUD Test - Input List (Configuration > Assets > Revenue_Lists > Input List, CD.0035).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_STREAM_ITEM_COLLECTION).
...                 Layered: this test -> input_list_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Unique AUTOTEST_IL_<timestamp> code per run.

Resource            ../../../../pageobjects/Configuration/Assets/Revenue_Lists/input_list_page.resource

Suite Setup         Set Up Input List Suite
Suite Teardown      Close EC

Test Tags           iud    input_list


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test input_list does not exist before inserting.
    [Tags]    clean-state
    Input List Row Should Not Exist    ${TEST_CODE}
    Capture Step    input_list_tc01_clean

TC02 Insert New Input List
    [Documentation]    Insert a new input_list; confirm in list + DB (OV_STREAM_ITEM_COLLECTION).
    [Tags]    insert
    Insert Input List Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Input List Row Should Exist    ${TEST_CODE}
    Input List Should Exist In DB    ${TEST_CODE}
    Capture Step    input_list_tc02_inserted

TC03 Update Input List
    [Documentation]    Edit Name; confirm in list + DB ground truth.
    [Tags]    update
    Update Input List Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Input List Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Field Should Equal In View    OV_STREAM_ITEM_COLLECTION    ${TEST_CODE}    NAME    ${OBJ_NAME_UPD}
    Capture Step    input_list_tc03_updated

TC04 Delete Input List
    [Documentation]    Delete via End Date = Start Date; confirm gone from list + DB.
    [Tags]    delete    cleanup
    Delete Input List    ${TEST_CODE}    ${END_DATE}
    Input List Row Should Not Exist    ${TEST_CODE}
    Input List Should Not Exist In DB    ${TEST_CODE}
    Capture Step    input_list_tc04_deleted


*** Keywords ***
Set Up Input List Suite
    [Documentation]    Generate a unique test code/name, then open the Input List screen.
    Prepare IUD Object Data    AUTOTEST_IL_    Input List
    Open Input List Screen
