*** Settings ***
Documentation       EC IUD Test - Well (Configuration > Assets > Well_and_Reservoir_Objects).
...                 OV-GM: 3-level cascade with SPECIFIC P1 values + GO (2nd-row Well filter dds
...                 left empty - owner screenshot ground truth; first-available AS1 left a deeper
...                 level empty = original park). Insert extra: Well Type (first-available).
...                 DELETE = End Date = Start Date (true delete in OV_WELL). NEVER touch existing
...                 data; unique AUTOTEST_WE_<timestamp> code per run. Start Date 2020-01-01.

Resource            ../../../../pageobjects/Configuration/Assets/Well_and_Reservoir_Objects/well_page.resource

Suite Setup         Set Up Well Suite
Suite Teardown      Close EC

Test Tags           iud    well


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
    Well Row Should Not Exist    ${TEST_CODE}
    Capture Step    well_tc01_clean

TC02 Insert New Well
    [Documentation]    Insert under the P1 navigator scope and confirm it lists.
    [Tags]    insert
    Insert Well Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Well Row Should Exist    ${TEST_CODE}
    Well Should Exist In DB    ${TEST_CODE}
    Capture Step    well_tc02_inserted

TC03 Update Well Name
    [Documentation]    Edit the name and confirm the list reflects the change.
    [Tags]    update
    Update Well Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Well Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    well_tc03_updated

TC04 Delete Well
    [Documentation]    Delete via End Date = Start Date and confirm it is gone.
    [Tags]    delete    cleanup
    Delete Well    ${TEST_CODE}    ${END_DATE}
    Well Row Should Not Exist    ${TEST_CODE}
    Well Should Not Exist In DB    ${TEST_CODE}
    Capture Step    well_tc04_deleted


*** Keywords ***
Set Up Well Suite
    [Documentation]    Generate a unique test code/name, open the screen, apply the P1 nav scope.
    Prepare IUD Object Data    AUTOTEST_WE_    Well
    Open Well Screen
