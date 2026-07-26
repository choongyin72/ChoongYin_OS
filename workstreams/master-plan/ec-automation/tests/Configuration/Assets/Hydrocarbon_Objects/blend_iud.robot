*** Settings ***
Documentation       EC IUD Test - Blend (Configuration > Assets > Hydrocarbon_Objects > Blend, CO.0219).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_BLEND).
...                 Layered: this test -> blend_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Unique AUTOTEST_BLEND_<timestamp> code per run.

Resource            ../../../../pageobjects/Configuration/Assets/Hydrocarbon_Objects/blend_page.resource

Suite Setup         Set Up Blend Suite
Suite Teardown      Close EC

Test Tags           iud    blend


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test blend does not exist before inserting.
    [Tags]    clean-state
    Blend Row Should Not Exist    ${TEST_CODE}
    Capture Step    blend_tc01_clean

TC02 Insert New Blend
    [Documentation]    Insert a new blend; confirm in list + DB (OV_BLEND).
    [Tags]    insert
    Insert Blend Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Blend Row Should Exist    ${TEST_CODE}
    Blend Should Exist In DB    ${TEST_CODE}
    Capture Step    blend_tc02_inserted

TC03 Update Blend
    [Documentation]    Edit Name; confirm in list + DB ground truth.
    [Tags]    update
    Update Blend Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Blend Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Field Should Equal In View    OV_BLEND    ${TEST_CODE}    NAME    ${OBJ_NAME_UPD}
    Capture Step    blend_tc03_updated

TC04 Delete Blend
    [Documentation]    Delete via End Date = Start Date; confirm gone from list + DB.
    [Tags]    delete    cleanup
    Delete Blend    ${TEST_CODE}    ${END_DATE}
    Blend Row Should Not Exist    ${TEST_CODE}
    Blend Should Not Exist In DB    ${TEST_CODE}
    Capture Step    blend_tc04_deleted


*** Keywords ***
Set Up Blend Suite
    [Documentation]    Generate a unique test code/name, then open the Blend screen.
    Prepare IUD Object Data    AUTOTEST_BLEND_    Blend
    Open Blend Screen
