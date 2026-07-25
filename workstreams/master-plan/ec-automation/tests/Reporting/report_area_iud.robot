*** Settings ***
Documentation       EC IUD Test - Report Area (Reporting > Report Area, RP.0017).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_REPORT_AREA).
...                 Layered: this test -> report_area_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Unique AUTOTEST_RPTA_<timestamp> code per run.

Resource            ../../pageobjects/Reporting/report_area_page.resource

Suite Setup         Set Up Report Area Suite
Suite Teardown      Close EC

Test Tags           iud    report_area


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test report area does not exist before inserting.
    [Tags]    clean-state
    Report Area Row Should Not Exist    ${TEST_CODE}
    Capture Step    report_area_tc01_clean

TC02 Insert New Report Area
    [Documentation]    Insert a new report area; confirm in list + DB (OV_REPORT_AREA).
    [Tags]    insert
    Insert Report Area Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Report Area Row Should Exist    ${TEST_CODE}
    Report Area Should Exist In DB    ${TEST_CODE}
    Capture Step    report_area_tc02_inserted

TC03 Update Report Area
    [Documentation]    Edit Name; confirm in list + DB ground truth.
    [Tags]    update
    Update Report Area Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Report Area Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Field Should Equal In View    OV_REPORT_AREA    ${TEST_CODE}    NAME    ${OBJ_NAME_UPD}
    Capture Step    report_area_tc03_updated

TC04 Delete Report Area
    [Documentation]    Delete via End Date = Start Date; confirm gone from list + DB.
    [Tags]    delete    cleanup
    Delete Report Area    ${TEST_CODE}    ${END_DATE}
    Report Area Row Should Not Exist    ${TEST_CODE}
    Report Area Should Not Exist In DB    ${TEST_CODE}
    Capture Step    report_area_tc04_deleted


*** Keywords ***
Set Up Report Area Suite
    [Documentation]    Generate a unique test code/name, then open the Report Area screen.
    Prepare IUD Object Data    AUTOTEST_RPTA_    Report Area
    Open Report Area Screen
