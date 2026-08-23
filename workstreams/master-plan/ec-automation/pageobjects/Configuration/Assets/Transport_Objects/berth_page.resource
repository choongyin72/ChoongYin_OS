*** Settings ***
Documentation       T3 (screen) — Berth page object.
...                 Screen: Configuration > Assets > Transport Objects > Berth (CO.2012).
...                 Manage-Object (OV) screen. Holds Berth's locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common).
...                 Rebuilt 2026-08-23 (Batch 7) to mirror Bank/State exactly - replaces the
...                 older generated-code/no-filter pattern with the label-driven,
...                 properties-file-driven, grid-filter-wired, T2-consolidated pattern.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${BERTH_SCREEN}         Berth
${BERTH_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/berth_insert.properties
${BERTH_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/berth_update.properties
${BERTH_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/berth_form_verify.properties
${BERTH_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/berth_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal.
${BERTH_TABLE}          ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date), matching Bank/State's convention.
${BERTH_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Berth's own form-field label set. Labels are "Berth Code"/"Berth Name" (screen-prefixed) -
# confirmed via ec-ui-knowledge/screens/berth.md (fresh scan 2026-07-26) and the already-proven
# Playwright driver py/berth_iud.py; NOT the generic "Code"/"Name" Bank/Object List use.
# Start Date deliberately excluded - Insert-only, not present in updateAttributes (same as
# Bank/State). Defined ONCE here so both Verify Berth Record Exists (TC02) and Verify Berth
# Record Found (TC04) share the same list.
@{BERTH_FORM_LABELS}    Berth Code    Berth Name


*** Keywords ***
Find Berth Row By Filter
    [Documentation]    Explicitly filter the Berth grid's Code column to ${code} via the shared
    ...    T2 Find Object Row By Filter (resources/manage_object.resource) - matches Account/
    ...    Bank/State's own explicit filter usage (owner, 2026-08-22: "others (Bank, State,
    ...    List_Object) should follow Account... utilise same filter feature"), rather than
    ...    relying only on Select Object Row's implicit 3s-timeout fallback.
    [Arguments]    ${code}
    Find Object Row By Filter    ${BERTH_TABLE}    ${code}

Clear Berth Row Filter
    [Documentation]    Clear the Code column filter (see Find Berth Row By Filter) via the
    ...    shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${BERTH_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Berth's OWN credentials (${BERTH_EC_USER}/
    ...    ${BERTH_EC_PASS} from credentials.py) on the current page. Standing decision
    ...    (owner, 2026-08-22): every EC screen gets its own dedicated credential pair.
    ...    Zero-argument wrapper so berth_iud.robot's test cases read as a plain business
    ...    step; supplies Berth's own credential defaults to the shared T1 Login To EC
    ...    Screen (common.resource), which owns the actual login mechanics.
    Login To EC Screen    ${BERTH_EC_USER}    ${BERTH_EC_PASS}

Open Berth Screen
    [Documentation]    Navigate to the Berth screen. Assumes the caller already logged in
    ...    this test case (via Login To EC Application) - this keyword ONLY navigates.
    ...    Delegates to the shared T1 Open EC Screen (common.resource) for the actual mechanics.
    Open EC Screen    ${BERTH_SCREEN}

Insert Berth Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties
    ...    And Verify Code, so berth_iud.robot's test case body reads as a plain business
    ...    step with ZERO arguments. Also checks the inserted Code matches the suite's
    ...    ${TEST_CODE}. Pre-save evidence screenshot captured before Save is clicked,
    ...    matching Bank/State.
    [Arguments]    ${properties_path}=${BERTH_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Berth Code
    RETURN    ${code}

Verify Berth Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (no DB check here, matching Bank/State's TC02 convention): row
    ...    exists in the grid, then the form shows what was just inserted (Berth
    ...    Code/Berth Name only - Start Date is grid/insert-only, not present in
    ...    updateAttributes). Delegates the full sequence (row-check, select, form-compare,
    ...    screenshot) to the shared T2 Verify Object Insert Exists.
    ...    Filters via Find Berth Row By Filter first, clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find Berth Row By Filter    ${code}
    Verify Object Insert Exists    ${BERTH_TABLE}    ${code}    Berth    ${BERTH_INSERT_PROPERTIES}
    ...    @{BERTH_FORM_LABELS}    code_label=Berth Code
    Clear Berth Row Filter

Update Berth Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Pre-save evidence screenshot captured before Save is clicked, matching Bank/State.
    ...    Filters via Find Berth Row By Filter first, clears after (2026-08-22
    ...    standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${BERTH_UPDATE_PROPERTIES}
    Find Berth Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${BERTH_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Berth Code
    Clear Berth Row Filter
    RETURN    ${data}

Verify Berth Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification, matching Bank/State's TC03 convention: the form shows the updated
    ...    Berth Name. Delegates the full sequence (select, form-compare, screenshot) to
    ...    the shared T2 Verify Object Form Record. Filters via Find Berth Row By Filter
    ...    first, clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find Berth Row By Filter    ${code}
    Verify Object Form Record    ${BERTH_TABLE}    ${code}    Berth    ${BERTH_UPDATE_PROPERTIES}
    ...    Berth Name    code_label=Berth Code
    Clear Berth Row Filter

Find Berth Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Delegates the full select+capture sequence. Calls Find Berth Row By Filter first
    ...    (2026-08-22 standardisation). Deliberately does NOT clear the filter afterward -
    ...    Verify Berth Record Found (called right after, same TC) needs the grid still
    ...    filtered to ${code} for its own grid-check, since it doesn't re-select the row
    ...    itself; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Berth Row By Filter    ${code}
    Find Object Record    ${BERTH_TABLE}    ${code}    Berth    code_label=Berth Code

Verify Berth Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the form record match the expected (post-update) data. Delegates the
    ...    full sequence (grid-compare, form-compare, screenshot) to the shared T2 Verify
    ...    Object Found. Caller must already have selected the row (TC04 does, via Find
    ...    Berth Record before this) AND left the Code filter active from that same call -
    ...    clears the filter itself once both checks are done (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${BERTH_TABLE}    ${code}    ${BERTH_GRID_VERIFY_PROPERTIES}
    ...    ${BERTH_FORM_VERIFY_PROPERTIES}    @{BERTH_FORM_LABELS}
    Clear Berth Row Filter

Delete Berth Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date,
    ...    called with ZERO arguments (defaults ${code}/${date} to the suite's
    ...    ${TEST_CODE}/${END_DATE}). Select the berth, set End Date = Start Date (true
    ...    delete), Save. Captures the TC05 evidence screenshot right after the End Date is
    ...    filled but BEFORE Save is clicked, matching Bank/State's convention.
    ...    Filters via Find Berth Row By Filter first, clears after (2026-08-22
    ...    standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Berth Row By Filter    ${code}
    Delete Object Via End Date    ${BERTH_TABLE}    ${BERTH_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Berth Row Filter

Verify Berth Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code}
    ...    is absent from BOTH the grid and the database.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${BERTH_TABLE}    OV_BERTH    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Berth Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to
    ...    the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${BERTH_TABLE}    ${code}
