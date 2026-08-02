*** Settings ***
Documentation       EC IUD Test - Property (Configuration > Assets > Data_Mapping_Objects).
...                 OV-GM (manage-object, groupmodel): grid filtered by the navigator cascade (PROVEN
...                 explicit values, not first-available).
...                 DELETE = End Date = Start Date (true delete in OV_PROPERTY). NEVER touch existing data;
...                 a unique AUTOTEST_PROP<timestamp> code is generated per run.

Resource            ../../../../pageobjects/Configuration/Assets/Data_Mapping_Objects/property_page.resource

Suite Setup         Set Up Property Suite
Suite Teardown      Close EC

Test Tags           iud    property


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       2003-01-01
${END_DATE}         2000-01-01


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test object does not exist before inserting.
    [Tags]    clean-state
    Property Row Should Not Exist    ${TEST_CODE}
    Capture Step    property_tc01_clean

TC02 Insert New Property
    [Documentation]    Insert under the navigator scope and confirm it lists.
    [Tags]    insert
    Insert Property Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Property Row Should Exist    ${TEST_CODE}
    Property Should Exist In DB    ${TEST_CODE}
    Capture Step    property_tc02_inserted

TC03 Update Property Name
    [Documentation]    Edit the name and confirm the list reflects the change.
    [Tags]    update
    Update Property Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Property Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    property_tc03_updated

TC04 Delete Property
    [Documentation]    Delete via End Date = Start Date and confirm it is gone.
    [Tags]    delete    cleanup
    Delete Property    ${TEST_CODE}    ${END_DATE}
    Property Row Should Not Exist    ${TEST_CODE}
    Property Should Not Exist In DB    ${TEST_CODE}
    Capture Step    property_tc04_deleted


*** Keywords ***
Set Up Property Suite
    [Documentation]    Generate a unique test code/name, open the screen, fill the navigator cascade
    ...    with PROVEN explicit values (not first-available).
    Prepare IUD Object Data    AUTOTEST_PROP    Property
    ${pu}=    Open Property Screen
    VAR    ${GM_PU}    ${pu}    scope=SUITE
