*** Settings ***
Documentation       EC IUD Test - Nomination Cycle (Configuration > Assets > Dispatching Objects).
...                 TABLE class (TV): inline grid, PHYSICAL delete (row gone from
...                 NOMINATION_CYCLE). Layered: this test -> nomination_cycle_page (T3) ->
...                 table_class (T2) + common (T1). NEVER touch existing data: unique
...                 AUTOTEST_NC_<timestamp> code per run.

Resource            ../../../../pageobjects/Configuration/Assets/Dispatching_Objects/nomination_cycle_page.resource

Suite Setup         Set Up Nomination Cycle Suite
Suite Teardown      Close EC

Test Tags           iud    nomination_cycle


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${SORT_ORDER}       990


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test cycle does not exist before inserting.
    [Tags]    clean-state
    Nomination Cycle Row Should Not Exist    ${TEST_CODE}
    Capture Step    nomination_cycle_tc01_clean

TC02 Insert New Nomination Cycle
    [Documentation]    Insert a new cycle row and confirm it appears in grid + base table.
    [Tags]    insert
    Insert Nomination Cycle    ${TEST_CODE}    ${OBJ_NAME}    ${SORT_ORDER}
    Nomination Cycle Row Should Exist    ${TEST_CODE}
    Nomination Cycle Should Exist In DB    ${TEST_CODE}
    Capture Step    nomination_cycle_tc02_inserted

TC03 Update Nomination Cycle Name
    [Documentation]    Edit the Name cell and confirm the grid reflects the change.
    [Tags]    update
    Update Nomination Cycle Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Nomination Cycle Name Should Be    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    nomination_cycle_tc03_updated

TC04 Delete Nomination Cycle
    [Documentation]    Physically delete the row and confirm it is gone (grid + base table).
    [Tags]    delete    cleanup
    Delete Nomination Cycle    ${TEST_CODE}
    Nomination Cycle Row Should Not Exist    ${TEST_CODE}
    Nomination Cycle Should Not Exist In DB    ${TEST_CODE}
    Capture Step    nomination_cycle_tc04_deleted


*** Keywords ***
Set Up Nomination Cycle Suite
    [Documentation]    Generate a unique test code/name, then open the Nomination Cycle screen.
    Prepare IUD Object Data    AUTOTEST_NC_    Nomination Cycle
    Open Nomination Cycle Screen
