*** Settings ***
Documentation       T3 (screen) — Product Price Object page object.
...                 Screen: Configuration > Assets > Sales Objects > Product Price Object
...                 (BF_CODE CD.0011, class PRICE_OBJECT, view OV_PRICE_OBJECT). Custom-URL OV
...                 screen (grid id nav:form:T_data, NO navigator - confirmed live 2026-08-25:
...                 zero nav fields, no GO button at all; reload is via T2's Save And Refresh
...                 List, which auto-detects the missing GO and falls back to toolbar Refresh -
...                 same shape as Cost Centre). Label-driven, properties-file-driven, T2-
...                 consolidated pattern (bank_page.resource/cost_centre_page.resource style).
...
...                 NOT the same screen/BF_CODE as the ALREADY-SHIPPED "Price Object"
...                 (CO.3016, pageobjects/Configuration/Assets/Sales_Objects/price_object_page.resource)
...                 - CO.3016 is an OV-GM screen reached via manage_object_navmodel_nav with a
...                 mandatory Business Unit navigator gate; this screen (CD.0011) is reached via
...                 a distinct custom "general_price_object" controller with NO navigator at all,
...                 confirmed via a live DB lookup (BUSINESS_FUNCTION.NAME/URL) and a live DOM
...                 scan before this build - both bind to the SAME underlying class
...                 (PRICE_OBJECT/OV_PRICE_OBJECT) but are genuinely separate menu entries/screens.
...                 Price Object Code/Name are screen-prefixed labels (NOT the generic
...                 "Code"/"Name"), matching Price Object/State/Product's own convention.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${PRODUCT_PRICE_OBJECT_SCREEN}    Product Price Object
${PRODUCT_PRICE_OBJECT_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/product_price_object_insert.properties
${PRODUCT_PRICE_OBJECT_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/product_price_object_update.properties
${PRODUCT_PRICE_OBJECT_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/product_price_object_form_verify.properties
${PRODUCT_PRICE_OBJECT_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/product_price_object_grid_verify.properties
# Grid id: CUSTOM-URL OV (not manage-object) - own constant, NOT T2's ${OV_MANAGE_OBJECT_TABLE}
# (that one is manage_object_nav_nav:form:T_data, a different screen family - the OV-GM "Price
# Object" CO.3016 uses yet a THIRD id, manageObject:form:T_data). Confirmed live 2026-08-25:
# nav:form:T_data count=1, zero nav fields, GO button count=0.
${PRODUCT_PRICE_OBJECT_TABLE}    nav:form:T_data
# objectdates field ID (Delete — End Date = Start Date), matching Bank/Cost Centre/Price
# Object's framework-invariant objectdates layout (Start Date C:1, End Date C:3).
${PRODUCT_PRICE_OBJECT_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Confirmed live 2026-08-25 (scan_product_price_object.py): the Code/Name labels on THIS screen
# are "Price Object Code"/"Price Object Name" (screen-prefixed), matching CO.3016's own labels
# for the same underlying class - NOT the generic "Code"/"Name" Bank/Cost Centre use.
${PRODUCT_PRICE_OBJECT_CODE_LABEL}    Price Object Code
# Form-field label set for the full-record compare (Verify Object Insert Exists/Verify Object
# Form Record). Start Date deliberately excluded - Insert-only (objectdates), not present in
# updateAttributes (confirmed live). Product Name/Price Concept/UOM are included since they DO
# appear on updateAttributes (confirmed live scan); Price Rounding Rule/Business Unit/Currency/
# Contract Name/Comments are left OUT of the round-trip compare - they exist on the form but
# were not filled with a specific asserted value (dropdowns filled __FIRST__, whose resolved
# text is not predictable ahead of a live run).
@{PRODUCT_PRICE_OBJECT_FORM_LABELS}    Price Object Code    Price Object Name


*** Keywords ***
Find Product Price Object Row By Filter
    [Documentation]    Explicitly filter the Product Price Object grid's Code column to ${code}
    ...    via the shared T2 Find Object Row By Filter (resources/manage_object.resource),
    ...    matching Bank/Cost Centre/Product's explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${PRODUCT_PRICE_OBJECT_TABLE}    ${code}

Clear Product Price Object Row Filter
    [Documentation]    Clear the Code column filter (see Find Product Price Object Row By
    ...    Filter) via the shared T2 Clear Object Row Filter, restoring the grid's normal
    ...    unfiltered view.
    Clear Object Row Filter    ${PRODUCT_PRICE_OBJECT_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Product Price Object's OWN credentials
    ...    (${PRODUCT_PRICE_OBJECT_EC_USER}/${PRODUCT_PRICE_OBJECT_EC_PASS} from
    ...    credentials.py) on the current page - works whether this is the very first login or
    ...    a re-login after Logout From EC Application. Screen-specific wrapper (matches
    ...    Bank/Cost Centre's convention) supplying this screen's own credential defaults to
    ...    the shared T1 Login To EC Screen (common.resource), which owns the actual mechanics.
    Login To EC Screen    ${PRODUCT_PRICE_OBJECT_EC_USER}    ${PRODUCT_PRICE_OBJECT_EC_PASS}

Open Product Price Object Screen
    [Documentation]    Navigate to the Product Price Object screen. Assumes the caller already
    ...    logged in this test case (via Login To EC Application) - this keyword ONLY
    ...    navigates. Delegates to the shared T1 Open EC Screen (common.resource). No
    ...    navigator/GO step needed - the grid is unscoped and loads immediately (confirmed
    ...    live: zero nav fields, no GO button).
    Open EC Screen    ${PRODUCT_PRICE_OBJECT_SCREEN}

Insert Product Price Object Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties And
    ...    Verify Code, so product_price_object_iud.robot's test case body reads as a plain
    ...    business step with ZERO arguments - the underlying mechanics (properties-file-driven
    ...    insert, auto-detecting each field's kind by label) are UNCHANGED. Also checks the
    ...    inserted Code matches the suite's ${TEST_CODE}. Pre-save evidence screenshot
    ...    captured before Save is clicked.
    [Arguments]    ${properties_path}=${PRODUCT_PRICE_OBJECT_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=${PRODUCT_PRICE_OBJECT_CODE_LABEL}
    RETURN    ${code}

Verify Product Price Object Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (no DB check here, matching Bank/Cost Centre's TC02 convention): row
    ...    exists in the grid, then the form shows what was just inserted (Price Object
    ...    Code/Name - ${PRODUCT_PRICE_OBJECT_FORM_LABELS}). Delegates the full sequence
    ...    (row-check, select, form-compare, screenshot) to the shared T2 Verify Object Insert
    ...    Exists. Filters via Find Product Price Object Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Product Price Object Row By Filter    ${code}
    Verify Object Insert Exists    ${PRODUCT_PRICE_OBJECT_TABLE}    ${code}    Product Price Object
    ...    ${PRODUCT_PRICE_OBJECT_INSERT_PROPERTIES}    @{PRODUCT_PRICE_OBJECT_FORM_LABELS}
    ...    code_label=${PRODUCT_PRICE_OBJECT_CODE_LABEL}
    Clear Product Price Object Row Filter

Update Product Price Object Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Returns
    ...    the applied {label: value} dict so the caller can DB-verify against exactly what was
    ...    set. Pre-save evidence screenshot captured before Save is clicked. Filters via Find
    ...    Product Price Object Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${PRODUCT_PRICE_OBJECT_UPDATE_PROPERTIES}
    Find Product Price Object Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${PRODUCT_PRICE_OBJECT_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=${PRODUCT_PRICE_OBJECT_CODE_LABEL}
    Clear Product Price Object Row Filter
    RETURN    ${data}

Verify Product Price Object Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification: selects the row (loading updateAttributes), then compares Price Object
    ...    Name's LIVE SCREEN value to testdata/product_price_object_update.properties.
    ...    Delegates the full sequence (select, form-compare, screenshot) to the shared T2
    ...    Verify Object Form Record. Filters via Find Product Price Object Row By Filter
    ...    first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Product Price Object Row By Filter    ${code}
    Verify Object Form Record    ${PRODUCT_PRICE_OBJECT_TABLE}    ${code}    Product Price Object
    ...    ${PRODUCT_PRICE_OBJECT_UPDATE_PROPERTIES}    Price Object Name
    ...    code_label=${PRODUCT_PRICE_OBJECT_CODE_LABEL}
    Clear Product Price Object Row Filter

Find Product Price Object Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Delegates the full select+capture sequence. Calls Find Product Price Object Row By
    ...    Filter first. Deliberately does NOT clear the filter afterward - Verify Product
    ...    Price Object Record Found (called right after, same TC) needs the grid still
    ...    filtered for its own grid-check; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Product Price Object Row By Filter    ${code}
    Find Object Record    ${PRODUCT_PRICE_OBJECT_TABLE}    ${code}    Product Price Object
    ...    code_label=${PRODUCT_PRICE_OBJECT_CODE_LABEL}

Verify Product Price Object Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the full form record match the expected (post-update) data. Delegates the
    ...    full sequence (grid-compare, form-compare, screenshot) to the shared T2 Verify
    ...    Object Found. Caller must already have selected the row (TC04 does, via Find Product
    ...    Price Object Record before this) AND left the Code filter active - clears the filter
    ...    itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${PRODUCT_PRICE_OBJECT_TABLE}    ${code}
    ...    ${PRODUCT_PRICE_OBJECT_GRID_VERIFY_PROPERTIES}    ${PRODUCT_PRICE_OBJECT_FORM_VERIFY_PROPERTIES}
    ...    @{PRODUCT_PRICE_OBJECT_FORM_LABELS}
    Clear Product Price Object Row Filter

Delete Product Price Object Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date,
    ...    called with ZERO arguments (defaults ${code}/${date} to the suite's
    ...    ${TEST_CODE}/${END_DATE}). Select the record, set End Date = Start Date (true
    ...    delete for this VERSIONED class), Save. Captures the TC05 evidence screenshot right
    ...    after the End Date is filled but BEFORE Save is clicked. Filters via Find Product
    ...    Price Object Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Product Price Object Row By Filter    ${code}
    Delete Object Via End Date    ${PRODUCT_PRICE_OBJECT_TABLE}    ${PRODUCT_PRICE_OBJECT_DEL_ENDDATE}
    ...    ${code}    ${date}    ${TEST NAME}_action
    Clear Product Price Object Row Filter

Verify Product Price Object Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is
    ...    absent from BOTH the grid and the database (OV_PRICE_OBJECT).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${PRODUCT_PRICE_OBJECT_TABLE}    OV_PRICE_OBJECT    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Product Price Object Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to the
    ...    shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${PRODUCT_PRICE_OBJECT_TABLE}    ${code}
