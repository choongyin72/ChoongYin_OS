*** Settings ***
Documentation       EC IUD Test - Company (Configuration > Assets > Commercial Objects > Company).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_COMPANY).
...                 NEVER touch existing data. A unique AUTOTEST_COMP_<timestamp> code is generated
...                 per run. Section Start Date 2003-01-01: reference dropdowns are
...                 effective-date-filtered (object start date acts as a version).

Resource            ../../../../pageobjects/Configuration/Assets/Commercial_Objects/company_page.resource

Suite Setup         Set Up Company Suite
Suite Teardown      Close EC

Test Tags           iud    company


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       2003-01-01
${END_DATE}         2003-01-01


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test company does not exist before inserting.
    [Tags]    clean-state
    Company Row Should Not Exist    ${TEST_CODE}
    Capture Step    company_tc01_clean

TC02 Insert New Company
    [Documentation]    Insert a new company and confirm it appears in the list.
    [Tags]    insert
    Insert Company Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Company Row Should Exist    ${TEST_CODE}
    Company Should Exist In DB    ${TEST_CODE}
    Capture Step    company_tc02_inserted

TC03 Update Company Name
    [Documentation]    Edit the company name and confirm the list reflects the change.
    [Tags]    update
    Update Company Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Company Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    company_tc03_updated

TC04 Delete Company
    [Documentation]    Delete via End Date = Start Date and confirm the company is gone.
    [Tags]    delete    cleanup
    Delete Company    ${TEST_CODE}    ${END_DATE}
    Company Row Should Not Exist    ${TEST_CODE}
    Company Should Not Exist In DB    ${TEST_CODE}
    Capture Step    company_tc04_deleted


*** Keywords ***
Set Up Company Suite
    [Documentation]    Generate a unique test code/name, then open the Company screen.
    ${code}    Generate Unique Code    AUTOTEST_COMP_
    VAR    ${TEST_CODE}    ${code}    scope=SUITE
    VAR    ${OBJ_NAME}    Company ${code}    scope=SUITE
    VAR    ${OBJ_NAME_UPD}    Company ${code} UPD    scope=SUITE
    Open Company Screen
