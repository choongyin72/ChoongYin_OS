*** Settings ***
Documentation       EC IUD Test - Chemical Tank (Configuration > Assets > Chemical Objects > Chemical Tank).
...                 OV-GM (manage-object, groupmodel): grid filtered by the navigator cascade
...                 (Production Unit -> Area -> Facility Class 1). Sibling of Node. DELETE = End Date =
...                 Start Date (true delete in OV_CHEM_TANK). NEVER touch existing data; a unique
...                 AUTOTEST_CT_<timestamp> code is generated per run.

Resource            ../../../../pageobjects/Configuration/Assets/Chemical_Objects/chemical_tank_page.resource

Suite Setup         Set Up Chemical Tank Suite
Suite Teardown      Close EC

Test Tags           iud    chemical_tank


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       2000-01-01
${END_DATE}         2000-01-01


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test tank does not exist before inserting.
    [Tags]    clean-state
    Chemical Tank Row Should Not Exist    ${TEST_CODE}
    Capture Step    chemical_tank_tc01_clean

TC02 Insert New Chemical Tank
    [Documentation]    Insert a new chemical tank under the navigator scope and confirm it lists.
    [Tags]    insert
    Insert Chemical Tank Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Chemical Tank Row Should Exist    ${TEST_CODE}
    Chemical Tank Should Exist In DB    ${TEST_CODE}
    Capture Step    chemical_tank_tc02_inserted

TC03 Update Chemical Tank Name
    [Documentation]    Edit the chemical tank name and confirm the list reflects the change.
    [Tags]    update
    Update Chemical Tank Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Chemical Tank Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    chemical_tank_tc03_updated

TC04 Delete Chemical Tank
    [Documentation]    Delete via End Date = Start Date and confirm the tank is gone.
    [Tags]    delete    cleanup
    Delete Chemical Tank    ${TEST_CODE}    ${END_DATE}
    Chemical Tank Row Should Not Exist    ${TEST_CODE}
    Chemical Tank Should Not Exist In DB    ${TEST_CODE}
    Capture Step    chemical_tank_tc04_deleted


*** Keywords ***
Set Up Chemical Tank Suite
    [Documentation]    Generate a unique test code/name, open the Chemical Tank screen, and fill
    ...    the OV-GM navigator cascade first-available + GO (capturing the top-parent PU).
    Prepare IUD Object Data    AUTOTEST_CT_    Chemical Tank
    ${pu}=    Open Chemical Tank Screen
    VAR    ${CT_PU}    ${pu}    scope=SUITE
