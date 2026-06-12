*** Settings ***
Documentation       EC IUD Test - Licence (Configuration > Assets > Commercial Objects > Licence).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_LICENCE).
...                 NEVER touch existing data. A unique AUTOTEST_LIC_<timestamp> code is generated
...                 per run. Section Start Date 2003-01-01: reference dropdowns are
...                 effective-date-filtered (object start date acts as a version).

Resource            ../../../../pageobjects/Configuration/Assets/Commercial_Objects/licence_page.resource

Suite Setup         Set Up Licence Suite
Suite Teardown      Close EC

Test Tags           iud    licence


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE_REFDD}
${END_DATE}         ${TEST_START_DATE_REFDD}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test licence does not exist before inserting.
    [Tags]    clean-state
    Licence Row Should Not Exist    ${TEST_CODE}
    Capture Step    licence_tc01_clean

TC02 Insert New Licence
    [Documentation]    Insert a new licence and confirm it appears in the list.
    [Tags]    insert
    Insert Licence Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Licence Row Should Exist    ${TEST_CODE}
    Licence Should Exist In DB    ${TEST_CODE}
    Capture Step    licence_tc02_inserted

TC03 Update Licence Name
    [Documentation]    Edit the licence name and confirm the list reflects the change.
    [Tags]    update
    Update Licence Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Licence Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    licence_tc03_updated

TC04 Delete Licence
    [Documentation]    Delete via End Date = Start Date and confirm the licence is gone.
    [Tags]    delete    cleanup
    Delete Licence    ${TEST_CODE}    ${END_DATE}
    Licence Row Should Not Exist    ${TEST_CODE}
    Licence Should Not Exist In DB    ${TEST_CODE}
    Capture Step    licence_tc04_deleted


*** Keywords ***
Set Up Licence Suite
    [Documentation]    Generate a unique test code/name, then open the Licence screen.
    Prepare IUD Object Data    AUTOTEST_LIC_    Licence
    Open Licence Screen
