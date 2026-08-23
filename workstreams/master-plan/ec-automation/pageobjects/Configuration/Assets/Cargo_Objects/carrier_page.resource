*** Settings ***
Documentation       T3 (screen) — Carrier page object.
...                 Screen: Configuration > Assets > Cargo Objects > Carrier.
...                 Manage-Object (OV) screen, Bank-family grid (manage_object_nav_nav:form:T_data) —
...                 NOT gated (navigator is just an optional date + GO — confirmed via the prior
...                 SOW recon (screens/.../Carrier/carrier_sow.md) and the already-proven Playwright
...                 driver screens/.../Carrier/playwright/ec_iud_carrier.py, both live-verified
...                 2026-06-19; re-confirmed genuinely Bank-shaped before Batch 11 conversion,
...                 2026-08-23 — no mandatory nav dropdown/cascade).
...                 Rebuilt 2026-08-23 (Batch 11) to mirror Bank/Berth/Port exactly - replaces the
...                 older arg-based (`Fill New Object Form`) pattern with the label-driven,
...                 properties-file-driven, grid-filter-wired, T2-consolidated pattern.
...                 Insert requires a mandatory reference dropdown - "Unit" - filled __FIRST__ (a
...                 throwaway record; deliberately EXCLUDED from @{CARRIER_FORM_LABELS} so the
...                 known __FIRST__-fails-round-trip-verify gotcha never applies here, matching the
...                 Batch 2/9 VAT Code/Process Train precedent).
...                 DELETE = End Date = Start Date (true delete from OV_CARRIER).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${CARRIER_SCREEN}          Carrier
${CARRIER_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/carrier_insert.properties
${CARRIER_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/carrier_update.properties
${CARRIER_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/carrier_form_verify.properties
${CARRIER_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/carrier_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal.
${CARRIER_TABLE}        ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date), matching Bank/Berth/Port's convention.
${CARRIER_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Carrier's own form-field label set. Labels are "Carrier Code"/"Carrier Name" (screen-prefixed) -
# confirmed via the prior SOW recon table (carrier_sow.md section 2) and the proven Playwright
# driver's field comments; NOT the generic "Code"/"Name" Bank/Object List use. Unit (mandatory
# reference dd) is deliberately EXCLUDED here - it is filled __FIRST__ at Insert time (throwaway
# record) but never round-trip-verified (see Documentation above). Start Date deliberately
# excluded - Insert-only, not present in updateAttributes (same as Bank/Berth/Port). Defined ONCE
# here so both Verify Carrier Record Exists (TC02) and Verify Carrier Record Found (TC04) share
# the same list.
@{CARRIER_FORM_LABELS}    Carrier Code    Carrier Name


*** Keywords ***
Find Carrier Row By Filter
    [Documentation]    Explicitly filter the Carrier grid's Code column to ${code} via the shared
    ...    T2 Find Object Row By Filter (resources/manage_object.resource) - matches Bank/
    ...    Berth/Port's own explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${CARRIER_TABLE}    ${code}

Clear Carrier Row Filter
    [Documentation]    Clear the Code column filter (see Find Carrier Row By Filter) via the
    ...    shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${CARRIER_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Carrier's OWN credentials (${CARRIER_EC_USER}/
    ...    ${CARRIER_EC_PASS} from credentials.py) on the current page. Standing decision
    ...    (owner, 2026-08-22): every EC screen gets its own dedicated credential pair.
    ...    Zero-argument wrapper so carrier_iud.robot's test cases read as a plain business
    ...    step; supplies Carrier's own credential defaults to the shared T1 Login To EC
    ...    Screen (common.resource), which owns the actual login mechanics.
    Login To EC Screen    ${CARRIER_EC_USER}    ${CARRIER_EC_PASS}

Open Carrier Screen
    [Documentation]    Navigate to the Carrier screen. Assumes the caller already logged in
    ...    this test case (via Login To EC Application) - this keyword ONLY navigates.
    ...    Delegates to the shared T1 Open EC Screen (common.resource) for the actual mechanics.
    Open EC Screen    ${CARRIER_SCREEN}

Insert Carrier Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties
    ...    And Verify Code, so carrier_iud.robot's test case body reads as a plain business
    ...    step with ZERO arguments. Also checks the inserted Code matches the suite's
    ...    ${TEST_CODE}. Pre-save evidence screenshot captured before Save is clicked,
    ...    matching Bank/Berth/Port.
    [Arguments]    ${properties_path}=${CARRIER_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Carrier Code
    RETURN    ${code}

Verify Carrier Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (no DB check here, matching Bank/Berth/Port's TC02 convention): row
    ...    exists in the grid, then the form shows what was just inserted (Carrier
    ...    Code/Carrier Name only - Unit is a mandatory-but-throwaway __FIRST__ dropdown never
    ...    round-trip-checked; Start Date is grid/insert-only, not present in updateAttributes).
    ...    Delegates the full sequence (row-check, select, form-compare, screenshot) to the
    ...    shared T2 Verify Object Insert Exists. Filters via Find Carrier Row By Filter first,
    ...    clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find Carrier Row By Filter    ${code}
    Verify Object Insert Exists    ${CARRIER_TABLE}    ${code}    Carrier    ${CARRIER_INSERT_PROPERTIES}
    ...    @{CARRIER_FORM_LABELS}    code_label=Carrier Code
    Clear Carrier Row Filter

Update Carrier Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Pre-save evidence screenshot captured before Save is clicked, matching Bank/Berth/
    ...    Port. Filters via Find Carrier Row By Filter first, clears after (2026-08-22
    ...    standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${CARRIER_UPDATE_PROPERTIES}
    Find Carrier Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${CARRIER_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Carrier Code
    Clear Carrier Row Filter
    RETURN    ${data}

Verify Carrier Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification, matching Bank/Berth/Port's TC03 convention: the form shows the
    ...    updated Carrier Name. Delegates the full sequence (select, form-compare,
    ...    screenshot) to the shared T2 Verify Object Form Record. Filters via Find Carrier
    ...    Row By Filter first, clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find Carrier Row By Filter    ${code}
    Verify Object Form Record    ${CARRIER_TABLE}    ${code}    Carrier    ${CARRIER_UPDATE_PROPERTIES}
    ...    Carrier Name    code_label=Carrier Code
    Clear Carrier Row Filter

Find Carrier Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Delegates the full select+capture sequence. Calls Find Carrier Row By Filter first
    ...    (2026-08-22 standardisation). Deliberately does NOT clear the filter afterward -
    ...    Verify Carrier Record Found (called right after, same TC) needs the grid still
    ...    filtered to ${code} for its own grid-check, since it doesn't re-select the row
    ...    itself; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Carrier Row By Filter    ${code}
    Find Object Record    ${CARRIER_TABLE}    ${code}    Carrier    code_label=Carrier Code

Verify Carrier Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the form record match the expected (post-update) data. Delegates the full
    ...    sequence (grid-compare, form-compare, screenshot) to the shared T2 Verify Object
    ...    Found. Caller must already have selected the row (TC04 does, via Find Carrier
    ...    Record before this) AND left the Code filter active from that same call - clears
    ...    the filter itself once both checks are done (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${CARRIER_TABLE}    ${code}    ${CARRIER_GRID_VERIFY_PROPERTIES}
    ...    ${CARRIER_FORM_VERIFY_PROPERTIES}    @{CARRIER_FORM_LABELS}
    Clear Carrier Row Filter

Delete Carrier Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date,
    ...    called with ZERO arguments (defaults ${code}/${date} to the suite's
    ...    ${TEST_CODE}/${END_DATE}). Select the carrier, set End Date = Start Date (true
    ...    delete), Save. Captures the TC05 evidence screenshot right after the End Date is
    ...    filled but BEFORE Save is clicked, matching Bank/Berth/Port's convention. Filters
    ...    via Find Carrier Row By Filter first, clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Carrier Row By Filter    ${code}
    Delete Object Via End Date    ${CARRIER_TABLE}    ${CARRIER_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Carrier Row Filter

Verify Carrier Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code}
    ...    is absent from BOTH the grid and the database.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${CARRIER_TABLE}    OV_CARRIER    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Carrier Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to
    ...    the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${CARRIER_TABLE}    ${code}
