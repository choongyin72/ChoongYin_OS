*** Settings ***
Documentation       EC IUD Test - Contract Area (Configuration > Assets > Contract Objects > Contract Area).
...                 OV-GM behaviour: navigator Business Unit + GO gates the grid; insert
...                 references "Business Unit Name" = ECP Norway so the row is visible
...                 under the ECP Norway filter. DELETE = End Date = Start Date (ov_contract_area).
...                 NEVER touch existing data: unique AUTOTEST_CA_<timestamp> code per run;
...                 the referenced Business Unit is READ-ONLY seed data.

Resource            ../../../../pageobjects/Configuration/Assets/Contract_Objects/contract_area_page.resource

Suite Setup         Set Up Contract Area Suite
Suite Teardown      Close EC

Test Tags           iud    contract_area


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE_REFDD}
${END_DATE}         ${TEST_START_DATE_REFDD}
${NAV_BU}           ECP Norway
${PARENT_VALUE}     ECP Norway


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test contract area does not exist before inserting.
    [Tags]    clean-state
    Contract Area Row Should Not Exist    ${TEST_CODE}
    Capture Step    contract_area_tc01_clean

TC02 Insert New Contract Area
    [Documentation]    Insert a new contract area and confirm it appears in the BU-filtered list.
    [Tags]    insert
    Insert Contract Area Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}    ${PARENT_VALUE}
    Contract Area Row Should Exist    ${TEST_CODE}
    Contract Area Should Exist In DB    ${TEST_CODE}
    Capture Step    contract_area_tc02_inserted

TC03 Update Contract Area Name
    [Documentation]    Edit the contract area name and confirm the list reflects the change.
    [Tags]    update
    Update Contract Area Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Contract Area Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    contract_area_tc03_updated

TC04 Delete Contract Area
    [Documentation]    Delete via End Date = Start Date and confirm the contract area is gone.
    [Tags]    delete    cleanup
    Delete Contract Area    ${TEST_CODE}    ${END_DATE}
    Contract Area Row Should Not Exist    ${TEST_CODE}
    Contract Area Should Not Exist In DB    ${TEST_CODE}
    Capture Step    contract_area_tc04_deleted


*** Keywords ***
Set Up Contract Area Suite
    [Documentation]    Generate a unique test code/name, then open the Contract Area screen
    ...    with the ${NAV_BU} navigator context.
    Prepare IUD Object Data    AUTOTEST_CA_    Contract Area
    Open Contract Area Screen    ${NAV_BU}
