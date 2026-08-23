*** Settings ***
Documentation       T3 (screen) — Country page object.
...                 Screen: Configuration > Assets > Basic Objects > Country.
...                 Manage-Object (OV) screen. Holds Country's locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common).
...                 Rebuilt 2026-08-23 to mirror Bank/State/Object List exactly (Batch 2
...                 plain-OV Bank-pattern conversion) - replaces the older hardcoded-field-id
...                 pattern (per-screen bespoke Insert/Update/Delete keywords, no
...                 properties-file-driven insert) with the label-driven, properties-file-
...                 driven, T2-consolidated pattern.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${COUNTRY_SCREEN}          Country
${COUNTRY_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/country_insert.properties
${COUNTRY_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/country_update.properties
${COUNTRY_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/country_form_verify.properties
${COUNTRY_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/country_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal
# string (manage_object.resource defines this ONCE specifically so no T3 duplicates it).
# Confirmed live 2026-08-23 (manage_object_nav_nav:form:T_data, plain manage-object OV, no
# mandatory nav dropdown/date before GO) - matches the batch's pre-confirmed navigator shape.
${COUNTRY_TABLE}        ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date), matching Bank/State/Account's
# already-proven, framework-invariant row layout (Start Date C:1, End Date label C:2, End
# Date input C:3) - not independently re-verified here per the batch's ground rules.
${COUNTRY_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Country's own form-field label set. Labels are "Country Code"/"Country Name"
# (screen-prefixed) - confirmed live 2026-08-23 via a field-label recon script dumping every
# ECCell label in both objectForm (Insert, 14 labels) and updateAttributes (Update, 10
# labels): Country Code, Country Name, Master System Code, Master System Name, Local Name,
# Start Date/End Date (objectdates-only, Insert form shows them inline but they are NOT part
# of updateAttributes), Dialing Code, Comments, Description, Nationality name. Only Code/Name
# are MandatoryCellStyle-confirmed mandatory besides Start Date (Insert-only) - IUD-fill-
# only-needed-fields convention, so @{COUNTRY_FORM_LABELS} deliberately lists only the
# mandatory, always-present pair (Start Date excluded - Insert-only, not in updateAttributes,
# same as Bank/State).
@{COUNTRY_FORM_LABELS}    Country Code    Country Name


*** Keywords ***
Find Country Row By Filter
    [Documentation]    Explicitly filter the Country grid's Code column to ${code} via the
    ...    shared T2 Find Object Row By Filter (resources/manage_object.resource) - matches
    ...    Account/Bank/State's own explicit filter usage (owner, 2026-08-22: "others (Bank,
    ...    State, List_Object) should follow Account... utilise same filter feature"), rather
    ...    than relying only on Select Object Row's implicit 3s-timeout fallback.
    [Arguments]    ${code}
    Find Object Row By Filter    ${COUNTRY_TABLE}    ${code}

Clear Country Row Filter
    [Documentation]    Clear the Code column filter (see Find Country Row By Filter) via the
    ...    shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${COUNTRY_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Country's OWN credentials (${COUNTRY_EC_USER}/
    ...    ${COUNTRY_EC_PASS} from credentials.py) on the current page. Standing decision
    ...    (owner, 2026-08-22): every EC screen gets its own dedicated credential pair.
    ...    Zero-argument wrapper so country_iud.robot's test cases read as a plain business
    ...    step; supplies Country's own credential defaults to the shared T1 Login To EC
    ...    Screen (common.resource), which owns the actual login mechanics.
    Login To EC Screen    ${COUNTRY_EC_USER}    ${COUNTRY_EC_PASS}

Open Country Screen
    [Documentation]    Navigate to the Country screen. Assumes the caller already logged in
    ...    this test case (via Login To EC Application) - this keyword ONLY navigates.
    ...    Delegates to the shared T1 Open EC Screen (common.resource) for the actual mechanics.
    Open EC Screen    ${COUNTRY_SCREEN}

Insert Country Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties
    ...    And Verify Code, so country_iud.robot's test case body reads as a plain business
    ...    step with ZERO arguments. Also checks the inserted Code matches the suite's
    ...    ${TEST_CODE}. Pre-save evidence screenshot captured before Save is clicked,
    ...    matching Bank/State.
    [Arguments]    ${properties_path}=${COUNTRY_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Country Code
    RETURN    ${code}

Verify Country Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (no DB check here, matching Bank/State's TC02 convention): row exists
    ...    in the grid, then the form shows what was just inserted (Country Code/Country Name
    ...    only - Start Date is grid/insert-only, not present in updateAttributes).
    ...    Delegates the full sequence (row-check, select, form-compare, screenshot) to the
    ...    shared T2 Verify Object Insert Exists. Filters via Find Country Row By Filter
    ...    first, clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find Country Row By Filter    ${code}
    Verify Object Insert Exists    ${COUNTRY_TABLE}    ${code}    Country    ${COUNTRY_INSERT_PROPERTIES}
    ...    @{COUNTRY_FORM_LABELS}    code_label=Country Code
    Clear Country Row Filter

Update Country Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Pre-save evidence screenshot captured before Save is clicked, matching Bank/State.
    ...    Filters via Find Country Row By Filter first, clears after (2026-08-22
    ...    standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${COUNTRY_UPDATE_PROPERTIES}
    Find Country Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${COUNTRY_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Country Code
    Clear Country Row Filter
    RETURN    ${data}

Verify Country Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification, matching Bank/State's TC03 convention: the form shows the updated
    ...    Country Name. Delegates the full sequence (select, form-compare, screenshot) to
    ...    the shared T2 Verify Object Form Record. Filters via Find Country Row By Filter
    ...    first, clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find Country Row By Filter    ${code}
    Verify Object Form Record    ${COUNTRY_TABLE}    ${code}    Country    ${COUNTRY_UPDATE_PROPERTIES}
    ...    Country Name    code_label=Country Code
    Clear Country Row Filter

Find Country Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Delegates the full select+capture sequence. Calls Find Country Row By Filter first
    ...    (2026-08-22 standardisation). Deliberately does NOT clear the filter afterward -
    ...    Verify Country Record Found (called right after, same TC) needs the grid still
    ...    filtered to ${code} for its own grid-check, since it doesn't re-select the row
    ...    itself; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Country Row By Filter    ${code}
    Find Object Record    ${COUNTRY_TABLE}    ${code}    Country    code_label=Country Code

Verify Country Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the form record match the expected (post-update) data. Delegates the
    ...    full sequence (grid-compare, form-compare, screenshot) to the shared T2 Verify
    ...    Object Found. Caller must already have selected the row (TC04 does, via Find
    ...    Country Record before this) AND left the Code filter active from that same call -
    ...    clears the filter itself once both checks are done (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${COUNTRY_TABLE}    ${code}    ${COUNTRY_GRID_VERIFY_PROPERTIES}
    ...    ${COUNTRY_FORM_VERIFY_PROPERTIES}    @{COUNTRY_FORM_LABELS}
    Clear Country Row Filter

Delete Country Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date,
    ...    called with ZERO arguments (defaults ${code}/${date} to the suite's
    ...    ${TEST_CODE}/${END_DATE}). Select the country, set End Date = Start Date (true
    ...    delete), Save. Captures the TC05 evidence screenshot right after the End Date is
    ...    filled but BEFORE Save is clicked, matching Bank/State's convention. Filters via
    ...    Find Country Row By Filter first, clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Country Row By Filter    ${code}
    Delete Object Via End Date    ${COUNTRY_TABLE}    ${COUNTRY_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Country Row Filter

Verify Country Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code}
    ...    is absent from BOTH the grid and the database (OV_COUNTRY).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${COUNTRY_TABLE}    OV_COUNTRY    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Country Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to
    ...    the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${COUNTRY_TABLE}    ${code}
