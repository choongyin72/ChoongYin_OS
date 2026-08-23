*** Settings ***
Documentation       T3 (screen) — Process Train page object.
...                 Screen: Configuration > Assets > Facility_Objects > Process Train (CO.0120).
...                 Manage-Object (OV) screen. Holds Process Train's locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common).
...                 Rebuilt 2026-08-23 (Batch 9) to mirror Bank/Berth exactly - replaces the
...                 older fixed-argument, no-filter pattern with the label-driven,
...                 properties-file-driven, grid-filter-wired, T2-consolidated pattern.
...                 CORRECTION (2026-08-23, live repro): the KB doc's "no mandatory dropdowns"
...                 note does not hold for actually persisting the record - Insert with only
...                 Code/Name/Start Date clicked Save successfully but the record never reached
...                 OV_PROCESS_TRAIN and left EC's own unsaved-changes confirmation modal open,
...                 stalling the suite. The already-proven driver py/process_train_iud.py (which
...                 fills "Production Facility Class 1" = __FIRST__) passed 7/7 unmodified, so
...                 that dropdown IS included in testdata/process_train_insert.properties too -
...                 deliberately EXCLUDED from @{PROCESS_TRAIN_FORM_LABELS} (round-trip verify)
...                 since __FIRST__ never matches the resolved literal text on reload (documented
...                 Batch 9 gotcha).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${PROCESS_TRAIN_SCREEN}    Process Train
${PROCESS_TRAIN_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/process_train_insert.properties
${PROCESS_TRAIN_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/process_train_update.properties
${PROCESS_TRAIN_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/process_train_form_verify.properties
${PROCESS_TRAIN_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/process_train_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal.
${PROCESS_TRAIN_TABLE}    ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date), matching Bank/Berth's convention -
# confirmed the SAME literal is used across every Bank-family screen (Bank/Berth/Company/
# Node/Chemical Transport Tank/etc.), not screen-specific.
${PROCESS_TRAIN_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Process Train's own form-field label set. Labels are "Process Train Code"/"Process Train
# Name" (screen-prefixed) - confirmed via ec-ui-knowledge/screens/process_train.md and the
# already-proven Playwright driver py/process_train_iud.py. Start Date deliberately excluded -
# Insert-only, not present in updateAttributes (same as Bank/Berth). Defined ONCE here so both
# Verify Process Train Record Exists (TC02) and Verify Process Train Record Found (TC04) share
# the same list.
@{PROCESS_TRAIN_FORM_LABELS}    Process Train Code    Process Train Name


*** Keywords ***
Find Process Train Row By Filter
    [Documentation]    Explicitly filter the Process Train grid's Code column to ${code} via the
    ...    shared T2 Find Object Row By Filter (resources/manage_object.resource) - matches
    ...    Account/Bank/Berth's own explicit filter usage (owner, 2026-08-22: "others...
    ...    should follow Account... utilise same filter feature"), rather than relying only on
    ...    Select Object Row's implicit 3s-timeout fallback.
    [Arguments]    ${code}
    Find Object Row By Filter    ${PROCESS_TRAIN_TABLE}    ${code}

Clear Process Train Row Filter
    [Documentation]    Clear the Code column filter (see Find Process Train Row By Filter) via
    ...    the shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${PROCESS_TRAIN_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Process Train's OWN credentials
    ...    (${PROCESS_TRAIN_EC_USER}/${PROCESS_TRAIN_EC_PASS} from credentials.py) on the
    ...    current page. Standing decision (owner, 2026-08-22): every EC screen gets its own
    ...    dedicated credential pair. Zero-argument wrapper so process_train_iud.robot's test
    ...    cases read as a plain business step; supplies Process Train's own credential
    ...    defaults to the shared T1 Login To EC Screen (common.resource), which owns the
    ...    actual login mechanics.
    Login To EC Screen    ${PROCESS_TRAIN_EC_USER}    ${PROCESS_TRAIN_EC_PASS}

Open Process Train Screen
    [Documentation]    Navigate to the Process Train screen. Assumes the caller already logged
    ...    in this test case (via Login To EC Application) - this keyword ONLY navigates.
    ...    Delegates to the shared T1 Open EC Screen (common.resource) for the actual mechanics.
    Open EC Screen    ${PROCESS_TRAIN_SCREEN}

Insert Process Train Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties And
    ...    Verify Code, so process_train_iud.robot's test case body reads as a plain business
    ...    step with ZERO arguments. Also checks the inserted Code matches the suite's
    ...    ${TEST_CODE}. Pre-save evidence screenshot captured before Save is clicked, matching
    ...    Bank/Berth.
    [Arguments]    ${properties_path}=${PROCESS_TRAIN_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Process Train Code
    RETURN    ${code}

Verify Process Train Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification (no
    ...    DB check here, matching Bank/Berth's TC02 convention): row exists in the grid, then the
    ...    form shows what was just inserted (Process Train Code/Process Train Name only - Start
    ...    Date is grid/insert-only, not present in updateAttributes). Delegates the full sequence
    ...    (row-check, select, form-compare, screenshot) to the shared T2 Verify Object Insert
    ...    Exists. Filters via Find Process Train Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Process Train Row By Filter    ${code}
    Verify Object Insert Exists    ${PROCESS_TRAIN_TABLE}    ${code}    Process Train
    ...    ${PROCESS_TRAIN_INSERT_PROPERTIES}    @{PROCESS_TRAIN_FORM_LABELS}
    ...    code_label=Process Train Code
    Clear Process Train Row Filter

Update Process Train Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Pre-save
    ...    evidence screenshot captured before Save is clicked, matching Bank/Berth. Filters via
    ...    Find Process Train Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${PROCESS_TRAIN_UPDATE_PROPERTIES}
    Find Process Train Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${PROCESS_TRAIN_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Process Train Code
    Clear Process Train Row Filter
    RETURN    ${data}

Verify Process Train Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification,
    ...    matching Bank/Berth's TC03 convention: the form shows the updated Process Train Name.
    ...    Delegates the full sequence (select, form-compare, screenshot) to the shared T2 Verify
    ...    Object Form Record. Filters via Find Process Train Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Process Train Row By Filter    ${code}
    Verify Object Form Record    ${PROCESS_TRAIN_TABLE}    ${code}    Process Train
    ...    ${PROCESS_TRAIN_UPDATE_PROPERTIES}    Process Train Name    code_label=Process Train Code
    Clear Process Train Row Filter

Find Process Train Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates the full
    ...    select+capture sequence. Calls Find Process Train Row By Filter first. Deliberately
    ...    does NOT clear the filter afterward - Verify Process Train Record Found (called right
    ...    after, same TC) needs the grid still filtered to ${code} for its own grid-check, since
    ...    it doesn't re-select the row itself; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Process Train Row By Filter    ${code}
    Find Object Record    ${PROCESS_TRAIN_TABLE}    ${code}    Process Train
    ...    code_label=Process Train Code

Verify Process Train Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND
    ...    the form record match the expected (post-update) data. Delegates the full sequence
    ...    (grid-compare, form-compare, screenshot) to the shared T2 Verify Object Found. Caller
    ...    must already have selected the row (TC04 does, via Find Process Train Record before
    ...    this) AND left the Code filter active from that same call - clears the filter itself
    ...    once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${PROCESS_TRAIN_TABLE}    ${code}    ${PROCESS_TRAIN_GRID_VERIFY_PROPERTIES}
    ...    ${PROCESS_TRAIN_FORM_VERIFY_PROPERTIES}    @{PROCESS_TRAIN_FORM_LABELS}
    Clear Process Train Row Filter

Delete Process Train Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the process train, set End Date = Start Date (true delete), Save. Captures the
    ...    TC05 evidence screenshot right after the End Date is filled but BEFORE Save is clicked,
    ...    matching Bank/Berth's convention. Filters via Find Process Train Row By Filter first,
    ...    clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Process Train Row By Filter    ${code}
    Delete Object Via End Date    ${PROCESS_TRAIN_TABLE}    ${PROCESS_TRAIN_DEL_ENDDATE}    ${code}
    ...    ${date}    ${TEST NAME}_action
    Clear Process Train Row Filter

Verify Process Train Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid and the database.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${PROCESS_TRAIN_TABLE}    OV_PROCESS_TRAIN    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Process Train Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to the shared
    ...    T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${PROCESS_TRAIN_TABLE}    ${code}
