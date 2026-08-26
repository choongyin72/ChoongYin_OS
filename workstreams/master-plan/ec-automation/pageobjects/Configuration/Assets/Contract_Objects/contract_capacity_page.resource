*** Settings ***
Documentation       T3 (screen) — Contract Capacity page object.
...                 Screen: Configuration > Assets > Contract Objects > Contract Capacity (CO.2044).
...                 OV-GM (groupmodel manage-object) screen: the grid loads ONLY after the
...                 mandatory Business Unit navigator dropdown is set + GO. Converted to the
...                 Area-pattern 5-TC/per-TC-login/pure-screen-verify/properties-driven STRUCTURE
...                 (this conversion, 2026-08-26) — Contract Capacity is still OV-GM, not plain
...                 Bank-shaped; the Business Unit+GO step is real and required, not something
...                 this conversion removed. Navigator value ("TS5 BU") and field labels
...                 (Contract Capacity Code/Contract Capacity Name/Start Date/Contract Name/
...                 Location Name) are all PROVEN live by the screen's own pre-existing driver
...                 (py/contract_capacity_iud.py, live 8/8 shipped 2026-08-01) — carried forward
...                 unchanged, not re-derived from a sibling screen.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${CONTRACT_CAPACITY_SCREEN}    Contract Capacity
${CONTRACT_CAPACITY_TABLE}     manageObject:form:T_data
# navigator (groupmodel): Business Unit dropdown — MANDATORY before the grid loads.
# Value confirmed live by the pre-existing driver (py/contract_capacity_iud.py: nav:form:G:0:R:1:
# C:1:dd = "TS5 BU", proven live 2026-08-01 shipped suite, 8/8 pass). The fill itself now goes
# through the shared T2 "Apply Navigator From Properties" (resources/manage_object.resource),
# driven by testdata/contract_capacity_navigator.properties — ${CONTRACT_CAPACITY_NAV_BU} and
# ${CONTRACT_CAPACITY_NAV_BU_VALUE} are kept only as documentation of the DOM id (row 1, C:1)
# and the required value; the properties-driven fill resolves to the same id/value.
${CONTRACT_CAPACITY_NAV_BU}    nav:form:G:0:R:1:C:1:dd
${CONTRACT_CAPACITY_NAV_BU_VALUE}    TS5 BU
${CONTRACT_CAPACITY_NAVIGATOR_PROPERTIES}    ${CURDIR}/../../../../testdata/contract_capacity_navigator.properties
${CONTRACT_CAPACITY_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/contract_capacity_insert.properties
${CONTRACT_CAPACITY_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/contract_capacity_update.properties
${CONTRACT_CAPACITY_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/contract_capacity_form_verify.properties
${CONTRACT_CAPACITY_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/contract_capacity_grid_verify.properties
# objectdates field ID (Delete — End Date = Start Date). Hardcoded deliberately, NOT label-driven —
# same documented rationale as Area's ${AREA_DEL_ENDDATE}: this row packs Start Date (C:1) and
# End Date (C:3) together with the End Date label at C:2, a shape the one-field-per-row label
# scan cannot safely resolve. Value confirmed live via the pre-existing driver
# (py/contract_capacity_iud.py: DEL_ENDDATE / this screen's own prior contract_capacity_page.resource).
${CONTRACT_CAPACITY_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Contract Capacity's own form-field label set (Start Date deliberately excluded — it lives only
# in objectdates, not updateAttributes/objectForm's fill-once trio; Contract Name/Location Name
# deliberately excluded from round-trip comparison — they're filled via resolved reference
# values which can re-render different display text after reload, same caveat as every other
# converted screen's dropdown fields).
@{CONTRACT_CAPACITY_FORM_LABELS}    Contract Capacity Code    Contract Capacity Name


*** Keywords ***
Find Contract Capacity Row By Filter
    [Documentation]    Explicitly filter the Contract Capacity grid's Code column to ${code} via
    ...    the shared T2 Find Object Row By Filter (resources/manage_object.resource), matching
    ...    every other Area/Bank-pattern-converted screen's explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${CONTRACT_CAPACITY_TABLE}    ${code}

Clear Contract Capacity Row Filter
    [Documentation]    Clear the Code column filter (see Find Contract Capacity Row By Filter)
    ...    via the shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${CONTRACT_CAPACITY_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Contract Capacity's OWN credentials
    ...    (${CONTRACT_CAPACITY_EC_USER}/${CONTRACT_CAPACITY_EC_PASS} from credentials.py) on the
    ...    current page — works whether this is the very first login (page freshly loaded on the
    ...    login form via the shared T1 Open EC Application) or a re-login after
    ...    Logout From EC Application (same login form, not a new page/tab).
    Login To EC Screen    ${CONTRACT_CAPACITY_EC_USER}    ${CONTRACT_CAPACITY_EC_PASS}

Open Contract Capacity Screen With Navigator Values Populated
    [Documentation]    Navigate to the Contract Capacity screen, THEN fill + submit the mandatory
    ...    Business Unit navigator (dropdown + GO) — Contract Capacity's grid stays empty until
    ...    this happens, so this single keyword bundles both steps for the test case. Assumes the
    ...    caller already logged in this test case (via Login To EC Application) — matches every
    ...    other Area/Bank-pattern-converted screen's "Open <Screen> Screen" convention. Navigator
    ...    fill delegates to the shared T2 "Apply Navigator From Properties"
    ...    (resources/manage_object.resource), driven by
    ...    testdata/contract_capacity_navigator.properties, instead of inlining
    ...    "Select EC Dropdown Option + Apply Navigator" here — so any other OV-GM screen with a
    ...    navigator can reuse the same shared keyword with its own properties file.
    Open EC Screen    ${CONTRACT_CAPACITY_SCREEN}
    Apply Navigator From Properties    ${CONTRACT_CAPACITY_NAVIGATOR_PROPERTIES}

Insert Contract Capacity Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Object From Properties And Verify
    ...    Code, called with ZERO arguments so contract_capacity_iud.robot's test case body reads
    ...    as a plain business step. Also owns the integrity check that the inserted Contract
    ...    Capacity Code matches the suite's ${TEST_CODE}. ${CONTRACT_CAPACITY_INSERT_PROPERTIES}'s
    ...    Contract Name/Location Name values MUST match the navigator's Business Unit scope or
    ...    the new row is not visible under this navigator scope (OV-GM constraint) — both are
    ...    PROVEN live by the screen's pre-existing driver.
    [Arguments]    ${properties_path}=${CONTRACT_CAPACITY_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Contract Capacity Code
    RETURN    ${code}

Verify Contract Capacity Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification (no
    ...    DB check here): row exists in the grid, then Contract Capacity Code/Contract Capacity
    ...    Name's LIVE SCREEN value is compared to testdata/contract_capacity_insert.properties.
    ...    Filters via Find Contract Capacity Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Contract Capacity Row By Filter    ${code}
    Verify Object Insert Exists    ${CONTRACT_CAPACITY_TABLE}    ${code}    Contract Capacity
    ...    ${CONTRACT_CAPACITY_INSERT_PROPERTIES}    @{CONTRACT_CAPACITY_FORM_LABELS}
    ...    code_label=Contract Capacity Code
    Clear Contract Capacity Row Filter

Update Contract Capacity Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Only
    ...    Contract Capacity Name is listed in testdata/contract_capacity_update.properties —
    ...    Contract Capacity Code is read-only in updateAttributes. Filters via Find Contract
    ...    Capacity Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${CONTRACT_CAPACITY_UPDATE_PROPERTIES}
    Find Contract Capacity Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${CONTRACT_CAPACITY_TABLE}    ${code}
    ...    ${properties_path}    ${TEST NAME}_action    code_label=Contract Capacity Code
    Clear Contract Capacity Row Filter
    RETURN    ${data}

Verify Contract Capacity Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification:
    ...    selects the row, compares Contract Capacity Name's LIVE SCREEN value to
    ...    testdata/contract_capacity_update.properties. Filters via Find Contract Capacity Row
    ...    By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Contract Capacity Row By Filter    ${code}
    Verify Object Form Record    ${CONTRACT_CAPACITY_TABLE}    ${code}    Contract Capacity
    ...    ${CONTRACT_CAPACITY_UPDATE_PROPERTIES}    Contract Capacity Name
    ...    code_label=Contract Capacity Code
    Clear Contract Capacity Row Filter

Find Contract Capacity Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Calls Find Contract
    ...    Capacity Row By Filter first. Deliberately does NOT clear the filter afterward —
    ...    Verify Contract Capacity Record Found (called right after, same TC) needs the grid
    ...    still filtered to ${code} for its own grid-check; it clears the filter once both
    ...    checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Contract Capacity Row By Filter    ${code}
    Find Object Record    ${CONTRACT_CAPACITY_TABLE}    ${code}    Contract Capacity
    ...    code_label=Contract Capacity Code

Verify Contract Capacity Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND
    ...    the full form record match the expected data. Caller must already have selected the
    ...    row (TC04 does, via Find Contract Capacity Record before this) AND left the Code
    ...    filter active — clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${CONTRACT_CAPACITY_TABLE}    ${code}
    ...    ${CONTRACT_CAPACITY_GRID_VERIFY_PROPERTIES}    ${CONTRACT_CAPACITY_FORM_VERIFY_PROPERTIES}
    ...    @{CONTRACT_CAPACITY_FORM_LABELS}
    Clear Contract Capacity Row Filter

Delete Contract Capacity Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the contract capacity, set End Date = Start Date (EC true delete for
    ...    OV_CONTRACT_CAPACITY), Save. Versioned groupmodel grids redraw lazily after a delete —
    ...    Save And Refresh List (inside T2) already re-applies the navigator, so the assertion
    ...    reads a fresh list. Filters via Find Contract Capacity Row By Filter first, clears
    ...    after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Contract Capacity Row By Filter    ${code}
    Delete Object Via End Date    ${CONTRACT_CAPACITY_TABLE}    ${CONTRACT_CAPACITY_DEL_ENDDATE}
    ...    ${code}    ${date}    ${TEST NAME}_action
    Clear Contract Capacity Row Filter

Verify Contract Capacity Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid AND the database (OV_CONTRACT_CAPACITY) — the DB check lives here,
    ...    in the shared T2 Verify Object Removed, NOT as a separate screen-local wrapper keyword.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${CONTRACT_CAPACITY_TABLE}    OV_CONTRACT_CAPACITY    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Contract Capacity Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification
    ...    (grid-only check) — delegates to the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${CONTRACT_CAPACITY_TABLE}    ${code}
