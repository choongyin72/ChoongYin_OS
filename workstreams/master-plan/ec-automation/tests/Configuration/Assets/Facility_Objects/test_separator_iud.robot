*** Settings ***
Documentation       EC IUD Test - Test Separator (Configuration > Assets > Facility_Objects).
...                 OV-GM (manage-object, groupmodel): grid filtered by the navigator cascade.
...                 DELETE = End Date = Start Date (true delete in OV_TESTSEPARATOR). NEVER touch existing data;
...                 a unique AUTOTEST_TSEP_<timestamp> code is generated per run.

Resource            ../../../../pageobjects/Configuration/Assets/Facility_Objects/test_separator_page.resource

Suite Setup         Set Up Test Separator Suite
Suite Teardown      Close EC

Test Tags           iud    test_separator


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
    Test Separator Row Should Not Exist    ${TEST_CODE}
    Capture Step    test_separator_tc01_clean

TC02 Insert New Test Separator
    [Documentation]    Insert under the navigator scope and confirm it lists.
    [Tags]    insert
    Insert Test Separator Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Test Separator Row Should Exist    ${TEST_CODE}
    Test Separator Should Exist In DB    ${TEST_CODE}
    Capture Step    test_separator_tc02_inserted

TC03 Update Test Separator Name
    [Documentation]    Edit the name and confirm the list reflects the change.
    [Tags]    update
    Update Test Separator Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Test Separator Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    test_separator_tc03_updated

TC04 Delete Test Separator
    [Documentation]    Delete via End Date = Start Date and confirm it is gone.
    [Tags]    delete    cleanup
    Delete Test Separator    ${TEST_CODE}    ${END_DATE}
    Test Separator Row Should Not Exist    ${TEST_CODE}
    Test Separator Should Not Exist In DB    ${TEST_CODE}
    Capture Step    test_separator_tc04_deleted


*** Keywords ***
Set Up Test Separator Suite
    [Documentation]    Generate a unique test code/name, open the screen, fill the navigator cascade.
    Prepare IUD Object Data    AUTOTEST_TSEP_    Test Separator
    ${pu}=    Open Test Separator Screen
    VAR    ${GM_PU}    ${pu}    scope=SUITE
