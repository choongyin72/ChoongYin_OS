*** Settings ***
Documentation       EC IUD Test - Inventory Area (Configuration > Assets > Inventory_Objects > Inventory Area, CD.0115).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_INVENTORY_AREA).
...                 Layered: this test -> inventory_area_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Unique AUTOTEST_INVA_<timestamp> code per run.

Resource            ../../../../pageobjects/Configuration/Assets/Inventory_Objects/inventory_area_page.resource

Suite Setup         Set Up Inventory Area Suite
Suite Teardown      Close EC

Test Tags           iud    inventory_area


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test inventory_area does not exist before inserting.
    [Tags]    clean-state
    Inventory Area Row Should Not Exist    ${TEST_CODE}
    Capture Step    inventory_area_tc01_clean

TC02 Insert New Inventory Area
    [Documentation]    Insert a new inventory_area; confirm in list + DB (OV_INVENTORY_AREA).
    [Tags]    insert
    Insert Inventory Area Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Inventory Area Row Should Exist    ${TEST_CODE}
    Inventory Area Should Exist In DB    ${TEST_CODE}
    Capture Step    inventory_area_tc02_inserted

TC03 Update Inventory Area
    [Documentation]    Edit Name; confirm in list + DB ground truth.
    [Tags]    update
    Update Inventory Area Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Inventory Area Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Field Should Equal In View    OV_INVENTORY_AREA    ${TEST_CODE}    NAME    ${OBJ_NAME_UPD}
    Capture Step    inventory_area_tc03_updated

TC04 Delete Inventory Area
    [Documentation]    Delete via End Date = Start Date; confirm gone from list + DB.
    [Tags]    delete    cleanup
    Delete Inventory Area    ${TEST_CODE}    ${END_DATE}
    Inventory Area Row Should Not Exist    ${TEST_CODE}
    Inventory Area Should Not Exist In DB    ${TEST_CODE}
    Capture Step    inventory_area_tc04_deleted


*** Keywords ***
Set Up Inventory Area Suite
    [Documentation]    Generate a unique test code/name, then open the Inventory Area screen.
    Prepare IUD Object Data    AUTOTEST_INVA_    Inventory Area
    Open Inventory Area Screen
