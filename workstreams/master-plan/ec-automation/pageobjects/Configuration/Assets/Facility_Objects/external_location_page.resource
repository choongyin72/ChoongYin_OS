*** Settings ***
Documentation       T3 (screen) — External Location page object.
...                 Screen: Configuration > Assets > Facility Objects > External Location.
...                 OV-GM (groupmodel manage-object) screen, but UNLIKE Area/Well/Test
...                 Separator/Chemical Tank: the grid loads on GO ALONE - the navigator has NO
...                 mandatory scope, its fields are optional filters only (confirmed live,
...                 ec-ui-knowledge/screens/external_location.md + docs/ec_screen_registry.md).
...                 Converted to the Bank-pattern 5-TC/per-TC-login/pure-screen-verify STRUCTURE
...                 (owner standing rule 2026-08-26: any EC screen with a navigator section,
...                 matching Area's screen layout, follows Area's FULL pattern - not just the
...                 navigator-fill piece PR #524/this-branch already did). External Location's
...                 genuine GO-only/no-mandatory-nav-scope behavior is KEPT EXACTLY as-is - this
...                 conversion is about STRUCTURE only (TC count/login-per-TC/verification-style/
...                 properties-driven/filter-wiring), same caveat as Area's own conversion
...                 documented 2026-08-25. Real labels confirmed (ec-ui-knowledge/screens/
...                 external_location.md, live-verified 2026-08-01/2026-08-26): objectForm/
...                 updateAttributes use SCREEN-PREFIXED "External Location Code"/"External
...                 Location Name" (like Area's "Area Code"/"Area Name"), NOT the generic
...                 "Code"/"Name" Bank/Object List use - every T2 call below passes
...                 code_label=External Location Code accordingly.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${EL_SCREEN}            External Location
${EL_TABLE}             manageObject:form:T_data
# objectdates field ID (Delete — End Date = Start Date). Hardcoded deliberately, NOT
# label-driven - same documented rationale as Area's ${AREA_DEL_ENDDATE}/Bank's
# ${BANK_DEL_ENDDATE}: this row packs Start Date (C:1) and End Date (C:3) together with the End
# Date label at C:2, a shape the one-field-per-row label scan cannot safely resolve. Value
# confirmed live via this screen's own pre-existing suite (unchanged since PR #295).
${EL_DEL_ENDDATE}       tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# 2026-08-26 (PR #524, this branch): navigator fill delegates to the shared T2 "Apply Navigator
# From Properties" driven by an INTENTIONALLY EMPTY testdata/external_location_navigator.properties
# (see that file's own header) - zero data lines -> zero fills -> falls straight through to GO
# alone, i.e. the exact same behavior this screen always had. Kept UNCHANGED by this structural
# conversion.
${EL_NAVIGATOR_PROPERTIES}    ${CURDIR}/../../../../testdata/external_location_navigator.properties
${EL_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/external_location_insert.properties
${EL_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/external_location_update.properties
${EL_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/external_location_form_verify.properties
${EL_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/external_location_grid_verify.properties
# External Location's own form-field label set (Start Date deliberately excluded - it lives only
# in objectdates, not updateAttributes/objectForm's fill-once trio, same as Area).
@{EL_FORM_LABELS}    External Location Code    External Location Name


*** Keywords ***
Find External Location Row By Filter
    [Documentation]    Explicitly filter the External Location grid's Code column to ${code} via
    ...    the shared T2 Find Object Row By Filter (resources/manage_object.resource), matching
    ...    every other Bank-pattern-converted screen's explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${EL_TABLE}    ${code}

Clear External Location Row Filter
    [Documentation]    Clear the Code column filter (see Find External Location Row By Filter)
    ...    via the shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${EL_TABLE}

Login To EC Application
    [Documentation]    Authenticate as External Location's OWN credentials
    ...    (${EXTERNAL_LOCATION_EC_USER}/${EXTERNAL_LOCATION_EC_PASS} from credentials.py) on the
    ...    current page - works whether this is the very first login (page freshly loaded on the
    ...    login form via the shared T1 Open EC Application) or a re-login after Logout From EC
    ...    Application (same login form, not a new page/tab).
    Login To EC Screen    ${EXTERNAL_LOCATION_EC_USER}    ${EXTERNAL_LOCATION_EC_PASS}

Open External Location Screen With Navigator Values Populated
    [Documentation]    Navigate to the External Location screen, THEN submit the navigator (GO
    ...    alone - no mandatory scope on this screen, fields are optional filters only). Named to
    ...    match Area's/every other converted OV-GM screen's "Open <Screen> Screen With Navigator
    ...    Values Populated" convention even though there is genuinely no value to populate here -
    ...    keeps the TEST CASE call shape identical across every converted screen regardless of
    ...    whether that screen's own navigator is mandatory-scoped or GO-only. Assumes the caller
    ...    already logged in this test case (via Login To EC Application). Navigator fill
    ...    delegates to the shared T2 "Apply Navigator From Properties" (resources/
    ...    manage_object.resource) driven by the intentionally-empty
    ...    testdata/external_location_navigator.properties (PR #524/this branch, UNCHANGED by
    ...    this structural conversion) - zero data lines -> zero fills -> GO alone.
    Open EC Screen    ${EL_SCREEN}
    Apply Navigator From Properties    ${EL_NAVIGATOR_PROPERTIES}

Insert External Location Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Object From Properties And Verify
    ...    Code, called with ZERO arguments so external_location_iud.robot's test case body reads
    ...    as a plain business step. Also owns the integrity check that the inserted External
    ...    Location Code matches the suite's ${TEST_CODE}. No navigator scope requirement here
    ...    (GO-only screen) - unlike Area, there is no "must equal the nav scope" constraint on
    ...    the inserted row's visibility.
    [Arguments]    ${properties_path}=${EL_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=External Location Code
    RETURN    ${code}

Verify External Location Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification (no
    ...    DB check here - DB ground-truth is out-of-band self-clean/evidence only, never an
    ...    in-test assertion): row exists in the grid, then External Location Code/External
    ...    Location Name's LIVE SCREEN value is compared to
    ...    testdata/external_location_insert.properties. Filters via Find External Location Row
    ...    By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find External Location Row By Filter    ${code}
    Verify Object Insert Exists    ${EL_TABLE}    ${code}    External Location
    ...    ${EL_INSERT_PROPERTIES}    @{EL_FORM_LABELS}    code_label=External Location Code
    Clear External Location Row Filter

Update External Location Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Only
    ...    External Location Name is listed in testdata/external_location_update.properties -
    ...    External Location Code is read-only in updateAttributes and External Location has no
    ...    Description field (confirmed via ec-ui-knowledge/screens/external_location.md's
    ...    updateAttributes field list). Filters via Find External Location Row By Filter first,
    ...    clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${EL_UPDATE_PROPERTIES}
    Find External Location Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${EL_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=External Location Code
    Clear External Location Row Filter
    RETURN    ${data}

Verify External Location Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification:
    ...    selects the row, compares External Location Name's LIVE SCREEN value to
    ...    testdata/external_location_update.properties. Filters via Find External Location Row
    ...    By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find External Location Row By Filter    ${code}
    Verify Object Form Record    ${EL_TABLE}    ${code}    External Location
    ...    ${EL_UPDATE_PROPERTIES}    External Location Name    code_label=External Location Code
    Clear External Location Row Filter

Find External Location Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Calls Find External
    ...    Location Row By Filter first. Deliberately does NOT clear the filter afterward - Verify
    ...    External Location Record Found (called right after, same TC) needs the grid still
    ...    filtered to ${code} for its own grid-check; it clears the filter once both checks are
    ...    done.
    [Arguments]    ${code}=${TEST_CODE}
    Find External Location Row By Filter    ${code}
    Find Object Record    ${EL_TABLE}    ${code}    External Location
    ...    code_label=External Location Code

Verify External Location Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND
    ...    the full form record match the expected data. Caller must already have selected the
    ...    row (TC04 does, via Find External Location Record before this) AND left the Code
    ...    filter active - clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${EL_TABLE}    ${code}    ${EL_GRID_VERIFY_PROPERTIES}
    ...    ${EL_FORM_VERIFY_PROPERTIES}    @{EL_FORM_LABELS}
    Clear External Location Row Filter

Delete External Location Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the External Location, set End Date = Start Date (EC true delete for
    ...    OV_EXTERNAL_LOCATION), Save. Versioned groupmodel grids redraw lazily after a delete -
    ...    Save And Refresh List (inside T2) already re-applies the navigator, so the assertion
    ...    reads a fresh list. Filters via Find External Location Row By Filter first, clears
    ...    after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find External Location Row By Filter    ${code}
    Delete Object Via End Date    ${EL_TABLE}    ${EL_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear External Location Row Filter

Verify External Location Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid AND the database (OV_EXTERNAL_LOCATION) - the DB check lives here,
    ...    in the shared T2 Verify Object Removed, NOT as a separate screen-local wrapper keyword
    ...    (that pattern was removed by this conversion - see Documentation above).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${EL_TABLE}    OV_EXTERNAL_LOCATION    ${code}
    Capture Step    ${TEST NAME}_verify

Verify External Location Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification
    ...    (grid-only check) - delegates to the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${EL_TABLE}    ${code}
