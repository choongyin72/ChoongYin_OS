*** Settings ***
Documentation       T3 (screen) — Stream Item Category page object.
...                 Screen: Configuration > Assets > Stream_Objects > Stream Item Category (CD.0016).
...                 Manage-Object (OV) screen. Rebuilt (Batch 10) to bring this screen up to the
...                 SAME full shape as Bank/Berth: label-driven (already had this), plus
...                 properties-file-driven insert/update/verify + explicit grid-filter wiring
...                 (both were missing before this change).
...                 OV object-config: Code / Name / Start Date mandatory (optional dropdowns
...                 skipped) - confirmed against the already-proven Playwright driver
...                 py/stream_item_category_iud.py (INSERT_FIELDS/UPDATE_FIELDS).
...                 NO hardcoded field ids: grid = shared T2 ${OV_MANAGE_OBJECT_TABLE};
...                 fields resolved by LABEL via T2 (Fill OV * By Label / Fill OV Field By
...                 Label Any Kind). GENERIC "Code"/"Name" labels (NOT screen-prefixed -
...                 confirmed via direct grep per batch10 shared findings).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${STREAM_ITEM_CATEGORY_SCREEN}          Stream Item Category
${STREAM_ITEM_CATEGORY_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/stream_item_category_insert.properties
${STREAM_ITEM_CATEGORY_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/stream_item_category_update.properties
${STREAM_ITEM_CATEGORY_FORM_VERIFY_PROPS}    ${CURDIR}/../../../../testdata/stream_item_category_form_verify.properties
${STREAM_ITEM_CATEGORY_GRID_VERIFY_PROPS}    ${CURDIR}/../../../../testdata/stream_item_category_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal.
${STREAM_ITEM_CATEGORY_TABLE}          ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date), matching Bank/Berth's convention
# (same framework-invariant objectdates row shape: Start Date C:1, End Date C:3). TO BE
# LIVE-VERIFIED same as Bank/Berth's own note - kept hardcoded per that already-proven
# precedent rather than a fresh guess.
${STREAM_ITEM_CATEGORY_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Stream Item Category's own form-field label set for updateAttributes round-trip checks.
# Start Date is EXCLUDED here (lives in objectForm at Insert time only, matching Bank/Berth's
# documented exclusion - confirmed against the existing driver, which only ever fills Name in
# UPDATE_FIELDS, never Start Date, implying it is not present/editable in updateAttributes).
@{STREAM_ITEM_CATEGORY_FORM_LABELS}    Code    Name


*** Keywords ***
Find Stream Item Category Row By Filter
    [Documentation]    Explicitly filter the Stream Item Category grid's Code column to ${code}
    ...    via the shared T2 Find Object Row By Filter (resources/manage_object.resource) -
    ...    matches Bank/Berth's own explicit filter usage (owner, 2026-08-22: "others...
    ...    should follow Account... utilise same filter feature"), rather than relying only on
    ...    Select Object Row's implicit 3s-timeout fallback.
    [Arguments]    ${code}
    Find Object Row By Filter    ${STREAM_ITEM_CATEGORY_TABLE}    ${code}

Clear Stream Item Category Row Filter
    [Documentation]    Clear the Code column filter (see Find Stream Item Category Row By
    ...    Filter) via the shared T2 Clear Object Row Filter, restoring the grid's normal
    ...    unfiltered view.
    Clear Object Row Filter    ${STREAM_ITEM_CATEGORY_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Stream Item Category's OWN credentials
    ...    (${STREAM_ITEM_CATEGORY_EC_USER}/${STREAM_ITEM_CATEGORY_EC_PASS} from
    ...    credentials.py) on the current page. Standing decision (owner, 2026-08-22): every
    ...    EC screen gets its own dedicated credential pair. Zero-argument wrapper so
    ...    stream_item_category_iud.robot's test cases read as a plain business step;
    ...    supplies this screen's own credential defaults to the shared T1 Login To EC
    ...    Screen (common.resource), which owns the actual login mechanics.
    Login To EC Screen    ${STREAM_ITEM_CATEGORY_EC_USER}    ${STREAM_ITEM_CATEGORY_EC_PASS}

Open Stream Item Category Screen
    [Documentation]    Navigate to the Stream Item Category screen. Assumes the caller
    ...    already logged in this test case (via Login To EC Application) - this keyword
    ...    ONLY navigates. Delegates to the shared T1 Open EC Screen (common.resource) for
    ...    the actual mechanics. Applies the navigator GO afterward (grid needs GO to
    ...    populate - no default rows on open, matching the pre-existing behavior).
    Open EC Screen    ${STREAM_ITEM_CATEGORY_SCREEN}
    Apply Navigator

Insert Stream Item Category Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties
    ...    And Verify Code, so stream_item_category_iud.robot's test case body reads as a
    ...    plain business step with ZERO arguments. Also checks the inserted Code matches the
    ...    suite's ${TEST_CODE}. Pre-save evidence screenshot captured before Save is clicked,
    ...    matching Bank/Berth.
    [Arguments]    ${properties_path}=${STREAM_ITEM_CATEGORY_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action
    RETURN    ${code}

Verify Stream Item Category Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (no DB check here, matching Bank/Berth's TC02 convention): row exists
    ...    in the grid, then the form shows what was just inserted (Code/Name only - Start
    ...    Date is objectForm/insert-only, not present in updateAttributes). Delegates the
    ...    full sequence (row-check, select, form-compare, screenshot) to the shared T2
    ...    Verify Object Insert Exists. Filters via Find Stream Item Category Row By Filter
    ...    first, clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find Stream Item Category Row By Filter    ${code}
    Verify Object Insert Exists    ${STREAM_ITEM_CATEGORY_TABLE}    ${code}    Stream Item Category
    ...    ${STREAM_ITEM_CATEGORY_INSERT_PROPERTIES}    @{STREAM_ITEM_CATEGORY_FORM_LABELS}
    Clear Stream Item Category Row Filter

Update Stream Item Category Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Pre-save evidence screenshot captured before Save is clicked, matching Bank/Berth.
    ...    Filters via Find Stream Item Category Row By Filter first, clears after
    ...    (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${STREAM_ITEM_CATEGORY_UPDATE_PROPERTIES}
    Find Stream Item Category Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${STREAM_ITEM_CATEGORY_TABLE}    ${code}
    ...    ${properties_path}    ${TEST NAME}_action
    Clear Stream Item Category Row Filter
    RETURN    ${data}

Verify Stream Item Category Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification, matching Bank/Berth's TC03 convention: the form shows the updated
    ...    Name. Delegates the full sequence (select, form-compare, screenshot) to the shared
    ...    T2 Verify Object Form Record. Filters via Find Stream Item Category Row By Filter
    ...    first, clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find Stream Item Category Row By Filter    ${code}
    Verify Object Form Record    ${STREAM_ITEM_CATEGORY_TABLE}    ${code}    Stream Item Category
    ...    ${STREAM_ITEM_CATEGORY_UPDATE_PROPERTIES}    Name
    Clear Stream Item Category Row Filter

Find Stream Item Category Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Delegates the full select+capture sequence. Calls Find Stream Item Category Row By
    ...    Filter first (2026-08-22 standardisation). Deliberately does NOT clear the filter
    ...    afterward - Verify Stream Item Category Record Found (called right after, same TC)
    ...    needs the grid still filtered to ${code} for its own grid-check, since it doesn't
    ...    re-select the row itself; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Stream Item Category Row By Filter    ${code}
    Find Object Record    ${STREAM_ITEM_CATEGORY_TABLE}    ${code}    Stream Item Category

Verify Stream Item Category Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the form record match the expected (post-update) data. Delegates the full
    ...    sequence (grid-compare, form-compare, screenshot) to the shared T2 Verify Object
    ...    Found. Caller must already have selected the row (TC04 does, via Find Stream Item
    ...    Category Record before this) AND left the Code filter active from that same call -
    ...    clears the filter itself once both checks are done (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${STREAM_ITEM_CATEGORY_TABLE}    ${code}
    ...    ${STREAM_ITEM_CATEGORY_GRID_VERIFY_PROPS}    ${STREAM_ITEM_CATEGORY_FORM_VERIFY_PROPS}
    ...    @{STREAM_ITEM_CATEGORY_FORM_LABELS}
    Clear Stream Item Category Row Filter

Delete Stream Item Category Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date,
    ...    called with ZERO arguments (defaults ${code}/${date} to the suite's
    ...    ${TEST_CODE}/${END_DATE}). Select the stream_item_category, set End Date = Start
    ...    Date (true delete), Save. Captures the TC05 evidence screenshot right after the End
    ...    Date is filled but BEFORE Save is clicked, matching Bank/Berth's convention.
    ...    Filters via Find Stream Item Category Row By Filter first, clears after
    ...    (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Stream Item Category Row By Filter    ${code}
    Delete Object Via End Date    ${STREAM_ITEM_CATEGORY_TABLE}    ${STREAM_ITEM_CATEGORY_DEL_ENDDATE}
    ...    ${code}    ${date}    ${TEST NAME}_action
    Clear Stream Item Category Row Filter

Verify Stream Item Category Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is
    ...    absent from BOTH the grid and the database (OV_STREAM_ITEM_CATEGORY).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${STREAM_ITEM_CATEGORY_TABLE}    OV_STREAM_ITEM_CATEGORY    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Stream Item Category Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to
    ...    the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${STREAM_ITEM_CATEGORY_TABLE}    ${code}
