*** Settings ***
Documentation       EC IUD Test - Company Contact (Configuration > Assets > Commercial Objects > Company Contact).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_COMPANY_CONTACT).
...                 NEVER touch existing data. A unique AUTOTEST_CCON_<timestamp> code is generated
...                 per run. Section Start Date 2003-01-01: reference dropdowns are
...                 effective-date-filtered (object start date acts as a version).

Resource            ../../../../pageobjects/Configuration/Assets/Commercial_Objects/company_contact_page.resource

Suite Setup         Set Up Company Contact Suite
Suite Teardown      Close EC

Test Tags           iud    company-contact


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE_REFDD}
${END_DATE}         ${TEST_START_DATE_REFDD}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test company contact does not exist before inserting.
    [Tags]    clean-state
    Company Contact Row Should Not Exist    ${TEST_CODE}
    Capture Step    company_contact_tc01_clean

TC02 Insert New Company Contact
    [Documentation]    Insert a new company contact and confirm it appears in the list.
    [Tags]    insert
    Insert Company Contact Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Company Contact Row Should Exist    ${TEST_CODE}
    Company Contact Should Exist In DB    ${TEST_CODE}
    Capture Step    company_contact_tc02_inserted

TC03 Update Company Contact Name
    [Documentation]    Edit the company contact name and confirm the list reflects the change.
    [Tags]    update
    Update Company Contact Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Company Contact Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    company_contact_tc03_updated

TC04 Delete Company Contact
    [Documentation]    Delete via End Date = Start Date and confirm the company contact is gone.
    [Tags]    delete    cleanup
    Delete Company Contact    ${TEST_CODE}    ${END_DATE}
    Company Contact Row Should Not Exist    ${TEST_CODE}
    Company Contact Should Not Exist In DB    ${TEST_CODE}
    Capture Step    company_contact_tc04_deleted


*** Keywords ***
Set Up Company Contact Suite
    [Documentation]    Generate a unique test code/name, then open the Company Contact screen.
    Prepare IUD Object Data    AUTOTEST_CCON_    Company Contact
    Open Company Contact Screen
