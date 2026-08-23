*** Settings ***
Documentation       T3 (screen) — State Lease page object.
...                 Screen: Configuration > Assets > Commercial Objects > State Lease.
...                 Manage-Object (OV) screen. Holds State Lease's locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common).
...                 Converted from the old hardcoded-field-id pattern to the label-driven,
...                 properties-file-driven, T2-consolidated "Bank pattern" (Batch 4, 2026-08-23).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${STATE_LEASE_SCREEN}          State Lease
${STATE_LEASE_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/state_lease_insert.properties
${STATE_LEASE_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/state_lease_update.properties
${STATE_LEASE_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/state_lease_form_verify.properties
${STATE_LEASE_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/state_lease_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal
# string (manage_object.resource defines this ONCE specifically so no T3 duplicates it).
${STATE_LEASE_TABLE}    ${OV_MANAGE_OBJECT_TABLE}
# State Lease's own Code label - screen-prefixed, NOT the generic "Code" (confirmed live
# 2026-08-23 via a field-inventory scan of objectForm/updateAttributes: this screen labels
# its fields "State Lease Code"/"State Lease Name", matching State's own "State Code"
# precedent (owner note in manage_object.resource, 2026-08-22) rather than Bank/Customer's
# generic "Code"/"Name").
${STATE_LEASE_CODE_LABEL}    State Lease Code
# objectdates field ID (Delete — End Date = Start Date). Hardcoded deliberately, NOT
# label-driven - same documented shape as Bank's/Customer's own DEL_ENDDATE (the row packs
# TWO fields, Start Date C:1 / End Date C:3, with the End Date label at C:2) - confirmed live
# 2026-08-23 (this exact id round-tripped a live insert+delete during recon).
${STATE_LEASE_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# State Lease's own form-field label set (Start Date/End Date deliberately excluded - a live
# scan 2026-08-23 confirmed updateAttributes only carries State Lease Code/State Lease Name/
# Description; Start Date lives only in objectForm (mandatory there) and objectdates, End Date
# only in objectForm (optional there) and objectdates - neither is present in updateAttributes,
# so neither can be verified via Verify Object Form Record, which always reads updateAttributes).
# Defined ONCE here so both Verify State Lease Record Exists (TC02, against
# state_lease_insert.properties) and Verify State Lease Record Found (TC04, against
# state_lease_form_verify.properties) share the same list.
@{STATE_LEASE_FORM_LABELS}    State Lease Code    State Lease Name    Description


*** Keywords ***
Find State Lease Row By Filter
    [Documentation]    Explicitly filter the State Lease grid's Code column to ${code} via the
    ...    shared T2 Find Object Row By Filter (resources/manage_object.resource) - matches
    ...    Bank's/Customer's own explicit filter usage (owner, 2026-08-22: "others... should
    ...    follow Account... utilise same filter feature").
    [Arguments]    ${code}
    Find Object Row By Filter    ${STATE_LEASE_TABLE}    ${code}

Clear State Lease Row Filter
    [Documentation]    Clear the Code column filter set by Find State Lease Row By Filter, via
    ...    the shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${STATE_LEASE_TABLE}

Login To EC Application
    [Documentation]    Authenticate as State Lease's OWN credentials (${STATE_LEASE_EC_USER}/
    ...    ${STATE_LEASE_EC_PASS} from credentials.py) on the current page - works whether this
    ...    is the very first login (page freshly loaded on the login form via the shared T1 Open
    ...    EC Application) or a re-login after Logout From EC Application. Screen-specific
    ...    wrapper (matches Bank's/Customer's own pattern) that supplies State Lease's own
    ...    credential defaults to the shared T1 Login To EC Screen (common.resource), which
    ...    owns the actual login mechanics.
    Login To EC Screen    ${STATE_LEASE_EC_USER}    ${STATE_LEASE_EC_PASS}

Open State Lease Screen
    [Documentation]    Navigate to the State Lease screen. Assumes the caller already logged in
    ...    this test case (via Login To EC Application) - this keyword ONLY navigates. Delegates
    ...    to the shared T1 Open EC Screen (common.resource) for the actual mechanics. Confirmed
    ...    live 2026-08-23: no mandatory navigator/cascade dropdown blocks this screen's grid -
    ...    only the universal as-at-date + GO bar every manage-object OV screen shows.
    Open EC Screen    ${STATE_LEASE_SCREEN}

Insert State Lease Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Object From Properties, so
    ...    state_lease_iud.robot's test case body reads as a plain business step with ZERO
    ...    arguments - the underlying mechanics (properties-file-driven insert) are UNCHANGED.
    ...    Also owns the integrity check that the inserted Code matches the suite's ${TEST_CODE}
    ...    - this keyword fails on its own if testdata/state_lease_insert.properties' Code ever
    ...    drifts out of sync with the suite variable. The TC02 evidence screenshot is captured
    ...    BEFORE Save is clicked, passed through to Insert Object From Properties, which fills
    ...    every field first.
    [Arguments]    ${properties_path}=${STATE_LEASE_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=${STATE_LEASE_CODE_LABEL}
    RETURN    ${code}

Verify State Lease Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN
    ...    verification (no DB check here): row exists in the grid, then every field's LIVE
    ...    SCREEN value (via Get OV Field Value By Label) is compared to
    ...    testdata/state_lease_insert.properties (the file used to insert, not the post-update
    ...    state_lease_form_verify.properties) - State Lease Code, State Lease Name, Description
    ...    (${STATE_LEASE_FORM_LABELS}). Start Date is NOT verified here - it lives only in
    ...    objectForm/objectdates, not updateAttributes. Delegates the full sequence (row-check,
    ...    select, form-compare, screenshot) to the shared T2 Verify Object Insert Exists.
    ...    Filters via Find State Lease Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find State Lease Row By Filter    ${code}
    Verify Object Insert Exists    ${STATE_LEASE_TABLE}    ${code}    State Lease
    ...    ${STATE_LEASE_INSERT_PROPERTIES}    @{STATE_LEASE_FORM_LABELS}
    ...    code_label=${STATE_LEASE_CODE_LABEL}
    Clear State Lease Row Filter

Update State Lease Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Returns
    ...    the applied {label: value} dict so the caller can DB-verify against exactly what was
    ...    set. The TC03 evidence screenshot is captured BEFORE Save is clicked. Filters via
    ...    Find State Lease Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${STATE_LEASE_UPDATE_PROPERTIES}
    Find State Lease Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${STATE_LEASE_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=${STATE_LEASE_CODE_LABEL}
    Clear State Lease Row Filter
    RETURN    ${data}

Verify State Lease Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN
    ...    verification (no DB check): selects the row (loading updateAttributes), then compares
    ...    State Lease Name/Description's LIVE SCREEN value (via Get OV Field Value By Label) to
    ...    testdata/state_lease_update.properties - only those two labels, since that's the only
    ...    fields that file has. Delegates the full sequence (select, form-compare, screenshot)
    ...    to the shared T2 Verify Object Form Record. Filters via Find State Lease Row By
    ...    Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find State Lease Row By Filter    ${code}
    Verify Object Form Record    ${STATE_LEASE_TABLE}    ${code}    State Lease
    ...    ${STATE_LEASE_UPDATE_PROPERTIES}    State Lease Name    Description
    ...    code_label=${STATE_LEASE_CODE_LABEL}
    Clear State Lease Row Filter

Find State Lease Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates
    ...    the full select+capture sequence. Calls Find State Lease Row By Filter first.
    ...    Deliberately does NOT clear the filter afterward - Verify State Lease Record Found
    ...    (called right after, same TC) needs the grid still filtered to ${code} for its own
    ...    grid-check; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find State Lease Row By Filter    ${code}
    Find Object Record    ${STATE_LEASE_TABLE}    ${code}    State Lease    code_label=${STATE_LEASE_CODE_LABEL}

Verify State Lease Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid
    ...    AND the full form record match the expected data - the SAME two existing live-DOM
    ...    round-trip keywords, just called under one name. Also captures the TC04 evidence
    ...    screenshot. Delegates the full sequence (grid-compare, form-compare, screenshot) to
    ...    the shared T2 Verify Object Found. Caller must already have selected the row (TC04
    ...    does, via Find State Lease Record before this) AND left the Code filter active from
    ...    that same call - clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${STATE_LEASE_TABLE}    ${code}    ${STATE_LEASE_GRID_VERIFY_PROPERTIES}
    ...    ${STATE_LEASE_FORM_VERIFY_PROPERTIES}    @{STATE_LEASE_FORM_LABELS}
    Clear State Lease Row Filter

Delete State Lease Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the state lease, set End Date = Start Date (true delete), Save. Captures the
    ...    TC05 evidence screenshot right after the End Date is filled but BEFORE Save is
    ...    clicked. Filters via Find State Lease Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find State Lease Row By Filter    ${code}
    Delete Object Via End Date    ${STATE_LEASE_TABLE}    ${STATE_LEASE_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear State Lease Row Filter

Verify State Lease Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is
    ...    absent from BOTH the grid and the database - the SAME two existing DB-ground-truth
    ...    keywords, just called under one name. Also captures the TC05 evidence screenshot.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${STATE_LEASE_TABLE}    OV_STATE_LEASE    ${code}
    Capture Step    ${TEST NAME}_verify

Verify State Lease Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to the
    ...    shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${STATE_LEASE_TABLE}    ${code}
