*** Settings ***
Documentation       T3 (screen) — Lifting Account page object.
...                 Screen: Configuration > Assets > Transport_Objects > Lifting Account (CO.2004).
...                 OV-GM (groupmodel manage-object) screen: the grid loads ONLY after the
...                 mandatory navigator is set + GO. Converted to the Area-pattern 5-TC/per-TC-
...                 login/pure-screen-verify STRUCTURE (2026-08-27). Live DOM recon (per-field,
...                 this session) confirmed the navigator is ONE group (nav:form:G:0, a single
...                 fieldset) but its mandatory cascade is rendered across TWO grid rows within
...                 that one group: R:1 C:1..C:3 (Production Unit/Area/Facility Class 1) then R:3
...                 C:0 (Storage) - all four dd spans carry "{mandatory:true} MandatoryCellStyle"
...                 (genuinely empty). This is NOT the "MULTIPLE independent groups" shape that
...                 disqualifies a screen from the Area pattern (that would be separate G:1/G:2
...                 fieldsets, per Tract's precedent) - it is a single group's cascade wrapped
...                 across rows, so it still fits, using the shared "Apply Navigator From
...                 Properties" keyword's new ${row2_from}/${row2}/${row2_start_col} args (added
...                 this session in resources/manage_object.resource) to span the row break.
...                 Storage has no options under the first-available AS1 path - the navigator
...                 uses the SPECIFIC scope already proven live by the pre-existing hand-built
...                 driver (py/lifting_account_iud.py, commit 6e88e371): P1 Production Unit ->
...                 P1 Area -> P1 Facility 1 -> Storage P1_CRUDE_STOR, reused verbatim here (field-
...                 reuse rule - same principle as Tract/Transport Zone/Pipeline Segment/Property).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${LA_SCREEN}            Lifting Account
${LA_TABLE}              manageObject:form:T_data
${LA_NAVIGATOR_PROPERTIES}    ${CURDIR}/../../../../testdata/lifting_account_navigator.properties
${LA_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/lifting_account_insert.properties
${LA_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/lifting_account_update.properties
${LA_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/lifting_account_form_verify.properties
${LA_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/lifting_account_grid_verify.properties
# objectdates field ID (Delete — End Date = Start Date), hardcoded deliberately, NOT label-driven -
# same documented rationale as Area/Bank's own del-enddate id; confirmed live via the pre-existing
# Playwright driver (py/lifting_account_iud.py: DEL_ENDDATE row).
${LA_DEL_ENDDATE}       tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Lifting Account's own form-field label set (Start Date deliberately excluded - it lives only in
# the insert form's own Start Date field, not a round-trip-compared updateAttributes label; Company
# Name/Storage Name deliberately excluded from round-trip comparison - both are dropdown/reference
# values that can re-render different display text after reload, same caveat as every other
# converted screen's dropdown fields).
@{LA_FORM_LABELS}    Lifting Account Code    Lifting Account Name


*** Keywords ***
Find Lifting Account Row By Filter
    [Documentation]    Explicitly filter the Lifting Account grid's Code column to ${code} via the
    ...    shared T2 Find Object Row By Filter (resources/manage_object.resource).
    [Arguments]    ${code}
    Find Object Row By Filter    ${LA_TABLE}    ${code}

Clear Lifting Account Row Filter
    [Documentation]    Clear the Code column filter (see Find Lifting Account Row By Filter) via
    ...    the shared T2 Clear Object Row Filter.
    Clear Object Row Filter    ${LA_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Lifting Account's OWN credentials (${LIFTING_ACCOUNT_EC_USER}/
    ...    ${LIFTING_ACCOUNT_EC_PASS} from credentials.py) on the current page - works whether this
    ...    is the very first login (page freshly loaded on the login form via the shared T1 Open
    ...    EC Application) or a re-login after Logout From EC Application.
    Login To EC Screen    ${LIFTING_ACCOUNT_EC_USER}    ${LIFTING_ACCOUNT_EC_PASS}

Open Lifting Account Screen With Navigator Values Populated
    [Documentation]    Navigate to the Lifting Account screen, THEN fill + submit the mandatory
    ...    navigator (cascade spanning R:1 C:1..3 + R:3 C:0, then GO) - the grid stays empty until
    ...    this happens. Delegates to the shared T2 "Apply Navigator From Properties" (resources/
    ...    manage_object.resource), driven by testdata/lifting_account_navigator.properties, using
    ...    the new ${row2_from}/${row2}/${row2_start_col} args to span Lifting Account's row break
    ...    (3 values on row=1 starting at C:1, then the 4th value on row=3 starting at C:0).
    Open EC Screen    ${LA_SCREEN}
    Apply Navigator From Properties    ${LA_NAVIGATOR_PROPERTIES}
    ...    row2_from=3    row2=3    row2_start_col=0

Insert Lifting Account Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Object From Properties And Verify
    ...    Code, called with ZERO arguments so lifting_account_iud.robot's test case body reads as
    ...    a plain business step. testdata/lifting_account_insert.properties' Storage Name value
    ...    MUST equal the navigator's own Storage value (P1_CRUDE_STOR) or the new row is not
    ...    visible under this OV-GM navigator scope (parent-matching rule).
    [Arguments]    ${properties_path}=${LA_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Lifting Account Code
    RETURN    ${code}

Verify Lifting Account Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification (no
    ...    DB check here - that's TC02's own separate DbVerify assertion): row exists in the grid,
    ...    then Lifting Account Code/Lifting Account Name's LIVE SCREEN value is compared to
    ...    testdata/lifting_account_insert.properties. Filters via Find Lifting Account Row By
    ...    Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Lifting Account Row By Filter    ${code}
    Verify Object Insert Exists    ${LA_TABLE}    ${code}    Lifting Account    ${LA_INSERT_PROPERTIES}
    ...    @{LA_FORM_LABELS}    code_label=Lifting Account Code
    Clear Lifting Account Row Filter

Update Lifting Account Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Only Lifting
    ...    Account Name is listed in testdata/lifting_account_update.properties - Lifting Account
    ...    Code is read-only in updateAttributes. Filters via Find Lifting Account Row By Filter
    ...    first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${LA_UPDATE_PROPERTIES}
    Find Lifting Account Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${LA_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Lifting Account Code
    Clear Lifting Account Row Filter
    RETURN    ${data}

Verify Lifting Account Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification:
    ...    selects the row, compares Lifting Account Name's LIVE SCREEN value to
    ...    testdata/lifting_account_update.properties. Filters via Find Lifting Account Row By
    ...    Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Lifting Account Row By Filter    ${code}
    Verify Object Form Record    ${LA_TABLE}    ${code}    Lifting Account    ${LA_UPDATE_PROPERTIES}
    ...    Lifting Account Name    code_label=Lifting Account Code
    Clear Lifting Account Row Filter

Find Lifting Account Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Calls Find Lifting
    ...    Account Row By Filter first. Deliberately does NOT clear the filter afterward - Verify
    ...    Lifting Account Record Found (called right after, same TC) needs the grid still
    ...    filtered to ${code} for its own grid-check; it clears the filter once both checks are
    ...    done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Lifting Account Row By Filter    ${code}
    Find Object Record    ${LA_TABLE}    ${code}    Lifting Account    code_label=Lifting Account Code

Verify Lifting Account Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND
    ...    the full form record match the expected data. Caller must already have selected the
    ...    row (TC04 does, via Find Lifting Account Record before this) AND left the Code filter
    ...    active - clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${LA_TABLE}    ${code}    ${LA_GRID_VERIFY_PROPERTIES}
    ...    ${LA_FORM_VERIFY_PROPERTIES}    @{LA_FORM_LABELS}
    Clear Lifting Account Row Filter

Delete Lifting Account Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the record, set End Date = Start Date (EC true delete for OV_LIFTING_ACCOUNT),
    ...    Save. Filters via Find Lifting Account Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Lifting Account Row By Filter    ${code}
    Delete Object Via End Date    ${LA_TABLE}    ${LA_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Lifting Account Row Filter

Verify Lifting Account Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid AND the database (OV_LIFTING_ACCOUNT) - the DB check lives here, in
    ...    the shared T2 Verify Object Removed.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${LA_TABLE}    OV_LIFTING_ACCOUNT    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Lifting Account Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification
    ...    (grid-only check) - delegates to the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${LA_TABLE}    ${code}
