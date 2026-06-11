*** Settings ***
Documentation       EC IUD Test - Customer (Configuration > Assets > Commercial Objects > Customer).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_CUSTOMER).
...                 NEVER touch existing data. A unique AUTOTEST_CUST_<timestamp> code is generated
...                 per run. Section Start Date 2003-01-01: reference dropdowns are
...                 effective-date-filtered (object start date acts as a version).

Resource            ../../../../pageobjects/Configuration/Assets/Commercial_Objects/customer_page.resource

Suite Setup         Set Up Customer Suite
Suite Teardown      Close EC

Test Tags           iud    customer


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       2003-01-01
${END_DATE}         2003-01-01


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test customer does not exist before inserting.
    [Tags]    clean-state
    Customer Row Should Not Exist    ${TEST_CODE}
    Capture Step    customer_tc01_clean

TC02 Insert New Customer
    [Documentation]    Insert a new customer and confirm it appears in the list.
    [Tags]    insert
    Insert Customer Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Customer Row Should Exist    ${TEST_CODE}
    Customer Should Exist In DB    ${TEST_CODE}
    Capture Step    customer_tc02_inserted

TC03 Update Customer Name
    [Documentation]    Edit the customer name and confirm the list reflects the change.
    [Tags]    update
    Update Customer Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Customer Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    customer_tc03_updated

TC04 Delete Customer
    [Documentation]    Delete via End Date = Start Date and confirm the customer is gone.
    [Tags]    delete    cleanup
    Delete Customer    ${TEST_CODE}    ${END_DATE}
    Customer Row Should Not Exist    ${TEST_CODE}
    Customer Should Not Exist In DB    ${TEST_CODE}
    Capture Step    customer_tc04_deleted


*** Keywords ***
Set Up Customer Suite
    [Documentation]    Generate a unique test code/name, then open the Customer screen.
    ${code}    Generate Unique Code    AUTOTEST_CUST_
    VAR    ${TEST_CODE}    ${code}    scope=SUITE
    VAR    ${OBJ_NAME}    Customer ${code}    scope=SUITE
    VAR    ${OBJ_NAME_UPD}    Customer ${code} UPD    scope=SUITE
    Open Customer Screen
