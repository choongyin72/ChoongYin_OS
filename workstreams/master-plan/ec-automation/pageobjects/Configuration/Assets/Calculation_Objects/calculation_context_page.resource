*** Settings ***
Documentation       T3 (screen) — Calculation Context page object.
...                 Screen: Configuration > Assets > Calculation Objects > Calculation Context (CO.1059).
...                 Manage-Object (OV) screen. Holds Calculation Context's locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common).
...                 Live recon (2026-08-23): objectForm fields = Calc Context Code / Calc Context
...                 Name / Start Date (mandatory) / End Date / Description / Comments. updateAttributes
...                 fields = Calc Context Code (read-only there) / Calc Context Name / Description /
...                 Comments (no Start/End Date - those live only in objectdates, matching Bank's
...                 documented shape). No mandatory navigator dropdown beyond the universal GO bar -
...                 confirmed Bank-pattern-shaped, brought up to full parity with bank_page.resource
...                 (batch7 ground-rules doc, Configuration Assets Calculation Objects Calculation
...                 Context assignment).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${CALC_CONTEXT_SCREEN}          Calculation Context
${CALC_CONTEXT_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/calculation_context_insert.properties
${CALC_CONTEXT_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/calculation_context_update.properties
${CALC_CONTEXT_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/calculation_context_form_verify.properties
${CALC_CONTEXT_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/calculation_context_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal
# string (manage_object.resource defines this ONCE specifically so no T3 duplicates it).
${CALC_CONTEXT_TABLE}           ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date). Hardcoded deliberately (matching Bank's
# documented precedent), live-verified 2026-08-23 via OV Field Id By Label on this exact screen
# (Select Object Row EC_PROD -> objectdates -> End Date resolved to this same
# G:0:R:0:C:3:da_input id), so unlike Bank's own note this value IS independently confirmed here,
# not just carried over on trust.
${CALC_CONTEXT_DEL_ENDDATE}     tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Calculation Context's own updateAttributes label set (Start Date/End Date deliberately excluded -
# they live only in objectdates, not updateAttributes; confirmed by the live field-inventory scan
# 2026-08-23). Defined ONCE here so both Verify Calculation Context Record Exists (TC02, against
# calculation_context_insert.properties) and Verify Calculation Context Record Found (TC04, against
# calculation_context_form_verify.properties) share the same list (matches Bank's 2026-08-22
# consolidation of the T2 Verify Object Insert Exists/Found calls).
@{CALC_CONTEXT_FORM_LABELS}    Calc Context Code    Calc Context Name    Description    Comments


*** Keywords ***
Find Calculation Context Row By Filter
    [Documentation]    Explicitly filter the Calculation Context grid's Code column to ${code} via
    ...    the shared T2 Find Object Row By Filter (resources/manage_object.resource) - matches
    ...    Bank's/Account's own explicit filter usage (owner, 2026-08-22: "others... should follow
    ...    Account... utilise same filter feature"), rather than relying only on Select Object
    ...    Row's implicit 3s-timeout fallback.
    [Arguments]    ${code}
    Find Object Row By Filter    ${CALC_CONTEXT_TABLE}    ${code}

Clear Calculation Context Row Filter
    [Documentation]    Clear the Code column filter (see Find Calculation Context Row By Filter)
    ...    via the shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${CALC_CONTEXT_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Calculation Context's OWN credentials
    ...    (${CALC_CONTEXT_EC_USER}/${CALC_CONTEXT_EC_PASS} from credentials.py) on
    ...    the current page - works whether this is the very first login (page freshly loaded on
    ...    the login form via the shared T1 Open EC Application) or a re-login after Logout From
    ...    EC Application (same login form, not a new page/tab). Screen-specific wrapper (matching
    ...    Bank's convention: bank_iud.robot's test cases call this with ZERO arguments) that
    ...    supplies Calculation Context's own credential defaults to the shared T1 Login To EC
    ...    Screen (common.resource), which owns the actual login mechanics - kept here only
    ...    because a shared file should not hardcode any screen's credentials.
    Login To EC Screen    ${CALC_CONTEXT_EC_USER}    ${CALC_CONTEXT_EC_PASS}

Open Calculation Context Screen
    [Documentation]    Navigate to the Calculation Context screen. Assumes the caller already
    ...    logged in this test case (via Login To EC Application) - this keyword ONLY navigates
    ...    (matching Bank's convention: every test case gets its own explicit Login/Logout step
    ...    instead of one shared Suite Setup/Teardown login). Delegates to the shared T1 Open EC
    ...    Screen (common.resource) for the actual mechanics. Loads the grid via Apply Navigator
    ...    (GO) right after navigating - this screen has no default rows on open (confirmed live).
    Open EC Screen    ${CALC_CONTEXT_SCREEN}
    Apply Navigator

Insert Calculation Context Record And Save
    [Documentation]    Friendly-narrative wrapper (matching Bank's convention) around Insert
    ...    Calculation Context From Properties, purely so calculation_context_iud.robot's test
    ...    case body reads as a plain business step with ZERO arguments - the underlying
    ...    mechanics (properties-file-driven insert) are UNCHANGED. Also owns the integrity check
    ...    that the inserted Code matches the suite's ${TEST_CODE} - fails on its own if
    ...    testdata/calculation_context_insert.properties' Code ever drifts out of sync with the
    ...    suite variable. The TC02 evidence screenshot is captured BEFORE Save is clicked (passed
    ...    through to Insert Object From Properties, which fills every field first).
    [Arguments]    ${properties_path}=${CALC_CONTEXT_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Calc Context Code
    RETURN    ${code}

Verify Calculation Context Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification: row
    ...    exists in the grid, then every field's LIVE SCREEN value (via Get OV Field Value By
    ...    Label) is compared to testdata/calculation_context_insert.properties (Calc Context
    ...    Code, Calc Context Name, Description, Comments — ${CALC_CONTEXT_FORM_LABELS}).
    ...    Start Date is NOT verified here - it only exists as a grid column/objectdates field,
    ...    not an updateAttributes field (matches Bank's documented convention).
    ...    Delegates the full sequence (row-check, select, form-compare, screenshot) to the
    ...    shared T2 Verify Object Insert Exists. Filters via Find Calculation Context Row By
    ...    Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Calculation Context Row By Filter    ${code}
    Verify Object Insert Exists    ${CALC_CONTEXT_TABLE}    ${code}    Calculation Context
    ...    ${CALC_CONTEXT_INSERT_PROPERTIES}    @{CALC_CONTEXT_FORM_LABELS}
    ...    code_label=Calc Context Code
    Clear Calculation Context Row Filter

Update Calculation Context Record And Save
    [Documentation]    Friendly-narrative wrapper (matching Bank's convention) around T2's Update
    ...    Object From Properties, called with ZERO arguments (defaults ${code} to the suite's
    ...    ${TEST_CODE}). Returns the applied {label: value} dict so the caller can DB-verify
    ...    against exactly what was set. The TC03 evidence screenshot is captured BEFORE Save is
    ...    clicked (passed through to Update Object From Properties, which fills every field
    ...    first). Filters via Find Calculation Context Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${CALC_CONTEXT_UPDATE_PROPERTIES}
    Find Calculation Context Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${CALC_CONTEXT_TABLE}    ${code}
    ...    ${properties_path}    ${TEST NAME}_action    code_label=Calc Context Code
    Clear Calculation Context Row Filter
    RETURN    ${data}

Verify Calculation Context Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification:
    ...    selects the row (loading updateAttributes), then compares Calc Context Name/
    ...    Description/Comments's LIVE SCREEN value (via Get OV Field Value By Label) to
    ...    testdata/calculation_context_update.properties - only those fields, since that's the
    ...    only fields that file has (unlike the default calculation_context_form_verify.properties
    ...    /${CALC_CONTEXT_FORM_LABELS}, which has the full field set). Delegates the full
    ...    sequence (select, form-compare, screenshot) to the shared T2 Verify Object Form Record.
    ...    Filters via Find Calculation Context Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Calculation Context Row By Filter    ${code}
    Verify Object Form Record    ${CALC_CONTEXT_TABLE}    ${code}    Calculation Context
    ...    ${CALC_CONTEXT_UPDATE_PROPERTIES}    Calc Context Name    Description    Comments
    ...    code_label=Calc Context Code
    Clear Calculation Context Row Filter

Find Calculation Context Record
    [Documentation]    Friendly-narrative wrapper (matching Bank's convention) around the shared
    ...    T2 Find Object Record, called with ZERO arguments (defaults ${code} to the suite's
    ...    ${TEST_CODE}). Delegates the full select+capture sequence. Calls Find Calculation
    ...    Context Row By Filter first. Deliberately does NOT clear the filter afterward - Verify
    ...    Calculation Context Record Found (called right after, same TC) needs the grid still
    ...    filtered to ${code} for its own grid-check, since it doesn't re-select the row itself;
    ...    it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Calculation Context Row By Filter    ${code}
    Find Object Record    ${CALC_CONTEXT_TABLE}    ${code}    Calculation Context
    ...    code_label=Calc Context Code

Verify Calculation Context Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND
    ...    the full form record match the expected data - the SAME two existing live-DOM
    ...    round-trip keywords, just called under one name. Also captures the TC04 evidence
    ...    screenshot. Delegates the full sequence (grid-compare, form-compare, screenshot) to
    ...    the shared T2 Verify Object Found. Caller must already have selected the row (TC04
    ...    does, via Find Calculation Context Record before this) AND left the Code filter active
    ...    from that same call - clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${CALC_CONTEXT_TABLE}    ${code}
    ...    ${CALC_CONTEXT_GRID_VERIFY_PROPERTIES}    ${CALC_CONTEXT_FORM_VERIFY_PROPERTIES}
    ...    @{CALC_CONTEXT_FORM_LABELS}
    Clear Calculation Context Row Filter

Delete Calculation Context Record And Save
    [Documentation]    Friendly-narrative wrapper (matching Bank's convention) around T2's Delete
    ...    Object Via End Date, called with ZERO arguments (defaults ${code}/${date} to the
    ...    suite's ${TEST_CODE}/${END_DATE}). Select the calculation_context, set End Date =
    ...    Start Date (true delete), Save. Captures the TC05 evidence screenshot right after the
    ...    End Date is filled but BEFORE Save is clicked. Filters via Find Calculation Context
    ...    Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Calculation Context Row By Filter    ${code}
    Delete Object Via End Date    ${CALC_CONTEXT_TABLE}    ${CALC_CONTEXT_DEL_ENDDATE}
    ...    ${code}    ${date}    ${TEST NAME}_action
    Clear Calculation Context Row Filter

Verify Calculation Context Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid and the database (OV_CALC_CONTEXT) - the SAME two existing
    ...    DB-ground-truth keywords, just called under one name. Also captures the TC05 evidence
    ...    screenshot.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${CALC_CONTEXT_TABLE}    OV_CALC_CONTEXT    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Calculation Context Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to the shared
    ...    T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${CALC_CONTEXT_TABLE}    ${code}
