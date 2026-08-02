*** Settings ***
Documentation       EC IUD Test - Division Order (EC_Revenue > Royalty > Royalty_USA).
...                 OV-GM (manage-object, groupmodel): grid filtered by the navigator cascade (PROVEN
...                 explicit values, not first-available).
...                 DELETE = End Date = Start Date (true delete in OV_DIVISION_ORDER). NEVER touch existing data;
...                 a unique AUTOTEST_DO_<timestamp> code is generated per run.

Resource            ../../../../pageobjects/EC_Revenue/Royalty/Royalty_USA/division_order_page.resource

Suite Setup         Set Up Division Order Suite
Suite Teardown      Close EC

Test Tags           iud    division_order


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
    Division Order Row Should Not Exist    ${TEST_CODE}
    Capture Step    division_order_tc01_clean

TC02 Insert New Division Order
    [Documentation]    Insert under the navigator scope and confirm it lists.
    [Tags]    insert
    Insert Division Order Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Division Order Row Should Exist    ${TEST_CODE}
    Division Order Should Exist In DB    ${TEST_CODE}
    Capture Step    division_order_tc02_inserted

TC03 Update Division Order Name
    [Documentation]    Edit the name and confirm the list reflects the change.
    [Tags]    update
    Update Division Order Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Division Order Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    division_order_tc03_updated

TC04 Delete Division Order
    [Documentation]    Delete via End Date = Start Date and confirm it is gone.
    [Tags]    delete    cleanup
    Delete Division Order    ${TEST_CODE}    ${END_DATE}
    Division Order Row Should Not Exist    ${TEST_CODE}
    Division Order Should Not Exist In DB    ${TEST_CODE}
    Capture Step    division_order_tc04_deleted


*** Keywords ***
Set Up Division Order Suite
    [Documentation]    Generate a unique test code/name, open the screen, fill the navigator cascade
    ...    with PROVEN explicit values (not first-available).
    Prepare IUD Object Data    AUTOTEST_DO_    Division Order
    ${pu}=    Open Division Order Screen
    VAR    ${GM_PU}    ${pu}    scope=SUITE
