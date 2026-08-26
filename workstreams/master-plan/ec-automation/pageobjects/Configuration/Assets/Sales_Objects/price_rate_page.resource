*** Settings ***
Documentation       T3 (screen) — Price Rate page object.
...                 Screen: Configuration > Assets > Sales_Objects > Price Rate (CO.3024).
...                 OV-GM (groupmodel manage-object) screen: the grid loads ONLY after the
...                 mandatory Business Unit navigator dropdown is set + GO (confirmed live,
...                 docs/ec_screen_registry.md line 332). Converted to the Area-pattern 5-TC/
...                 per-TC-login/pure-screen-verify STRUCTURE (2026-08-26) while KEEPING this
...                 genuine navigator gesture - Price Rate is still OV-GM, not plain Bank-shaped;
...                 the Business Unit+GO step is real and required, not something this
...                 conversion removed. Real labels confirmed live via the prior OLD-pattern
...                 driver ("Insert Price Rate Record"/py/price_rate_iud.py): objectForm/
...                 updateAttributes use SCREEN-PREFIXED "Price Rate Code"/"Price Rate Name"
...                 (like Area's "Area Code"/"Area Name"), NOT the generic "Code"/"Name"
...                 Bank/Object List use - every T2 call below passes code_label=Price Rate Code
...                 accordingly.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${PRICE_RATE_SCREEN}          Price Rate
${PRICE_RATE_TABLE}           manageObject:form:T_data
# navigator (groupmodel): Business Unit dropdown — MANDATORY before the grid loads.
# Value confirmed live (prior OLD-pattern price_rate_page.resource "Open Price Rate Screen" +
# py/price_rate_iud.py: both filled "SS2 BU" at nav:form:G:0:R:1:C:1:dd).
# 2026-08-26: the fill itself now goes through the shared T2 "Apply Navigator From Properties"
# (resources/manage_object.resource), driven by testdata/price_rate_navigator.properties.
# ${PRICE_RATE_NAV_DD} and ${PRICE_RATE_NAV_VALUE} are kept only as documentation of the DOM id
# (row 1, C:1) and the required value - the properties-driven fill resolves to the same id/value,
# not a different one.
${PRICE_RATE_NAV_DD}          nav:form:G:0:R:1:C:1:dd
${PRICE_RATE_NAV_VALUE}       SS2 BU
${PRICE_RATE_NAVIGATOR_PROPERTIES}    ${CURDIR}/../../../../testdata/price_rate_navigator.properties
${PRICE_RATE_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/price_rate_insert.properties
${PRICE_RATE_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/price_rate_update.properties
${PRICE_RATE_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/price_rate_form_verify.properties
${PRICE_RATE_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/price_rate_grid_verify.properties
# objectdates field ID (Delete — End Date = Start Date). Hardcoded deliberately, NOT label-driven -
# same documented rationale as Area's ${AREA_DEL_ENDDATE}/Bank's ${BANK_DEL_ENDDATE}: this row
# packs Start Date (C:1) and End Date (C:3) together with the End Date label at C:2, a shape the
# one-field-per-row label scan cannot safely resolve. Value confirmed live via the prior
# OLD-pattern price_rate_page.resource's own ${DEL_ENDDATE}.
${PRICE_RATE_DEL_ENDDATE}     tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Price Rate's own form-field label set (Start Date deliberately excluded - it lives only in
# objectdates/the insert-time fill, not updateAttributes' fill-once trio; Frequency/Business Unit
# deliberately excluded from round-trip comparison - they are filled via resolved dropdown/
# reference values which can re-render different display text after reload, same caveat as every
# other converted screen's dropdown fields).
@{PRICE_RATE_FORM_LABELS}    Price Rate Code    Price Rate Name


*** Keywords ***
Find Price Rate Row By Filter
    [Documentation]    Explicitly filter the Price Rate grid's Code column to ${code} via the
    ...    shared T2 Find Object Row By Filter (resources/manage_object.resource), matching every
    ...    other Area-pattern-converted screen's explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${PRICE_RATE_TABLE}    ${code}

Clear Price Rate Row Filter
    [Documentation]    Clear the Code column filter (see Find Price Rate Row By Filter) via the
    ...    shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${PRICE_RATE_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Price Rate's OWN credentials (${PRICE_RATE_EC_USER}/
    ...    ${PRICE_RATE_EC_PASS} from credentials.py) on the current page - works whether this is
    ...    the very first login (page freshly loaded on the login form via the shared T1 Open EC
    ...    Application) or a re-login after Logout From EC Application (same login form, not a
    ...    new page/tab).
    Login To EC Screen    ${PRICE_RATE_EC_USER}    ${PRICE_RATE_EC_PASS}

Open Price Rate Screen With Navigator Values Populated
    [Documentation]    Navigate to the Price Rate screen, THEN fill + submit the mandatory
    ...    Business Unit navigator (dropdown + GO) - Price Rate's grid stays empty until this
    ...    happens, so this single keyword bundles both steps for the test case (one line per
    ...    TC, not two). Assumes the caller already logged in this test case (via Login To EC
    ...    Application) - matches every other Area-pattern-converted screen's "Open <Screen>
    ...    Screen" convention. Navigator fill delegates to the shared T2 "Apply Navigator From
    ...    Properties" (resources/manage_object.resource, added 2026-08-26), driven by
    ...    testdata/price_rate_navigator.properties, instead of inlining "Select EC Dropdown
    ...    Option + Apply Navigator" here.
    Open EC Screen    ${PRICE_RATE_SCREEN}
    Apply Navigator From Properties    ${PRICE_RATE_NAVIGATOR_PROPERTIES}

Insert Price Rate Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Object From Properties And
    ...    Verify Code, called with ZERO arguments so price_rate_iud.robot's test case body reads
    ...    as a plain business step. Also owns the integrity check that the inserted Price Rate
    ...    Code matches the suite's ${TEST_CODE}. ${PRICE_RATE_INSERT_PROPERTIES}'s Business Unit
    ...    value MUST equal ${PRICE_RATE_NAV_VALUE} or the new row is not visible under this
    ...    navigator scope (OV-GM constraint).
    [Arguments]    ${properties_path}=${PRICE_RATE_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Price Rate Code
    RETURN    ${code}

Verify Price Rate Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification (no
    ...    DB check here - that's TC02's own separate DbVerify assertion): row exists in the grid,
    ...    then Price Rate Code/Price Rate Name's LIVE SCREEN value is compared to
    ...    testdata/price_rate_insert.properties. Filters via Find Price Rate Row By Filter
    ...    first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Price Rate Row By Filter    ${code}
    Verify Object Insert Exists    ${PRICE_RATE_TABLE}    ${code}    Price Rate
    ...    ${PRICE_RATE_INSERT_PROPERTIES}    @{PRICE_RATE_FORM_LABELS}    code_label=Price Rate Code
    Clear Price Rate Row Filter

Update Price Rate Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Only Price
    ...    Rate Name is listed in testdata/price_rate_update.properties - Price Rate Code is
    ...    read-only in updateAttributes. Filters via Find Price Rate Row By Filter first, clears
    ...    after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${PRICE_RATE_UPDATE_PROPERTIES}
    Find Price Rate Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${PRICE_RATE_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Price Rate Code
    Clear Price Rate Row Filter
    RETURN    ${data}

Verify Price Rate Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification:
    ...    selects the row, compares Price Rate Name's LIVE SCREEN value to
    ...    testdata/price_rate_update.properties. Filters via Find Price Rate Row By Filter
    ...    first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Price Rate Row By Filter    ${code}
    Verify Object Form Record    ${PRICE_RATE_TABLE}    ${code}    Price Rate
    ...    ${PRICE_RATE_UPDATE_PROPERTIES}    Price Rate Name    code_label=Price Rate Code
    Clear Price Rate Row Filter

Find Price Rate Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Calls Find Price
    ...    Rate Row By Filter first. Deliberately does NOT clear the filter afterward - Verify
    ...    Price Rate Record Found (called right after, same TC) needs the grid still filtered to
    ...    ${code} for its own grid-check; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Price Rate Row By Filter    ${code}
    Find Object Record    ${PRICE_RATE_TABLE}    ${code}    Price Rate    code_label=Price Rate Code

Verify Price Rate Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND
    ...    the full form record match the expected data. Caller must already have selected the
    ...    row (TC04 does, via Find Price Rate Record before this) AND left the Code filter
    ...    active - clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${PRICE_RATE_TABLE}    ${code}    ${PRICE_RATE_GRID_VERIFY_PROPERTIES}
    ...    ${PRICE_RATE_FORM_VERIFY_PROPERTIES}    @{PRICE_RATE_FORM_LABELS}
    Clear Price Rate Row Filter

Delete Price Rate Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the price rate, set End Date = Start Date (EC true delete for OV_PRICE_RATE),
    ...    Save. Versioned groupmodel grids redraw lazily after a delete - Save And Refresh List
    ...    (inside T2) already re-applies the navigator, so the assertion reads a fresh list.
    ...    Filters via Find Price Rate Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Price Rate Row By Filter    ${code}
    Delete Object Via End Date    ${PRICE_RATE_TABLE}    ${PRICE_RATE_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Price Rate Row Filter

Verify Price Rate Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid AND the database (OV_PRICE_RATE) - the DB check lives here, in the
    ...    shared T2 Verify Object Removed, NOT as a separate screen-local wrapper keyword (that
    ...    pattern was removed by this conversion - see Documentation above).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${PRICE_RATE_TABLE}    OV_PRICE_RATE    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Price Rate Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification
    ...    (grid-only check) - delegates to the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${PRICE_RATE_TABLE}    ${code}
