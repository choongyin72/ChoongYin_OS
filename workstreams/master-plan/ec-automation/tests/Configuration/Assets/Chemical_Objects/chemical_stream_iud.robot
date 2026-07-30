*** Settings ***
Documentation       EC IUD Test - Chemical Stream (Configuration > Assets > Chemical_Objects).
...                 OV-GM with a mandatory From Connection POPUP (stream_node_ref_popup: inner
...                 Object Type CHEM_TANK + inner GO + grid manage_object_nav_nav:form:T_data -
...                 screen-local picker). Navigator = SPECIFIC P1 values (popup source empty under
...                 first-available AS1 - the original park). DELETE = End Date = Start Date (true
...                 delete in OV_CHEM_STREAM). NEVER touch existing data; unique
...                 AUTOTEST_CHS_<timestamp> code per run. Start Date 2020-01-01.

Resource            ../../../../pageobjects/Configuration/Assets/Chemical_Objects/chemical_stream_page.resource

Suite Setup         Set Up Chemical Stream Suite
Suite Teardown      Close EC

Test Tags           iud    chemical-stream


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       2020-01-01
${END_DATE}         2020-01-01


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test object does not exist before inserting.
    [Tags]    clean-state
    Chemical Stream Row Should Not Exist    ${TEST_CODE}
    Capture Step    chemical_stream_tc01_clean

TC02 Insert New Chemical Stream
    [Documentation]    Insert under the P1 navigator scope (incl. the From Connection popup) and confirm it lists.
    [Tags]    insert
    Insert Chemical Stream Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Chemical Stream Row Should Exist    ${TEST_CODE}
    Chemical Stream Should Exist In DB    ${TEST_CODE}
    Capture Step    chemical_stream_tc02_inserted

TC03 Update Chemical Stream Name
    [Documentation]    Edit the name and confirm the list reflects the change.
    [Tags]    update
    Update Chemical Stream Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Chemical Stream Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    chemical_stream_tc03_updated

TC04 Delete Chemical Stream
    [Documentation]    Delete via End Date = Start Date and confirm it is gone.
    [Tags]    delete    cleanup
    Delete Chemical Stream    ${TEST_CODE}    ${END_DATE}
    Chemical Stream Row Should Not Exist    ${TEST_CODE}
    Chemical Stream Should Not Exist In DB    ${TEST_CODE}
    Capture Step    chemical_stream_tc04_deleted


*** Keywords ***
Set Up Chemical Stream Suite
    [Documentation]    Generate a unique test code/name, open the screen, apply the P1 nav scope.
    Prepare IUD Object Data    AUTOTEST_CHS_    Chemical Stream
    Open Chemical Stream Screen
