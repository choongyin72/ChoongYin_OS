*** Settings ***
Documentation       EC IUD Test - Test Device (Configuration > Assets > Facility_Objects).
...                 OV-GM (manage-object, groupmodel): grid filtered by the navigator cascade.
...                 DELETE = End Date = Start Date (true delete in OV_TEST_DEVICE). NEVER touch existing data;
...                 a unique AUTOTEST_TD_<timestamp> code is generated per run.

Resource            ../../../../pageobjects/Configuration/Assets/Facility_Objects/test_device_page.resource

Suite Setup         Set Up Test Device Suite
Suite Teardown      Close EC

Test Tags           iud    test_device


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
    Test Device Row Should Not Exist    ${TEST_CODE}
    Capture Step    test_device_tc01_clean

TC02 Insert New Test Device
    [Documentation]    Insert under the navigator scope and confirm it lists.
    [Tags]    insert
    Insert Test Device Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Test Device Row Should Exist    ${TEST_CODE}
    Test Device Should Exist In DB    ${TEST_CODE}
    Capture Step    test_device_tc02_inserted

TC03 Update Test Device Name
    [Documentation]    Edit the name and confirm the list reflects the change.
    [Tags]    update
    Update Test Device Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Test Device Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    test_device_tc03_updated

TC04 Delete Test Device
    [Documentation]    Delete via End Date = Start Date and confirm it is gone.
    [Tags]    delete    cleanup
    Delete Test Device    ${TEST_CODE}    ${END_DATE}
    Test Device Row Should Not Exist    ${TEST_CODE}
    Test Device Should Not Exist In DB    ${TEST_CODE}
    Capture Step    test_device_tc04_deleted


*** Keywords ***
Set Up Test Device Suite
    [Documentation]    Generate a unique test code/name, open the screen, fill the navigator cascade.
    Prepare IUD Object Data    AUTOTEST_TD_    Test Device
    ${pu}=    Open Test Device Screen
    VAR    ${GM_PU}    ${pu}    scope=SUITE
