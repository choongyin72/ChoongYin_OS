*** Settings ***
Documentation       EC IUD Test - Price Object (Configuration > Assets > Sales_Objects).
...                 OV-GM (manage-object, groupmodel): grid filtered by the navigator cascade.
...                 DELETE = End Date = Start Date (true delete in OV_PRICE_OBJECT). NEVER touch existing data;
...                 a unique AUTOTEST_PO_<timestamp> code is generated per run.

Resource            ../../../../pageobjects/Configuration/Assets/Sales_Objects/price_object_page.resource

Suite Setup         Set Up Price Object Suite
Suite Teardown      Close EC

Test Tags           iud    price_object


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       2020-01-01
${END_DATE}         2000-01-01


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test object does not exist before inserting.
    [Tags]    clean-state
    Price Object Row Should Not Exist    ${TEST_CODE}
    Capture Step    price_object_tc01_clean

TC02 Insert New Price Object
    [Documentation]    Insert under the navigator scope and confirm it lists.
    [Tags]    insert
    Insert Price Object Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Price Object Row Should Exist    ${TEST_CODE}
    Price Object Should Exist In DB    ${TEST_CODE}
    Capture Step    price_object_tc02_inserted

TC03 Update Price Object Name
    [Documentation]    Edit the name and confirm the list reflects the change.
    [Tags]    update
    Update Price Object Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Price Object Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    price_object_tc03_updated

TC04 Delete Price Object
    [Documentation]    Delete via End Date = Start Date and confirm it is gone.
    [Tags]    delete    cleanup
    Delete Price Object    ${TEST_CODE}    ${END_DATE}
    Price Object Row Should Not Exist    ${TEST_CODE}
    Price Object Should Not Exist In DB    ${TEST_CODE}
    Capture Step    price_object_tc04_deleted


*** Keywords ***
Set Up Price Object Suite
    [Documentation]    Generate a unique test code/name, open the screen, fill the navigator cascade.
    Prepare IUD Object Data    AUTOTEST_PO_    Price Object
    ${pu}=    Open Price Object Screen
    VAR    ${GM_PU}    ${pu}    scope=SUITE
