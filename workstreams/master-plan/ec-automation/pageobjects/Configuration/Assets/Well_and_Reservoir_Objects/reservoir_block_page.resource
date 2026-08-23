*** Settings ***
Documentation       T3 (screen) — Reservoir Block page object.
...                 Screen: Configuration > Assets > Well_and_Reservoir_Objects > Reservoir Block (CO.0133).
...                 Manage-Object (OV) screen. Holds Reservoir Block's locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common).
...                 Rebuilt 2026-08-23 (Batch 9) to mirror Bank/Berth exactly — replaces the
...                 older label-driven-only pattern (no properties files, no grid-filter
...                 wiring) with the label-driven, properties-file-driven, grid-filter-wired,
...                 T2-consolidated pattern.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${RESERVOIR_BLOCK_SCREEN}    Reservoir Block
${RESERVOIR_BLOCK_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/reservoir_block_insert.properties
${RESERVOIR_BLOCK_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/reservoir_block_update.properties
${RESERVOIR_BLOCK_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/reservoir_block_form_verify.properties
${RESERVOIR_BLOCK_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/reservoir_block_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal.
${RESERVOIR_BLOCK_TABLE}    ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date), matching Bank/Berth's convention -
# confirmed identical across every screen in this Well_and_Reservoir_Objects family
# (choke/perf_interval/well_bore_interval/well_bore/well_hole/well_page all use this same id).
${RESERVOIR_BLOCK_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Reservoir Block's own form-field label set. Labels are "Reservoir Block Code"/"Reservoir
# Block Name" (screen-prefixed) — confirmed via the already-proven Playwright driver
# py/reservoir_block_iud.py (INSERT_FIELDS) and the prior label-driven page object (this file,
# pre-rebuild); NOT the generic "Code"/"Name" Bank/Object List use.
# Start Date deliberately excluded — Insert-only, not present in updateAttributes (same as
# Bank/Berth). Defined ONCE here so both Verify Reservoir Block Record Exists (TC02) and
# Verify Reservoir Block Record Found (TC04) share the same list.
@{RESERVOIR_BLOCK_FORM_LABELS}    Reservoir Block Code    Reservoir Block Name


*** Keywords ***
Find Reservoir Block Row By Filter
    [Documentation]    Explicitly filter the Reservoir Block grid's Code column to ${code} via
    ...    the shared T2 Find Object Row By Filter (resources/manage_object.resource) —
    ...    matches Account/Bank/Berth/State's own explicit filter usage (owner, 2026-08-22:
    ...    "others (Bank, State, List_Object) should follow Account... utilise same filter
    ...    feature"), rather than relying only on Select Object Row's implicit 3s-timeout
    ...    fallback.
    [Arguments]    ${code}
    Find Object Row By Filter    ${RESERVOIR_BLOCK_TABLE}    ${code}

Clear Reservoir Block Row Filter
    [Documentation]    Clear the Code column filter (see Find Reservoir Block Row By Filter)
    ...    via the shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered
    ...    view.
    Clear Object Row Filter    ${RESERVOIR_BLOCK_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Reservoir Block's OWN credentials
    ...    (${RESERVOIR_BLOCK_EC_USER}/${RESERVOIR_BLOCK_EC_PASS} from credentials.py) on the
    ...    current page. Standing decision (owner, 2026-08-22): every EC screen gets its own
    ...    dedicated credential pair. Zero-argument wrapper so reservoir_block_iud.robot's
    ...    test cases read as a plain business step; supplies Reservoir Block's own credential
    ...    defaults to the shared T1 Login To EC Screen (common.resource), which owns the
    ...    actual login mechanics.
    Login To EC Screen    ${RESERVOIR_BLOCK_EC_USER}    ${RESERVOIR_BLOCK_EC_PASS}

Open Reservoir Block Screen
    [Documentation]    Navigate to the Reservoir Block screen. Assumes the caller already
    ...    logged in this test case (via Login To EC Application) — this keyword ONLY
    ...    navigates. Delegates to the shared T1 Open EC Screen (common.resource) for the
    ...    actual mechanics.
    Open EC Screen    ${RESERVOIR_BLOCK_SCREEN}

Insert Reservoir Block Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties
    ...    And Verify Code, so reservoir_block_iud.robot's test case body reads as a plain
    ...    business step with ZERO arguments. Also checks the inserted Code matches the
    ...    suite's ${TEST_CODE}. Pre-save evidence screenshot captured before Save is clicked,
    ...    matching Bank/Berth.
    [Arguments]    ${properties_path}=${RESERVOIR_BLOCK_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Reservoir Block Code
    RETURN    ${code}

Verify Reservoir Block Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (no DB check here, matching Bank/Berth's TC02 convention): row exists
    ...    in the grid, then the form shows what was just inserted (Reservoir Block
    ...    Code/Reservoir Block Name only — Start Date is grid/insert-only, not present in
    ...    updateAttributes). Delegates the full sequence (row-check, select, form-compare,
    ...    screenshot) to the shared T2 Verify Object Insert Exists.
    ...    Filters via Find Reservoir Block Row By Filter first, clears after (2026-08-22
    ...    standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find Reservoir Block Row By Filter    ${code}
    Verify Object Insert Exists    ${RESERVOIR_BLOCK_TABLE}    ${code}    Reservoir Block
    ...    ${RESERVOIR_BLOCK_INSERT_PROPERTIES}    @{RESERVOIR_BLOCK_FORM_LABELS}
    ...    code_label=Reservoir Block Code
    Clear Reservoir Block Row Filter

Update Reservoir Block Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Pre-save evidence screenshot captured before Save is clicked, matching Bank/Berth.
    ...    Filters via Find Reservoir Block Row By Filter first, clears after (2026-08-22
    ...    standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${RESERVOIR_BLOCK_UPDATE_PROPERTIES}
    Find Reservoir Block Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${RESERVOIR_BLOCK_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Reservoir Block Code
    Clear Reservoir Block Row Filter
    RETURN    ${data}

Verify Reservoir Block Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification, matching Bank/Berth's TC03 convention: the form shows the updated
    ...    Reservoir Block Name. Delegates the full sequence (select, form-compare,
    ...    screenshot) to the shared T2 Verify Object Form Record. Filters via Find Reservoir
    ...    Block Row By Filter first, clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find Reservoir Block Row By Filter    ${code}
    Verify Object Form Record    ${RESERVOIR_BLOCK_TABLE}    ${code}    Reservoir Block
    ...    ${RESERVOIR_BLOCK_UPDATE_PROPERTIES}    Reservoir Block Name
    ...    code_label=Reservoir Block Code
    Clear Reservoir Block Row Filter

Find Reservoir Block Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Delegates the full select+capture sequence. Calls Find Reservoir Block Row By
    ...    Filter first (2026-08-22 standardisation). Deliberately does NOT clear the filter
    ...    afterward — Verify Reservoir Block Record Found (called right after, same TC)
    ...    needs the grid still filtered to ${code} for its own grid-check, since it doesn't
    ...    re-select the row itself; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Reservoir Block Row By Filter    ${code}
    Find Object Record    ${RESERVOIR_BLOCK_TABLE}    ${code}    Reservoir Block
    ...    code_label=Reservoir Block Code

Verify Reservoir Block Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the form record match the expected (post-update) data. Delegates the full
    ...    sequence (grid-compare, form-compare, screenshot) to the shared T2 Verify Object
    ...    Found. Caller must already have selected the row (TC04 does, via Find Reservoir
    ...    Block Record before this) AND left the Code filter active from that same call —
    ...    clears the filter itself once both checks are done (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${RESERVOIR_BLOCK_TABLE}    ${code}    ${RESERVOIR_BLOCK_GRID_VERIFY_PROPERTIES}
    ...    ${RESERVOIR_BLOCK_FORM_VERIFY_PROPERTIES}    @{RESERVOIR_BLOCK_FORM_LABELS}
    Clear Reservoir Block Row Filter

Delete Reservoir Block Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date,
    ...    called with ZERO arguments (defaults ${code}/${date} to the suite's
    ...    ${TEST_CODE}/${END_DATE}). Select the reservoir block, set End Date = Start Date
    ...    (true delete), Save. Captures the TC05 evidence screenshot right after the End
    ...    Date is filled but BEFORE Save is clicked, matching Bank/Berth's convention.
    ...    Filters via Find Reservoir Block Row By Filter first, clears after (2026-08-22
    ...    standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Reservoir Block Row By Filter    ${code}
    Delete Object Via End Date    ${RESERVOIR_BLOCK_TABLE}    ${RESERVOIR_BLOCK_DEL_ENDDATE}    ${code}
    ...    ${date}    ${TEST NAME}_action
    Clear Reservoir Block Row Filter

Verify Reservoir Block Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is
    ...    absent from BOTH the grid and the database.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${RESERVOIR_BLOCK_TABLE}    OV_RESV_BLOCK    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Reservoir Block Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to
    ...    the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${RESERVOIR_BLOCK_TABLE}    ${code}
