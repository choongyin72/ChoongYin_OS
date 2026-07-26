*** Settings ***
Documentation       EC IUD Test - Chemical Transport Tank (Configuration > Assets > Chemical_Objects > Chemical Transport Tank, CO.0257).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_CHEM_TRANS_TANK).
...                 Layered: this test -> chemical_transport_tank_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Unique AUTOTEST_CTT_<timestamp> code per run.

Resource            ../../../../pageobjects/Configuration/Assets/Chemical_Objects/chemical_transport_tank_page.resource

Suite Setup         Set Up Chemical Transport Tank Suite
Suite Teardown      Close EC

Test Tags           iud    chemical_transport_tank


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test chemical_transport_tank does not exist before inserting.
    [Tags]    clean-state
    Chemical Transport Tank Row Should Not Exist    ${TEST_CODE}
    Capture Step    chemical_transport_tank_tc01_clean

TC02 Insert New Chemical Transport Tank
    [Documentation]    Insert a new chemical_transport_tank; confirm in list + DB (OV_CHEM_TRANS_TANK).
    [Tags]    insert
    Insert Chemical Transport Tank Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Chemical Transport Tank Row Should Exist    ${TEST_CODE}
    Chemical Transport Tank Should Exist In DB    ${TEST_CODE}
    Capture Step    chemical_transport_tank_tc02_inserted

TC03 Update Chemical Transport Tank
    [Documentation]    Edit Name; confirm in list + DB ground truth.
    [Tags]    update
    Update Chemical Transport Tank Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Chemical Transport Tank Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Field Should Equal In View    OV_CHEM_TRANS_TANK    ${TEST_CODE}    NAME    ${OBJ_NAME_UPD}
    Capture Step    chemical_transport_tank_tc03_updated

TC04 Delete Chemical Transport Tank
    [Documentation]    Delete via End Date = Start Date; confirm gone from list + DB.
    [Tags]    delete    cleanup
    Delete Chemical Transport Tank    ${TEST_CODE}    ${END_DATE}
    Chemical Transport Tank Row Should Not Exist    ${TEST_CODE}
    Chemical Transport Tank Should Not Exist In DB    ${TEST_CODE}
    Capture Step    chemical_transport_tank_tc04_deleted


*** Keywords ***
Set Up Chemical Transport Tank Suite
    [Documentation]    Generate a unique test code/name, then open the Chemical Transport Tank screen.
    Prepare IUD Object Data    AUTOTEST_CTT_    Chemical Transport Tank
    Open Chemical Transport Tank Screen
