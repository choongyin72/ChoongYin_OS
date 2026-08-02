*** Settings ***
Documentation       EC IUD Test - Stream Item (Configuration > Assets > Stream Objects > Stream
...                 Item, CD.0008). Custom-URL OV screen, date-effective (VERSIONED). DELETE =
...                 End Date = Start Date (true delete in OV_STREAM_ITEM). Layered: this test ->
...                 stream_item_page (T3) -> manage_object (T2) + common (T1).
...
...                 INSERT + DELETE ONLY - no Update test case. Any Save on this screen's
...                 updateAttributes tab fails with EC's own error "Cannot run schedule job
...                 UpdateStreamItem because it has not been configured" - a genuine EC sandbox
...                 configuration gap (BF VO.0031 - Daily SI Pending Calculation scheduler job not
...                 enabled here), confirmed live and against EC's own online help for this screen.
...                 Owner instruction 2026-08-02: skip Update, cover Insert + Delete only.
...
...                 NEVER touch existing data. A unique AUTOTEST_SI_<timestamp> code is generated
...                 per run (EC keeps deleted codes in the base table, so codes are never reused).

Resource            ../../../../pageobjects/Configuration/Assets/Stream_Objects/stream_item_page.resource

Suite Setup         Set Up Stream Item Suite
Suite Teardown      Close EC

Test Tags           iud    stream-item


*** Variables ***
${TEST_CODE}        ${EMPTY}
${START_DATE}       ${TEST_START_DATE_REFDD}
${END_DATE}         ${TEST_START_DATE_REFDD}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test stream item does not exist before inserting.
    [Tags]    clean-state
    Stream Item Row Should Not Exist    ${TEST_CODE}
    Capture Step    stream_item_tc01_clean

TC02 Insert New Stream Item
    [Documentation]    Insert a new stream item (Code + Start Date + 12 mandatory reference
    ...    dropdowns first-available + Name) and confirm it appears in the list + DB.
    [Tags]    insert
    Insert Stream Item Record    ${TEST_CODE}    ${START_DATE}
    Stream Item Row Should Exist    ${TEST_CODE}
    Stream Item Should Exist In DB    ${TEST_CODE}
    Capture Step    stream_item_tc02_inserted

TC03 Delete Stream Item
    [Documentation]    Delete via End Date = Start Date and confirm the stream item is gone.
    [Tags]    delete    cleanup
    Delete Stream Item    ${TEST_CODE}    ${END_DATE}
    Stream Item Row Should Not Exist    ${TEST_CODE}
    Stream Item Should Not Exist In DB    ${TEST_CODE}
    Capture Step    stream_item_tc03_deleted


*** Keywords ***
Set Up Stream Item Suite
    [Documentation]    Generate a unique test code, then open the Stream Item screen.
    Prepare IUD Object Data    AUTOTEST_SI_    Stream Item
    Open Stream Item Screen
