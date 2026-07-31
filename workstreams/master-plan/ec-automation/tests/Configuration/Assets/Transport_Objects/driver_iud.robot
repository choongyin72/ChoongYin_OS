*** Settings ***
Documentation       EC IUD Test - Driver (Configuration > Assets > Transport_Objects).
...                 OV-GM (manage-object, groupmodel): grid filtered by the navigator cascade.
...                 DELETE = End Date = Start Date (true delete in OV_DRIVER). NEVER touch existing data;
...                 a unique AUTOTEST_DR_<timestamp> code is generated per run.

Resource            ../../../../pageobjects/Configuration/Assets/Transport_Objects/driver_page.resource

Suite Setup         Set Up Driver Suite
Suite Teardown      Close EC

Test Tags           iud    driver


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
    Driver Row Should Not Exist    ${TEST_CODE}
    Capture Step    driver_tc01_clean

TC02 Insert New Driver
    [Documentation]    Insert under the navigator scope and confirm it lists.
    [Tags]    insert
    Insert Driver Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Driver Row Should Exist    ${TEST_CODE}
    Driver Should Exist In DB    ${TEST_CODE}
    Capture Step    driver_tc02_inserted

TC03 Update Driver Name
    [Documentation]    Edit the name and confirm the list reflects the change.
    [Tags]    update
    Update Driver Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Driver Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    driver_tc03_updated

TC04 Delete Driver
    [Documentation]    Delete via End Date = Start Date and confirm it is gone.
    [Tags]    delete    cleanup
    Delete Driver    ${TEST_CODE}    ${END_DATE}
    Driver Row Should Not Exist    ${TEST_CODE}
    Driver Should Not Exist In DB    ${TEST_CODE}
    Capture Step    driver_tc04_deleted


*** Keywords ***
Set Up Driver Suite
    [Documentation]    Generate a unique test code/name, open the screen, GO (date-only navigator).
    Prepare IUD Object Data    AUTOTEST_DR_    Driver
    Open Driver Screen
