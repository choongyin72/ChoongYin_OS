*** Settings ***
Documentation       EC IUD Test - Nomination Point (Configuration > Assets > Dispatching Objects > Nomination Point).
...                 OV-GM behaviour: navigator Business Unit + GO gates the grid; insert
...                 references "Contract Name" = ECP Norway 3P Gas Purchase so the row is visible
...                 under the ECP Norway filter. DELETE = End Date = Start Date (ov_nomination_point).
...                 NEVER touch existing data: unique AUTOTEST_NP_<timestamp> code per run;
...                 the referenced parent objects are READ-ONLY seed data.

Resource            ../../../../pageobjects/Configuration/Assets/Dispatching_Objects/nomination_point_page.resource

Suite Setup         Set Up Nomination Point Suite
Suite Teardown      Close EC

Test Tags           iud    nomination_point


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE_REFDD}
${END_DATE}         ${TEST_START_DATE_REFDD}
${NAV_BU}           ECP Norway
${PARENT_VALUE}     ECP Norway 3P Gas Purchase


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test nomination point does not exist before inserting.
    [Tags]    clean-state
    Nomination Point Row Should Not Exist    ${TEST_CODE}
    Capture Step    nomination_point_tc01_clean

TC02 Insert New Nomination Point
    [Documentation]    Insert a new nomination point and confirm it appears in the BU-filtered list.
    [Tags]    insert
    Insert Nomination Point Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}    ${PARENT_VALUE}
    Nomination Point Row Should Exist    ${TEST_CODE}
    Nomination Point Should Exist In DB    ${TEST_CODE}
    Capture Step    nomination_point_tc02_inserted

TC03 Update Nomination Point Name
    [Documentation]    Edit the nomination point name and confirm the list reflects the change.
    [Tags]    update
    Update Nomination Point Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Nomination Point Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    nomination_point_tc03_updated

TC04 Delete Nomination Point
    [Documentation]    Delete via End Date = Start Date and confirm the nomination point is gone.
    [Tags]    delete    cleanup
    Delete Nomination Point    ${TEST_CODE}    ${END_DATE}
    Nomination Point Row Should Not Exist    ${TEST_CODE}
    Nomination Point Should Not Exist In DB    ${TEST_CODE}
    Capture Step    nomination_point_tc04_deleted


*** Keywords ***
Set Up Nomination Point Suite
    [Documentation]    Generate a unique test code/name, then open the Nomination Point screen
    ...    with the ${NAV_BU} navigator context.
    Prepare IUD Object Data    AUTOTEST_NP_    Nomination Point
    Open Nomination Point Screen    ${NAV_BU}
