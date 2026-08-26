*** Settings ***
Documentation       T3 (screen) — Contract Inventory page object.
...                 Screen: Configuration > Assets > Contract_Objects > Contract Inventory (CO.2054).
...                 OV-GM (groupmodel manage-object) screen: the grid loads ONLY after the
...                 navigator (single group G:0, single row R:1, increasing column) + GO. Live
...                 recon 2026-08-26 (tmp/recon_contract_inventory_mandatory_2026_08_26.py,
...                 tmp/recon_contract_inventory_cascade_2026_08_26.py) found ONLY C:1 (Business
...                 Unit) is genuinely mandatory-yellow+empty; C:2 (Contract Area) and C:3
...                 (Contract) stay white/optional even after C:1 is filled (filling C:1 does NOT
...                 turn C:2 yellow). This is a same-row, increasing-column shape the shared T2
...                 "Apply Navigator From Properties" (resources/manage_object.resource) already
...                 supports with ZERO shared-file changes. Contract Area is still filled (kept
...                 from the already-proven prior scope, registry: "Business Unit -> Contract Area
...                 cascade + GO") even though only Business Unit is strictly mandatory.
...                 Converted to the Area-pattern 5-TC/per-TC-login/pure-screen-verify STRUCTURE
...                 (owner standing rule 2026-08-26: any EC screen with a navigator matching
...                 Area's layout MUST follow Area's FULL pattern). Grid columns confirmed live
...                 (manageObject:form:T_head scan, tmp/recon_contract_inventory_grid_headers_2026_08_26.py):
...                 Contract Inventory Code / Contract Inventory Name / Start Date / End Date -
...                 same 4-column shape as Area/Facility Class 1. objectForm labels confirmed live
...                 (tmp/recon_contract_inventory_form_fields_2026_08_26.py): SCREEN-PREFIXED
...                 "Contract Inventory Code"/"Contract Inventory Name" (like Area's "Area
...                 Code"/"Area Name"); no "Business Unit"/"Contract Area" field on objectForm, so
...                 no navigator/form field-reuse conflict. "Contract name" dropdown (value "TS5
...                 Shipper C") kept from the already-proven driver (py/contract_inventory_iud.py,
...                 live 4/4 + Playwright 8/8, verify_screen PASS 2026-08-02).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${CI_SCREEN}            Contract Inventory
${CI_TABLE}             manageObject:form:T_data
# navigator (groupmodel): single group G:0, single row R:1, increasing column - Business Unit
# (C:1, genuinely mandatory) then Contract Area (C:2, kept for parity with the already-proven
# scope) - MANDATORY-ENOUGH before the grid loads. Filled via the shared T2 "Apply Navigator From
# Properties" (resources/manage_object.resource), driven by
# testdata/contract_inventory_navigator.properties.
${CI_NAVIGATOR_PROPERTIES}    ${CURDIR}/../../../../testdata/contract_inventory_navigator.properties
${CI_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/contract_inventory_insert.properties
${CI_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/contract_inventory_update.properties
${CI_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/contract_inventory_form_verify.properties
${CI_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/contract_inventory_grid_verify.properties
# objectdates field ID (Delete - End Date = Start Date). Hardcoded deliberately, NOT label-driven -
# same documented rationale as Area's/Facility Class 1's own del-enddate constant: this row packs
# Start Date (C:1) and End Date (C:3) together with the End Date label at C:2, a shape the
# one-field-per-row label scan cannot safely resolve. Value confirmed live via the pre-existing
# Playwright driver (py/contract_inventory_iud.py: END_DATE_ID convention shared across every
# OV-GM screen).
${CI_DEL_ENDDATE}       tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Contract Inventory's own form-field label set (Start Date/End Date deliberately excluded - they
# live only in objectdates, not updateAttributes/objectForm's fill-once trio).
@{CI_FORM_LABELS}       Contract Inventory Code    Contract Inventory Name


*** Keywords ***
Find Contract Inventory Row By Filter
    [Documentation]    Explicitly filter the Contract Inventory grid's Code column to ${code} via
    ...    the shared T2 Find Object Row By Filter (resources/manage_object.resource), matching
    ...    every other Area-pattern-converted screen's explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${CI_TABLE}    ${code}

Clear Contract Inventory Row Filter
    [Documentation]    Clear the Code column filter (see Find Contract Inventory Row By Filter)
    ...    via the shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${CI_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Contract Inventory's OWN credentials
    ...    (${CONTRACT_INVENTORY_EC_USER}/${CONTRACT_INVENTORY_EC_PASS} from credentials.py) on
    ...    the current page - works whether this is the very first login (page freshly loaded on
    ...    the login form via the shared T1 Open EC Application) or a re-login after Logout From
    ...    EC Application (same login form, not a new page/tab).
    Login To EC Screen    ${CONTRACT_INVENTORY_EC_USER}    ${CONTRACT_INVENTORY_EC_PASS}

Open Contract Inventory Screen With Navigator Values Populated
    [Documentation]    Navigate to the Contract Inventory screen, THEN fill + submit the
    ...    navigator (dropdowns + GO) - the grid stays empty until this happens, so this single
    ...    keyword bundles both steps for the test case (Area's exact skeleton calls this as ONE
    ...    line per TC, not two). Assumes the caller already logged in this test case (via Login
    ...    To EC Application). Navigator fill delegates to the shared T2 "Apply Navigator From
    ...    Properties" (resources/manage_object.resource), driven by
    ...    testdata/contract_inventory_navigator.properties.
    Open EC Screen    ${CI_SCREEN}
    Apply Navigator From Properties    ${CI_NAVIGATOR_PROPERTIES}

Insert Contract Inventory Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Object From Properties And Verify
    ...    Code, called with ZERO arguments so contract_inventory_iud.robot's test case body reads
    ...    as a plain business step. Also owns the integrity check that the inserted Contract
    ...    Inventory Code matches the suite's ${TEST_CODE}.
    [Arguments]    ${properties_path}=${CI_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Contract Inventory Code
    RETURN    ${code}

Verify Contract Inventory Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification (no
    ...    DB check here - that's TC02's own separate DbVerify assertion): row exists in the grid,
    ...    then Contract Inventory Code/Contract Inventory Name's LIVE SCREEN value is compared to
    ...    testdata/contract_inventory_insert.properties. Filters via Find Contract Inventory Row
    ...    By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Contract Inventory Row By Filter    ${code}
    Verify Object Insert Exists    ${CI_TABLE}    ${code}    Contract Inventory
    ...    ${CI_INSERT_PROPERTIES}    @{CI_FORM_LABELS}    code_label=Contract Inventory Code
    Clear Contract Inventory Row Filter

Update Contract Inventory Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Only
    ...    Contract Inventory Name is listed in testdata/contract_inventory_update.properties -
    ...    Contract Inventory Code is read-only in updateAttributes. Filters via Find Contract
    ...    Inventory Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${CI_UPDATE_PROPERTIES}
    Find Contract Inventory Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${CI_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Contract Inventory Code
    Clear Contract Inventory Row Filter
    RETURN    ${data}

Verify Contract Inventory Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification:
    ...    selects the row, compares Contract Inventory Name's LIVE SCREEN value to
    ...    testdata/contract_inventory_update.properties. Filters via Find Contract Inventory Row
    ...    By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Contract Inventory Row By Filter    ${code}
    Verify Object Form Record    ${CI_TABLE}    ${code}    Contract Inventory
    ...    ${CI_UPDATE_PROPERTIES}    Contract Inventory Name    code_label=Contract Inventory Code
    Clear Contract Inventory Row Filter

Find Contract Inventory Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Calls Find Contract
    ...    Inventory Row By Filter first. Deliberately does NOT clear the filter afterward -
    ...    Verify Contract Inventory Record Found (called right after, same TC) needs the grid
    ...    still filtered to ${code} for its own grid-check; it clears the filter once both checks
    ...    are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Contract Inventory Row By Filter    ${code}
    Find Object Record    ${CI_TABLE}    ${code}    Contract Inventory    code_label=Contract Inventory Code

Verify Contract Inventory Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND
    ...    the full form record match the expected data. Caller must already have selected the
    ...    row (TC04 does, via Find Contract Inventory Record before this) AND left the Code
    ...    filter active - clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${CI_TABLE}    ${code}    ${CI_GRID_VERIFY_PROPERTIES}
    ...    ${CI_FORM_VERIFY_PROPERTIES}    @{CI_FORM_LABELS}
    Clear Contract Inventory Row Filter

Delete Contract Inventory Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the object, set End Date = Start Date (EC true delete for
    ...    OV_CONTRACT_INVENTORY), Save. Filters via Find Contract Inventory Row By Filter first,
    ...    clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Contract Inventory Row By Filter    ${code}
    Delete Object Via End Date    ${CI_TABLE}    ${CI_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Contract Inventory Row Filter

Verify Contract Inventory Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid and the database (OV_CONTRACT_INVENTORY) - the DB check lives here,
    ...    in the shared T2 Verify Object Removed, NOT as a separate screen-local wrapper keyword.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${CI_TABLE}    OV_CONTRACT_INVENTORY    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Contract Inventory Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification
    ...    (grid-only check) - delegates to the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${CI_TABLE}    ${code}
