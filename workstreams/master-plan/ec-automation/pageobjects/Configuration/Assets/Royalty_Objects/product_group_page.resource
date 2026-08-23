*** Settings ***
Documentation       T3 (screen) — Product Group page object.
...                 Screen: Configuration > Assets > Royalty Objects > Product Group.
...                 Manage-Object (OV) screen. Holds Product Group's locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common).
...                 Rebuilt 2026-08-23 (Batch 5) to mirror Bank/State exactly (owner:
...                 "reflect the current EC screen exactly the same way as the OV_BANK
...                 IUD related task") - replaces the older hardcoded-field-id pattern
...                 with the label-driven, properties-file-driven, T2-consolidated pattern.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${PG_SCREEN}            Product Group
${PG_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/product_group_insert.properties
${PG_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/product_group_update.properties
${PG_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/product_group_form_verify.properties
${PG_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/product_group_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal.
${PG_TABLE}             ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date), matching Bank/State's convention -
# confirmed unchanged in this screen's objectdates panel (same tab:tabPanel:objectdates
# shape as every other manage-object OV screen tested this batch).
${PG_DEL_ENDDATE}       tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Product Group's own form-field label set. Labels are "Product Group Code"/"Product Group
# Name" (screen-prefixed) - confirmed live 2026-08-23 via the New Object form label dump
# (objectForm ECCell scan); NOT the generic "Code"/"Name" Bank/Object List use. Start Date
# deliberately excluded - Insert-only, not present in updateAttributes (confirmed live:
# updateAttributes shows only Product Group Code, Product Group Name, Sort Order, Product
# Group Type, Comments). Sort Order/Product Group Type/Comments are optional fields, left
# out of this suite's IUD flow (fill-only-needed-fields convention) - not exercised here.
# Defined ONCE here so both Verify Product Group Record Exists (TC02) and Verify Product
# Group Record Found (TC04) share the same list.
@{PG_FORM_LABELS}       Product Group Code    Product Group Name


*** Keywords ***
Find Product Group Row By Filter
    [Documentation]    Explicitly filter the Product Group grid's Code column to ${code} via
    ...    the shared T2 Find Object Row By Filter (resources/manage_object.resource) -
    ...    matches Bank/State/Account's own explicit filter usage (owner, 2026-08-22:
    ...    "others (Bank, State, List_Object) should follow Account... utilise same filter
    ...    feature"), rather than relying only on Select Object Row's implicit 3s-timeout
    ...    fallback.
    [Arguments]    ${code}
    Find Object Row By Filter    ${PG_TABLE}    ${code}

Clear Product Group Row Filter
    [Documentation]    Clear the Code column filter (see Find Product Group Row By Filter)
    ...    via the shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered
    ...    view.
    Clear Object Row Filter    ${PG_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Product Group's OWN credentials
    ...    (${PRODUCT_GROUP_EC_USER}/${PRODUCT_GROUP_EC_PASS} from credentials.py) on the
    ...    current page. Standing decision (owner, 2026-08-22): every EC screen gets its own
    ...    dedicated credential pair. Zero-argument wrapper so product_group_iud.robot's test
    ...    cases read as a plain business step; supplies Product Group's own credential
    ...    defaults to the shared T1 Login To EC Screen (common.resource), which owns the
    ...    actual login mechanics.
    Login To EC Screen    ${PRODUCT_GROUP_EC_USER}    ${PRODUCT_GROUP_EC_PASS}

Open Product Group Screen
    [Documentation]    Navigate to the Product Group screen. Assumes the caller already
    ...    logged in this test case (via Login To EC Application) - this keyword ONLY
    ...    navigates. Delegates to the shared T1 Open EC Screen (common.resource) for the
    ...    actual mechanics.
    Open EC Screen    ${PG_SCREEN}

Insert Product Group Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties
    ...    And Verify Code, so product_group_iud.robot's test case body reads as a plain
    ...    business step with ZERO arguments. Also checks the inserted Code matches the
    ...    suite's ${TEST_CODE}. Pre-save evidence screenshot captured before Save is
    ...    clicked, matching Bank/State.
    [Arguments]    ${properties_path}=${PG_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Product Group Code
    RETURN    ${code}

Verify Product Group Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (no DB check here, matching Bank/State's TC02 convention): row
    ...    exists in the grid, then the form shows what was just inserted (Product Group
    ...    Code/Product Group Name only - Start Date is grid/insert-only, not present in
    ...    updateAttributes). Delegates the full sequence (row-check, select, form-compare,
    ...    screenshot) to the shared T2 Verify Object Insert Exists. Filters via Find
    ...    Product Group Row By Filter first, clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find Product Group Row By Filter    ${code}
    Verify Object Insert Exists    ${PG_TABLE}    ${code}    Product Group    ${PG_INSERT_PROPERTIES}
    ...    @{PG_FORM_LABELS}    code_label=Product Group Code
    Clear Product Group Row Filter

Update Product Group Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Pre-save evidence screenshot captured before Save is clicked, matching Bank/State.
    ...    Filters via Find Product Group Row By Filter first, clears after (2026-08-22
    ...    standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${PG_UPDATE_PROPERTIES}
    Find Product Group Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${PG_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Product Group Code
    Clear Product Group Row Filter
    RETURN    ${data}

Verify Product Group Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification, matching Bank/State's TC03 convention: the form shows the updated
    ...    Name. Delegates the full sequence (select, form-compare, screenshot) to the
    ...    shared T2 Verify Object Form Record. Filters via Find Product Group Row By
    ...    Filter first, clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find Product Group Row By Filter    ${code}
    Verify Object Form Record    ${PG_TABLE}    ${code}    Product Group    ${PG_UPDATE_PROPERTIES}
    ...    Product Group Name    code_label=Product Group Code
    Clear Product Group Row Filter

Find Product Group Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Delegates the full select+capture sequence. Calls Find Product Group Row By
    ...    Filter first (2026-08-22 standardisation). Deliberately does NOT clear the
    ...    filter afterward - Verify Product Group Record Found (called right after, same
    ...    TC) needs the grid still filtered to ${code} for its own grid-check, since it
    ...    doesn't re-select the row itself; it clears the filter once both checks are
    ...    done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Product Group Row By Filter    ${code}
    Find Object Record    ${PG_TABLE}    ${code}    Product Group    code_label=Product Group Code

Verify Product Group Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the form record match the expected (post-update) data. Delegates the
    ...    full sequence (grid-compare, form-compare, screenshot) to the shared T2 Verify
    ...    Object Found. Caller must already have selected the row (TC04 does, via Find
    ...    Product Group Record before this) AND left the Code filter active from that same
    ...    call - clears the filter itself once both checks are done (2026-08-22
    ...    standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${PG_TABLE}    ${code}    ${PG_GRID_VERIFY_PROPERTIES}
    ...    ${PG_FORM_VERIFY_PROPERTIES}    @{PG_FORM_LABELS}
    Clear Product Group Row Filter

Delete Product Group Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date,
    ...    called with ZERO arguments (defaults ${code}/${date} to the suite's
    ...    ${TEST_CODE}/${END_DATE}). Select the product group, set End Date = Start Date
    ...    (true delete), Save. Captures the TC05 evidence screenshot right after the End
    ...    Date is filled but BEFORE Save is clicked, matching Bank/State's convention.
    ...    Filters via Find Product Group Row By Filter first, clears after (2026-08-22
    ...    standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Product Group Row By Filter    ${code}
    Delete Object Via End Date    ${PG_TABLE}    ${PG_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Product Group Row Filter

Verify Product Group Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code}
    ...    is absent from BOTH the grid and the database.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${PG_TABLE}    OV_PRODUCT_GROUP    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Product Group Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to
    ...    the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${PG_TABLE}    ${code}
