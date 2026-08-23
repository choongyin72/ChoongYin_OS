*** Settings ***
Documentation       T3 (screen) — Meter Run page object.
...                 Screen: Configuration > Assets > Stream Objects > Meter Run (CO.0091).
...                 Manage-Object (OV) screen. Holds Meter Run's locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common).
...                 Rebuilt 2026-08-23 (Batch 8) to mirror Bank/Berth exactly - replaces the
...                 older label-driven-only, no-properties-file, no-filter pattern with the
...                 properties-file-driven, grid-filter-wired, T2-consolidated pattern.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${METER_RUN_SCREEN}        Meter Run
${METER_RUN_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/meter_run_insert.properties
${METER_RUN_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/meter_run_update.properties
${METER_RUN_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/meter_run_form_verify.properties
${METER_RUN_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/meter_run_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal.
${METER_RUN_TABLE}      ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date), matching Bank/Berth's convention.
# Confirmed live 2026-08-23 (read-only recon, existing row): C:1=Start Date, C:3=End Date.
${METER_RUN_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Meter Run's own form-field label set. Labels are "Meter Run Code"/"Meter Run Name"
# (screen-prefixed) - confirmed via the already-proven Playwright driver py/meter_run_iud.py
# and the prior live-tested version of this page object; NOT the generic "Code"/"Name"
# Bank/Object List use. Start Date deliberately excluded - Insert-only, not present in
# updateAttributes (same as Bank/Berth). Defined ONCE here so both Verify Meter Run Record
# Exists (TC02) and Verify Meter Run Record Found (TC04) share the same list.
@{METER_RUN_FORM_LABELS}    Meter Run Code    Meter Run Name


*** Keywords ***
Find Meter Run Row By Filter
    [Documentation]    Explicitly filter the Meter Run grid's Code column to ${code} via the
    ...    shared T2 Find Object Row By Filter (resources/manage_object.resource) - matches
    ...    Account/Bank/Berth/State's own explicit filter usage, rather than relying only on
    ...    Select Object Row's implicit 3s-timeout fallback.
    [Arguments]    ${code}
    Find Object Row By Filter    ${METER_RUN_TABLE}    ${code}

Clear Meter Run Row Filter
    [Documentation]    Clear the Code column filter (see Find Meter Run Row By Filter) via the
    ...    shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${METER_RUN_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Meter Run's OWN credentials (${METER_RUN_EC_USER}/
    ...    ${METER_RUN_EC_PASS} from credentials.py) on the current page. Standing decision
    ...    (owner, 2026-08-22): every EC screen gets its own dedicated credential pair.
    ...    Zero-argument wrapper so meter_run_iud.robot's test cases read as a plain business
    ...    step; supplies Meter Run's own credential defaults to the shared T1 Login To EC
    ...    Screen (common.resource), which owns the actual login mechanics.
    Login To EC Screen    ${METER_RUN_EC_USER}    ${METER_RUN_EC_PASS}

Open Meter Run Screen
    [Documentation]    Navigate to the Meter Run screen. Assumes the caller already logged in
    ...    this test case (via Login To EC Application) - this keyword ONLY navigates.
    ...    Delegates to the shared T1 Open EC Screen (common.resource) for the actual mechanics.
    Open EC Screen    ${METER_RUN_SCREEN}

Insert Meter Run Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties
    ...    And Verify Code, so meter_run_iud.robot's test case body reads as a plain business
    ...    step with ZERO arguments. Also checks the inserted Code matches the suite's
    ...    ${TEST_CODE}. Pre-save evidence screenshot captured before Save is clicked,
    ...    matching Bank/Berth.
    [Arguments]    ${properties_path}=${METER_RUN_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Meter Run Code
    RETURN    ${code}

Verify Meter Run Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (no DB check here, matching Bank/Berth's TC02 convention): row exists
    ...    in the grid, then the form shows what was just inserted (Meter Run Code/Meter Run
    ...    Name only - Start Date is grid/insert-only, not present in updateAttributes).
    ...    Delegates the full sequence (row-check, select, form-compare, screenshot) to the
    ...    shared T2 Verify Object Insert Exists. Filters via Find Meter Run Row By Filter
    ...    first, clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find Meter Run Row By Filter    ${code}
    Verify Object Insert Exists    ${METER_RUN_TABLE}    ${code}    Meter Run
    ...    ${METER_RUN_INSERT_PROPERTIES}    @{METER_RUN_FORM_LABELS}    code_label=Meter Run Code
    Clear Meter Run Row Filter

Update Meter Run Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Pre-save evidence screenshot captured before Save is clicked, matching Bank/Berth.
    ...    Filters via Find Meter Run Row By Filter first, clears after (2026-08-22
    ...    standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${METER_RUN_UPDATE_PROPERTIES}
    Find Meter Run Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${METER_RUN_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Meter Run Code
    Clear Meter Run Row Filter
    RETURN    ${data}

Verify Meter Run Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification, matching Bank/Berth's TC03 convention: the form shows the updated
    ...    Meter Run Name. Delegates the full sequence (select, form-compare, screenshot) to
    ...    the shared T2 Verify Object Form Record. Filters via Find Meter Run Row By Filter
    ...    first, clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find Meter Run Row By Filter    ${code}
    Verify Object Form Record    ${METER_RUN_TABLE}    ${code}    Meter Run
    ...    ${METER_RUN_UPDATE_PROPERTIES}    Meter Run Name    code_label=Meter Run Code
    Clear Meter Run Row Filter

Find Meter Run Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Delegates the full select+capture sequence. Calls Find Meter Run Row By Filter
    ...    first (2026-08-22 standardisation). Deliberately does NOT clear the filter
    ...    afterward - Verify Meter Run Record Found (called right after, same TC) needs the
    ...    grid still filtered to ${code} for its own grid-check, since it doesn't re-select
    ...    the row itself; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Meter Run Row By Filter    ${code}
    Find Object Record    ${METER_RUN_TABLE}    ${code}    Meter Run    code_label=Meter Run Code

Verify Meter Run Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the form record match the expected (post-update) data. Delegates the full
    ...    sequence (grid-compare, form-compare, screenshot) to the shared T2 Verify Object
    ...    Found. Caller must already have selected the row (TC04 does, via Find Meter Run
    ...    Record before this) AND left the Code filter active from that same call - clears
    ...    the filter itself once both checks are done (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${METER_RUN_TABLE}    ${code}    ${METER_RUN_GRID_VERIFY_PROPERTIES}
    ...    ${METER_RUN_FORM_VERIFY_PROPERTIES}    @{METER_RUN_FORM_LABELS}
    Clear Meter Run Row Filter

Delete Meter Run Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date,
    ...    called with ZERO arguments (defaults ${code}/${date} to the suite's
    ...    ${TEST_CODE}/${END_DATE}). Select the meter run, set End Date = Start Date (true
    ...    delete), Save. Captures the TC05 evidence screenshot right after the End Date is
    ...    filled but BEFORE Save is clicked, matching Bank/Berth. Filters via Find Meter Run
    ...    Row By Filter first, clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Meter Run Row By Filter    ${code}
    Delete Object Via End Date    ${METER_RUN_TABLE}    ${METER_RUN_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Meter Run Row Filter

Verify Meter Run Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code}
    ...    is absent from BOTH the grid and the database.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${METER_RUN_TABLE}    OV_METER_RUN    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Meter Run Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to
    ...    the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${METER_RUN_TABLE}    ${code}
