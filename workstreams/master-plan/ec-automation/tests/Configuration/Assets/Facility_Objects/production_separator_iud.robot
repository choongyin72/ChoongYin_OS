*** Settings ***
Documentation       EC IUD Test - Production Separator (Configuration > Assets > Facility_Objects).
...                 OV-GM (manage-object, groupmodel): grid filtered by the navigator cascade.
...                 DELETE = End Date = Start Date (true delete in OV_PRODSEPARATOR). NEVER touch existing data;
...                 a unique AUTOTEST_PSEP_<timestamp> code is generated per run.

Resource            ../../../../pageobjects/Configuration/Assets/Facility_Objects/production_separator_page.resource

Suite Setup         Set Up Production Separator Suite
Suite Teardown      Close EC

Test Tags           iud    production_separator


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
    Production Separator Row Should Not Exist    ${TEST_CODE}
    Capture Step    production_separator_tc01_clean

TC02 Insert New Production Separator
    [Documentation]    Insert under the navigator scope and confirm it lists.
    [Tags]    insert
    Insert Production Separator Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Production Separator Row Should Exist    ${TEST_CODE}
    Production Separator Should Exist In DB    ${TEST_CODE}
    Capture Step    production_separator_tc02_inserted

TC03 Update Production Separator Name
    [Documentation]    Edit the name and confirm the list reflects the change.
    [Tags]    update
    Update Production Separator Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Production Separator Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    production_separator_tc03_updated

TC04 Delete Production Separator
    [Documentation]    Delete via End Date = Start Date and confirm it is gone.
    [Tags]    delete    cleanup
    Delete Production Separator    ${TEST_CODE}    ${END_DATE}
    Production Separator Row Should Not Exist    ${TEST_CODE}
    Production Separator Should Not Exist In DB    ${TEST_CODE}
    Capture Step    production_separator_tc04_deleted


*** Keywords ***
Set Up Production Separator Suite
    [Documentation]    Generate a unique test code/name, open the screen, fill the navigator cascade.
    Prepare IUD Object Data    AUTOTEST_PSEP_    Production Separator
    ${pu}=    Open Production Separator Screen
    VAR    ${GM_PU}    ${pu}    scope=SUITE
