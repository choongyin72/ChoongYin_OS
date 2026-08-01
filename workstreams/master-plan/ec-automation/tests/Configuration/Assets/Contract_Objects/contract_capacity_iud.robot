*** Settings ***
Documentation       EC IUD Test - Contract Capacity (Configuration > Assets > Contract_Objects).
...                 OV-GM (manage-object, groupmodel): grid filtered by the navigator cascade (PROVEN
...                 explicit values, not first-available).
...                 DELETE = End Date = Start Date (true delete in OV_CONTRACT_CAPACITY). NEVER touch existing data;
...                 a unique AUTOTEST_CC<timestamp> code is generated per run.

Resource            ../../../../pageobjects/Configuration/Assets/Contract_Objects/contract_capacity_page.resource

Suite Setup         Set Up Contract Capacity Suite
Suite Teardown      Close EC

Test Tags           iud    contract_capacity


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       2020-01-01
${END_DATE}         2000-01-01


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test object does not exist before inserting.
    [Tags]    clean-state
    Contract Capacity Row Should Not Exist    ${TEST_CODE}
    Capture Step    contract_capacity_tc01_clean

TC02 Insert New Contract Capacity
    [Documentation]    Insert under the navigator scope and confirm it lists.
    [Tags]    insert
    Insert Contract Capacity Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Contract Capacity Row Should Exist    ${TEST_CODE}
    Contract Capacity Should Exist In DB    ${TEST_CODE}
    Capture Step    contract_capacity_tc02_inserted

TC03 Update Contract Capacity Name
    [Documentation]    Edit the name and confirm the list reflects the change.
    [Tags]    update
    Update Contract Capacity Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Contract Capacity Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    contract_capacity_tc03_updated

TC04 Delete Contract Capacity
    [Documentation]    Delete via End Date = Start Date and confirm it is gone.
    [Tags]    delete    cleanup
    Delete Contract Capacity    ${TEST_CODE}    ${END_DATE}
    Contract Capacity Row Should Not Exist    ${TEST_CODE}
    Contract Capacity Should Not Exist In DB    ${TEST_CODE}
    Capture Step    contract_capacity_tc04_deleted


*** Keywords ***
Set Up Contract Capacity Suite
    [Documentation]    Generate a unique test code/name, open the screen, fill the navigator cascade
    ...    with PROVEN explicit values (not first-available).
    Prepare IUD Object Data    AUTOTEST_CC    Contract Capacity
    ${pu}=    Open Contract Capacity Screen
    VAR    ${GM_PU}    ${pu}    scope=SUITE
