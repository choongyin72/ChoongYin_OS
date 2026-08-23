*** Settings ***
Documentation       T3 (screen) — Product Description page object.
...                 Screen: Configuration > Assets > Financial Objects > Product Description.
...                 Manage-Object (OV) screen. Holds Product Description's locators + thin IUD
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
${PRODUCT_DESCRIPTION_SCREEN}    Product Description
${PRODUCT_DESCRIPTION_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/product_description_insert.properties
${PRODUCT_DESCRIPTION_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/product_description_update.properties
${PRODUCT_DESCRIPTION_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/product_description_form_verify.properties
${PRODUCT_DESCRIPTION_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/product_description_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal
# string (manage_object.resource defines this ONCE specifically so no T3 duplicates it).
${PRODUCT_DESCRIPTION_TABLE}    ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date). Hardcoded deliberately, NOT
# label-driven - same documented shape as Bank's/Customer's/VAT Code's own del-enddate id (the
# row packs TWO fields, Start Date C:1 / End Date C:3, with the End Date label at C:2) -
# live-confirmed present on this screen too (2026-08-23,
# tmp/recon_product_description.robot "Recon ObjectDates Form": element count = 1).
${PRODUCT_DESCRIPTION_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Product Description's own Code label is SCREEN-PREFIXED ("Product Node Item Code"), not the
# generic "Code" - confirmed live 2026-08-23 (objectForm AND updateAttributes both show it,
# tmp/recon_product_description.robot). Passed as code_label to every T2 keyword that accepts it.
${PRODUCT_DESCRIPTION_CODE_LABEL}    Product Node Item Code
# Product Description's own form-field label set (Start Date/End Date deliberately excluded -
# they live only in objectdates, not updateAttributes; confirmed live 2026-08-23 via the
# updateAttributes ECCell label dump). Product/Node/Financial Code are mandatory reference
# dropdowns (MandatoryCellStyle confirmed live), present in BOTH objectForm and
# updateAttributes. Defined ONCE here so both Verify Product Description Record Exists (TC02,
# against product_description_insert.properties) and Verify Product Description Record Found
# (TC04, against product_description_form_verify.properties) share the same list.
@{PRODUCT_DESCRIPTION_FORM_LABELS}    ${PRODUCT_DESCRIPTION_CODE_LABEL}    Name    Description
...    Product    Node    Financial Code


*** Keywords ***
Find Product Description Row By Filter
    [Documentation]    Explicitly filter the Product Description grid's Code column to ${code}
    ...    via the shared T2 Find Object Row By Filter (resources/manage_object.resource) -
    ...    matches Bank's/Account's/Customer's own explicit filter usage (owner, 2026-08-22:
    ...    "others... should follow Account... utilise same filter feature").
    [Arguments]    ${code}
    Find Object Row By Filter    ${PRODUCT_DESCRIPTION_TABLE}    ${code}

Clear Product Description Row Filter
    [Documentation]    Clear the Code column filter set by Find Product Description Row By
    ...    Filter, via the shared T2 Clear Object Row Filter, restoring the grid's normal
    ...    unfiltered view.
    Clear Object Row Filter    ${PRODUCT_DESCRIPTION_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Product Description's OWN credentials
    ...    (${PRODUCT_DESCRIPTION_EC_USER}/${PRODUCT_DESCRIPTION_EC_PASS} from credentials.py)
    ...    on the current page - works whether this is the very first login (page freshly
    ...    loaded on the login form via the shared T1 Open EC Application) or a re-login after
    ...    Logout From EC Application. Screen-specific wrapper (matches Bank's/Customer's own
    ...    pattern) that supplies Product Description's own credential defaults to the shared
    ...    T1 Login To EC Screen (common.resource), which owns the actual login mechanics.
    Login To EC Screen    ${PRODUCT_DESCRIPTION_EC_USER}    ${PRODUCT_DESCRIPTION_EC_PASS}

Open Product Description Screen
    [Documentation]    Navigate to the Product Description screen. Assumes the caller already
    ...    logged in this test case (via Login To EC Application) - this keyword ONLY
    ...    navigates. Delegates to the shared T1 Open EC Screen (common.resource) for the
    ...    actual mechanics.
    Open EC Screen    ${PRODUCT_DESCRIPTION_SCREEN}

Insert Product Description Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Object From Properties, so
    ...    product_description_iud.robot's test case body reads as a plain business step with
    ...    ZERO arguments - the underlying mechanics (properties-file-driven insert) are
    ...    UNCHANGED. Also owns the integrity check that the inserted Code matches the suite's
    ...    ${TEST_CODE} - this keyword fails on its own if
    ...    testdata/product_description_insert.properties' Code ever drifts out of sync with
    ...    the suite variable. The TC02 evidence screenshot is captured BEFORE Save is clicked,
    ...    passed through to Insert Object From Properties, which fills every field first.
    [Arguments]    ${properties_path}=${PRODUCT_DESCRIPTION_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=${PRODUCT_DESCRIPTION_CODE_LABEL}
    RETURN    ${code}

Verify Product Description Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN
    ...    verification (no DB check here): row exists in the grid, then every field's LIVE
    ...    SCREEN value (via Get OV Field Value By Label) is compared to
    ...    testdata/product_description_insert.properties (the file used to insert, not the
    ...    post-update product_description_form_verify.properties) -
    ...    ${PRODUCT_DESCRIPTION_FORM_LABELS}. Start Date is NOT verified here - it only exists
    ...    as a grid column / objectdates field, not an updateAttributes field. Delegates the
    ...    full sequence (row-check, select, form-compare, screenshot) to the shared T2 Verify
    ...    Object Insert Exists. Filters via Find Product Description Row By Filter first,
    ...    clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Product Description Row By Filter    ${code}
    Verify Object Insert Exists    ${PRODUCT_DESCRIPTION_TABLE}    ${code}    Product Description
    ...    ${PRODUCT_DESCRIPTION_INSERT_PROPERTIES}    @{PRODUCT_DESCRIPTION_FORM_LABELS}
    ...    code_label=${PRODUCT_DESCRIPTION_CODE_LABEL}
    Clear Product Description Row Filter

Update Product Description Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Returns
    ...    the applied {label: value} dict so the caller can DB-verify against exactly what was
    ...    set. The TC03 evidence screenshot is captured BEFORE Save is clicked. Filters via
    ...    Find Product Description Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${PRODUCT_DESCRIPTION_UPDATE_PROPERTIES}
    Find Product Description Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${PRODUCT_DESCRIPTION_TABLE}    ${code}
    ...    ${properties_path}    ${TEST NAME}_action    code_label=${PRODUCT_DESCRIPTION_CODE_LABEL}
    Clear Product Description Row Filter
    RETURN    ${data}

Verify Product Description Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN
    ...    verification (no DB check): selects the row (loading updateAttributes), then
    ...    compares Name/Description's LIVE SCREEN value (via Get OV Field Value By Label) to
    ...    testdata/product_description_update.properties - only those two labels, since
    ...    that's the only fields that file has. Delegates the full sequence (select,
    ...    form-compare, screenshot) to the shared T2 Verify Object Form Record. Filters via
    ...    Find Product Description Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Product Description Row By Filter    ${code}
    Verify Object Form Record    ${PRODUCT_DESCRIPTION_TABLE}    ${code}    Product Description
    ...    ${PRODUCT_DESCRIPTION_UPDATE_PROPERTIES}    Name    Description
    ...    code_label=${PRODUCT_DESCRIPTION_CODE_LABEL}
    Clear Product Description Row Filter

Find Product Description Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Delegates the full select+capture sequence. Calls Find Product Description Row By
    ...    Filter first. Deliberately does NOT clear the filter afterward - Verify Product
    ...    Description Record Found (called right after, same TC) needs the grid still
    ...    filtered to ${code} for its own grid-check; it clears the filter once both checks
    ...    are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Product Description Row By Filter    ${code}
    Find Object Record    ${PRODUCT_DESCRIPTION_TABLE}    ${code}    Product Description
    ...    code_label=${PRODUCT_DESCRIPTION_CODE_LABEL}

Verify Product Description Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the full form record match the expected data - the SAME two existing
    ...    live-DOM round-trip keywords, just called under one name. Also captures the TC04
    ...    evidence screenshot. Delegates the full sequence (grid-compare, form-compare,
    ...    screenshot) to the shared T2 Verify Object Found. Caller must already have selected
    ...    the row (TC04 does, via Find Product Description Record before this) AND left the
    ...    Code filter active from that same call - clears the filter itself once both checks
    ...    are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${PRODUCT_DESCRIPTION_TABLE}    ${code}
    ...    ${PRODUCT_DESCRIPTION_GRID_VERIFY_PROPERTIES}    ${PRODUCT_DESCRIPTION_FORM_VERIFY_PROPERTIES}
    ...    @{PRODUCT_DESCRIPTION_FORM_LABELS}
    Clear Product Description Row Filter

Delete Product Description Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date,
    ...    called with ZERO arguments (defaults ${code}/${date} to the suite's
    ...    ${TEST_CODE}/${END_DATE}). Select the product description, set End Date = Start Date
    ...    (true delete), Save. Captures the TC05 evidence screenshot right after the End Date
    ...    is filled but BEFORE Save is clicked. Filters via Find Product Description Row By
    ...    Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Product Description Row By Filter    ${code}
    Delete Object Via End Date    ${PRODUCT_DESCRIPTION_TABLE}    ${PRODUCT_DESCRIPTION_DEL_ENDDATE}
    ...    ${code}    ${date}    ${TEST NAME}_action
    Clear Product Description Row Filter

Verify Product Description Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is
    ...    absent from BOTH the grid and the database - the SAME two existing DB-ground-truth
    ...    keywords, just called under one name. Also captures the TC05 evidence screenshot.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${PRODUCT_DESCRIPTION_TABLE}    OV_PRODUCT_NODE_ITEM    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Product Description Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to the
    ...    shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${PRODUCT_DESCRIPTION_TABLE}    ${code}
