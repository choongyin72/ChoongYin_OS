*** Settings ***
Documentation       EC IUD Test - Deferment Group (Configuration > Assets > Facility_Objects > Deferment Group, CO.0149).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_DEFERMENT_GROUP).
...                 Layered: this test -> deferment_group_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Unique AUTOTEST_DG_<timestamp> code per run.

Resource            ../../../../pageobjects/Configuration/Assets/Facility_Objects/deferment_group_page.resource

Suite Setup         Set Up Deferment Group Suite
Suite Teardown      Close EC

Test Tags           iud    deferment_group


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test deferment_group does not exist before inserting.
    [Tags]    clean-state
    Deferment Group Row Should Not Exist    ${TEST_CODE}
    Capture Step    deferment_group_tc01_clean

TC02 Insert New Deferment Group
    [Documentation]    Insert a new deferment_group; confirm in list + DB (OV_DEFERMENT_GROUP).
    [Tags]    insert
    Insert Deferment Group Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Deferment Group Row Should Exist    ${TEST_CODE}
    Deferment Group Should Exist In DB    ${TEST_CODE}
    Capture Step    deferment_group_tc02_inserted

TC03 Update Deferment Group
    [Documentation]    Edit Name; confirm in list + DB ground truth.
    [Tags]    update
    Update Deferment Group Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Deferment Group Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Field Should Equal In View    OV_DEFERMENT_GROUP    ${TEST_CODE}    NAME    ${OBJ_NAME_UPD}
    Capture Step    deferment_group_tc03_updated

TC04 Delete Deferment Group
    [Documentation]    Delete via End Date = Start Date; confirm gone from list + DB.
    [Tags]    delete    cleanup
    Delete Deferment Group    ${TEST_CODE}    ${END_DATE}
    Deferment Group Row Should Not Exist    ${TEST_CODE}
    Deferment Group Should Not Exist In DB    ${TEST_CODE}
    Capture Step    deferment_group_tc04_deleted


*** Keywords ***
Set Up Deferment Group Suite
    [Documentation]    Generate a unique test code/name, then open the Deferment Group screen.
    Prepare IUD Object Data    AUTOTEST_DG_    Deferment Group
    Open Deferment Group Screen
