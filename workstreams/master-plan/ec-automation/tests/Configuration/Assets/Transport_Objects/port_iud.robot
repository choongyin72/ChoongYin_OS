*** Settings ***
Documentation       EC IUD Test - Port (Configuration > Assets > Transport Objects > Port, CO.2003).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_PORT).
...                 Layered: this test -> port_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Unique AUTOTEST_PORT_<timestamp> code per run.

Resource            ../../../../pageobjects/Configuration/Assets/Transport_Objects/port_page.resource

Suite Setup         Set Up Port Suite
Suite Teardown      Close EC

Test Tags           iud    port


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test port does not exist before inserting.
    [Tags]    clean-state
    Port Row Should Not Exist    ${TEST_CODE}
    Capture Step    port_tc01_clean

TC02 Insert New Port
    [Documentation]    Insert a new port; confirm in list + DB (OV_PORT).
    [Tags]    insert
    Insert Port Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Port Row Should Exist    ${TEST_CODE}
    Port Should Exist In DB    ${TEST_CODE}
    Capture Step    port_tc02_inserted

TC03 Update Port
    [Documentation]    Edit Name; confirm in list + DB ground truth.
    [Tags]    update
    Update Port Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Port Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Field Should Equal In View    OV_PORT    ${TEST_CODE}    NAME    ${OBJ_NAME_UPD}
    Capture Step    port_tc03_updated

TC04 Delete Port
    [Documentation]    Delete via End Date = Start Date; confirm gone from list + DB.
    [Tags]    delete    cleanup
    Delete Port    ${TEST_CODE}    ${END_DATE}
    Port Row Should Not Exist    ${TEST_CODE}
    Port Should Not Exist In DB    ${TEST_CODE}
    Capture Step    port_tc04_deleted


*** Keywords ***
Set Up Port Suite
    [Documentation]    Generate a unique test code/name, then open the Port screen.
    Prepare IUD Object Data    AUTOTEST_PORT_    Port
    Open Port Screen
