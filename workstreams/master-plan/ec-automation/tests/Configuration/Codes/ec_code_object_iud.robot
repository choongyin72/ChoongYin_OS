*** Settings ***
Documentation       EC IUD Test - EC Code Object (Configuration > Codes > EC Code Object, CD.0135).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_EC_CODE_OBJECT).
...                 Layered: this test -> ec_code_object_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Unique AUTOTEST_ECO_<timestamp> code per run.

Resource            ../../../pageobjects/Configuration/Codes/ec_code_object_page.resource

Suite Setup         Set Up EC Code Object Suite
Suite Teardown      Close EC

Test Tags           iud    ec_code_object


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test ec_code_object does not exist before inserting.
    [Tags]    clean-state
    EC Code Object Row Should Not Exist    ${TEST_CODE}
    Capture Step    ec_code_object_tc01_clean

TC02 Insert New EC Code Object
    [Documentation]    Insert a new ec_code_object; confirm in list + DB (OV_EC_CODE_OBJECT).
    [Tags]    insert
    Insert EC Code Object Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    EC Code Object Row Should Exist    ${TEST_CODE}
    EC Code Object Should Exist In DB    ${TEST_CODE}
    Capture Step    ec_code_object_tc02_inserted

TC03 Update EC Code Object
    [Documentation]    Edit Name; confirm in list + DB ground truth.
    [Tags]    update
    Update EC Code Object Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    EC Code Object Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Field Should Equal In View    OV_EC_CODE_OBJECT    ${TEST_CODE}    NAME    ${OBJ_NAME_UPD}
    Capture Step    ec_code_object_tc03_updated

TC04 Delete EC Code Object
    [Documentation]    Delete via End Date = Start Date; confirm gone from list + DB.
    [Tags]    delete    cleanup
    Delete EC Code Object    ${TEST_CODE}    ${END_DATE}
    EC Code Object Row Should Not Exist    ${TEST_CODE}
    EC Code Object Should Not Exist In DB    ${TEST_CODE}
    Capture Step    ec_code_object_tc04_deleted


*** Keywords ***
Set Up EC Code Object Suite
    [Documentation]    Generate a unique test code/name, then open the EC Code Object screen.
    Prepare IUD Object Data    AUTOTEST_ECO_    EC Code Object
    Open EC Code Object Screen
