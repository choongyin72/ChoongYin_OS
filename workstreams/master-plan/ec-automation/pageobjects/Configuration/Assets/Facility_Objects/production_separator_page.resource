*** Settings ***
Documentation       T3 (screen) — Production Separator page object.
...                 Screen: Configuration > Assets > Facility_Objects > Production Separator.
...                 OV-GM (groupmodel manage-object) screen: the grid loads ONLY after the
...                 mandatory Production Unit -> Area -> Facility Class 1 navigator cascade
...                 (3-level, C:1/C:2/C:3 same row, C:4 absent - confirmed live 2026-08-26 via
...                 tmp/recon_psep_navigator.py) is set + GO. Converted to the Bank-pattern 5-TC/
...                 per-TC-login/pure-screen-verify STRUCTURE (owner standing rule 2026-08-26: any
...                 EC screen with a navigator matching Area's layout MUST follow Area's FULL
...                 pattern) - Production Separator remains OV-GM, its genuine 3-level PU->Area->
...                 Facility Class 1 cascade + GO is KEPT, now filled via Apply Navigator From
...                 Properties with EXPLICIT values (testdata/production_separator_navigator.properties:
...                 Op Production Unit=AS1 EC Exploration Norway, Op Area=AS1_Area, Op Facility
...                 Class 1=AS1_Facility_01 - the SAME values the prior "First Available" cascade
...                 already resolved to live, captured explicitly rather than re-invented). This
...                 is a STRUCTURAL conversion, not a reclassification of the screen as plain
...                 Bank-shaped.
...                 Real labels confirmed live (2026-08-26, objectForm label scan): objectForm/
...                 updateAttributes use SCREEN-PREFIXED "Production Separator Code"/"Production
...                 Separator Name" (like Area's "Area Code"/"Area Name"), NOT the generic
...                 "Code"/"Name" Bank/Object List use - every T2 call below passes
...                 code_label=Production Separator Code accordingly. Grid columns confirmed live
...                 (manageObject:form:T_head scan): Production Separator Code / Production
...                 Separator Name / Start Date / End Date - same 4-column shape as Area/Facility
...                 Class 1.
...                 objectForm exposes many extra fields (Sort Order, Meter Frequency, Op
...                 Area/Op Facility Class 1, Cp Production Unit, Geo Area/Geo Field, etc. -
...                 confirmed live 2026-08-26) but the already-proven driver
...                 (py/production_separator_iud.py, verify_screen PASS 2026-07-30, RF 4/4 +
...                 Playwright 8/8, still passing) inserts successfully filling only Code/Name/
...                 Start Date/Op Production Unit; trusting that proven behavior rather than
...                 hunting for an unstated requirement - the rest are NOT added to
...                 testdata/production_separator_insert.properties.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${PSEP_SCREEN}          Production Separator
${PSEP_TABLE}            manageObject:form:T_data
# navigator (groupmodel): Production Unit -> Area -> Facility Class 1 3-level cascade — MANDATORY
# before the grid loads. The fill goes through the shared T2 "Apply Navigator From Properties"
# (resources/manage_object.resource), driven by testdata/production_separator_navigator.properties.
${PSEP_NAVIGATOR_PROPERTIES}    ${CURDIR}/../../../../testdata/production_separator_navigator.properties
${PSEP_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/production_separator_insert.properties
${PSEP_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/production_separator_update.properties
${PSEP_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/production_separator_form_verify.properties
${PSEP_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/production_separator_grid_verify.properties
# objectdates field ID (Delete — End Date = Start Date). Hardcoded deliberately, NOT label-driven -
# same documented rationale as Area's/Facility Class 1's own del-enddate constant: this row packs
# Start Date (C:1) and End Date (C:3) together with the End Date label at C:2, a shape the
# one-field-per-row label scan cannot safely resolve. Value confirmed live via the pre-existing
# resource file's own ${DEL_ENDDATE} constant (unchanged by this conversion).
${PSEP_DEL_ENDDATE}      tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Production Separator's own form-field label set (Start Date/End Date deliberately excluded -
# they live only in objectdates, not updateAttributes/objectForm's fill-once trio; Op Production
# Unit deliberately excluded from round-trip comparison - it's filled via a resolved reference
# value which can re-render different display text after reload, same caveat as every other
# converted screen's dropdown fields).
@{PSEP_FORM_LABELS}    Production Separator Code    Production Separator Name


*** Keywords ***
Find Production Separator Row By Filter
    [Documentation]    Explicitly filter the Production Separator grid's Code column to ${code}
    ...    via the shared T2 Find Object Row By Filter (resources/manage_object.resource),
    ...    matching every other Bank-pattern-converted screen's explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${PSEP_TABLE}    ${code}

Clear Production Separator Row Filter
    [Documentation]    Clear the Code column filter (see Find Production Separator Row By Filter)
    ...    via the shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${PSEP_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Production Separator's OWN credentials
    ...    (${PRODUCTION_SEPARATOR_EC_USER}/${PRODUCTION_SEPARATOR_EC_PASS} from credentials.py)
    ...    on the current page - works whether this is the very first login (page freshly loaded
    ...    on the login form via the shared T1 Open EC Application) or a re-login after Logout
    ...    From EC Application (same login form, not a new page/tab).
    Login To EC Screen    ${PRODUCTION_SEPARATOR_EC_USER}    ${PRODUCTION_SEPARATOR_EC_PASS}

Open Production Separator Screen With Navigator Values Populated
    [Documentation]    Navigate to the Production Separator screen, THEN fill + submit the
    ...    mandatory 3-level Production Unit -> Area -> Facility Class 1 navigator (dropdowns +
    ...    GO) - the grid stays empty until this happens, so this single keyword bundles both
    ...    steps for the test case (Area's exact skeleton calls this as ONE line per TC, not two).
    ...    Assumes the caller already logged in this test case (via Login To EC Application).
    ...    Navigator fill delegates to the shared T2 "Apply Navigator From Properties"
    ...    (resources/manage_object.resource), driven by
    ...    testdata/production_separator_navigator.properties.
    Open EC Screen    ${PSEP_SCREEN}
    Apply Navigator From Properties    ${PSEP_NAVIGATOR_PROPERTIES}

Insert Production Separator Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Object From Properties And Verify
    ...    Code, called with ZERO arguments so production_separator_iud.robot's test case body
    ...    reads as a plain business step. Also owns the integrity check that the inserted
    ...    Production Separator Code matches the suite's ${TEST_CODE}.
    ...    ${PSEP_INSERT_PROPERTIES}'s Op Production Unit value MUST equal the navigator's own
    ...    C:1 value or the new row is not visible under this navigator scope (OV-GM constraint).
    [Arguments]    ${properties_path}=${PSEP_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Production Separator Code
    RETURN    ${code}

Verify Production Separator Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification (no
    ...    DB check here - that's TC02's own separate DbVerify assertion): row exists in the grid,
    ...    then Production Separator Code/Production Separator Name's LIVE SCREEN value is
    ...    compared to testdata/production_separator_insert.properties. Filters via Find
    ...    Production Separator Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Production Separator Row By Filter    ${code}
    Verify Object Insert Exists    ${PSEP_TABLE}    ${code}    Production Separator
    ...    ${PSEP_INSERT_PROPERTIES}    @{PSEP_FORM_LABELS}    code_label=Production Separator Code
    Clear Production Separator Row Filter

Update Production Separator Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Only
    ...    Production Separator Name is listed in testdata/production_separator_update.properties -
    ...    Production Separator Code is read-only in updateAttributes. Filters via Find
    ...    Production Separator Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${PSEP_UPDATE_PROPERTIES}
    Find Production Separator Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${PSEP_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Production Separator Code
    Clear Production Separator Row Filter
    RETURN    ${data}

Verify Production Separator Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification:
    ...    selects the row, compares Production Separator Name's LIVE SCREEN value to
    ...    testdata/production_separator_update.properties. Filters via Find Production Separator
    ...    Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Production Separator Row By Filter    ${code}
    Verify Object Form Record    ${PSEP_TABLE}    ${code}    Production Separator
    ...    ${PSEP_UPDATE_PROPERTIES}    Production Separator Name    code_label=Production Separator Code
    Clear Production Separator Row Filter

Find Production Separator Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Calls Find
    ...    Production Separator Row By Filter first. Deliberately does NOT clear the filter
    ...    afterward - Verify Production Separator Record Found (called right after, same TC)
    ...    needs the grid still filtered to ${code} for its own grid-check; it clears the filter
    ...    once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Production Separator Row By Filter    ${code}
    Find Object Record    ${PSEP_TABLE}    ${code}    Production Separator
    ...    code_label=Production Separator Code

Verify Production Separator Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND
    ...    the full form record match the expected data. Caller must already have selected the
    ...    row (TC04 does, via Find Production Separator Record before this) AND left the Code
    ...    filter active - clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${PSEP_TABLE}    ${code}    ${PSEP_GRID_VERIFY_PROPERTIES}
    ...    ${PSEP_FORM_VERIFY_PROPERTIES}    @{PSEP_FORM_LABELS}
    Clear Production Separator Row Filter

Delete Production Separator Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the object, set End Date = Start Date (EC true delete for OV_PRODSEPARATOR),
    ...    Save. Versioned groupmodel grids redraw lazily after a delete - Save And Refresh List
    ...    (inside T2) already re-applies the navigator, so the assertion reads a fresh list.
    ...    Filters via Find Production Separator Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Production Separator Row By Filter    ${code}
    Delete Object Via End Date    ${PSEP_TABLE}    ${PSEP_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Production Separator Row Filter

Verify Production Separator Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid and the database (OV_PRODSEPARATOR) - the DB check lives here, in
    ...    the shared T2 Verify Object Removed, NOT as a separate screen-local wrapper keyword.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${PSEP_TABLE}    OV_PRODSEPARATOR    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Production Separator Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification
    ...    (grid-only check) - delegates to the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${PSEP_TABLE}    ${code}
