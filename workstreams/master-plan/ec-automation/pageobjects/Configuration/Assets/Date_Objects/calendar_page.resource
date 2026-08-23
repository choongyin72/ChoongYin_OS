*** Settings ***
Documentation       T3 (screen) — Calendar page object.
...                 Screen: Configuration > Assets > Date Objects > Calendar (CD.0024).
...                 Manage-Object (OV, date-effective), CUSTOM-URL variant (grid
...                 `nav:form:T_data`, NO navigator/GO button - confirmed live 2026-08-23,
...                 matching the registry's prior note; T2's Save And Refresh List already
...                 falls back to the toolbar Refresh automatically when no GO exists, so no
...                 T3-local workaround is needed). Rebuilt 2026-08-23 (Batch 6 Bank-pattern
...                 conversion, final batch) from the older hardcoded-field-id pattern to the
...                 label-driven, properties-file-driven, T2-consolidated pattern (mirrors
...                 bank_page.resource / royalty_owner_page.resource).
...                 OUT OF SCOPE: the related "Member Calendars"/"Calendar Usage" child grid
...                 (per docs/ec_screen_registry.md's existing entry) - this page object only
...                 covers the plain Code/Name/Start Date IUD flow on the CALENDAR tab.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${CALENDAR_SCREEN}         Calendar
${CALENDAR_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/calendar_insert.properties
${CALENDAR_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/calendar_update.properties
${CALENDAR_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/calendar_form_verify.properties
${CALENDAR_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/calendar_grid_verify.properties
# Calendar is a custom-URL OV: grid is nav:form:T_data, NOT the standard
# manage_object_nav_nav:form:T_data manage-object shape - confirmed live 2026-08-23 (no
# navigator/GO button on this screen at all).
${CALENDAR_TABLE}          nav:form:T_data
# objectdates field ID (Delete — End Date = Start Date). Confirmed live 2026-08-23: the
# objectdates sub-form exists in the DOM (tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input)
# with the same R:0:C:1 Start Date / C:2 End-Date-label / C:3 End-Date-input shape as
# Bank/Royalty Owner, even though this screen has no separate "Object Dates" sub-tab link -
# matching the already-proven hardcoded precedent rather than a fresh guess.
${CALENDAR_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Calendar's own form-field label set. Labels are "Calendar Code"/"Calendar Name"
# (screen-prefixed) - confirmed live 2026-08-23 via a field-inventory scan of both the New
# Object (objectForm) and updateAttributes forms (same convention as Royalty Owner/State).
# Start Date is deliberately excluded - insert-only, not present in updateAttributes
# (confirmed live: updateAttributes starts at Calendar Code/Calendar Name/Description/
# Comments/7 weekday indicators, no Start Date/End Date). Description/Comments/weekday
# indicators are optional (not {mandatory:true}) and out of this screen's IUD scope
# (unchanged from the prior driver).
@{CALENDAR_FORM_LABELS}    Calendar Code    Calendar Name


*** Keywords ***
Find Calendar Row By Filter
    [Documentation]    Explicitly filter the Calendar grid's Code column to ${code} via the
    ...    shared T2 Find Object Row By Filter (resources/manage_object.resource) - matches
    ...    Bank/Royalty Owner's own explicit filter usage, rather than relying only on
    ...    Select Object Row's implicit 3s-timeout fallback.
    [Arguments]    ${code}
    Find Object Row By Filter    ${CALENDAR_TABLE}    ${code}

Clear Calendar Row Filter
    [Documentation]    Clear the Code column filter (see Find Calendar Row By Filter) via the
    ...    shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${CALENDAR_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Calendar's OWN credentials (${CALENDAR_EC_USER}/
    ...    ${CALENDAR_EC_PASS} from credentials.py) on the current page. Standing decision:
    ...    every EC screen gets its own dedicated credential pair. Zero-argument wrapper so
    ...    calendar_iud.robot's test cases read as a plain business step; supplies Calendar's
    ...    own credential defaults to the shared T1 Login To EC Screen (common.resource),
    ...    which owns the actual login mechanics.
    Login To EC Screen    ${CALENDAR_EC_USER}    ${CALENDAR_EC_PASS}

Open Calendar Screen
    [Documentation]    Navigate to the Calendar screen. Assumes the caller already logged in
    ...    this test case (via Login To EC Application) - this keyword ONLY navigates.
    ...    Delegates to the shared T1 Open EC Screen (common.resource) for the actual
    ...    mechanics.
    Open EC Screen    ${CALENDAR_SCREEN}

Insert Calendar Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties
    ...    And Verify Code, so calendar_iud.robot's test case body reads as a plain business
    ...    step with ZERO arguments. Also checks the inserted Code matches the suite's
    ...    ${TEST_CODE}. Pre-save evidence screenshot captured before Save is clicked,
    ...    matching Bank/Royalty Owner.
    [Arguments]    ${properties_path}=${CALENDAR_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Calendar Code
    RETURN    ${code}

Verify Calendar Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (no DB check here, matching Bank/Royalty Owner's TC02 convention):
    ...    row exists in the grid, then the form shows what was just inserted (Calendar
    ...    Code/Calendar Name only - Start Date is insert/grid-only, not present in
    ...    updateAttributes). Delegates the full sequence to the shared T2 Verify Object
    ...    Insert Exists. Filters via Find Calendar Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Calendar Row By Filter    ${code}
    Verify Object Insert Exists    ${CALENDAR_TABLE}    ${code}    Calendar
    ...    ${CALENDAR_INSERT_PROPERTIES}    @{CALENDAR_FORM_LABELS}
    ...    code_label=Calendar Code
    Clear Calendar Row Filter

Update Calendar Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Pre-save evidence screenshot captured before Save is clicked, matching Bank/
    ...    Royalty Owner. Filters via Find Calendar Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${CALENDAR_UPDATE_PROPERTIES}
    Find Calendar Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${CALENDAR_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Calendar Code
    Clear Calendar Row Filter
    RETURN    ${data}

Verify Calendar Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification, matching Bank/Royalty Owner's TC03 convention: the form shows the
    ...    updated Name. Delegates the full sequence to the shared T2 Verify Object Form
    ...    Record. Filters via Find Calendar Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Calendar Row By Filter    ${code}
    Verify Object Form Record    ${CALENDAR_TABLE}    ${code}    Calendar
    ...    ${CALENDAR_UPDATE_PROPERTIES}    Calendar Name    code_label=Calendar Code
    Clear Calendar Row Filter

Find Calendar Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Delegates the full select+capture sequence. Calls Find Calendar Row By Filter
    ...    first. Deliberately does NOT clear the filter afterward - Verify Calendar Record
    ...    Found (called right after, same TC) needs the grid still filtered to ${code} for
    ...    its own grid-check, since it doesn't re-select the row itself; it clears the
    ...    filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Calendar Row By Filter    ${code}
    Find Object Record    ${CALENDAR_TABLE}    ${code}    Calendar    code_label=Calendar Code

Verify Calendar Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the form record match the expected (post-update) data. Delegates the full
    ...    sequence to the shared T2 Verify Object Found. Caller must already have selected
    ...    the row (TC04 does, via Find Calendar Record before this) AND left the Code filter
    ...    active from that same call - clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${CALENDAR_TABLE}    ${code}    ${CALENDAR_GRID_VERIFY_PROPERTIES}
    ...    ${CALENDAR_FORM_VERIFY_PROPERTIES}    @{CALENDAR_FORM_LABELS}
    Clear Calendar Row Filter

Delete Calendar Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date,
    ...    called with ZERO arguments (defaults ${code}/${date} to the suite's
    ...    ${TEST_CODE}/${END_DATE}). Select the calendar, set End Date = Start Date (true
    ...    delete), Save. Captures the TC05 evidence screenshot right after the End Date is
    ...    filled but BEFORE Save is clicked, matching Bank/Royalty Owner's convention.
    ...    Filters via Find Calendar Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Calendar Row By Filter    ${code}
    Delete Object Via End Date    ${CALENDAR_TABLE}    ${CALENDAR_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Calendar Row Filter

Verify Calendar Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is
    ...    absent from BOTH the grid and the database.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${CALENDAR_TABLE}    OV_CALENDAR    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Calendar Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to
    ...    the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${CALENDAR_TABLE}    ${code}
