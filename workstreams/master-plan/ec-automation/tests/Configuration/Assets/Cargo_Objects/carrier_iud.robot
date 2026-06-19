*** Settings ***
Documentation       EC IUD Test - Carrier (Configuration > Assets > Cargo Objects > Carrier).
...                 Manage-Object (OV) screen, Bank-family grid (not gated). Insert requires the
...                 mandatory "Unit" reference dropdown (first option used). DELETE = End Date =
...                 Start Date (ov_carrier). NEVER touch existing data: a unique
...                 AUTOTEST_CARR_<timestamp> code per run (EC keeps deleted codes, so never reused);
...                 the referenced Unit is READ-ONLY seed data.

Resource            ../../../../pageobjects/Configuration/Assets/Cargo_Objects/carrier_page.resource

Suite Setup         Set Up Carrier Suite
Suite Teardown      Close EC

Test Tags           iud    carrier


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE_REFDD}
${END_DATE}         ${TEST_START_DATE_REFDD}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test carrier does not exist before inserting.
    [Tags]    clean-state
    Carrier Row Should Not Exist    ${TEST_CODE}
    Capture Step    carrier_tc01_clean

TC02 Insert New Carrier
    [Documentation]    Insert a new carrier and confirm it appears in the list and persisted in the DB.
    [Tags]    insert
    Insert Carrier Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Carrier Row Should Exist    ${TEST_CODE}
    Carrier Should Exist In DB    ${TEST_CODE}
    Capture Step    carrier_tc02_inserted

TC03 Update Carrier Name
    [Documentation]    Edit the carrier name and confirm the list reflects the change.
    [Tags]    update
    Update Carrier Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Carrier Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    carrier_tc03_updated

TC04 Delete Carrier
    [Documentation]    Delete via End Date = Start Date and confirm the carrier is gone (UI + DB).
    [Tags]    delete    cleanup
    Delete Carrier    ${TEST_CODE}    ${END_DATE}
    Carrier Row Should Not Exist    ${TEST_CODE}
    Carrier Should Not Exist In DB    ${TEST_CODE}
    Capture Step    carrier_tc04_deleted


*** Keywords ***
Set Up Carrier Suite
    [Documentation]    Generate a unique test code/name, then open the Carrier screen.
    Prepare IUD Object Data    AUTOTEST_CARR_    Carrier
    Open Carrier Screen
