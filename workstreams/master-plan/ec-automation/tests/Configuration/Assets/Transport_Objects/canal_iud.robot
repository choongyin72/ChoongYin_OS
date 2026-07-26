*** Settings ***
Documentation       EC IUD Test - Canal (Configuration > Assets > Transport_Objects > Canal, CO.2069).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_CANAL).
...                 Layered: this test -> canal_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Unique AUTOTEST_CANAL_<timestamp> code per run.

Resource            ../../../../pageobjects/Configuration/Assets/Transport_Objects/canal_page.resource

Suite Setup         Set Up Canal Suite
Suite Teardown      Close EC

Test Tags           iud    canal


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test canal does not exist before inserting.
    [Tags]    clean-state
    Canal Row Should Not Exist    ${TEST_CODE}
    Capture Step    canal_tc01_clean

TC02 Insert New Canal
    [Documentation]    Insert a new canal; confirm in list + DB (OV_CANAL).
    [Tags]    insert
    Insert Canal Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Canal Row Should Exist    ${TEST_CODE}
    Canal Should Exist In DB    ${TEST_CODE}
    Capture Step    canal_tc02_inserted

TC03 Update Canal
    [Documentation]    Edit Name; confirm in list + DB ground truth.
    [Tags]    update
    Update Canal Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Canal Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Field Should Equal In View    OV_CANAL    ${TEST_CODE}    NAME    ${OBJ_NAME_UPD}
    Capture Step    canal_tc03_updated

TC04 Delete Canal
    [Documentation]    Delete via End Date = Start Date; confirm gone from list + DB.
    [Tags]    delete    cleanup
    Delete Canal    ${TEST_CODE}    ${END_DATE}
    Canal Row Should Not Exist    ${TEST_CODE}
    Canal Should Not Exist In DB    ${TEST_CODE}
    Capture Step    canal_tc04_deleted


*** Keywords ***
Set Up Canal Suite
    [Documentation]    Generate a unique test code/name, then open the Canal screen.
    Prepare IUD Object Data    AUTOTEST_CANAL_    Canal
    Open Canal Screen
