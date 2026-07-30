*** Settings ***
Documentation       EC IUD Test - Well (Configuration > Assets > Well and Reservoir Objects).
...                 OV-GM (manage-object, groupmodel): grid filtered by the navigator cascade.
...                 DELETE = End Date = Start Date (true delete in OV_WELL). NEVER touch existing data;
...                 a unique AUTOTEST_WL_<timestamp> code is generated per run.

Resource            ../../../../pageobjects/Configuration/Assets/Well and Reservoir Objects/well_page.resource

Suite Setup         Set Up Well Suite
Suite Teardown      Close EC

Test Tags           iud    well


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
    Well Row Should Not Exist    ${TEST_CODE}
    Capture Step    well_tc01_clean

TC02 Insert New Well
    [Documentation]    Insert under the navigator scope and confirm it lists.
    [Tags]    insert
    Insert Well Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Well Row Should Exist    ${TEST_CODE}
    Well Should Exist In DB    ${TEST_CODE}
    Capture Step    well_tc02_inserted

TC03 Update Well Name
    [Documentation]    Edit the name and confirm the list reflects the change.
    [Tags]    update
    Update Well Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Well Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    well_tc03_updated

TC04 Delete Well
    [Documentation]    Delete via End Date = Start Date and confirm it is gone.
    [Tags]    delete    cleanup
    Delete Well    ${TEST_CODE}    ${END_DATE}
    Well Row Should Not Exist    ${TEST_CODE}
    Well Should Not Exist In DB    ${TEST_CODE}
    Capture Step    well_tc04_deleted


*** Keywords ***
Set Up Well Suite
    [Documentation]    Generate a unique test code/name, open the screen, fill the navigator cascade.
    Prepare IUD Object Data    AUTOTEST_WL_    Well
    ${pu}=    Open Well Screen
    VAR    ${GM_PU}    ${pu}    scope=SUITE
