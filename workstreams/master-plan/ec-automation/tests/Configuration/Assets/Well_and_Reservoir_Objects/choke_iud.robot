*** Settings ***
Documentation       EC IUD Test - Choke (Configuration > Assets > Well and Reservoir Objects > Choke, CO.0185).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_CHOKE).
...                 Layered: this test -> choke_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Unique AUTOTEST_CHK_<timestamp> code per run.

Resource            ../../../../pageobjects/Configuration/Assets/Well_and_Reservoir_Objects/choke_page.resource

Suite Setup         Set Up Choke Suite
Suite Teardown      Close EC

Test Tags           iud    choke


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${OBJ_CMT_UPD}      AUTOTEST cmt UPDATED
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test choke does not exist before inserting.
    [Tags]    clean-state
    Choke Row Should Not Exist    ${TEST_CODE}
    Capture Step    choke_tc01_clean

TC02 Insert New Choke
    [Documentation]    Insert a new choke; confirm in list + DB (OV_CHOKE).
    [Tags]    insert
    Insert Choke Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Choke Row Should Exist    ${TEST_CODE}
    Choke Should Exist In DB    ${TEST_CODE}
    Capture Step    choke_tc02_inserted

TC03 Update Choke
    [Documentation]    Edit Name + Comments; confirm in list + DB ground truth.
    [Tags]    update
    Update Choke    ${TEST_CODE}    ${OBJ_NAME_UPD}    ${OBJ_CMT_UPD}
    Choke Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Field Should Equal In View    OV_CHOKE    ${TEST_CODE}    NAME    ${OBJ_NAME_UPD}
    Field Should Equal In View    OV_CHOKE    ${TEST_CODE}    COMMENTS    ${OBJ_CMT_UPD}
    Capture Step    choke_tc03_updated

TC04 Delete Choke
    [Documentation]    Delete via End Date = Start Date; confirm gone from list + DB.
    [Tags]    delete    cleanup
    Delete Choke    ${TEST_CODE}    ${END_DATE}
    Choke Row Should Not Exist    ${TEST_CODE}
    Choke Should Not Exist In DB    ${TEST_CODE}
    Capture Step    choke_tc04_deleted


*** Keywords ***
Set Up Choke Suite
    [Documentation]    Generate a unique test code/name, then open the Choke screen.
    Prepare IUD Object Data    AUTOTEST_CHK_    Choke
    Open Choke Screen
