*** Settings ***
Documentation       EC IUD Test - Revenue Order (Configuration > Assets > Financial Objects > Revenue Order).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_FIN_REVENUE_ORDER).
...                 NEVER touch existing data. A unique AUTOTEST_RO_<timestamp> code is generated
...                 per run (EC keeps deleted codes in the base table, so codes are never reused).

Resource            ../../../../pageobjects/Configuration/Assets/Financial_Objects/revenue_order_page.resource

Suite Setup         Set Up Revenue Order Suite
Suite Teardown      Close EC

Test Tags           iud    revenue-order


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       2000-01-01
${END_DATE}         2000-01-01


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test revenue order does not exist before inserting.
    [Tags]    clean-state
    Revenue Order Row Should Not Exist    ${TEST_CODE}
    Capture Step    revenue_order_tc01_clean

TC02 Insert New Revenue Order
    [Documentation]    Insert a new revenue order and confirm it appears in the list.
    [Tags]    insert
    Insert Revenue Order Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Revenue Order Row Should Exist    ${TEST_CODE}
    Revenue Order Should Exist In DB    ${TEST_CODE}
    Capture Step    revenue_order_tc02_inserted

TC03 Update Revenue Order Name
    [Documentation]    Edit the revenue order name and confirm the list reflects the change.
    [Tags]    update
    Update Revenue Order Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Revenue Order Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    revenue_order_tc03_updated

TC04 Delete Revenue Order
    [Documentation]    Delete via End Date = Start Date and confirm the revenue order is gone.
    [Tags]    delete    cleanup
    Delete Revenue Order    ${TEST_CODE}    ${END_DATE}
    Revenue Order Row Should Not Exist    ${TEST_CODE}
    Revenue Order Should Not Exist In DB    ${TEST_CODE}
    Capture Step    revenue_order_tc04_deleted


*** Keywords ***
Set Up Revenue Order Suite
    [Documentation]    Generate a unique test code/name, then open the Revenue Order screen.
    ${code}    Generate Unique Code    AUTOTEST_RO_
    VAR    ${TEST_CODE}    ${code}    scope=SUITE
    VAR    ${OBJ_NAME}    Revenue Order ${code}    scope=SUITE
    VAR    ${OBJ_NAME_UPD}    Revenue Order ${code} UPD    scope=SUITE
    Open Revenue Order Screen
