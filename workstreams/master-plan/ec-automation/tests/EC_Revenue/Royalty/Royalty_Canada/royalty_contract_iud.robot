*** Settings ***
Documentation       EC INSERT+UPDATE-ONLY Test - Royalty Contract (EC_Revenue > Royalty > Royalty_Canada).
...                 OV-GM (manage-object, groupmodel): grid filtered by the navigator cascade (PROVEN
...                 explicit values, not first-available).
...                 DELETE IS PERMANENTLY OUT OF SCOPE (owner-confirmed 2026-08-15, closes Issue #336,
...                 same precedent as Production Day Table CO.1033): Contract Template "Royalty Fixed
...                 Percentage Canada" causes EC to auto-provision CNTR_PG_SETUP child rows with no UI
...                 path to remove them, so End=Start always fails with EC's own "Child record
...                 found..." error - a genuine EC product limitation, not a bug (see PR #331). Each
...                 live run of this suite permanently accumulates one more AUTOTEST_RC_<timestamp>
...                 residual row - accepted, not a defect. NEVER touch existing data.

Resource            ../../../../pageobjects/EC_Revenue/Royalty/Royalty_Canada/royalty_contract_page.resource

Suite Setup         Set Up Royalty Contract Suite
Suite Teardown      Close EC

Test Tags           iud    royalty_contract


*** Variables ***
${TEST_CODE}        ${EMPTY}
${OBJ_NAME}         ${EMPTY}
${OBJ_NAME_UPD}     ${EMPTY}
${START_DATE}       2003-01-01


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test object does not exist before inserting.
    [Tags]    clean-state
    Royalty Contract Row Should Not Exist    ${TEST_CODE}
    Capture Step    royalty_contract_tc01_clean

TC02 Insert New Royalty Contract
    [Documentation]    Insert under the navigator scope and confirm it lists.
    [Tags]    insert
    Insert Royalty Contract Record    ${TEST_CODE}    ${OBJ_NAME}    ${START_DATE}
    Royalty Contract Row Should Exist    ${TEST_CODE}
    Royalty Contract Should Exist In DB    ${TEST_CODE}
    Capture Step    royalty_contract_tc02_inserted

TC03 Update Royalty Contract Name
    [Documentation]    Edit the name and confirm the list reflects the change.
    [Tags]    update
    Update Royalty Contract Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Royalty Contract Row Should Show Name    ${TEST_CODE}    ${OBJ_NAME_UPD}
    Capture Step    royalty_contract_tc03_updated


*** Keywords ***
Set Up Royalty Contract Suite
    [Documentation]    Generate a unique test code/name, open the screen, fill the navigator cascade
    ...    with PROVEN explicit values (not first-available).
    Prepare IUD Object Data    AUTOTEST_RC_    Royalty Contract
    ${pu}=    Open Royalty Contract Screen
    VAR    ${GM_PU}    ${pu}    scope=SUITE
