*** Settings ***
Documentation       EC IUD Test - Product Description (Configuration > Assets > Financial Objects > Product Description).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_PRODUCT_NODE_ITEM).
...                 NEVER touch existing data. A unique AUTOTEST_PD_<timestamp> code is generated
...                 per run (EC keeps deleted codes in the base table, so codes are never reused).

Resource            ../../../../pageobjects/Configuration/Assets/Financial_Objects/product_description_page.resource

Suite Setup         Set Up Product Description Suite
Suite Teardown      Close EC

Test Tags           iud    product-description


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test product description does not exist before inserting.
    [Tags]    clean-state
    Product Description Row Should Not Exist    ${TEST_CODE}
    Capture Step    product_description_tc01_clean

TC02 Insert New Product Description
    [Documentation]    Insert a new product description and confirm it appears in the list.
    [Tags]    insert
    Insert Product Description Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Product Description Row Should Exist    ${TEST_CODE}
    Product Description Should Exist In DB    ${TEST_CODE}
    Capture Step    product_description_tc02_inserted

TC03 Update Product Description Name
    [Documentation]    Edit the product description name and confirm the list reflects the change.
    [Tags]    update
    Update Product Description Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Product Description Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    product_description_tc03_updated

TC04 Delete Product Description
    [Documentation]    Delete via End Date = Start Date and confirm the product description is gone.
    [Tags]    delete    cleanup
    Delete Product Description    ${TEST_CODE}    ${END_DATE}
    Product Description Row Should Not Exist    ${TEST_CODE}
    Product Description Should Not Exist In DB    ${TEST_CODE}
    Capture Step    product_description_tc04_deleted


*** Keywords ***
Set Up Product Description Suite
    [Documentation]    Generate a unique test code/name, then open the Product Description screen.
    Prepare IUD Object Data    AUTOTEST_PD_    Product Description
    Open Product Description Screen
