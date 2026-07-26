*** Settings ***
Documentation       EC IUD Test - UOP Key (Configuration > Assets > Revenue_Lists > UOP Key, CD.0099).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_FIN_UOP_DEPR_KEY).
...                 Layered: this test -> uop_key_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Unique AUTOTEST_UOP_<timestamp> code per run.

Resource            ../../../../pageobjects/Configuration/Assets/Revenue_Lists/uop_key_page.resource

Suite Setup         Set Up UOP Key Suite
Suite Teardown      Close EC

Test Tags           iud    uop_key


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test uop_key does not exist before inserting.
    [Tags]    clean-state
    UOP Key Row Should Not Exist    ${TEST_CODE}
    Capture Step    uop_key_tc01_clean

TC02 Insert New UOP Key
    [Documentation]    Insert a new uop_key; confirm in list + DB (OV_FIN_UOP_DEPR_KEY).
    [Tags]    insert
    Insert UOP Key Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    UOP Key Row Should Exist    ${TEST_CODE}
    UOP Key Should Exist In DB    ${TEST_CODE}
    Capture Step    uop_key_tc02_inserted

TC03 Update UOP Key
    [Documentation]    Edit Name; confirm in list + DB ground truth.
    [Tags]    update
    Update UOP Key Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    UOP Key Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Field Should Equal In View    OV_FIN_UOP_DEPR_KEY    ${TEST_CODE}    NAME    ${OBJ_NAME_UPD}
    Capture Step    uop_key_tc03_updated

TC04 Delete UOP Key
    [Documentation]    Delete via End Date = Start Date; confirm gone from list + DB.
    [Tags]    delete    cleanup
    Delete UOP Key    ${TEST_CODE}    ${END_DATE}
    UOP Key Row Should Not Exist    ${TEST_CODE}
    UOP Key Should Not Exist In DB    ${TEST_CODE}
    Capture Step    uop_key_tc04_deleted


*** Keywords ***
Set Up UOP Key Suite
    [Documentation]    Generate a unique test code/name, then open the UOP Key screen.
    Prepare IUD Object Data    AUTOTEST_UOP_    UOP Key
    Open UOP Key Screen
