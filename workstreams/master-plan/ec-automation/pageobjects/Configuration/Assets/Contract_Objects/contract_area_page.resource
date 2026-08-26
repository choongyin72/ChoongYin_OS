*** Settings ***
Documentation       T3 (screen) — Contract Area page object.
...                 Screen: Configuration > Assets > Contract Objects > Contract Area.
...                 OV-GM (groupmodel manage-object) screen: the grid loads ONLY after the
...                 mandatory Business Unit navigator dropdown is set + GO. Converted to the
...                 Area-pattern 5-TC/per-TC-login/pure-screen-verify STRUCTURE (2026-08-26,
...                 mirroring area_page.resource/area_iud.robot exactly) while KEEPING this
...                 genuine navigator gesture - Contract Area is still OV-GM, not plain
...                 Bank-shaped; the Business Unit+GO step is real and required, not something
...                 this conversion removed. Real labels confirmed live (screenshot evidence,
...                 screens/Configuration/Assets/Contract_Objects/Contract_Area/evidence/
...                 ca_04_insert_filled.png / ca_06_update_result.png): objectForm/updateAttributes
...                 use SCREEN-PREFIXED "Contract Area Code"/"Contract Area Name" (like Area's own
...                 "Area Code"/"Area Name"), NOT the generic "Code"/"Name" Bank/Object List use -
...                 every T2 call below passes code_label=Contract Area Code accordingly.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${CONTRACT_AREA_SCREEN}         Contract Area
${CONTRACT_AREA_TABLE}          manageObject:form:T_data
# navigator (groupmodel): Business Unit dropdown — MANDATORY before the grid loads.
# Value confirmed live (pre-existing suite's user-approved ${NAV_BU}/${PARENT_VALUE} = ECP Norway,
# 2026-06-18): "ECP Norway" is a real, already-used Business Unit in this sandbox.
# 2026-08-26: the fill itself now goes through the shared T2 "Apply Navigator From Properties"
# (resources/manage_object.resource), driven by testdata/contract_area_navigator.properties.
# ${CONTRACT_AREA_NAV_BU} and ${CONTRACT_AREA_NAV_BU_VALUE} are kept only as documentation of the
# DOM id (row 1, C:1) and the required value - the properties-driven fill resolves to the same
# id/value, not a different one.
${CONTRACT_AREA_NAV_BU}         nav:form:G:0:R:1:C:1:dd
${CONTRACT_AREA_NAV_BU_VALUE}    ECP Norway
${CONTRACT_AREA_NAVIGATOR_PROPERTIES}    ${CURDIR}/../../../../testdata/contract_area_navigator.properties
${CONTRACT_AREA_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/contract_area_insert.properties
${CONTRACT_AREA_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/contract_area_update.properties
${CONTRACT_AREA_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/contract_area_form_verify.properties
${CONTRACT_AREA_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/contract_area_grid_verify.properties
# objectdates field ID (Delete — End Date = Start Date). Hardcoded deliberately, NOT label-driven -
# same documented rationale as Area's ${AREA_DEL_ENDDATE}: this row packs Start Date (C:1) and
# End Date (C:3) together with the End Date label at C:2, a shape the one-field-per-row label
# scan cannot safely resolve. Value confirmed live via screenshot evidence
# ca_07_delete_end_date_set.png and the pre-existing Playwright driver
# (screens/.../Contract_Area/playwright/ec_iud_contract_area.py: DEL_END).
${CONTRACT_AREA_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Contract Area's own form-field label set (Start Date/End Date deliberately excluded - they live
# only in objectdates, not updateAttributes/objectForm's fill-once trio; Business Unit Name
# deliberately excluded from round-trip comparison - it's filled via a resolved reference value
# which can re-render different display text after reload, same caveat as every other converted
# screen's dropdown fields).
@{CONTRACT_AREA_FORM_LABELS}    Contract Area Code    Contract Area Name


*** Keywords ***
Find Contract Area Row By Filter
    [Documentation]    Explicitly filter the Contract Area grid's Code column to ${code} via the
    ...    shared T2 Find Object Row By Filter (resources/manage_object.resource), matching every
    ...    other Area-pattern-converted screen's explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${CONTRACT_AREA_TABLE}    ${code}

Clear Contract Area Row Filter
    [Documentation]    Clear the Code column filter (see Find Contract Area Row By Filter) via the
    ...    shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${CONTRACT_AREA_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Contract Area's OWN credentials (${CONTRACT_AREA_EC_USER}/
    ...    ${CONTRACT_AREA_EC_PASS} from credentials.py) on the current page - works whether this
    ...    is the very first login (page freshly loaded on the login form via the shared T1 Open
    ...    EC Application) or a re-login after Logout From EC Application (same login form, not a
    ...    new page/tab).
    Login To EC Screen    ${CONTRACT_AREA_EC_USER}    ${CONTRACT_AREA_EC_PASS}

Open Contract Area Screen With Navigator Values Populated
    [Documentation]    Navigate to the Contract Area screen, THEN fill + submit the mandatory
    ...    Business Unit navigator (dropdown + GO) - Contract Area's grid stays empty until this
    ...    happens, so this single keyword bundles both steps for the test case (owner's exact
    ...    skeleton calls this as ONE line per TC, not two). Assumes the caller already logged in
    ...    this test case (via Login To EC Application) - matches every other Area-pattern-
    ...    converted screen's "Open <Screen> Screen" convention. Navigator fill delegates to the
    ...    shared T2 "Apply Navigator From Properties" (resources/manage_object.resource),
    ...    driven by testdata/contract_area_navigator.properties, instead of inlining
    ...    "Select EC Dropdown Option + Apply Navigator" here - so any other OV-GM screen with a
    ...    navigator can reuse the same shared keyword with its own properties file.
    Open EC Screen    ${CONTRACT_AREA_SCREEN}
    Apply Navigator From Properties    ${CONTRACT_AREA_NAVIGATOR_PROPERTIES}

Insert Contract Area Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Object From Properties And Verify
    ...    Code, called with ZERO arguments so contract_area_iud.robot's test case body reads as a
    ...    plain business step. Also owns the integrity check that the inserted Contract Area Code
    ...    matches the suite's ${TEST_CODE}. ${CONTRACT_AREA_INSERT_PROPERTIES}'s Business Unit
    ...    Name value MUST equal ${CONTRACT_AREA_NAV_BU_VALUE} or the new row is not visible under
    ...    this navigator scope (OV-GM constraint).
    [Arguments]    ${properties_path}=${CONTRACT_AREA_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Contract Area Code
    RETURN    ${code}

Verify Contract Area Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification (no
    ...    DB check here - that's the mandatory live-run DB self-clean check, not an in-suite
    ...    assertion): row exists in the grid, then Contract Area Code/Contract Area Name's LIVE
    ...    SCREEN value is compared to testdata/contract_area_insert.properties. Filters via Find
    ...    Contract Area Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Contract Area Row By Filter    ${code}
    Verify Object Insert Exists    ${CONTRACT_AREA_TABLE}    ${code}    Contract Area
    ...    ${CONTRACT_AREA_INSERT_PROPERTIES}    @{CONTRACT_AREA_FORM_LABELS}
    ...    code_label=Contract Area Code
    Clear Contract Area Row Filter

Update Contract Area Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Only
    ...    Contract Area Name is listed in testdata/contract_area_update.properties - Contract
    ...    Area Code is read-only in updateAttributes. Filters via Find Contract Area Row By
    ...    Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${CONTRACT_AREA_UPDATE_PROPERTIES}
    Find Contract Area Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${CONTRACT_AREA_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Contract Area Code
    Clear Contract Area Row Filter
    RETURN    ${data}

Verify Contract Area Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification:
    ...    selects the row, compares Contract Area Name's LIVE SCREEN value to
    ...    testdata/contract_area_update.properties. Filters via Find Contract Area Row By Filter
    ...    first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Contract Area Row By Filter    ${code}
    Verify Object Form Record    ${CONTRACT_AREA_TABLE}    ${code}    Contract Area
    ...    ${CONTRACT_AREA_UPDATE_PROPERTIES}    Contract Area Name    code_label=Contract Area Code
    Clear Contract Area Row Filter

Find Contract Area Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Calls Find Contract
    ...    Area Row By Filter first. Deliberately does NOT clear the filter afterward - Verify
    ...    Contract Area Record Found (called right after, same TC) needs the grid still filtered
    ...    to ${code} for its own grid-check; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Contract Area Row By Filter    ${code}
    Find Object Record    ${CONTRACT_AREA_TABLE}    ${code}    Contract Area    code_label=Contract Area Code

Verify Contract Area Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND
    ...    the full form record match the expected data. Caller must already have selected the
    ...    row (TC04 does, via Find Contract Area Record before this) AND left the Code filter
    ...    active - clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${CONTRACT_AREA_TABLE}    ${code}    ${CONTRACT_AREA_GRID_VERIFY_PROPERTIES}
    ...    ${CONTRACT_AREA_FORM_VERIFY_PROPERTIES}    @{CONTRACT_AREA_FORM_LABELS}
    Clear Contract Area Row Filter

Delete Contract Area Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the contract area, set End Date = Start Date (EC true delete for
    ...    OV_CONTRACT_AREA), Save. Versioned groupmodel grids redraw lazily after a delete - Save
    ...    And Refresh List (inside T2) already re-applies the navigator, so the assertion reads a
    ...    fresh list. Filters via Find Contract Area Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Contract Area Row By Filter    ${code}
    Delete Object Via End Date    ${CONTRACT_AREA_TABLE}    ${CONTRACT_AREA_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Contract Area Row Filter

Verify Contract Area Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid and the database (OV_CONTRACT_AREA) - the DB check lives here, in
    ...    the shared T2 Verify Object Removed, NOT as a separate screen-local wrapper keyword
    ...    (that pattern was removed by this conversion - see Documentation above).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${CONTRACT_AREA_TABLE}    OV_CONTRACT_AREA    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Contract Area Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification
    ...    (grid-only check) - delegates to the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${CONTRACT_AREA_TABLE}    ${code}
