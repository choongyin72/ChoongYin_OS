*** Settings ***
Documentation       EC IUD Test - Contract Inventory (Configuration > Assets > Contract_Objects).
...                 OV-GM (manage-object, groupmodel): grid filtered by the navigator cascade (PROVEN
...                 explicit values, not first-available).
...                 DELETE = End Date = Start Date (true delete in OV_CONTRACT_INVENTORY). NEVER touch existing data;
...                 a unique AUTOTEST_CI_<timestamp> code is generated per run.

Resource            ../../../../pageobjects/Configuration/Assets/Contract_Objects/contract_inventory_page.resource

Suite Setup         Set Up Contract Inventory Suite
Suite Teardown      Close EC

Test Tags           iud    contract_inventory


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       2000-01-01
${END_DATE}         2000-01-01


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test object does not exist before inserting.
    [Tags]    clean-state
    Contract Inventory Row Should Not Exist    ${TEST_CODE}
    Capture Step    contract_inventory_tc01_clean

TC02 Insert New Contract Inventory
    [Documentation]    Insert under the navigator scope and confirm it lists.
    [Tags]    insert
    Insert Contract Inventory Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Contract Inventory Row Should Exist    ${TEST_CODE}
    Contract Inventory Should Exist In DB    ${TEST_CODE}
    Capture Step    contract_inventory_tc02_inserted

TC03 Update Contract Inventory Name
    [Documentation]    Edit the name and confirm the list reflects the change.
    [Tags]    update
    Update Contract Inventory Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Contract Inventory Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    contract_inventory_tc03_updated

TC04 Delete Contract Inventory
    [Documentation]    Delete via End Date = Start Date and confirm it is gone.
    [Tags]    delete    cleanup
    Delete Contract Inventory    ${TEST_CODE}    ${END_DATE}
    Contract Inventory Row Should Not Exist    ${TEST_CODE}
    Contract Inventory Should Not Exist In DB    ${TEST_CODE}
    Capture Step    contract_inventory_tc04_deleted


*** Keywords ***
Set Up Contract Inventory Suite
    [Documentation]    Generate a unique test code/name, open the screen, fill the navigator cascade
    ...    with PROVEN explicit values (not first-available).
    Prepare IUD Object Data    AUTOTEST_CI_    Contract Inventory
    ${pu}=    Open Contract Inventory Screen
    VAR    ${GM_PU}    ${pu}    scope=SUITE
