*** Settings ***
Documentation       EC IUD Test - Tug Boat (Configuration > Assets > Transport Objects).
...                 OV-GM (manage-object, groupmodel): grid filtered by the navigator cascade.
...                 DELETE = End Date = Start Date (true delete in OV_TUG_BOAT). NEVER touch existing data;
...                 a unique AUTOTEST_TB_<timestamp> code is generated per run.

Resource            ../../../../pageobjects/Configuration/Assets/Transport Objects/tug_boat_page.resource

Suite Setup         Set Up Tug Boat Suite
Suite Teardown      Close EC

Test Tags           iud    tug_boat


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
    Tug Boat Row Should Not Exist    ${TEST_CODE}
    Capture Step    tug_boat_tc01_clean

TC02 Insert New Tug Boat
    [Documentation]    Insert under the navigator scope and confirm it lists.
    [Tags]    insert
    Insert Tug Boat Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Tug Boat Row Should Exist    ${TEST_CODE}
    Tug Boat Should Exist In DB    ${TEST_CODE}
    Capture Step    tug_boat_tc02_inserted

TC03 Update Tug Boat Name
    [Documentation]    Edit the name and confirm the list reflects the change.
    [Tags]    update
    Update Tug Boat Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Tug Boat Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    tug_boat_tc03_updated

TC04 Delete Tug Boat
    [Documentation]    Delete via End Date = Start Date and confirm it is gone.
    [Tags]    delete    cleanup
    Delete Tug Boat    ${TEST_CODE}    ${END_DATE}
    Tug Boat Row Should Not Exist    ${TEST_CODE}
    Tug Boat Should Not Exist In DB    ${TEST_CODE}
    Capture Step    tug_boat_tc04_deleted


*** Keywords ***
Set Up Tug Boat Suite
    [Documentation]    Generate a unique test code/name, open the screen, fill the navigator cascade.
    Prepare IUD Object Data    AUTOTEST_TB_    Tug Boat
    ${pu}=    Open Tug Boat Screen
    VAR    ${GM_PU}    ${pu}    scope=SUITE
