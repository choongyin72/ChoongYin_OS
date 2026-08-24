*** Settings ***
Documentation       T3 (screen) — Payment Term page object.
...                 Screen: Configuration > Assets > Date Objects > Payment Term (CD.0023).
...                 Manage-Object (OV, date-effective) screen. Holds Payment Term's locators + thin
...                 IUD wrappers that delegate to T2 (manage_object) and T1 (common). Navigator is
...                 a single Date field (pre-filled with today's date) + GO - same "date nav + GO
...                 to load" shape as Berth/Port (docs/ec_screen_registry.md), NOT a genuine
...                 mandatory gate: confirmed via the screen's own proven Playwright driver
...                 (screens/.../Payment_Term/playwright/ec_iud_payment_term.py) and its live
...                 evidence screenshot (evidence/pt_01_loaded.png), which both check/act on the
...                 grid immediately after Open EC Screen with NO Apply Navigator call first -
...                 the grid auto-populates on open, exactly like Bank/Berth/Port.
...                 Richer than Bank: the New-Object form has two extra mandatory inputs beyond
...                 the universal Code/Name/Start-Date trio - a "Date Calculation Method"
...                 autocomplete dropdown and a mandatory numeric "Number Of Days" cell (labels
...                 confirmed live via evidence/pt_04_insert_filled.png - NOT "Method"/"Offset" as
...                 the driver's own internal variable names might suggest).
...                 Converted to the full Bank-pattern shape (2026-08-24): was previously an OLD
...                 hardcoded-field-id build (Fill New Object Form with raw R:n:C:n ids, one
...                 shared Suite Setup login, 4 TCs/no Find). Now matches bank_page.resource/
...                 berth_page.resource exactly: properties-file-driven insert/update/verify,
...                 explicit grid-filter wiring, fixed test code, per-TC Login/Logout, 5 TCs,
...                 PURE SCREEN verification (no inline DB-verify in the T3/test file).
...                 DELETE = End Date = Start Date (true delete; row leaves OV_PAYMENT_TERM).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${PT_SCREEN}            Payment Term
${PT_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/payment_term_insert.properties
${PT_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/payment_term_update.properties
${PT_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/payment_term_form_verify.properties
${PT_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/payment_term_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal
# string (manage_object.resource defines this ONCE specifically so no T3 duplicates it).
${PT_TABLE}             ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date). Hardcoded deliberately, NOT label-driven
# — same documented precedent as Bank's own BANK_DEL_ENDDATE (the objectdates row packs TWO fields,
# Start Date C:1 / End Date C:3, a shape the one-field-per-row label scan cannot safely resolve).
# Confirmed live by the proven Playwright driver (DEL_ENDDATE_ID, results.json delete=PASS).
${PT_DEL_ENDDATE}       tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Payment Term's own form-field label set (Start Date deliberately excluded - it lives only in
# objectForm/objectdates, not updateAttributes, same exclusion Bank/Disposition Type document for
# their own Start Date). Labels are a MIX: "Payment Term Code" is screen-prefixed, but "Name" is
# the GENERIC label Bank also uses (confirmed live via evidence/pt_04_insert_filled.png -
# pt_07_update_filled.png confirms Date Calculation Method/Number Of Days also live inside
# updateAttributes, alongside Name). Defined ONCE here so both Verify Payment Term Record Exists
# (TC02) and Verify Payment Term Record Found (TC04) share the same list.
@{PT_FORM_LABELS}    Payment Term Code    Name    Date Calculation Method    Number Of Days


*** Keywords ***
Find Payment Term Row By Filter
    [Documentation]    Explicitly filter the Payment Term grid's Code column to ${code} via the
    ...    shared T2 Find Object Row By Filter (resources/manage_object.resource) - matches
    ...    Bank's/Disposition Type's own explicit filter usage, rather than relying only on
    ...    Select Object Row's implicit 3s-timeout fallback. Payment Term's grid is paginated (5
    ...    pages at recon time, confirmed via evidence/pt_04_insert_filled.png) so this matters
    ...    more here than on a single-page grid.
    [Arguments]    ${code}
    Find Object Row By Filter    ${PT_TABLE}    ${code}

Clear Payment Term Row Filter
    [Documentation]    Clear the Code column filter (see Find Payment Term Row By Filter) via the
    ...    shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${PT_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Payment Term's OWN credentials
    ...    (${PAYMENT_TERM_EC_USER}/${PAYMENT_TERM_EC_PASS} from credentials.py) on the current
    ...    page - works whether this is the very first login (page freshly loaded on the login
    ...    form via the shared T1 Open EC Application) or a re-login after Logout From EC
    ...    Application (same login form, not a new page/tab). Screen-specific wrapper (matches
    ...    Bank's convention: payment_term_iud.robot's test cases call this with ZERO arguments)
    ...    that supplies Payment Term's own credential defaults to the shared T1 Login To EC
    ...    Screen (common.resource), which owns the actual login mechanics.
    Login To EC Screen    ${PAYMENT_TERM_EC_USER}    ${PAYMENT_TERM_EC_PASS}

Open Payment Term Screen
    [Documentation]    Navigate to the Payment Term screen. Assumes the caller already logged in
    ...    this test case (via Login To EC Application) - this keyword ONLY navigates, matching
    ...    Bank's per-TC Login/Open/action/Logout convention. Deliberately does NOT call Apply
    ...    Navigator - the grid auto-populates on open (confirmed live: the proven Playwright
    ...    driver checks/acts on the grid immediately after opening the screen, with no GO click
    ...    first - same as Bank/Berth/Port).
    Open EC Screen    ${PT_SCREEN}

Insert Payment Term Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Object From Properties And Verify
    ...    Code, purely so payment_term_iud.robot's test case body reads as a plain business step
    ...    with ZERO arguments - the underlying mechanics (properties-file-driven insert) are
    ...    UNCHANGED. Also owns the integrity check that the inserted Code matches the suite's
    ...    ${TEST_CODE}. The TC02 evidence screenshot is captured BEFORE Save is clicked (passed
    ...    through to Insert Object From Properties, which fills every field first).
    [Arguments]    ${properties_path}=${PT_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Payment Term Code
    RETURN    ${code}

Verify Payment Term Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification: row
    ...    exists in the grid, then every field's LIVE SCREEN value (via Get OV Field Value By
    ...    Label) is compared to testdata/payment_term_insert.properties (the file used to insert,
    ...    not the post-update payment_term_form_verify.properties) - Payment Term Code, Name,
    ...    Date Calculation Method, Number Of Days (${PT_FORM_LABELS}). NOTE: Start Date is NOT
    ...    verified here - it only exists as a grid column / objectForm-objectdates field, not an
    ...    updateAttributes field (matches Bank's own convention). Delegates the full sequence
    ...    (row-check, select, form-compare, screenshot) to the shared T2 Verify Object Insert
    ...    Exists. Filters via Find Payment Term Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Payment Term Row By Filter    ${code}
    Verify Object Insert Exists    ${PT_TABLE}    ${code}    Payment Term
    ...    ${PT_INSERT_PROPERTIES}    @{PT_FORM_LABELS}    code_label=Payment Term Code
    Clear Payment Term Row Filter

Update Payment Term Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Returns the
    ...    applied {label: value} dict so the caller can DB-verify against exactly what was set.
    ...    The TC03 evidence screenshot is captured BEFORE Save is clicked (passed through to
    ...    Update Object From Properties, which fills every field first). Filters via Find Payment
    ...    Term Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${PT_UPDATE_PROPERTIES}
    Find Payment Term Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${PT_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Payment Term Code
    Clear Payment Term Row Filter
    RETURN    ${data}

Verify Payment Term Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification:
    ...    selects the row (loading updateAttributes), then compares Name's LIVE SCREEN value (via
    ...    Get OV Field Value By Label) to testdata/payment_term_update.properties - only that one
    ...    label, since that's the only field that file has. Delegates the full sequence (select,
    ...    form-compare, screenshot) to the shared T2 Verify Object Form Record. Filters via Find
    ...    Payment Term Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Payment Term Row By Filter    ${code}
    Verify Object Form Record    ${PT_TABLE}    ${code}    Payment Term
    ...    ${PT_UPDATE_PROPERTIES}    Name    code_label=Payment Term Code
    Clear Payment Term Row Filter

Find Payment Term Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates the full
    ...    select+capture sequence. Calls Find Payment Term Row By Filter first. Deliberately does
    ...    NOT clear the filter afterward - Verify Payment Term Record Found (called right after,
    ...    same TC) needs the grid still filtered to ${code} for its own grid-check, since it
    ...    doesn't re-select the row itself; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Payment Term Row By Filter    ${code}
    Find Object Record    ${PT_TABLE}    ${code}    Payment Term    code_label=Payment Term Code

Verify Payment Term Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND
    ...    the full form record match the expected data - the SAME two existing live-DOM
    ...    round-trip keywords, just called under one name. Also captures the TC04 evidence
    ...    screenshot. Delegates the full sequence (grid-compare, form-compare, screenshot) to the
    ...    shared T2 Verify Object Found. Caller must already have selected the row (TC04 does,
    ...    via Find Payment Term Record before this) AND left the Code filter active from that
    ...    same call - clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${PT_TABLE}    ${code}    ${PT_GRID_VERIFY_PROPERTIES}
    ...    ${PT_FORM_VERIFY_PROPERTIES}    @{PT_FORM_LABELS}
    Clear Payment Term Row Filter

Delete Payment Term Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the payment term, set End Date = Start Date (true delete), Save. Captures the
    ...    TC05 evidence screenshot right after the End Date is filled but BEFORE Save is clicked -
    ...    showing the data as entered, not the after-save/reloaded-grid state. Filters via Find
    ...    Payment Term Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Payment Term Row By Filter    ${code}
    Delete Object Via End Date    ${PT_TABLE}    ${PT_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Payment Term Row Filter

Verify Payment Term Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid and the database - the SAME two existing DB-ground-truth keywords,
    ...    just called under one name. Also captures the TC05 evidence screenshot.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${PT_TABLE}    OV_PAYMENT_TERM    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Payment Term Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to the shared
    ...    T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${PT_TABLE}    ${code}
