*** Settings ***
Documentation       EC IUD Test - Well Hookup (Configuration > Assets > Facility_Objects).
...                 OV-GM (manage-object, groupmodel): grid filtered by the navigator cascade.
...                 DELETE = End Date = Start Date (true delete in OV_WELL_HOOKUP). NEVER touch existing data;
...                 a unique AUTOTEST_WH_<timestamp> code is generated per run.

Resource            ../../../../pageobjects/Configuration/Assets/Facility_Objects/well_hookup_page.resource

Suite Setup         Set Up Well Hookup Suite
Suite Teardown      Close EC

Test Tags           iud    well_hookup


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
    Well Hookup Row Should Not Exist    ${TEST_CODE}
    Capture Step    well_hookup_tc01_clean

TC02 Insert New Well Hookup
    [Documentation]    Insert under the navigator scope and confirm it lists.
    [Tags]    insert
    Insert Well Hookup Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Well Hookup Row Should Exist    ${TEST_CODE}
    Well Hookup Should Exist In DB    ${TEST_CODE}
    Capture Step    well_hookup_tc02_inserted

TC03 Update Well Hookup Name
    [Documentation]    Edit the name and confirm the list reflects the change.
    [Tags]    update
    Update Well Hookup Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Well Hookup Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    well_hookup_tc03_updated

TC04 Delete Well Hookup
    [Documentation]    Delete via End Date = Start Date and confirm it is gone.
    [Tags]    delete    cleanup
    Delete Well Hookup    ${TEST_CODE}    ${END_DATE}
    Well Hookup Row Should Not Exist    ${TEST_CODE}
    Well Hookup Should Not Exist In DB    ${TEST_CODE}
    Capture Step    well_hookup_tc04_deleted


*** Keywords ***
Set Up Well Hookup Suite
    [Documentation]    Generate a unique test code/name, open the screen, fill the navigator cascade.
    Prepare IUD Object Data    AUTOTEST_WH_    Well Hookup
    ${pu}=    Open Well Hookup Screen
    VAR    ${GM_PU}    ${pu}    scope=SUITE
