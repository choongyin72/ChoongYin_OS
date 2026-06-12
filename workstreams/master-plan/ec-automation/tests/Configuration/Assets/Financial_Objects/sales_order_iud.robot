*** Settings ***
Documentation       EC IUD Test - Sales Order (Configuration > Assets > Financial Objects > Sales Order).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_PRODUCT_SALES_ORDER).
...                 NEVER touch existing data. A unique AUTOTEST_SO_<timestamp> code is generated
...                 per run (EC keeps deleted codes in the base table, so codes are never reused).

Resource            ../../../../pageobjects/Configuration/Assets/Financial_Objects/sales_order_page.resource

Suite Setup         Set Up Sales Order Suite
Suite Teardown      Close EC

Test Tags           iud    sales-order


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test sales order does not exist before inserting.
    [Tags]    clean-state
    Sales Order Row Should Not Exist    ${TEST_CODE}
    Capture Step    sales_order_tc01_clean

TC02 Insert New Sales Order
    [Documentation]    Insert a new sales order and confirm it appears in the list.
    [Tags]    insert
    Insert Sales Order Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Sales Order Row Should Exist    ${TEST_CODE}
    Sales Order Should Exist In DB    ${TEST_CODE}
    Capture Step    sales_order_tc02_inserted

TC03 Update Sales Order Name
    [Documentation]    Edit the sales order name and confirm the list reflects the change.
    [Tags]    update
    Update Sales Order Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Sales Order Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    sales_order_tc03_updated

TC04 Delete Sales Order
    [Documentation]    Delete via End Date = Start Date and confirm the sales order is gone.
    [Tags]    delete    cleanup
    Delete Sales Order    ${TEST_CODE}    ${END_DATE}
    Sales Order Row Should Not Exist    ${TEST_CODE}
    Sales Order Should Not Exist In DB    ${TEST_CODE}
    Capture Step    sales_order_tc04_deleted


*** Keywords ***
Set Up Sales Order Suite
    [Documentation]    Generate a unique test code/name, then open the Sales Order screen.
    Prepare IUD Object Data    AUTOTEST_SO_    Sales Order
    Open Sales Order Screen
