*** Settings ***
Documentation       EC IUD Test - Transport Zone (Configuration > Assets > Dispatching Objects > Transport Zone).
...                 OV-GM behaviour: navigator Business Unit + GO gates the grid; insert
...                 references "Transport System Name" = TS5 Transport System so the row is visible
...                 under the TS5 BU filter. DELETE = End Date = Start Date (ov_transport_zone).
...                 NEVER touch existing data: unique AUTOTEST_TZ_<timestamp> code per run;
...                 the referenced parent objects are READ-ONLY seed data.

Resource            ../../../../pageobjects/Configuration/Assets/Dispatching_Objects/transport_zone_page.resource

Suite Setup         Set Up Transport Zone Suite
Suite Teardown      Close EC

Test Tags           iud    transport_zone


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE_REFDD}
${END_DATE}         ${TEST_START_DATE_REFDD}
${NAV_BU}           TS5 BU
${PARENT_VALUE}     TS5 Transport System


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test transport zone does not exist before inserting.
    [Tags]    clean-state
    Transport Zone Row Should Not Exist    ${TEST_CODE}
    Capture Step    transport_zone_tc01_clean

TC02 Insert New Transport Zone
    [Documentation]    Insert a new transport zone and confirm it appears in the BU-filtered list.
    [Tags]    insert
    Insert Transport Zone Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}    ${PARENT_VALUE}
    Transport Zone Row Should Exist    ${TEST_CODE}
    Transport Zone Should Exist In DB    ${TEST_CODE}
    Capture Step    transport_zone_tc02_inserted

TC03 Update Transport Zone Name
    [Documentation]    Edit the transport zone name and confirm the list reflects the change.
    [Tags]    update
    Update Transport Zone Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Transport Zone Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    transport_zone_tc03_updated

TC04 Delete Transport Zone
    [Documentation]    Delete via End Date = Start Date and confirm the transport zone is gone.
    [Tags]    delete    cleanup
    Delete Transport Zone    ${TEST_CODE}    ${END_DATE}
    Transport Zone Row Should Not Exist    ${TEST_CODE}
    Transport Zone Should Not Exist In DB    ${TEST_CODE}
    Capture Step    transport_zone_tc04_deleted


*** Keywords ***
Set Up Transport Zone Suite
    [Documentation]    Generate a unique test code/name, then open the Transport Zone screen
    ...    with the ${NAV_BU} navigator context.
    Prepare IUD Object Data    AUTOTEST_TZ_    Transport Zone
    Open Transport Zone Screen    ${NAV_BU}
