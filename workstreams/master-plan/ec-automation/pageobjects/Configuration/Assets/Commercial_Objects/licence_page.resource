*** Settings ***
Documentation       T3 (screen) — Licence page object.
...                 Screen: Configuration > Assets > Commercial Objects > Licence.
...                 Manage-Object (OV) screen. Holds Licence's locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common).
...                 Rebuilt 2026-08-23 (Batch 3 plain-OV Bank-pattern conversion) to mirror
...                 Bank/State/Country exactly - replaces the older hardcoded-field-id pattern
...                 (per-screen bespoke Insert/Update/Delete keywords, no properties-file-
...                 driven insert) with the label-driven, properties-file-driven,
...                 T2-consolidated pattern.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${LICENCE_SCREEN}          Licence
${LICENCE_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/licence_insert.properties
${LICENCE_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/licence_update.properties
${LICENCE_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/licence_form_verify.properties
${LICENCE_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/licence_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal
# string (manage_object.resource defines this ONCE specifically so no T3 duplicates it).
# Confirmed live 2026-08-23 (manage_object_nav_nav:form:T_data, plain manage-object OV, NO
# GO button - manage_object_nav GO-button count=0/94 elements present) - nav-free, matching
# the batch's pre-confirmed navigator shape (docs/bank-pattern-conversion-checklist.md).
${LICENCE_TABLE}        ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date), matching Bank/State/Country/
# Account's already-proven, framework-invariant row layout (Start Date C:1, End Date label
# C:2, End Date input C:3) - not independently re-verified here per the batch's ground rules.
${LICENCE_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Licence's own form-field label set. Labels are "Licence Code"/"Licence Name"
# (screen-prefixed) - confirmed live 2026-08-23 via a field-label recon script dumping every
# ECCell label in both objectForm (Insert, 8 labels) and updateAttributes (Update, 6 labels):
# Licence Code, Licence Name, Sort Order, Description, Master System Code, Master System
# Name, Start Date/End Date (objectdates-only, Insert form shows them inline but they are NOT
# part of updateAttributes). Only Licence Code/Licence Name are MandatoryCellStyle-confirmed
# mandatory besides Start Date (Insert-only) - IUD-fill-only-needed-fields convention, so
# @{LICENCE_FORM_LABELS} deliberately lists only the mandatory, always-present pair (Start
# Date excluded - Insert-only, not in updateAttributes, same as Bank/State/Country).
@{LICENCE_FORM_LABELS}    Licence Code    Licence Name


*** Keywords ***
Find Licence Row By Filter
    [Documentation]    Explicitly filter the Licence grid's Code column to ${code} via the
    ...    shared T2 Find Object Row By Filter (resources/manage_object.resource) - matches
    ...    Account/Bank/State/Country's own explicit filter usage (owner, 2026-08-22: "others
    ...    (Bank, State, List_Object) should follow Account... utilise same filter feature"),
    ...    rather than relying only on Select Object Row's implicit 3s-timeout fallback.
    [Arguments]    ${code}
    Find Object Row By Filter    ${LICENCE_TABLE}    ${code}

Clear Licence Row Filter
    [Documentation]    Clear the Code column filter (see Find Licence Row By Filter) via the
    ...    shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${LICENCE_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Licence's OWN credentials (${LICENCE_EC_USER}/
    ...    ${LICENCE_EC_PASS} from credentials.py) on the current page. Standing decision
    ...    (owner, 2026-08-22): every EC screen gets its own dedicated credential pair.
    ...    Zero-argument wrapper so licence_iud.robot's test cases read as a plain business
    ...    step; supplies Licence's own credential defaults to the shared T1 Login To EC
    ...    Screen (common.resource), which owns the actual login mechanics.
    Login To EC Screen    ${LICENCE_EC_USER}    ${LICENCE_EC_PASS}

Open Licence Screen
    [Documentation]    Navigate to the Licence screen. Assumes the caller already logged in
    ...    this test case (via Login To EC Application) - this keyword ONLY navigates.
    ...    Delegates to the shared T1 Open EC Screen (common.resource) for the actual mechanics.
    Open EC Screen    ${LICENCE_SCREEN}

Insert Licence Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties
    ...    And Verify Code, so licence_iud.robot's test case body reads as a plain business
    ...    step with ZERO arguments. Also checks the inserted Code matches the suite's
    ...    ${TEST_CODE}. Pre-save evidence screenshot captured before Save is clicked,
    ...    matching Bank/State/Country.
    [Arguments]    ${properties_path}=${LICENCE_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Licence Code
    RETURN    ${code}

Verify Licence Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (no DB check here, matching Bank/State/Country's TC02 convention): row
    ...    exists in the grid, then the form shows what was just inserted (Licence Code/
    ...    Licence Name only - Start Date is grid/insert-only, not present in
    ...    updateAttributes). Delegates the full sequence (row-check, select, form-compare,
    ...    screenshot) to the shared T2 Verify Object Insert Exists. Filters via Find Licence
    ...    Row By Filter first, clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find Licence Row By Filter    ${code}
    Verify Object Insert Exists    ${LICENCE_TABLE}    ${code}    Licence    ${LICENCE_INSERT_PROPERTIES}
    ...    @{LICENCE_FORM_LABELS}    code_label=Licence Code
    Clear Licence Row Filter

Update Licence Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Pre-save evidence screenshot captured before Save is clicked, matching Bank/State/
    ...    Country. Filters via Find Licence Row By Filter first, clears after (2026-08-22
    ...    standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${LICENCE_UPDATE_PROPERTIES}
    Find Licence Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${LICENCE_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Licence Code
    Clear Licence Row Filter
    RETURN    ${data}

Verify Licence Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification, matching Bank/State/Country's TC03 convention: the form shows the
    ...    updated Licence Name. Delegates the full sequence (select, form-compare, screenshot)
    ...    to the shared T2 Verify Object Form Record. Filters via Find Licence Row By Filter
    ...    first, clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find Licence Row By Filter    ${code}
    Verify Object Form Record    ${LICENCE_TABLE}    ${code}    Licence    ${LICENCE_UPDATE_PROPERTIES}
    ...    Licence Name    code_label=Licence Code
    Clear Licence Row Filter

Find Licence Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Delegates the full select+capture sequence. Calls Find Licence Row By Filter first
    ...    (2026-08-22 standardisation). Deliberately does NOT clear the filter afterward -
    ...    Verify Licence Record Found (called right after, same TC) needs the grid still
    ...    filtered to ${code} for its own grid-check, since it doesn't re-select the row
    ...    itself; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Licence Row By Filter    ${code}
    Find Object Record    ${LICENCE_TABLE}    ${code}    Licence    code_label=Licence Code

Verify Licence Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the form record match the expected (post-update) data. Delegates the
    ...    full sequence (grid-compare, form-compare, screenshot) to the shared T2 Verify
    ...    Object Found. Caller must already have selected the row (TC04 does, via Find
    ...    Licence Record before this) AND left the Code filter active from that same call -
    ...    clears the filter itself once both checks are done (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${LICENCE_TABLE}    ${code}    ${LICENCE_GRID_VERIFY_PROPERTIES}
    ...    ${LICENCE_FORM_VERIFY_PROPERTIES}    @{LICENCE_FORM_LABELS}
    Clear Licence Row Filter

Delete Licence Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date,
    ...    called with ZERO arguments (defaults ${code}/${date} to the suite's
    ...    ${TEST_CODE}/${END_DATE}). Select the licence, set End Date = Start Date (true
    ...    delete), Save. Captures the TC05 evidence screenshot right after the End Date is
    ...    filled but BEFORE Save is clicked, matching Bank/State/Country's convention.
    ...    Filters via Find Licence Row By Filter first, clears after (2026-08-22
    ...    standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Licence Row By Filter    ${code}
    Delete Object Via End Date    ${LICENCE_TABLE}    ${LICENCE_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Licence Row Filter

Verify Licence Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code}
    ...    is absent from BOTH the grid and the database (OV_LICENCE).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${LICENCE_TABLE}    OV_LICENCE    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Licence Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to
    ...    the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${LICENCE_TABLE}    ${code}
