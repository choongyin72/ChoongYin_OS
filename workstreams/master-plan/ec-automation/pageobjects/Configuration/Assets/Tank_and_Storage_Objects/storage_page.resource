*** Settings ***
Documentation       T3 (screen) — Storage page object.
...                 Screen: Configuration > Assets > Tank_and_Storage_Objects > Storage (CO.0034).
...                 OV-GM (groupmodel manage-object) screen: the grid loads ONLY after the
...                 mandatory Production Unit -> Area -> Facility Class 1 navigator cascade
...                 (3-level, C:1/C:2/C:3 same row - confirmed live 2026-08-26,
...                 tmp/recon_storage_navigator_cascade.py) is set + GO. Converted to the
...                 Bank-pattern 5-TC/per-TC-login/pure-screen-verify STRUCTURE (owner standing
...                 rule 2026-08-26: any EC screen with a navigator matching Area's layout MUST
...                 follow Area's FULL pattern) - Storage remains OV-GM, its genuine 3-level
...                 PU->Area->Facility Class 1 cascade + GO is KEPT (Apply Navigator From
...                 Properties, EXPLICIT values from testdata/storage_navigator.properties:
...                 Op Production Unit=AS1 EC Exploration Norway, Op Area=AS1_Area, Op Facility
...                 Class 1=AS1_Facility_01 - the same first-available resolution the prior
...                 "Apply OV-GM Navigator First Available" driver already picked, captured here
...                 as explicit values, not re-invented). This is a STRUCTURAL conversion, not a
...                 reclassification of the screen as plain Bank-shaped.
...                 Real labels confirmed live (2026-08-26, objectForm label scan): objectForm/
...                 updateAttributes use SCREEN-PREFIXED "Storage Code"/"Storage Name" (like
...                 Area's "Area Code"/"Area Name"), NOT the generic "Code"/"Name" Bank/Object
...                 List use - every T2 call below passes code_label=Storage Code accordingly.
...                 Grid columns confirmed live (manageObject:form:T_head scan): Storage Code /
...                 Storage Name / Start Date / End Date - same 4-column shape as Area/Facility
...                 Class 1.
...                 objectForm also exposes Storage's own genuine MANDATORY dropdowns "Storage
...                 Type"/"Product Name" (confirmed live + the pre-existing proven driver
...                 py/storage_iud.py, verify_screen PASS 2026-07-30, which fills them) - KEPT as
...                 __FIRST__ in testdata/storage_insert.properties (a supported literal in the
...                 shared T2 properties-fill mechanism), preserving that exact proven handling.
...                 "Op Production Unit"/"Op Area"/"Op Facility Class 1" fields also exist on this
...                 objectForm (confirmed live 2026-08-26), but the already-proven driver inserts
...                 successfully leaving them blank; trusting that proven behavior rather than
...                 hunting for an unstated requirement - they are NOT added to
...                 testdata/storage_insert.properties.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${STORAGE_SCREEN}          Storage
${STORAGE_TABLE}           manageObject:form:T_data
# navigator (groupmodel): Production Unit -> Area -> Facility Class 1 3-level cascade — MANDATORY
# before the grid loads. The fill goes through the shared T2 "Apply Navigator From Properties"
# (resources/manage_object.resource), driven by testdata/storage_navigator.properties.
${STORAGE_NAVIGATOR_PROPERTIES}    ${CURDIR}/../../../../testdata/storage_navigator.properties
${STORAGE_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/storage_insert.properties
${STORAGE_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/storage_update.properties
${STORAGE_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/storage_form_verify.properties
${STORAGE_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/storage_grid_verify.properties
# objectdates field ID (Delete — End Date = Start Date). Hardcoded deliberately, NOT label-driven -
# same documented rationale as Area's/Facility Class 1's own del-enddate constant: this row packs
# Start Date (C:1) and End Date (C:3) together with the End Date label at C:2, a shape the
# one-field-per-row label scan cannot safely resolve. Value confirmed live via the pre-existing
# Playwright driver (py/storage_iud.py: ${DEL_ENDDATE} convention shared across every OV-GM screen).
${STORAGE_DEL_ENDDATE}     tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Storage's own form-field label set (Start Date/End Date deliberately excluded - they live only
# in objectdates, not updateAttributes/objectForm's fill-once trio; Storage Type/Product Name/
# Op Production Unit/Op Area/Op Facility Class 1 deliberately excluded from round-trip comparison -
# filled via __FIRST__/left blank, dropdown display text is not a safe round-trip target, same
# caveat as every other converted screen's dropdown fields).
@{STORAGE_FORM_LABELS}    Storage Code    Storage Name


*** Keywords ***
Find Storage Row By Filter
    [Documentation]    Explicitly filter the Storage grid's Code column to ${code} via the shared
    ...    T2 Find Object Row By Filter (resources/manage_object.resource), matching every other
    ...    Bank-pattern-converted screen's explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${STORAGE_TABLE}    ${code}

Clear Storage Row Filter
    [Documentation]    Clear the Code column filter (see Find Storage Row By Filter) via the
    ...    shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${STORAGE_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Storage's OWN credentials (${STORAGE_EC_USER}/
    ...    ${STORAGE_EC_PASS} from credentials.py) on the current page - works whether this is the
    ...    very first login (page freshly loaded on the login form via the shared T1 Open EC
    ...    Application) or a re-login after Logout From EC Application (same login form, not a
    ...    new page/tab).
    Login To EC Screen    ${STORAGE_EC_USER}    ${STORAGE_EC_PASS}

Open Storage Screen With Navigator Values Populated
    [Documentation]    Navigate to the Storage screen, THEN fill + submit the mandatory 3-level
    ...    Production Unit -> Area -> Facility Class 1 navigator (dropdowns + GO) - the grid stays
    ...    empty until this happens, so this single keyword bundles both steps for the test case
    ...    (Area's/Facility Class 1's exact skeleton calls this as ONE line per TC, not two).
    ...    Assumes the caller already logged in this test case (via Login To EC Application).
    ...    Navigator fill delegates to the shared T2 "Apply Navigator From Properties"
    ...    (resources/manage_object.resource), driven by testdata/storage_navigator.properties.
    Open EC Screen    ${STORAGE_SCREEN}
    Apply Navigator From Properties    ${STORAGE_NAVIGATOR_PROPERTIES}

Insert Storage Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Object From Properties And Verify
    ...    Code, called with ZERO arguments so storage_iud.robot's test case body reads as a plain
    ...    business step. Also owns the integrity check that the inserted Storage Code matches the
    ...    suite's ${TEST_CODE}.
    [Arguments]    ${properties_path}=${STORAGE_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Storage Code
    RETURN    ${code}

Verify Storage Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification (no
    ...    DB check here - that's TC02's own separate DbVerify assertion): row exists in the grid,
    ...    then Storage Code/Storage Name's LIVE SCREEN value is compared to
    ...    testdata/storage_insert.properties. Filters via Find Storage Row By Filter first,
    ...    clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Storage Row By Filter    ${code}
    Verify Object Insert Exists    ${STORAGE_TABLE}    ${code}    Storage    ${STORAGE_INSERT_PROPERTIES}
    ...    @{STORAGE_FORM_LABELS}    code_label=Storage Code
    Clear Storage Row Filter

Update Storage Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Only Storage
    ...    Name is listed in testdata/storage_update.properties - Storage Code is read-only in
    ...    updateAttributes. Filters via Find Storage Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${STORAGE_UPDATE_PROPERTIES}
    Find Storage Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${STORAGE_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Storage Code
    Clear Storage Row Filter
    RETURN    ${data}

Verify Storage Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification:
    ...    selects the row, compares Storage Name's LIVE SCREEN value to
    ...    testdata/storage_update.properties. Filters via Find Storage Row By Filter first,
    ...    clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Storage Row By Filter    ${code}
    Verify Object Form Record    ${STORAGE_TABLE}    ${code}    Storage    ${STORAGE_UPDATE_PROPERTIES}
    ...    Storage Name    code_label=Storage Code
    Clear Storage Row Filter

Find Storage Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Calls Find Storage
    ...    Row By Filter first. Deliberately does NOT clear the filter afterward - Verify Storage
    ...    Record Found (called right after, same TC) needs the grid still filtered to ${code}
    ...    for its own grid-check; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Storage Row By Filter    ${code}
    Find Object Record    ${STORAGE_TABLE}    ${code}    Storage    code_label=Storage Code

Verify Storage Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND
    ...    the full form record match the expected data. Caller must already have selected the
    ...    row (TC04 does, via Find Storage Record before this) AND left the Code filter active -
    ...    clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${STORAGE_TABLE}    ${code}    ${STORAGE_GRID_VERIFY_PROPERTIES}
    ...    ${STORAGE_FORM_VERIFY_PROPERTIES}    @{STORAGE_FORM_LABELS}
    Clear Storage Row Filter

Delete Storage Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the storage, set End Date = Start Date (EC true delete for OV_STORAGE), Save.
    ...    Versioned groupmodel grids redraw lazily after a delete - Save And Refresh List (inside
    ...    T2) already re-applies the navigator, so the assertion reads a fresh list. Filters via
    ...    Find Storage Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Storage Row By Filter    ${code}
    Delete Object Via End Date    ${STORAGE_TABLE}    ${STORAGE_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Storage Row Filter

Verify Storage Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid AND the database (OV_STORAGE) - the DB check lives here, in the
    ...    shared T2 Verify Object Removed, NOT as a separate screen-local wrapper keyword.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${STORAGE_TABLE}    OV_STORAGE    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Storage Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification
    ...    (grid-only check) - delegates to the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${STORAGE_TABLE}    ${code}
