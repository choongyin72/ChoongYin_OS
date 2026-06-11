*** Settings ***
Documentation       EC IUD Test - Vendor (Configuration > Assets > Commercial Objects > Vendor).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_VENDOR).
...                 NEVER touch existing data. A unique AUTOTEST_VEND_<timestamp> code is generated
...                 per run. Section Start Date 2003-01-01: reference dropdowns are
...                 effective-date-filtered (object start date acts as a version).

Resource            ../../../../pageobjects/Configuration/Assets/Commercial_Objects/vendor_page.resource

Suite Setup         Set Up Vendor Suite
Suite Teardown      Close EC

Test Tags           iud    vendor


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       2003-01-01
${END_DATE}         2003-01-01


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test vendor does not exist before inserting.
    [Tags]    clean-state
    Vendor Row Should Not Exist    ${TEST_CODE}
    Capture Step    vendor_tc01_clean

TC02 Insert New Vendor
    [Documentation]    Insert a new vendor and confirm it appears in the list.
    [Tags]    insert
    Insert Vendor Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Vendor Row Should Exist    ${TEST_CODE}
    Vendor Should Exist In DB    ${TEST_CODE}
    Capture Step    vendor_tc02_inserted

TC03 Update Vendor Name
    [Documentation]    Edit the vendor name and confirm the list reflects the change.
    [Tags]    update
    Update Vendor Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Vendor Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    vendor_tc03_updated

TC04 Delete Vendor
    [Documentation]    Delete via End Date = Start Date and confirm the vendor is gone.
    [Tags]    delete    cleanup
    Delete Vendor    ${TEST_CODE}    ${END_DATE}
    Vendor Row Should Not Exist    ${TEST_CODE}
    Vendor Should Not Exist In DB    ${TEST_CODE}
    Capture Step    vendor_tc04_deleted


*** Keywords ***
Set Up Vendor Suite
    [Documentation]    Generate a unique test code/name, then open the Vendor screen.
    ${code}    Generate Unique Code    AUTOTEST_VEND_
    VAR    ${TEST_CODE}    ${code}    scope=SUITE
    VAR    ${OBJ_NAME}    Vendor ${code}    scope=SUITE
    VAR    ${OBJ_NAME_UPD}    Vendor ${code} UPD    scope=SUITE
    Open Vendor Screen
