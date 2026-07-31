*** Settings ***
Documentation       EC IUD Test - Report Group (Configuration > Assets > Facility_Objects).
...                 OV-GM (manage-object, groupmodel): grid filtered by the navigator cascade.
...                 DELETE = End Date = Start Date (true delete in OV_REPORT_GROUP). NEVER touch existing data;
...                 a unique AUTOTEST_RG<timestamp> code is generated per run.

Resource            ../../../../pageobjects/Configuration/Assets/Facility_Objects/report_group_page.resource

Suite Setup         Set Up Report Group Suite
Suite Teardown      Close EC

Test Tags           iud    report_group


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
    Report Group Row Should Not Exist    ${TEST_CODE}
    Capture Step    report_group_tc01_clean

TC02 Insert New Report Group
    [Documentation]    Insert under the navigator scope and confirm it lists.
    [Tags]    insert
    Insert Report Group Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Report Group Row Should Exist    ${TEST_CODE}
    Report Group Should Exist In DB    ${TEST_CODE}
    Capture Step    report_group_tc02_inserted

TC03 Update Report Group Name
    [Documentation]    Edit the name and confirm the list reflects the change.
    [Tags]    update
    Update Report Group Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Report Group Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    report_group_tc03_updated

TC04 Delete Report Group
    [Documentation]    Delete via End Date = Start Date and confirm it is gone.
    [Tags]    delete    cleanup
    Delete Report Group    ${TEST_CODE}    ${END_DATE}
    Report Group Row Should Not Exist    ${TEST_CODE}
    Report Group Should Not Exist In DB    ${TEST_CODE}
    Capture Step    report_group_tc04_deleted


*** Keywords ***
Set Up Report Group Suite
    [Documentation]    Generate a unique test code/name, open the screen, GO (date-only navigator).
    Prepare IUD Object Data    AUTOTEST_RG    Reporting Group
    Open Report Group Screen
