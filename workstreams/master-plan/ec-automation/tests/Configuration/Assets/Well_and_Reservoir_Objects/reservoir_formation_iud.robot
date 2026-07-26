*** Settings ***
Documentation       EC IUD Test - Reservoir Formation (Configuration > Assets > Well_and_Reservoir_Objects > Reservoir Formation, CO.0135).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_RESV_FORMATION).
...                 Layered: this test -> reservoir_formation_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Unique AUTOTEST_RESVF_<timestamp> code per run.

Resource            ../../../../pageobjects/Configuration/Assets/Well_and_Reservoir_Objects/reservoir_formation_page.resource

Suite Setup         Set Up Reservoir Formation Suite
Suite Teardown      Close EC

Test Tags           iud    reservoir_formation


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test reservoir_formation does not exist before inserting.
    [Tags]    clean-state
    Reservoir Formation Row Should Not Exist    ${TEST_CODE}
    Capture Step    reservoir_formation_tc01_clean

TC02 Insert New Reservoir Formation
    [Documentation]    Insert a new reservoir_formation; confirm in list + DB (OV_RESV_FORMATION).
    [Tags]    insert
    Insert Reservoir Formation Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Reservoir Formation Row Should Exist    ${TEST_CODE}
    Reservoir Formation Should Exist In DB    ${TEST_CODE}
    Capture Step    reservoir_formation_tc02_inserted

TC03 Update Reservoir Formation
    [Documentation]    Edit Name; confirm in list + DB ground truth.
    [Tags]    update
    Update Reservoir Formation Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Reservoir Formation Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Field Should Equal In View    OV_RESV_FORMATION    ${TEST_CODE}    NAME    ${OBJ_NAME_UPD}
    Capture Step    reservoir_formation_tc03_updated

TC04 Delete Reservoir Formation
    [Documentation]    Delete via End Date = Start Date; confirm gone from list + DB.
    [Tags]    delete    cleanup
    Delete Reservoir Formation    ${TEST_CODE}    ${END_DATE}
    Reservoir Formation Row Should Not Exist    ${TEST_CODE}
    Reservoir Formation Should Not Exist In DB    ${TEST_CODE}
    Capture Step    reservoir_formation_tc04_deleted


*** Keywords ***
Set Up Reservoir Formation Suite
    [Documentation]    Generate a unique test code/name, then open the Reservoir Formation screen.
    Prepare IUD Object Data    AUTOTEST_RESVF_    Reservoir Formation
    Open Reservoir Formation Screen
