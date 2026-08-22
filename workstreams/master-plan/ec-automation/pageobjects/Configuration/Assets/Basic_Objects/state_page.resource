*** Settings ***
Documentation       T3 (screen) — State page object.
...                 Screen: Configuration > Assets > Basic Objects > State.
...                 Manage-Object (OV) screen. Holds State's locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common).
...                 Rebuilt 2026-08-22 to mirror Bank/Object List exactly (owner:
...                 "reflect the current EC screen exactly the same way as the OV_BANK
...                 IUD related task") - replaces the older hardcoded-field-id/generated
...                 -code pattern with the label-driven, properties-file-driven,
...                 T2-consolidated pattern.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${STATE_SCREEN}         State
${STATE_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/state_insert.properties
${STATE_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/state_update.properties
${STATE_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/state_form_verify.properties
${STATE_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/state_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal.
${STATE_TABLE}          ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date), matching Bank/Object List's convention.
${STATE_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# State's own form-field label set. Labels are "State Code"/"State Name" (screen-prefixed) -
# confirmed live 2026-08-22 via the New Object form screenshot after TC02's first live run
# failed on the generic "Code"/"Name" labels Bank/Object List use; NOT a Bank-family universal
# convention. Start Date deliberately excluded - Insert-only, not present in updateAttributes.
# Defined ONCE here so both Verify State Record Exists (TC02) and Verify State Record Found
# (TC04) share the same list.
@{STATE_FORM_LABELS}    State Code    State Name


*** Keywords ***
Find State Row By Filter
    [Documentation]    Explicitly filter the State grid's Code column to ${code} via the shared
    ...    T2 Find Object Row By Filter (resources/manage_object.resource) - matches Account's
    ...    own explicit filter usage (owner, 2026-08-22: "others (Bank, State, List_Object)
    ...    should follow Account... utilise same filter feature"), rather than relying only on
    ...    Select Object Row's implicit 3s-timeout fallback.
    [Arguments]    ${code}
    Find Object Row By Filter    ${STATE_TABLE}    ${code}

Clear State Row Filter
    [Documentation]    Clear the Code column filter (see Find State Row By Filter) via the
    ...    shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${STATE_TABLE}

Login To EC Application
    [Documentation]    Authenticate as State's OWN credentials (${STATE_EC_USER}/
    ...    ${STATE_EC_PASS} from credentials.py) on the current page. Standing decision
    ...    (owner, 2026-08-22): every EC screen gets its own dedicated credential pair.
    ...    Zero-argument wrapper so state_iud.robot's test cases read as a plain business
    ...    step; supplies State's own credential defaults to the shared T1 Login To EC
    ...    Screen (common.resource), which owns the actual login mechanics.
    Login To EC Screen    ${STATE_EC_USER}    ${STATE_EC_PASS}

Open State Screen
    [Documentation]    Navigate to the State screen. Assumes the caller already logged in
    ...    this test case (via Login To EC Application) - this keyword ONLY navigates.
    ...    Delegates to the shared T1 Open EC Screen (common.resource) for the actual mechanics.
    Open EC Screen    ${STATE_SCREEN}

Insert State Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties
    ...    And Verify Code, so state_iud.robot's test case body reads as a plain business
    ...    step with ZERO arguments. Also checks the inserted Code matches the suite's
    ...    ${TEST_CODE}. Pre-save evidence screenshot captured before Save is clicked,
    ...    matching Bank/Object List.
    [Arguments]    ${properties_path}=${STATE_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=State Code
    RETURN    ${code}

Verify State Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (no DB check here, matching Bank/Object List's TC02 convention):
    ...    row exists in the grid, then the form shows what was just inserted (State
    ...    Code/State Name only - Start Date is grid/insert-only, not present in updateAttributes).
    ...    Delegates the full sequence (row-check, select, form-compare, screenshot) to the
    ...    shared T2 Verify Object Insert Exists.
    ...    Filters via Find State Row By Filter first, clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find State Row By Filter    ${code}
    Verify Object Insert Exists    ${STATE_TABLE}    ${code}    State    ${STATE_INSERT_PROPERTIES}
    ...    @{STATE_FORM_LABELS}    code_label=State Code
    Clear State Row Filter

Update State Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Pre-save evidence screenshot captured before Save is clicked, matching Bank/Object
    ...    List. Filters via Find State Row By Filter first, clears after (2026-08-22
    ...    standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${STATE_UPDATE_PROPERTIES}
    Find State Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${STATE_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=State Code
    Clear State Row Filter
    RETURN    ${data}

Verify State Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification, matching Bank/Object List's TC03 convention: the form shows the
    ...    updated Name. Delegates the full sequence (select, form-compare, screenshot) to
    ...    the shared T2 Verify Object Form Record. Filters via Find State Row By Filter
    ...    first, clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find State Row By Filter    ${code}
    Verify Object Form Record    ${STATE_TABLE}    ${code}    State    ${STATE_UPDATE_PROPERTIES}
    ...    State Name    code_label=State Code
    Clear State Row Filter

Find State Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Delegates the full select+capture sequence. Calls Find State Row By Filter first
    ...    (2026-08-22 standardisation). Deliberately does NOT clear the filter afterward -
    ...    Verify State Record Found (called right after, same TC) needs the grid still
    ...    filtered to ${code} for its own grid-check, since it doesn't re-select the row
    ...    itself; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find State Row By Filter    ${code}
    Find Object Record    ${STATE_TABLE}    ${code}    State    code_label=State Code

Verify State Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the form record match the expected (post-update) data. Delegates the
    ...    full sequence (grid-compare, form-compare, screenshot) to the shared T2 Verify
    ...    Object Found. Caller must already have selected the row (TC04 does, via Find
    ...    State Record before this) AND left the Code filter active from that same call -
    ...    clears the filter itself once both checks are done (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${STATE_TABLE}    ${code}    ${STATE_GRID_VERIFY_PROPERTIES}
    ...    ${STATE_FORM_VERIFY_PROPERTIES}    @{STATE_FORM_LABELS}
    Clear State Row Filter

Delete State Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date,
    ...    called with ZERO arguments (defaults ${code}/${date} to the suite's
    ...    ${TEST_CODE}/${END_DATE}). Select the state, set End Date = Start Date (true
    ...    delete), Save. Captures the TC05 evidence screenshot right after the End Date is
    ...    filled but BEFORE Save is clicked, matching Bank/Object List's convention.
    ...    Filters via Find State Row By Filter first, clears after (2026-08-22
    ...    standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find State Row By Filter    ${code}
    Delete Object Via End Date    ${STATE_TABLE}    ${STATE_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear State Row Filter

Verify State Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code}
    ...    is absent from BOTH the grid and the database.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${STATE_TABLE}    OV_STATE    ${code}
    Capture Step    ${TEST NAME}_verify

Verify State Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to
    ...    the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${STATE_TABLE}    ${code}
