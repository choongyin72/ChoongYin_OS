*** Settings ***
Documentation       EC IUD Test - Config Variable (Configuration > Assets > Calculation_Objects > Config Variable, IN.0031).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_CONFIG_VARIABLE).
...                 Layered: this test -> config_variable_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Unique AUTOTEST_CV_<timestamp> code per run.

Resource            ../../../../pageobjects/Configuration/Assets/Calculation_Objects/config_variable_page.resource

Suite Setup         Set Up Config Variable Suite
Suite Teardown      Close EC

Test Tags           iud    config_variable


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test config_variable does not exist before inserting.
    [Tags]    clean-state
    Config Variable Row Should Not Exist    ${TEST_CODE}
    Capture Step    config_variable_tc01_clean

TC02 Insert New Config Variable
    [Documentation]    Insert a new config_variable; confirm in list + DB (OV_CONFIG_VARIABLE).
    [Tags]    insert
    Insert Config Variable Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Config Variable Row Should Exist    ${TEST_CODE}
    Config Variable Should Exist In DB    ${TEST_CODE}
    Capture Step    config_variable_tc02_inserted

TC03 Update Config Variable
    [Documentation]    Edit Name; confirm in list + DB ground truth.
    [Tags]    update
    Update Config Variable Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Config Variable Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Field Should Equal In View    OV_CONFIG_VARIABLE    ${TEST_CODE}    NAME    ${OBJ_NAME_UPD}
    Capture Step    config_variable_tc03_updated

TC04 Delete Config Variable
    [Documentation]    Delete via End Date = Start Date; confirm gone from list + DB.
    [Tags]    delete    cleanup
    Delete Config Variable    ${TEST_CODE}    ${END_DATE}
    Config Variable Row Should Not Exist    ${TEST_CODE}
    Config Variable Should Not Exist In DB    ${TEST_CODE}
    Capture Step    config_variable_tc04_deleted


*** Keywords ***
Set Up Config Variable Suite
    [Documentation]    Generate a unique test code/name, then open the Config Variable screen.
    Prepare IUD Object Data    AUTOTEST_CV_    Config Variable
    Open Config Variable Screen
