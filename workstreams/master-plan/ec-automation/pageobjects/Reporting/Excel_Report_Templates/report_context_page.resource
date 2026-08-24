*** Settings ***
Documentation       T3 (screen) — Report Context page object.
...                 Screen: Reporting > Excel Report Templates > Report Context (RP.0007).
...                 Custom-URL OV (no navigator/GO at all — reload via toolbar Refresh,
...                 confirmed live 2026-08-24: navigator fields=[], go=[], grid id is
...                 nav:form:T_data, renders directly on open - matches WBS/Calendar/Account/
...                 Cost Centre/Revenue Order, NOT the manage-object
...                 manage_object_nav_nav:form:T_data + GO variant). CLASS_NAME=REPT_CONTEXT
...                 (class_property_cnfg LABEL is "Reporting context", NOT "Report Context" -
...                 the menu/BUSINESS_FUNCTION.NAME - confirmed via direct class_cnfg query by
...                 CLASS_NAME rather than trusting the LABEL lookup). CLASS_TYPE=OBJECT,
...                 TIME_SCOPE_CODE=VERSIONED, base table REPT_CONTEXT, version table
...                 REPT_CONTEXT_VERSION, view OV_REPT_CONTEXT.
...                 Brand-new build 2026-08-24 (no prior automation existed) - built directly
...                 to the label-driven, properties-file-driven, T2-consolidated pattern
...                 matching Bank/WBS/Currency (ec-bank-pattern-new-screen skill).

Library             Browser
Library             ../../../libraries/DbVerify.py
Library             ../../../libraries/PropertiesReader.py
Resource            ../../../resources/common.resource
Resource            ../../../resources/manage_object.resource
Variables           ../../../resources/credentials.py


*** Variables ***
${REPORT_CONTEXT_SCREEN}    Report Context
${REPORT_CONTEXT_INSERT_PROPERTIES}    ${CURDIR}/../../../testdata/report_context_insert.properties
${REPORT_CONTEXT_UPDATE_PROPERTIES}    ${CURDIR}/../../../testdata/report_context_update.properties
${REPORT_CONTEXT_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../testdata/report_context_form_verify.properties
${REPORT_CONTEXT_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../testdata/report_context_grid_verify.properties
# Grid id: Report Context is a custom-URL OV - grid is nav:form:T_data (NOT the manage-object
# manage_object_nav_nav:form:T_data variant) and there is NO navigator/GO button at all
# (navigator fields=[], go=[] - confirmed live 2026-08-24). T2's Save And Refresh List
# auto-detects this (falls back to toolbar Refresh) - matches WBS/Calendar/Account/Cost
# Centre/Revenue Order.
${REPORT_CONTEXT_TABLE}    nav:form:T_data
# objectdates field ID (Delete — End Date = Start Date), matching Bank/WBS's convention -
# framework-invariant objectdates layout (R:0:C:1 = Start Date, R:0:C:3 = End Date).
${REPORT_CONTEXT_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Report Context's own form-field label set. Labels are plain "Code"/"Name" (NOT
# screen-prefixed) - confirmed live 2026-08-24 via both the New Object form (objectForm) and
# the row-select form (updateAttributes) label dumps, same convention as Bank/WBS/Currency.
# Start Date deliberately excluded - Insert-only, not present in updateAttributes. The
# objectForm also has End Date/Description/Comments - all confirmed optional (not
# mandatory-yellow) live and deliberately omitted (IUD-fill-only-needed-fields convention).
@{REPORT_CONTEXT_FORM_LABELS}    Code    Name


*** Keywords ***
Find Report Context Row By Filter
    [Documentation]    Explicitly filter the Report Context grid's Code column to ${code} via
    ...    the shared T2 Find Object Row By Filter (resources/manage_object.resource) -
    ...    matches Account/Bank/WBS/Currency's explicit filter usage, rather than relying only
    ...    on Select Object Row's implicit 3s-timeout fallback.
    [Arguments]    ${code}
    Find Object Row By Filter    ${REPORT_CONTEXT_TABLE}    ${code}

Clear Report Context Row Filter
    [Documentation]    Clear the Code column filter (see Find Report Context Row By Filter)
    ...    via the shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered
    ...    view.
    Clear Object Row Filter    ${REPORT_CONTEXT_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Report Context's OWN credentials
    ...    (${REPORT_CONTEXT_EC_USER}/${REPORT_CONTEXT_EC_PASS} from credentials.py) on the
    ...    current page. Standing decision: every EC screen gets its own dedicated credential
    ...    pair. Zero-argument wrapper so report_context_iud.robot's test cases read as a
    ...    plain business step; supplies Report Context's own credential defaults to the
    ...    shared T1 Login To EC Screen (common.resource), which owns the actual login
    ...    mechanics.
    Login To EC Screen    ${REPORT_CONTEXT_EC_USER}    ${REPORT_CONTEXT_EC_PASS}

Open Report Context Screen
    [Documentation]    Navigate to the Report Context screen. Assumes the caller already
    ...    logged in this test case (via Login To EC Application) - this keyword ONLY
    ...    navigates. Delegates to the shared T1 Open EC Screen (common.resource) for the
    ...    actual mechanics. Deliberately does NOT click any GO button or call Apply
    ...    Navigator - live scan 2026-08-24 confirmed this screen has NO navigator at all
    ...    (fields=[], go=[]); the grid (nav:form:T_data) renders directly on open, same as
    ...    WBS/Calendar/Account/Cost Centre/Revenue Order.
    Open EC Screen    ${REPORT_CONTEXT_SCREEN}

Insert Report Context Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties
    ...    And Verify Code, so report_context_iud.robot's test case body reads as a plain
    ...    business step with ZERO arguments. Also checks the inserted Code matches the
    ...    suite's ${TEST_CODE}. Pre-save evidence screenshot captured before Save is clicked,
    ...    matching Bank/WBS.
    [Arguments]    ${properties_path}=${REPORT_CONTEXT_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action
    RETURN    ${code}

Verify Report Context Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (no DB check here, matching Bank/WBS's TC02 convention): row exists
    ...    in the grid, then the form shows what was just inserted (Code/Name only - Start
    ...    Date is grid/insert-only, not present in updateAttributes). Delegates the full
    ...    sequence (row-check, select, form-compare, screenshot) to the shared T2 Verify
    ...    Object Insert Exists. Filters via Find Report Context Row By Filter first, clears
    ...    after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Report Context Row By Filter    ${code}
    Verify Object Insert Exists    ${REPORT_CONTEXT_TABLE}    ${code}    Report Context
    ...    ${REPORT_CONTEXT_INSERT_PROPERTIES}    @{REPORT_CONTEXT_FORM_LABELS}
    Clear Report Context Row Filter

Update Report Context Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Pre-save evidence screenshot captured before Save is clicked, matching Bank/WBS.
    ...    Filters via Find Report Context Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${REPORT_CONTEXT_UPDATE_PROPERTIES}
    Find Report Context Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${REPORT_CONTEXT_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action
    Clear Report Context Row Filter
    RETURN    ${data}

Verify Report Context Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification, matching Bank/WBS's TC03 convention: the form shows the updated Name.
    ...    Delegates the full sequence (select, form-compare, screenshot) to the shared T2
    ...    Verify Object Form Record. Filters via Find Report Context Row By Filter first,
    ...    clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Report Context Row By Filter    ${code}
    Verify Object Form Record    ${REPORT_CONTEXT_TABLE}    ${code}    Report Context
    ...    ${REPORT_CONTEXT_UPDATE_PROPERTIES}    Name
    Clear Report Context Row Filter

Find Report Context Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Delegates the full select+capture sequence. Calls Find Report Context Row By
    ...    Filter first. Deliberately does NOT clear the filter afterward - Verify Report
    ...    Context Record Found (called right after, same TC) needs the grid still filtered
    ...    to ${code} for its own grid-check, since it doesn't re-select the row itself; it
    ...    clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Report Context Row By Filter    ${code}
    Find Object Record    ${REPORT_CONTEXT_TABLE}    ${code}    Report Context

Verify Report Context Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the form record match the expected (post-update) data. Delegates the full
    ...    sequence (grid-compare, form-compare, screenshot) to the shared T2 Verify Object
    ...    Found. Caller must already have selected the row (TC04 does, via Find Report
    ...    Context Record before this) AND left the Code filter active from that same call -
    ...    clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${REPORT_CONTEXT_TABLE}    ${code}    ${REPORT_CONTEXT_GRID_VERIFY_PROPERTIES}
    ...    ${REPORT_CONTEXT_FORM_VERIFY_PROPERTIES}    @{REPORT_CONTEXT_FORM_LABELS}
    Clear Report Context Row Filter

Delete Report Context Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date,
    ...    called with ZERO arguments (defaults ${code}/${date} to the suite's
    ...    ${TEST_CODE}/${END_DATE}). Select the report context, set End Date = Start Date
    ...    (true delete), Save. Captures the TC05 evidence screenshot right after the End
    ...    Date is filled but BEFORE Save is clicked, matching Bank/WBS's convention. Filters
    ...    via Find Report Context Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Report Context Row By Filter    ${code}
    Delete Object Via End Date    ${REPORT_CONTEXT_TABLE}    ${REPORT_CONTEXT_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Report Context Row Filter

Verify Report Context Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is
    ...    absent from BOTH the grid and the database.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${REPORT_CONTEXT_TABLE}    OV_REPT_CONTEXT    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Report Context Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to
    ...    the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${REPORT_CONTEXT_TABLE}    ${code}
