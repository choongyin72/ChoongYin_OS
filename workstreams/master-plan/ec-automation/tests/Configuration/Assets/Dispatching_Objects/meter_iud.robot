*** Settings ***
Documentation       EC IUD Test - Meter (Configuration > Assets > Dispatching Objects).
...                 OV-GM (BU-gated) with the POPUP-PICKER pattern: insert needs Meter
...                 Type (dd) + Delivery Point (EC object popup, the new T1 gesture).
...                 The DP belongs to the nav BU so the row is grid-visible. DELETE =
...                 End Date = Start Date (ov_meter). Unique AUTOTEST_MTR_<ts> per run.

Resource            ../../../../pageobjects/Configuration/Assets/Dispatching_Objects/meter_page.resource

Suite Setup         Set Up Meter Suite
Suite Teardown      Close EC

Test Tags           iud    meter


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE_REFDD}
${END_DATE}         ${TEST_START_DATE_REFDD}
${NAV_BU}           ECP Norway
${METER_TYPE}       Entry
${DELIVERY_POINT}   300005 PG Hoogerheide


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test meter does not exist before inserting.
    [Tags]    clean-state
    Meter Row Should Not Exist    ${TEST_CODE}
    Capture Step    meter_tc01_clean

TC02 Insert New Meter
    [Documentation]    Insert a new meter (dd + popup pick) and confirm grid + DB.
    [Tags]    insert
    Insert Meter Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}    ${METER_TYPE}    ${DELIVERY_POINT}
    Meter Row Should Exist    ${TEST_CODE}
    Meter Should Exist In DB    ${TEST_CODE}
    Capture Step    meter_tc02_inserted

TC03 Update Meter Name
    [Documentation]    Edit the meter name and confirm the list reflects the change.
    [Tags]    update
    Update Meter Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Meter Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    meter_tc03_updated

TC04 Delete Meter
    [Documentation]    Delete via End Date = Start Date and confirm the meter is gone.
    [Tags]    delete    cleanup
    Delete Meter    ${TEST_CODE}    ${END_DATE}
    Meter Row Should Not Exist    ${TEST_CODE}
    Meter Should Not Exist In DB    ${TEST_CODE}
    Capture Step    meter_tc04_deleted


*** Keywords ***
Set Up Meter Suite
    [Documentation]    Generate a unique test code/name, then open the Meter screen with
    ...    the ${NAV_BU} navigator context (gates both the grid and the DP popup list).
    Prepare IUD Object Data    AUTOTEST_MTR_    Meter
    Open Meter Screen    ${NAV_BU}
