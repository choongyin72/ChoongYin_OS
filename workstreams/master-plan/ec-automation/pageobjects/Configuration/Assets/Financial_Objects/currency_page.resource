*** Settings ***
Documentation       T3 (screen) — Currency page object.
...                 Screen: Configuration > Assets > Financial Objects > Currency.
...                 Manage-Object (OV) screen (grid manage_object_nav_nav:form:T_data,
...                 standard navigator GO button, no mandatory nav dropdown/date - confirmed
...                 already in docs/ec_screen_registry.md, not re-verified here). Holds
...                 Currency's locators + thin IUD wrappers that delegate to T2
...                 (manage_object) and T1 (common).
...                 Rebuilt 2026-08-23 to mirror Bank/Cost Centre exactly - replaces the
...                 older hardcoded-field-id pattern with the label-driven,
...                 properties-file-driven, T2-consolidated pattern (batch-2 5-screen
...                 conversion: Country/County/Regulatory Permits/Currency/VAT Code).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${CURRENCY_SCREEN}    Currency
${CURRENCY_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/currency_insert.properties
${CURRENCY_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/currency_update.properties
${CURRENCY_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/currency_form_verify.properties
${CURRENCY_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/currency_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal string
# (manage_object.resource defines this ONCE specifically so no T3 duplicates it). Confirmed
# live 2026-08-23 (this IS a manage-object nav screen, per the registry).
${CURRENCY_TABLE}       ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date), matching Bank/Cost Centre's
# convention - the framework-invariant objectdates layout. Live-verified 2026-08-23: a full
# Insert -> Delete Via End Date -> DB-absence round trip on AUTOTEST_CURRENCY passed using
# this exact id (tmp/recon_currency_cleanup.robot, deleted before commit).
${CURRENCY_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Currency's own form-field label set: "Code"/"Name" (generic, NOT screen-prefixed) -
# confirmed live 2026-08-23 via both the New Object form (objectForm) and the row-select
# form (updateAttributes) label dumps - same convention as Bank/Cost Centre/Object List.
# Start Date deliberately excluded - Insert-only, not present in updateAttributes.
# The objectForm also has Description/Comments/Active (checkbox)/"1/100 Units" - all
# confirmed optional/non-save-blocking live (see currency_insert.properties comment for the
# Active-checkbox finding) and deliberately omitted (IUD-fill-only-needed-fields convention).
@{CURRENCY_FORM_LABELS}    Code    Name


*** Keywords ***
Find Currency Row By Filter
    [Documentation]    Explicitly filter the Currency grid's Code column to ${code} via the
    ...    shared T2 Find Object Row By Filter (resources/manage_object.resource) - matches
    ...    Account/Bank/State/Cost Centre/Object List's explicit filter usage, rather than
    ...    relying only on Select Object Row's implicit 3s-timeout fallback.
    [Arguments]    ${code}
    Find Object Row By Filter    ${CURRENCY_TABLE}    ${code}

Clear Currency Row Filter
    [Documentation]    Clear the Code column filter (see Find Currency Row By Filter) via the
    ...    shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${CURRENCY_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Currency's OWN credentials (${CURRENCY_EC_USER}/
    ...    ${CURRENCY_EC_PASS} from credentials.py) on the current page. Standing decision:
    ...    every EC screen gets its own dedicated credential pair. Zero-argument wrapper so
    ...    currency_iud.robot's test cases read as a plain business step; supplies
    ...    Currency's own credential defaults to the shared T1 Login To EC Screen
    ...    (common.resource), which owns the actual login mechanics.
    Login To EC Screen    ${CURRENCY_EC_USER}    ${CURRENCY_EC_PASS}

Open Currency Screen
    [Documentation]    Navigate to the Currency screen. Assumes the caller already logged in
    ...    this test case (via Login To EC Application) - this keyword ONLY navigates.
    ...    Delegates to the shared T1 Open EC Screen (common.resource) for the actual
    ...    mechanics.
    Open EC Screen    ${CURRENCY_SCREEN}

Insert Currency Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties
    ...    And Verify Code, so currency_iud.robot's test case body reads as a plain business
    ...    step with ZERO arguments. Also checks the inserted Code matches the suite's
    ...    ${TEST_CODE}. Pre-save evidence screenshot captured before Save is clicked,
    ...    matching Bank/Cost Centre.
    [Arguments]    ${properties_path}=${CURRENCY_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action
    RETURN    ${code}

Verify Currency Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (no DB check here, matching Bank/Cost Centre's TC02 convention): row
    ...    exists in the grid, then the form shows what was just inserted (Code/Name only -
    ...    Start Date is grid/insert-only, not present in updateAttributes). Delegates the
    ...    full sequence (row-check, select, form-compare, screenshot) to the shared T2
    ...    Verify Object Insert Exists. Filters via Find Currency Row By Filter first, clears
    ...    after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Currency Row By Filter    ${code}
    Verify Object Insert Exists    ${CURRENCY_TABLE}    ${code}    Currency    ${CURRENCY_INSERT_PROPERTIES}
    ...    @{CURRENCY_FORM_LABELS}
    Clear Currency Row Filter

Update Currency Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Pre-save evidence screenshot captured before Save is clicked, matching Bank/Cost
    ...    Centre. Filters via Find Currency Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${CURRENCY_UPDATE_PROPERTIES}
    Find Currency Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${CURRENCY_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action
    Clear Currency Row Filter
    RETURN    ${data}

Verify Currency Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification, matching Bank/Cost Centre's TC03 convention: the form shows the
    ...    updated Name. Delegates the full sequence (select, form-compare, screenshot) to
    ...    the shared T2 Verify Object Form Record. Filters via Find Currency Row By Filter
    ...    first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Currency Row By Filter    ${code}
    Verify Object Form Record    ${CURRENCY_TABLE}    ${code}    Currency    ${CURRENCY_UPDATE_PROPERTIES}
    ...    Name
    Clear Currency Row Filter

Find Currency Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Delegates the full select+capture sequence. Calls Find Currency Row By Filter
    ...    first. Deliberately does NOT clear the filter afterward - Verify Currency Record
    ...    Found (called right after, same TC) needs the grid still filtered to ${code} for
    ...    its own grid-check, since it doesn't re-select the row itself; it clears the
    ...    filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Currency Row By Filter    ${code}
    Find Object Record    ${CURRENCY_TABLE}    ${code}    Currency

Verify Currency Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the form record match the expected (post-update) data. Delegates the full
    ...    sequence (grid-compare, form-compare, screenshot) to the shared T2 Verify Object
    ...    Found. Caller must already have selected the row (TC04 does, via Find Currency
    ...    Record before this) AND left the Code filter active from that same call - clears
    ...    the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${CURRENCY_TABLE}    ${code}    ${CURRENCY_GRID_VERIFY_PROPERTIES}
    ...    ${CURRENCY_FORM_VERIFY_PROPERTIES}    @{CURRENCY_FORM_LABELS}
    Clear Currency Row Filter

Delete Currency Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date,
    ...    called with ZERO arguments (defaults ${code}/${date} to the suite's
    ...    ${TEST_CODE}/${END_DATE}). Select the currency, set End Date = Start Date (true
    ...    delete), Save. Captures the TC05 evidence screenshot right after the End Date is
    ...    filled but BEFORE Save is clicked, matching Bank/Cost Centre's convention. Filters
    ...    via Find Currency Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Currency Row By Filter    ${code}
    Delete Object Via End Date    ${CURRENCY_TABLE}    ${CURRENCY_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Currency Row Filter

Verify Currency Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is
    ...    absent from BOTH the grid and the database.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${CURRENCY_TABLE}    OV_CURRENCY    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Currency Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to
    ...    the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${CURRENCY_TABLE}    ${code}
