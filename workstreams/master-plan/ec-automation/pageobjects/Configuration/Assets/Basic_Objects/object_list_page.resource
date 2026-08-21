*** Settings ***
Documentation       T3 (screen) — Object List page object.
...                 Screen: Configuration > Assets > Basic Objects > Object List.
...                 Manage-Object (OV) screen. Holds Object List's locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${OBJECT_LIST_SCREEN}    Object List
${OBJECT_LIST_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/object_list_insert.properties
${OBJECT_LIST_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/object_list_update.properties
${OBJECT_LIST_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/object_list_form_verify.properties
${OBJECT_LIST_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/object_list_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal.
${OBJECT_LIST_TABLE}    ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date). Hardcoded, matching Bank's convention
# and cross-confirmed against the already-proven Playwright driver config (del_end, identical id).
${OBJECT_LIST_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Object List's own form-field label set (Class Name/Start Date deliberately excluded - Insert-only,
# not present in updateAttributes). Defined ONCE here so both Verify Object List Record Exists (TC02,
# against object_list_insert.properties) and Verify Object List Record Found (TC04, against
# object_list_form_verify.properties) share the same list instead of each hardcoding it inline
# (owner-requested 2026-08-22 consolidation of the T2 Verify Object Insert Exists/Found calls).
@{OBJECT_LIST_FORM_LABELS}    Code    Name


*** Keywords ***
Login To EC Application
    [Documentation]    Authenticate as Object List's OWN credentials (${OBJECT_LIST_EC_USER}/
    ...    ${OBJECT_LIST_EC_PASS} from credentials.py) on the current page. Standing decision
    ...    (owner, 2026-08-22): every EC screen gets its own dedicated credential pair - real
    ...    EC deployments gate different screens behind different role access, so a
    ...    screen-specific login identity is the default going forward (supersedes the
    ...    earlier "shared default unless overridden" convention). Zero-argument wrapper so
    ...    object_list_iud.robot's test cases read as a plain business step; supplies Object
    ...    List's own credential defaults to the shared T1 Login To EC Screen (common.resource),
    ...    which owns the actual login mechanics.
    Login To EC Screen    ${OBJECT_LIST_EC_USER}    ${OBJECT_LIST_EC_PASS}

Open Object List Screen
    [Documentation]    Navigate to the Object List screen. Assumes the caller already
    ...    logged in this test case (via Login To EC Application) - this keyword ONLY
    ...    navigates, matching Bank's per-TC Login/Open Screen/Action/Verify/Logout shape.
    ...    Delegates to the shared T1 Open EC Screen (common.resource) for the actual mechanics.
    Open EC Screen    ${OBJECT_LIST_SCREEN}

Object List Row Should Exist
    [Documentation]    Assert an object list with ${code} is present in the grid.
    [Arguments]    ${code}
    Row Should Exist    ${OBJECT_LIST_TABLE}    ${code}

Object List Row Should Not Exist
    [Documentation]    Assert an object list with ${code} is absent from the grid.
    [Arguments]    ${code}
    Row Should Not Exist    ${OBJECT_LIST_TABLE}    ${code}

Insert Object List Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties And
    ...    Verify Code, so object_list_iud.robot's test case body reads as a plain business step
    ...    with ZERO arguments. Also checks the inserted Code matches the suite's ${TEST_CODE}.
    ...    Pre-save evidence screenshot captured before Save is clicked, matching Bank.
    [Arguments]    ${properties_path}=${OBJECT_LIST_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action
    RETURN    ${code}

Find Object List
    [Documentation]    Locate the object list row by ${code} and select it (loads
    ...    updateAttributes), verifying row-identity (Code read back) before returning.
    [Arguments]    ${code}
    Find Object By Code    ${OBJECT_LIST_TABLE}    ${code}    Object List

Find Object List Record
    [Documentation]    Friendly-narrative wrapper around Find Object List, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}).
    [Arguments]    ${code}=${TEST_CODE}
    Find Object List    ${code}
    Capture Step    ${TEST NAME}_action

Verify Object List Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (no DB check here, matching Bank's TC02 convention): row exists in
    ...    the grid, then the form shows what was just inserted (Code/Name only - Class
    ...    Name/Start Date are grid/insert-only, not present in updateAttributes).
    ...    Delegates the full sequence (row-check, select, form-compare, screenshot) to the
    ...    shared T2 Verify Object Insert Exists (owner-requested 2026-08-22 consolidation).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Insert Exists    ${OBJECT_LIST_TABLE}    ${code}    Object List
    ...    ${OBJECT_LIST_INSERT_PROPERTIES}    @{OBJECT_LIST_FORM_LABELS}

Update Object List Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Pre-save evidence screenshot captured before Save is clicked, matching Bank.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${OBJECT_LIST_UPDATE_PROPERTIES}
    ${data}=    Update Object From Properties    ${OBJECT_LIST_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action
    RETURN    ${data}

Verify Object List Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification, matching Bank's TC03 convention: the form shows the updated Name.
    ...    Delegates the full sequence (select, form-compare, screenshot) to the shared T2
    ...    Verify Object Form Record (owner-requested 2026-08-22 consolidation).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Form Record    ${OBJECT_LIST_TABLE}    ${code}    Object List
    ...    ${OBJECT_LIST_UPDATE_PROPERTIES}    Name

Verify Object List Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the form record match the expected (post-update) data.
    ...    Delegates the full sequence (grid-compare, form-compare, screenshot) to the shared
    ...    T2 Verify Object Found (owner-requested 2026-08-22 consolidation). Caller must
    ...    already have selected the row (TC04 does, via Find Object List Record before this).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${OBJECT_LIST_TABLE}    ${code}    ${OBJECT_LIST_GRID_VERIFY_PROPERTIES}
    ...    ${OBJECT_LIST_FORM_VERIFY_PROPERTIES}    @{OBJECT_LIST_FORM_LABELS}

Delete Object List
    [Documentation]    Select the object list, set End Date = Start Date (true delete), Save.
    ...    Captures the TC05 evidence screenshot right after End Date is filled but BEFORE
    ...    Save is clicked, matching Bank's convention.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${OBJECT_LIST_TABLE}    ${OBJECT_LIST_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action

Delete Object List Record And Save
    [Documentation]    Friendly-narrative wrapper around Delete Object List, called with ZERO
    ...    arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Delete Object List    ${code}    ${date}

Verify Object List Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code}
    ...    is absent from BOTH the grid and the database.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${OBJECT_LIST_TABLE}    OV_OBJECT_LIST    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Object List Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    [Arguments]    ${code}=${TEST_CODE}
    Object List Row Should Not Exist    ${code}
    Capture Step    ${TEST NAME}_verify
