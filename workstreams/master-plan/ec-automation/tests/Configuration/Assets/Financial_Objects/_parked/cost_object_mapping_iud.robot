*** Settings ***
Documentation       EC IUD Test - Cost Object Mapping (Configuration > Assets > Financial Objects > Cost Object Mapping).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_FIN_COST_OBJECT).
...                 NEVER touch existing data. A unique AUTOTEST_COM_<timestamp> code is generated
...                 per run (EC keeps deleted codes in the base table, so codes are never reused).

Resource            ../../../../../pageobjects/Configuration/Assets/Financial_Objects/cost_object_mapping_page.resource

Suite Setup         Set Up Cost Object Mapping Suite
Suite Teardown      Close EC

Test Tags           iud    parked-needs-deeper-work    cost-object-mapping


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       2000-01-01
${END_DATE}         2000-01-01


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test cost object mapping does not exist before inserting.
    [Tags]    clean-state
    Cost Object Mapping Row Should Not Exist    ${TEST_CODE}
    Capture Step    cost_object_mapping_tc01_clean

TC02 Insert New Cost Object Mapping
    [Documentation]    Insert a new cost object mapping and confirm it appears in the list.
    [Tags]    insert
    Insert Cost Object Mapping Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Cost Object Mapping Row Should Exist    ${TEST_CODE}
    Cost Object Mapping Should Exist In DB    ${TEST_CODE}
    Capture Step    cost_object_mapping_tc02_inserted

TC03 Update Cost Object Mapping Name
    [Documentation]    Edit the cost object mapping name and confirm the list reflects the change.
    [Tags]    update
    Update Cost Object Mapping Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Cost Object Mapping Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    cost_object_mapping_tc03_updated

TC04 Delete Cost Object Mapping
    [Documentation]    Delete via End Date = Start Date and confirm the cost object mapping is gone.
    [Tags]    delete    cleanup
    Delete Cost Object Mapping    ${TEST_CODE}    ${END_DATE}
    Cost Object Mapping Row Should Not Exist    ${TEST_CODE}
    Cost Object Mapping Should Not Exist In DB    ${TEST_CODE}
    Capture Step    cost_object_mapping_tc04_deleted


*** Keywords ***
Set Up Cost Object Mapping Suite
    [Documentation]    Generate a unique test code/name, then open the Cost Object Mapping screen.
    ${code}    Generate Unique Code    AUTOTEST_COM_
    VAR    ${TEST_CODE}    ${code}    scope=SUITE
    VAR    ${OBJ_NAME}    Cost Object Mapping ${code}    scope=SUITE
    VAR    ${OBJ_NAME_UPD}    Cost Object Mapping ${code} UPD    scope=SUITE
    Open Cost Object Mapping Screen
