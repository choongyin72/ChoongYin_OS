*** Settings ***
Documentation       EC IUD Test - MIME Type Mapping (Configuration > System).
...                 TABLE class (TV view): inline-editable paginated grid, NO navigator,
...                 PHYSICAL delete (gone from base table CTRL_MIME_TYPE_MAPPING).
...                 Layered: this test -> mime_page (T3) -> common/table/toolbar (T1) + DbVerify.
...                 Contrast to OV (Bank/Equipment): no manage_object, no navigator, delete is physical.
...                 NEVER touch existing data. Unique application/x-ec-autotest-<timestamp> per run.

Resource            ../../../pageobjects/Configuration/System/mime_page.resource

Suite Setup         Set Up MIME Suite
Suite Teardown      Close EC

Test Tags           iud    mime


*** Variables ***
${TEST_MIME}    ${EMPTY}
${EXT_INS}      .ectest
${EXT_UPD}      .ectest,.ectest2


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test MIME type does not exist yet.
    [Tags]    clean-state
    MIME Row Should Not Exist    ${TEST_MIME}
    Capture Step    mime_tc01_clean

TC02 Insert MIME Mapping
    [Documentation]    Insert a new MIME mapping and confirm it appears (UI + DB).
    [Tags]    insert
    Insert MIME Mapping    ${TEST_MIME}    ${EXT_INS}
    MIME Row Should Exist    ${TEST_MIME}
    MIME Should Exist In DB    ${TEST_MIME}
    Capture Step    mime_tc02_inserted

TC03 Update File Extensions
    [Documentation]    Edit the File Extensions and confirm the change persisted.
    [Tags]    update
    Update MIME Extensions    ${TEST_MIME}    ${EXT_UPD}
    MIME Extensions Should Be    ${TEST_MIME}    ${EXT_UPD}
    Capture Step    mime_tc03_updated

TC04 Delete MIME Mapping (physical)
    [Documentation]    Physically delete the mapping and confirm it is gone (UI + base table).
    [Tags]    delete    cleanup
    Delete MIME Mapping    ${TEST_MIME}
    MIME Row Should Not Exist    ${TEST_MIME}
    MIME Should Not Exist In DB    ${TEST_MIME}
    Capture Step    mime_tc04_deleted


*** Keywords ***
Set Up MIME Suite
    [Documentation]    Generate a unique test MIME type, then open the MIME screen.
    ${code}=    Generate Unique Code    application/x-ec-autotest-
    VAR    ${TEST_MIME}=    ${code}    scope=SUITE
    Open MIME Screen
