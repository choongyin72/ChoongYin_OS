*** Settings ***
Documentation       T3 (screen) — Bank page object.
...                 Screen: Configuration > Assets > Financial Objects > Bank.
...                 Manage-Object (OV) screen. Holds Bank's locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${BANK_SCREEN}          Bank
${BANK_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/bank_insert.properties
${BANK_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/bank_update.properties
${BANK_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/bank_form_verify.properties
${BANK_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/bank_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal
# string (manage_object.resource defines this ONCE specifically so no T3 duplicates it).
${BANK_TABLE}           ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date). Hardcoded deliberately, NOT
# label-driven: the proven Python driver (py/ec_object_iud.py END_DATE_ID) documents that
# this row packs TWO fields (Start Date C:1, End Date C:3) with the End Date label at C:2 -
# a shape the one-field-per-row label scan cannot safely resolve. TO BE LIVE-VERIFIED
# (2026-08-17) whether OV Field Id By Label's following-sibling lookup agrees with this
# value before relying on it generally - left hardcoded here regardless, matching the
# documented, already-proven precedent rather than a claim not yet checked.
${BANK_DEL_ENDDATE}     tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Bank's own form-field label set (Start Date/End Date deliberately excluded - they live only in
# objectdates, not updateAttributes). Defined ONCE here so both Verify Bank Record Exists (TC02,
# against bank_insert.properties) and Verify Bank Record Found (TC04, against
# bank_form_verify.properties) share the same list instead of each hardcoding it inline
# (owner-requested 2026-08-22 consolidation of the T2 Verify Object Insert Exists/Found calls).
@{BANK_FORM_LABELS}    Code    Name    Description    Swift Code    Address Line 1
...    Address Line 2    Address Line 3    Country


*** Keywords ***
Login To EC Application
    [Documentation]    Authenticate as Bank's OWN credentials (${BANK_EC_USER}/${BANK_EC_PASS}
    ...    from credentials.py) on the current page - works whether this is the very first login
    ...    (page freshly loaded on the login form via the shared T1 Open EC Application) or a
    ...    re-login after Logout From EC Application (same login form, not a new page/tab).
    ...    Screen-specific wrapper (owner-requested 2026-08-18: bank_iud.robot's test cases call
    ...    this with ZERO arguments) that supplies Bank's own credential defaults to the shared
    ...    T1 Login To EC Screen (common.resource), which owns the actual login mechanics - kept
    ...    here only because a shared file should not hardcode any screen's credentials.
    Login To EC Screen    ${BANK_EC_USER}    ${BANK_EC_PASS}

Open Bank Screen
    [Documentation]    Navigate to the Bank screen. Assumes the caller already logged in this
    ...    test case (via Login To EC Application) - this keyword ONLY navigates, it no longer
    ...    bundles launch+login (owner-requested 2026-08-18, so every test case gets its own
    ...    explicit Login/Logout step instead of one shared Suite Setup/Teardown login).
    ...    Delegates to the shared T1 Open EC Screen (common.resource) for the actual mechanics.
    Open EC Screen    ${BANK_SCREEN}

Insert Bank Record And Save
    [Documentation]    Friendly-narrative wrapper (owner-requested 2026-08-18) around Insert Bank
    ...    From Properties, purely so bank_iud.robot's test case body reads as a plain business
    ...    step with ZERO arguments - the underlying mechanics (properties-file-driven insert) are
    ...    UNCHANGED. Also owns the integrity check that the inserted Code matches the suite's
    ...    ${TEST_CODE} (moved in from the test case, owner-requested 2026-08-18) - this keyword
    ...    fails on its own if testdata/bank_insert.properties' Code ever drifts out of sync with
    ...    the suite variable, instead of the test case asserting it separately. The TC02 evidence
    ...    screenshot is captured BEFORE Save is clicked (owner-requested 2026-08-18 - passed
    ...    through to Insert Object From Properties, which fills every field first).
    [Arguments]    ${properties_path}=${BANK_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action
    RETURN    ${code}

Verify Bank Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments (owner-requested 2026-08-18): defaults ${code} to the suite's ${TEST_CODE}.
    ...    PURE SCREEN verification (owner-requested 2026-08-18: no DB check at all here): row
    ...    exists in the grid, then every field's LIVE SCREEN value (via Get OV Field Value By
    ...    Label) is compared to testdata/bank_insert.properties (the file used to insert, not
    ...    the post-update bank_form_verify.properties) - Code, Name, Description, Swift Code,
    ...    Address Line 1-3, Country (${BANK_FORM_LABELS}). Country is screen-compared
    ...    deliberately, not DB-compared - a live recon (2026-08-18) proved the DB stores an
    ...    internal code (e.g. COUNTRY_CODE 'NL' for an existing Netherlands record), not the
    ...    display text the properties file and the screen both show.
    ...    NOTE (owner-decided 2026-08-18): Start Date is NOT verified anywhere in this keyword -
    ...    it only exists as a grid column, not a form field.
    ...    Delegates the full sequence (row-check, select, form-compare, screenshot) to the
    ...    shared T2 Verify Object Insert Exists (owner-requested 2026-08-22 consolidation).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Insert Exists    ${BANK_TABLE}    ${code}    Bank    ${BANK_INSERT_PROPERTIES}
    ...    @{BANK_FORM_LABELS}

Update Bank Record And Save
    [Documentation]    Friendly-narrative wrapper (owner-requested 2026-08-18) around T2's Update
    ...    Object From Properties, called with ZERO arguments (defaults ${code} to the suite's
    ...    ${TEST_CODE}). Returns the applied {label: value} dict so the caller can DB-verify
    ...    against exactly what was set. The TC03 evidence screenshot is captured BEFORE Save is
    ...    clicked (owner-requested 2026-08-18 - passed through to Update Object From Properties,
    ...    which fills every field first).
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${BANK_UPDATE_PROPERTIES}
    ${data}=    Update Object From Properties    ${BANK_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action
    RETURN    ${data}

Verify Bank Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments (owner-requested 2026-08-18): defaults ${code} to the suite's ${TEST_CODE}.
    ...    PURE SCREEN verification (owner-requested 2026-08-18: no DB check): selects the row
    ...    (loading updateAttributes), then compares Name/Description's LIVE SCREEN value (via
    ...    Get OV Field Value By Label) to testdata/bank_update.properties - only those two
    ...    labels, since that's the only fields that file has (unlike the default
    ...    bank_form_verify.properties/${BANK_FORM_LABELS}, which has the full field set).
    ...    Delegates the full sequence (select, form-compare, screenshot) to the shared T2
    ...    Verify Object Form Record (owner-requested 2026-08-22 consolidation).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Form Record    ${BANK_TABLE}    ${code}    Bank    ${BANK_UPDATE_PROPERTIES}
    ...    Name    Description

Find Bank
    [Documentation]    Locate the bank row by ${code} and select it (loads updateAttributes),
    ...    verifying row-identity (Code read back) before returning - so a caller can then safely
    ...    read/verify its form fields. Same row-identity safeguard as T2's Update Object From
    ...    Properties.
    [Arguments]    ${code}
    Find Object By Code    ${BANK_TABLE}    ${code}    Bank

Find Bank Record
    [Documentation]    Friendly-narrative wrapper (owner-requested 2026-08-18) around Find Bank,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}) - underlying
    ...    mechanics (select + row-identity check) UNCHANGED.
    [Arguments]    ${code}=${TEST_CODE}
    Find Bank    ${code}
    Capture Step    ${TEST NAME}_action

Verify Bank Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}, owner-requested 2026-08-18):
    ...    confirms BOTH the grid AND the full form record match the expected data - the SAME two
    ...    existing live-DOM round-trip keywords, just called under one name. Also captures the
    ...    TC04 evidence screenshot (moved in from the test case's own Capture Step line).
    ...    Delegates the full sequence (grid-compare, form-compare, screenshot) to the shared
    ...    T2 Verify Object Found (owner-requested 2026-08-22 consolidation). Caller must
    ...    already have selected the row (TC04 does, via Find Bank Record before this).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${BANK_TABLE}    ${code}    ${BANK_GRID_VERIFY_PROPERTIES}
    ...    ${BANK_FORM_VERIFY_PROPERTIES}    @{BANK_FORM_LABELS}

Delete Bank
    [Documentation]    Select the bank, set End Date = Start Date (true delete), Save.
    ...    Captures the TC05 evidence screenshot right after the End Date is filled but
    ...    BEFORE Save is clicked (owner-requested 2026-08-18) - showing the data as entered,
    ...    not the after-save/reloaded-grid state.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${BANK_TABLE}    ${BANK_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action

Delete Bank Record And Save
    [Documentation]    Friendly-narrative wrapper (owner-requested 2026-08-18) around Delete Bank,
    ...    called with ZERO arguments (defaults ${code}/${date} to the suite's
    ...    ${TEST_CODE}/${END_DATE}) - underlying mechanics (End Date = Start Date true delete)
    ...    UNCHANGED.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Delete Bank    ${code}    ${date}

Verify Bank Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}, owner-requested 2026-08-18):
    ...    confirms ${code} is absent from BOTH the grid AND the database - the SAME two existing
    ...    DB-ground-truth keywords, just called under one name. Also captures the TC05 evidence
    ...    screenshot (moved in from the test case's own Capture Step line).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${BANK_TABLE}    ov_bank    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Bank Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}, owner-requested
    ...    2026-08-18). Delegates to the shared T2 Verify Object Does Not Exist (owner-requested
    ...    2026-08-22 consolidation).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${BANK_TABLE}    ${code}
