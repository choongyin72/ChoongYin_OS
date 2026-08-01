*** Settings ***
Documentation       EC IUD Test - Operator Route (Configuration > Assets > Facility_Objects).
...                 OV-GM (manage-object, groupmodel): grid filtered by the navigator cascade (PROVEN
...                 explicit values, not first-available).
...                 DELETE = End Date = Start Date (true delete in OV_OPERATOR_ROUTE). NEVER touch existing data;
...                 a unique AUTOTEST_OR_<timestamp> code is generated per run.

Resource            ../../../../pageobjects/Configuration/Assets/Facility_Objects/operator_route_page.resource

Suite Setup         Set Up Operator Route Suite
Suite Teardown      Close EC

Test Tags           iud    operator_route


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
    Operator Route Row Should Not Exist    ${TEST_CODE}
    Capture Step    operator_route_tc01_clean

TC02 Insert New Operator Route
    [Documentation]    Insert under the navigator scope and confirm it lists.
    [Tags]    insert
    Insert Operator Route Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Operator Route Row Should Exist    ${TEST_CODE}
    Operator Route Should Exist In DB    ${TEST_CODE}
    Capture Step    operator_route_tc02_inserted

TC03 Update Operator Route Name
    [Documentation]    Edit the name and confirm the list reflects the change.
    [Tags]    update
    Update Operator Route Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Operator Route Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    operator_route_tc03_updated

TC04 Delete Operator Route
    [Documentation]    Delete via End Date = Start Date and confirm it is gone.
    [Tags]    delete    cleanup
    Delete Operator Route    ${TEST_CODE}    ${END_DATE}
    Operator Route Row Should Not Exist    ${TEST_CODE}
    Operator Route Should Not Exist In DB    ${TEST_CODE}
    Capture Step    operator_route_tc04_deleted


*** Keywords ***
Set Up Operator Route Suite
    [Documentation]    Generate a unique test code/name, open the screen, fill the navigator cascade
    ...    with PROVEN explicit values (not first-available).
    Prepare IUD Object Data    AUTOTEST_OR_    Operator Route
    ${pu}=    Open Operator Route Screen
    VAR    ${GM_PU}    ${pu}    scope=SUITE
