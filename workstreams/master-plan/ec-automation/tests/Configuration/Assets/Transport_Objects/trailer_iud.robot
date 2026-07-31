*** Settings ***
Documentation       EC IUD Test - Trailer (Configuration > Assets > Transport_Objects).
...                 OV-GM (manage-object, groupmodel): grid filtered by the navigator cascade.
...                 DELETE = End Date = Start Date (true delete in OV_TRAILER). NEVER touch existing data;
...                 a unique AUTOTEST_TR_<timestamp> code is generated per run.

Resource            ../../../../pageobjects/Configuration/Assets/Transport_Objects/trailer_page.resource

Suite Setup         Set Up Trailer Suite
Suite Teardown      Close EC

Test Tags           iud    trailer


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       2000-01-01
${END_DATE}         2000-01-01


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test object does not exist before inserting.
    [Tags]    clean-state
    Trailer Row Should Not Exist    ${TEST_CODE}
    Capture Step    trailer_tc01_clean

TC02 Insert New Trailer
    [Documentation]    Insert under the navigator scope and confirm it lists.
    [Tags]    insert
    Insert Trailer Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Trailer Row Should Exist    ${TEST_CODE}
    Trailer Should Exist In DB    ${TEST_CODE}
    Capture Step    trailer_tc02_inserted

TC03 Update Trailer Name
    [Documentation]    Edit the name and confirm the list reflects the change.
    [Tags]    update
    Update Trailer Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Trailer Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    trailer_tc03_updated

TC04 Delete Trailer
    [Documentation]    Delete via End Date = Start Date and confirm it is gone.
    [Tags]    delete    cleanup
    Delete Trailer    ${TEST_CODE}    ${END_DATE}
    Trailer Row Should Not Exist    ${TEST_CODE}
    Trailer Should Not Exist In DB    ${TEST_CODE}
    Capture Step    trailer_tc04_deleted


*** Keywords ***
Set Up Trailer Suite
    [Documentation]    Generate a unique test code/name, open the screen, GO (date-only navigator).
    Prepare IUD Object Data    AUTOTEST_TR_    Trailer
    Open Trailer Screen
