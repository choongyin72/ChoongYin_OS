*** Settings ***
Documentation       EC IUD Test - Collection Point (Configuration > Assets > Facility_Objects).
...                 OV-GM (manage-object, groupmodel): grid filtered by the navigator cascade.
...                 DELETE = End Date = Start Date (true delete in OV_COLLECTION_POINT). NEVER touch existing data;
...                 a unique AUTOTEST_CP<timestamp> code is generated per run.

Resource            ../../../../pageobjects/Configuration/Assets/Facility_Objects/collection_point_page.resource

Suite Setup         Set Up Collection Point Suite
Suite Teardown      Close EC

Test Tags           iud    collection_point


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
    Collection Point Row Should Not Exist    ${TEST_CODE}
    Capture Step    collection_point_tc01_clean

TC02 Insert New Collection Point
    [Documentation]    Insert under the navigator scope and confirm it lists.
    [Tags]    insert
    Insert Collection Point Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Collection Point Row Should Exist    ${TEST_CODE}
    Collection Point Should Exist In DB    ${TEST_CODE}
    Capture Step    collection_point_tc02_inserted

TC03 Update Collection Point Name
    [Documentation]    Edit the name and confirm the list reflects the change.
    [Tags]    update
    Update Collection Point Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Collection Point Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    collection_point_tc03_updated

TC04 Delete Collection Point
    [Documentation]    Delete via End Date = Start Date and confirm it is gone.
    [Tags]    delete    cleanup
    Delete Collection Point    ${TEST_CODE}    ${END_DATE}
    Collection Point Row Should Not Exist    ${TEST_CODE}
    Collection Point Should Not Exist In DB    ${TEST_CODE}
    Capture Step    collection_point_tc04_deleted


*** Keywords ***
Set Up Collection Point Suite
    [Documentation]    Generate a unique test code/name, open the screen, fill the navigator cascade.
    Prepare IUD Object Data    AUTOTEST_CP    Collection Point
    ${pu}=    Open Collection Point Screen
    VAR    ${GM_PU}    ${pu}    scope=SUITE
