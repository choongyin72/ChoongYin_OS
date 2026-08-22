*** Settings ***
Documentation       T3 (screen) — Revenue Order page object.
...                 Screen: Configuration > Assets > Financial Objects > Revenue Order.
...                 Custom-URL OV screen (NO navigator, NO GO button) — grid is
...                 nav:form:T_data (not manage_object_nav_nav:form:T_data), reload via
...                 toolbar Refresh; T2's Save And Refresh List auto-detects this (checks
...                 for a visible GO button, falls back to Refresh Screen) — confirmed
...                 live 2026-08-22 (grid-id scan: nav:form:T_data count=1,
...                 manage_object_nav_ count=0, GO button count=0). Rebuilt to mirror
...                 Bank/State exactly (owner: "reflect the current EC screen exactly the
...                 same way as the OV_BANK IUD related task") - replaces the older
...                 hardcoded-field-id/generated-code pattern with the label-driven,
...                 properties-file-driven, T2-consolidated pattern.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${REVENUE_ORDER_SCREEN}    Revenue Order
${REVENUE_ORDER_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/revenue_order_insert.properties
${REVENUE_ORDER_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/revenue_order_update.properties
${REVENUE_ORDER_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/revenue_order_form_verify.properties
${REVENUE_ORDER_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/revenue_order_grid_verify.properties
# Custom-URL OV grid id — confirmed live 2026-08-22 (nav:form:T_data count=1, manage_object_nav_
# count=0), NOT T2's ${OV_MANAGE_OBJECT_TABLE} constant (that is the manage-object variant's grid).
${REVENUE_ORDER_TABLE}    nav:form:T_data
# objectdates field ID (Delete — End Date = Start Date), matching Bank/State's convention.
${REVENUE_ORDER_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Revenue Order's own form-field label set: "Code"/"Name" - the generic Bank-family labels
# (NOT screen-prefixed like State's "State Code"/"State Name") - confirmed live 2026-08-22 via
# the New Object form scan (objectForm field dump) AND the updateAttributes scan on the real
# existing row RO_01 (read-only select, no edits/Save). Start Date deliberately excluded -
# Insert-only, not present in updateAttributes. Defined ONCE here so both Verify Revenue Order
# Record Exists (TC02) and Verify Revenue Order Record Found (TC04) share the same list.
@{REVENUE_ORDER_FORM_LABELS}    Code    Name


*** Keywords ***
Login To EC Application
    [Documentation]    Authenticate as Revenue Order's OWN credentials
    ...    (${REVENUE_ORDER_EC_USER}/${REVENUE_ORDER_EC_PASS} from credentials.py) on the
    ...    current page. Standing decision (owner, 2026-08-22): every EC screen gets its own
    ...    dedicated credential pair. Zero-argument wrapper so revenue_order_iud.robot's test
    ...    cases read as a plain business step; supplies Revenue Order's own credential
    ...    defaults to the shared T1 Login To EC Screen (common.resource), which owns the
    ...    actual login mechanics.
    Login To EC Screen    ${REVENUE_ORDER_EC_USER}    ${REVENUE_ORDER_EC_PASS}

Open Revenue Order Screen
    [Documentation]    Navigate to the Revenue Order screen. Assumes the caller already
    ...    logged in this test case (via Login To EC Application) - this keyword ONLY
    ...    navigates. Delegates to the shared T1 Open EC Screen (common.resource) for the
    ...    actual mechanics.
    Open EC Screen    ${REVENUE_ORDER_SCREEN}

Insert Revenue Order Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties
    ...    And Verify Code, so revenue_order_iud.robot's test case body reads as a plain
    ...    business step with ZERO arguments. Also checks the inserted Code matches the
    ...    suite's ${TEST_CODE}. Pre-save evidence screenshot captured before Save is
    ...    clicked, matching Bank/State. code_label defaults to "Code" (Revenue Order's real
    ...    label, confirmed live) so it is omitted here.
    [Arguments]    ${properties_path}=${REVENUE_ORDER_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action
    RETURN    ${code}

Verify Revenue Order Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (no DB check here, matching Bank/State's TC02 convention): row
    ...    exists in the grid, then the form shows what was just inserted (Code/Name only -
    ...    Start Date is grid/insert-only, not present in updateAttributes). Delegates the
    ...    full sequence (row-check, select, form-compare, screenshot) to the shared T2
    ...    Verify Object Insert Exists.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Insert Exists    ${REVENUE_ORDER_TABLE}    ${code}    Revenue Order
    ...    ${REVENUE_ORDER_INSERT_PROPERTIES}    @{REVENUE_ORDER_FORM_LABELS}

Update Revenue Order Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Pre-save evidence screenshot captured before Save is clicked, matching Bank/State.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${REVENUE_ORDER_UPDATE_PROPERTIES}
    ${data}=    Update Object From Properties    ${REVENUE_ORDER_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action
    RETURN    ${data}

Verify Revenue Order Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification, matching Bank/State's TC03 convention: the form shows the updated
    ...    Name. Delegates the full sequence (select, form-compare, screenshot) to the
    ...    shared T2 Verify Object Form Record.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Form Record    ${REVENUE_ORDER_TABLE}    ${code}    Revenue Order
    ...    ${REVENUE_ORDER_UPDATE_PROPERTIES}    Name

Find Revenue Order Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Delegates the full select+capture sequence.
    [Arguments]    ${code}=${TEST_CODE}
    Find Object Record    ${REVENUE_ORDER_TABLE}    ${code}    Revenue Order

Verify Revenue Order Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the form record match the expected (post-update) data. Delegates the
    ...    full sequence (grid-compare, form-compare, screenshot) to the shared T2 Verify
    ...    Object Found. Caller must already have selected the row (TC04 does, via Find
    ...    Revenue Order Record before this).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${REVENUE_ORDER_TABLE}    ${code}    ${REVENUE_ORDER_GRID_VERIFY_PROPERTIES}
    ...    ${REVENUE_ORDER_FORM_VERIFY_PROPERTIES}    @{REVENUE_ORDER_FORM_LABELS}

Delete Revenue Order Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date,
    ...    called with ZERO arguments (defaults ${code}/${date} to the suite's
    ...    ${TEST_CODE}/${END_DATE}). Select the revenue order, set End Date = Start Date
    ...    (true delete), Save. Captures the TC05 evidence screenshot right after the End
    ...    Date is filled but BEFORE Save is clicked, matching Bank/State's convention.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Delete Object Via End Date    ${REVENUE_ORDER_TABLE}    ${REVENUE_ORDER_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action

Verify Revenue Order Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code}
    ...    is absent from BOTH the grid and the database.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${REVENUE_ORDER_TABLE}    OV_FIN_REVENUE_ORDER    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Revenue Order Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to
    ...    the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${REVENUE_ORDER_TABLE}    ${code}
