*** Settings ***
Documentation       T3 (screen) — Transport Zone page object.
...                 Screen: Configuration > Assets > Dispatching Objects > Transport Zone.
...                 OV-GM (groupmodel manage-object) screen: the grid loads ONLY after the
...                 mandatory Business Unit navigator dropdown (nav:form:G:0, C:1) is set + GO.
...                 Converted to the Area-pattern 5-TC/per-TC-login/pure-screen-verify STRUCTURE
...                 (2026-08-26) while KEEPING this genuine navigator gesture - Transport Zone is
...                 still OV-GM, not plain Bank-shaped; the Business Unit+GO step is real and
...                 required, not something this conversion removed. Live recon (2026-08-26)
...                 confirmed G:0 has THREE columns: C:0 Date (mandatory:true but ALREADY
...                 defaulted/filled on load - no fill needed), C:1 Business Unit dropdown
...                 (mandatory:true, genuinely empty - MandatoryCellStyle, the ONLY field that
...                 needs a fill), C:2 a second dropdown (mandatory:false, optional filter -
...                 GO succeeds with C:2 left empty once C:1 is set). This is the single-dropdown/
...                 same-row-cascade shape Area's pattern supports - exactly ONE genuinely
...                 mandatory+empty field in this one navigator group.
...                 Real labels confirmed live (2026-08-26): objectForm/updateAttributes use
...                 SCREEN-PREFIXED "Transport Zone Code"/"Transport Zone Name" (like Area's
...                 "Area Code"/"Area Name"), NOT the generic "Code"/"Name" Bank/Object List use -
...                 every T2 call below passes code_label=Transport Zone Code accordingly. The
...                 insert form's mandatory "Transport System Name" dropdown (R:5) is bound to
...                 the nav Business Unit scope - "TS5 Transport System" pairs with nav
...                 "TS5 BU" (recon-confirmed, matches the pre-existing driver's proven value).
...                 "Zone Type" (R:2) and "End Date" (R:4) on objectForm are confirmed
...                 mandatory:false - deliberately excluded from the insert data.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${TRNZON_SCREEN}          Transport Zone
${TRNZON_TABLE}           manageObject:form:T_data
${TRNZON_NAVIGATOR_PROPERTIES}    ${CURDIR}/../../../../testdata/transport_zone_navigator.properties
${TRNZON_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/transport_zone_insert.properties
${TRNZON_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/transport_zone_update.properties
${TRNZON_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/transport_zone_form_verify.properties
${TRNZON_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/transport_zone_grid_verify.properties
# objectdates field ID (Delete — End Date = Start Date). Hardcoded deliberately, NOT label-driven -
# this row packs Start Date (C:1) and End Date (C:3) together with the End Date label at C:2, a
# shape the one-field-per-row label scan cannot safely resolve (same rationale as Area/Bank).
# Value confirmed live 2026-08-26.
${TRNZON_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Transport Zone's own form-field label set (Start Date/End Date deliberately excluded - they
# live only in objectdates, not updateAttributes/objectForm's fill-once trio; Transport System
# Name deliberately excluded from round-trip comparison - it's filled via a resolved reference
# value which can re-render different display text after reload, same caveat as every other
# converted screen's dropdown fields).
@{TRNZON_FORM_LABELS}    Transport Zone Code    Transport Zone Name


*** Keywords ***
Find Transport Zone Row By Filter
    [Documentation]    Explicitly filter the Transport Zone grid's Code column to ${code} via the
    ...    shared T2 Find Object Row By Filter (resources/manage_object.resource), matching every
    ...    other Area-pattern-converted screen's explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${TRNZON_TABLE}    ${code}

Clear Transport Zone Row Filter
    [Documentation]    Clear the Code column filter (see Find Transport Zone Row By Filter) via
    ...    the shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${TRNZON_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Transport Zone's OWN credentials
    ...    (${TRANSPORT_ZONE_EC_USER}/${TRANSPORT_ZONE_EC_PASS} from credentials.py) on the
    ...    current page - works whether this is the very first login (page freshly loaded on the
    ...    login form via the shared T1 Open EC Application) or a re-login after Logout From EC
    ...    Application (same login form, not a new page/tab).
    Login To EC Screen    ${TRANSPORT_ZONE_EC_USER}    ${TRANSPORT_ZONE_EC_PASS}

Open Transport Zone Screen With Navigator Values Populated
    [Documentation]    Navigate to the Transport Zone screen, THEN fill + submit the mandatory
    ...    Business Unit navigator (dropdown + GO) - Transport Zone's grid stays empty until this
    ...    happens, so this single keyword bundles both steps for the test case. Assumes the
    ...    caller already logged in this test case (via Login To EC Application). Navigator fill
    ...    delegates to the shared T2 "Apply Navigator From Properties"
    ...    (resources/manage_object.resource), driven by
    ...    testdata/transport_zone_navigator.properties, instead of inlining
    ...    "Select EC Dropdown Option + Apply Navigator" here.
    Open EC Screen    ${TRNZON_SCREEN}
    Apply Navigator From Properties    ${TRNZON_NAVIGATOR_PROPERTIES}

Insert Transport Zone Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Object From Properties And Verify
    ...    Code, called with ZERO arguments so transport_zone_iud.robot's test case body reads as
    ...    a plain business step. Also owns the integrity check that the inserted Transport Zone
    ...    Code matches the suite's ${TEST_CODE}. ${TRNZON_INSERT_PROPERTIES}'s Transport System
    ...    Name value MUST pair with the navigator's own Business Unit value (TS5 BU <->
    ...    TS5 Transport System) or the new row is not visible under this navigator scope
    ...    (OV-GM constraint).
    [Arguments]    ${properties_path}=${TRNZON_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Transport Zone Code
    RETURN    ${code}

Verify Transport Zone Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification (no
    ...    DB check here - that's TC02's own separate DbVerify assertion): row exists in the grid,
    ...    then Transport Zone Code/Transport Zone Name's LIVE SCREEN value is compared to
    ...    testdata/transport_zone_insert.properties. Filters via Find Transport Zone Row By
    ...    Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Transport Zone Row By Filter    ${code}
    Verify Object Insert Exists    ${TRNZON_TABLE}    ${code}    Transport Zone
    ...    ${TRNZON_INSERT_PROPERTIES}    @{TRNZON_FORM_LABELS}    code_label=Transport Zone Code
    Clear Transport Zone Row Filter

Update Transport Zone Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Only
    ...    Transport Zone Name is listed in testdata/transport_zone_update.properties - Transport
    ...    Zone Code is read-only in updateAttributes. Filters via Find Transport Zone Row By
    ...    Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${TRNZON_UPDATE_PROPERTIES}
    Find Transport Zone Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${TRNZON_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Transport Zone Code
    Clear Transport Zone Row Filter
    RETURN    ${data}

Verify Transport Zone Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification:
    ...    selects the row, compares Transport Zone Name's LIVE SCREEN value to
    ...    testdata/transport_zone_update.properties. Filters via Find Transport Zone Row By
    ...    Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Transport Zone Row By Filter    ${code}
    Verify Object Form Record    ${TRNZON_TABLE}    ${code}    Transport Zone
    ...    ${TRNZON_UPDATE_PROPERTIES}    Transport Zone Name    code_label=Transport Zone Code
    Clear Transport Zone Row Filter

Find Transport Zone Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Calls Find
    ...    Transport Zone Row By Filter first. Deliberately does NOT clear the filter afterward -
    ...    Verify Transport Zone Record Found (called right after, same TC) needs the grid still
    ...    filtered to ${code} for its own grid-check; it clears the filter once both checks are
    ...    done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Transport Zone Row By Filter    ${code}
    Find Object Record    ${TRNZON_TABLE}    ${code}    Transport Zone
    ...    code_label=Transport Zone Code

Verify Transport Zone Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND
    ...    the full form record match the expected data. Caller must already have selected the
    ...    row (TC04 does, via Find Transport Zone Record before this) AND left the Code filter
    ...    active - clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${TRNZON_TABLE}    ${code}    ${TRNZON_GRID_VERIFY_PROPERTIES}
    ...    ${TRNZON_FORM_VERIFY_PROPERTIES}    @{TRNZON_FORM_LABELS}
    Clear Transport Zone Row Filter

Delete Transport Zone Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the transport zone, set End Date = Start Date (EC true delete for
    ...    OV_TRANSPORT_ZONE), Save. Filters via Find Transport Zone Row By Filter first, clears
    ...    after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Transport Zone Row By Filter    ${code}
    Delete Object Via End Date    ${TRNZON_TABLE}    ${TRNZON_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Transport Zone Row Filter

Verify Transport Zone Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid AND the database (OV_TRANSPORT_ZONE) - the DB check lives here, in
    ...    the shared T2 Verify Object Removed.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${TRNZON_TABLE}    OV_TRANSPORT_ZONE    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Transport Zone Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification
    ...    (grid-only check) - delegates to the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${TRNZON_TABLE}    ${code}
