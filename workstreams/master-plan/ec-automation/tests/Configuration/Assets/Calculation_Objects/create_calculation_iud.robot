*** Settings ***
Documentation       EC IUD Test - Create Calculation (Configuration > Assets > Calculation_Objects).
...                 Context-gated TV-style dual grid: header calc row IUD ONLY (no equations -
...                 calc-lab scope). INSERT = blank inline row + Period/Type dds; UPDATE = VERSIONS
...                 grid Calculation Name (authoritative); DELETE = the purpose-built DELETE
...                 CALCULATION button. NEVER touch the existing EC_GRS_TO_NET_* calcs; unique
...                 AUTOTEST_CC_<timestamp> code per run. Start Date 2020-01-01.

Resource            ../../../../pageobjects/Configuration/Assets/Calculation_Objects/create_calculation_page.resource

Suite Setup         Set Up Create Calculation Suite
Suite Teardown      Close EC

Test Tags           iud    create-calculation


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       2020-01-01


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test calc does not exist before inserting.
    [Tags]    clean-state
    Create Calculation Row Should Not Exist    ${TEST_CODE}
    Capture Step    create_calculation_tc01_clean

TC02 Insert New Calculation Header
    [Documentation]    Insert the calc header row (Code/Name/Start Date + Period/Type dds) and confirm it lists.
    [Tags]    insert
    Insert Create Calculation Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Create Calculation Row Should Exist    ${TEST_CODE}
    Create Calculation Should Exist In DB    ${TEST_CODE}
    Capture Step    create_calculation_tc02_inserted

TC03 Update Calculation Name
    [Documentation]    Edit the VERSIONS grid's Calculation Name and confirm the DB reflects it.
    [Tags]    update
    Update Create Calculation Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Field Should Equal In View    OV_CALCULATION    ${TEST_CODE}    NAME    ${OBJ_NAME_UPD}
    Capture Step    create_calculation_tc03_updated

TC04 Delete Calculation
    [Documentation]    Delete via the DELETE CALCULATION button and confirm it is gone (grid + DB).
    [Tags]    delete    cleanup
    Delete Create Calculation    ${TEST_CODE}
    Create Calculation Row Should Not Exist    ${TEST_CODE}
    Create Calculation Should Not Exist In DB    ${TEST_CODE}
    Capture Step    create_calculation_tc04_deleted


*** Keywords ***
Set Up Create Calculation Suite
    [Documentation]    Generate a unique test code/name, open the screen, pick the first context + GO.
    Prepare IUD Object Data    AUTOTEST_CC_    Create Calculation
    Open Create Calculation Screen
