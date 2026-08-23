*** Settings ***
Documentation       T3 (screen) — Customer page object.
...                 Screen: Configuration > Assets > Commercial Objects > Customer.
...                 Manage-Object (OV) screen. Holds Customer's locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common).
...                 Converted from the old hardcoded-field-id pattern to the label-driven,
...                 properties-file-driven, T2-consolidated "Bank pattern" (Batch 3, 2026-08-23).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${CUSTOMER_SCREEN}          Customer
${CUSTOMER_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/customer_insert.properties
${CUSTOMER_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/customer_update.properties
${CUSTOMER_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/customer_form_verify.properties
${CUSTOMER_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/customer_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal
# string (manage_object.resource defines this ONCE specifically so no T3 duplicates it).
${CUSTOMER_TABLE}       ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date). Hardcoded deliberately, NOT
# label-driven - same documented shape as Bank's own ${BANK_DEL_ENDDATE} (the row packs TWO
# fields, Start Date C:1 / End Date C:3, with the End Date label at C:2).
${CUSTOMER_DEL_ENDDATE}     tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Customer's own form-field label set (Start Date/End Date deliberately excluded - they live
# only in objectdates, not updateAttributes). Confirmed live 2026-08-23: objectForm AND
# updateAttributes both carry Code/Name/Description/ERP Customer Code/Official Name/Customer
# Group with the SAME mandatory set (Code, Name, Start Date, ERP Customer Code, Official Name,
# Customer Group - MandatoryCellStyle on each). Defined ONCE here so both Verify Customer Record
# Exists (TC02, against customer_insert.properties) and Verify Customer Record Found (TC04,
# against customer_form_verify.properties) share the same list.
@{CUSTOMER_FORM_LABELS}    Code    Name    Description    ERP Customer Code    Official Name
...    Customer Group


*** Keywords ***
Find Customer Row By Filter
    [Documentation]    Explicitly filter the Customer grid's Code column to ${code} via the
    ...    shared T2 Find Object Row By Filter (resources/manage_object.resource) - matches
    ...    Bank's/Account's own explicit filter usage (owner, 2026-08-22: "others... should
    ...    follow Account... utilise same filter feature").
    [Arguments]    ${code}
    Find Object Row By Filter    ${CUSTOMER_TABLE}    ${code}

Clear Customer Row Filter
    [Documentation]    Clear the Code column filter set by Find Customer Row By Filter, via
    ...    the shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${CUSTOMER_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Customer's OWN credentials (${CUSTOMER_EC_USER}/
    ...    ${CUSTOMER_EC_PASS} from credentials.py) on the current page - works whether this is
    ...    the very first login (page freshly loaded on the login form via the shared T1 Open EC
    ...    Application) or a re-login after Logout From EC Application. Screen-specific wrapper
    ...    (matches Bank's own pattern) that supplies Customer's own credential defaults to the
    ...    shared T1 Login To EC Screen (common.resource), which owns the actual login mechanics.
    Login To EC Screen    ${CUSTOMER_EC_USER}    ${CUSTOMER_EC_PASS}

Open Customer Screen
    [Documentation]    Navigate to the Customer screen. Assumes the caller already logged in
    ...    this test case (via Login To EC Application) - this keyword ONLY navigates.
    ...    Delegates to the shared T1 Open EC Screen (common.resource) for the actual mechanics.
    Open EC Screen    ${CUSTOMER_SCREEN}

Insert Customer Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Object From Properties, so
    ...    customer_iud.robot's test case body reads as a plain business step with ZERO
    ...    arguments - the underlying mechanics (properties-file-driven insert) are UNCHANGED.
    ...    Also owns the integrity check that the inserted Code matches the suite's ${TEST_CODE}
    ...    - this keyword fails on its own if testdata/customer_insert.properties' Code ever
    ...    drifts out of sync with the suite variable. The TC02 evidence screenshot is captured
    ...    BEFORE Save is clicked, passed through to Insert Object From Properties, which fills
    ...    every field first.
    [Arguments]    ${properties_path}=${CUSTOMER_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action
    RETURN    ${code}

Verify Customer Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN
    ...    verification (no DB check here): row exists in the grid, then every field's LIVE
    ...    SCREEN value (via Get OV Field Value By Label) is compared to
    ...    testdata/customer_insert.properties (the file used to insert, not the post-update
    ...    customer_form_verify.properties) - Code, Name, Description, ERP Customer Code,
    ...    Official Name, Customer Group (${CUSTOMER_FORM_LABELS}). Start Date is NOT verified
    ...    here - it only exists as a grid column / objectdates field, not an updateAttributes
    ...    field. Delegates the full sequence (row-check, select, form-compare, screenshot) to
    ...    the shared T2 Verify Object Insert Exists. Filters via Find Customer Row By Filter
    ...    first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Customer Row By Filter    ${code}
    Verify Object Insert Exists    ${CUSTOMER_TABLE}    ${code}    Customer    ${CUSTOMER_INSERT_PROPERTIES}
    ...    @{CUSTOMER_FORM_LABELS}
    Clear Customer Row Filter

Update Customer Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Returns
    ...    the applied {label: value} dict so the caller can DB-verify against exactly what was
    ...    set. The TC03 evidence screenshot is captured BEFORE Save is clicked. Filters via
    ...    Find Customer Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${CUSTOMER_UPDATE_PROPERTIES}
    Find Customer Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${CUSTOMER_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action
    Clear Customer Row Filter
    RETURN    ${data}

Verify Customer Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN
    ...    verification (no DB check): selects the row (loading updateAttributes), then compares
    ...    Name/Description's LIVE SCREEN value (via Get OV Field Value By Label) to
    ...    testdata/customer_update.properties - only those two labels, since that's the only
    ...    fields that file has. Delegates the full sequence (select, form-compare, screenshot)
    ...    to the shared T2 Verify Object Form Record. Filters via Find Customer Row By Filter
    ...    first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Customer Row By Filter    ${code}
    Verify Object Form Record    ${CUSTOMER_TABLE}    ${code}    Customer    ${CUSTOMER_UPDATE_PROPERTIES}
    ...    Name    Description
    Clear Customer Row Filter

Find Customer Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates
    ...    the full select+capture sequence. Calls Find Customer Row By Filter first. Deliberately
    ...    does NOT clear the filter afterward - Verify Customer Record Found (called right after,
    ...    same TC) needs the grid still filtered to ${code} for its own grid-check; it clears
    ...    the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Customer Row By Filter    ${code}
    Find Object Record    ${CUSTOMER_TABLE}    ${code}    Customer

Verify Customer Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid
    ...    AND the full form record match the expected data - the SAME two existing live-DOM
    ...    round-trip keywords, just called under one name. Also captures the TC04 evidence
    ...    screenshot. Delegates the full sequence (grid-compare, form-compare, screenshot) to
    ...    the shared T2 Verify Object Found. Caller must already have selected the row (TC04
    ...    does, via Find Customer Record before this) AND left the Code filter active from that
    ...    same call - clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${CUSTOMER_TABLE}    ${code}    ${CUSTOMER_GRID_VERIFY_PROPERTIES}
    ...    ${CUSTOMER_FORM_VERIFY_PROPERTIES}    @{CUSTOMER_FORM_LABELS}
    Clear Customer Row Filter

Delete Customer Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the customer, set End Date = Start Date (true delete), Save. Captures the TC05
    ...    evidence screenshot right after the End Date is filled but BEFORE Save is clicked.
    ...    Filters via Find Customer Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Customer Row By Filter    ${code}
    Delete Object Via End Date    ${CUSTOMER_TABLE}    ${CUSTOMER_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Customer Row Filter

Verify Customer Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is
    ...    absent from BOTH the grid and the database - the SAME two existing DB-ground-truth
    ...    keywords, just called under one name. Also captures the TC05 evidence screenshot.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${CUSTOMER_TABLE}    OV_CUSTOMER    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Customer Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to the shared
    ...    T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${CUSTOMER_TABLE}    ${code}
