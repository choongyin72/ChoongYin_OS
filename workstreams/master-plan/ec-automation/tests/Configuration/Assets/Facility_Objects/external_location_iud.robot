*** Settings ***
Documentation       EC IUD Test - External Location (Configuration > Assets > Facility_Objects).
...                 OV-GM (manage-object, groupmodel): grid loads on GO alone (no mandatory nav scope).
...                 DELETE = End Date = Start Date (true delete in OV_EXTERNAL_LOCATION). NEVER touch existing data;
...                 a unique AUTOTEST_EL<timestamp> code is generated per run.

Resource            ../../../../pageobjects/Configuration/Assets/Facility_Objects/external_location_page.resource

Suite Setup         Set Up External Location Suite
Suite Teardown      Close EC

Test Tags           iud    external_location


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
    External Location Row Should Not Exist    ${TEST_CODE}
    Capture Step    external_location_tc01_clean

TC02 Insert New External Location
    [Documentation]    Insert (no mandatory nav scope on this screen) and confirm it lists.
    [Tags]    insert
    Insert External Location Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    External Location Row Should Exist    ${TEST_CODE}
    External Location Should Exist In DB    ${TEST_CODE}
    Capture Step    external_location_tc02_inserted

TC03 Update External Location Name
    [Documentation]    Edit the name and confirm the list reflects the change.
    [Tags]    update
    Update External Location Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    External Location Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    external_location_tc03_updated

TC04 Delete External Location
    [Documentation]    Delete via End Date = Start Date and confirm it is gone.
    [Tags]    delete    cleanup
    Delete External Location    ${TEST_CODE}    ${END_DATE}
    External Location Row Should Not Exist    ${TEST_CODE}
    External Location Should Not Exist In DB    ${TEST_CODE}
    Capture Step    external_location_tc04_deleted


*** Keywords ***
Set Up External Location Suite
    [Documentation]    Generate a unique test code/name, open the screen (GO alone, no mandatory nav
    ...    scope on this screen).
    Prepare IUD Object Data    AUTOTEST_EL    External Location
    ${pu}=    Open External Location Screen
    VAR    ${GM_PU}    ${pu}    scope=SUITE
