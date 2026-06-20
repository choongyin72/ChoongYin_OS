*** Settings ***
Documentation       EC IUD Test - Analysis Point (Configuration > Assets > Laboratory Objects > Analysis Point).
...                 OV-GM (groupmodel, 3-level cascade): navigator PU → Area → Facility Class 1 + GO gates
...                 the grid; insert sets Op PU/Area/Facility = the same scope so the row is visible, plus a
...                 mandatory Analysis Point Type. DELETE = End Date = Start Date (ov_analysis_point).
...                 NEVER touch existing data: unique AUTOTEST_AP_<timestamp> code per run; the referenced
...                 PU/Area/Facility + Type are READ-ONLY seed data.

Resource            ../../../../pageobjects/Configuration/Assets/Laboratory_Objects/analysis_point_page.resource

Suite Setup         Set Up Analysis Point Suite
Suite Teardown      Close EC

Test Tags           iud    analysis_point


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE_REFDD}
${END_DATE}         ${TEST_START_DATE_REFDD}
${NAV_PU}           P1 Production Unit
${NAV_AREA}         P1 Area
${NAV_FACILITY}     P1 Facility 1


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test analysis point does not exist before inserting.
    [Tags]    clean-state
    Analysis Point Row Should Not Exist    ${TEST_CODE}
    Capture Step    analysis_point_tc01_clean

TC02 Insert New Analysis Point
    [Documentation]    Insert a new analysis point and confirm it appears in the scoped list and the DB.
    [Tags]    insert
    Insert Analysis Point Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}    ${NAV_PU}    ${NAV_AREA}    ${NAV_FACILITY}
    Analysis Point Row Should Exist    ${TEST_CODE}
    Analysis Point Should Exist In DB    ${TEST_CODE}
    Capture Step    analysis_point_tc02_inserted

TC03 Update Analysis Point Name
    [Documentation]    Edit the analysis point name and confirm the list reflects the change.
    [Tags]    update
    Update Analysis Point Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Analysis Point Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    analysis_point_tc03_updated

TC04 Delete Analysis Point
    [Documentation]    Delete via End Date = Start Date and confirm the analysis point is gone (UI + DB).
    [Tags]    delete    cleanup
    Delete Analysis Point    ${TEST_CODE}    ${END_DATE}
    Analysis Point Row Should Not Exist    ${TEST_CODE}
    Analysis Point Should Not Exist In DB    ${TEST_CODE}
    Capture Step    analysis_point_tc04_deleted


*** Keywords ***
Set Up Analysis Point Suite
    [Documentation]    Generate a unique test code/name, then open the Analysis Point screen with the
    ...    P1 PU/Area/Facility navigator scope.
    Prepare IUD Object Data    AUTOTEST_AP_    Analysis Point
    Open Analysis Point Screen    ${NAV_PU}    ${NAV_AREA}    ${NAV_FACILITY}
