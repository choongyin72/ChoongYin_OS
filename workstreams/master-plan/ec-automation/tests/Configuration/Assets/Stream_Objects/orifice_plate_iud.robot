*** Settings ***
Documentation       EC IUD Test - Orifice Plate (Configuration > Assets > Stream_Objects > Orifice Plate, CO.0089).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_ORIFICE_PLATE).
...                 Layered: this test -> orifice_plate_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Unique AUTOTEST_OP_<timestamp> code per run.

Resource            ../../../../pageobjects/Configuration/Assets/Stream_Objects/orifice_plate_page.resource

Suite Setup         Set Up Orifice Plate Suite
Suite Teardown      Close EC

Test Tags           iud    orifice_plate


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test orifice_plate does not exist before inserting.
    [Tags]    clean-state
    Orifice Plate Row Should Not Exist    ${TEST_CODE}
    Capture Step    orifice_plate_tc01_clean

TC02 Insert New Orifice Plate
    [Documentation]    Insert a new orifice_plate; confirm in list + DB (OV_ORIFICE_PLATE).
    [Tags]    insert
    Insert Orifice Plate Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Orifice Plate Row Should Exist    ${TEST_CODE}
    Orifice Plate Should Exist In DB    ${TEST_CODE}
    Capture Step    orifice_plate_tc02_inserted

TC03 Update Orifice Plate
    [Documentation]    Edit Name; confirm in list + DB ground truth.
    [Tags]    update
    Update Orifice Plate Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Orifice Plate Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Field Should Equal In View    OV_ORIFICE_PLATE    ${TEST_CODE}    NAME    ${OBJ_NAME_UPD}
    Capture Step    orifice_plate_tc03_updated

TC04 Delete Orifice Plate
    [Documentation]    Delete via End Date = Start Date; confirm gone from list + DB.
    [Tags]    delete    cleanup
    Delete Orifice Plate    ${TEST_CODE}    ${END_DATE}
    Orifice Plate Row Should Not Exist    ${TEST_CODE}
    Orifice Plate Should Not Exist In DB    ${TEST_CODE}
    Capture Step    orifice_plate_tc04_deleted


*** Keywords ***
Set Up Orifice Plate Suite
    [Documentation]    Generate a unique test code/name, then open the Orifice Plate screen.
    Prepare IUD Object Data    AUTOTEST_OP_    Orifice Plate
    Open Orifice Plate Screen
