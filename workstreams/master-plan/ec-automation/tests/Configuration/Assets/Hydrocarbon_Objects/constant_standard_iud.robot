*** Settings ***
Documentation       EC IUD Test - Constant Standard (Configuration > Assets > Hydrocarbon_Objects).
...                 TV-style inline-editable grid, but date-effective (VERSIONED) underneath -
...                 DELETE = End Date = Start Date in the inline cell (true close in
...                 OV_CONSTANT_STANDARD). NEVER touch existing data; a unique
...                 AUTOTEST_CS_<timestamp> code is generated per run.

Resource            ../../../../pageobjects/Configuration/Assets/Hydrocarbon_Objects/constant_standard_page.resource

Suite Setup         Set Up Constant Standard Suite
Suite Teardown      Close EC

Test Tags           iud    constant_standard


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       2000-01-01


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test object does not exist before inserting.
    [Tags]    clean-state
    Constant Standard Row Should Not Exist    ${TEST_CODE}
    Capture Step    constant_standard_tc01_clean

TC02 Insert New Constant Standard
    [Documentation]    Insert via the real (title-case) menu item; fill mandatory cells incl.
    ...    Daytime; confirm it lists and persists.
    [Tags]    insert
    Insert Constant Standard Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Constant Standard Row Should Exist    ${TEST_CODE}
    Constant Standard Should Exist In DB    ${TEST_CODE}
    Capture Step    constant_standard_tc02_inserted

TC03 Update Constant Standard Name
    [Documentation]    Edit the Name cell and confirm the grid reflects the change.
    [Tags]    update
    Update Constant Standard Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Constant Standard Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    constant_standard_tc03_updated

TC04 Delete Constant Standard
    [Documentation]    Close via End Date = Start Date (this class IS date-effective) and confirm
    ...    it is gone from the DB view.
    [Tags]    delete    cleanup
    Delete Constant Standard    ${TEST_CODE}    ${START_DATE}
    Constant Standard Should Not Exist In DB    ${TEST_CODE}
    Capture Step    constant_standard_tc04_deleted


*** Keywords ***
Set Up Constant Standard Suite
    [Documentation]    Generate a unique test code/name, open the screen.
    Prepare IUD Object Data    AUTOTEST_CS_    Constant Standard
    Open Constant Standard Screen
