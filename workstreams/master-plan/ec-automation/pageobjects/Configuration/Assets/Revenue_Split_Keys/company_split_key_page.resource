*** Settings ***
Documentation       T3 (screen) — Company Split Key page object.
...                 Screen: Configuration > Assets > Revenue Split Keys > Company Split Key
...                 (CD.0044). One of 6 sibling "* Split Key" screens sharing ONE underlying
...                 class SPLIT_KEY (OBJECT/VERSIONED, base table SPLIT_KEY, view
...                 OV_SPLIT_KEY) via the SAME generic controller URL
...                 manage_object_split_key/CLASS_NAME/SPLIT_KEY/SPLIT_TYPE/<TYPE> - this
...                 screen's own confirmed URL is .../SPLIT_TYPE/COMPANY (live 2026-08-25).
...                 The other 5 siblings (Product/Field/Stream Item Category/Other/Stream
...                 Item Split Key) are built independently in parallel, each with its OWN
...                 distinctly-scoped test code, to avoid cross-screen collision on the
...                 shared OV_SPLIT_KEY view — DO NOT reuse a generic AUTOTEST_SPLIT_KEY code.
...                 Custom-URL OV (confirmed live 2026-08-25: navigator fields=[], no Date/GO
...                 pair despite the sibling-screen investigation note describing one - a live
...                 dump of every nav:form:* input/button on THIS screen found no da_input/
...                 dd_input at all, only the grid's own column-filter inputs and a
...                 navButton:form:B labelled "Go..." whose click made no difference to the
...                 11-row grid already rendered before it was clicked - genuinely no
...                 mandatory nav gate, matches Report Context/WBS/Calendar/Account, NOT the
...                 manage-object manage_object_nav_nav:form:T_data+GO variant). Grid id is
...                 nav:form:T_data.
...                 Brand-new build 2026-08-25 (no prior automation existed for this specific
...                 screen - grep confirmed the only other Split-Key-family automation
...                 targets Split Item Other CD.0017, a DIFFERENT screen/class via a DIFFERENT
...                 controller manage_object_nav, do not confuse the two). Built directly to
...                 the label-driven, properties-file-driven, T2-consolidated pattern matching
...                 Bank/WBS/Report Context (ec-bank-pattern-new-screen skill).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${COMPANY_SPLIT_KEY_SCREEN}    Company Split Key
${COMPANY_SPLIT_KEY_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/company_split_key_insert.properties
${COMPANY_SPLIT_KEY_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/company_split_key_update.properties
${COMPANY_SPLIT_KEY_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/company_split_key_form_verify.properties
${COMPANY_SPLIT_KEY_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/company_split_key_grid_verify.properties
# Grid id: custom-URL OV - grid is nav:form:T_data (NOT manage_object_nav_nav:form:T_data) and
# there is no mandatory navigator field to fill (confirmed live 2026-08-25 - see Documentation
# above). T2's Save And Refresh List auto-detects this and falls back to toolbar Refresh.
${COMPANY_SPLIT_KEY_TABLE}    nav:form:T_data
# objectdates field ID (Delete — End Date = Start Date), framework-invariant objectdates
# layout (R:0:C:1 = Start Date, R:0:C:3 = End Date), matching Bank/WBS/Report Context.
${COMPANY_SPLIT_KEY_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Company Split Key's own form-field label set - SCREEN-PREFIXED labels ("Split Key Code" /
# "Split Key Name"), NOT plain "Code"/"Name" (confirmed live 2026-08-25 via both the New
# Object form (objectForm) and the row-select form (updateAttributes) label dumps). Only
# Split Key Code / Split Key Name / Start Date are mandatory-yellow-and-empty on a fresh
# Insert; Description/Comments/Value Method/Shares add to 100%/Rounding Rule/Number of
# Rounding Decimals/Number Display Format all showed populated/optional on existing rows
# (CO0001 etc in OV_SPLIT_KEY), matching the sibling-screen investigation's shared-field note
# and this screen's own live scan - deliberately left unset per the IUD-fill-only-needed-
# fields convention. Start Date deliberately excluded from this label set - Insert-only, not
# present in updateAttributes (same as Bank/WBS/Report Context).
@{COMPANY_SPLIT_KEY_FORM_LABELS}    Split Key Code    Split Key Name


*** Keywords ***
Find Company Split Key Row By Filter
    [Documentation]    Explicitly filter the Company Split Key grid's Code column to ${code}
    ...    via the shared T2 Find Object Row By Filter (resources/manage_object.resource) -
    ...    matches Account/Bank/WBS/Report Context's explicit filter usage, rather than
    ...    relying only on Select Object Row's implicit 3s-timeout fallback.
    [Arguments]    ${code}
    Find Object Row By Filter    ${COMPANY_SPLIT_KEY_TABLE}    ${code}

Clear Company Split Key Row Filter
    [Documentation]    Clear the Code column filter (see Find Company Split Key Row By
    ...    Filter) via the shared T2 Clear Object Row Filter, restoring the grid's normal
    ...    unfiltered view.
    Clear Object Row Filter    ${COMPANY_SPLIT_KEY_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Company Split Key's OWN credentials
    ...    (${COMPANY_SPLIT_KEY_EC_USER}/${COMPANY_SPLIT_KEY_EC_PASS} from credentials.py) on
    ...    the current page. Standing decision: every EC screen gets its own dedicated
    ...    credential pair. Zero-argument wrapper so company_split_key_iud.robot's test cases
    ...    read as a plain business step; supplies Company Split Key's own credential
    ...    defaults to the shared T1 Login To EC Screen (common.resource), which owns the
    ...    actual login mechanics.
    Login To EC Screen    ${COMPANY_SPLIT_KEY_EC_USER}    ${COMPANY_SPLIT_KEY_EC_PASS}

Open Company Split Key Screen
    [Documentation]    Navigate to the Company Split Key screen. Assumes the caller already
    ...    logged in this test case (via Login To EC Application) - this keyword ONLY
    ...    navigates. Delegates to the shared T1 Open EC Screen (common.resource) for the
    ...    actual mechanics. Deliberately does NOT click any GO/navButton or call Apply
    ...    Navigator - live scan 2026-08-25 confirmed this screen has no mandatory navigator
    ...    field (fields=[]); the grid (nav:form:T_data) renders with its existing 11 rows
    ...    directly on open, and clicking the "Go..." button made zero difference to the row
    ...    count, same behaviour as Report Context/WBS/Calendar/Account.
    Open EC Screen    ${COMPANY_SPLIT_KEY_SCREEN}

Insert Company Split Key Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties
    ...    And Verify Code, so company_split_key_iud.robot's test case body reads as a plain
    ...    business step with ZERO arguments. Also checks the inserted Code matches the
    ...    suite's ${TEST_CODE}. Pre-save evidence screenshot captured before Save is clicked,
    ...    matching Bank/WBS/Report Context.
    [Arguments]    ${properties_path}=${COMPANY_SPLIT_KEY_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Split Key Code
    RETURN    ${code}

Verify Company Split Key Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (no DB check here, matching Bank/WBS/Report Context's TC02
    ...    convention): row exists in the grid, then the form shows what was just inserted
    ...    (Split Key Code/Split Key Name only - Start Date is grid/insert-only, not present
    ...    in updateAttributes). Delegates the full sequence (row-check, select,
    ...    form-compare, screenshot) to the shared T2 Verify Object Insert Exists. Filters via
    ...    Find Company Split Key Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Company Split Key Row By Filter    ${code}
    Verify Object Insert Exists    ${COMPANY_SPLIT_KEY_TABLE}    ${code}    Company Split Key
    ...    ${COMPANY_SPLIT_KEY_INSERT_PROPERTIES}    @{COMPANY_SPLIT_KEY_FORM_LABELS}
    ...    code_label=Split Key Code
    Clear Company Split Key Row Filter

Update Company Split Key Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Pre-save evidence screenshot captured before Save is clicked, matching
    ...    Bank/WBS/Report Context. Filters via Find Company Split Key Row By Filter first,
    ...    clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${COMPANY_SPLIT_KEY_UPDATE_PROPERTIES}
    Find Company Split Key Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${COMPANY_SPLIT_KEY_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Split Key Code
    Clear Company Split Key Row Filter
    RETURN    ${data}

Verify Company Split Key Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification, matching Bank/WBS/Report Context's TC03 convention: the form shows
    ...    the updated Split Key Name. Delegates the full sequence (select, form-compare,
    ...    screenshot) to the shared T2 Verify Object Form Record. Filters via Find Company
    ...    Split Key Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Company Split Key Row By Filter    ${code}
    Verify Object Form Record    ${COMPANY_SPLIT_KEY_TABLE}    ${code}    Company Split Key
    ...    ${COMPANY_SPLIT_KEY_UPDATE_PROPERTIES}    Split Key Name
    ...    code_label=Split Key Code
    Clear Company Split Key Row Filter

Find Company Split Key Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Delegates the full select+capture sequence. Calls Find Company Split Key Row By
    ...    Filter first. Deliberately does NOT clear the filter afterward - Verify Company
    ...    Split Key Record Found (called right after, same TC) needs the grid still filtered
    ...    to ${code} for its own grid-check, since it doesn't re-select the row itself; it
    ...    clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Company Split Key Row By Filter    ${code}
    Find Object Record    ${COMPANY_SPLIT_KEY_TABLE}    ${code}    Company Split Key
    ...    code_label=Split Key Code

Verify Company Split Key Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the form record match the expected (post-update) data. Delegates the full
    ...    sequence (grid-compare, form-compare, screenshot) to the shared T2 Verify Object
    ...    Found. Caller must already have selected the row (TC04 does, via Find Company
    ...    Split Key Record before this) AND left the Code filter active from that same call -
    ...    clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${COMPANY_SPLIT_KEY_TABLE}    ${code}    ${COMPANY_SPLIT_KEY_GRID_VERIFY_PROPERTIES}
    ...    ${COMPANY_SPLIT_KEY_FORM_VERIFY_PROPERTIES}    @{COMPANY_SPLIT_KEY_FORM_LABELS}
    Clear Company Split Key Row Filter

Delete Company Split Key Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date,
    ...    called with ZERO arguments (defaults ${code}/${date} to the suite's
    ...    ${TEST_CODE}/${END_DATE}). Select the Company Split Key record, set End Date =
    ...    Start Date (true delete), Save. Captures the TC05 evidence screenshot right after
    ...    the End Date is filled but BEFORE Save is clicked, matching Bank/WBS/Report
    ...    Context. Filters via Find Company Split Key Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Company Split Key Row By Filter    ${code}
    Delete Object Via End Date    ${COMPANY_SPLIT_KEY_TABLE}    ${COMPANY_SPLIT_KEY_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Company Split Key Row Filter

Verify Company Split Key Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is
    ...    absent from BOTH the grid and the database (OV_SPLIT_KEY, scoped by Code - the
    ...    same shared view all 6 Split Key siblings write to, so this check is specific to
    ...    THIS test code only, never a blanket "no Split Key rows" check).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${COMPANY_SPLIT_KEY_TABLE}    OV_SPLIT_KEY    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Company Split Key Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to
    ...    the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${COMPANY_SPLIT_KEY_TABLE}    ${code}
