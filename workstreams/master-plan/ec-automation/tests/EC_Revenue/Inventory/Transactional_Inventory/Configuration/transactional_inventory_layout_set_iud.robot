*** Settings ***
Documentation       EC IUD Test - Transactional Inventory Layout Set (EC_Revenue > Inventory > Transactional_Inventory > Configuration > Transactional Inventory Layout Set, IN.0033).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_TRANS_INV_TMPL_SET).
...                 Layered: this test -> transactional_inventory_layout_set_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Unique AUTOTEST_TILS_<timestamp> code per run.

Resource            ../../../../../pageobjects/EC_Revenue/Inventory/Transactional_Inventory/Configuration/transactional_inventory_layout_set_page.resource

Suite Setup         Set Up Transactional Inventory Layout Set Suite
Suite Teardown      Close EC

Test Tags           iud    transactional_inventory_layout_set


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test transactional_inventory_layout_set does not exist before inserting.
    [Tags]    clean-state
    Transactional Inventory Layout Set Row Should Not Exist    ${TEST_CODE}
    Capture Step    transactional_inventory_layout_set_tc01_clean

TC02 Insert New Transactional Inventory Layout Set
    [Documentation]    Insert a new transactional_inventory_layout_set; confirm in list + DB (OV_TRANS_INV_TMPL_SET).
    [Tags]    insert
    Insert Transactional Inventory Layout Set Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Transactional Inventory Layout Set Row Should Exist    ${TEST_CODE}
    Transactional Inventory Layout Set Should Exist In DB    ${TEST_CODE}
    Capture Step    transactional_inventory_layout_set_tc02_inserted

TC03 Update Transactional Inventory Layout Set
    [Documentation]    Edit Name; confirm in list + DB ground truth.
    [Tags]    update
    Update Transactional Inventory Layout Set Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Transactional Inventory Layout Set Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Field Should Equal In View    OV_TRANS_INV_TMPL_SET    ${TEST_CODE}    NAME    ${OBJ_NAME_UPD}
    Capture Step    transactional_inventory_layout_set_tc03_updated

TC04 Delete Transactional Inventory Layout Set
    [Documentation]    Delete via End Date = Start Date; confirm gone from list + DB.
    [Tags]    delete    cleanup
    Delete Transactional Inventory Layout Set    ${TEST_CODE}    ${END_DATE}
    Transactional Inventory Layout Set Row Should Not Exist    ${TEST_CODE}
    Transactional Inventory Layout Set Should Not Exist In DB    ${TEST_CODE}
    Capture Step    transactional_inventory_layout_set_tc04_deleted


*** Keywords ***
Set Up Transactional Inventory Layout Set Suite
    [Documentation]    Generate a unique test code/name, then open the Transactional Inventory Layout Set screen.
    Prepare IUD Object Data    AUTOTEST_TILS_    Transactional Inventory Layout Set
    Open Transactional Inventory Layout Set Screen
