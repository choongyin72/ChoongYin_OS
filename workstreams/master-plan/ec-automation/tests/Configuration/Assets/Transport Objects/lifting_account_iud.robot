*** Settings ***
Documentation       EC IUD Test - Lifting Account (Configuration > Assets > Transport Objects).
...                 OV-GM (manage-object, groupmodel): grid filtered by the navigator cascade.
...                 DELETE = End Date = Start Date (true delete in OV_LIFTING_ACCOUNT). NEVER touch existing data;
...                 a unique AUTOTEST_LA_<timestamp> code is generated per run.

Resource            ../../../../pageobjects/Configuration/Assets/Transport Objects/lifting_account_page.resource

Suite Setup         Set Up Lifting Account Suite
Suite Teardown      Close EC

Test Tags           iud    lifting_account


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
    Lifting Account Row Should Not Exist    ${TEST_CODE}
    Capture Step    lifting_account_tc01_clean

TC02 Insert New Lifting Account
    [Documentation]    Insert under the navigator scope and confirm it lists.
    [Tags]    insert
    Insert Lifting Account Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Lifting Account Row Should Exist    ${TEST_CODE}
    Lifting Account Should Exist In DB    ${TEST_CODE}
    Capture Step    lifting_account_tc02_inserted

TC03 Update Lifting Account Name
    [Documentation]    Edit the name and confirm the list reflects the change.
    [Tags]    update
    Update Lifting Account Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Lifting Account Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    lifting_account_tc03_updated

TC04 Delete Lifting Account
    [Documentation]    Delete via End Date = Start Date and confirm it is gone.
    [Tags]    delete    cleanup
    Delete Lifting Account    ${TEST_CODE}    ${END_DATE}
    Lifting Account Row Should Not Exist    ${TEST_CODE}
    Lifting Account Should Not Exist In DB    ${TEST_CODE}
    Capture Step    lifting_account_tc04_deleted


*** Keywords ***
Set Up Lifting Account Suite
    [Documentation]    Generate a unique test code/name, open the screen, fill the navigator cascade.
    Prepare IUD Object Data    AUTOTEST_LA_    Lifting Account
    ${pu}=    Open Lifting Account Screen
    VAR    ${GM_PU}    ${pu}    scope=SUITE
