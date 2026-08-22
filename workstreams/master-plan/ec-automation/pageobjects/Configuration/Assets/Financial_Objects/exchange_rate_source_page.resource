*** Settings ***
Documentation       T3 (screen) — Exchange Rate Source page object.
...                 Screen: Configuration > Assets > Financial Objects > Exchange Rate Source.
...                 Manage-Object (OV) screen. Holds Exchange Rate Source's locators + thin
...                 IUD wrappers that delegate to T2 (manage_object) and T1 (common).
...                 Rebuilt 2026-08-22 to mirror Bank/State exactly (owner: "reflect the
...                 current EC screen exactly the same way as the OV_BANK IUD related task") -
...                 replaces the older hardcoded-field-id/no-properties-file pattern with the
...                 label-driven, properties-file-driven, T2-consolidated pattern.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${EXCHANGE_RATE_SOURCE_SCREEN}    Exchange Rate Source
${EXCHANGE_RATE_SOURCE_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/exchange_rate_source_insert.properties
${EXCHANGE_RATE_SOURCE_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/exchange_rate_source_update.properties
${EXCHANGE_RATE_SOURCE_FORM_VERIFY}    ${CURDIR}/../../../../testdata/exchange_rate_source_form_verify.properties
${EXCHANGE_RATE_SOURCE_GRID_VERIFY}    ${CURDIR}/../../../../testdata/exchange_rate_source_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal.
${EXCHANGE_RATE_SOURCE_TABLE}    ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date), matching Bank/State's convention.
${EXCHANGE_RATE_SOURCE_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Exchange Rate Source's own form-field label set. Labels are the GENERIC "Code"/"Name" (NOT
# screen-prefixed like State's "State Code"/"State Name") - confirmed live 2026-08-22 via the
# New Object form outerHTML dump AND a read-only scan of updateAttributes on the real existing
# row ECB (select only, no edits/Save). Start Date deliberately excluded - Insert-only, not
# present in updateAttributes. Defined ONCE here so both Verify Exchange Rate Source Record
# Exists (TC02) and Verify Exchange Rate Source Record Found (TC04) share the same list.
@{EXCHANGE_RATE_SOURCE_FORM_LABELS}    Code    Name


*** Keywords ***
Find Exchange Rate Source Row By Filter
    [Documentation]    Explicitly filter the Exchange Rate Source grid's Code column to ${code}
    ...    via the shared T2 Find Object Row By Filter (resources/manage_object.resource) -
    ...    matches Account/Bank/State/Object List's explicit filter usage (owner, 2026-08-22:
    ...    "same to other ec screens"), rather than relying only on Select Object Row's
    ...    implicit 3s-timeout fallback.
    [Arguments]    ${code}
    Find Object Row By Filter    ${EXCHANGE_RATE_SOURCE_TABLE}    ${code}

Clear Exchange Rate Source Row Filter
    [Documentation]    Clear the Code column filter (see Find Exchange Rate Source Row By
    ...    Filter) via the shared T2 Clear Object Row Filter, restoring the grid's normal
    ...    unfiltered view.
    Clear Object Row Filter    ${EXCHANGE_RATE_SOURCE_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Exchange Rate Source's OWN credentials
    ...    (${EXCHANGE_RATE_SOURCE_EC_USER}/${EXCHANGE_RATE_SOURCE_EC_PASS} from
    ...    credentials.py) on the current page. Standing decision (owner, 2026-08-22): every
    ...    EC screen gets its own dedicated credential pair. Zero-argument wrapper so
    ...    exchange_rate_source_iud.robot's test cases read as a plain business step; supplies
    ...    Exchange Rate Source's own credential defaults to the shared T1 Login To EC Screen
    ...    (common.resource), which owns the actual login mechanics.
    Login To EC Screen    ${EXCHANGE_RATE_SOURCE_EC_USER}    ${EXCHANGE_RATE_SOURCE_EC_PASS}

Open Exchange Rate Source Screen
    [Documentation]    Navigate to the Exchange Rate Source screen. Assumes the caller already
    ...    logged in this test case (via Login To EC Application) - this keyword ONLY
    ...    navigates. Delegates to the shared T1 Open EC Screen (common.resource) for the
    ...    actual mechanics.
    Open EC Screen    ${EXCHANGE_RATE_SOURCE_SCREEN}

Insert Exchange Rate Source Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties
    ...    And Verify Code, so exchange_rate_source_iud.robot's test case body reads as a
    ...    plain business step with ZERO arguments. Also checks the inserted Code matches the
    ...    suite's ${TEST_CODE}. Pre-save evidence screenshot captured before Save is clicked,
    ...    matching Bank/State.
    [Arguments]    ${properties_path}=${EXCHANGE_RATE_SOURCE_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Code
    RETURN    ${code}

Verify Exchange Rate Source Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (no DB check here, matching Bank/State's TC02 convention): row exists
    ...    in the grid, then the form shows what was just inserted (Code/Name only - Start
    ...    Date is grid/insert-only, not present in updateAttributes). Delegates the full
    ...    sequence (row-check, select, form-compare, screenshot) to the shared T2 Verify
    ...    Object Insert Exists.
    ...    Filters via Find Exchange Rate Source Row By Filter first, clears after (2026-08-22
    ...    standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find Exchange Rate Source Row By Filter    ${code}
    Verify Object Insert Exists    ${EXCHANGE_RATE_SOURCE_TABLE}    ${code}    Exchange Rate Source
    ...    ${EXCHANGE_RATE_SOURCE_INSERT_PROPERTIES}    @{EXCHANGE_RATE_SOURCE_FORM_LABELS}    code_label=Code
    Clear Exchange Rate Source Row Filter

Update Exchange Rate Source Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Pre-save evidence screenshot captured before Save is clicked, matching Bank/State.
    ...    Filters via Find Exchange Rate Source Row By Filter first, clears after
    ...    (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${EXCHANGE_RATE_SOURCE_UPDATE_PROPERTIES}
    Find Exchange Rate Source Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${EXCHANGE_RATE_SOURCE_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Code
    Clear Exchange Rate Source Row Filter
    RETURN    ${data}

Verify Exchange Rate Source Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification, matching Bank/State's TC03 convention: the form shows the updated
    ...    Name. Delegates the full sequence (select, form-compare, screenshot) to the shared
    ...    T2 Verify Object Form Record. Filters via Find Exchange Rate Source Row By Filter
    ...    first, clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find Exchange Rate Source Row By Filter    ${code}
    Verify Object Form Record    ${EXCHANGE_RATE_SOURCE_TABLE}    ${code}    Exchange Rate Source
    ...    ${EXCHANGE_RATE_SOURCE_UPDATE_PROPERTIES}    Name    code_label=Code
    Clear Exchange Rate Source Row Filter

Find Exchange Rate Source Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Delegates the full select+capture sequence. Calls Find Exchange Rate Source Row By
    ...    Filter first (2026-08-22 standardisation). Deliberately does NOT clear the filter
    ...    afterward - Verify Exchange Rate Source Record Found (called right after, same TC)
    ...    needs the grid still filtered to ${code} for its own grid-check, since it doesn't
    ...    re-select the row itself; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Exchange Rate Source Row By Filter    ${code}
    Find Object Record    ${EXCHANGE_RATE_SOURCE_TABLE}    ${code}    Exchange Rate Source    code_label=Code

Verify Exchange Rate Source Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the form record match the expected (post-update) data. Delegates the full
    ...    sequence (grid-compare, form-compare, screenshot) to the shared T2 Verify Object
    ...    Found. Caller must already have selected the row (TC04 does, via Find Exchange
    ...    Rate Source Record before this) AND left the Code filter active from that same
    ...    call - clears the filter itself once both checks are done (2026-08-22
    ...    standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${EXCHANGE_RATE_SOURCE_TABLE}    ${code}    ${EXCHANGE_RATE_SOURCE_GRID_VERIFY}
    ...    ${EXCHANGE_RATE_SOURCE_FORM_VERIFY}    @{EXCHANGE_RATE_SOURCE_FORM_LABELS}
    Clear Exchange Rate Source Row Filter

Delete Exchange Rate Source Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date,
    ...    called with ZERO arguments (defaults ${code}/${date} to the suite's
    ...    ${TEST_CODE}/${END_DATE}). Select the exchange rate source, set End Date = Start
    ...    Date (true delete), Save. Captures the TC05 evidence screenshot right after the End
    ...    Date is filled but BEFORE Save is clicked, matching Bank/State's convention.
    ...    Filters via Find Exchange Rate Source Row By Filter first, clears after
    ...    (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Exchange Rate Source Row By Filter    ${code}
    Delete Object Via End Date    ${EXCHANGE_RATE_SOURCE_TABLE}    ${EXCHANGE_RATE_SOURCE_DEL_ENDDATE}
    ...    ${code}    ${date}    ${TEST NAME}_action
    Clear Exchange Rate Source Row Filter

Verify Exchange Rate Source Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is
    ...    absent from BOTH the grid and the database.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${EXCHANGE_RATE_SOURCE_TABLE}    OV_FOREX_SOURCE    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Exchange Rate Source Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to
    ...    the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${EXCHANGE_RATE_SOURCE_TABLE}    ${code}
