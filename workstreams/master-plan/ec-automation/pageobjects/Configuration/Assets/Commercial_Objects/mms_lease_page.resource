*** Settings ***
Documentation       T3 (screen) — MMS Lease page object.
...                 Screen: Configuration > Assets > Commercial Objects > MMS Lease.
...                 Manage-Object (OV) screen. Holds MMS Lease's locators + thin IUD
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
${MMS_LEASE_SCREEN}          MMS Lease
${MMS_LEASE_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/mms_lease_insert.properties
${MMS_LEASE_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/mms_lease_update.properties
${MMS_LEASE_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/mms_lease_form_verify.properties
${MMS_LEASE_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/mms_lease_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal
# string (manage_object.resource defines this ONCE specifically so no T3 duplicates it).
# Confirmed live 2026-08-23 (manage_object_nav_nav:form:T_data, plain manage-object OV, no
# mandatory nav dropdown/date before GO - manage_object_nav GO button count = 0) - matches
# the registry's documented navigator ("manage-object") and this batch's ground rules.
${MMS_LEASE_TABLE}        ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date), matching Bank/State/Country's
# already-proven, framework-invariant row layout (Start Date C:1, End Date label C:2, End
# Date input C:3) - confirmed live 2026-08-23 via a real insert+select+delete+DB-verify
# recon cycle on a throwaway AUTOTEST_MMS_LEASE record.
${MMS_LEASE_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# MMS Lease's own form-field label set. Labels are "MMS Lease Code"/"MMS Lease Name"
# (screen-prefixed) - confirmed live 2026-08-23 via a field-label recon dumping every
# ECCell label in both objectForm (Insert, 6 labels: MMS Lease Code, MMS Lease Name,
# Description, Start Date, End Date, Operator) and updateAttributes (Update, 4 labels: MMS
# Lease Code, MMS Lease Name, Description, Operator - no Start/End Date there, same as
# Bank/State/Country). Only Code/Name are MandatoryCellStyle-confirmed mandatory besides
# Start Date (Insert-only, objectForm mandatory count = 3: Code/Name/Start Date;
# updateAttributes mandatory count = 2: Code/Name) - IUD-fill-only-needed-fields
# convention, so @{MMS_LEASE_FORM_LABELS} deliberately lists only the mandatory,
# always-present pair (Start Date excluded - Insert-only, not in updateAttributes, same as
# Bank/State/Country).
@{MMS_LEASE_FORM_LABELS}    MMS Lease Code    MMS Lease Name


*** Keywords ***
Find MMS Lease Row By Filter
    [Documentation]    Explicitly filter the MMS Lease grid's Code column to ${code} via the
    ...    shared T2 Find Object Row By Filter (resources/manage_object.resource) - matches
    ...    Account/Bank/State/Country's own explicit filter usage (owner, 2026-08-22: "others
    ...    (Bank, State, List_Object) should follow Account... utilise same filter feature"),
    ...    rather than relying only on Select Object Row's implicit 3s-timeout fallback.
    [Arguments]    ${code}
    Find Object Row By Filter    ${MMS_LEASE_TABLE}    ${code}

Clear MMS Lease Row Filter
    [Documentation]    Clear the Code column filter (see Find MMS Lease Row By Filter) via the
    ...    shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${MMS_LEASE_TABLE}

Login To EC Application
    [Documentation]    Authenticate as MMS Lease's OWN credentials (${MMS_LEASE_EC_USER}/
    ...    ${MMS_LEASE_EC_PASS} from credentials.py) on the current page. Standing decision
    ...    (owner, 2026-08-22): every EC screen gets its own dedicated credential pair.
    ...    Zero-argument wrapper so mms_lease_iud.robot's test cases read as a plain
    ...    business step; supplies MMS Lease's own credential defaults to the shared T1
    ...    Login To EC Screen (common.resource), which owns the actual login mechanics.
    Login To EC Screen    ${MMS_LEASE_EC_USER}    ${MMS_LEASE_EC_PASS}

Open MMS Lease Screen
    [Documentation]    Navigate to the MMS Lease screen. Assumes the caller already logged
    ...    in this test case (via Login To EC Application) - this keyword ONLY navigates.
    ...    Delegates to the shared T1 Open EC Screen (common.resource) for the actual mechanics.
    Open EC Screen    ${MMS_LEASE_SCREEN}

Insert MMS Lease Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties
    ...    And Verify Code, so mms_lease_iud.robot's test case body reads as a plain business
    ...    step with ZERO arguments. Also checks the inserted Code matches the suite's
    ...    ${TEST_CODE}. Pre-save evidence screenshot captured before Save is clicked,
    ...    matching Bank/State/Country.
    [Arguments]    ${properties_path}=${MMS_LEASE_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=MMS Lease Code
    RETURN    ${code}

Verify MMS Lease Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (no DB check here, matching Bank/State/Country's TC02 convention):
    ...    row exists in the grid, then the form shows what was just inserted (MMS Lease
    ...    Code/MMS Lease Name only - Start Date is grid/insert-only, not present in
    ...    updateAttributes). Delegates the full sequence (row-check, select, form-compare,
    ...    screenshot) to the shared T2 Verify Object Insert Exists. Filters via Find MMS
    ...    Lease Row By Filter first, clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find MMS Lease Row By Filter    ${code}
    Verify Object Insert Exists    ${MMS_LEASE_TABLE}    ${code}    MMS Lease    ${MMS_LEASE_INSERT_PROPERTIES}
    ...    @{MMS_LEASE_FORM_LABELS}    code_label=MMS Lease Code
    Clear MMS Lease Row Filter

Update MMS Lease Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Pre-save evidence screenshot captured before Save is clicked, matching
    ...    Bank/State/Country. Filters via Find MMS Lease Row By Filter first, clears after
    ...    (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${MMS_LEASE_UPDATE_PROPERTIES}
    Find MMS Lease Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${MMS_LEASE_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=MMS Lease Code
    Clear MMS Lease Row Filter
    RETURN    ${data}

Verify MMS Lease Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification, matching Bank/State/Country's TC03 convention: the form shows the
    ...    updated MMS Lease Name. Delegates the full sequence (select, form-compare,
    ...    screenshot) to the shared T2 Verify Object Form Record. Filters via Find MMS
    ...    Lease Row By Filter first, clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find MMS Lease Row By Filter    ${code}
    Verify Object Form Record    ${MMS_LEASE_TABLE}    ${code}    MMS Lease    ${MMS_LEASE_UPDATE_PROPERTIES}
    ...    MMS Lease Name    code_label=MMS Lease Code
    Clear MMS Lease Row Filter

Find MMS Lease Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Delegates the full select+capture sequence. Calls Find MMS Lease Row By Filter
    ...    first (2026-08-22 standardisation). Deliberately does NOT clear the filter
    ...    afterward - Verify MMS Lease Record Found (called right after, same TC) needs the
    ...    grid still filtered to ${code} for its own grid-check, since it doesn't re-select
    ...    the row itself; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find MMS Lease Row By Filter    ${code}
    Find Object Record    ${MMS_LEASE_TABLE}    ${code}    MMS Lease    code_label=MMS Lease Code

Verify MMS Lease Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the form record match the expected (post-update) data. Delegates the
    ...    full sequence (grid-compare, form-compare, screenshot) to the shared T2 Verify
    ...    Object Found. Caller must already have selected the row (TC04 does, via Find MMS
    ...    Lease Record before this) AND left the Code filter active from that same call -
    ...    clears the filter itself once both checks are done (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${MMS_LEASE_TABLE}    ${code}    ${MMS_LEASE_GRID_VERIFY_PROPERTIES}
    ...    ${MMS_LEASE_FORM_VERIFY_PROPERTIES}    @{MMS_LEASE_FORM_LABELS}
    Clear MMS Lease Row Filter

Delete MMS Lease Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date,
    ...    called with ZERO arguments (defaults ${code}/${date} to the suite's
    ...    ${TEST_CODE}/${END_DATE}). Select the mms lease, set End Date = Start Date (true
    ...    delete), Save. Captures the TC05 evidence screenshot right after the End Date is
    ...    filled but BEFORE Save is clicked, matching Bank/State/Country's convention.
    ...    Filters via Find MMS Lease Row By Filter first, clears after (2026-08-22
    ...    standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find MMS Lease Row By Filter    ${code}
    Delete Object Via End Date    ${MMS_LEASE_TABLE}    ${MMS_LEASE_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear MMS Lease Row Filter

Verify MMS Lease Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code}
    ...    is absent from BOTH the grid and the database (OV_MMS_LEASE).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${MMS_LEASE_TABLE}    OV_MMS_LEASE    ${code}
    Capture Step    ${TEST NAME}_verify

Verify MMS Lease Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to
    ...    the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${MMS_LEASE_TABLE}    ${code}
