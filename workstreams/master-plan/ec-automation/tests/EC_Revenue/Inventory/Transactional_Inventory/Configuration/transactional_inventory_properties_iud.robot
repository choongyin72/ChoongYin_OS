*** Settings ***
Documentation       EC IUD Test - Transactional Inventory Properties (EC_Revenue > Inventory > Transactional_Inventory > Configuration > Transactional Inventory Properties, IN.0023).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_TRANS_INVENTORY).
...                 Layered: this test -> transactional_inventory_properties_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Unique AUTOTEST_TIP_<timestamp> code per run.

Resource            ../../../../../pageobjects/EC_Revenue/Inventory/Transactional_Inventory/Configuration/transactional_inventory_properties_page.resource

Suite Setup         Set Up Transactional Inventory Properties Suite
Suite Teardown      Close EC

Test Tags           iud    transactional_inventory_properties


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test transactional_inventory_properties does not exist before inserting.
    [Tags]    clean-state
    Transactional Inventory Properties Row Should Not Exist    ${TEST_CODE}
    Capture Step    transactional_inventory_properties_tc01_clean

TC02 Insert New Transactional Inventory Properties
    [Documentation]    Insert a new transactional_inventory_properties; confirm in list + DB (OV_TRANS_INVENTORY).
    [Tags]    insert
    Insert Transactional Inventory Properties Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Transactional Inventory Properties Row Should Exist    ${TEST_CODE}
    Transactional Inventory Properties Should Exist In DB    ${TEST_CODE}
    Capture Step    transactional_inventory_properties_tc02_inserted

TC03 Update Transactional Inventory Properties
    [Documentation]    Edit Name; confirm in list + DB ground truth.
    [Tags]    update
    Update Transactional Inventory Properties Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Transactional Inventory Properties Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Field Should Equal In View    OV_TRANS_INVENTORY    ${TEST_CODE}    NAME    ${OBJ_NAME_UPD}
    Capture Step    transactional_inventory_properties_tc03_updated

TC04 Delete Transactional Inventory Properties
    [Documentation]    Delete via End Date = Start Date; confirm gone from list + DB.
    [Tags]    delete    cleanup
    Delete Transactional Inventory Properties    ${TEST_CODE}    ${END_DATE}
    Transactional Inventory Properties Row Should Not Exist    ${TEST_CODE}
    Transactional Inventory Properties Should Not Exist In DB    ${TEST_CODE}
    Capture Step    transactional_inventory_properties_tc04_deleted


*** Keywords ***
Set Up Transactional Inventory Properties Suite
    [Documentation]    Generate a unique test code/name, then open the Transactional Inventory Properties screen.
    Prepare IUD Object Data    AUTOTEST_TIP_    Transactional Inventory Properties
    Open Transactional Inventory Properties Screen
