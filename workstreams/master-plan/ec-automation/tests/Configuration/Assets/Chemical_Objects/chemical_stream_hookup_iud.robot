*** Settings ***
Documentation       EC IUD Test - Chemical Stream Hookup (Configuration > Assets > Chemical_Objects).
...                 OV-GM (manage-object, groupmodel): grid filtered by the navigator cascade.
...                 DELETE = End Date = Start Date (true delete in OV_CHEM_STRM_HOOKUP). NEVER touch existing data;
...                 a unique AUTOTEST_CSH_<timestamp> code is generated per run.

Resource            ../../../../pageobjects/Configuration/Assets/Chemical_Objects/chemical_stream_hookup_page.resource

Suite Setup         Set Up Chemical Stream Hookup Suite
Suite Teardown      Close EC

Test Tags           iud    chemical_stream_hookup


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
    Chemical Stream Hookup Row Should Not Exist    ${TEST_CODE}
    Capture Step    chemical_stream_hookup_tc01_clean

TC02 Insert New Chemical Stream Hookup
    [Documentation]    Insert under the navigator scope and confirm it lists.
    [Tags]    insert
    Insert Chemical Stream Hookup Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Chemical Stream Hookup Row Should Exist    ${TEST_CODE}
    Chemical Stream Hookup Should Exist In DB    ${TEST_CODE}
    Capture Step    chemical_stream_hookup_tc02_inserted

TC03 Update Chemical Stream Hookup Name
    [Documentation]    Edit the name and confirm the list reflects the change.
    [Tags]    update
    Update Chemical Stream Hookup Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Chemical Stream Hookup Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    chemical_stream_hookup_tc03_updated

TC04 Delete Chemical Stream Hookup
    [Documentation]    Delete via End Date = Start Date and confirm it is gone.
    [Tags]    delete    cleanup
    Delete Chemical Stream Hookup    ${TEST_CODE}    ${END_DATE}
    Chemical Stream Hookup Row Should Not Exist    ${TEST_CODE}
    Chemical Stream Hookup Should Not Exist In DB    ${TEST_CODE}
    Capture Step    chemical_stream_hookup_tc04_deleted


*** Keywords ***
Set Up Chemical Stream Hookup Suite
    [Documentation]    Generate a unique test code/name, open the screen, fill the navigator cascade.
    Prepare IUD Object Data    AUTOTEST_CSH_    Chemical Stream Hookup
    ${pu}=    Open Chemical Stream Hookup Screen
    VAR    ${GM_PU}    ${pu}    scope=SUITE
