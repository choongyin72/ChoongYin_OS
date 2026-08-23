*** Settings ***
Documentation       T3 (screen) — Deferment Group page object.
...                 Screen: Configuration > Assets > Facility_Objects > Deferment Group (CO.0149).
...                 Manage-Object (OV) screen. Holds Deferment Group's locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common).
...                 Rebuilt 2026-08-23 (Batch 8) to mirror Bank/State/Berth exactly - replaces
...                 the older label-driven-but-no-filter pattern with the label-driven,
...                 properties-file-driven, grid-filter-wired, T2-consolidated pattern.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${DEFERMENT_GROUP_SCREEN}    Deferment Group
${DEFERMENT_GROUP_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/deferment_group_insert.properties
${DEFERMENT_GROUP_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/deferment_group_update.properties
${DEFERMENT_GROUP_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/deferment_group_form_verify.properties
${DEFERMENT_GROUP_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/deferment_group_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal.
${DEFERMENT_GROUP_TABLE}    ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date), matching Bank/State/Berth's convention.
${DEFERMENT_GROUP_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Deferment Group's own form-field label set. Labels are "Deferment Group Code"/"Deferment
# Group Name" (screen-prefixed) - confirmed via the page object's prior recon comment and the
# already-proven Playwright driver py/deferment_group_iud.py (INSERT_FIELDS/UPDATE_FIELDS).
# Start Date deliberately excluded - Insert-only, not present in updateAttributes (same as
# Bank/State/Berth). Defined ONCE here so both Verify Deferment Group Record Exists (TC02)
# and Verify Deferment Group Record Found (TC04) share the same list.
@{DEFERMENT_GROUP_FORM_LABELS}    Deferment Group Code    Deferment Group Name


*** Keywords ***
Find Deferment Group Row By Filter
    [Documentation]    Explicitly filter the Deferment Group grid's Code column to ${code} via
    ...    the shared T2 Find Object Row By Filter (resources/manage_object.resource) -
    ...    matches Account/Bank/State/Berth's own explicit filter usage (owner, 2026-08-22:
    ...    "others (Bank, State, List_Object) should follow Account... utilise same filter
    ...    feature"), rather than relying only on Select Object Row's implicit 3s-timeout
    ...    fallback.
    [Arguments]    ${code}
    Find Object Row By Filter    ${DEFERMENT_GROUP_TABLE}    ${code}

Clear Deferment Group Row Filter
    [Documentation]    Clear the Code column filter (see Find Deferment Group Row By Filter)
    ...    via the shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered
    ...    view.
    Clear Object Row Filter    ${DEFERMENT_GROUP_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Deferment Group's OWN credentials
    ...    (${DEFERMENT_GROUP_EC_USER}/${DEFERMENT_GROUP_EC_PASS} from credentials.py) on the
    ...    current page. Standing decision (owner, 2026-08-22): every EC screen gets its own
    ...    dedicated credential pair. Zero-argument wrapper so deferment_group_iud.robot's test
    ...    cases read as a plain business step; supplies Deferment Group's own credential
    ...    defaults to the shared T1 Login To EC Screen (common.resource), which owns the
    ...    actual login mechanics.
    Login To EC Screen    ${DEFERMENT_GROUP_EC_USER}    ${DEFERMENT_GROUP_EC_PASS}

Open Deferment Group Screen
    [Documentation]    Navigate to the Deferment Group screen. Assumes the caller already
    ...    logged in this test case (via Login To EC Application) - this keyword ONLY
    ...    navigates. Delegates to the shared T1 Open EC Screen (common.resource) for the
    ...    actual mechanics.
    Open EC Screen    ${DEFERMENT_GROUP_SCREEN}

Insert Deferment Group Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties
    ...    And Verify Code, so deferment_group_iud.robot's test case body reads as a plain
    ...    business step with ZERO arguments. Also checks the inserted Code matches the
    ...    suite's ${TEST_CODE}. Pre-save evidence screenshot captured before Save is clicked,
    ...    matching Bank/State/Berth.
    [Arguments]    ${properties_path}=${DEFERMENT_GROUP_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Deferment Group Code
    RETURN    ${code}

Verify Deferment Group Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (no DB check here, matching Bank/State/Berth's TC02 convention): row
    ...    exists in the grid, then the form shows what was just inserted (Deferment Group
    ...    Code/Deferment Group Name only - Start Date is grid/insert-only, not present in
    ...    updateAttributes). Delegates the full sequence (row-check, select, form-compare,
    ...    screenshot) to the shared T2 Verify Object Insert Exists. Filters via Find
    ...    Deferment Group Row By Filter first, clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find Deferment Group Row By Filter    ${code}
    Verify Object Insert Exists    ${DEFERMENT_GROUP_TABLE}    ${code}    Deferment Group
    ...    ${DEFERMENT_GROUP_INSERT_PROPERTIES}    @{DEFERMENT_GROUP_FORM_LABELS}
    ...    code_label=Deferment Group Code
    Clear Deferment Group Row Filter

Update Deferment Group Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Pre-save evidence screenshot captured before Save is clicked, matching Bank/State/
    ...    Berth. Filters via Find Deferment Group Row By Filter first, clears after
    ...    (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${DEFERMENT_GROUP_UPDATE_PROPERTIES}
    Find Deferment Group Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${DEFERMENT_GROUP_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Deferment Group Code
    Clear Deferment Group Row Filter
    RETURN    ${data}

Verify Deferment Group Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification, matching Bank/State/Berth's TC03 convention: the form shows the
    ...    updated Deferment Group Name. Delegates the full sequence (select, form-compare,
    ...    screenshot) to the shared T2 Verify Object Form Record. Filters via Find Deferment
    ...    Group Row By Filter first, clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find Deferment Group Row By Filter    ${code}
    Verify Object Form Record    ${DEFERMENT_GROUP_TABLE}    ${code}    Deferment Group
    ...    ${DEFERMENT_GROUP_UPDATE_PROPERTIES}    Deferment Group Name    code_label=Deferment Group Code
    Clear Deferment Group Row Filter

Find Deferment Group Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Delegates the full select+capture sequence. Calls Find Deferment Group Row By
    ...    Filter first (2026-08-22 standardisation). Deliberately does NOT clear the filter
    ...    afterward - Verify Deferment Group Record Found (called right after, same TC) needs
    ...    the grid still filtered to ${code} for its own grid-check, since it doesn't
    ...    re-select the row itself; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Deferment Group Row By Filter    ${code}
    Find Object Record    ${DEFERMENT_GROUP_TABLE}    ${code}    Deferment Group    code_label=Deferment Group Code

Verify Deferment Group Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the form record match the expected (post-update) data. Delegates the full
    ...    sequence (grid-compare, form-compare, screenshot) to the shared T2 Verify Object
    ...    Found. Caller must already have selected the row (TC04 does, via Find Deferment
    ...    Group Record before this) AND left the Code filter active from that same call -
    ...    clears the filter itself once both checks are done (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${DEFERMENT_GROUP_TABLE}    ${code}    ${DEFERMENT_GROUP_GRID_VERIFY_PROPERTIES}
    ...    ${DEFERMENT_GROUP_FORM_VERIFY_PROPERTIES}    @{DEFERMENT_GROUP_FORM_LABELS}
    Clear Deferment Group Row Filter

Delete Deferment Group Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date,
    ...    called with ZERO arguments (defaults ${code}/${date} to the suite's
    ...    ${TEST_CODE}/${END_DATE}). Select the deferment group, set End Date = Start Date
    ...    (true delete), Save. Captures the TC05 evidence screenshot right after the End Date
    ...    is filled but BEFORE Save is clicked, matching Bank/State/Berth. Filters via Find
    ...    Deferment Group Row By Filter first, clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Deferment Group Row By Filter    ${code}
    Delete Object Via End Date    ${DEFERMENT_GROUP_TABLE}    ${DEFERMENT_GROUP_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Deferment Group Row Filter

Verify Deferment Group Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is
    ...    absent from BOTH the grid and the database.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${DEFERMENT_GROUP_TABLE}    OV_DEFERMENT_GROUP    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Deferment Group Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to
    ...    the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${DEFERMENT_GROUP_TABLE}    ${code}
