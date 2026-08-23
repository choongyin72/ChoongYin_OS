*** Settings ***
Documentation       T3 (screen) — Sales Order page object.
...                 Screen: Configuration > Assets > Financial Objects > Sales Order.
...                 Manage-Object (OV) screen. Holds Sales Order's locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common).
...                 Rebuilt 2026-08-23 (Batch 5) to mirror Bank/Cost Object Mapping exactly -
...                 replaces the older hardcoded-field-id pattern with the label-driven,
...                 properties-file-driven, T2-consolidated pattern.
...                 Live-confirmed 2026-08-23 (tmp/recon_so.py + tmp/recon_so_dd.py +
...                 tmp/recon_so_dates.py - deleted before final commit): NAV_DD_COUNT=0 (no
...                 mandatory nav dropdown - only the universal Date+GO as-at-date bar), so this
...                 is a genuine nav-free manage-object OV, NOT a document-header-plus-lines
...                 shape (naming concern from tmp/batch5_shared_findings.md resolved - same
...                 outcome as Cost Object Mapping in Batch 4). objectForm order is Product Sales
...                 Order Code, Name, Start Date, End Date, Description, Comments, Restrict Use
...                 (checkbox), Company, Field. Code label is SCREEN-PREFIXED
...                 **"Product Sales Order Code"** (NOT generic "Code", same pattern as Product
...                 Description). TWO mandatory reference dropdowns beyond Code/Name/Start Date
...                 (confirmed via MandatoryCellStyle on the wrapping <span>): Company, Field -
...                 NEITHER is a cascade (both populate immediately, no "Dependent field" banner).
...                 End Date/Description/Comments/Restrict Use are all optional and omitted (IUD
...                 fills only needed fields). Real literal option text used for insert (NOT
...                 __FIRST__ - Batch 2 VAT Code gotcha): Company="Acme Chemicals" (same clean
...                 option already proven on Cost Object Mapping), Field="Apollo" (clean option,
...                 no leading/internal double-spaces unlike several sibling options e.g.
...                 "  Esso Kizomba"). updateAttributes carries Code (read-only guard), Name,
...                 Description, Comments, Restrict Use, Company, Field - no Start/End Date
...                 (same convention as Bank/Cost Object Mapping - dates live only in
...                 objectForm/objectdates). Grid shows Product Sales Order Code/Name/Start
...                 Date/End Date (20+ existing rows, e.g. BU_0001). objectdates: Start Date
...                 C:1/End Date label C:2/End Date input C:3 (same row-packing convention as
...                 Bank/Cost Object Mapping).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${SALES_ORDER_SCREEN}          Sales Order
${SALES_ORDER_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/sales_order_insert.properties
${SALES_ORDER_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/sales_order_update.properties
${SALES_ORDER_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/sales_order_form_verify.properties
${SALES_ORDER_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/sales_order_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal
# string (manage_object.resource defines this ONCE specifically so no T3 duplicates it).
${SALES_ORDER_TABLE}       ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date). Hardcoded deliberately, NOT
# label-driven - same documented shape as Bank's/Cost Object Mapping's own DEL_ENDDATE (the row
# packs TWO fields, Start Date C:1 / End Date C:3, with the End Date label at C:2) - confirmed
# live 2026-08-23 (objectdates plan: single row, End Date at C:3).
${SALES_ORDER_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Sales Order's own form-field label set, using its real SCREEN-PREFIXED Code label. Defined
# ONCE here so both Verify Sales Order Record Exists (TC02, against
# sales_order_insert.properties) and Verify Sales Order Record Found (TC04, against
# sales_order_form_verify.properties) share the same list.
@{SALES_ORDER_FORM_LABELS}    Product Sales Order Code    Name    Company    Field


*** Keywords ***
Find Sales Order Row By Filter
    [Documentation]    Explicitly filter the Sales Order grid's Code column to ${code} via the
    ...    shared T2 Find Object Row By Filter (resources/manage_object.resource) - matches
    ...    Bank's/Cost Object Mapping's own explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${SALES_ORDER_TABLE}    ${code}

Clear Sales Order Row Filter
    [Documentation]    Clear the Code column filter set by Find Sales Order Row By Filter, via
    ...    the shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${SALES_ORDER_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Sales Order's OWN credentials
    ...    (${SALES_ORDER_EC_USER}/${SALES_ORDER_EC_PASS} from credentials.py) on the current
    ...    page - works whether this is the very first login (page freshly loaded on the login
    ...    form via the shared T1 Open EC Application) or a re-login after Logout From EC
    ...    Application. Screen-specific wrapper (matches Bank's/Cost Object Mapping's own
    ...    pattern) that supplies Sales Order's own credential defaults to the shared T1 Login
    ...    To EC Screen (common.resource), which owns the actual login mechanics.
    Login To EC Screen    ${SALES_ORDER_EC_USER}    ${SALES_ORDER_EC_PASS}

Open Sales Order Screen
    [Documentation]    Navigate to the Sales Order screen. Assumes the caller already logged in
    ...    this test case (via Login To EC Application) - this keyword ONLY navigates.
    ...    Delegates to the shared T1 Open EC Screen (common.resource) for the actual mechanics.
    Open EC Screen    ${SALES_ORDER_SCREEN}

Insert Sales Order Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Object From Properties, so
    ...    sales_order_iud.robot's test case body reads as a plain business step with ZERO
    ...    arguments - the underlying mechanics (properties-file-driven insert) are UNCHANGED.
    ...    Also owns the integrity check that the inserted Code matches the suite's
    ...    ${TEST_CODE} - this keyword fails on its own if testdata/sales_order_insert.properties'
    ...    Code ever drifts out of sync with the suite variable. The TC02 evidence screenshot is
    ...    captured BEFORE Save is clicked, passed through to Insert Object From Properties,
    ...    which fills every field first (in file order).
    [Arguments]    ${properties_path}=${SALES_ORDER_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Product Sales Order Code
    RETURN    ${code}

Verify Sales Order Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN
    ...    verification (no DB check here): row exists in the grid, then every field's LIVE
    ...    SCREEN value (via Get OV Field Value By Label) is compared to
    ...    testdata/sales_order_insert.properties (the file used to insert, not the post-update
    ...    sales_order_form_verify.properties) - Product Sales Order Code, Name, Company, Field
    ...    (${SALES_ORDER_FORM_LABELS}). Start Date is NOT verified here - it only exists as a
    ...    grid column / objectdates field, not an updateAttributes field. Delegates the full
    ...    sequence (row-check, select, form-compare, screenshot) to the shared T2 Verify Object
    ...    Insert Exists. Filters via Find Sales Order Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Sales Order Row By Filter    ${code}
    Verify Object Insert Exists    ${SALES_ORDER_TABLE}    ${code}    Sales Order
    ...    ${SALES_ORDER_INSERT_PROPERTIES}    @{SALES_ORDER_FORM_LABELS}
    ...    code_label=Product Sales Order Code
    Clear Sales Order Row Filter

Update Sales Order Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Returns
    ...    the applied {label: value} dict so the caller can DB-verify against exactly what was
    ...    set. The TC03 evidence screenshot is captured BEFORE Save is clicked. Filters via
    ...    Find Sales Order Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${SALES_ORDER_UPDATE_PROPERTIES}
    Find Sales Order Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${SALES_ORDER_TABLE}    ${code}
    ...    ${properties_path}    ${TEST NAME}_action    code_label=Product Sales Order Code
    Clear Sales Order Row Filter
    RETURN    ${data}

Verify Sales Order Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN
    ...    verification (no DB check): selects the row (loading updateAttributes), then compares
    ...    Name's LIVE SCREEN value (via Get OV Field Value By Label) to
    ...    testdata/sales_order_update.properties - only that label, since that's the only field
    ...    this file has. Delegates the full sequence (select, form-compare, screenshot) to the
    ...    shared T2 Verify Object Form Record. Filters via Find Sales Order Row By Filter first,
    ...    clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Sales Order Row By Filter    ${code}
    Verify Object Form Record    ${SALES_ORDER_TABLE}    ${code}    Sales Order
    ...    ${SALES_ORDER_UPDATE_PROPERTIES}    Name    code_label=Product Sales Order Code
    Clear Sales Order Row Filter

Find Sales Order Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates the full
    ...    select+capture sequence. Calls Find Sales Order Row By Filter first. Deliberately does
    ...    NOT clear the filter afterward - Verify Sales Order Record Found (called right after,
    ...    same TC) needs the grid still filtered to ${code} for its own grid-check; it clears
    ...    the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Sales Order Row By Filter    ${code}
    Find Object Record    ${SALES_ORDER_TABLE}    ${code}    Sales Order
    ...    code_label=Product Sales Order Code

Verify Sales Order Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND
    ...    the full form record match the expected data - the SAME two existing live-DOM
    ...    round-trip keywords, just called under one name. Also captures the TC04 evidence
    ...    screenshot. Delegates the full sequence (grid-compare, form-compare, screenshot) to
    ...    the shared T2 Verify Object Found. Caller must already have selected the row (TC04
    ...    does, via Find Sales Order Record before this) AND left the Code filter active from
    ...    that same call - clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${SALES_ORDER_TABLE}    ${code}
    ...    ${SALES_ORDER_GRID_VERIFY_PROPERTIES}    ${SALES_ORDER_FORM_VERIFY_PROPERTIES}
    ...    @{SALES_ORDER_FORM_LABELS}
    Clear Sales Order Row Filter

Delete Sales Order Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the sales order, set End Date = Start Date (true delete), Save. Captures the
    ...    TC05 evidence screenshot right after the End Date is filled but BEFORE Save is
    ...    clicked. Filters via Find Sales Order Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Sales Order Row By Filter    ${code}
    Delete Object Via End Date    ${SALES_ORDER_TABLE}    ${SALES_ORDER_DEL_ENDDATE}
    ...    ${code}    ${date}    ${TEST NAME}_action
    Clear Sales Order Row Filter

Verify Sales Order Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid and the database - the SAME two existing DB-ground-truth keywords,
    ...    just called under one name. Also captures the TC05 evidence screenshot.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${SALES_ORDER_TABLE}    OV_PRODUCT_SALES_ORDER    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Sales Order Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to the shared
    ...    T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${SALES_ORDER_TABLE}    ${code}
