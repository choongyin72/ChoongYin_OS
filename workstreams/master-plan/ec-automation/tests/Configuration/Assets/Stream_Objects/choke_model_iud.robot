*** Settings ***
Documentation       EC IUD Test - Choke Model (Configuration > Assets > Stream Objects > Choke Model, CO.0217).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_CHOKE_MODEL).
...                 Layered: this test -> choke_model_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Unique AUTOTEST_CHKM_<timestamp> code per run.

Resource            ../../../../pageobjects/Configuration/Assets/Stream_Objects/choke_model_page.resource

Suite Setup         Set Up Choke Model Suite
Suite Teardown      Close EC

Test Tags           iud    choke_model


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${OBJ_DESC_UPD}     AUTOTEST desc UPDATED
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test choke model does not exist before inserting.
    [Tags]    clean-state
    Choke Model Row Should Not Exist    ${TEST_CODE}
    Capture Step    choke_model_tc01_clean

TC02 Insert New Choke Model
    [Documentation]    Insert a new choke model; confirm in list + DB (OV_CHOKE_MODEL).
    [Tags]    insert
    Insert Choke Model Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Choke Model Row Should Exist    ${TEST_CODE}
    Choke Model Should Exist In DB    ${TEST_CODE}
    Capture Step    choke_model_tc02_inserted

TC03 Update Choke Model
    [Documentation]    Edit Name + Description; confirm in list + DB ground truth.
    [Tags]    update
    Update Choke Model    ${TEST_CODE}    ${OBJ_NAME_UPD}    ${OBJ_DESC_UPD}
    Choke Model Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Field Should Equal In View    OV_CHOKE_MODEL    ${TEST_CODE}    NAME    ${OBJ_NAME_UPD}
    Field Should Equal In View    OV_CHOKE_MODEL    ${TEST_CODE}    DESCRIPTION    ${OBJ_DESC_UPD}
    Capture Step    choke_model_tc03_updated

TC04 Delete Choke Model
    [Documentation]    Delete via End Date = Start Date; confirm gone from list + DB.
    [Tags]    delete    cleanup
    Delete Choke Model    ${TEST_CODE}    ${END_DATE}
    Choke Model Row Should Not Exist    ${TEST_CODE}
    Choke Model Should Not Exist In DB    ${TEST_CODE}
    Capture Step    choke_model_tc04_deleted


*** Keywords ***
Set Up Choke Model Suite
    [Documentation]    Generate a unique test code/name, then open the Choke Model screen.
    Prepare IUD Object Data    AUTOTEST_CHKM_    Choke Model
    Open Choke Model Screen
