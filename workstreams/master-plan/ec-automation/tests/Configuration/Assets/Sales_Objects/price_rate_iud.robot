*** Settings ***
Documentation       EC IUD Test - Price Rate (Configuration > Assets > Sales_Objects).
...                 OV-GM (manage-object, groupmodel): grid filtered by the navigator cascade (PROVEN
...                 explicit values, not first-available).
...                 DELETE = End Date = Start Date (true delete in OV_PRICE_RATE). NEVER touch existing data;
...                 a unique AUTOTEST_PRT_<timestamp> code is generated per run.

Resource            ../../../../pageobjects/Configuration/Assets/Sales_Objects/price_rate_page.resource

Suite Setup         Set Up Price Rate Suite
Suite Teardown      Close EC

Test Tags           iud    price_rate


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
    Price Rate Row Should Not Exist    ${TEST_CODE}
    Capture Step    price_rate_tc01_clean

TC02 Insert New Price Rate
    [Documentation]    Insert under the navigator scope and confirm it lists.
    [Tags]    insert
    Insert Price Rate Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Price Rate Row Should Exist    ${TEST_CODE}
    Price Rate Should Exist In DB    ${TEST_CODE}
    Capture Step    price_rate_tc02_inserted

TC03 Update Price Rate Name
    [Documentation]    Edit the name and confirm the list reflects the change.
    [Tags]    update
    Update Price Rate Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Price Rate Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    price_rate_tc03_updated

TC04 Delete Price Rate
    [Documentation]    Delete via End Date = Start Date and confirm it is gone.
    [Tags]    delete    cleanup
    Delete Price Rate    ${TEST_CODE}    ${END_DATE}
    Price Rate Row Should Not Exist    ${TEST_CODE}
    Price Rate Should Not Exist In DB    ${TEST_CODE}
    Capture Step    price_rate_tc04_deleted


*** Keywords ***
Set Up Price Rate Suite
    [Documentation]    Generate a unique test code/name, open the screen, fill the navigator cascade
    ...    with PROVEN explicit values (not first-available).
    Prepare IUD Object Data    AUTOTEST_PRT_    Price Rate
    ${pu}=    Open Price Rate Screen
    VAR    ${GM_PU}    ${pu}    scope=SUITE
