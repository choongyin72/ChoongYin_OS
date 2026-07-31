*** Settings ***
Documentation       EC IUD Test - Pilot (Configuration > Assets > Transport_Objects).
...                 OV-GM (manage-object, groupmodel): grid filtered by the navigator cascade.
...                 DELETE = End Date = Start Date (true delete in OV_PILOT). NEVER touch existing data;
...                 a unique AUTOTEST_PL_<timestamp> code is generated per run.

Resource            ../../../../pageobjects/Configuration/Assets/Transport_Objects/pilot_page.resource

Suite Setup         Set Up Pilot Suite
Suite Teardown      Close EC

Test Tags           iud    pilot


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
    Pilot Row Should Not Exist    ${TEST_CODE}
    Capture Step    pilot_tc01_clean

TC02 Insert New Pilot
    [Documentation]    Insert under the navigator scope and confirm it lists.
    [Tags]    insert
    Insert Pilot Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Pilot Row Should Exist    ${TEST_CODE}
    Pilot Should Exist In DB    ${TEST_CODE}
    Capture Step    pilot_tc02_inserted

TC03 Update Pilot Name
    [Documentation]    Edit the name and confirm the list reflects the change.
    [Tags]    update
    Update Pilot Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Pilot Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    pilot_tc03_updated

TC04 Delete Pilot
    [Documentation]    Delete via End Date = Start Date and confirm it is gone.
    [Tags]    delete    cleanup
    Delete Pilot    ${TEST_CODE}    ${END_DATE}
    Pilot Row Should Not Exist    ${TEST_CODE}
    Pilot Should Not Exist In DB    ${TEST_CODE}
    Capture Step    pilot_tc04_deleted


*** Keywords ***
Set Up Pilot Suite
    [Documentation]    Generate a unique test code/name, open the screen, fill the navigator cascade.
    Prepare IUD Object Data    AUTOTEST_PL_    Pilot
    ${pu}=    Open Pilot Screen
    VAR    ${GM_PU}    ${pu}    scope=SUITE
