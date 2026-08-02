*** Settings ***
Documentation       EC IUD Test - Price Index (Configuration > Assets > Sales_Objects).
...                 OV-GM (manage-object, groupmodel): grid filtered by the navigator cascade (PROVEN
...                 explicit values, not first-available).
...                 DELETE = End Date = Start Date (true delete in OV_PRICE_INDEX). NEVER touch existing data;
...                 a unique AUTOTEST_PI_<timestamp> code is generated per run.

Resource            ../../../../pageobjects/Configuration/Assets/Sales_Objects/price_index_page.resource

Suite Setup         Set Up Price Index Suite
Suite Teardown      Close EC

Test Tags           iud    price_index


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       2003-01-01
${END_DATE}         2000-01-01


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test object does not exist before inserting.
    [Tags]    clean-state
    Price Index Row Should Not Exist    ${TEST_CODE}
    Capture Step    price_index_tc01_clean

TC02 Insert New Price Index
    [Documentation]    Insert under the navigator scope and confirm it lists.
    [Tags]    insert
    Insert Price Index Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Price Index Row Should Exist    ${TEST_CODE}
    Price Index Should Exist In DB    ${TEST_CODE}
    Capture Step    price_index_tc02_inserted

TC03 Update Price Index Name
    [Documentation]    Edit the name and confirm the list reflects the change.
    [Tags]    update
    Update Price Index Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Price Index Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    price_index_tc03_updated

TC04 Delete Price Index
    [Documentation]    Delete via End Date = Start Date and confirm it is gone.
    [Tags]    delete    cleanup
    Delete Price Index    ${TEST_CODE}    ${END_DATE}
    Price Index Row Should Not Exist    ${TEST_CODE}
    Price Index Should Not Exist In DB    ${TEST_CODE}
    Capture Step    price_index_tc04_deleted


*** Keywords ***
Set Up Price Index Suite
    [Documentation]    Generate a unique test code/name, open the screen, fill the navigator cascade
    ...    with PROVEN explicit values (not first-available).
    Prepare IUD Object Data    AUTOTEST_PI_    Price Index
    ${pu}=    Open Price Index Screen
    VAR    ${GM_PU}    ${pu}    scope=SUITE
