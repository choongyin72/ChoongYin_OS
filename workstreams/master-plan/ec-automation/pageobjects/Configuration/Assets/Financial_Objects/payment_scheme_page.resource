*** Settings ***
Documentation       T3 (screen) — Payment Scheme page object.
...                 Screen: Configuration > Assets > Financial Objects > Payment Scheme.
...                 Manage-Object (OV) screen. Holds Payment Scheme's locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common).
...                 Rebuilt 2026-08-22 to mirror Bank/State/Object List exactly (owner:
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
${PAYMENT_SCHEME_SCREEN}         Payment Scheme
${PAYMENT_SCHEME_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/payment_scheme_insert.properties
${PAYMENT_SCHEME_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/payment_scheme_update.properties
${PAYMENT_SCHEME_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/payment_scheme_form_verify.properties
${PAYMENT_SCHEME_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/payment_scheme_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal.
${PAYMENT_SCHEME_TABLE}          ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date), matching Bank/State's convention.
${PAYMENT_SCHEME_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Payment Scheme's own form-field label set. Labels are the generic "Code"/"Name" (NOT
# screen-prefixed like State's "State Code"/"State Name") - confirmed live 2026-08-22 via the
# New Object form field dump (objectForm: Code, Name, Start Date, End Date, Comments,
# Description - only Code/Name/Start Date carry the mandatory yellow background). Start Date
# deliberately excluded here - Insert-only, not present in updateAttributes. Defined ONCE here
# so both Verify Payment Scheme Record Exists (TC02) and Verify Payment Scheme Record Found
# (TC04) share the same list.
@{PAYMENT_SCHEME_FORM_LABELS}    Code    Name


*** Keywords ***
Login To EC Application
    [Documentation]    Authenticate as Payment Scheme's OWN credentials
    ...    (${PAYMENT_SCHEME_EC_USER}/${PAYMENT_SCHEME_EC_PASS} from credentials.py) on the
    ...    current page. Standing decision (owner, 2026-08-22): every EC screen gets its own
    ...    dedicated credential pair. Zero-argument wrapper so payment_scheme_iud.robot's test
    ...    cases read as a plain business step; supplies Payment Scheme's own credential
    ...    defaults to the shared T1 Login To EC Screen (common.resource), which owns the
    ...    actual login mechanics.
    Login To EC Screen    ${PAYMENT_SCHEME_EC_USER}    ${PAYMENT_SCHEME_EC_PASS}

Open Payment Scheme Screen
    [Documentation]    Navigate to the Payment Scheme screen. Assumes the caller already
    ...    logged in this test case (via Login To EC Application) - this keyword ONLY
    ...    navigates. Delegates to the shared T1 Open EC Screen (common.resource) for the
    ...    actual mechanics.
    Open EC Screen    ${PAYMENT_SCHEME_SCREEN}

Insert Payment Scheme Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties
    ...    And Verify Code, so payment_scheme_iud.robot's test case body reads as a plain
    ...    business step with ZERO arguments. Also checks the inserted Code matches the
    ...    suite's ${TEST_CODE}. Pre-save evidence screenshot captured before Save is clicked,
    ...    matching Bank/State.
    [Arguments]    ${properties_path}=${PAYMENT_SCHEME_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Code
    RETURN    ${code}

Verify Payment Scheme Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (no DB check here, matching Bank/State's TC02 convention): row exists
    ...    in the grid, then the form shows what was just inserted (Code/Name only - Start
    ...    Date is grid/insert-only, not present in updateAttributes). Delegates the full
    ...    sequence (row-check, select, form-compare, screenshot) to the shared T2 Verify
    ...    Object Insert Exists.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Insert Exists    ${PAYMENT_SCHEME_TABLE}    ${code}    Payment Scheme
    ...    ${PAYMENT_SCHEME_INSERT_PROPERTIES}    @{PAYMENT_SCHEME_FORM_LABELS}    code_label=Code

Update Payment Scheme Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Pre-save evidence screenshot captured before Save is clicked, matching Bank/State.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${PAYMENT_SCHEME_UPDATE_PROPERTIES}
    ${data}=    Update Object From Properties    ${PAYMENT_SCHEME_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Code
    RETURN    ${data}

Verify Payment Scheme Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification, matching Bank/State's TC03 convention: the form shows the updated
    ...    Name. Delegates the full sequence (select, form-compare, screenshot) to the shared
    ...    T2 Verify Object Form Record.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Form Record    ${PAYMENT_SCHEME_TABLE}    ${code}    Payment Scheme
    ...    ${PAYMENT_SCHEME_UPDATE_PROPERTIES}    Name    code_label=Code

Find Payment Scheme Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Delegates the full select+capture sequence.
    [Arguments]    ${code}=${TEST_CODE}
    Find Object Record    ${PAYMENT_SCHEME_TABLE}    ${code}    Payment Scheme    code_label=Code

Verify Payment Scheme Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the form record match the expected (post-update) data. Delegates the full
    ...    sequence (grid-compare, form-compare, screenshot) to the shared T2 Verify Object
    ...    Found. Caller must already have selected the row (TC04 does, via Find Payment
    ...    Scheme Record before this).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${PAYMENT_SCHEME_TABLE}    ${code}    ${PAYMENT_SCHEME_GRID_VERIFY_PROPERTIES}
    ...    ${PAYMENT_SCHEME_FORM_VERIFY_PROPERTIES}    @{PAYMENT_SCHEME_FORM_LABELS}

Delete Payment Scheme Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date,
    ...    called with ZERO arguments (defaults ${code}/${date} to the suite's
    ...    ${TEST_CODE}/${END_DATE}). Select the payment scheme, set End Date = Start Date
    ...    (true delete), Save. Captures the TC05 evidence screenshot right after the End
    ...    Date is filled but BEFORE Save is clicked, matching Bank/State's convention.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Delete Object Via End Date    ${PAYMENT_SCHEME_TABLE}    ${PAYMENT_SCHEME_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action

Verify Payment Scheme Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is
    ...    absent from BOTH the grid and the database.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${PAYMENT_SCHEME_TABLE}    OV_PAYMENT_SCHEME    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Payment Scheme Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to
    ...    the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${PAYMENT_SCHEME_TABLE}    ${code}
