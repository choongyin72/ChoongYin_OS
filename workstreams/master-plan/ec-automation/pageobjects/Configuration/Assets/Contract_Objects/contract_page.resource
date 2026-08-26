*** Settings ***
Documentation       T3 (screen) — Contract page object.
...                 Screen: Configuration > Assets > Contract_Objects > Contract.
...                 OV-GM (groupmodel manage-object) screen: the grid loads ONLY after the
...                 mandatory Business Unit navigator dropdown is set + GO. Converted to the
...                 Area-pattern 5-TC/per-TC-login/pure-screen-verify STRUCTURE (2026-08-26)
...                 while KEEPING this genuine navigator gesture - Contract is still OV-GM, not
...                 plain Bank-shaped; the Business Unit+GO step is real and required, not
...                 something this conversion removed. Real labels reused as-is from the
...                 screen's own prior driver (contract_page.resource pre-conversion / py/
...                 contract_iud.py): objectForm/updateAttributes use SCREEN-PREFIXED
...                 "Contract Code"/"Contract Name" - every T2 call below passes
...                 code_label=Contract Code accordingly. Business Unit value = "TS5 BU",
...                 reused as-is from the screen's own prior proven driver (NOT the "TS3 BU"
...                 mentioned in an earlier task brief - the real, already-live value confirmed
...                 in this screen's own contract_page.resource/py/contract_iud.py is TS5 BU).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${CONTRACT_SCREEN}          Contract
${CONTRACT_TABLE}           manageObject:form:T_data
# navigator (groupmodel): Business Unit dropdown — MANDATORY before the grid loads.
# Value confirmed live (screen's own prior proven driver): Business Unit = "TS5 BU".
# The fill itself goes through the shared T2 "Apply Navigator From Properties"
# (resources/manage_object.resource), driven by testdata/contract_navigator.properties.
# ${CONTRACT_NAV_BU}/${CONTRACT_NAV_BU_VALUE} are kept only as documentation of the DOM id
# (row 1, C:1) and the required value - the properties-driven fill resolves to the same
# id/value, not a different one.
${CONTRACT_NAV_BU}          nav:form:G:0:R:1:C:1:dd
${CONTRACT_NAV_BU_VALUE}    TS5 BU
${CONTRACT_NAVIGATOR_PROPERTIES}    ${CURDIR}/../../../../testdata/contract_navigator.properties
${CONTRACT_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/contract_insert.properties
${CONTRACT_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/contract_update.properties
${CONTRACT_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/contract_form_verify.properties
${CONTRACT_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/contract_grid_verify.properties
# objectdates field ID (Delete — End Date = Start Date). Hardcoded deliberately, NOT label-driven -
# same documented rationale as Bank's/Area's own del-enddate constants: this row packs Start Date
# (C:1) and End Date (C:3) together with the End Date label at C:2, a shape the one-field-per-row
# label scan cannot safely resolve. Value reused as-is from the screen's own prior driver.
${CONTRACT_DEL_ENDDATE}     tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Contract's own form-field label set for the round-trip Find/Verify check (TC04) - Start
# Date/End Date deliberately excluded (they live only in objectdates, not
# updateAttributes/objectForm's fill-once trio, same convention as every other converted
# OV-GM screen); Contract Template/Contract Area deliberately excluded - filled via resolved
# reference values which can re-render different display text after reload, same caveat as
# every other converted screen's dropdown fields.
@{CONTRACT_FORM_LABELS}    Contract Code    Contract Name


*** Keywords ***
Find Contract Row By Filter
    [Documentation]    Explicitly filter the Contract grid's Code column to ${code} via the
    ...    shared T2 Find Object Row By Filter (resources/manage_object.resource), matching
    ...    every other Area-pattern-converted screen's explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${CONTRACT_TABLE}    ${code}

Clear Contract Row Filter
    [Documentation]    Clear the Code column filter (see Find Contract Row By Filter) via the
    ...    shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${CONTRACT_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Contract's OWN credentials (${CONTRACT_EC_USER}/
    ...    ${CONTRACT_EC_PASS} from credentials.py) on the current page - works whether this is
    ...    the very first login (page freshly loaded on the login form via the shared T1 Open EC
    ...    Application) or a re-login after Logout From EC Application (same login form, not a
    ...    new page/tab).
    Login To EC Screen    ${CONTRACT_EC_USER}    ${CONTRACT_EC_PASS}

Open Contract Screen With Navigator Values Populated
    [Documentation]    Navigate to the Contract screen, THEN fill + submit the mandatory
    ...    Business Unit navigator (dropdown + GO) - Contract's grid stays empty until this
    ...    happens, so this single keyword bundles both steps for the test case (owner's exact
    ...    skeleton calls this as ONE line per TC, not two). Assumes the caller already logged
    ...    in this test case (via Login To EC Application) - matches every other
    ...    Area-pattern-converted screen's "Open <Screen> Screen" convention. Navigator fill
    ...    delegates to the shared T2 "Apply Navigator From Properties"
    ...    (resources/manage_object.resource), driven by testdata/contract_navigator.properties,
    ...    instead of inlining "Select EC Dropdown Option + Apply Navigator" here - so any other
    ...    OV-GM screen with a navigator can reuse the same shared keyword with its own
    ...    properties file.
    Open EC Screen    ${CONTRACT_SCREEN}
    Apply Navigator From Properties    ${CONTRACT_NAVIGATOR_PROPERTIES}

Insert Contract Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Object From Properties, called
    ...    with ZERO arguments so contract_iud.robot's test case body reads as a plain business
    ...    step. Also owns the integrity check that the inserted Contract Code matches the
    ...    suite's ${TEST_CODE}. ${CONTRACT_INSERT_PROPERTIES}'s Contract Area value MUST sit
    ...    under the navigator's own Business Unit=TS5 BU scope or the new row is not visible
    ...    under this navigator scope (OV-GM constraint).
    [Arguments]    ${properties_path}=${CONTRACT_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Contract Code
    RETURN    ${code}

Verify Contract Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN
    ...    verification (no DB check here - that's TC02's own separate DbVerify assertion): row
    ...    exists in the grid, then Contract Code/Contract Name's LIVE SCREEN value is compared
    ...    to testdata/contract_insert.properties. Filters via Find Contract Row By Filter
    ...    first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Contract Row By Filter    ${code}
    Verify Object Insert Exists    ${CONTRACT_TABLE}    ${code}    Contract    ${CONTRACT_INSERT_PROPERTIES}
    ...    @{CONTRACT_FORM_LABELS}    code_label=Contract Code
    Clear Contract Row Filter

Update Contract Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Only
    ...    Contract Name is listed in testdata/contract_update.properties - Contract Code is
    ...    read-only in updateAttributes. Filters via Find Contract Row By Filter first, clears
    ...    after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${CONTRACT_UPDATE_PROPERTIES}
    Find Contract Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${CONTRACT_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Contract Code
    Clear Contract Row Filter
    RETURN    ${data}

Verify Contract Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN
    ...    verification: selects the row, compares Contract Name's LIVE SCREEN value to
    ...    testdata/contract_update.properties. Filters via Find Contract Row By Filter first,
    ...    clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Contract Row By Filter    ${code}
    Verify Object Form Record    ${CONTRACT_TABLE}    ${code}    Contract    ${CONTRACT_UPDATE_PROPERTIES}
    ...    Contract Name    code_label=Contract Code
    Clear Contract Row Filter

Find Contract Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Calls
    ...    Find Contract Row By Filter first. Deliberately does NOT clear the filter afterward -
    ...    Verify Contract Record Found (called right after, same TC) needs the grid still
    ...    filtered to ${code} for its own grid-check; it clears the filter once both checks
    ...    are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Contract Row By Filter    ${code}
    Find Object Record    ${CONTRACT_TABLE}    ${code}    Contract    code_label=Contract Code

Verify Contract Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid
    ...    AND the full form record match the expected data. Caller must already have selected
    ...    the row (TC04 does, via Find Contract Record before this) AND left the Code filter
    ...    active - clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${CONTRACT_TABLE}    ${code}    ${CONTRACT_GRID_VERIFY_PROPERTIES}
    ...    ${CONTRACT_FORM_VERIFY_PROPERTIES}    @{CONTRACT_FORM_LABELS}
    Clear Contract Row Filter

Delete Contract Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the contract, set End Date = Start Date (EC true delete for OV_CONTRACT), Save.
    ...    Versioned groupmodel grids redraw lazily after a delete - Save And Refresh List
    ...    (inside T2) already re-applies the navigator, so the assertion reads a fresh list.
    ...    Filters via Find Contract Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Contract Row By Filter    ${code}
    Delete Object Via End Date    ${CONTRACT_TABLE}    ${CONTRACT_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Contract Row Filter

Verify Contract Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is
    ...    absent from BOTH the grid and the database (OV_CONTRACT) - the DB check lives here,
    ...    in the shared T2 Verify Object Removed, NOT as a separate screen-local wrapper
    ...    keyword.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${CONTRACT_TABLE}    OV_CONTRACT    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Contract Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (grid-only check) - delegates to the shared T2 Verify Object Does Not
    ...    Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${CONTRACT_TABLE}    ${code}
