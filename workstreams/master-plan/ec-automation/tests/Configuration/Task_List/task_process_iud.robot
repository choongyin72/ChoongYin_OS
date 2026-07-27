*** Settings ***
Documentation       EC IUD Test - Task Process (Configuration > Task_List > Task Process, CO.0191).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_TASK_PROCESS).
...                 Layered: this test -> task_process_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Unique AUTOTEST_TP_<timestamp> code per run.

Resource            ../../../pageobjects/Configuration/Task_List/task_process_page.resource

Suite Setup         Set Up Task Process Suite
Suite Teardown      Close EC

Test Tags           iud    task_process


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test task_process does not exist before inserting.
    [Tags]    clean-state
    Task Process Row Should Not Exist    ${TEST_CODE}
    Capture Step    task_process_tc01_clean

TC02 Insert New Task Process
    [Documentation]    Insert a new task_process; confirm in list + DB (OV_TASK_PROCESS).
    [Tags]    insert
    Insert Task Process Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Task Process Row Should Exist    ${TEST_CODE}
    Task Process Should Exist In DB    ${TEST_CODE}
    Capture Step    task_process_tc02_inserted

TC03 Update Task Process
    [Documentation]    Edit Name; confirm in list + DB ground truth.
    [Tags]    update
    Update Task Process Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Task Process Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Field Should Equal In View    OV_TASK_PROCESS    ${TEST_CODE}    NAME    ${OBJ_NAME_UPD}
    Capture Step    task_process_tc03_updated

TC04 Delete Task Process
    [Documentation]    Delete via End Date = Start Date; confirm gone from list + DB.
    [Tags]    delete    cleanup
    Delete Task Process    ${TEST_CODE}    ${END_DATE}
    Task Process Row Should Not Exist    ${TEST_CODE}
    Task Process Should Not Exist In DB    ${TEST_CODE}
    Capture Step    task_process_tc04_deleted


*** Keywords ***
Set Up Task Process Suite
    [Documentation]    Generate a unique test code/name, then open the Task Process screen.
    Prepare IUD Object Data    AUTOTEST_TP_    Task Process
    Open Task Process Screen
