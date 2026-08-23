*** Settings ***
Documentation       T3 (screen) — Vendor page object.
...                 Screen: Configuration > Assets > Commercial Objects > Vendor.
...                 Manage-Object (OV) screen. Holds Vendor's locators + thin IUD
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
${VENDOR_SCREEN}            Vendor
${VENDOR_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/vendor_insert.properties
${VENDOR_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/vendor_update.properties
${VENDOR_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/vendor_form_verify.properties
${VENDOR_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/vendor_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal
# string (manage_object.resource defines this ONCE specifically so no T3 duplicates it).
${VENDOR_TABLE}       ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date). Hardcoded deliberately, NOT
# label-driven - same documented shape as Bank's own ${BANK_DEL_ENDDATE} (the row packs TWO
# fields, Start Date C:1 / End Date C:3, with the End Date label at C:2).
${VENDOR_DEL_ENDDATE}     tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Vendor's own form-field label set (Start Date/End Date deliberately excluded - they live
# only in objectdates, not updateAttributes). Confirmed live 2026-08-23: objectForm AND
# updateAttributes both carry the SAME mandatory set (Code, Name, ERP Vendor Code, Official
# Name, Vendor Group - MandatoryCellStyle on each; Description is optional but included here to
# give TC03's Update a second field to change, matching Bank's/Customer's own precedent).
# Defined ONCE here so both Verify Vendor Record Exists (TC02, against vendor_insert.properties)
# and Verify Vendor Record Found (TC04, against vendor_form_verify.properties) share the same
# list.
@{VENDOR_FORM_LABELS}    Code    Name    Description    ERP Vendor Code    Official Name
...    Vendor Group


*** Keywords ***
Find Vendor Row By Filter
    [Documentation]    Explicitly filter the Vendor grid's Code column to ${code} via the
    ...    shared T2 Find Object Row By Filter (resources/manage_object.resource) - matches
    ...    Bank's/Account's/Customer's own explicit filter usage (owner, 2026-08-22: "others...
    ...    should follow Account... utilise same filter feature").
    [Arguments]    ${code}
    Find Object Row By Filter    ${VENDOR_TABLE}    ${code}

Clear Vendor Row Filter
    [Documentation]    Clear the Code column filter set by Find Vendor Row By Filter, via
    ...    the shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${VENDOR_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Vendor's OWN credentials (${VENDOR_EC_USER}/
    ...    ${VENDOR_EC_PASS} from credentials.py) on the current page - works whether this is
    ...    the very first login (page freshly loaded on the login form via the shared T1 Open EC
    ...    Application) or a re-login after Logout From EC Application. Screen-specific wrapper
    ...    (matches Bank's/Customer's own pattern) that supplies Vendor's own credential defaults
    ...    to the shared T1 Login To EC Screen (common.resource), which owns the actual login
    ...    mechanics.
    Login To EC Screen    ${VENDOR_EC_USER}    ${VENDOR_EC_PASS}

Open Vendor Screen
    [Documentation]    Navigate to the Vendor screen. Assumes the caller already logged in
    ...    this test case (via Login To EC Application) - this keyword ONLY navigates.
    ...    Delegates to the shared T1 Open EC Screen (common.resource) for the actual mechanics.
    Open EC Screen    ${VENDOR_SCREEN}

Insert Vendor Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Object From Properties, so
    ...    vendor_iud.robot's test case body reads as a plain business step with ZERO
    ...    arguments - the underlying mechanics (properties-file-driven insert) are UNCHANGED.
    ...    Also owns the integrity check that the inserted Code matches the suite's ${TEST_CODE}
    ...    - this keyword fails on its own if testdata/vendor_insert.properties' Code ever
    ...    drifts out of sync with the suite variable. The TC02 evidence screenshot is captured
    ...    BEFORE Save is clicked, passed through to Insert Object From Properties, which fills
    ...    every field first.
    [Arguments]    ${properties_path}=${VENDOR_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action
    RETURN    ${code}

Verify Vendor Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN
    ...    verification (no DB check here): row exists in the grid, then every field's LIVE
    ...    SCREEN value (via Get OV Field Value By Label) is compared to
    ...    testdata/vendor_insert.properties (the file used to insert, not the post-update
    ...    vendor_form_verify.properties) - Code, Name, Description, ERP Vendor Code, Official
    ...    Name, Vendor Group (${VENDOR_FORM_LABELS}). Start Date is NOT verified here - it only
    ...    exists as a grid column / objectdates field, not an updateAttributes field. Delegates
    ...    the full sequence (row-check, select, form-compare, screenshot) to the shared T2
    ...    Verify Object Insert Exists. Filters via Find Vendor Row By Filter first, clears
    ...    after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Vendor Row By Filter    ${code}
    Verify Object Insert Exists    ${VENDOR_TABLE}    ${code}    Vendor    ${VENDOR_INSERT_PROPERTIES}
    ...    @{VENDOR_FORM_LABELS}
    Clear Vendor Row Filter

Update Vendor Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Returns
    ...    the applied {label: value} dict so the caller can DB-verify against exactly what was
    ...    set. The TC03 evidence screenshot is captured BEFORE Save is clicked. Filters via
    ...    Find Vendor Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${VENDOR_UPDATE_PROPERTIES}
    Find Vendor Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${VENDOR_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action
    Clear Vendor Row Filter
    RETURN    ${data}

Verify Vendor Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN
    ...    verification (no DB check): selects the row (loading updateAttributes), then compares
    ...    Name/Description's LIVE SCREEN value (via Get OV Field Value By Label) to
    ...    testdata/vendor_update.properties - only those two labels, since that's the only
    ...    fields that file has. Delegates the full sequence (select, form-compare, screenshot)
    ...    to the shared T2 Verify Object Form Record. Filters via Find Vendor Row By Filter
    ...    first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Vendor Row By Filter    ${code}
    Verify Object Form Record    ${VENDOR_TABLE}    ${code}    Vendor    ${VENDOR_UPDATE_PROPERTIES}
    ...    Name    Description
    Clear Vendor Row Filter

Find Vendor Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates
    ...    the full select+capture sequence. Calls Find Vendor Row By Filter first. Deliberately
    ...    does NOT clear the filter afterward - Verify Vendor Record Found (called right after,
    ...    same TC) needs the grid still filtered to ${code} for its own grid-check; it clears
    ...    the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Vendor Row By Filter    ${code}
    Find Object Record    ${VENDOR_TABLE}    ${code}    Vendor

Verify Vendor Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid
    ...    AND the full form record match the expected data - the SAME two existing live-DOM
    ...    round-trip keywords, just called under one name. Also captures the TC04 evidence
    ...    screenshot. Delegates the full sequence (grid-compare, form-compare, screenshot) to
    ...    the shared T2 Verify Object Found. Caller must already have selected the row (TC04
    ...    does, via Find Vendor Record before this) AND left the Code filter active from that
    ...    same call - clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${VENDOR_TABLE}    ${code}    ${VENDOR_GRID_VERIFY_PROPERTIES}
    ...    ${VENDOR_FORM_VERIFY_PROPERTIES}    @{VENDOR_FORM_LABELS}
    Clear Vendor Row Filter

Delete Vendor Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the vendor, set End Date = Start Date (true delete), Save. Captures the TC05
    ...    evidence screenshot right after the End Date is filled but BEFORE Save is clicked.
    ...    Filters via Find Vendor Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Vendor Row By Filter    ${code}
    Delete Object Via End Date    ${VENDOR_TABLE}    ${VENDOR_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Vendor Row Filter

Verify Vendor Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is
    ...    absent from BOTH the grid and the database - the SAME two existing DB-ground-truth
    ...    keywords, just called under one name. Also captures the TC05 evidence screenshot.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${VENDOR_TABLE}    OV_VENDOR    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Vendor Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to the shared
    ...    T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${VENDOR_TABLE}    ${code}
