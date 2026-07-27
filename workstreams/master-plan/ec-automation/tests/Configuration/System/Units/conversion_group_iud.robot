*** Settings ***
Documentation       EC IUD Test - Conversion Group (Configuration > System > Units > Conversion Group, CO.1049).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_CONVERSION_GROUP).
...                 Layered: this test -> conversion_group_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Unique AUTOTEST_CVG_<timestamp> code per run.

Resource            ../../../../pageobjects/Configuration/System/Units/conversion_group_page.resource

Suite Setup         Set Up Conversion Group Suite
Suite Teardown      Close EC

Test Tags           iud    conversion_group


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test conversion_group does not exist before inserting.
    [Tags]    clean-state
    Conversion Group Row Should Not Exist    ${TEST_CODE}
    Capture Step    conversion_group_tc01_clean

TC02 Insert New Conversion Group
    [Documentation]    Insert a new conversion_group; confirm in list + DB (OV_CONVERSION_GROUP).
    [Tags]    insert
    Insert Conversion Group Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Conversion Group Row Should Exist    ${TEST_CODE}
    Conversion Group Should Exist In DB    ${TEST_CODE}
    Capture Step    conversion_group_tc02_inserted

TC03 Update Conversion Group
    [Documentation]    Edit Name; confirm in list + DB ground truth.
    [Tags]    update
    Update Conversion Group Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Conversion Group Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Field Should Equal In View    OV_CONVERSION_GROUP    ${TEST_CODE}    NAME    ${OBJ_NAME_UPD}
    Capture Step    conversion_group_tc03_updated

TC04 Delete Conversion Group
    [Documentation]    Delete via End Date = Start Date; confirm gone from list + DB.
    [Tags]    delete    cleanup
    Delete Conversion Group    ${TEST_CODE}    ${END_DATE}
    Conversion Group Row Should Not Exist    ${TEST_CODE}
    Conversion Group Should Not Exist In DB    ${TEST_CODE}
    Capture Step    conversion_group_tc04_deleted


*** Keywords ***
Set Up Conversion Group Suite
    [Documentation]    Generate a unique test code/name, then open the Conversion Group screen.
    Prepare IUD Object Data    AUTOTEST_CVG_    Conversion Group
    Open Conversion Group Screen
