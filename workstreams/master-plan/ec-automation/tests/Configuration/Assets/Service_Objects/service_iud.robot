*** Settings ***
Documentation       EC IUD Test - Service (Configuration > Assets > Service_Objects).
...                 OV-GM (manage-object, groupmodel): grid filtered by the navigator cascade (PROVEN
...                 explicit values, not first-available).
...                 DELETE = End Date = Start Date (true delete in OV_SERVICE). NEVER touch existing data;
...                 a unique AUTOTEST_SV<timestamp> code is generated per run.

Resource            ../../../../pageobjects/Configuration/Assets/Service_Objects/service_page.resource

Suite Setup         Set Up Service Suite
Suite Teardown      Close EC

Test Tags           iud    service


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       2011-01-01
${END_DATE}         2000-01-01


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test object does not exist before inserting.
    [Tags]    clean-state
    Service Row Should Not Exist    ${TEST_CODE}
    Capture Step    service_tc01_clean

TC02 Insert New Service
    [Documentation]    Insert under the navigator scope and confirm it lists.
    [Tags]    insert
    Insert Service Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Service Row Should Exist    ${TEST_CODE}
    Service Should Exist In DB    ${TEST_CODE}
    Capture Step    service_tc02_inserted

TC03 Update Service Name
    [Documentation]    Edit the name and confirm the list reflects the change.
    [Tags]    update
    Update Service Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Service Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    service_tc03_updated

TC04 Delete Service
    [Documentation]    Delete via End Date = Start Date and confirm it is gone.
    [Tags]    delete    cleanup
    Delete Service    ${TEST_CODE}    ${END_DATE}
    Service Row Should Not Exist    ${TEST_CODE}
    Service Should Not Exist In DB    ${TEST_CODE}
    Capture Step    service_tc04_deleted


*** Keywords ***
Set Up Service Suite
    [Documentation]    Generate a unique test code/name, open the screen, fill the navigator cascade
    ...    with PROVEN explicit values (not first-available).
    Prepare IUD Object Data    AUTOTEST_SV    Service
    ${pu}=    Open Service Screen
    VAR    ${GM_PU}    ${pu}    scope=SUITE
