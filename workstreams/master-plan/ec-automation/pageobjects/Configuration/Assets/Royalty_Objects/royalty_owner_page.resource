*** Settings ***
Documentation       T3 (screen) — Royalty Owner page object.
...                 Screen: Configuration > Assets > Royalty Objects > Royalty Owner.
...                 Manage-Object (OV) screen. Holds Royalty Owner's locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common).
...                 Rebuilt 2026-08-23 to mirror Bank/State/Object List exactly (Batch 5
...                 Bank-pattern conversion) - replaces the older hardcoded-field-id/
...                 generated-code pattern with the label-driven, properties-file-driven,
...                 T2-consolidated pattern.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${ROYALTY_OWNER_SCREEN}         Royalty Owner
${ROYALTY_OWNER_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/royalty_owner_insert.properties
${ROYALTY_OWNER_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/royalty_owner_update.properties
${ROYALTY_OWNER_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/royalty_owner_form_verify.properties
${ROYALTY_OWNER_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/royalty_owner_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal.
${ROYALTY_OWNER_TABLE}          ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date), matching Bank/State/Object List's
# convention - confirmed live 2026-08-23 (objectdates tab: Start Date at R:0:C:1, End Date
# label at R:0:C:2, End Date INPUT at R:0:C:3).
${ROYALTY_OWNER_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Royalty Owner's own form-field label set. Labels are "Royalty Owner Code"/"Royalty Owner
# Name" (screen-prefixed) - confirmed live 2026-08-23 via a field-inventory scan of the New
# Object (objectForm) and updateAttributes forms; NOT the generic "Code"/"Name" Bank/Object
# List use (same pattern as State). Start Date deliberately excluded - Insert-only, not
# present in updateAttributes (confirmed live: updateAttributes has 28 ECCell labels starting
# at Royalty Owner Code/Royalty Owner Name/Official Name..., no Start Date/End Date).
# Defined ONCE here so both Verify Royalty Owner Record Exists (TC02) and Verify Royalty Owner
# Record Found (TC04) share the same list.
@{ROYALTY_OWNER_FORM_LABELS}    Royalty Owner Code    Royalty Owner Name


*** Keywords ***
Find Royalty Owner Row By Filter
    [Documentation]    Explicitly filter the Royalty Owner grid's Code column to ${code} via
    ...    the shared T2 Find Object Row By Filter (resources/manage_object.resource) -
    ...    matches Account/Bank/State's own explicit filter usage, rather than relying only on
    ...    Select Object Row's implicit 3s-timeout fallback.
    [Arguments]    ${code}
    Find Object Row By Filter    ${ROYALTY_OWNER_TABLE}    ${code}

Clear Royalty Owner Row Filter
    [Documentation]    Clear the Code column filter (see Find Royalty Owner Row By Filter) via
    ...    the shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${ROYALTY_OWNER_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Royalty Owner's OWN credentials
    ...    (${ROYALTY_OWNER_EC_USER}/${ROYALTY_OWNER_EC_PASS} from credentials.py) on the
    ...    current page. Standing decision: every EC screen gets its own dedicated credential
    ...    pair. Zero-argument wrapper so royalty_owner_iud.robot's test cases read as a plain
    ...    business step; supplies Royalty Owner's own credential defaults to the shared T1
    ...    Login To EC Screen (common.resource), which owns the actual login mechanics.
    Login To EC Screen    ${ROYALTY_OWNER_EC_USER}    ${ROYALTY_OWNER_EC_PASS}

Open Royalty Owner Screen
    [Documentation]    Navigate to the Royalty Owner screen. Assumes the caller already logged
    ...    in this test case (via Login To EC Application) - this keyword ONLY navigates.
    ...    Delegates to the shared T1 Open EC Screen (common.resource) for the actual mechanics.
    Open EC Screen    ${ROYALTY_OWNER_SCREEN}

Insert Royalty Owner Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties
    ...    And Verify Code, so royalty_owner_iud.robot's test case body reads as a plain
    ...    business step with ZERO arguments. Also checks the inserted Code matches the
    ...    suite's ${TEST_CODE}. Pre-save evidence screenshot captured before Save is clicked,
    ...    matching Bank/State/Object List.
    [Arguments]    ${properties_path}=${ROYALTY_OWNER_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Royalty Owner Code
    RETURN    ${code}

Verify Royalty Owner Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (no DB check here, matching Bank/State/Object List's TC02
    ...    convention): row exists in the grid, then the form shows what was just inserted
    ...    (Royalty Owner Code/Royalty Owner Name only - Start Date is grid/insert-only, not
    ...    present in updateAttributes). Delegates the full sequence (row-check, select,
    ...    form-compare, screenshot) to the shared T2 Verify Object Insert Exists. Filters via
    ...    Find Royalty Owner Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Royalty Owner Row By Filter    ${code}
    Verify Object Insert Exists    ${ROYALTY_OWNER_TABLE}    ${code}    Royalty Owner
    ...    ${ROYALTY_OWNER_INSERT_PROPERTIES}    @{ROYALTY_OWNER_FORM_LABELS}
    ...    code_label=Royalty Owner Code
    Clear Royalty Owner Row Filter

Update Royalty Owner Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Pre-save evidence screenshot captured before Save is clicked, matching Bank/State/
    ...    Object List. Filters via Find Royalty Owner Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${ROYALTY_OWNER_UPDATE_PROPERTIES}
    Find Royalty Owner Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${ROYALTY_OWNER_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Royalty Owner Code
    Clear Royalty Owner Row Filter
    RETURN    ${data}

Verify Royalty Owner Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification, matching Bank/State/Object List's TC03 convention: the form shows
    ...    the updated Name. Delegates the full sequence (select, form-compare, screenshot)
    ...    to the shared T2 Verify Object Form Record. Filters via Find Royalty Owner Row By
    ...    Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Royalty Owner Row By Filter    ${code}
    Verify Object Form Record    ${ROYALTY_OWNER_TABLE}    ${code}    Royalty Owner
    ...    ${ROYALTY_OWNER_UPDATE_PROPERTIES}    Royalty Owner Name    code_label=Royalty Owner Code
    Clear Royalty Owner Row Filter

Find Royalty Owner Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Delegates the full select+capture sequence. Calls Find Royalty Owner Row By Filter
    ...    first. Deliberately does NOT clear the filter afterward - Verify Royalty Owner
    ...    Record Found (called right after, same TC) needs the grid still filtered to
    ...    ${code} for its own grid-check, since it doesn't re-select the row itself; it
    ...    clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Royalty Owner Row By Filter    ${code}
    Find Object Record    ${ROYALTY_OWNER_TABLE}    ${code}    Royalty Owner    code_label=Royalty Owner Code

Verify Royalty Owner Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the form record match the expected (post-update) data. Delegates the full
    ...    sequence (grid-compare, form-compare, screenshot) to the shared T2 Verify Object
    ...    Found. Caller must already have selected the row (TC04 does, via Find Royalty
    ...    Owner Record before this) AND left the Code filter active from that same call -
    ...    clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${ROYALTY_OWNER_TABLE}    ${code}    ${ROYALTY_OWNER_GRID_VERIFY_PROPERTIES}
    ...    ${ROYALTY_OWNER_FORM_VERIFY_PROPERTIES}    @{ROYALTY_OWNER_FORM_LABELS}
    Clear Royalty Owner Row Filter

Delete Royalty Owner Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date,
    ...    called with ZERO arguments (defaults ${code}/${date} to the suite's
    ...    ${TEST_CODE}/${END_DATE}). Select the royalty owner, set End Date = Start Date
    ...    (true delete), Save. Captures the TC05 evidence screenshot right after the End
    ...    Date is filled but BEFORE Save is clicked, matching Bank/State/Object List's
    ...    convention. Filters via Find Royalty Owner Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Royalty Owner Row By Filter    ${code}
    Delete Object Via End Date    ${ROYALTY_OWNER_TABLE}    ${ROYALTY_OWNER_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Royalty Owner Row Filter

Verify Royalty Owner Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is
    ...    absent from BOTH the grid and the database.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${ROYALTY_OWNER_TABLE}    OV_ROYALTY_OWNER    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Royalty Owner Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to
    ...    the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${ROYALTY_OWNER_TABLE}    ${code}
