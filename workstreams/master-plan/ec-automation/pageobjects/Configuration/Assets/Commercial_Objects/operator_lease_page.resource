*** Settings ***
Documentation       T3 (screen) — Operator Lease page object.
...                 Screen: Configuration > Assets > Commercial Objects > Operator Lease.
...                 Manage-Object (OV) screen. Holds Operator Lease's locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common).
...                 Rebuilt 2026-08-23 to mirror Bank/State/Country/Object List exactly
...                 (Batch 3 plain-OV Bank-pattern conversion) - replaces the older
...                 hardcoded-field-id pattern (per-screen bespoke Insert/Update/Delete
...                 keywords, no properties-file-driven insert) with the label-driven,
...                 properties-file-driven, T2-consolidated pattern.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${OPERATOR_LEASE_SCREEN}          Operator Lease
${OPERATOR_LEASE_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/operator_lease_insert.properties
${OPERATOR_LEASE_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/operator_lease_update.properties
${OPERATOR_LEASE_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/operator_lease_form_verify.properties
${OPERATOR_LEASE_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/operator_lease_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal
# string (manage_object.resource defines this ONCE specifically so no T3 duplicates it).
# Confirmed live 2026-08-23 (manage_object_nav_nav:form:T_data, plain manage-object OV, no
# mandatory nav dropdown/date before GO - the top "Date" field is the same universal
# as-at-date filter Bank also has, pre-filled + auto-queries on page load, not a blocking
# nav requirement) - matches the batch's pre-confirmed navigator shape.
${OPERATOR_LEASE_TABLE}    ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date), matching Bank/State/Country/
# Account's already-proven, framework-invariant row layout (Start Date C:1, End Date label
# C:2, End Date input C:3) - not independently re-verified here per the batch's ground rules.
${OPERATOR_LEASE_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Operator Lease's own form-field label set. Labels are "Operator Lease Code"/"Operator
# Lease Name" (screen-prefixed) - confirmed live 2026-08-23 via a field-label recon script
# dumping every ECCell label + MandatoryCellStyle class in both objectForm (Insert, 7
# labels: Operator Lease Code, Operator Lease Name, Description, Start Date, End Date -
# mandatory: Code/Name/Start Date only) and updateAttributes (Update, 3 labels: Operator
# Lease Code, Operator Lease Name, Description - mandatory: Code/Name only, Description
# optional). Confirmed via a live throwaway Insert+Delete round-trip (RECON_OL_TMP,
# self-cleaned, DB re-checked empty after) since the grid held zero real Operator Lease
# rows in this environment to select for updateAttributes recon.
@{OPERATOR_LEASE_FORM_LABELS}    Operator Lease Code    Operator Lease Name


*** Keywords ***
Find Operator Lease Row By Filter
    [Documentation]    Explicitly filter the Operator Lease grid's Code column to ${code} via
    ...    the shared T2 Find Object Row By Filter (resources/manage_object.resource) -
    ...    matches Account/Bank/State/Country's own explicit filter usage (owner, 2026-08-22:
    ...    "others (Bank, State, List_Object) should follow Account... utilise same filter
    ...    feature"), rather than relying only on Select Object Row's implicit 3s-timeout
    ...    fallback.
    [Arguments]    ${code}
    Find Object Row By Filter    ${OPERATOR_LEASE_TABLE}    ${code}

Clear Operator Lease Row Filter
    [Documentation]    Clear the Code column filter (see Find Operator Lease Row By Filter)
    ...    via the shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered
    ...    view.
    Clear Object Row Filter    ${OPERATOR_LEASE_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Operator Lease's OWN credentials
    ...    (${OPERATOR_LEASE_EC_USER}/${OPERATOR_LEASE_EC_PASS} from credentials.py) on the
    ...    current page. Standing decision (owner, 2026-08-22): every EC screen gets its own
    ...    dedicated credential pair. Zero-argument wrapper so operator_lease_iud.robot's test
    ...    cases read as a plain business step; supplies Operator Lease's own credential
    ...    defaults to the shared T1 Login To EC Screen (common.resource), which owns the
    ...    actual login mechanics.
    Login To EC Screen    ${OPERATOR_LEASE_EC_USER}    ${OPERATOR_LEASE_EC_PASS}

Open Operator Lease Screen
    [Documentation]    Navigate to the Operator Lease screen. Assumes the caller already
    ...    logged in this test case (via Login To EC Application) - this keyword ONLY
    ...    navigates. Delegates to the shared T1 Open EC Screen (common.resource) for the
    ...    actual mechanics.
    Open EC Screen    ${OPERATOR_LEASE_SCREEN}

Insert Operator Lease Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties
    ...    And Verify Code, so operator_lease_iud.robot's test case body reads as a plain
    ...    business step with ZERO arguments. Also checks the inserted Code matches the
    ...    suite's ${TEST_CODE}. Pre-save evidence screenshot captured before Save is
    ...    clicked, matching Bank/State/Country.
    [Arguments]    ${properties_path}=${OPERATOR_LEASE_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Operator Lease Code
    RETURN    ${code}

Verify Operator Lease Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (no DB check here, matching Bank/State/Country's TC02 convention):
    ...    row exists in the grid, then the form shows what was just inserted (Operator
    ...    Lease Code/Operator Lease Name only - Start Date is grid/insert-only, not present
    ...    in updateAttributes). Delegates the full sequence (row-check, select,
    ...    form-compare, screenshot) to the shared T2 Verify Object Insert Exists. Filters
    ...    via Find Operator Lease Row By Filter first, clears after (2026-08-22
    ...    standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find Operator Lease Row By Filter    ${code}
    Verify Object Insert Exists    ${OPERATOR_LEASE_TABLE}    ${code}    Operator Lease
    ...    ${OPERATOR_LEASE_INSERT_PROPERTIES}    @{OPERATOR_LEASE_FORM_LABELS}
    ...    code_label=Operator Lease Code
    Clear Operator Lease Row Filter

Update Operator Lease Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Pre-save evidence screenshot captured before Save is clicked, matching
    ...    Bank/State/Country. Filters via Find Operator Lease Row By Filter first, clears
    ...    after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${OPERATOR_LEASE_UPDATE_PROPERTIES}
    Find Operator Lease Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${OPERATOR_LEASE_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Operator Lease Code
    Clear Operator Lease Row Filter
    RETURN    ${data}

Verify Operator Lease Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification, matching Bank/State/Country's TC03 convention: the form shows the
    ...    updated Operator Lease Name. Delegates the full sequence (select, form-compare,
    ...    screenshot) to the shared T2 Verify Object Form Record. Filters via Find Operator
    ...    Lease Row By Filter first, clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find Operator Lease Row By Filter    ${code}
    Verify Object Form Record    ${OPERATOR_LEASE_TABLE}    ${code}    Operator Lease
    ...    ${OPERATOR_LEASE_UPDATE_PROPERTIES}    Operator Lease Name    code_label=Operator Lease Code
    Clear Operator Lease Row Filter

Find Operator Lease Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Delegates the full select+capture sequence. Calls Find Operator Lease Row By
    ...    Filter first (2026-08-22 standardisation). Deliberately does NOT clear the filter
    ...    afterward - Verify Operator Lease Record Found (called right after, same TC)
    ...    needs the grid still filtered to ${code} for its own grid-check, since it doesn't
    ...    re-select the row itself; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Operator Lease Row By Filter    ${code}
    Find Object Record    ${OPERATOR_LEASE_TABLE}    ${code}    Operator Lease    code_label=Operator Lease Code

Verify Operator Lease Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the form record match the expected (post-update) data. Delegates the
    ...    full sequence (grid-compare, form-compare, screenshot) to the shared T2 Verify
    ...    Object Found. Caller must already have selected the row (TC04 does, via Find
    ...    Operator Lease Record before this) AND left the Code filter active from that same
    ...    call - clears the filter itself once both checks are done (2026-08-22
    ...    standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${OPERATOR_LEASE_TABLE}    ${code}    ${OPERATOR_LEASE_GRID_VERIFY_PROPERTIES}
    ...    ${OPERATOR_LEASE_FORM_VERIFY_PROPERTIES}    @{OPERATOR_LEASE_FORM_LABELS}
    Clear Operator Lease Row Filter

Delete Operator Lease Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date,
    ...    called with ZERO arguments (defaults ${code}/${date} to the suite's
    ...    ${TEST_CODE}/${END_DATE}). Select the operator lease, set End Date = Start Date
    ...    (true delete), Save. Captures the TC05 evidence screenshot right after the End
    ...    Date is filled but BEFORE Save is clicked, matching Bank/State/Country's
    ...    convention. Filters via Find Operator Lease Row By Filter first, clears after
    ...    (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Operator Lease Row By Filter    ${code}
    Delete Object Via End Date    ${OPERATOR_LEASE_TABLE}    ${OPERATOR_LEASE_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Operator Lease Row Filter

Verify Operator Lease Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code}
    ...    is absent from BOTH the grid and the database (OV_OPERATOR_LEASE).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${OPERATOR_LEASE_TABLE}    OV_OPERATOR_LEASE    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Operator Lease Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to
    ...    the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${OPERATOR_LEASE_TABLE}    ${code}
