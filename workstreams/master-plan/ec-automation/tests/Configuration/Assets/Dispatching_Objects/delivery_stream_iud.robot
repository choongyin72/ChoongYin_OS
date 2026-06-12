*** Settings ***
Documentation       EC IUD Test - Delivery Stream (Configuration > Assets > Dispatching Objects > Delivery Stream).
...                 OV-GM behaviour: navigator Business Unit + GO gates the grid; insert
...                 references "Business Unit" = ECP Norway so the row is visible
...                 under the ECP Norway filter. DELETE = End Date = Start Date (ov_delivery_stream).
...                 NEVER touch existing data: unique AUTOTEST_DS_<timestamp> code per run;
...                 the referenced parent objects are READ-ONLY seed data.

Resource            ../../../../pageobjects/Configuration/Assets/Dispatching_Objects/delivery_stream_page.resource

Suite Setup         Set Up Delivery Stream Suite
Suite Teardown      Close EC

Test Tags           iud    delivery_stream


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE_REFDD}
${END_DATE}         ${TEST_START_DATE_REFDD}
${NAV_BU}           ECP Norway
${PARENT_VALUE}     ECP Norway
# Entry Delivery Point = an ECP Norway DP — THE link that makes the row visible in the
# BU-filtered grid (the stream's own Business Unit column is NOT the grid filter)
${ENTRY_DP}         Any Safe Port in Norway


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test delivery stream does not exist before inserting.
    [Tags]    clean-state
    Delivery Stream Row Should Not Exist    ${TEST_CODE}
    Capture Step    delivery_stream_tc01_clean

TC02 Insert New Delivery Stream
    [Documentation]    Insert a new delivery stream and confirm it appears in the BU-filtered list.
    [Tags]    insert
    Insert Delivery Stream Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}    ${PARENT_VALUE}    ${ENTRY_DP}
    Delivery Stream Row Should Exist    ${TEST_CODE}
    Delivery Stream Should Exist In DB    ${TEST_CODE}
    Capture Step    delivery_stream_tc02_inserted

TC03 Update Delivery Stream Name
    [Documentation]    Edit the delivery stream name and confirm the list reflects the change.
    [Tags]    update
    Update Delivery Stream Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Delivery Stream Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    delivery_stream_tc03_updated

TC04 Delete Delivery Stream
    [Documentation]    Delete via End Date = Start Date and confirm the delivery stream is gone.
    [Tags]    delete    cleanup
    Delete Delivery Stream    ${TEST_CODE}    ${END_DATE}
    Delivery Stream Row Should Not Exist    ${TEST_CODE}
    Delivery Stream Should Not Exist In DB    ${TEST_CODE}
    Capture Step    delivery_stream_tc04_deleted


*** Keywords ***
Set Up Delivery Stream Suite
    [Documentation]    Generate a unique test code/name, then open the Delivery Stream screen
    ...    with the ${NAV_BU} navigator context.
    Prepare IUD Object Data    AUTOTEST_DS_    Delivery Stream
    Open Delivery Stream Screen    ${NAV_BU}
