*** Settings ***
Documentation       EC IUD Test - MMS Lease (Configuration > Assets > Commercial Objects > MMS Lease).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_MMS_LEASE).
...                 NEVER touch existing data. A unique AUTOTEST_MMSL_<timestamp> code is generated
...                 per run. Section Start Date 2003-01-01: reference dropdowns are
...                 effective-date-filtered (object start date acts as a version).

Resource            ../../../../pageobjects/Configuration/Assets/Commercial_Objects/mms_lease_page.resource

Suite Setup         Set Up MMS Lease Suite
Suite Teardown      Close EC

Test Tags           iud    mms-lease


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE_REFDD}
${END_DATE}         ${TEST_START_DATE_REFDD}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test mms lease does not exist before inserting.
    [Tags]    clean-state
    MMS Lease Row Should Not Exist    ${TEST_CODE}
    Capture Step    mms_lease_tc01_clean

TC02 Insert New MMS Lease
    [Documentation]    Insert a new mms lease and confirm it appears in the list.
    [Tags]    insert
    Insert MMS Lease Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    MMS Lease Row Should Exist    ${TEST_CODE}
    MMS Lease Should Exist In DB    ${TEST_CODE}
    Capture Step    mms_lease_tc02_inserted

TC03 Update MMS Lease Name
    [Documentation]    Edit the mms lease name and confirm the list reflects the change.
    [Tags]    update
    Update MMS Lease Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    MMS Lease Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    mms_lease_tc03_updated

TC04 Delete MMS Lease
    [Documentation]    Delete via End Date = Start Date and confirm the mms lease is gone.
    [Tags]    delete    cleanup
    Delete MMS Lease    ${TEST_CODE}    ${END_DATE}
    MMS Lease Row Should Not Exist    ${TEST_CODE}
    MMS Lease Should Not Exist In DB    ${TEST_CODE}
    Capture Step    mms_lease_tc04_deleted


*** Keywords ***
Set Up MMS Lease Suite
    [Documentation]    Generate a unique test code/name, then open the MMS Lease screen.
    Prepare IUD Object Data    AUTOTEST_MMSL_    MMS Lease
    Open MMS Lease Screen
