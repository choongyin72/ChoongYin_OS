*** Settings ***
Documentation       EC IUD Test - Tract (Configuration > Assets > Royalty Objects > Tract).
...                 OV-GM behaviour: navigator Unit Agreement + GO gates the grid; insert
...                 references "Unit Agreement" = Unit Agreement 1 so the row is visible under
...                 that filter. DELETE = End Date = Start Date (true delete in ov_tract).
...                 NEVER touch existing data: unique AUTOTEST_TR_<timestamp> code per run;
...                 the referenced Unit Agreement parents are READ-ONLY seed data.

Resource            ../../../../pageobjects/Configuration/Assets/Royalty_Objects/tract_page.resource

Suite Setup         Set Up Tract Suite
Suite Teardown      Close EC

Test Tags           iud    tract


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
# Unit Agreement parents are effective from 2010-01-01 (DB: ov_unit_agr.OBJECT_START_DATE),
# so the date-filtered insert parent dd only offers them at/after that date - use 2011-01-01.
${START_DATE}       2011-01-01
${END_DATE}         2011-01-01
${NAV_UA}           Unit Agreement 1
${PARENT_VALUE}     Unit Agreement 1


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test tract does not exist before inserting.
    [Tags]    clean-state
    Tract Row Should Not Exist    ${TEST_CODE}
    Capture Step    tract_tc01_clean

TC02 Insert New Tract
    [Documentation]    Insert a new tract and confirm it appears in the UA-filtered list.
    [Tags]    insert
    Insert Tract Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}    ${PARENT_VALUE}
    Tract Row Should Exist    ${TEST_CODE}
    Tract Should Exist In DB    ${TEST_CODE}
    Capture Step    tract_tc02_inserted

TC03 Update Tract Name
    [Documentation]    Edit the tract name and confirm the list reflects the change.
    [Tags]    update
    Update Tract Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Tract Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    tract_tc03_updated

TC04 Delete Tract
    [Documentation]    Delete via End Date = Start Date and confirm the tract is gone.
    [Tags]    delete    cleanup
    Delete Tract    ${TEST_CODE}    ${END_DATE}
    Tract Row Should Not Exist    ${TEST_CODE}
    Tract Should Not Exist In DB    ${TEST_CODE}
    Capture Step    tract_tc04_deleted


*** Keywords ***
Set Up Tract Suite
    [Documentation]    Generate a unique test code/name, then open the Tract screen
    ...    with the ${NAV_UA} navigator context.
    Prepare IUD Object Data    AUTOTEST_TR_    Tract
    Open Tract Screen    ${NAV_UA}
