*** Settings ***
Documentation       T3 (screen) — Product Split Key page object.
...                 Screen: Configuration > Assets > Revenue Split Keys > Product Split Key
...                 (BF_CODE CD.0036, class SPLIT_KEY, view OV_SPLIT_KEY). Custom-URL OV screen
...                 (grid id nav:form:T_data, NO navigator/GO gate - confirmed live 2026-08-25
...                 via tmp/scan_product_split_key.py: zero nav fields, the grid loads directly
...                 with its own column-filter row; a navButton:form:B exists but is not a
...                 gating GO, clicking it is unnecessary) - same shape as Product Price Object
...                 (CD.0011, product_price_object_page.resource), used as this build's clone
...                 template. Label-driven, properties-file-driven, T2-consolidated pattern
...                 (bank_page.resource/cost_centre_page.resource style).
...
...                 One of 6 sibling "* Split Key" screens (Product/Company/Field/Stream Item
...                 Category/Other/Stream Item) that ALL share the SAME underlying class
...                 (SPLIT_KEY) and base view (OV_SPLIT_KEY), differentiated only by a
...                 server-side SPLIT_TYPE value bound to which menu entry/URL is opened
...                 (this screen's own real URL: manage_object_split_key/CLASS_NAME/SPLIT_KEY/
...                 SPLIT_TYPE/PRODUCT, confirmed live via page.url capture after open). Each
...                 sibling screen is built independently with its OWN distinctly-scoped fixed
...                 test code (this one: AUTOTEST_SPLITKEY_PRODUCT, confirmed free in
...                 OV_SPLIT_KEY via a fresh DB query before use) to avoid cross-screen
...                 collision on the shared view - do NOT reuse a generic "AUTOTEST_SPLIT_KEY"
...                 code for any of the 6.
...
...                 NOT the same screen as "Split Item Other" (CD.0017,
...                 pageobjects/.../split_item_other_page.resource, same folder) - that is a
...                 DIFFERENT, already-built, standalone screen on class SPLIT_ITEM_OTHER via
...                 the plain manage_object_nav controller, unrelated to this build.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${PRODUCT_SPLIT_KEY_SCREEN}    Product Split Key
${PRODUCT_SPLIT_KEY_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/product_split_key_insert.properties
${PRODUCT_SPLIT_KEY_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/product_split_key_update.properties
${PRODUCT_SPLIT_KEY_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/product_split_key_form_verify.properties
${PRODUCT_SPLIT_KEY_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/product_split_key_grid_verify.properties
# Grid id: CUSTOM-URL OV (not manage-object) - own constant, NOT T2's ${OV_MANAGE_OBJECT_TABLE}.
# Confirmed live 2026-08-25 (tmp/scan_product_split_key.py): nav:form:T_data, zero nav fields,
# the column-filter row already present (CODE/NAME/OBJECT_START_DATE/OBJECT_END_DATE).
${PRODUCT_SPLIT_KEY_TABLE}    nav:form:T_data
# objectdates field ID (Delete — End Date = Start Date), matching Bank/Product Price Object's
# framework-invariant objectdates layout (Start Date C:1, End Date C:3). Confirmed live
# 2026-08-25: tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input.
${PRODUCT_SPLIT_KEY_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Confirmed live 2026-08-25 (tmp/scan_product_split_key.py): the Code/Name labels on THIS
# screen are "Split Key Code"/"Split Key Name" (screen-prefixed), NOT the generic "Code"/"Name"
# Bank/Cost Centre use.
${PRODUCT_SPLIT_KEY_CODE_LABEL}    Split Key Code
# Form-field label set for the full-record compare (Verify Object Insert Exists/Verify Object
# Form Record). Start Date deliberately excluded - Insert-only (objectdates), not present in
# updateAttributes (confirmed live). Description/Comments/Value Method/Shares add to 100%/
# Rounding Rule/Number of Rounding Decimals/Number Display Format all confirmed live as NOT
# mandatory on the pristine Insert form and are left out of the round-trip compare - not filled
# with a specific asserted value this build.
@{PRODUCT_SPLIT_KEY_FORM_LABELS}    Split Key Code    Split Key Name


*** Keywords ***
Find Product Split Key Row By Filter
    [Documentation]    Explicitly filter the Product Split Key grid's Code column to ${code}
    ...    via the shared T2 Find Object Row By Filter (resources/manage_object.resource),
    ...    matching Bank/Product Price Object's explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${PRODUCT_SPLIT_KEY_TABLE}    ${code}

Clear Product Split Key Row Filter
    [Documentation]    Clear the Code column filter (see Find Product Split Key Row By
    ...    Filter) via the shared T2 Clear Object Row Filter, restoring the grid's normal
    ...    unfiltered view.
    Clear Object Row Filter    ${PRODUCT_SPLIT_KEY_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Product Split Key's OWN credentials
    ...    (${PRODUCT_SPLIT_KEY_EC_USER}/${PRODUCT_SPLIT_KEY_EC_PASS} from
    ...    credentials.py) on the current page - works whether this is the very first login or
    ...    a re-login after Logout From EC Application. Screen-specific wrapper (matches
    ...    Bank/Product Price Object's convention) supplying this screen's own credential
    ...    defaults to the shared T1 Login To EC Screen (common.resource), which owns the
    ...    actual mechanics.
    Login To EC Screen    ${PRODUCT_SPLIT_KEY_EC_USER}    ${PRODUCT_SPLIT_KEY_EC_PASS}

Open Product Split Key Screen
    [Documentation]    Navigate to the Product Split Key screen. Assumes the caller already
    ...    logged in this test case (via Login To EC Application) - this keyword ONLY
    ...    navigates. Delegates to the shared T1 Open EC Screen (common.resource). No
    ...    navigator/GO step needed - the grid is unscoped and loads immediately (confirmed
    ...    live: zero nav fields, no gating GO button).
    Open EC Screen    ${PRODUCT_SPLIT_KEY_SCREEN}

Insert Product Split Key Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties And
    ...    Verify Code, so product_split_key_iud.robot's test case body reads as a plain
    ...    business step with ZERO arguments - the underlying mechanics (properties-file-driven
    ...    insert, auto-detecting each field's kind by label) are UNCHANGED. Also checks the
    ...    inserted Code matches the suite's ${TEST_CODE}. Pre-save evidence screenshot
    ...    captured before Save is clicked.
    [Arguments]    ${properties_path}=${PRODUCT_SPLIT_KEY_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=${PRODUCT_SPLIT_KEY_CODE_LABEL}
    RETURN    ${code}

Verify Product Split Key Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (no DB check here, matching Bank/Product Price Object's TC02
    ...    convention): row exists in the grid, then the form shows what was just inserted
    ...    (Split Key Code/Name - ${PRODUCT_SPLIT_KEY_FORM_LABELS}). Delegates the full
    ...    sequence (row-check, select, form-compare, screenshot) to the shared T2 Verify
    ...    Object Insert Exists. Filters via Find Product Split Key Row By Filter first, clears
    ...    after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Product Split Key Row By Filter    ${code}
    Verify Object Insert Exists    ${PRODUCT_SPLIT_KEY_TABLE}    ${code}    Product Split Key
    ...    ${PRODUCT_SPLIT_KEY_INSERT_PROPERTIES}    @{PRODUCT_SPLIT_KEY_FORM_LABELS}
    ...    code_label=${PRODUCT_SPLIT_KEY_CODE_LABEL}
    Clear Product Split Key Row Filter

Update Product Split Key Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Returns
    ...    the applied {label: value} dict so the caller can compare against exactly what was
    ...    set. Pre-save evidence screenshot captured before Save is clicked. Filters via Find
    ...    Product Split Key Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${PRODUCT_SPLIT_KEY_UPDATE_PROPERTIES}
    Find Product Split Key Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${PRODUCT_SPLIT_KEY_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=${PRODUCT_SPLIT_KEY_CODE_LABEL}
    Clear Product Split Key Row Filter
    RETURN    ${data}

Verify Product Split Key Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification: selects the row (loading updateAttributes), then compares Split Key
    ...    Name's LIVE SCREEN value to testdata/product_split_key_update.properties. Delegates
    ...    the full sequence (select, form-compare, screenshot) to the shared T2 Verify Object
    ...    Form Record. Filters via Find Product Split Key Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Product Split Key Row By Filter    ${code}
    Verify Object Form Record    ${PRODUCT_SPLIT_KEY_TABLE}    ${code}    Product Split Key
    ...    ${PRODUCT_SPLIT_KEY_UPDATE_PROPERTIES}    Split Key Name
    ...    code_label=${PRODUCT_SPLIT_KEY_CODE_LABEL}
    Clear Product Split Key Row Filter

Find Product Split Key Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Delegates the full select+capture sequence. Calls Find Product Split Key Row By
    ...    Filter first. Deliberately does NOT clear the filter afterward - Verify Product
    ...    Split Key Record Found (called right after, same TC) needs the grid still filtered
    ...    for its own grid-check; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Product Split Key Row By Filter    ${code}
    Find Object Record    ${PRODUCT_SPLIT_KEY_TABLE}    ${code}    Product Split Key
    ...    code_label=${PRODUCT_SPLIT_KEY_CODE_LABEL}

Verify Product Split Key Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the full form record match the expected (post-update) data. Delegates the
    ...    full sequence (grid-compare, form-compare, screenshot) to the shared T2 Verify
    ...    Object Found. Caller must already have selected the row (TC04 does, via Find Product
    ...    Split Key Record before this) AND left the Code filter active - clears the filter
    ...    itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${PRODUCT_SPLIT_KEY_TABLE}    ${code}
    ...    ${PRODUCT_SPLIT_KEY_GRID_VERIFY_PROPERTIES}    ${PRODUCT_SPLIT_KEY_FORM_VERIFY_PROPERTIES}
    ...    @{PRODUCT_SPLIT_KEY_FORM_LABELS}
    Clear Product Split Key Row Filter

Delete Product Split Key Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date,
    ...    called with ZERO arguments (defaults ${code}/${date} to the suite's
    ...    ${TEST_CODE}/${END_DATE}). Select the record, set End Date = Start Date (true
    ...    delete for this VERSIONED class), Save. Captures the TC05 evidence screenshot right
    ...    after the End Date is filled but BEFORE Save is clicked. Filters via Find Product
    ...    Split Key Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Product Split Key Row By Filter    ${code}
    Delete Object Via End Date    ${PRODUCT_SPLIT_KEY_TABLE}    ${PRODUCT_SPLIT_KEY_DEL_ENDDATE}
    ...    ${code}    ${date}    ${TEST NAME}_action
    Clear Product Split Key Row Filter

Verify Product Split Key Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is
    ...    absent from BOTH the grid and the database (OV_SPLIT_KEY).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${PRODUCT_SPLIT_KEY_TABLE}    OV_SPLIT_KEY    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Product Split Key Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to the
    ...    shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${PRODUCT_SPLIT_KEY_TABLE}    ${code}
