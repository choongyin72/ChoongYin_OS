*** Settings ***
Documentation       EC IUD Test - HCB System (Configuration > Assets > Revenue_Lists > HCB System, CD.0097).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_BALANCE).
...                 Layered: this test -> hcb_system_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Unique AUTOTEST_HCB_<timestamp> code per run.

Resource            ../../../../pageobjects/Configuration/Assets/Revenue_Lists/hcb_system_page.resource

Suite Setup         Set Up HCB System Suite
Suite Teardown      Close EC

Test Tags           iud    hcb_system


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test hcb_system does not exist before inserting.
    [Tags]    clean-state
    HCB System Row Should Not Exist    ${TEST_CODE}
    Capture Step    hcb_system_tc01_clean

TC02 Insert New HCB System
    [Documentation]    Insert a new hcb_system; confirm in list + DB (OV_BALANCE).
    [Tags]    insert
    Insert HCB System Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    HCB System Row Should Exist    ${TEST_CODE}
    HCB System Should Exist In DB    ${TEST_CODE}
    Capture Step    hcb_system_tc02_inserted

TC03 Update HCB System
    [Documentation]    Edit Name; confirm in list + DB ground truth.
    [Tags]    update
    Update HCB System Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    HCB System Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Field Should Equal In View    OV_BALANCE    ${TEST_CODE}    NAME    ${OBJ_NAME_UPD}
    Capture Step    hcb_system_tc03_updated

TC04 Delete HCB System
    [Documentation]    Delete via End Date = Start Date; confirm gone from list + DB.
    [Tags]    delete    cleanup
    Delete HCB System    ${TEST_CODE}    ${END_DATE}
    HCB System Row Should Not Exist    ${TEST_CODE}
    HCB System Should Not Exist In DB    ${TEST_CODE}
    Capture Step    hcb_system_tc04_deleted


*** Keywords ***
Set Up HCB System Suite
    [Documentation]    Generate a unique test code/name, then open the HCB System screen.
    Prepare IUD Object Data    AUTOTEST_HCB_    HCB System
    Open HCB System Screen
