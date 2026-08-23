*** Settings ***
Documentation       T3 (screen) — Trailer page object.
...                 Screen: Configuration > Assets > Transport_Objects > Trailer.
...                 PLAIN OV (Bank family): navigator is date-only - GO populates the grid (no
...                 mandatory cascade). Fields resolved BY LABEL (no hardcoded rows); extra
...                 mandatory dropdowns first-available. DELETE = End Date = Start Date.
...                 Rebuilt 2026-08-23 (Batch 10) to mirror Bank/Berth exactly - replaces the
...                 label-driven-but-hardcoded-arguments pattern with the label-driven,
...                 properties-file-driven, grid-filter-wired, T2-consolidated pattern.
...                 Grid id trailer_object:form:T_data is Trailer's OWN grid id (NOT the
...                 invariant manage_object_nav_nav:form:T_data most manage-object screens
...                 share) - confirmed via the already-proven Playwright driver
...                 py/trailer_iud.py (GRID_DATA_ID), kept unchanged from the pre-existing
...                 page object rather than assumed to match Bank/Berth's shared constant.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${TRAILER_SCREEN}          Trailer
${TRAILER_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/trailer_insert.properties
${TRAILER_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/trailer_update.properties
${TRAILER_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/trailer_form_verify.properties
${TRAILER_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/trailer_grid_verify.properties
# Trailer's OWN grid id (see Documentation above) - NOT ${OV_MANAGE_OBJECT_TABLE}.
${TRAILER_TABLE}           trailer_object:form:T_data
# objectdates field ID (Delete — End Date = Start Date), matching Bank/Berth's convention.
${TRAILER_DEL_ENDDATE}     tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Trailer's own form-field label set. Labels are "Trailer Code"/"Trailer Name" (screen-prefixed) -
# confirmed via direct grep and the already-proven Playwright driver py/trailer_iud.py; NOT the
# generic "Code"/"Name" Bank/Object List use. Only Trailer Code/Trailer Name are used for the
# round-trip form compare - Start Date is Insert-only (not in updateAttributes) and the
# Trailer Type/UOM/Transport Company dropdowns are excluded (can re-render Description text
# instead of code after reload - not a stable live-DOM comparison target). Defined ONCE here so
# both Verify Trailer Record Exists (TC02) and Verify Trailer Record Found (TC04) share the
# same list.
@{TRAILER_FORM_LABELS}    Trailer Code    Trailer Name


*** Keywords ***
Find Trailer Row By Filter
    [Documentation]    Explicitly filter the Trailer grid's Code column to ${code} via the
    ...    shared T2 Find Object Row By Filter (resources/manage_object.resource) - matches
    ...    Account/Bank/Berth/State's own explicit filter usage (owner, 2026-08-22: "others
    ...    (Bank, State, List_Object) should follow Account... utilise same filter feature"),
    ...    rather than relying only on Select Object Row's implicit 3s-timeout fallback.
    [Arguments]    ${code}
    Find Object Row By Filter    ${TRAILER_TABLE}    ${code}

Clear Trailer Row Filter
    [Documentation]    Clear the Code column filter (see Find Trailer Row By Filter) via the
    ...    shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${TRAILER_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Trailer's OWN credentials (${TRAILER_EC_USER}/
    ...    ${TRAILER_EC_PASS} from credentials.py) on the current page. Standing decision
    ...    (owner, 2026-08-22): every EC screen gets its own dedicated credential pair.
    ...    Zero-argument wrapper so trailer_iud.robot's test cases read as a plain business
    ...    step; supplies Trailer's own credential defaults to the shared T1 Login To EC
    ...    Screen (common.resource), which owns the actual login mechanics.
    Login To EC Screen    ${TRAILER_EC_USER}    ${TRAILER_EC_PASS}

Open Trailer Screen
    [Documentation]    Navigate to the Trailer screen, then GO (date-only navigator - no
    ...    mandatory cascade) to populate the grid. Assumes the caller already logged in
    ...    this test case (via Login To EC Application).
    Open EC Screen    ${TRAILER_SCREEN}
    Apply Navigator

Insert Trailer Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties
    ...    And Verify Code, so trailer_iud.robot's test case body reads as a plain business
    ...    step with ZERO arguments. Also checks the inserted Code matches the suite's
    ...    ${TEST_CODE}. Pre-save evidence screenshot captured before Save is clicked,
    ...    matching Bank/Berth.
    [Arguments]    ${properties_path}=${TRAILER_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Trailer Code
    RETURN    ${code}

Verify Trailer Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (no DB check here, matching Bank/Berth's TC02 convention): row
    ...    exists in the grid, then the form shows what was just inserted (Trailer
    ...    Code/Trailer Name only - Start Date/dropdowns excluded, see @{TRAILER_FORM_LABELS}
    ...    docs). Delegates the full sequence (row-check, select, form-compare, screenshot)
    ...    to the shared T2 Verify Object Insert Exists. Filters via Find Trailer Row By
    ...    Filter first, clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find Trailer Row By Filter    ${code}
    Verify Object Insert Exists    ${TRAILER_TABLE}    ${code}    Trailer    ${TRAILER_INSERT_PROPERTIES}
    ...    @{TRAILER_FORM_LABELS}    code_label=Trailer Code
    Clear Trailer Row Filter

Update Trailer Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Pre-save evidence screenshot captured before Save is clicked, matching Bank/Berth.
    ...    Filters via Find Trailer Row By Filter first, clears after (2026-08-22
    ...    standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${TRAILER_UPDATE_PROPERTIES}
    Find Trailer Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${TRAILER_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Trailer Code
    Clear Trailer Row Filter
    RETURN    ${data}

Verify Trailer Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification, matching Bank/Berth's TC03 convention: the form shows the updated
    ...    Trailer Name. Delegates the full sequence (select, form-compare, screenshot) to
    ...    the shared T2 Verify Object Form Record. Filters via Find Trailer Row By Filter
    ...    first, clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find Trailer Row By Filter    ${code}
    Verify Object Form Record    ${TRAILER_TABLE}    ${code}    Trailer    ${TRAILER_UPDATE_PROPERTIES}
    ...    Trailer Name    code_label=Trailer Code
    Clear Trailer Row Filter

Find Trailer Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Delegates the full select+capture sequence. Calls Find Trailer Row By Filter first
    ...    (2026-08-22 standardisation). Deliberately does NOT clear the filter afterward -
    ...    Verify Trailer Record Found (called right after, same TC) needs the grid still
    ...    filtered to ${code} for its own grid-check, since it doesn't re-select the row
    ...    itself; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Trailer Row By Filter    ${code}
    Find Object Record    ${TRAILER_TABLE}    ${code}    Trailer    code_label=Trailer Code

Verify Trailer Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the form record match the expected (post-update) data. Delegates the
    ...    full sequence (grid-compare, form-compare, screenshot) to the shared T2 Verify
    ...    Object Found. Caller must already have selected the row (TC04 does, via Find
    ...    Trailer Record before this) AND left the Code filter active from that same call -
    ...    clears the filter itself once both checks are done (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${TRAILER_TABLE}    ${code}    ${TRAILER_GRID_VERIFY_PROPERTIES}
    ...    ${TRAILER_FORM_VERIFY_PROPERTIES}    @{TRAILER_FORM_LABELS}
    Clear Trailer Row Filter

Delete Trailer Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date,
    ...    called with ZERO arguments (defaults ${code}/${date} to the suite's
    ...    ${TEST_CODE}/${END_DATE}). Select the trailer, set End Date = Start Date (true
    ...    delete), Save. Captures the TC05 evidence screenshot right after the End Date is
    ...    filled but BEFORE Save is clicked, matching Bank/Berth's convention.
    ...    Filters via Find Trailer Row By Filter first, clears after (2026-08-22
    ...    standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Trailer Row By Filter    ${code}
    Delete Object Via End Date    ${TRAILER_TABLE}    ${TRAILER_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Trailer Row Filter

Verify Trailer Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code}
    ...    is absent from BOTH the grid and the database.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${TRAILER_TABLE}    OV_TRAILER    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Trailer Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to
    ...    the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${TRAILER_TABLE}    ${code}
