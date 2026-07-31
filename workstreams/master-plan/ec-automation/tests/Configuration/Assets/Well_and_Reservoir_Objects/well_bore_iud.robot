*** Settings ***
Documentation       EC IUD Test - Well Bore (Configuration > Assets > Well_and_Reservoir_Objects).
...                 OV-GM, per-field nav groups with SPECIFIC values (G:4 = a REAL well, P1 W008 OP;
...                 G:5 skipped - zero options under every scope tried). Mandatory 'Well' POPUP with
...                 list grid Objects:form:T_data (screen-local picker; picks the nav-scope well, not
...                 the popup's first row which is a graph object). DELETE = End Date = Start Date
...                 (true delete in OV_WELL_BORE). NEVER touch existing data; unique
...                 AUTOTEST_WB_<timestamp> code per run. Start Date 2020-01-01.

Resource            ../../../../pageobjects/Configuration/Assets/Well_and_Reservoir_Objects/well_bore_page.resource

Suite Setup         Set Up Well Bore Suite
Suite Teardown      Close EC

Test Tags           iud    well-bore


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       2020-01-01
${END_DATE}         2020-01-01


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test object does not exist before inserting.
    [Tags]    clean-state
    Well Bore Row Should Not Exist    ${TEST_CODE}
    Capture Step    well_bore_tc01_clean

TC02 Insert New Well Bore
    [Documentation]    Insert under the P1 well scope (incl. the mandatory Well popup) and confirm it lists.
    [Tags]    insert
    Insert Well Bore Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Well Bore Row Should Exist    ${TEST_CODE}
    Well Bore Should Exist In DB    ${TEST_CODE}
    Capture Step    well_bore_tc02_inserted

TC03 Update Well Bore Name
    [Documentation]    Edit the name and confirm the list reflects the change.
    [Tags]    update
    Update Well Bore Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Well Bore Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    well_bore_tc03_updated

TC04 Delete Well Bore
    [Documentation]    Delete via End Date = Start Date and confirm it is gone.
    [Tags]    delete    cleanup
    Delete Well Bore    ${TEST_CODE}    ${END_DATE}
    Well Bore Row Should Not Exist    ${TEST_CODE}
    Well Bore Should Not Exist In DB    ${TEST_CODE}
    Capture Step    well_bore_tc04_deleted


*** Keywords ***
Set Up Well Bore Suite
    [Documentation]    Generate a unique test code/name, open the screen, apply the P1 nav scope.
    Prepare IUD Object Data    AUTOTEST_WB_    Well Bore
    Open Well Bore Screen
