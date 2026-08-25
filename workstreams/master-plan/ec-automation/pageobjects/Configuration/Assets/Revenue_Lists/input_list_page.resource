*** Settings ***
Documentation       T3 (screen) — Input List page object.
...                 Screen: Configuration > Assets > Revenue_Lists > Input List (CD.0035).
...                 Manage-Object (OV) screen. Holds Input List's locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common).
...                 Bank-pattern conversion (2026-08-25): upgraded from the earlier
...                 generated/label-driven suite (inline DB-verify keywords called directly
...                 from the .robot file, 4 TCs, Suite-level login, generated unique
...                 AUTOTEST_IL_<timestamp> code) to the consolidated properties-file-driven
...                 shape matching bank_page.resource/object_list_page.resource - fixed
...                 AUTOTEST_INPUTLIST code, explicit grid-filter wiring, per-TC Login/Logout,
...                 PURE SCREEN verification in the .robot file (DB ground-truth lives inside
...                 the shared T2 keywords this delegates to, never called inline from the
...                 test suite itself).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${INPUT_LIST_SCREEN}    Input List
${INPUT_LIST_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/input_list_insert.properties
${INPUT_LIST_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/input_list_update.properties
${INPUT_LIST_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/input_list_form_verify.properties
${INPUT_LIST_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/input_list_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal.
${INPUT_LIST_TABLE}    ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date). Hardcoded, matching Bank/Object List's
# convention (same manage_object_nav objectdates row shape: Start Date C:1, End Date C:3).
${INPUT_LIST_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Input List's own form-field label set (List Category/Start Date deliberately excluded -
# Insert-only, not present in updateAttributes). Defined ONCE here so both Verify Input List
# Record Exists (TC02, against input_list_insert.properties) and Verify Input List Record
# Found (TC04, against input_list_form_verify.properties) share the same list.
@{INPUT_LIST_FORM_LABELS}    Code    Name


*** Keywords ***
Find Input List Row By Filter
    [Documentation]    Explicitly filter the Input List grid's Code column to ${code} via the
    ...    shared T2 Find Object Row By Filter (resources/manage_object.resource), matching
    ...    Bank/Object List's own explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${INPUT_LIST_TABLE}    ${code}

Clear Input List Row Filter
    [Documentation]    Clear the Code column filter (see Find Input List Row By Filter) via
    ...    the shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${INPUT_LIST_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Input List's OWN credentials (${INPUT_LIST_EC_USER}/
    ...    ${INPUT_LIST_EC_PASS} from credentials.py) on the current page. Zero-argument
    ...    wrapper so input_list_iud.robot's test cases read as a plain business step;
    ...    supplies Input List's own credential defaults to the shared T1 Login To EC Screen
    ...    (common.resource), which owns the actual login mechanics.
    Login To EC Screen    ${INPUT_LIST_EC_USER}    ${INPUT_LIST_EC_PASS}

Open Input List Screen
    [Documentation]    Navigate to the Input List screen. Assumes the caller already logged
    ...    in this test case (via Login To EC Application) - matches Bank/Object List's per-TC
    ...    Login/Open Screen/Action/Verify/Logout shape. The grid needs a GO to populate (no
    ...    default rows on open) - handled by Insert/Update/Delete/Find's own T2 calls, which
    ...    all reload the list after acting.
    Open EC Screen    ${INPUT_LIST_SCREEN}

Insert Input List Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties And
    ...    Verify Code, so input_list_iud.robot's test case body reads as a plain business step
    ...    with ZERO arguments. Also checks the inserted Code matches the suite's ${TEST_CODE}.
    ...    Pre-save evidence screenshot captured before Save is clicked, matching Bank.
    [Arguments]    ${properties_path}=${INPUT_LIST_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action
    RETURN    ${code}

Find Input List Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Calls
    ...    Find Input List Row By Filter first. Deliberately does NOT clear the filter
    ...    afterward - Verify Input List Record Found (called right after, same TC) needs the
    ...    grid still filtered to ${code} for its own grid-check.
    [Arguments]    ${code}=${TEST_CODE}
    Find Input List Row By Filter    ${code}
    Find Object Record    ${INPUT_LIST_TABLE}    ${code}    Input List

Verify Input List Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (no DB check here, matching Bank/Object List's TC02 convention): row
    ...    exists in the grid, then the form shows what was just inserted (Code/Name only -
    ...    List Category/Start Date are grid/insert-only, not present in updateAttributes).
    ...    Filters via Find Input List Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Input List Row By Filter    ${code}
    Verify Object Insert Exists    ${INPUT_LIST_TABLE}    ${code}    Input List
    ...    ${INPUT_LIST_INSERT_PROPERTIES}    @{INPUT_LIST_FORM_LABELS}
    Clear Input List Row Filter

Update Input List Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Pre-save evidence screenshot captured before Save is clicked, matching Bank.
    ...    Filters via Find Input List Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${INPUT_LIST_UPDATE_PROPERTIES}
    Find Input List Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${INPUT_LIST_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action
    Clear Input List Row Filter
    RETURN    ${data}

Verify Input List Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification, matching Bank/Object List's TC03 convention: the form shows the
    ...    updated Name. Filters via Find Input List Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Input List Row By Filter    ${code}
    Verify Object Form Record    ${INPUT_LIST_TABLE}    ${code}    Input List
    ...    ${INPUT_LIST_UPDATE_PROPERTIES}    Name
    Clear Input List Row Filter

Verify Input List Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the form record match the expected (post-update) data. Caller must already
    ...    have selected the row (TC04 does, via Find Input List Record before this) AND left
    ...    the Code filter active from that same call - clears the filter itself once both
    ...    checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${INPUT_LIST_TABLE}    ${code}    ${INPUT_LIST_GRID_VERIFY_PROPERTIES}
    ...    ${INPUT_LIST_FORM_VERIFY_PROPERTIES}    @{INPUT_LIST_FORM_LABELS}
    Clear Input List Row Filter

Delete Input List Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the input list, set End Date = Start Date (true delete), Save. Captures the
    ...    TC05 evidence screenshot right after End Date is filled but BEFORE Save is clicked,
    ...    matching Bank's convention. Filters via Find Input List Row By Filter first, clears
    ...    after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Input List Row By Filter    ${code}
    Delete Object Via End Date    ${INPUT_LIST_TABLE}    ${INPUT_LIST_DEL_ENDDATE}    ${code}
    ...    ${date}    ${TEST NAME}_action
    Clear Input List Row Filter

Verify Input List Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code}
    ...    is absent from BOTH the grid and the database (OV_STREAM_ITEM_COLLECTION).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${INPUT_LIST_TABLE}    OV_STREAM_ITEM_COLLECTION    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Input List Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to the
    ...    shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${INPUT_LIST_TABLE}    ${code}
