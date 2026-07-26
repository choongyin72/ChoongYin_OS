*** Settings ***
Documentation       EC IUD Test - Split Item Other (Configuration > Assets > Revenue_Split_Keys > Split Item Other, CD.0017).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_SPLIT_ITEM_OTHER).
...                 Layered: this test -> split_item_other_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Unique AUTOTEST_SIO_<timestamp> code per run.

Resource            ../../../../pageobjects/Configuration/Assets/Revenue_Split_Keys/split_item_other_page.resource

Suite Setup         Set Up Split Item Other Suite
Suite Teardown      Close EC

Test Tags           iud    split_item_other


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       ${TEST_START_DATE}
${END_DATE}         ${TEST_START_DATE}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test split_item_other does not exist before inserting.
    [Tags]    clean-state
    Split Item Other Row Should Not Exist    ${TEST_CODE}
    Capture Step    split_item_other_tc01_clean

TC02 Insert New Split Item Other
    [Documentation]    Insert a new split_item_other; confirm in list + DB (OV_SPLIT_ITEM_OTHER).
    [Tags]    insert
    Insert Split Item Other Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Split Item Other Row Should Exist    ${TEST_CODE}
    Split Item Other Should Exist In DB    ${TEST_CODE}
    Capture Step    split_item_other_tc02_inserted

TC03 Update Split Item Other
    [Documentation]    Edit Name; confirm in list + DB ground truth.
    [Tags]    update
    Update Split Item Other Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Split Item Other Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Field Should Equal In View    OV_SPLIT_ITEM_OTHER    ${TEST_CODE}    NAME    ${OBJ_NAME_UPD}
    Capture Step    split_item_other_tc03_updated

TC04 Delete Split Item Other
    [Documentation]    Delete via End Date = Start Date; confirm gone from list + DB.
    [Tags]    delete    cleanup
    Delete Split Item Other    ${TEST_CODE}    ${END_DATE}
    Split Item Other Row Should Not Exist    ${TEST_CODE}
    Split Item Other Should Not Exist In DB    ${TEST_CODE}
    Capture Step    split_item_other_tc04_deleted


*** Keywords ***
Set Up Split Item Other Suite
    [Documentation]    Generate a unique test code/name, then open the Split Item Other screen.
    Prepare IUD Object Data    AUTOTEST_SIO_    Split Item Other
    Open Split Item Other Screen
