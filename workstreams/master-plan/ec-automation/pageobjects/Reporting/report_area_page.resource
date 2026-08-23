*** Settings ***
Documentation       T3 (screen) - Report Area page object.
...                 Screen: Reporting > Report Area (RP.0017). Manage-Object (OV) screen.
...                 Simplest OV: Code / Name / Start Date (no Description, no dropdowns).
...                 Rebuilt 2026-08-23 (Batch 9) to mirror Bank/Berth exactly - replaces the
...                 older no-properties/no-filter pattern with the label-driven,
...                 properties-file-driven, grid-filter-wired, T2-consolidated pattern.

Library             Browser
Library             ../../libraries/DbVerify.py
Library             ../../libraries/PropertiesReader.py
Resource            ../../resources/common.resource
Resource            ../../resources/manage_object.resource
Variables           ../../resources/credentials.py


*** Variables ***
${RPTA_SCREEN}          Report Area
${RPTA_INSERT_PROPERTIES}    ${CURDIR}/../../testdata/report_area_insert.properties
${RPTA_UPDATE_PROPERTIES}    ${CURDIR}/../../testdata/report_area_update.properties
${RPTA_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../testdata/report_area_form_verify.properties
${RPTA_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../testdata/report_area_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal.
${RPTA_TABLE}           ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date), matching Bank/Berth's convention.
${RPTA_DEL_ENDDATE}     tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Report Area's own form-field label set. Labels are "Report Area Code"/"Report Area Name"
# (screen-prefixed) - confirmed via the pre-existing page object and the already-proven
# Playwright driver py/report_area_iud.py; NOT the generic "Code"/"Name" Bank/Object List use.
# Start Date deliberately excluded - Insert-only, not present in updateAttributes (same as
# Bank/Berth). Defined ONCE here so both Verify Report Area Record Exists (TC02) and Verify
# Report Area Record Found (TC04) share the same list.
@{RPTA_FORM_LABELS}    Report Area Code    Report Area Name


*** Keywords ***
Find Report Area Row By Filter
    [Documentation]    Explicitly filter the Report Area grid's Code column to ${code} via the
    ...    shared T2 Find Object Row By Filter (resources/manage_object.resource) - matches
    ...    Account/Bank/Berth/State's own explicit filter usage, rather than relying only on
    ...    Select Object Row's implicit 3s-timeout fallback.
    [Arguments]    ${code}
    Find Object Row By Filter    ${RPTA_TABLE}    ${code}

Clear Report Area Row Filter
    [Documentation]    Clear the Code column filter (see Find Report Area Row By Filter) via
    ...    the shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${RPTA_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Report Area's OWN credentials (${REPORT_AREA_EC_USER}/
    ...    ${REPORT_AREA_EC_PASS} from credentials.py) on the current page. Standing decision
    ...    (owner, 2026-08-22): every EC screen gets its own dedicated credential pair.
    ...    Zero-argument wrapper so report_area_iud.robot's test cases read as a plain
    ...    business step; supplies Report Area's own credential defaults to the shared T1
    ...    Login To EC Screen (common.resource), which owns the actual login mechanics.
    Login To EC Screen    ${REPORT_AREA_EC_USER}    ${REPORT_AREA_EC_PASS}

Open Report Area Screen
    [Documentation]    Navigate to the Report Area screen, then load the list (grid needs GO
    ...    to populate - no default rows on open). Assumes the caller already logged in this
    ...    test case (via Login To EC Application) - this keyword ONLY navigates + loads.
    ...    Delegates to the shared T1 Open EC Screen (common.resource) for the actual
    ...    navigation mechanics.
    Open EC Screen    ${RPTA_SCREEN}
    Apply Navigator

Insert Report Area Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties
    ...    And Verify Code, so report_area_iud.robot's test case body reads as a plain
    ...    business step with ZERO arguments. Also checks the inserted Code matches the
    ...    suite's ${TEST_CODE}. Pre-save evidence screenshot captured before Save is clicked,
    ...    matching Bank/Berth.
    [Arguments]    ${properties_path}=${RPTA_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Report Area Code
    RETURN    ${code}

Verify Report Area Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (no DB check here, matching Bank/Berth's TC02 convention): row exists
    ...    in the grid, then the form shows what was just inserted (Report Area Code/Report
    ...    Area Name only - Start Date is grid/insert-only, not present in updateAttributes).
    ...    Delegates the full sequence (row-check, select, form-compare, screenshot) to the
    ...    shared T2 Verify Object Insert Exists. Filters via Find Report Area Row By Filter
    ...    first, clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find Report Area Row By Filter    ${code}
    Verify Object Insert Exists    ${RPTA_TABLE}    ${code}    Report Area    ${RPTA_INSERT_PROPERTIES}
    ...    @{RPTA_FORM_LABELS}    code_label=Report Area Code
    Clear Report Area Row Filter

Update Report Area Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Pre-save evidence screenshot captured before Save is clicked, matching Bank/Berth.
    ...    Filters via Find Report Area Row By Filter first, clears after (2026-08-22
    ...    standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${RPTA_UPDATE_PROPERTIES}
    Find Report Area Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${RPTA_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Report Area Code
    Clear Report Area Row Filter
    RETURN    ${data}

Verify Report Area Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification, matching Bank/Berth's TC03 convention: the form shows the updated
    ...    Report Area Name. Delegates the full sequence (select, form-compare, screenshot)
    ...    to the shared T2 Verify Object Form Record. Filters via Find Report Area Row By
    ...    Filter first, clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find Report Area Row By Filter    ${code}
    Verify Object Form Record    ${RPTA_TABLE}    ${code}    Report Area    ${RPTA_UPDATE_PROPERTIES}
    ...    Report Area Name    code_label=Report Area Code
    Clear Report Area Row Filter

Find Report Area Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Delegates the full select+capture sequence. Calls Find Report Area Row By Filter
    ...    first (2026-08-22 standardisation). Deliberately does NOT clear the filter
    ...    afterward - Verify Report Area Record Found (called right after, same TC) needs
    ...    the grid still filtered to ${code} for its own grid-check, since it doesn't
    ...    re-select the row itself; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Report Area Row By Filter    ${code}
    Find Object Record    ${RPTA_TABLE}    ${code}    Report Area    code_label=Report Area Code

Verify Report Area Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the form record match the expected (post-update) data. Delegates the full
    ...    sequence (grid-compare, form-compare, screenshot) to the shared T2 Verify Object
    ...    Found. Caller must already have selected the row (TC04 does, via Find Report Area
    ...    Record before this) AND left the Code filter active from that same call - clears
    ...    the filter itself once both checks are done (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${RPTA_TABLE}    ${code}    ${RPTA_GRID_VERIFY_PROPERTIES}
    ...    ${RPTA_FORM_VERIFY_PROPERTIES}    @{RPTA_FORM_LABELS}
    Clear Report Area Row Filter

Delete Report Area Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date,
    ...    called with ZERO arguments (defaults ${code}/${date} to the suite's
    ...    ${TEST_CODE}/${END_DATE}). Select the report area, set End Date = Start Date (true
    ...    delete), Save. Captures the TC05 evidence screenshot right after the End Date is
    ...    filled but BEFORE Save is clicked, matching Bank/Berth. Filters via Find Report
    ...    Area Row By Filter first, clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Report Area Row By Filter    ${code}
    Delete Object Via End Date    ${RPTA_TABLE}    ${RPTA_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Report Area Row Filter

Verify Report Area Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is
    ...    absent from BOTH the grid and the database.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${RPTA_TABLE}    OV_REPORT_AREA    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Report Area Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to
    ...    the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${RPTA_TABLE}    ${code}
