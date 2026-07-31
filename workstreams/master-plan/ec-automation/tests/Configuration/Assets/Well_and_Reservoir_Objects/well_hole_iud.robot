*** Settings ***
Documentation       EC IUD Test - Well Hole (Configuration > Assets > Well_and_Reservoir_Objects).
...                 OV-GM (manage-object, groupmodel): grid filtered by the navigator cascade.
...                 DELETE = End Date = Start Date (true delete in OV_WELL_HOLE). NEVER touch existing data;
...                 a unique AUTOTEST_WHL_<timestamp> code is generated per run.

Resource            ../../../../pageobjects/Configuration/Assets/Well_and_Reservoir_Objects/well_hole_page.resource

Suite Setup         Set Up Well Hole Suite
Suite Teardown      Close EC

Test Tags           iud    well_hole


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
    Well Hole Row Should Not Exist    ${TEST_CODE}
    Capture Step    well_hole_tc01_clean

TC02 Insert New Well Hole
    [Documentation]    Insert under the navigator scope and confirm it lists.
    [Tags]    insert
    Insert Well Hole Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Well Hole Row Should Exist    ${TEST_CODE}
    Well Hole Should Exist In DB    ${TEST_CODE}
    Capture Step    well_hole_tc02_inserted

TC03 Update Well Hole Name
    [Documentation]    Edit the name and confirm the list reflects the change.
    [Tags]    update
    Update Well Hole Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Well Hole Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    well_hole_tc03_updated

TC04 Delete Well Hole
    [Documentation]    Delete via End Date = Start Date and confirm it is gone.
    [Tags]    delete    cleanup
    Delete Well Hole    ${TEST_CODE}    ${END_DATE}
    Well Hole Row Should Not Exist    ${TEST_CODE}
    Well Hole Should Not Exist In DB    ${TEST_CODE}
    Capture Step    well_hole_tc04_deleted


*** Keywords ***
Set Up Well Hole Suite
    [Documentation]    Generate a unique test code/name, open the screen, fill the navigator cascade.
    Prepare IUD Object Data    AUTOTEST_WHL_    Well Hole
    ${pu}=    Open Well Hole Screen
    VAR    ${GM_PU}    ${pu}    scope=SUITE
