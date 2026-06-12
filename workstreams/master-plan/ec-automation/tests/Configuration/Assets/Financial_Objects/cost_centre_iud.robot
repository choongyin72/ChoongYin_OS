*** Settings ***
Documentation       EC IUD Test - Cost Centre (Configuration > Assets > Financial Objects > Cost Centre).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_FIN_COST_CENTER).
...                 NEVER touch existing data. A unique AUTOTEST_CC_<timestamp> code is generated
...                 per run (EC keeps deleted codes in the base table, so codes are never reused).

Resource            ../../../../pageobjects/Configuration/Assets/Financial_Objects/cost_centre_page.resource

Suite Setup         Set Up Cost Centre Suite
Suite Teardown      Close EC

Test Tags           iud    cost-centre


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test cost centre does not exist before inserting.
    [Tags]    clean-state
    Cost Centre Row Should Not Exist    ${TEST_CODE}
    Capture Step    cost_centre_tc01_clean

TC02 Insert New Cost Centre
    [Documentation]    Insert a new cost centre and confirm it appears in the list.
    [Tags]    insert
    Insert Cost Centre Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Cost Centre Row Should Exist    ${TEST_CODE}
    Cost Centre Should Exist In DB    ${TEST_CODE}
    Capture Step    cost_centre_tc02_inserted

TC03 Update Cost Centre Name
    [Documentation]    Edit the cost centre name and confirm the list reflects the change.
    [Tags]    update
    Update Cost Centre Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Cost Centre Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    cost_centre_tc03_updated

TC04 Delete Cost Centre
    [Documentation]    Delete via End Date = Start Date and confirm the cost centre is gone.
    [Tags]    delete    cleanup
    Delete Cost Centre    ${TEST_CODE}    ${END_DATE}
    Cost Centre Row Should Not Exist    ${TEST_CODE}
    Cost Centre Should Not Exist In DB    ${TEST_CODE}
    Capture Step    cost_centre_tc04_deleted


*** Keywords ***
Set Up Cost Centre Suite
    [Documentation]    Generate a unique test code/name, then open the Cost Centre screen.
    Prepare IUD Object Data    AUTOTEST_CC_    Cost Centre
    Open Cost Centre Screen
