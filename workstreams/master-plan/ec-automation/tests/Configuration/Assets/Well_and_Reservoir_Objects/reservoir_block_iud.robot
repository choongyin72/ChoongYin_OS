*** Settings ***
Documentation       EC IUD Test - Reservoir Block (Configuration > Assets > Well_and_Reservoir_Objects > Reservoir Block, CO.0133).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_RESV_BLOCK).
...                 Layered: this test -> reservoir_block_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Unique AUTOTEST_RESVB_<timestamp> code per run.

Resource            ../../../../pageobjects/Configuration/Assets/Well_and_Reservoir_Objects/reservoir_block_page.resource

Suite Setup         Set Up Reservoir Block Suite
Suite Teardown      Close EC

Test Tags           iud    reservoir_block


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test reservoir_block does not exist before inserting.
    [Tags]    clean-state
    Reservoir Block Row Should Not Exist    ${TEST_CODE}
    Capture Step    reservoir_block_tc01_clean

TC02 Insert New Reservoir Block
    [Documentation]    Insert a new reservoir_block; confirm in list + DB (OV_RESV_BLOCK).
    [Tags]    insert
    Insert Reservoir Block Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Reservoir Block Row Should Exist    ${TEST_CODE}
    Reservoir Block Should Exist In DB    ${TEST_CODE}
    Capture Step    reservoir_block_tc02_inserted

TC03 Update Reservoir Block
    [Documentation]    Edit Name; confirm in list + DB ground truth.
    [Tags]    update
    Update Reservoir Block Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Reservoir Block Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Field Should Equal In View    OV_RESV_BLOCK    ${TEST_CODE}    NAME    ${OBJ_NAME_UPD}
    Capture Step    reservoir_block_tc03_updated

TC04 Delete Reservoir Block
    [Documentation]    Delete via End Date = Start Date; confirm gone from list + DB.
    [Tags]    delete    cleanup
    Delete Reservoir Block    ${TEST_CODE}    ${END_DATE}
    Reservoir Block Row Should Not Exist    ${TEST_CODE}
    Reservoir Block Should Not Exist In DB    ${TEST_CODE}
    Capture Step    reservoir_block_tc04_deleted


*** Keywords ***
Set Up Reservoir Block Suite
    [Documentation]    Generate a unique test code/name, then open the Reservoir Block screen.
    Prepare IUD Object Data    AUTOTEST_RESVB_    Reservoir Block
    Open Reservoir Block Screen
