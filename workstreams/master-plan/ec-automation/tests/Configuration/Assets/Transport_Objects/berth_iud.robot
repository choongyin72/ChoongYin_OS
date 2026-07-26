*** Settings ***
Documentation       EC IUD Test - Berth (Configuration > Assets > Transport Objects > Berth, CO.2012).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_BERTH).
...                 Layered: this test -> berth_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Unique AUTOTEST_BERTH_<timestamp> code per run.

Resource            ../../../../pageobjects/Configuration/Assets/Transport_Objects/berth_page.resource

Suite Setup         Set Up Berth Suite
Suite Teardown      Close EC

Test Tags           iud    berth


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test berth does not exist before inserting.
    [Tags]    clean-state
    Berth Row Should Not Exist    ${TEST_CODE}
    Capture Step    berth_tc01_clean

TC02 Insert New Berth
    [Documentation]    Insert a new berth; confirm in list + DB (OV_BERTH).
    [Tags]    insert
    Insert Berth Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Berth Row Should Exist    ${TEST_CODE}
    Berth Should Exist In DB    ${TEST_CODE}
    Capture Step    berth_tc02_inserted

TC03 Update Berth
    [Documentation]    Edit Name; confirm in list + DB ground truth.
    [Tags]    update
    Update Berth Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Berth Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Field Should Equal In View    OV_BERTH    ${TEST_CODE}    NAME    ${OBJ_NAME_UPD}
    Capture Step    berth_tc03_updated

TC04 Delete Berth
    [Documentation]    Delete via End Date = Start Date; confirm gone from list + DB.
    [Tags]    delete    cleanup
    Delete Berth    ${TEST_CODE}    ${END_DATE}
    Berth Row Should Not Exist    ${TEST_CODE}
    Berth Should Not Exist In DB    ${TEST_CODE}
    Capture Step    berth_tc04_deleted


*** Keywords ***
Set Up Berth Suite
    [Documentation]    Generate a unique test code/name, then open the Berth screen.
    Prepare IUD Object Data    AUTOTEST_BERTH_    Berth
    Open Berth Screen
