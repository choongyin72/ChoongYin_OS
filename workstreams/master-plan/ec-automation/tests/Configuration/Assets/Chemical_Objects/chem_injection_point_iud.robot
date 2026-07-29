*** Settings ***
Documentation       EC IUD Test - Chemical Injection Point (Configuration > Assets > Chemical Objects).
...                 OV-GM (manage-object, groupmodel): grid filtered by the navigator cascade
...                 (Production Unit -> Area -> Facility Class 1). Sibling of Node. DELETE = End Date =
...                 Start Date (true delete in OV_CHEM_INJ_POINT). NEVER touch existing data; a unique
...                 AUTOTEST_CIP_<timestamp> code is generated per run.

Resource            ../../../../pageobjects/Configuration/Assets/Chemical_Objects/chem_injection_point_page.resource

Suite Setup         Set Up Chemical Injection Point Suite
Suite Teardown      Close EC

Test Tags           iud    chem_injection_point


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       2000-01-01
${END_DATE}         2000-01-01


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test point does not exist before inserting.
    [Tags]    clean-state
    Chemical Injection Point Row Should Not Exist    ${TEST_CODE}
    Capture Step    chem_injection_point_tc01_clean

TC02 Insert New Chemical Injection Point
    [Documentation]    Insert a new point under the navigator scope and confirm it lists.
    [Tags]    insert
    Insert Chemical Injection Point Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Chemical Injection Point Row Should Exist    ${TEST_CODE}
    Chemical Injection Point Should Exist In DB    ${TEST_CODE}
    Capture Step    chem_injection_point_tc02_inserted

TC03 Update Chemical Injection Point Name
    [Documentation]    Edit the point name and confirm the list reflects the change.
    [Tags]    update
    Update Chemical Injection Point Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Chemical Injection Point Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    chem_injection_point_tc03_updated

TC04 Delete Chemical Injection Point
    [Documentation]    Delete via End Date = Start Date and confirm the point is gone.
    [Tags]    delete    cleanup
    Delete Chemical Injection Point    ${TEST_CODE}    ${END_DATE}
    Chemical Injection Point Row Should Not Exist    ${TEST_CODE}
    Chemical Injection Point Should Not Exist In DB    ${TEST_CODE}
    Capture Step    chem_injection_point_tc04_deleted


*** Keywords ***
Set Up Chemical Injection Point Suite
    [Documentation]    Generate a unique test code/name, open the screen, and fill the OV-GM
    ...    navigator cascade first-available + GO (capturing the top-parent PU).
    Prepare IUD Object Data    AUTOTEST_CIP_    Chem Inj Point
    ${pu}=    Open Chemical Injection Point Screen
    VAR    ${CIP_PU}    ${pu}    scope=SUITE
