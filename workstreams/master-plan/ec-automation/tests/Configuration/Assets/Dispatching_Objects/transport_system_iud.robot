*** Settings ***
Documentation       EC IUD Test - Transport System (Configuration > Assets > Dispatching Objects > Transport System).
...                 OV-GM behaviour: navigator Business Unit + GO gates the grid; insert
...                 references "Business Unit Name" = ECP Norway so the row is visible
...                 under the ECP Norway filter. DELETE = End Date = Start Date (ov_transport_system).
...                 NEVER touch existing data: unique AUTOTEST_TS_<timestamp> code per run;
...                 the referenced parent objects are READ-ONLY seed data.

Resource            ../../../../pageobjects/Configuration/Assets/Dispatching_Objects/transport_system_page.resource

Suite Setup         Set Up Transport System Suite
Suite Teardown      Close EC

Test Tags           iud    transport_system


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE_REFDD}
${END_DATE}         ${TEST_START_DATE_REFDD}
${NAV_BU}           ECP Norway
${PARENT_VALUE}     ECP Norway


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test transport system does not exist before inserting.
    [Tags]    clean-state
    Transport System Row Should Not Exist    ${TEST_CODE}
    Capture Step    transport_system_tc01_clean

TC02 Insert New Transport System
    [Documentation]    Insert a new transport system and confirm it appears in the BU-filtered list.
    [Tags]    insert
    Insert Transport System Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}    ${PARENT_VALUE}
    Transport System Row Should Exist    ${TEST_CODE}
    Transport System Should Exist In DB    ${TEST_CODE}
    Capture Step    transport_system_tc02_inserted

TC03 Update Transport System Name
    [Documentation]    Edit the transport system name and confirm the list reflects the change.
    [Tags]    update
    Update Transport System Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Transport System Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    transport_system_tc03_updated

TC04 Delete Transport System
    [Documentation]    Delete via End Date = Start Date and confirm the transport system is gone.
    [Tags]    delete    cleanup
    Delete Transport System    ${TEST_CODE}    ${END_DATE}
    Transport System Row Should Not Exist    ${TEST_CODE}
    Transport System Should Not Exist In DB    ${TEST_CODE}
    Capture Step    transport_system_tc04_deleted


*** Keywords ***
Set Up Transport System Suite
    [Documentation]    Generate a unique test code/name, then open the Transport System screen
    ...    with the ${NAV_BU} navigator context.
    Prepare IUD Object Data    AUTOTEST_TS_    Transport System
    Open Transport System Screen    ${NAV_BU}
