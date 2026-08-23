*** Settings ***
Documentation       T3 (screen) — Calendar Collection page object.
...                 Screen: Configuration > Assets > Date Objects > Calendar Collection (CD.0105).
...                 Custom-URL OV, date-effective screen (grid nav:form:T_data, NO navigator GO -
...                 confirmed live 2026-08-23: manage_object_nav grid count=0, GO button count=0;
...                 Save And Refresh List's toolbar-Refresh fallback already handles this).
...                 Rebuilt 2026-08-23 to mirror Bank/Country/State exactly (Batch 6, FINAL batch,
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
${CC_SCREEN}          Calendar Collection
${CC_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/calendar_collection_insert.properties
${CC_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/calendar_collection_update.properties
${CC_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/calendar_collection_form_verify.properties
${CC_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/calendar_collection_grid_verify.properties
# Custom-URL OV table id (NOT the manage_object_nav constant - confirmed live 2026-08-23:
# nav:form:T_data present=1, manage_object_nav present=0, per docs/ec_screen_registry.md's
# existing entry for this screen).
${CC_TABLE}           nav:form:T_data
# objectdates field ID (Delete — End Date = Start Date), confirmed live 2026-08-23
# (tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input).
${CC_DEL_ENDDATE}     tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Calendar Collection's own form-field label set. Labels are GENERIC "Code"/"Name" (NOT
# screen-prefixed) - confirmed live 2026-08-23 via a field-label recon dumping every ECCell
# label in both objectForm (Insert, 8 labels: Code, Name, Start Date (mandatory), End Date,
# Description, Comments - NO weekday-indicator checkboxes on this EC build, contrary to the
# pre-existing hardcoded-pattern page object's stale docstring) and updateAttributes (Update,
# 4 labels: Code, Name, Description, Comments). Only Code/Name are MandatoryCellStyle-confirmed
# mandatory besides Start Date (Insert-only) - IUD-fill-only-needed-fields convention, so
# @{CC_FORM_LABELS} deliberately lists only the mandatory, always-present pair (Start Date
# excluded - Insert-only, not in updateAttributes, same as Bank/Country/State).
@{CC_FORM_LABELS}    Code    Name


*** Keywords ***
Find Calendar Collection Row By Filter
    [Documentation]    Explicitly filter the Calendar Collection grid's Code column to ${code}
    ...    via the shared T2 Find Object Row By Filter (resources/manage_object.resource) -
    ...    matches Account/Bank/State/Country's own explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${CC_TABLE}    ${code}

Clear Calendar Collection Row Filter
    [Documentation]    Clear the Code column filter (see Find Calendar Collection Row By
    ...    Filter) via the shared T2 Clear Object Row Filter, restoring the grid's normal
    ...    unfiltered view.
    Clear Object Row Filter    ${CC_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Calendar Collection's OWN credentials
    ...    (${CALENDAR_COLLECTION_EC_USER}/${CALENDAR_COLLECTION_EC_PASS} from credentials.py)
    ...    on the current page. Standing decision (owner, 2026-08-22): every EC screen gets its
    ...    own dedicated credential pair. Zero-argument wrapper so calendar_collection_iud.robot's
    ...    test cases read as a plain business step; supplies Calendar Collection's own
    ...    credential defaults to the shared T1 Login To EC Screen (common.resource), which owns
    ...    the actual login mechanics.
    Login To EC Screen    ${CALENDAR_COLLECTION_EC_USER}    ${CALENDAR_COLLECTION_EC_PASS}

Open Calendar Collection Screen
    [Documentation]    Navigate to the Calendar Collection screen. Assumes the caller already
    ...    logged in this test case (via Login To EC Application) - this keyword ONLY navigates.
    ...    Delegates to the shared T1 Open EC Screen (common.resource) for the actual mechanics.
    Open EC Screen    ${CC_SCREEN}

Insert Calendar Collection Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties And
    ...    Verify Code, so calendar_collection_iud.robot's test case body reads as a plain
    ...    business step with ZERO arguments. Also checks the inserted Code matches the suite's
    ...    ${TEST_CODE}. Pre-save evidence screenshot captured before Save is clicked, matching
    ...    Bank/Country.
    [Arguments]    ${properties_path}=${CC_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Code
    RETURN    ${code}

Verify Calendar Collection Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification (no
    ...    DB check here, matching Bank/Country's TC02 convention): row exists in the grid, then
    ...    the form shows what was just inserted (Code/Name only - Start Date is grid/insert-only,
    ...    not present in updateAttributes). Delegates the full sequence (row-check, select,
    ...    form-compare, screenshot) to the shared T2 Verify Object Insert Exists. Filters via
    ...    Find Calendar Collection Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Calendar Collection Row By Filter    ${code}
    Verify Object Insert Exists    ${CC_TABLE}    ${code}    Calendar Collection    ${CC_INSERT_PROPERTIES}
    ...    @{CC_FORM_LABELS}    code_label=Code
    Clear Calendar Collection Row Filter

Update Calendar Collection Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Pre-save
    ...    evidence screenshot captured before Save is clicked, matching Bank/Country. Filters
    ...    via Find Calendar Collection Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${CC_UPDATE_PROPERTIES}
    Find Calendar Collection Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${CC_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Code
    Clear Calendar Collection Row Filter
    RETURN    ${data}

Verify Calendar Collection Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification,
    ...    matching Bank/Country's TC03 convention: the form shows the updated Name. Delegates
    ...    the full sequence (select, form-compare, screenshot) to the shared T2 Verify Object
    ...    Form Record. Filters via Find Calendar Collection Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Calendar Collection Row By Filter    ${code}
    Verify Object Form Record    ${CC_TABLE}    ${code}    Calendar Collection    ${CC_UPDATE_PROPERTIES}
    ...    Name    code_label=Code
    Clear Calendar Collection Row Filter

Find Calendar Collection Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates the full
    ...    select+capture sequence. Calls Find Calendar Collection Row By Filter first.
    ...    Deliberately does NOT clear the filter afterward - Verify Calendar Collection Record
    ...    Found (called right after, same TC) needs the grid still filtered to ${code} for its
    ...    own grid-check, since it doesn't re-select the row itself; it clears the filter once
    ...    both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Calendar Collection Row By Filter    ${code}
    Find Object Record    ${CC_TABLE}    ${code}    Calendar Collection    code_label=Code

Verify Calendar Collection Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND
    ...    the form record match the expected (post-update) data. Delegates the full sequence
    ...    (grid-compare, form-compare, screenshot) to the shared T2 Verify Object Found. Caller
    ...    must already have selected the row (TC04 does, via Find Calendar Collection Record
    ...    before this) AND left the Code filter active from that same call - clears the filter
    ...    itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${CC_TABLE}    ${code}    ${CC_GRID_VERIFY_PROPERTIES}
    ...    ${CC_FORM_VERIFY_PROPERTIES}    @{CC_FORM_LABELS}
    Clear Calendar Collection Row Filter

Delete Calendar Collection Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the Calendar Collection, set End Date = Start Date (true delete), Save.
    ...    Captures the TC05 evidence screenshot right after the End Date is filled but BEFORE
    ...    Save is clicked, matching Bank/Country. Filters via Find Calendar Collection Row By
    ...    Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Calendar Collection Row By Filter    ${code}
    Delete Object Via End Date    ${CC_TABLE}    ${CC_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Calendar Collection Row Filter

Verify Calendar Collection Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid and the database (OV_CALENDAR_COLLECTION).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${CC_TABLE}    OV_CALENDAR_COLLECTION    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Calendar Collection Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to the shared
    ...    T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${CC_TABLE}    ${code}
