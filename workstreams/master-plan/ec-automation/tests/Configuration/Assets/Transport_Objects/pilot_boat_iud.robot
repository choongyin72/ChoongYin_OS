*** Settings ***
Documentation       EC IUD Test - Pilot Boat (Configuration > Assets > Transport_Objects).
...                 OV-GM (manage-object, groupmodel): grid filtered by the navigator cascade.
...                 DELETE = End Date = Start Date (true delete in OV_PILOT_BOAT). NEVER touch existing data;
...                 a unique AUTOTEST_PB_<timestamp> code is generated per run.

Resource            ../../../../pageobjects/Configuration/Assets/Transport_Objects/pilot_boat_page.resource

Suite Setup         Set Up Pilot Boat Suite
Suite Teardown      Close EC

Test Tags           iud    pilot_boat


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
    Pilot Boat Row Should Not Exist    ${TEST_CODE}
    Capture Step    pilot_boat_tc01_clean

TC02 Insert New Pilot Boat
    [Documentation]    Insert under the navigator scope and confirm it lists.
    [Tags]    insert
    Insert Pilot Boat Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Pilot Boat Row Should Exist    ${TEST_CODE}
    Pilot Boat Should Exist In DB    ${TEST_CODE}
    Capture Step    pilot_boat_tc02_inserted

TC03 Update Pilot Boat Name
    [Documentation]    Edit the name and confirm the list reflects the change.
    [Tags]    update
    Update Pilot Boat Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Pilot Boat Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    pilot_boat_tc03_updated

TC04 Delete Pilot Boat
    [Documentation]    Delete via End Date = Start Date and confirm it is gone.
    [Tags]    delete    cleanup
    Delete Pilot Boat    ${TEST_CODE}    ${END_DATE}
    Pilot Boat Row Should Not Exist    ${TEST_CODE}
    Pilot Boat Should Not Exist In DB    ${TEST_CODE}
    Capture Step    pilot_boat_tc04_deleted


*** Keywords ***
Set Up Pilot Boat Suite
    [Documentation]    Generate a unique test code/name, open the screen, fill the navigator cascade.
    Prepare IUD Object Data    AUTOTEST_PB_    Pilot Boat
    ${pu}=    Open Pilot Boat Screen
    VAR    ${GM_PU}    ${pu}    scope=SUITE
