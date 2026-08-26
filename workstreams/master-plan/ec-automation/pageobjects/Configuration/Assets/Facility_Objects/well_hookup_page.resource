*** Settings ***
Documentation       T3 (screen) — Well Hookup page object.
...                 Screen: Configuration > Assets > Facility_Objects > Well Hookup (CO.0108).
...                 OV-GM (groupmodel manage-object) screen: the grid loads ONLY after the
...                 mandatory Production Unit -> Area -> Facility Class 1 navigator cascade
...                 (3-level, C:1/C:2/C:3 same row, C:4 absent - confirmed live 2026-08-26 via
...                 tmp/recon_well_hookup_navigator_cascade.py) is set + GO. Converted to the
...                 Area-pattern 5-TC/per-TC-login/pure-screen-verify STRUCTURE (owner standing
...                 rule 2026-08-26: any EC screen with a navigator matching Area's layout MUST
...                 follow Area's FULL pattern, not just the navigator-fill piece) - Well Hookup
...                 remains OV-GM, its genuine 3-level PU->Area->Facility Class 1 cascade + GO is
...                 KEPT exactly as the prior build proved it (now via Apply Navigator From
...                 Properties, EXPLICIT values from testdata/well_hookup_navigator.properties:
...                 Op Production Unit=AS1 EC Exploration Norway, Op Area=AS1_Area, Op Facility
...                 Class 1=AS1_Facility_01 - the SAME first-available resolution the old
...                 "Apply OV-GM Navigator First Available" cascade already used successfully,
...                 verify_screen PASS + RF 4/4 + Playwright 8/8, 2026-07-30). This is a
...                 STRUCTURAL conversion, not a reclassification of the screen as plain
...                 Bank/Area-shaped.
...                 Real labels reused from the already-proven driver (py/well_hookup_iud.py,
...                 pageobjects' prior Insert Well Hookup Record): objectForm/updateAttributes
...                 use SCREEN-PREFIXED "Well Hookup Code"/"Well Hookup Name" (like Area's "Area
...                 Code"/"Area Name"), NOT the generic "Code"/"Name" Bank/Object List use - every
...                 T2 call below passes code_label=Well Hookup Code accordingly. Grid columns
...                 confirmed live (manageObject:form:T_head scan, 2026-08-26): Well Hookup Code /
...                 Well Hookup Name / Start Date / End Date - same 4-column shape as Area/
...                 Facility Class 1.
...                 objectForm's "Op Production Unit" dropdown IS filled at Insert (the already-
...                 proven driver treats it as mandatory and always fills it __FIRST__) - kept as
...                 an insert field in testdata/well_hookup_insert.properties, but EXCLUDED from
...                 @WH_FORM_LABELS below (its value is a fill directive, not a comparable screen
...                 value).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${WH_SCREEN}            Well Hookup
${WH_TABLE}              manageObject:form:T_data
# navigator (groupmodel): Production Unit -> Area -> Facility Class 1, 3-level cascade — MANDATORY
# before the grid loads. The fill goes through the shared T2 "Apply Navigator From Properties"
# (resources/manage_object.resource), driven by testdata/well_hookup_navigator.properties.
${WH_NAVIGATOR_PROPERTIES}    ${CURDIR}/../../../../testdata/well_hookup_navigator.properties
${WH_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/well_hookup_insert.properties
${WH_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/well_hookup_update.properties
${WH_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/well_hookup_form_verify.properties
${WH_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/well_hookup_grid_verify.properties
# objectdates field ID (Delete — End Date = Start Date). Hardcoded deliberately, NOT label-driven -
# same documented rationale as Area's/Facility Class 1's own del-enddate constant: this row packs
# Start Date (C:1) and End Date (C:3) together with the End Date label at C:2, a shape the
# one-field-per-row label scan cannot safely resolve. Value confirmed live via the pre-existing
# Playwright driver (py/well_hookup_iud.py: DEL_ENDDATE convention shared across every OV-GM
# screen).
${WH_DEL_ENDDATE}        tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Well Hookup's own form-field label set (Start Date deliberately excluded - lives only in
# objectdates, not updateAttributes/objectForm's fill-once trio; Op Production Unit deliberately
# excluded - its insert value is "__FIRST__", a fill directive not a comparable screen value; see
# Documentation above).
@{WH_FORM_LABELS}       Well Hookup Code    Well Hookup Name


*** Keywords ***
Find Well Hookup Row By Filter
    [Documentation]    Explicitly filter the Well Hookup grid's Code column to ${code} via
    ...    the shared T2 Find Object Row By Filter (resources/manage_object.resource), matching
    ...    every other Area-pattern-converted screen's explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${WH_TABLE}    ${code}

Clear Well Hookup Row Filter
    [Documentation]    Clear the Code column filter (see Find Well Hookup Row By Filter) via
    ...    the shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${WH_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Well Hookup's OWN credentials
    ...    (${WELL_HOOKUP_EC_USER}/${WELL_HOOKUP_EC_PASS} from credentials.py) on the
    ...    current page - works whether this is the very first login (page freshly loaded on the
    ...    login form via the shared T1 Open EC Application) or a re-login after Logout From EC
    ...    Application (same login form, not a new page/tab).
    Login To EC Screen    ${WELL_HOOKUP_EC_USER}    ${WELL_HOOKUP_EC_PASS}

Open Well Hookup Screen With Navigator Values Populated
    [Documentation]    Navigate to the Well Hookup screen, THEN fill + submit the mandatory
    ...    3-level Production Unit -> Area -> Facility Class 1 navigator (dropdowns + GO) - the
    ...    grid stays empty until this happens, so this single keyword bundles both steps for the
    ...    test case (Area's exact skeleton calls this as ONE line per TC, not two). Assumes the
    ...    caller already logged in this test case (via Login To EC Application). Navigator fill
    ...    delegates to the shared T2 "Apply Navigator From Properties"
    ...    (resources/manage_object.resource), driven by
    ...    testdata/well_hookup_navigator.properties.
    Open EC Screen    ${WH_SCREEN}
    Apply Navigator From Properties    ${WH_NAVIGATOR_PROPERTIES}

Insert Well Hookup Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Object From Properties And Verify
    ...    Code, called with ZERO arguments so well_hookup_iud.robot's test case body reads as a
    ...    plain business step. Also owns the integrity check that the inserted Well Hookup Code
    ...    matches the suite's ${TEST_CODE}.
    [Arguments]    ${properties_path}=${WH_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Well Hookup Code
    RETURN    ${code}

Verify Well Hookup Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification (no
    ...    DB check here - that's TC02's own separate DbVerify assertion): row exists in the grid,
    ...    then Well Hookup Code/Well Hookup Name's LIVE SCREEN value is compared to
    ...    testdata/well_hookup_insert.properties. Filters via Find Well Hookup Row By Filter
    ...    first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Well Hookup Row By Filter    ${code}
    Verify Object Insert Exists    ${WH_TABLE}    ${code}    Well Hookup
    ...    ${WH_INSERT_PROPERTIES}    @{WH_FORM_LABELS}    code_label=Well Hookup Code
    Clear Well Hookup Row Filter

Update Well Hookup Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Only Well
    ...    Hookup Name is listed in testdata/well_hookup_update.properties - Well Hookup Code is
    ...    read-only in updateAttributes. Filters via Find Well Hookup Row By Filter first, clears
    ...    after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${WH_UPDATE_PROPERTIES}
    Find Well Hookup Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${WH_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Well Hookup Code
    Clear Well Hookup Row Filter
    RETURN    ${data}

Verify Well Hookup Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification:
    ...    selects the row, compares Well Hookup Name's LIVE SCREEN value to
    ...    testdata/well_hookup_update.properties. Filters via Find Well Hookup Row By Filter
    ...    first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Well Hookup Row By Filter    ${code}
    Verify Object Form Record    ${WH_TABLE}    ${code}    Well Hookup
    ...    ${WH_UPDATE_PROPERTIES}    Well Hookup Name    code_label=Well Hookup Code
    Clear Well Hookup Row Filter

Find Well Hookup Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Calls Find Well
    ...    Hookup Row By Filter first. Deliberately does NOT clear the filter afterward - Verify
    ...    Well Hookup Record Found (called right after, same TC) needs the grid still filtered
    ...    to ${code} for its own grid-check; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Well Hookup Row By Filter    ${code}
    Find Object Record    ${WH_TABLE}    ${code}    Well Hookup    code_label=Well Hookup Code

Verify Well Hookup Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND
    ...    the full form record match the expected data. Caller must already have selected the
    ...    row (TC04 does, via Find Well Hookup Record before this) AND left the Code filter
    ...    active - clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${WH_TABLE}    ${code}    ${WH_GRID_VERIFY_PROPERTIES}
    ...    ${WH_FORM_VERIFY_PROPERTIES}    @{WH_FORM_LABELS}
    Clear Well Hookup Row Filter

Delete Well Hookup Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the object, set End Date = Start Date (EC true delete for OV_WELL_HOOKUP), Save.
    ...    Versioned groupmodel grids redraw lazily after a delete - Save And Refresh List (inside
    ...    T2) already re-applies the navigator, so the assertion reads a fresh list. Filters via
    ...    Find Well Hookup Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Well Hookup Row By Filter    ${code}
    Delete Object Via End Date    ${WH_TABLE}    ${WH_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Well Hookup Row Filter

Verify Well Hookup Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid and the database (OV_WELL_HOOKUP) - the DB check lives here, in the
    ...    shared T2 Verify Object Removed, NOT as a separate screen-local wrapper keyword.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${WH_TABLE}    OV_WELL_HOOKUP    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Well Hookup Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification
    ...    (grid-only check) - delegates to the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${WH_TABLE}    ${code}
