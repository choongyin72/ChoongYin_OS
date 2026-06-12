*** Settings ***
Documentation       EC IUD Test - Area (Configuration > Assets > Basic Objects > Area).
...                 Manage-Object (OV, groupmodel) screen: grid is filtered by the navigator
...                 Production Unit. DELETE = End Date = Start Date (true delete in OV_AREA).
...                 NEVER touch existing data. A unique AUTOTEST_AREA_<timestamp> code is
...                 generated per run. Navigator/Op PU value user-approved 2026-06-11.

Resource            ../../../../pageobjects/Configuration/Assets/Basic_Objects/area_page.resource

Suite Setup         Set Up Area Suite
Suite Teardown      Close EC

Test Tags           iud    area


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
# 2003+: the Op Production Unit dropdown only offers PUs effective at the form's
# start date, and 'Production Unit' (user-approved context) starts 2002-01-01
${START_DATE}       ${TEST_START_DATE_REFDD}
${END_DATE}         ${TEST_START_DATE_REFDD}
# navigator context + Op Production Unit of the test area - user-approved 2026-06-11
${NAV_PU}           Production Unit


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test area does not exist before inserting.
    [Tags]    clean-state
    Area Row Should Not Exist    ${TEST_CODE}
    Capture Step    area_tc01_clean

TC02 Insert New Area
    [Documentation]    Insert a new area under ${NAV_PU} and confirm it appears in the list.
    [Tags]    insert
    Insert Area Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}    ${NAV_PU}
    Area Row Should Exist    ${TEST_CODE}
    Area Should Exist In DB    ${TEST_CODE}
    Capture Step    area_tc02_inserted

TC03 Update Area Name
    [Documentation]    Edit the area name and confirm the list reflects the change.
    [Tags]    update
    Update Area Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Area Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    area_tc03_updated

TC04 Delete Area
    [Documentation]    Delete via End Date = Start Date and confirm the area is gone.
    [Tags]    delete    cleanup
    Delete Area    ${TEST_CODE}    ${END_DATE}
    Area Row Should Not Exist    ${TEST_CODE}
    Area Should Not Exist In DB    ${TEST_CODE}
    Capture Step    area_tc04_deleted


*** Keywords ***
Set Up Area Suite
    [Documentation]    Generate a unique test code/name, then open the Area screen
    ...    with the approved Production Unit navigator context.
    Prepare IUD Object Data    AUTOTEST_AREA_    Area
    Open Area Screen    ${NAV_PU}
