*** Settings ***
Documentation       T3 (screen) — Storage Flow page object.
...                 Screen: Configuration > Assets > Tank_and_Storage_Objects > Storage Flow (CO.2091).
...                 Manage-Object (OV) screen. Holds Storage Flow's locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common).
...                 Rebuilt 2026-08-23 (Batch 10) to mirror Bank/Berth exactly - replaces the
...                 older unique-timestamped-code/no-filter pattern with the label-driven,
...                 properties-file-driven, grid-filter-wired, T2-consolidated pattern.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${STORAGE_FLOW_SCREEN}         Storage Flow
${STORAGE_FLOW_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/storage_flow_insert.properties
${STORAGE_FLOW_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/storage_flow_update.properties
${STORAGE_FLOW_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/storage_flow_form_verify.properties
${STORAGE_FLOW_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/storage_flow_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal.
${STORAGE_FLOW_TABLE}          ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date) - same universal OV id confirmed on
# Bank/Berth/State/Storage (sibling screen in this same folder): objectdates form, column 3.
${STORAGE_FLOW_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Storage Flow's own form-field label set. Labels are "Storage Flow Code"/"Storage Flow Name"
# (screen-prefixed) - confirmed via direct grep [from fresh scan] and the already-proven
# Playwright driver py/storage_flow_iud.py; NOT the generic "Code"/"Name" Bank/Object List use.
# Start Date deliberately excluded - Insert-only, not present in updateAttributes (same as
# Bank/Berth). Defined ONCE here so both Verify Storage Flow Record Exists (TC02) and Verify
# Storage Flow Record Found (TC04) share the same list.
@{STORAGE_FLOW_FORM_LABELS}    Storage Flow Code    Storage Flow Name


*** Keywords ***
Find Storage Flow Row By Filter
    [Documentation]    Explicitly filter the Storage Flow grid's Code column to ${code} via the
    ...    shared T2 Find Object Row By Filter (resources/manage_object.resource) - matches
    ...    Bank/Berth/State's own explicit filter usage (owner, 2026-08-22: "others... should
    ...    follow Account... utilise same filter feature"), rather than relying only on Select
    ...    Object Row's implicit 3s-timeout fallback.
    [Arguments]    ${code}
    Find Object Row By Filter    ${STORAGE_FLOW_TABLE}    ${code}

Clear Storage Flow Row Filter
    [Documentation]    Clear the Code column filter (see Find Storage Flow Row By Filter) via
    ...    the shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${STORAGE_FLOW_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Storage Flow's OWN credentials (${STORAGE_FLOW_EC_USER}/
    ...    ${STORAGE_FLOW_EC_PASS} from credentials.py) on the current page. Standing decision
    ...    (owner, 2026-08-22): every EC screen gets its own dedicated credential pair.
    ...    Zero-argument wrapper so storage_flow_iud.robot's test cases read as a plain
    ...    business step; supplies Storage Flow's own credential defaults to the shared T1
    ...    Login To EC Screen (common.resource), which owns the actual login mechanics.
    Login To EC Screen    ${STORAGE_FLOW_EC_USER}    ${STORAGE_FLOW_EC_PASS}

Open Storage Flow Screen
    [Documentation]    Navigate to the Storage Flow screen. Assumes the caller already logged
    ...    in this test case (via Login To EC Application) - this keyword ONLY navigates.
    ...    Delegates to the shared T1 Open EC Screen (common.resource) for the actual
    ...    mechanics.
    Open EC Screen    ${STORAGE_FLOW_SCREEN}

Insert Storage Flow Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties
    ...    And Verify Code, so storage_flow_iud.robot's test case body reads as a plain
    ...    business step with ZERO arguments. Also checks the inserted Code matches the
    ...    suite's ${TEST_CODE}. The properties file also fills Storage Flow's own mandatory
    ...    "Flow Direction"/"Storage" dropdowns (__FIRST__) - carried over from the already-
    ...    proven page object/driver (Batch-9 Process Train lesson: trust the existing proven
    ...    field set over a static CSS mandatory scan). Pre-save evidence screenshot captured
    ...    before Save is clicked, matching Bank/Berth.
    [Arguments]    ${properties_path}=${STORAGE_FLOW_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Storage Flow Code
    RETURN    ${code}

Verify Storage Flow Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (no DB check here, matching Bank/Berth's TC02 convention): row exists
    ...    in the grid, then the form shows what was just inserted (Storage Flow Code/
    ...    Storage Flow Name only - Start Date is grid/insert-only, and Flow Direction/
    ...    Storage are __FIRST__ dropdowns whose rendered label is not knowable ahead of
    ...    time, so both are excluded from this round-trip check same as Bank/Berth exclude
    ...    Start Date). Delegates the full sequence (row-check, select, form-compare,
    ...    screenshot) to the shared T2 Verify Object Insert Exists. Filters via Find Storage
    ...    Flow Row By Filter first, clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find Storage Flow Row By Filter    ${code}
    Verify Object Insert Exists    ${STORAGE_FLOW_TABLE}    ${code}    Storage Flow
    ...    ${STORAGE_FLOW_INSERT_PROPERTIES}    @{STORAGE_FLOW_FORM_LABELS}    code_label=Storage Flow Code
    Clear Storage Flow Row Filter

Update Storage Flow Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Pre-save evidence screenshot captured before Save is clicked, matching Bank/Berth.
    ...    Filters via Find Storage Flow Row By Filter first, clears after (2026-08-22
    ...    standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${STORAGE_FLOW_UPDATE_PROPERTIES}
    Find Storage Flow Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${STORAGE_FLOW_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Storage Flow Code
    Clear Storage Flow Row Filter
    RETURN    ${data}

Verify Storage Flow Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification, matching Bank/Berth's TC03 convention: the form shows the updated
    ...    Storage Flow Name. Delegates the full sequence (select, form-compare, screenshot)
    ...    to the shared T2 Verify Object Form Record. Filters via Find Storage Flow Row By
    ...    Filter first, clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find Storage Flow Row By Filter    ${code}
    Verify Object Form Record    ${STORAGE_FLOW_TABLE}    ${code}    Storage Flow
    ...    ${STORAGE_FLOW_UPDATE_PROPERTIES}    Storage Flow Name    code_label=Storage Flow Code
    Clear Storage Flow Row Filter

Find Storage Flow Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Delegates the full select+capture sequence. Calls Find Storage Flow Row By Filter
    ...    first (2026-08-22 standardisation). Deliberately does NOT clear the filter
    ...    afterward - Verify Storage Flow Record Found (called right after, same TC) needs
    ...    the grid still filtered to ${code} for its own grid-check, since it doesn't
    ...    re-select the row itself; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Storage Flow Row By Filter    ${code}
    Find Object Record    ${STORAGE_FLOW_TABLE}    ${code}    Storage Flow    code_label=Storage Flow Code

Verify Storage Flow Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the form record match the expected (post-update) data. Delegates the
    ...    full sequence (grid-compare, form-compare, screenshot) to the shared T2 Verify
    ...    Object Found. Caller must already have selected the row (TC04 does, via Find
    ...    Storage Flow Record before this) AND left the Code filter active from that same
    ...    call - clears the filter itself once both checks are done (2026-08-22
    ...    standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${STORAGE_FLOW_TABLE}    ${code}    ${STORAGE_FLOW_GRID_VERIFY_PROPERTIES}
    ...    ${STORAGE_FLOW_FORM_VERIFY_PROPERTIES}    @{STORAGE_FLOW_FORM_LABELS}
    Clear Storage Flow Row Filter

Delete Storage Flow Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date,
    ...    called with ZERO arguments (defaults ${code}/${date} to the suite's
    ...    ${TEST_CODE}/${END_DATE}). Select the storage_flow, set End Date = Start Date
    ...    (true delete), Save. Captures the TC05 evidence screenshot right after the End
    ...    Date is filled but BEFORE Save is clicked, matching Bank/Berth. Filters via Find
    ...    Storage Flow Row By Filter first, clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Storage Flow Row By Filter    ${code}
    Delete Object Via End Date    ${STORAGE_FLOW_TABLE}    ${STORAGE_FLOW_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Storage Flow Row Filter

Verify Storage Flow Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is
    ...    absent from BOTH the grid and the database.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${STORAGE_FLOW_TABLE}    OV_STORAGE_FLOW    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Storage Flow Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to
    ...    the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${STORAGE_FLOW_TABLE}    ${code}
