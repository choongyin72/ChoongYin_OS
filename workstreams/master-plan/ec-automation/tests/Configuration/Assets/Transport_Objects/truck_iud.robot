*** Settings ***
Documentation       EC IUD Test - Truck (Configuration > Assets > Transport_Objects).
...                 OV-GM (manage-object, groupmodel): grid filtered by the navigator cascade.
...                 DELETE = End Date = Start Date (true delete in OV_TRUCK). NEVER touch existing data;
...                 a unique AUTOTEST_TK_<timestamp> code is generated per run.

Resource            ../../../../pageobjects/Configuration/Assets/Transport_Objects/truck_page.resource

Suite Setup         Set Up Truck Suite
Suite Teardown      Close EC

Test Tags           iud    truck


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
    Truck Row Should Not Exist    ${TEST_CODE}
    Capture Step    truck_tc01_clean

TC02 Insert New Truck
    [Documentation]    Insert under the navigator scope and confirm it lists.
    [Tags]    insert
    Insert Truck Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Truck Row Should Exist    ${TEST_CODE}
    Truck Should Exist In DB    ${TEST_CODE}
    Capture Step    truck_tc02_inserted

TC03 Update Truck Name
    [Documentation]    Edit the name and confirm the list reflects the change.
    [Tags]    update
    Update Truck Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Truck Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    truck_tc03_updated

TC04 Delete Truck
    [Documentation]    Delete via End Date = Start Date and confirm it is gone.
    [Tags]    delete    cleanup
    Delete Truck    ${TEST_CODE}    ${END_DATE}
    Truck Row Should Not Exist    ${TEST_CODE}
    Truck Should Not Exist In DB    ${TEST_CODE}
    Capture Step    truck_tc04_deleted


*** Keywords ***
Set Up Truck Suite
    [Documentation]    Generate a unique test code/name, open the screen, GO (date-only navigator).
    Prepare IUD Object Data    AUTOTEST_TK_    Truck
    Open Truck Screen
