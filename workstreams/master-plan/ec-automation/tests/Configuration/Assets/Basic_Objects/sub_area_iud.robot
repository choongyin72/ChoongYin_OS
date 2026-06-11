*** Settings ***
Documentation       EC IUD Test - Sub Area (Configuration > Assets > Basic Objects > Sub Area).
...                 Manage-Object (OV, groupmodel) screen with cascading navigator
...                 (Production Unit -> Area). DELETE = End Date = Start Date (true delete
...                 in OV_SUB_AREA). NEVER touch existing data. Navigator values
...                 user-approved 2026-06-11.

Resource            ../../../../pageobjects/Configuration/Assets/Basic_Objects/sub_area_page.resource

Suite Setup         Set Up Sub Area Suite
Suite Teardown      Close EC

Test Tags           iud    sub-area


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
# 2003+: the Op PU / Op Area dropdowns only offer objects effective at the form's
# start date, and 'Production Unit' / 'Offshore area' start 2002-01-01
${START_DATE}       2003-01-01
${END_DATE}         2003-01-01
# cascading navigator context + Op fields of the test sub area - user-approved 2026-06-11
${NAV_PU}           Production Unit
${NAV_AREA}         Offshore area


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test sub area does not exist before inserting.
    [Tags]    clean-state
    Sub Area Row Should Not Exist    ${TEST_CODE}
    Capture Step    sub_area_tc01_clean

TC02 Insert New Sub Area
    [Documentation]    Insert a new sub area under ${NAV_PU} / ${NAV_AREA} and confirm it appears.
    [Tags]    insert
    Insert Sub Area Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}    ${NAV_PU}    ${NAV_AREA}
    Sub Area Row Should Exist    ${TEST_CODE}
    Sub Area Should Exist In DB    ${TEST_CODE}
    Capture Step    sub_area_tc02_inserted

TC03 Update Sub Area Name
    [Documentation]    Edit the sub area name and confirm the list reflects the change.
    [Tags]    update
    Update Sub Area Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Sub Area Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    sub_area_tc03_updated

TC04 Delete Sub Area
    [Documentation]    Delete via End Date = Start Date and confirm the sub area is gone.
    [Tags]    delete    cleanup
    Delete Sub Area    ${TEST_CODE}    ${END_DATE}
    Sub Area Row Should Not Exist    ${TEST_CODE}
    Sub Area Should Not Exist In DB    ${TEST_CODE}
    Capture Step    sub_area_tc04_deleted


*** Keywords ***
Set Up Sub Area Suite
    [Documentation]    Generate a unique test code/name, then open the Sub Area screen
    ...    with the approved cascading navigator context.
    ${code}    Generate Unique Code    AUTOTEST_SUBAREA_
    VAR    ${TEST_CODE}    ${code}    scope=SUITE
    VAR    ${OBJ_NAME}    Sub Area ${code}    scope=SUITE
    VAR    ${OBJ_NAME_UPD}    Sub Area ${code} UPD    scope=SUITE
    Open Sub Area Screen    ${NAV_PU}    ${NAV_AREA}
