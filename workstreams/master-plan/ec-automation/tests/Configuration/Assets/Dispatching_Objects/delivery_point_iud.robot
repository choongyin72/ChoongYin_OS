*** Settings ***
Documentation       EC IUD Test - Delivery Point (Configuration > Assets > Dispatching Objects > Delivery Point).
...                 OV-GM behaviour: navigator Business Unit + GO gates the grid; insert
...                 references "Business Unit Name" = ECP Norway so the row is visible
...                 under the ECP Norway filter. DELETE = End Date = Start Date (ov_delivery_point).
...                 NEVER touch existing data: unique AUTOTEST_DP_<timestamp> code per run;
...                 the referenced parent objects are READ-ONLY seed data.

Resource            ../../../../pageobjects/Configuration/Assets/Dispatching_Objects/delivery_point_page.resource

Suite Setup         Set Up Delivery Point Suite
Suite Teardown      Close EC

Test Tags           iud    delivery_point


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
    [Documentation]    Confirm the (freshly generated) test delivery point does not exist before inserting.
    [Tags]    clean-state
    Delivery Point Row Should Not Exist    ${TEST_CODE}
    Capture Step    delivery_point_tc01_clean

TC02 Insert New Delivery Point
    [Documentation]    Insert a new delivery point and confirm it appears in the BU-filtered list.
    [Tags]    insert
    Insert Delivery Point Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}    ${PARENT_VALUE}
    Delivery Point Row Should Exist    ${TEST_CODE}
    Delivery Point Should Exist In DB    ${TEST_CODE}
    Capture Step    delivery_point_tc02_inserted

TC03 Update Delivery Point Name
    [Documentation]    Edit the delivery point name and confirm the list reflects the change.
    [Tags]    update
    Update Delivery Point Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Delivery Point Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    delivery_point_tc03_updated

TC04 Delete Delivery Point
    [Documentation]    Delete via End Date = Start Date and confirm the delivery point is gone.
    [Tags]    delete    cleanup
    Delete Delivery Point    ${TEST_CODE}    ${END_DATE}
    Delivery Point Row Should Not Exist    ${TEST_CODE}
    Delivery Point Should Not Exist In DB    ${TEST_CODE}
    Capture Step    delivery_point_tc04_deleted


*** Keywords ***
Set Up Delivery Point Suite
    [Documentation]    Generate a unique test code/name, then open the Delivery Point screen
    ...    with the ${NAV_BU} navigator context.
    Prepare IUD Object Data    AUTOTEST_DP_    Delivery Point
    Open Delivery Point Screen    ${NAV_BU}
