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


*** Keywords ***
Login To EC Application
    [Documentation]    Authenticate as Bank's OWN credentials (${BANK_EC_USER}/${BANK_EC_PASS}
    ...    from credentials.py) on the current page - works whether this is the very first login
    ...    (page freshly loaded on the login form via the shared T1 Open EC Application) or a
    ...    re-login after Logout From EC Application (same login form, not a new page/tab).
    ...    Screen-specific wrapper (owner-requested 2026-08-18: bank_iud.robot's test cases call
    ...    this with ZERO arguments) that calls the shared T1 Fill EC Login Form for the actual
    ...    login mechanics - kept here only to supply Bank's own credential defaults, which a
    ...    shared file should not hardcode. A future login-flow change (SSO/MFA/renamed field id)
    ...    is a one-place edit to Fill EC Login Form, not a per-screen duplicate fix.
    Fill EC Login Form    ${BANK_EC_USER}    ${BANK_EC_PASS}
    Capture Step    ${TEST NAME}_login

Open Bank Screen
    [Documentation]    Navigate to the Bank screen. Assumes the caller already logged in this
    ...    test case (via Login To EC Application) - this keyword ONLY navigates, it no longer
    ...    bundles launch+login (owner-requested 2026-08-18, so every test case gets its own
    ...    explicit Login/Logout step instead of one shared Suite Setup/Teardown login).
    Navigate To Screen    ${BANK_SCREEN}
    Capture Step    ${TEST NAME}_open_screen

Bank Row Should Exist
    [Documentation]    Assert a bank with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${BANK_TABLE}    ${code}

Bank Row Should Not Exist
    [Documentation]    Assert a bank with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${BANK_TABLE}    ${code}

Bank Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in ov_bank.
    [Arguments]    ${code}
    Code Should Be Present In View    ov_bank    ${code}

Bank Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from ov_bank.
    [Arguments]    ${code}
    Code Should Be Absent In View    ov_bank    ${code}

Bank Description Should Equal In DB
    [Documentation]    DB ground-truth: assert ${code}'s DESCRIPTION column equals ${description}
    ...    in ov_bank. Column name + value match the already-proven Python driver
    ...    (py/bank_iud.py: DESC="AUTOTEST desc", DB-verified against ov_bank.DESCRIPTION).
    [Arguments]    ${code}    ${description}
    Field Should Equal In View    ov_bank    ${code}    DESCRIPTION    ${description}

Bank Field Should Equal In DB
    [Documentation]    DB ground-truth: assert ${code}'s ${column} equals ${expected} in ov_bank.
    ...    Generic wrapper for verifying any ov_bank column - real column names confirmed live
    ...    (2026-08-17): ADDRESS_1..ADDRESS_8, BANK_SWIFT_CODE, COUNTRY_CODE, DESCRIPTION,
    ...    COMMENTS. "Address Line 1"/"Swift Code" are the FORM labels, not the column names.
    [Arguments]    ${code}    ${column}    ${expected}
    Field Should Equal In View    ov_bank    ${code}    ${column}    ${expected}

Bank Fields Should Equal In DB
    [Documentation]    DB ground-truth: assert MULTIPLE ov_bank columns in ONE call, instead of
    ...    one "Bank Field Should Equal In DB" line per column. Pass columns as named arguments,
    ...    e.g.: Bank Fields Should Equal In DB    ${TEST_CODE}    DESCRIPTION=${OBJ_DESC}
    ...    ...    ADDRESS_1=${OBJ_ADDR1}    BANK_SWIFT_CODE=${OBJ_SWIFT}
    [Arguments]    ${code}    &{columns}
    FOR    ${column}    ${expected}    IN    &{columns}
        Bank Field Should Equal In DB    ${code}    ${column}    ${expected}
    END

Bank Row Should Show Name
    [Documentation]    Assert the Bank row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    ${row}=    Get Text    xpath=//tbody[@id='${BANK_TABLE}']//tr[.//span[normalize-space(text())='${code}']]
    Should Contain    ${row}    ${name}    msg=Bank row ${code} does not show name ${name}

Insert Bank Record
    [Documentation]    Insert a new bank: New Object form -> Code/Name/Start Date/Description ->
    ...    Save. Fields resolved BY LABEL (not a hardcoded R:n:C:n id) - robust to a form-layout
    ...    shift, matching manage_object.resource's documented label-driven convention.
    ...    Description is optional on this screen but included here to match the already-proven
    ...    Python driver's own field coverage (py/bank_iud.py INSERT_FIELDS).
    ...    SUPERSEDED for TC02 by "Insert Bank From Properties" (data-driven, owner-requested
    ...    2026-08-17) - kept here as a working fallback, not deleted, in case that needs
    ...    reverting quickly.
    [Arguments]    ${code}    ${name}    ${start_date}    ${description}=${EMPTY}
    Open New Object Form
    Fill OV Field By Label    objectForm    Code    ${code}
    Fill OV Field By Label    objectForm    Name    ${name}
    Fill OV Date By Label    objectForm    Start Date    ${start_date}
    IF    '${description}' != ''
        Fill OV Field By Label    objectForm    Description    ${description}
    END
    Save
    Apply Navigator

Insert Bank From Properties
    [Documentation]    Insert a new bank by reading EVERY column=value entry from
    ...    ${BANK_INSERT_PROPERTIES} (testdata/bank_insert.properties) and filling each field by
    ...    label, auto-detecting its kind (text/date/dropdown/popup) live - so the fields filled
    ...    and their values live entirely in the properties file, not in this keyword or the
    ...    suite. Returns the Code that was inserted (read back from the properties file).
    [Arguments]    ${properties_path}=${BANK_INSERT_PROPERTIES}    ${pre_save_screenshot}=${EMPTY}
    ${code}=    Insert Object From Properties    ${properties_path}    ${pre_save_screenshot}
    RETURN    ${code}

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
    ...    PURE SCREEN verification (owner-requested 2026-08-18: no DB check at all here), reusing
    ...    the SAME existing keyword TC04 already uses for its form check - just pointed at
    ...    testdata/bank_insert.properties (the file used to insert) instead of its own default
    ...    bank_form_verify.properties, since that represents the state AFTER TC03's update, not
    ...    the just-inserted state:
    ...    1. Bank Row Should Exist - the grid shows the row.
    ...    2. Find Bank - selects the row, loading updateAttributes.
    ...    3. Bank Form Should Match Properties - compares every field's LIVE SCREEN value (via
    ...       Get OV Field Value By Label) to the properties file: Code, Name, Description, Swift
    ...       Code, Address Line 1-3, Country. Country is screen-compared deliberately, not
    ...       DB-compared - a live recon (2026-08-18) proved the DB stores an internal code (e.g.
    ...       COUNTRY_CODE 'NL' for an existing Netherlands record), not the display text the
    ...       properties file and the screen both show.
    ...    NOTE (owner-decided 2026-08-18): Start Date is NOT verified anywhere in this keyword -
    ...    it only exists as a grid column, not a form field, and the grid-level check (Bank Row
    ...    Should Match Properties) was deliberately dropped here.
    ...    Also captures the TC02 evidence screenshot (Capture Step - evidence capture, not a
    ...    business step, excluded from the friendly report same as elsewhere).
    [Arguments]    ${code}=${TEST_CODE}
    Bank Row Should Exist    ${code}
    Find Bank    ${code}
    Bank Form Should Match Properties    ${BANK_INSERT_PROPERTIES}
    Capture Step    ${TEST NAME}_verify

Update Bank Name
    [Documentation]    Select the bank, confirm it loaded, edit Name, Save. The Code field
    ...    is resolved BY LABEL each call (not a hardcoded id) so a row-load check never
    ...    silently reads the wrong field if the update form's layout ever shifts.
    ...    NOT called by TC03 currently (TC03 uses "Update Bank From Properties") - kept as a
    ...    working, narrower option. Owner flagged 2026-08-18 that its NAME is questionable
    ...    (a real OV_BANK update covers more than just Name) - restored 2026-08-18 after being
    ...    wrongly deleted on an assumption; owner has not said to remove or rename it, so it
    ...    stays exactly as it was until told otherwise.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${BANK_TABLE}    ${code}
    ${code_id}=    OV Field Id By Label    updateAttributes    Code
    ${loaded}=    Get Property    css=[id="${code_id}"]    value
    Should Be Equal    ${loaded}    ${code}    msg=Row select failed - code not loaded
    Fill OV Field By Label    updateAttributes    Name    ${new_name}
    Save
    Apply Navigator

Update Bank From Properties
    [Documentation]    Update the bank identified by ${code} by reading EVERY column=value entry
    ...    from ${properties_path} (testdata/bank_update.properties) and filling each field by
    ...    label into updateAttributes, auto-detecting its kind - so the fields updated and their
    ...    new values live entirely in the properties file, not in this keyword or the suite.
    ...    Row-identity is verified (Code read back) before anything is written, same safeguard
    ...    as Update Bank Name. Returns the applied {label: value} dict so the caller can DB-verify
    ...    against exactly what was set, without duplicating the values as separate suite variables.
    [Arguments]    ${code}    ${properties_path}=${BANK_UPDATE_PROPERTIES}    ${pre_save_screenshot}=${EMPTY}
    ${data}=    Update Object From Properties    ${BANK_TABLE}    ${code}    ${properties_path}
    ...    ${pre_save_screenshot}
    RETURN    ${data}

Update Bank Record And Save
    [Documentation]    Friendly-narrative wrapper (owner-requested 2026-08-18) around Update Bank
    ...    From Properties, called with ZERO arguments (defaults ${code} to the suite's
    ...    ${TEST_CODE}) - underlying mechanics UNCHANGED. Returns the applied {label: value}
    ...    dict, same as Update Bank From Properties. The TC03 evidence screenshot is captured
    ...    BEFORE Save is clicked (owner-requested 2026-08-18 - passed through to Update Object
    ...    From Properties, which fills every field first).
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${BANK_UPDATE_PROPERTIES}
    ${data}=    Update Object From Properties    ${BANK_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action
    RETURN    ${data}

Verify Bank Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments (owner-requested 2026-08-18): defaults ${code} to the suite's ${TEST_CODE}.
    ...    PURE SCREEN verification (owner-requested 2026-08-18: no DB check), matching TC02's
    ...    pattern - reuses the SAME existing keyword (Bank Form Should Match Properties), pointed
    ...    at testdata/bank_update.properties (the file used to update) with an explicit label
    ...    override of just Name/Description, since that's the only fields that file has (unlike
    ...    the default bank_form_verify.properties, which has the full field set):
    ...    1. Find Bank - selects the row, loading updateAttributes.
    ...    2. Bank Form Should Match Properties - compares Name/Description's LIVE SCREEN value
    ...       (via Get OV Field Value By Label) to testdata/bank_update.properties.
    ...    Also captures the TC03 evidence screenshot (moved in from the test case's own Capture
    ...    Step line).
    [Arguments]    ${code}=${TEST_CODE}
    Find Bank    ${code}
    Bank Form Should Match Properties    ${BANK_UPDATE_PROPERTIES}    Name    Description
    Capture Step    ${TEST NAME}_verify

Find Bank
    [Documentation]    Locate the bank row by ${code} and select it (loads updateAttributes),
    ...    verifying row-identity (Code read back) before returning - so a caller can then safely
    ...    read/verify its form fields. Same row-identity safeguard as Update Bank From Properties.
    [Arguments]    ${code}
    Find Object By Code    ${BANK_TABLE}    ${code}    Bank

Find Bank Record
    [Documentation]    Friendly-narrative wrapper (owner-requested 2026-08-18) around Find Bank,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}) - underlying
    ...    mechanics (select + row-identity check) UNCHANGED.
    [Arguments]    ${code}=${TEST_CODE}
    Find Bank    ${code}
    Capture Step    ${TEST NAME}_action

Bank Row Should Match Properties
    [Documentation]    Assert the grid row for ${code} shows Code/Name/Start Date matching
    ...    ${properties_path} (testdata/bank_grid_verify.properties by default - its OWN dedicated
    ...    file, owner-requested 2026-08-18, since the grid genuinely shows fewer columns than the
    ...    form record). If @{labels} is given, ONLY those labels are checked against the grid -
    ...    needed when ${properties_path} is a FULLER file (e.g. bank_insert.properties, which also
    ...    has Description/Swift Code/etc. that are never shown in the grid and would always fail
    ...    here); if omitted, every key in the file is checked (correct when the file is already
    ...    grid-only, like bank_grid_verify.properties).
    [Arguments]    ${code}    ${properties_path}=${BANK_GRID_VERIFY_PROPERTIES}    @{labels}
    Verify Object Row Fields From Properties    ${BANK_TABLE}    ${code}    ${properties_path}
    ...    @{labels}

Bank Form Should Match Properties
    [Documentation]    Assert fields shows the expected value live in the updateAttributes form -
    ...    a round-trip UI check reading straight off the screen. Caller must already have
    ...    selected the row (e.g. via Find Bank) before calling this.
    ...    If @{labels} is given, ONLY those labels are checked (needed when ${properties_path} is
    ...    a SMALLER file than the default - e.g. testdata/bank_update.properties only has
    ...    Name/Description, so checking the full default label set against it would error looking
    ...    up keys that file doesn't have). If omitted, defaults to Code/Name/Description/Swift
    ...    Code/Address Line 1-3/Country (the full field set, correct for the default
    ...    testdata/bank_form_verify.properties). "Start Date" is never included by default - the
    ...    live field-inventory scan (2026-08-17) confirmed updateAttributes has no Start Date
    ...    field (it lives only in objectdates); Bank Row Should Match Properties covers it via the
    ...    grid instead, where applicable.
    [Arguments]    ${properties_path}=${BANK_FORM_VERIFY_PROPERTIES}    @{labels}
    ${default_labels}=    Create List    Code    Name    Description    Swift Code
    ...    Address Line 1    Address Line 2    Address Line 3    Country
    ${use_labels}=    Set Variable If    ${labels}    ${labels}    ${default_labels}
    Verify Object Form Fields From Properties    updateAttributes    ${properties_path}
    ...    @{use_labels}

Verify Bank Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}, owner-requested 2026-08-18):
    ...    confirms BOTH the grid AND the full form record match the expected data - the SAME two
    ...    existing live-DOM round-trip keywords, just called under one name. Also captures the
    ...    TC04 evidence screenshot (moved in from the test case's own Capture Step line).
    [Arguments]    ${code}=${TEST_CODE}
    Bank Row Should Match Properties    ${code}
    Bank Form Should Match Properties
    Capture Step    ${TEST NAME}_verify

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
    ...    2026-08-18) - underlying mechanics (Bank Row Should Not Exist) UNCHANGED. Also captures
    ...    the TC01 evidence screenshot (moved in from the test case's own Capture Step line).
    [Arguments]    ${code}=${TEST_CODE}
    Bank Row Should Not Exist    ${code}
    Capture Step    ${TEST NAME}_verify
