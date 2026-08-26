*** Settings ***
Documentation       T3 (screen) — Price Object page object.
...                 Screen: Configuration > Assets > Sales_Objects > Price Object (CO.3016).
...                 OV-GM (manage-object, groupmodel) screen: the grid loads ONLY after the
...                 navigator's single mandatory Business Unit dropdown is set + GO - NOT a
...                 real cascade (the 2 sibling nav dropdown columns are unrelated optional
...                 filters, confirmed live, same class of gap as Service/CO.2103 and Area's
...                 own single-dropdown shape). Converted to the Area-pattern full STRUCTURE
...                 (2026-08-26): 5 TCs, per-TC login/logout, fixed test code, properties-file-
...                 driven insert/update/verify, explicit grid-filter wiring, zero inline
...                 DB-verify calls in the .robot file. Real labels confirmed live via the
...                 prior hand-written driver (py/price_object_iud.py): objectForm/
...                 updateAttributes use SCREEN-PREFIXED "Price Object Code"/"Price Object
...                 Name" - every T2 call below passes code_label=Price Object Code
...                 accordingly.
...
...                 NOT the same screen as the separately-built "Product Price Object"
...                 (CD.0011, PR #502) - that is a distinct custom-URL controller with NO
...                 navigator at all; this file/screen is untouched by that build and vice
...                 versa.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${PRICE_OBJECT_SCREEN}          Price Object
${PRICE_OBJECT_TABLE}           manageObject:form:T_data
# navigator (groupmodel): single Business Unit dropdown - MANDATORY before the grid loads.
# Value confirmed LIVE this session (2026-08-26, tmp/recon_price_object_nav.py): first-
# available resolves to "EC LNG Norway" in this sandbox - NOT "Royalty Canada" (that value
# belongs to sibling screens Property/Price Index/Division Order/Royalty Contract, a
# DIFFERENT environment default, confirmed not reusable here without guessing).
# The fill itself goes through the shared T2 "Apply Navigator From Properties"
# (resources/manage_object.resource), driven by testdata/price_object_navigator.properties.
# ${PRICE_OBJECT_NAV_BU} and ${PRICE_OBJECT_NAV_BU_VALUE} are kept only as documentation of
# the DOM id (row 1, C:1) and the required value - the properties-driven fill resolves to the
# same id/value, not a different one.
${PRICE_OBJECT_NAV_BU}          nav:form:G:0:R:1:C:1:dd
${PRICE_OBJECT_NAV_BU_VALUE}    EC LNG Norway
${PRICE_OBJECT_NAVIGATOR_PROPERTIES}    ${CURDIR}/../../../../testdata/price_object_navigator.properties
${PRICE_OBJECT_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/price_object_insert.properties
${PRICE_OBJECT_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/price_object_update.properties
${PRICE_OBJECT_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/price_object_form_verify.properties
${PRICE_OBJECT_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/price_object_grid_verify.properties
# objectdates field ID (Delete - End Date = Start Date). Hardcoded deliberately, NOT
# label-driven - same documented rationale as Area's/Bank's own del-enddate id: this row
# packs Start Date (C:1) and End Date (C:3) together with the End Date label at C:2, a shape
# the one-field-per-row label scan cannot safely resolve. Value confirmed live via the prior
# hand-written driver's own DOM (same framework-invariant layout as every other OV-GM screen).
${PRICE_OBJECT_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Price Object's own form-field label set (Start Date/End Date deliberately excluded - they
# live only in objectdates, not updateAttributes/objectForm's fill-once trio; Business Unit
# deliberately excluded from round-trip comparison - it's filled via a resolved reference
# value which can re-render different display text after reload, same caveat as every other
# converted screen's dropdown fields).
@{PRICE_OBJECT_FORM_LABELS}    Price Object Code    Price Object Name


*** Keywords ***
Find Price Object Row By Filter
    [Documentation]    Explicitly filter the Price Object grid's Code column to ${code} via
    ...    the shared T2 Find Object Row By Filter (resources/manage_object.resource),
    ...    matching every other Area-pattern-converted screen's explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${PRICE_OBJECT_TABLE}    ${code}

Clear Price Object Row Filter
    [Documentation]    Clear the Code column filter (see Find Price Object Row By Filter) via
    ...    the shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${PRICE_OBJECT_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Price Object's OWN credentials (${PRICE_OBJECT_EC_USER}/
    ...    ${PRICE_OBJECT_EC_PASS} from credentials.py) on the current page - works whether
    ...    this is the very first login (page freshly loaded on the login form via the shared
    ...    T1 Open EC Application) or a re-login after Logout From EC Application.
    Login To EC Screen    ${PRICE_OBJECT_EC_USER}    ${PRICE_OBJECT_EC_PASS}

Open Price Object Screen With Navigator Values Populated
    [Documentation]    Navigate to the Price Object screen, THEN fill + submit the mandatory
    ...    Business Unit navigator (dropdown + GO) - the grid stays empty until this happens,
    ...    so this single keyword bundles both steps for the test case (one line per TC).
    ...    Assumes the caller already logged in this test case (via Login To EC Application).
    ...    Navigator fill delegates to the shared T2 "Apply Navigator From Properties"
    ...    (resources/manage_object.resource), driven by testdata/price_object_navigator.properties.
    Open EC Screen    ${PRICE_OBJECT_SCREEN}
    Apply Navigator From Properties    ${PRICE_OBJECT_NAVIGATOR_PROPERTIES}

Insert Price Object Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Object From Properties And
    ...    Verify Code, called with ZERO arguments so price_object_iud.robot's test case body
    ...    reads as a plain business step. ${PRICE_OBJECT_INSERT_PROPERTIES}'s Business Unit
    ...    value MUST equal ${PRICE_OBJECT_NAV_BU_VALUE} or the new row is not visible under
    ...    this navigator scope (OV-GM constraint).
    [Arguments]    ${properties_path}=${PRICE_OBJECT_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Price Object Code
    RETURN    ${code}

Verify Price Object Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN
    ...    verification (no DB check here - that's TC02's own separate DbVerify assertion):
    ...    row exists in the grid, then Price Object Code/Price Object Name's LIVE SCREEN
    ...    value is compared to testdata/price_object_insert.properties. Filters via Find
    ...    Price Object Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Price Object Row By Filter    ${code}
    Verify Object Insert Exists    ${PRICE_OBJECT_TABLE}    ${code}    Price Object
    ...    ${PRICE_OBJECT_INSERT_PROPERTIES}    @{PRICE_OBJECT_FORM_LABELS}
    ...    code_label=Price Object Code
    Clear Price Object Row Filter

Update Price Object Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Only
    ...    Price Object Name is listed in testdata/price_object_update.properties - Price
    ...    Object Code is read-only in updateAttributes. Filters via Find Price Object Row By
    ...    Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${PRICE_OBJECT_UPDATE_PROPERTIES}
    Find Price Object Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${PRICE_OBJECT_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Price Object Code
    Clear Price Object Row Filter
    RETURN    ${data}

Verify Price Object Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN
    ...    verification: selects the row, compares Price Object Name's LIVE SCREEN value to
    ...    testdata/price_object_update.properties. Filters via Find Price Object Row By
    ...    Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Price Object Row By Filter    ${code}
    Verify Object Form Record    ${PRICE_OBJECT_TABLE}    ${code}    Price Object
    ...    ${PRICE_OBJECT_UPDATE_PROPERTIES}    Price Object Name    code_label=Price Object Code
    Clear Price Object Row Filter

Find Price Object Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Calls
    ...    Find Price Object Row By Filter first. Deliberately does NOT clear the filter
    ...    afterward - Verify Price Object Record Found (called right after, same TC) needs
    ...    the grid still filtered to ${code} for its own grid-check; it clears the filter
    ...    once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Price Object Row By Filter    ${code}
    Find Object Record    ${PRICE_OBJECT_TABLE}    ${code}    Price Object    code_label=Price Object Code

Verify Price Object Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the full form record match the expected data. Caller must already have
    ...    selected the row (TC04 does, via Find Price Object Record before this) AND left
    ...    the Code filter active - clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${PRICE_OBJECT_TABLE}    ${code}    ${PRICE_OBJECT_GRID_VERIFY_PROPERTIES}
    ...    ${PRICE_OBJECT_FORM_VERIFY_PROPERTIES}    @{PRICE_OBJECT_FORM_LABELS}
    Clear Price Object Row Filter

Delete Price Object Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date,
    ...    called with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/
    ...    ${END_DATE}). Select the object, set End Date = Start Date (EC true delete for
    ...    OV_PRICE_OBJECT), Save. Versioned groupmodel grids redraw lazily after a delete -
    ...    Save And Refresh List (inside T2) already re-applies the navigator, so the
    ...    assertion reads a fresh list. Filters via Find Price Object Row By Filter first,
    ...    clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Price Object Row By Filter    ${code}
    Delete Object Via End Date    ${PRICE_OBJECT_TABLE}    ${PRICE_OBJECT_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Price Object Row Filter

Verify Price Object Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is
    ...    absent from BOTH the grid and the database (OV_PRICE_OBJECT) - the DB check lives
    ...    here, in the shared T2 Verify Object Removed, NOT as a separate screen-local
    ...    wrapper keyword.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${PRICE_OBJECT_TABLE}    OV_PRICE_OBJECT    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Price Object Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (grid-only check) - delegates to the shared T2 Verify Object Does Not
    ...    Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${PRICE_OBJECT_TABLE}    ${code}
