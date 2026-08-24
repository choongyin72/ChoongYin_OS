*** Settings ***
Documentation       T3 (screen) — Product page object.
...                 Screen: Configuration > Assets > Hydrocarbon Objects > Product (CO.0007,
...                 class PRODUCT, view OV_PRODUCT). Manage-Object (OV) screen. Holds Product's
...                 locators + thin IUD wrappers that delegate to T2 (manage_object) and T1
...                 (common). NOT the same class as the already-automated siblings "Product
...                 Description" (CD.0012) or "Product Group" (RC.0053) - this is PRODUCT_MAINTAIN.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${PRODUCT_SCREEN}          Product
${PRODUCT_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/product_insert.properties
${PRODUCT_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/product_update.properties
${PRODUCT_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/product_form_verify.properties
${PRODUCT_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/product_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal string
# (manage_object.resource defines this ONCE specifically so no T3 duplicates it). Confirmed
# live via scan_ec_screen.py (2026-08-24): grid id is manage_object_nav_nav:form:T_data, GO
# button:form:B present - this IS the plain manage-object (OV) family, not OV_CUSTOM_URL.
${PRODUCT_TABLE}           ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date). Hardcoded deliberately, NOT
# label-driven: confirmed live (2026-08-24 scan_ec_screen.py) that this row packs TWO fields
# (Start Date C:1, End Date C:3) with the same "Start Date" label text reported for both - the
# same shape already documented on Bank (py/ec_object_iud.py END_DATE_ID), so the C:3 convention
# is reused here rather than trusting the one-field-per-row label scan for this row.
${PRODUCT_DEL_ENDDATE}     tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Product's own Code field is labelled "Product Code" (NOT the generic "Code" Bank/Object List
# use) - confirmed live via scan_ec_screen.py (2026-08-24). Every T2 keyword that defaults
# code_label to "Code" is called with code_label=${PRODUCT_CODE_LABEL} below, matching the same
# pattern State's build already proved necessary for a screen-prefixed Code label.
${PRODUCT_CODE_LABEL}      Product Code
# Product's own form-field label set for the full-record compare (Verify Object Insert Exists /
# Verify Object Form Record). Start Date deliberately excluded - it lives only in objectdates,
# not updateAttributes (confirmed live, matches Bank's convention). Hydrocarbon Component,
# Product Group, Product Type, ERP Code are all optional dropdowns left unset (no live-verified
# valid option values for AUTOTEST data) - not included here since they are never filled.
@{PRODUCT_FORM_LABELS}    Product Code    Product Name    Description    Sort Order


*** Keywords ***
Find Product Row By Filter
    [Documentation]    Explicitly filter the Product grid's Code column to ${code} via the
    ...    shared T2 Find Object Row By Filter (resources/manage_object.resource) - matches
    ...    Bank's/Account's own explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${PRODUCT_TABLE}    ${code}

Clear Product Row Filter
    [Documentation]    Clear the Code column filter (see Find Product Row By Filter) via the
    ...    shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${PRODUCT_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Product's OWN credentials (${PRODUCT_EC_USER}/
    ...    ${PRODUCT_EC_PASS} from credentials.py) on the current page - works whether this is
    ...    the very first login (page freshly loaded on the login form via the shared T1 Open EC
    ...    Application) or a re-login after Logout From EC Application (same login form, not a
    ...    new page/tab). Screen-specific wrapper (matches Bank's convention) that supplies
    ...    Product's own credential defaults to the shared T1 Login To EC Screen
    ...    (common.resource), which owns the actual login mechanics.
    Login To EC Screen    ${PRODUCT_EC_USER}    ${PRODUCT_EC_PASS}

Open Product Screen
    [Documentation]    Navigate to the Product screen. Assumes the caller already logged in
    ...    this test case (via Login To EC Application) - this keyword ONLY navigates.
    ...    Delegates to the shared T1 Open EC Screen (common.resource) for the actual mechanics.
    Open EC Screen    ${PRODUCT_SCREEN}

Insert Product Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Product From Properties, purely
    ...    so product_iud.robot's test case body reads as a plain business step with ZERO
    ...    arguments - the underlying mechanics (properties-file-driven insert) are UNCHANGED.
    ...    Also owns the integrity check that the inserted Code matches the suite's
    ...    ${TEST_CODE} - fails on its own if testdata/product_insert.properties' Product Code
    ...    ever drifts out of sync with the suite variable. The TC02 evidence screenshot is
    ...    captured BEFORE Save is clicked, passed through to Insert Object From Properties,
    ...    which fills every field first.
    [Arguments]    ${properties_path}=${PRODUCT_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=${PRODUCT_CODE_LABEL}
    RETURN    ${code}

Verify Product Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification: row
    ...    exists in the grid, then every field's LIVE SCREEN value (via Get OV Field Value By
    ...    Label) is compared to testdata/product_insert.properties - Product Code, Product
    ...    Name, Description, Sort Order (${PRODUCT_FORM_LABELS}). NOTE: Start Date is NOT
    ...    verified anywhere in this keyword - it only exists as a grid column / objectdates
    ...    field, not an updateAttributes form field (matches Bank's convention).
    ...    Delegates the full sequence (row-check, select, form-compare, screenshot) to the
    ...    shared T2 Verify Object Insert Exists. Filters via Find Product Row By Filter first,
    ...    clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Product Row By Filter    ${code}
    Verify Object Insert Exists    ${PRODUCT_TABLE}    ${code}    Product    ${PRODUCT_INSERT_PROPERTIES}
    ...    @{PRODUCT_FORM_LABELS}    code_label=${PRODUCT_CODE_LABEL}
    Clear Product Row Filter

Update Product Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Returns
    ...    the applied {label: value} dict so the caller can DB-verify against exactly what was
    ...    set. The TC03 evidence screenshot is captured BEFORE Save is clicked. Filters via
    ...    Find Product Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${PRODUCT_UPDATE_PROPERTIES}
    Find Product Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${PRODUCT_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=${PRODUCT_CODE_LABEL}
    Clear Product Row Filter
    RETURN    ${data}

Verify Product Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification:
    ...    selects the row (loading updateAttributes), then compares Product Name/Description's
    ...    LIVE SCREEN value (via Get OV Field Value By Label) to testdata/product_update.properties
    ...    - only those two labels, since that's the only fields that file has. Delegates the
    ...    full sequence (select, form-compare, screenshot) to the shared T2 Verify Object Form
    ...    Record. Filters via Find Product Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Product Row By Filter    ${code}
    Verify Object Form Record    ${PRODUCT_TABLE}    ${code}    Product    ${PRODUCT_UPDATE_PROPERTIES}
    ...    Product Name    Description    code_label=${PRODUCT_CODE_LABEL}
    Clear Product Row Filter

Find Product Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates
    ...    the full select+capture sequence. Calls Find Product Row By Filter first.
    ...    Deliberately does NOT clear the filter afterward - Verify Product Record Found
    ...    (called right after, same TC) needs the grid still filtered to ${code} for its own
    ...    grid-check, since it doesn't re-select the row itself; it clears the filter once both
    ...    checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Product Row By Filter    ${code}
    Find Object Record    ${PRODUCT_TABLE}    ${code}    Product    code_label=${PRODUCT_CODE_LABEL}

Verify Product Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND
    ...    the full form record match the expected data. Also captures the TC04 evidence
    ...    screenshot. Delegates the full sequence (grid-compare, form-compare, screenshot) to
    ...    the shared T2 Verify Object Found. Caller must already have selected the row (TC04
    ...    does, via Find Product Record before this) AND left the Code filter active from that
    ...    same call - clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${PRODUCT_TABLE}    ${code}    ${PRODUCT_GRID_VERIFY_PROPERTIES}
    ...    ${PRODUCT_FORM_VERIFY_PROPERTIES}    @{PRODUCT_FORM_LABELS}
    Clear Product Row Filter

Delete Product Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the product, set End Date = Start Date (true delete), Save. Captures the TC05
    ...    evidence screenshot right after the End Date is filled but BEFORE Save is clicked.
    ...    Filters via Find Product Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Product Row By Filter    ${code}
    Delete Object Via End Date    ${PRODUCT_TABLE}    ${PRODUCT_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Product Row Filter

Verify Product Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid and the database - the SAME two existing DB-ground-truth keywords,
    ...    just called under one name. Also captures the TC05 evidence screenshot.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${PRODUCT_TABLE}    ov_product    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Product Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to the
    ...    shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${PRODUCT_TABLE}    ${code}
