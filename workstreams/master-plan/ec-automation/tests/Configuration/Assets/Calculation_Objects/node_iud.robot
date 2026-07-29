*** Settings ***
Documentation       EC IUD Test - Node (Configuration > Assets > Calculation Objects > Node).
...                 OV-GM (manage-object, groupmodel) screen: the grid is filtered by the navigator
...                 cascade (Production Unit -> Area -> Facility Class 1). The insert Op Production Unit
...                 = the captured navigator top-parent so the new row appears in the filtered grid.
...                 DELETE = End Date = Start Date (true delete in OV_NODE). NEVER touch existing data;
...                 a unique AUTOTEST_ND_<timestamp> code is generated per run.

Resource            ../../../../pageobjects/Configuration/Assets/Calculation_Objects/node_page.resource

Suite Setup         Set Up Node Suite
Suite Teardown      Close EC

Test Tags           iud    node


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
# proven start date for the first-available nav PU (Op Production Unit dropdown is date-filtered)
${START_DATE}       2000-01-01
${END_DATE}         2000-01-01
${CALC_SEQ}         1


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test node does not exist before inserting.
    [Tags]    clean-state
    Node Row Should Not Exist    ${TEST_CODE}
    Capture Step    node_tc01_clean

TC02 Insert New Node
    [Documentation]    Insert a new node under the captured navigator PU and confirm it lists.
    [Tags]    insert
    # Op Production Unit = __FIRST__: the Op PU panel does NOT contain the nav top-parent PU (${NODE_PU});
    # ground truth tmp/node/probe_op_pu.py - the row lists after GO regardless (proven by the PW driver 8/8).
    Insert Node Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}    ${CALC_SEQ}    __FIRST__
    Node Row Should Exist    ${TEST_CODE}
    Node Should Exist In DB    ${TEST_CODE}
    Capture Step    node_tc02_inserted

TC03 Update Node Name
    [Documentation]    Edit the node name and confirm the list reflects the change.
    [Tags]    update
    Update Node Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Node Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    node_tc03_updated

TC04 Delete Node
    [Documentation]    Delete via End Date = Start Date and confirm the node is gone.
    [Tags]    delete    cleanup
    Delete Node    ${TEST_CODE}    ${END_DATE}
    Node Row Should Not Exist    ${TEST_CODE}
    Node Should Not Exist In DB    ${TEST_CODE}
    Capture Step    node_tc04_deleted


*** Keywords ***
Set Up Node Suite
    [Documentation]    Generate a unique test code/name, open the Node screen, and fill the
    ...    OV-GM navigator cascade first-available + GO, capturing the top-parent PU for the insert.
    Prepare IUD Object Data    AUTOTEST_ND_    Node
    ${pu}=    Open Node Screen
    VAR    ${NODE_PU}    ${pu}    scope=SUITE
