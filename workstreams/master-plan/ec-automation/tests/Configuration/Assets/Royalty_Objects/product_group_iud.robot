*** Settings ***
Documentation       EC IUD Test - Product Group (Configuration > Assets > Royalty Objects > Product Group).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in ov_product_group).
...                 Layered: this test -> product_group_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. A unique AUTOTEST_PG_<timestamp> code is generated
...                 per run (EC keeps deleted codes in the base table, so codes are never reused).

Resource            ../../../../pageobjects/Configuration/Assets/Royalty_Objects/product_group_page.resource

Suite Setup         Set Up Product Group Suite
Suite Teardown      Close EC

Test Tags           iud    product_group


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}        ${EMPTY}
${OBJ_NAME_UPD}    ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test product group does not exist before inserting.
    [Tags]    clean-state
    Product Group Row Should Not Exist    ${TEST_CODE}
    Capture Step    product_group_tc01_clean

TC02 Insert New Product Group
    [Documentation]    Insert a new product group and confirm it appears in the list.
    [Tags]    insert
    Insert Product Group Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Product Group Row Should Exist    ${TEST_CODE}
    Product Group Should Exist In DB    ${TEST_CODE}
    Capture Step    product_group_tc02_inserted

TC03 Update Product Group Name
    [Documentation]    Edit the product group name and confirm the list reflects the change.
    [Tags]    update
    Update Product Group Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Product Group Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    product_group_tc03_updated

TC04 Delete Product Group
    [Documentation]    Delete via End Date = Start Date and confirm the product group is gone.
    [Tags]    delete    cleanup
    Delete Product Group    ${TEST_CODE}    ${END_DATE}
    Product Group Row Should Not Exist    ${TEST_CODE}
    Product Group Should Not Exist In DB    ${TEST_CODE}
    Capture Step    product_group_tc04_deleted


*** Keywords ***
Set Up Product Group Suite
    [Documentation]    Generate a unique test code/name, then open the Product Group screen.
    Prepare IUD Object Data    AUTOTEST_PG_    Product Group
    Open Product Group Screen
