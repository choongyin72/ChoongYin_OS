*** Settings ***
Documentation       EC IUD Test - Remote Endpoint Configuration (Configuration > Integration
...                 Services > Remote Endpoint Configuration, CO.1082). TV-style inline-editable
...                 grid, no navigator, physical delete (`TIME_SCOPE_CODE=INVARIANT`). Layered:
...                 this test -> remote_endpoint_config_page (T3) -> table/toolbar (T1) + DbVerify.
...
...                 QUIRK: Code must be lowercase alphanumeric + hyphens only (EC rejects the
...                 project's usual AUTOTEST_XX_ uppercase-underscore convention here) - a unique
...                 `autotest-rec-<timestamp>` code is generated per run instead.

Resource            ../../../pageobjects/Configuration/Integration_Services/remote_endpoint_config_page.resource

Suite Setup         Set Up Remote Endpoint Configuration Suite
Suite Teardown      Close EC

Test Tags           iud    remote-endpoint-config


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test record does not exist before inserting.
    [Tags]    clean-state
    Remote Endpoint Configuration Should Not Exist In DB    ${TEST_CODE}
    Capture Step    rec_tc01_clean

TC02 Insert New Remote Endpoint Configuration
    [Documentation]    Insert (Code + Name + Remote Type first-available) and confirm it persists.
    [Tags]    insert
    Insert Remote Endpoint Configuration Record    ${TEST_CODE}    ${OBJ_NAME}
    Remote Endpoint Configuration Should Exist In DB    ${TEST_CODE}
    Capture Step    rec_tc02_inserted

TC03 Update Remote Endpoint Configuration Name
    [Documentation]    Edit the name and confirm the DB reflects the change.
    [Tags]    update
    Update Remote Endpoint Configuration Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Remote Endpoint Configuration Should Exist In DB    ${TEST_CODE}
    Capture Step    rec_tc03_updated

TC04 Delete Remote Endpoint Configuration
    [Documentation]    Physically delete and confirm it is gone from the DB.
    [Tags]    delete    cleanup
    Delete Remote Endpoint Configuration    ${TEST_CODE}
    Remote Endpoint Configuration Should Not Exist In DB    ${TEST_CODE}
    Capture Step    rec_tc04_deleted


*** Keywords ***
Set Up Remote Endpoint Configuration Suite
    [Documentation]    Generate a unique lowercase-slug test code (this screen rejects the
    ...    project's usual AUTOTEST_XX_ uppercase convention), then open the screen.
    ${code}=    Generate Unique Code    autotest-rec-
    VAR    ${TEST_CODE}    ${code}    scope=SUITE
    VAR    ${OBJ_NAME}    AUTOTEST REC ${code}    scope=SUITE
    VAR    ${OBJ_NAME_UPD}    AUTOTEST REC ${code} UPD    scope=SUITE
    Open Remote Endpoint Configuration Screen
