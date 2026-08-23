*** Settings ***
Documentation       T3 (screen) — Orifice Plate page object.
...                 Screen: Configuration > Assets > Stream_Objects > Orifice Plate (CO.0089).
...                 Manage-Object (OV) screen. Holds Orifice Plate's locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common).
...                 Rebuilt 2026-08-23 (Batch 8) to mirror Bank/Berth exactly — replaces the
...                 older generated-code/no-filter pattern with the label-driven,
...                 properties-file-driven, grid-filter-wired, T2-consolidated pattern.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${ORIFICE_PLATE_SCREEN}    Orifice Plate
${ORIFICE_PLATE_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/orifice_plate_insert.properties
${ORIFICE_PLATE_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/orifice_plate_update.properties
${ORIFICE_PLATE_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/orifice_plate_form_verify.properties
${ORIFICE_PLATE_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/orifice_plate_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal.
${ORIFICE_PLATE_TABLE}    ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date), matching Bank/Berth's convention.
${ORIFICE_PLATE_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Orifice Plate's own form-field label set. Labels are "Orifice Code"/"Orifice Name"
# (screen-prefixed) — confirmed via ec-ui-knowledge/screens/orifice_plate.md (fresh scan
# 2026-07-26) and the already-proven Playwright driver py/orifice_plate_iud.py; NOT the
# generic "Code"/"Name" Bank/Object List use. Start Date deliberately excluded — Insert-only,
# not present in updateAttributes (same as Bank/Berth). Defined ONCE here so both Verify
# Orifice Plate Record Exists (TC02) and Verify Orifice Plate Record Found (TC04) share the
# same list.
@{ORIFICE_PLATE_FORM_LABELS}    Orifice Code    Orifice Name


*** Keywords ***
Find Orifice Plate Row By Filter
    [Documentation]    Explicitly filter the Orifice Plate grid's Code column to ${code} via
    ...    the shared T2 Find Object Row By Filter (resources/manage_object.resource) —
    ...    matches Account/Bank/Berth/State's own explicit filter usage (owner, 2026-08-22:
    ...    "others (Bank, State, List_Object) should follow Account... utilise same filter
    ...    feature"), rather than relying only on Select Object Row's implicit 3s-timeout
    ...    fallback.
    [Arguments]    ${code}
    Find Object Row By Filter    ${ORIFICE_PLATE_TABLE}    ${code}

Clear Orifice Plate Row Filter
    [Documentation]    Clear the Code column filter (see Find Orifice Plate Row By Filter) via
    ...    the shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${ORIFICE_PLATE_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Orifice Plate's OWN credentials
    ...    (${ORIFICE_PLATE_EC_USER}/${ORIFICE_PLATE_EC_PASS} from credentials.py) on the
    ...    current page. Standing decision (owner, 2026-08-22): every EC screen gets its own
    ...    dedicated credential pair. Zero-argument wrapper so orifice_plate_iud.robot's test
    ...    cases read as a plain business step; supplies Orifice Plate's own credential
    ...    defaults to the shared T1 Login To EC Screen (common.resource), which owns the
    ...    actual login mechanics.
    Login To EC Screen    ${ORIFICE_PLATE_EC_USER}    ${ORIFICE_PLATE_EC_PASS}

Open Orifice Plate Screen
    [Documentation]    Navigate to the Orifice Plate screen. Assumes the caller already
    ...    logged in this test case (via Login To EC Application) — this keyword ONLY
    ...    navigates. Delegates to the shared T1 Open EC Screen (common.resource) for the
    ...    actual mechanics.
    Open EC Screen    ${ORIFICE_PLATE_SCREEN}

Insert Orifice Plate Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties
    ...    And Verify Code, so orifice_plate_iud.robot's test case body reads as a plain
    ...    business step with ZERO arguments. Also checks the inserted Code matches the
    ...    suite's ${TEST_CODE}. Pre-save evidence screenshot captured before Save is
    ...    clicked, matching Bank/Berth.
    [Arguments]    ${properties_path}=${ORIFICE_PLATE_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Orifice Code
    RETURN    ${code}

Verify Orifice Plate Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (no DB check here, matching Bank/Berth's TC02 convention): row
    ...    exists in the grid, then the form shows what was just inserted (Orifice
    ...    Code/Orifice Name only — Start Date is grid/insert-only, not present in
    ...    updateAttributes). Delegates the full sequence (row-check, select, form-compare,
    ...    screenshot) to the shared T2 Verify Object Insert Exists.
    ...    Filters via Find Orifice Plate Row By Filter first, clears after (2026-08-22
    ...    standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find Orifice Plate Row By Filter    ${code}
    Verify Object Insert Exists    ${ORIFICE_PLATE_TABLE}    ${code}    Orifice Plate
    ...    ${ORIFICE_PLATE_INSERT_PROPERTIES}    @{ORIFICE_PLATE_FORM_LABELS}
    ...    code_label=Orifice Code
    Clear Orifice Plate Row Filter

Update Orifice Plate Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Pre-save evidence screenshot captured before Save is clicked, matching Bank/Berth.
    ...    Filters via Find Orifice Plate Row By Filter first, clears after (2026-08-22
    ...    standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${ORIFICE_PLATE_UPDATE_PROPERTIES}
    Find Orifice Plate Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${ORIFICE_PLATE_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Orifice Code
    Clear Orifice Plate Row Filter
    RETURN    ${data}

Verify Orifice Plate Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification, matching Bank/Berth's TC03 convention: the form shows the updated
    ...    Orifice Name. Delegates the full sequence (select, form-compare, screenshot) to
    ...    the shared T2 Verify Object Form Record. Filters via Find Orifice Plate Row By
    ...    Filter first, clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find Orifice Plate Row By Filter    ${code}
    Verify Object Form Record    ${ORIFICE_PLATE_TABLE}    ${code}    Orifice Plate
    ...    ${ORIFICE_PLATE_UPDATE_PROPERTIES}    Orifice Name    code_label=Orifice Code
    Clear Orifice Plate Row Filter

Find Orifice Plate Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Delegates the full select+capture sequence. Calls Find Orifice Plate Row By
    ...    Filter first (2026-08-22 standardisation). Deliberately does NOT clear the filter
    ...    afterward — Verify Orifice Plate Record Found (called right after, same TC) needs
    ...    the grid still filtered to ${code} for its own grid-check, since it doesn't
    ...    re-select the row itself; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Orifice Plate Row By Filter    ${code}
    Find Object Record    ${ORIFICE_PLATE_TABLE}    ${code}    Orifice Plate    code_label=Orifice Code

Verify Orifice Plate Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the form record match the expected (post-update) data. Delegates the
    ...    full sequence (grid-compare, form-compare, screenshot) to the shared T2 Verify
    ...    Object Found. Caller must already have selected the row (TC04 does, via Find
    ...    Orifice Plate Record before this) AND left the Code filter active from that same
    ...    call — clears the filter itself once both checks are done (2026-08-22
    ...    standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${ORIFICE_PLATE_TABLE}    ${code}    ${ORIFICE_PLATE_GRID_VERIFY_PROPERTIES}
    ...    ${ORIFICE_PLATE_FORM_VERIFY_PROPERTIES}    @{ORIFICE_PLATE_FORM_LABELS}
    Clear Orifice Plate Row Filter

Delete Orifice Plate Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date,
    ...    called with ZERO arguments (defaults ${code}/${date} to the suite's
    ...    ${TEST_CODE}/${END_DATE}). Select the orifice plate, set End Date = Start Date
    ...    (true delete), Save. Captures the TC05 evidence screenshot right after the End
    ...    Date is filled but BEFORE Save is clicked, matching Bank/Berth's convention.
    ...    Filters via Find Orifice Plate Row By Filter first, clears after (2026-08-22
    ...    standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Orifice Plate Row By Filter    ${code}
    Delete Object Via End Date    ${ORIFICE_PLATE_TABLE}    ${ORIFICE_PLATE_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Orifice Plate Row Filter

Verify Orifice Plate Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code}
    ...    is absent from BOTH the grid and the database.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${ORIFICE_PLATE_TABLE}    OV_ORIFICE_PLATE    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Orifice Plate Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to
    ...    the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${ORIFICE_PLATE_TABLE}    ${code}
